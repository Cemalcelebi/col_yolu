# DOSYA KAPISI: İZLEME LİSTESİ (PNLSN, FORTE, GWIND, YEOTK), KAP birincil kaynak, 16 Kasım 2026

> Bu bir bulgu tablosudur. Hiçbir satır 'al' ya da 'öneri' değildir. ÖLÇÜLMÜŞ SİNYAL YOK: BIST'te ölçülmüş bir iz yok; 'sıkı dosya' (YEOTK profili) K57 / K57-B / K57-C'de ön kayıtlı testte İZ DEĞİL çıktı.
> Taban oranlar (ONERI_DEFTERI risk süzgeci, ABD 2012-2026, yalnız yaşayan şirketler): 12 ayda ikiye katlanma %4-7, yarıya inme %6-7. Oynak havuzda ikiye katlanma %9-16, yarıya inme %17-21; tipik sonuç eksidir. 3 yılda 10x: ABD mikro-cap yaklaşık %1, BIST USD yaklaşık %1,85.
> Claude yatırım danışmanı değildir. Alım-satım kararı Cemal'indir.

Kaynak: kap.org.tr. Bildirim listesi `api/disclosure/members/byCriteria` ile 16.11.2025 - 16.11.2026 arası iki sorguyla tarandı (PNLSN 101, FORTE 143, GWIND 89, YEOTK 162 satır). Bildirim sayfaları `/tr/Bildirim/<no>`, ekler `api/file/download/<id>`, ortaklık tablosu `/tr/sirket-bilgileri/genel/<şirket>`. Finansal tablolar sayfadaki XBRL satırlarından okundu. Sütun sırası sayfa başlığından doğrulandı: 9A26, 9A25, 3Ç26, 3Ç25.
Bilgi tarihi: kullanılan en geç bildirim 13.11.2026 (MKK 1698076). Her sayının yanında bildirimin "Gönderim Tarihi" yazılıdır; sayfa tarihi kullanılmadı. Fiyatlar Yahoo günlük verisinden okundu (scratchpad/canli/bist_3y.pkl, karar günü 13.11.2026 kapanışı). 16.11.2026 barı gün içi olabilir; yalnız bilgi olarak kullanıldı.
Tutarlar: 3Ç26 finansal raporları TMS 29 enflasyon düzeltmeli (30.09.2026 satın alma gücü), yani 3Ç25 / 9A25 karşılaştırmaları reeldir. Hepsi mn TL'ye çevrildi; rapor birimi TL.
Bilanço günü tepkisi: bildirim seans sonrası geldiği için tepki günü bir sonraki işlem günüdür. r = kapanış / önceki kapanış - 1; hacim oranı = o günün hacmi / önceki 20 gün ortalaması; evren = 587 BIST hissesinin aynı gün medyanı.

## Kapı kuralı (DOSYA_2026-11-16.md ile aynı uygulama tanımı; sonuç görülmeden kopyalandı)
- GEÇTİ: gerçek gelir VAR, 3Ç26 ivme POZİTİF, nakit seyrelmesi YOK ve leke YOK. Biri eksikse GEÇMEDİ; kaynak bulunamadıysa BELİRSİZ.
- 3Ç26 ivme pozitif: 3Ç26 satış > 3Ç25 satış VE 3Ç26 net kâr (ana ortaklık payı) > 3Ç25 net kâr (zararın daralması dahil).
- Nakit seyrelmesi: son 12 ayda gerçekleşen bedelli ya da tahsisli sermaye artırımı. Bedelsiz sayılmaz.
- Leke: SPK tedbiri / suç duyurusu, kayyım / TMSF, tasfiye fonu ortaklığı, yürürlükteki brüt takas / açığa satış yasağı / VBTS, MSCI çıkarma, going concern ya da şartlı / olumsuz denetim görüşü. MKK "SPK İşlem Yasağı Nedeniyle Pay Duyurusu" yasaklı YATIRIMCININ elindeki payı gösterir; leke sayılmaz.
- Bayraklar: zarar eden (9A26 net kâr < 0), nakit yakan (9A26 faaliyet nakit akışı < 0), hisse ihraç eden, bedelli, raf benzeri (12 ayda kayıtlı sermaye tavanı artırımı), zirveden en uzak / en küçük / en düşük fiyat (tarama evreninin, 586 hisse, alt %20'si; 'en küçük' için 20 gün işlem değeri vekil), ters bölünme, ortak satışı (12 ayda hakim ya da büyük ortak satışı).
- Koruma: kârlı (9A26 > 0), seyreltmeyen, bilanço tepkisi iyi (tepki günü r > 0), likit (20 gün işlem değeri evrenin üst yarısında).

## ÖZET

| Aday | DOSYA kapısı | Bayrak | Koruma | Tek satır neden |
|---|---|---|---|---|
| PNLSN | GEÇTİ | 1 | 3 | 3Ç26 satış +%30,5, net kâr +%39,0; seyrelme ve leke yok. Uyarılar: faaliyet nakdi 9A -242,9 mn, sözleşmeler isimsiz, likidite düşük, bilanço tavanı kilitli ve hacimsiz |
| FORTE | GEÇMEDİ (mekanik) | 2 | 4 | 3Ç26 satış +%267, faaliyet kârı -43,5'ten 657,6 mn'ye; ama ana ortaklık 3Ç kârı 2.413,6'dan 337,4 mn'ye indi (3Ç25'te 2.137,7 mn parasal kazanç vardı). Kurucular Mart-Eylül'de yaklaşık %5,1 sattı |
| GWIND | GEÇMEDİ | 1 | 4 | 3Ç26 satış -%29,3, net kâr -%17,4. 9A kârı +%130 ama kaynağı 1.386,6 mn ertelenmiş vergi geliri. Nakit 1.475,8'den 400,8 mn'ye indi, CEO 27.10'da ayrıldı |
| YEOTK | GEÇMEDİ (mekanik) | 0 | 4 | 3Ç26 satış +%17,7, faaliyet kârı +%39,9, konsolide kâr +%39,5; ama ana ortaklık 3Ç kârı 1.055,1'den 826,6 mn'ye indi (-%21,7; azınlık payı). Net borç / özkaynak 0,76. Tasfiye fonu payı %0,003 (şirket açıklaması) |

- GEÇTİ olan tek aday PNLSN. Bu yalnız DOSYA kapısıdır. Öneri için TARAMA (ölçülmüş sinyal YOK) ve RİSK kapıları da gerekir; PNLSN bu hâliyle 'izleme'dir.
- FORTE ve YEOTK kâr satırı yüzünden düştü, faaliyet yüzünden değil. Kural ana ortaklık payının 3Ç kârını okuyor. FORTE'de baz çeyrekte tek seferlik parasal kazanç var. YEOTK'de azınlık payının 3Ç25'te -205,9 mn zarar, 3Ç26'da +357,9 mn kâr yazması ana ortaklık payını düşürdü. Kural sonuç görülmeden yazıldığı için değiştirilmedi. Kâr satırının yerine faaliyet kârı ya da konsolide kâr okunsun mu, kararı ana modelindir (HATA 2).

---

## 1. PNLSN: Panelsan Çatı Cephe Sistemleri (sandviç panel, taş yünü, çatı ve cephe sistemleri; GES yatırımları)

| Kalem | Değer | Kaynak (KAP bildirim tarihi, başlık, no) |
|---|---|---|
| 3Ç26 bilanço | 06.11.2026 18:11 (konsolide) | 06.11.2026 Finansal Rapor 1694037 |
| Satış 9A26 / 9A25 | 3.258,0 / 2.646,0 mn TL (+%23,1) | 1694037 |
| Satış 3Ç26 / 3Ç25 | 1.296,3 / 993,1 mn TL (+%30,5) | 1694037 |
| Esas faaliyet kârı 3Ç26 / 3Ç25 (9A26 / 9A25) | 204,9 / 132,1 mn TL (390,1 / 216,7) | 1694037 |
| Net kâr (ana ortaklık = toplam) 9A26 / 9A25 | 146,1 / 108,2 mn TL (+%35,0) | 1694037 |
| Net kâr 3Ç26 / 3Ç25 | 126,9 / 91,3 mn TL (+%39,0) | 1694037 |
| Nakit (30.09.2026 / 31.12.2025) | 283,3 / 262,5 mn TL | 1694037 |
| Borçlanma: KV / UV'nin KV kısmı / UV | 416,4 / 39,4 / 91,9 mn TL (31.12.2025: 1,1 / 127,4 / 0). UV kısmın tamamı ilişkili taraflardan | 1694037 |
| Özkaynak; net borç / özkaynak | 3.803,3 mn TL; 264,4 mn → 0,07 | 1694037 (hesap) |
| Faaliyet nakit akışı 9A26 / 9A25 | -242,9 / +3,6 mn TL. Stok 622,1 → 781,9; ticari alacak 1.441,5 → 1.608,1 | 1694037 |
| Yatırım harcaması 9A26 | -154,6 mn TL | 1694037 |
| Sermaye / seyrelme | 75 mn TL, değişmedi. 12 ayda bedelli, tahsisli ya da ihraç bulunamadı. Kayıtlı tavan artırımı bildirimi bulunamadı. Pay geri alım programı 02.12.2025'te bitti (azami 2,5 mn nominal, %3,33) | 1694037; 03.12.2025 Pay Geri Alım Programının Sona Ermesi 1522866 |
| Ortaklık | Maşlak Holding %45,53 (oy %62,04); KAP tablosundaki tarih 29.07.2023 (bayat). Azimut Portföy'ün kurucusu olduğu fonlar (Erciyes Hisse Senedi Serbest Özel Fon dahil) yaklaşık %20: 06.01.2026 alış 194.094 → %20,14; 21.01 satış 54.094 → %19,99; 18.02 alış 200.000 → %20,07; 15.04 satış 200.000 (44,16 TL) → %19,80. Fiili dolaşım %25,09 (15.11.2026) | KAP şirket sayfası; 07.01.2026 1535018, 22.01.2026 1545949, 19.02.2026 1559347, 16.04.2026 1594428 (Azimut Pay Alım Satım Bildirimi, PDF ek) |
| Sözleşme / katalizör | 17.11.2025: 87,5 mn TL sipariş (Niğde merkezli özel firma, isim yok). 06.04.2026: 3,10 mn USD sipariş (Ankara merkezli özel firma, isim yok). Elazığ GES 2.015 kW işletmeye alındı, toplam GES 4.140 kW (09.11.2026). BIST Katılım Temettü ve Katılım Tüm endekslerine alındı (01.10.2026) | 17.11.2025 Yeni İş İlişkisi 1517348; 06.04.2026 Yeni İş İlişkisi 1584825; 09.11.2026 Elazığ GES Yatırımı 1695732; 29.09.2026 BIST Katılım Endeksleri 1669816 |
| Kâr payı | 2025 için nakit; 9A26'da 53,5 mn TL ödendi | 12.05.2026 Kar Payı Dağıtım İşlemleri 1606181; 1694037 |
| Denetim görüşü 2025 | Güncel Bağımsız Denetim, OLUMLU. Dikkat çekilen husus yalnız TMS 29 (rutin). Süreklilik belirsizliği yok | 25.02.2026 Finansal Rapor (yıllık) 1561484 |
| Lekeler | Şirket tedbiri, VBTS, kayyım, TMSF ya da MSCI bildirimi bulunamadı. Şirket 30.09.2026'da tasfiye edilen fonlarla idari, ticari ya da ortaklık ilişkisi olmadığını açıkladı. Fon tablosu (K25, Eylül raporları): tasfiye fonu pozisyonu 0 | 30.09.2026 Kamuoyu ve Yatırımcılarımıza Duyuru 1669956; G.pkl (en geç bilinme 12.10.2026) |
| Bilanço günü tepkisi | 09.11.2026: +%10,0 (tavan, açılış = kapanış 30,58-30,60), hacim 0,39x, evren medyanı +%1,9. 10.11: +%10,0 kilitli tavan (O=H=L=C 33,66), hacim 0,79x. 3 gün (06.11 → 11.11): +%16,5, evren -%0,9 | Yahoo |

Bayraklar (1): nakit yakan EVET (9A26 faaliyet nakdi -242,9 mn). Zarar, ihraç, bedelli, raf, ters bölünme ve ortak satışı HAYIR (Azimut fonları 12 ayda net +140.000 lot alıcı; hakim ortak satışı bulunamadı). Zirveden uzaklık -%40,9 (evren yüzdeliği 0,72), likidite yüzdeliği 0,27, fiyat yüzdeliği 0,69; hiçbiri alt %20'de değil.
Koruma (3): kârlı, seyreltmeyen, bilanço tepkisi iyi. Likit değil: 20 gün işlem değeri 11,7 mn TL, yüzdelik 0,27.
DOSYA kapısı: GEÇTİ.
Düz dil: Panelsan gerçek bir sanayi işi; 3. çeyrekte satış %30, kâr %39 arttı ve hisse ihracı yok. Zayıf yanları şunlar: büyüme stok ve alacakla finanse ediliyor, faaliyetten nakit çıkıyor (-243 mn) ve kısa vadeli banka borcu 1'den 416 mn TL'ye çıktı (borç hâlâ özkaynağa göre küçük, 0,07). KAP'taki sözleşmeler müşteri adı vermiyor. Sermayenin yaklaşık %20'si tek bir portföy yöneticisinin fonlarında; bu fonlar %20 sınırında alıp satıyor. Bilanço günü fiyat iki gün tavan oldu ama ilk gün hacim normalin %39'uydu (kilitli tavan; gerçek alıcı derinliği ölçülmedi, K3).

## 2. FORTE: Forte Bilgi İletişim Teknolojileri ve Savunma Sanayi (BT / siber güvenlik donanım-yazılım, kamu ihaleleri; %100 bağlı ortaklık Milsoft savunma yazılımı)

| Kalem | Değer | Kaynak |
|---|---|---|
| 3Ç26 bilanço | 06.11.2026 18:16 (konsolide) | 06.11.2026 Finansal Rapor 1694174 |
| Satış 9A26 / 9A25 | 4.820,4 / 1.444,6 mn TL (+%233,7) | 1694174 |
| Satış 3Ç26 / 3Ç25 | 2.613,6 / 712,5 mn TL (+%266,8) | 1694174 |
| Esas faaliyet kârı 3Ç26 / 3Ç25 (9A26 / 9A25) | 657,6 / -43,5 mn TL (981,0 / -17,1) | 1694174 |
| Net kâr (ana ortaklık) 9A26 / 9A25 | 562,4 / 2.336,2 mn TL (-%75,9) | 1694174 |
| Net kâr (ana ortaklık) 3Ç26 / 3Ç25 | 337,4 / 2.413,6 mn TL (-%86,0) | 1694174 |
| 3Ç25 kârının kaynağı | 3Ç25 vergi öncesi kâr 2.415,0 mn. Bunun 2.137,7 mn'si net parasal pozisyon kazancı, 541,1 mn'si yatırım faaliyet geliri; esas faaliyet -43,5 mn. 9A25 yatırım faaliyet geliri 2.709,1 mn | 1694174 |
| Nakit (30.09.2026 / 31.12.2025) | 819,3 / 503,1 mn TL | 1694174 |
| Borçlanma: KV / UV'nin KV kısmı / UV | 452,9 / 655,1 / 1.647,0 mn TL (toplam 2.755,0; 31.12.2025: 2.240,1) | 1694174 |
| Özkaynak; net borç / özkaynak | 3.643,1 mn TL; 1.935,7 mn → 0,53 | 1694174 (hesap) |
| Faaliyet nakit akışı 9A26 / 9A25 | +267,8 / +370,0 mn TL. Stok 1.058,2 → 2.340,2; ticari alacak 978,1 → 1.509,7; finansman gideri 9A26 880,1 mn | 1694174 |
| Sermaye / seyrelme | 67 mn TL, değişmedi; 12 ayda bedelli veya tahsisli bulunamadı. Kayıtlı tavan 225 → 335 mn TL (2026-2030; GK onayı 29.06.2026). Borçlanma aracı ihraç tavanı 1.000 mn TL için SPK başvurusu (05.10.2026); önceki tavandan ihraç yapılmadı | 03.04.2026 KSS Tavan SPK Başvurusu 1583999; 14.05.2026 Ticaret Bakanlığı Onayı 1607325; 29.06.2026 GK Kabulü 1621587; 30.09.2026 1670422; 05.10.2026 İhraç Tavanı SPK Başvurusu 1672578 |
| Ortak satışı | Kurucular Mart 2026'da 2.000.000'er lot (toplam 6 mn) borsada işlem gören tipe dönüştürdü. Satışlar: Ebubekir Balıkçı 2.000.000 lot (03.04-26.08; %14,36 → %11,79), Hasan Cengiz Bayrak 772.000 lot (28.08-02.09; %23,63 → %23,03), Ali Celal Asiltürk 641.210 lot (11.03-02.09; %27,73 → %27,25). Toplam 3.413.210 lot, sermayenin yaklaşık %5,1'i; fiyat aralığı 90-143,80 TL. Alıcı tarafta: AK Portföy fonları 01.10.2026'da 198.006 lot aldı (fiili dolaşımda %3,27) | 02.03.2026 Dönüşüm 1563677; 04.03.2026 Dönüşüm 1565758; MKK Pay Alım Satım Bildirimleri 1583278, 1584250, 1585307, 1594496, 1595086, 1602907, 1605922, 1654282, 1654667, 1655182, 1656014, 1656550, 1657745, 1657751 (PDF ekler); 05.10.2026 AK Portföy 1672404 |
| Ortaklık (05.09.2026) | Asiltürk %27,25, Bayrak %23,03, Balıkçı %11,79, diğer %37,93. Fiili dolaşım %37,32 (15.11.2026) | KAP şirket sayfası |
| Sözleşme / katalizör (Ağu-Kas 2026) | DMO veri depolama 124,5 mn TL, sözleşme imzalandı (10.08). Kamu kurumu bilişim güvenliği 29,96 mn TL (04.08). Savunma kamu kuruluşu siparişi 43,45 mn TL (26.08). Milsoft savunma siparişleri 745.000 USD (15.09) ve 700.000 USD (28.09). AFAD malzeme ihalesi 31,9 mn TL (23.09). MEB laboratuvar modernizasyonu ihalesi 49,1 mn TL (02.10). Savunma donanımı 621.000 USD, teslim 30.11.2026 (26.10). Savunma alıcılarının adı yok. Cetwell sermaye artırımına katılım ve Techfor unvan / sermaye değişikliği (09.10). BIST 500 ve Katılım 100'e alındı (10.09) | 1646198; 1642664; 1655096; 1662639; 1668772; 1667023; 1671316; 1687223; 1678460; 1678462; 09.09.2026 Endeks Şirketlerinde Değişiklik 1661014 |
| Denetim görüşü 2025 | Eren Bağımsız Denetim, OLUMLU. Dikkat çekilen husus yok, süreklilik belirsizliği yok | 27.02.2026 Finansal Rapor (yıllık) 1562943 |
| Lekeler | Şirket tedbiri, VBTS, kayyım, TMSF ya da MSCI bildirimi bulunamadı. MKK yasaklı yatırımcı listesinde 6 TL nominal (yatırımcı düzeyi). Fon tablosu Eylül: tasfiye fonu 0 | 11.11.2026 SPK İşlem Yasağı Nedeniyle Pay Duyurusu 1697234; G.pkl |
| Bilanço günü tepkisi | 09.11.2026: +%10,0 (tavan 88,05), hacim 0,68x, evren medyanı +%1,9. 10.11: -%1,4, hacim 2,66x. 3 gün (06.11 → 11.11): +%6,8, evren -%0,9 | Yahoo |

Bayraklar (2): ortak satışı EVET (üç kurucu yaklaşık %5,1 sattı); raf benzeri EVET (kayıtlı tavan 335 mn TL, sermayenin 5 katı). Zarar, nakit yakma, ihraç, bedelli ve ters bölünme HAYIR. Zirveden uzaklık -%35,0 (yüzdelik 0,80), likidite 0,69, fiyat 0,85.
Koruma (4): kârlı, seyreltmeyen, bilanço tepkisi iyi, likit.
DOSYA kapısı: GEÇMEDİ (mekanik: ana ortaklık 3Ç kârı -%86). Faaliyet tarafında ivme çok güçlü.
Düz dil: Forte'nin satışı bir yılda üç buçuk katına çıktı ve esas faaliyet zarardan 658 mn TL kâra döndü. Kâr satırının düşmesinin nedeni, geçen yılın 3. çeyreğinde 2,1 mlr TL'lik muhasebe kaynaklı parasal kazancın olmasıdır. Sözleşmeler kamu ve savunma kaynaklı; DMO, MEB ve AFAD isimli, savunma alıcıları isimsiz. Kaygı verenler: büyüme stok (2,3 mlr TL) ve borçla taşınıyor, finansman gideri 9 ayda 880 mn TL. Üç kurucu Mart-Eylül 2026'da, fiyat 90-144 TL iken, sermayenin yaklaşık %5'ini sattı ('Uzak' sinyali).

## 3. GWIND: Galata Wind Enerji (Doğan Holding %70; RES / GES elektrik üretimi)

| Kalem | Değer | Kaynak |
|---|---|---|
| 3Ç26 bilanço | 03.11.2026 18:24 (konsolide) | 03.11.2026 Finansal Rapor 1691851 |
| Satış 9A26 / 9A25 | 2.037,7 / 2.895,1 mn TL (-%29,6) | 1691851 |
| Satış 3Ç26 / 3Ç25 | 868,6 / 1.229,2 mn TL (-%29,3) | 1691851 |
| Esas faaliyet kârı 3Ç26 / 3Ç25 | 463,5 / 707,1 mn TL | 1691851 |
| Net kâr 9A26 / 9A25 | 2.189,2 / 953,5 mn TL (+%129,6). 9A26'da 1.386,6 mn ertelenmiş vergi GELİRİ var; vergi öncesi kâr 837,7 / 1.530,9 | 1691851 |
| Net kâr 3Ç26 / 3Ç25 | 312,6 / 378,4 mn TL (-%17,4) | 1691851 |
| Nakit (30.09.2026 / 31.12.2025) | 400,8 / 1.475,8 mn TL | 1691851 |
| Borçlanma: UV'nin KV kısmı / UV | 835,5 / 2.363,4 mn TL (31.12.2025: 880,1 / 3.263,0); KV banka borcu yok | 1691851 |
| Özkaynak; net borç / özkaynak | 19.284,7 mn TL; 2.798,2 mn → 0,15 | 1691851 (hesap) |
| Faaliyet nakit akışı 9A26 / 9A25 | +737,4 / +1.783,5 mn TL. Yatırım harcaması -1.623,7 mn; ödenen kâr payı 433,7 mn (özkaynak tablosu) | 1691851 |
| Sermaye / seyrelme | 540 mn TL, değişmedi. Kayıtlı tavan 1.000 → 5.000 mn TL (2026-2030; SPK onayı 06.03, GK 02.04, tescil 24.04.2026). Pay geri alımı: 05.05.2026'ya kadar 970.810 pay (%0,18) | 03.03.2026 Kayıtlı Sermaye Tavanı Tadili 1565242; 1567668; 02.04.2026 1583156; 24.04.2026 1597124; 24.03.2026 Pay Geri Alım Programı 1575256; 05.05.2026 Geri Alım İşlemleri 1601346 |
| Kâr payı | 2025 için brüt 0,7407 TL / pay; ödeme en geç 31.12.2026 | 02.04.2026 Kar Dağıtımı GK Kararı 1583162 |
| Ortaklık | Doğan Şirketler Grubu Holding %70 (KAP tablosundaki tarih 02.08.2023). Fiili dolaşım %29,62 (15.11.2026). 12 ayda ortak satışı bildirimi bulunamadı | KAP şirket sayfası |
| Sözleşme / katalizör | Ağu-Kas 2026 arasında isimli sözleşme ya da yeni iş bildirimi YOK. BIST 100'e alındı (01.10-31.12.2026). CEO Burak Kuyan ayrıldı; vekil Mehmet Ali Gürpınar (27.10.2026) | 21.09.2026 BIST Pay Endeksleri 1666347; 27.10.2026 Üst Yönetim Değişikliği 1688318 |
| Denetim görüşü 2025 | DRT, OLUMLU. Dikkat çekilen husus yok | 26.02.2026 Finansal Rapor (yıllık) 1562171 |
| Lekeler | Şirket tedbiri, VBTS, kayyım ya da TMSF bulunamadı. MKK yasaklı yatırımcı listelerinde 519 TL, 1.000 TL, 0,274 TL ve 1 TL nominal (yatırımcı düzeyi). Fon tablosu: Haziran 238.129 lot, Temmuz 104.629 lot (tasfiye şirketi fonları), Ağustos-Eylül 0. 17.12.2025 'MSCI' bildirimi ESG derecelendirmesidir, endeks değil | 21.09.2026 1666319; 01.10.2026 1671000; 27.10.2026 1688483; 11.11.2026 1697234; G.pkl; 17.12.2025 MSCI Provisional ESG Derecelendirmesi 1527239 |
| Bilanço günü tepkisi | 04.11.2026: +%6,0, hacim 2,47x; evren medyanı aynı gün +%5,2 (piyasa geneli yükseldi). 3 gün (03.11 → 06.11): +%6,5, evren +%7,7 | Yahoo |

Bayraklar (1): raf benzeri EVET (kayıtlı tavan 5.000 mn TL, sermayenin 9,3 katı). Diğerleri HAYIR. Zirveden uzaklık -%39,3 (yüzdelik 0,74), likidite 0,60, fiyat 0,61.
Koruma (4): kârlı, seyreltmeyen (geri alım yaptı), bilanço tepkisi r > 0 (piyasa ile aynı), likit.
DOSYA kapısı: GEÇMEDİ (3Ç26 satış -%29, net kâr -%17).
Düz dil: Galata Wind sağlam bilançolu bir üretici: borç özkaynağın %15'i, denetim temiz, temettü dağıtıyor. Ama bu yıl üretim geliri yaklaşık %30 düştü. 9 aylık kârın ikiye katlanmış görünmesi, tek seferlik ertelenmiş vergi gelirinden geliyor. Nakit 1,48 mlr TL'den 0,40 mlr TL'ye indi (yatırım, borç ödemesi, temettü). CEO Ekim sonunda ayrıldı ve yeni sözleşme bildirimi yok. Bilanço günü yükseliş piyasanın kendi yükselişinden ayrışmıyor.

## 4. YEOTK: YEO Teknoloji Enerji ve Endüstri (enerji EPC: GES, batarya depolama, trafo merkezi; yurt dışı projeler; Reap batarya üretimi)

| Kalem | Değer | Kaynak |
|---|---|---|
| 3Ç26 bilanço | 05.11.2026 22:51 (konsolide) | 05.11.2026 Finansal Rapor 1693502 |
| Satış 9A26 / 9A25 | 17.504,9 / 13.329,4 mn TL (+%31,3) | 1693502 |
| Satış 3Ç26 / 3Ç25 | 8.728,6 / 7.413,6 mn TL (+%17,7) | 1693502 |
| Brüt kâr 3Ç26 / 3Ç25 | 2.225,9 / 1.779,7 mn TL | 1693502 |
| Esas faaliyet kârı 3Ç26 / 3Ç25 (9A26 / 9A25) | 1.963,3 / 1.403,3 mn TL, +%39,9 (3.822,8 / 2.149,3) | 1693502 |
| Dönem kârı (konsolide) 3Ç26 / 3Ç25 | 1.184,5 / 849,2 mn TL (+%39,5) | 1693502 |
| Net kâr (ana ortaklık) 9A26 / 9A25 | 1.533,6 / 934,3 mn TL (+%64,1) | 1693502 |
| Net kâr (ana ortaklık) 3Ç26 / 3Ç25 | 826,6 / 1.055,1 mn TL (-%21,7). Azınlık payı 3Ç26 +357,9, 3Ç25 -205,9 mn | 1693502 |
| Nakit (30.09.2026 / 31.12.2025) | 2.124,9 / 2.351,2 mn TL | 1693502 |
| Borçlanma: KV / UV'nin KV kısmı / UV | 1.936,4 / 2.514,1 / 3.263,7 mn TL (toplam 7.714,2; 31.12.2025: 8.827,9) | 1693502 |
| Özkaynak; net borç / özkaynak | Toplam 7.372,9 mn (ana ortaklık 6.486,6); net borç 5.589,3 mn → 0,76. Toplam yükümlülük 30.090,8 mn = özkaynağın 4,1 katı | 1693502 (hesap) |
| Faaliyet nakit akışı 9A26 / 9A25 | +3.309,7 / -846,9 mn TL. Yatırım harcaması -3.839,6 mn; finansman gideri 9A26 2.895,5 mn | 1693502 |
| Sermaye / seyrelme | Bedelsiz %133,80: 355 → 830 mn TL, iç kaynaktan (nakit seyrelmesi değil); SPK onayı 23.07, tescil 06.08.2026. 12 ayda bedelli veya tahsisli bulunamadı. Borçlanma: Eurobond tavanı 300 mn USD için SPK başvurusu (19.08.2026). TRFYEOTK2616 bonosunun 247 mn TL'si erken itfa edildi (23.10.2026) | 13.05.2026 Bedelsiz SPK Başvurusu 1606952; 24.07.2026 Bedelsiz SPK Onayı 1636665; 06.08.2026 Tescil ve İlan 1644640; 19.08.2026 Yurt Dışında Borçlanma Aracı İhracı 1652898; 23.10.2026 Finansman Bonosunun Erken İtfası 1686873 |
| Ortaklık (05.08.2026) | Orhan Yıldız %13,89 (oy %14,87), Tolunay Yıldız %13,89 (oy %32,42), Özbey Yıldız %13,89 (oy %14,86); Sinan Karahan, Yasin Düven ve Barış Esen %6,37'şer; diğer %39,22. Fiili dolaşım %36,20 (15.11.2026). Ağustos MKK %5 bildirimlerindeki oran değişimi bedelsiz geçişinden geliyor, satış değil. 12 ayda hakim ortak satışı bulunamadı. Dönüşüm başvurusu: Sezai Bekgöz 20.774 TL nominal (29.09.2026) | KAP şirket sayfası; 03.08.2026 MKK 12-(4) 1641869 ve 05.08.2026 1643245 (PDF ek); 29.09.2026 Dönüşüm 1669632 |
| Sözleşme / katalizör (Ağu-Kas 2026) | Azerenerji 250 MWh BESS, EPC-F 58,6 mn USD (21.09); finansman PAŞA Bank ile, kredi kullandırıldı (20.10). Azerenerji Nahçıvan 40 MWh BESS 9,54 mn USD (28.08). Enda Enerji ile Romanya 54 MWp GES + 80 MWh BESS: CEISD izin başvurusu yapıldı, SPA sürüyor (24.08). Intelligent Industries LLC'nin %50'si 115.255 USD'ye satıldı (26.08). Daha önce: Zambiya 60 MWp GES + 20 MWh, ZESCO'ya 20 yıl USD tarifeli, finansman tamam (27.02.2026). ARC Clean Technology yatırımı (22.12.2025) | 21.09.2026 Yeni İş İlişkisi 1665639; 20.10.2026 1684214; 28.08.2026 1655524; 24.08.2026 İşbirliği ve Ortaklık 1654336; 26.08.2026 Finansal Duran Varlık Satışı 1655239; 27.02.2026 Finansal Kapanış 1562351; 22.12.2025 İştirak alımı 1528311 |
| Endeks / pazar | BIST 100'den çıkarıldı (01.04.2026); 3Ç26'da BIST 100 yedeği. Yıldız Pazar'dan Ana Pazar'a geçti (01.10.2026). BIST Katılım 30'un çıkarılacaklar listesinde (01.10.2026 - 30.04.2027) | 19.03.2026 BIST Pay Endeksleri 1574461; 19.06.2026 1619135; 30.09.2026 Endeks Şirketlerinde Değişiklik 1670215; 29.09.2026 1669816 (PDF ekler) |
| Denetim görüşü 2025 | Güreli YMM ve Bağımsız Denetim, OLUMLU. Dikkat çekilen husus yok, süreklilik belirsizliği yok | 10.03.2026 Finansal Rapor (yıllık) 1569760 |
| Lekeler | Şirket tedbiri, VBTS, kayyım ya da TMSF bulunamadı. MKK yasaklı yatırımcı listelerinde 9.650,849 TL, 0,194 TL ve 15.864,928 TL nominal (yatırımcı düzeyi). Tasfiye fonu: aşağıdaki ayrı bölüm | 21.09.2026 1666319; 01.10.2026 1671000; 21.10.2026 1685308 |
| Bilanço günü tepkisi | 06.11.2026: +%9,95 (tavan 25,64), hacim 0,48x, evren medyanı +%1,0. 09.11: +%10,0, hacim 1,98x. 3 gün (05.11 → 10.11): +%20,1, evren +%1,5 | Yahoo |

### YEOTK fon durumu (Cemal pozisyonda)
- ŞİRKETİN KENDİ AÇIKLAMASI (22.09.2026 09:00, "Yatırım Fonlarının Şirketimiz Paylarındaki Pozisyonlarına İlişkin Kamuoyu Bilgilendirmesi", 1666364): KAP ve TEFAS'taki en güncel portföy bilgilerine göre tasfiyeye giren fonlardan yalnız 1 tanesinin portföyünde YEOTK var: 27.001 lot, sermayenin %0,003'ü. Fonun adı verilmedi.
- K25 FON TABLOSU (G.pkl, 30.09.2026 ay sonu raporları, KAP'a 02-07.10.2026'da geldi): tasfiye şirketlerinin 5 fonunda toplam 683.502 lot (830 mn sermayenin %0,082'si).
  - Bulls Portföy Atak Değişken Fon (BAG) 238.500,75 lot (02.10.2026, 1671285).
  - Bulls Portföy Çoklu Varlık Katılım Fonu (BCO) 115.000 lot (1671288).
  - Bulls Portföy Hisse Senedi (TL) Fonu (BHA) 205.000 lot (1671291).
  - A1 Capital Portföy Çoklu Varlık Katılım Fonu (CVL) 125.001,41 lot (07.10.2026, 1674183).
  - Pardus Portföy Birinci Değişken Fon (BHF) 0,32 lot (1674245).
- BU 5 FON TASFİYEDE Mİ: KAP rapor sayfalarında 'tasfiye' ibaresi yok. SPK'nın 131 fonluk tasfiye listesinde bu beş fonun adı geçmiyor. Liste ikincil kaynaktan, cnbce.com 17.09.2026 haberinden kontrol edildi; Bulls'un 15, A1 Capital'in 9 fonu listede var ama bu adlar yok. SPK bülteni ayrıca okunmadı. Yani K25 tablosundaki 683.502 lotluk 'leke', fon yöneticisinin ADINA göre işaretlenmiş (FI_TASFIYE_RE); bu fonların kendisi tasfiyede görünmüyor (HATA 1).
- Ek bilgi (ikincil kaynak, KAP değil): Bulls Portföy 18.10.2026'da tasfiye kapsamındaki 15 fonunun tasfiyesinin tamamlandığını duyurdu (cnbce.com, Bulls'un X paylaşımına dayanıyor).
- Fon yöneticisi iştiraki: YEOTK'nin %3 üstü ortakları 6 gerçek kişi. Ortaklık tablosunda portföy yönetim şirketi ya da fon yok.
- Sonuç: tasfiyedeki fon payı şirket açıklamasına göre %0,003. Tasfiyede olmayan ama sorunlu yöneticilerin fonlarındaki pay Eylül sonunda %0,082. İkisi de fiili dolaşımın (%36,2) yanında çok küçük. Leke sayılmadı. Ekim-Kasım fon portföy raporları okunmadı; güncel lot bilinmiyor.

Bayraklar (0): zarar, nakit yakma, ihraç (bedelsiz sayılmaz), bedelli, raf (kayıtlı tavan değişikliği bulunamadı), ters bölünme ve ortak satışı HAYIR. Zirveden uzaklık -%46,8 (yüzdelik 0,63), likidite 0,89, fiyat 0,67. Listede olmayan risk: yükümlülük / özkaynak 4,1 ve finansman gideri 9 ayda 2,9 mlr TL.
Koruma (4): kârlı, seyreltmeyen, bilanço tepkisi iyi, likit.
DOSYA kapısı: GEÇMEDİ (mekanik: ana ortaklık 3Ç kârı -%21,7). Satış, faaliyet kârı ve konsolide kâr ivmesi pozitif.
Düz dil: YEO'nun işi büyüyor: 3. çeyrekte satış %18, faaliyet kârı %40, toplam kâr %40 arttı. Faaliyetten 9 ayda 3,3 mlr TL nakit girdi (geçen yıl -0,85 mlr). Kapı, kârın ortaklara düşen kısmı 3Ç25'e göre düştüğü için kapandı: geçen yıl bağlı ortaklıklardaki azınlık zararı ana şirkete yazılmıştı, bu yıl azınlık kârlı. İsimli ve büyük sözleşmeler var: Azerbaycan 58,6 + 9,5 mn USD, finansmanı sağlanmış. Riskler şunlar: borç yükü (net borç 5,6 mlr TL, yükümlülükler özkaynağın 4 katı); BIST 100 ve Yıldız Pazar'dan çıkış (endeks fonu talebi düştü); bilanço günü ilk tavanın hacimsiz olması. Tasfiye fonu riski, şirketin açıkladığı rakamla ihmal edilebilir düzeyde.

---

## KAYNAK LİSTESİ (KAP bildirim tarihi, başlık, no)

PNLSN: 06.11.2026 Finansal Rapor 3Ç26 (1694037); 06.11.2026 Faaliyet Raporu (1694050); 25.02.2026 Finansal Rapor 2025 yıllık (1561484); 03.12.2025 Pay Geri Alım Programının Sona Ermesi (1522866); 07.01.2026, 22.01.2026, 19.02.2026, 16.04.2026 Azimut Pay Alım Satım Bildirimi (1535018, 1545949, 1559347, 1594428; PDF ekler); 17.11.2025 Yeni İş İlişkisi (1517348); 06.04.2026 Yeni İş İlişkisi (1584825); 03.07.2026, 14.08.2026, 09.11.2026 Elazığ GES (1623894, 1650210, 1695732); 30.09.2026 Kamuoyu ve Yatırımcılarımıza Duyuru (1669956); 12.05.2026 Kar Payı (1606181); 11.12.2025 İştirak Genel Kurulu (1526071); 29.09.2026 BIST Katılım Endeksleri (1669816); KAP şirket genel bilgi sayfası (ortaklık, fiili dolaşım 15.11.2026).
FORTE: 06.11.2026 Finansal Rapor 3Ç26 (1694174); 27.02.2026 Finansal Rapor 2025 yıllık (1562943); 02.03.2026 ve 04.03.2026 Dönüşüm Duyurusu (1563677, 1565758); MKK Pay Alım Satım Bildirimleri 03.04-03.09.2026 (1583278, 1584250, 1585307, 1594496, 1595086, 1602907, 1605922, 1654282, 1654667, 1655182, 1656014, 1656550, 1657745, 1657751; PDF ekler); 05.10.2026 AK Portföy Pay Alım Satım (1672404); 03.04.2026, 14.05.2026, 29.06.2026 Kayıtlı Sermaye Tavanı (1583999, 1607325, 1621587); 30.09.2026 ve 05.10.2026 İhraç Tavanı (1670422, 1672578); 04.08.2026 (1642664); 10.08.2026 DMO (1646198); 26.08.2026 (1655096); 15.09.2026 (1662639); 23.09.2026 AFAD (1667023); 28.09.2026 (1668772); 02.10.2026 MEB (1671316); 09.10.2026 Cetwell / Techfor (1678460, 1678462); 26.10.2026 (1687223); 08.09.2026 FDPO (1659988); 09.09.2026 Endeks Değişikliği (1661014); 11.11.2026 SPK İşlem Yasağı (1697234); KAP şirket sayfası.
GWIND: 03.11.2026 Finansal Rapor 3Ç26 (1691851); 26.02.2026 Finansal Rapor 2025 yıllık (1562171); 03.03.2026, 06.03.2026, 02.04.2026, 24.04.2026 Kayıtlı Sermaye Tavanı (1565242, 1567668, 1583156, 1597124); 24.03.2026 Pay Geri Alım Programı (1575256); 05.05.2026 Geri Alım İşlemleri (1601346); 02.04.2026 Kar Dağıtımı GK Kararı (1583162); 21.09.2026 BIST Pay Endeksleri (1666347, PDF ek); 27.10.2026 Üst Yönetim Değişikliği (1688318); 17.12.2025 MSCI ESG (1527239); 21.09.2026, 01.10.2026, 27.10.2026, 11.11.2026 SPK İşlem Yasağı (1666319, 1671000, 1688483, 1697234); KAP şirket sayfası.
YEOTK: 05.11.2026 Finansal Rapor 3Ç26 (1693502); 10.03.2026 Finansal Rapor 2025 yıllık (1569760); 22.09.2026 Yatırım Fonlarının Şirketimiz Paylarındaki Pozisyonlarına İlişkin Kamuoyu Bilgilendirmesi (1666364); 17.03.2026, 13.05.2026, 24.07.2026, 06.08.2026 bedelsiz (1573672, 1606952, 1636665, 1644640); 03.08.2026 ve 05.08.2026 MKK 12-(4) (1641869, 1643245; PDF ekler); 19.08.2026 Eurobond tavanı (1652898); 24.08.2026 Enda (1654336); 26.08.2026 Finansal Duran Varlık Satışı (1655239); 28.08.2026 Nahçıvan (1655524); 11.09.2026 Geleceğe Dönük Değerlendirmeler (1661745); 21.09.2026 Azerenerji (1665639); 20.10.2026 Azerbaycan Finansmanı (1684214); 23.10.2026 Bono Erken İtfası (1686873, 1686130); 29.09.2026 Dönüşüm (1669632); 19.03.2026, 19.06.2026, 29.09.2026, 30.09.2026 endeks / pazar (1574461, 1619135, 1669816, 1670215; PDF ekler); 27.02.2026 Finansal Kapanış (1562351); 22.12.2025 İştirak alımı (1528311); 30.12.2025 Kredi kullanımı (1530860); 01.04.2026 MKK Pay Alım Satım (İbrahim Cura, 571 TL; 1582047); 21.09.2026, 01.10.2026, 21.10.2026 SPK İşlem Yasağı (1666319, 1671000, 1685308); fon portföy raporları 30.09.2026: BAG 1671285, BCO 1671288, BHA 1671291 (02.10.2026), CVL 1674183, BHF 1674245 (07.10.2026); KAP şirket sayfası.
KAP dışı: Yahoo günlük fiyat (scratchpad/canli/bist_3y.pkl, 13.11.2026'ya kadar); arastirma_cikti/oneri/bist_tarama_2026-11-16.csv (yüzdelikler, leke sütunu); K25 fon tablosu scratchpad/veri/G.pkl (KAP aylık portföy raporları, en geç bilinme 12.10.2026). İkincil (yalnız ipucu): cnbce.com 17.09.2026 "Hangi fonlar kapatıldı? İşte TEFAS'ta tasfiye edilecek fonların tam listesi" (https://www.cnbce.com/yatirim/hangi-fonlar-kapatildi-iste-tefasta-tasfiye-edilecek-fonlarin-tam-listesi-h37433); cnbce.com 18.10.2026 "Bulls Portföy'den 5,3 milyar liralık tasfiye açıklaması" (https://www.cnbce.com/borsa/bulls-portfoyden-53-milyar-liralik-tasfiye-aciklamasi-h39710).

Erişilemeyen / okunmayan:
- SPK haftalık bültenleri ve SPK'nın 131 fonluk tasfiye kararının asıl metni okunmadı (fon listesi ikincil kaynaktan).
- Ekim-Kasım 2026 fon portföy raporları (tasfiye fonlarının haftalık raporları dahil) okunmadı.
- YEOTK 22.09 açıklamasındaki tek tasfiye fonunun adı bilinmiyor.
- Okunmayan PDF ekler: yatırımcı sunumları (PNLSN 1697667, GWIND 1691875, YEOTK 1661745) ve JCR raporu (YEOTK 1637893).
- Faaliyet raporları ve FAVÖK satırları okunmadı.
- PNLSN'nin kayıtlı sermaye tavanı ve ortaklık tablosunun güncel hâli: KAP'taki tablo 29.07.2023 tarihli.
- KAP fon arama API'si (`api/fund/filter`) sayfa döndürmedi.

## HATA

1. Tarama leke tanımı hatası (YEOTK): bist_tarama_2026-11-16.csv'de YEOTK 'leke = True' (tasf_lot 683.502, %0,082). Bu lotlar Bulls BAG / BCO / BHA, A1 Capital CVL ve Pardus BHF fonlarında. Bu fonlar tasfiye listesinde görünmüyor (ikincil kaynak). FI_TASFIYE_RE fonu değil, portföy yöneticisinin ADINI eşliyor; tasfiyede olmayan fonlar da 'tasfiye' sayılıyor. Şirketin 22.09.2026 KAP açıklamasıyla (1 fon, 27.001 lot, %0,003) çelişiyor; iki kaynak da yukarıda yazılı. Etki: LEKE sayısı fazla sayılmış olabilir (taramada 211 hisse). Düzeltme önerisi (ana model): fon kodu bazında tasfiye listesi.
2. Kapı kuralı ana ortaklık payının 3Ç kârını okuyor; iki adayı faaliyetten bağımsız nedenle düşürdü. FORTE'de baz çeyrekte 2.137,7 mn parasal pozisyon kazancı var. YEOTK'de azınlık payı işaret değiştirdi (3Ç25 -205,9, 3Ç26 +357,9). Kural sonuç görülmeden yazıldığı için değiştirilmedi; mekanik sonuç yazıldı, faaliyet ve konsolide kâr yanına kondu.
3. Kaynak içi tutarsızlık (FORTE XBRL): net parasal pozisyon kazancı 9A25 -34,8 mn, ama 3Ç25 +2.137,7 mn; 3 aylık tutar 9 aylıktan büyük. Ya 6A25 -2.172 mn ya da 3Ç25 sütunu hatalı. Dipnot okunmadı. FORTE kapısı her iki durumda da kâr satırında düşüyor (3Ç25 ana ortaklık kârı 2.413,6 mn raporda yazılı).
4. PNLSN için K25 fon tablosu (G.pkl) yalnız DENİZ fonunda 90.000 lot gösteriyor; oysa Azimut fonları yaklaşık 14,8 mn lot (%19,8) tutuyor (KAP 16.04.2026). Serbest özel fonlar aylık portföy raporu vermediği için tabloda yok: fon tablosu fon sahipliğinin alt sınırıdır.
5. K3 (geçerli bar): PNLSN (09.11, 0,39x; 10.11 O=H=L=C) ve YEOTK (06.11, 0,48x) bilanço günü tepkileri kilitli / hacimsiz tavan barları. 'Tepki iyi' koruması bu yüzden zayıf kanıttır.
6. Ortaklık tablolarının tarihleri bayat: PNLSN 29.07.2023, GWIND 02.08.2023 (KAP şirket sayfası). Azimut yüzdesi 2026 bildirimlerinden ayrıca okundu.
7. GWIND tasfiye fonu pozisyonu (Haziran-Temmuz) da aynı ad eşlemesiyle sayıldı (madde 1). Ağustos-Eylül 0 olduğu için sonucu etkilemiyor.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K2 | geleceğe bakma | EVET | Bildirim listesi toDate 16.11.2026. Kullanılan en geç KAP bildirimi 13.11.2026 (1698076); sayılar için en geç 12.11.2026 (PNLSN yatırımcı sunumu, okunmadı) ve 11.11.2026 (1697234). Her sayının yanında bildirimin 'Gönderim Tarihi' yazılı, sayfa tarihi değil. Fon tablosu bilinme <= 12.10.2026. Fiyatlar 13.11.2026 kapanışına kadar; 16.11 barı kullanılmadı. Fiili dolaşım verisi 15.11.2026 tarihli |
| K10 | ayrıştırma (her adayda en az 3 sayı KAP'tan doğrudan) | EVET | Dört adayda satış (9A / 3Ç), net kâr, esas faaliyet kârı, nakit, borç ve faaliyet nakit akışı KAP finansal rapor sayfasındaki XBRL satırlarından okundu. Sütun sırası sayfa başlığından doğrulandı (01.01-30.09.2026 / 2025 / 01.07-30.09 2026 / 2025). Satış satırı dört raporda ham HTML'den ikinci kez bağımsız okundu ve eşleşti. Dipnot numaraları (ör. '29', '7') sayılardan ayrıldı. Azimut ve kurucu satışları PDF eklerden okundu (Azimut ekleri taranmış görüntüydü; gözle okundu) |
| K12 | ifade | EVET | 'al' / 'öneri' sözü yok. GEÇTİ yalnız DOSYA kapısıdır, PNLSN 'izleme'dir. Başta 'ölçülmüş sinyal yok' ve taban oranlar yazılı. Çıkarımlar (Bulls fonlarının tasfiye dışı olması, azınlık payı açıklaması) kaynağıyla birlikte ve 'ikincil' / 'çıkarım' diye işaretli |
