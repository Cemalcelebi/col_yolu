# K62 ÖN KAYIT — BIST PEAD birebir tekrar (Ahlatcıoğlu & Okay 2021)

K62 v1.0 (2026-11-11): BIST PEAD birebir tekrar (Ahlatcıoğlu & Okay 2021): SUETF, SUEAF (veri yok), EAR; CAR[2,61]; dönemler; FI_OLCUT

- MÜHÜR (K62_ESIK + FI_OLCUT sha256): `7dbda78a5d6f6c33a54f22abaab3a956a3f9c233308617d3a74331c3f8f2b68d`
- VERİ (önbellek sha256): `d35b377408b45ccdf7a55229e44f6b411d34143d1dc67a19e5ae848ca1e3220c`
- V_BIST.pkl (sha256): `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`
- ZAMAN (UTC): `2026-11-12 04:09:42 UTC`

Bu dosya ölçümden ÖNCE yazıldı. Yazıldığı anda gerçek veride sürprize bağlı hiçbir getiri / CAR / fark hesaplanmadı (yalnız indirme ve sayım:
`python K62.py indir`, `python K62.py kapsam`). `python -I K62.py kos` bu dosyanın mührünü, git'e işlenmiş ve değişmemiş olmasını ve veri
sha256'sını doğrulamadan ölçüm yapmaz. Sonuç görüldükten sonra bu dosyaya ve K62_ESIK'e kural / eşik eklenmez.

## 0. Kaynak makale ve yöntemi

- Künye: Aykut Ahlatcıoğlu, Nesrin Okay (2021). "Post-earnings announcement drift: Evidence from Turkey". Borsa Istanbul Review 21(1), 92-103.
  doi 10.1016/j.bir.2020.09.001 (açık erişim, CC BY-NC-ND; çevrim içi Eylül 2020).
- Erişim: ScienceDirect tam metni bu ortamdan alınamadı (HTTP 403), EconStor kopyası bot engelinde. Yöntem ve tablolar aynı yazarın doktora tezinden
  okundu: A. Ahlatcıoğlu (2020), "Determinants of post-announcement drift and market reaction to earnings announcements", Boğaziçi Üniversitesi,
  3. bölüm "PEAD: Evidence from Turkey" (bölümün giriş paragrafı makale özetiyle kelimesi kelimesine aynı; %2,9 / %2,9 / %2,2 aynı).
  BİLİNMEYEN: makalenin teze göre olası küçük farkları (tablo numaraları, yuvarlama, hakem düzeltmeleri) doğrulanamadı.
- Örneklem: 2007-2018, çeyreklik kazanç açıklamaları; başlangıç 16.061 şirket-çeyrek, süzgeçlerden sonra TAM ÖRNEKLEM 6471 gözlem; ANALİST ÖRNEKLEMİ 2398 gözlem.
  Süzgeçler: (i) mali yılı Aralık'ta biten şirketler; (ii) bütün ölçü ve açıklayıcı değişkenlerin verisi var; (iii) önceki yıl sonu piyasa değeri
  > 100 milyon USD ve özkaynak negatif değil; CAR ve EAR pencerelerindeki günlük getirilerin en az 2/3'ü var. Sürekli değişkenler çeyreklik dağılımın
  %1 ve %99'unda kırpılır (winsorize). Kotasyondan çıkan hisse kalan günlerde eşleşen portföyün getirisini kazanır (dipnot 5).
- Veri kaynakları (makale): muhasebe verisi Rasyonet; piyasa verisi ve açıklama günü Bloomberg; kurumsal sahiplik MKK; sektör GICS (Compustat Global);
  analist tahmini 2014'e kadar CNBC-E anketleri, sonra Bloomberg anketleri (en az 1 tahmin).
- Ölçü 1, SUETF_(i,q) = (E_(i,q) - E_(i,q-4)) / MV_(i,q): mevsimsel rassal yürüyüş; E çeyreklik kazanç (TL), MV çeyrek sonu piyasa değeri.
- Ölçü 2, SUEAF_(i,q) = (E_(i,q) - F_(i,q)) / MV_(i,q): F analist tahminlerinin ortalaması.
- Ölçü 3, EAR_(i,q) = prod_(k=t-1..t+1)(1 + R_(i,k)) - prod_(k=t-1..t+1)(1 + R_(p,k)): açıklama günü t çevresinde üç işlem günü; p hissenin eşleştiği
  büyüklük-DD/PD portföyü. Portföyler: her yıl Haziran sonunda 2 büyüklük x 3 DD/PD grubu kesişimi (6 portföy); büyüklük = Haziran sonu piyasa
  değeri; DD/PD = önceki mali yıl sonu defter değeri / önceki Aralık sonu piyasa değeri; günlük EŞİT AĞIRLIKLI getiri, Temmuz t - Haziran t+1.
- Gruplama: üç ölçü de her takvim çeyreğinde sıraya göre TERTİL puanına çevrilir (0, 0,5, 1); Q1 en olumsuz, Q3 en olumlu.
- Sonuç ölçüsü: CAR[2,61]_(i,q) = prod_(k=t+2..t+61)(1 + R_(i,k)) - prod_(k=t+2..t+61)(1 + R_(p,k)) (60 işlem günü; ayrıca [2,21], [2,41]).
  PEAD[2,61] = ortalama CAR(Q3) - ortalama CAR(Q1) (üst üçte bir uzun, alt üçte bir kısa korunma portföyü; olay zamanı). p değerleri değişen varyansa
  dayanıklı, kazanç çeyreğine göre kümelenmiş standart hatayla.
- Kontrol değişkenleri (Tablo 5-6; CAR = a0 + a1 PUAN + b X + c PUAN x X; sektör ve çeyrek sabit etkisi; çeyreğe göre küme; X standartlaştırılmış):
  CONCEARNINGS (aynı gün açıklayan şirket sayısı), FRIDUM (Cuma), IVOL ([t-61, t-2] piyasa modeli kalıntı standart sapması, BIST-100), ILLIQUIDITY
  (ort. ln(1 + |R| / enflasyon düzeltmeli hacim, milyon TL), [t-61, t-2]), SIZE (önceki yıl sonu piyasa değeri, milyon USD; logaritması), REPORTLAG
  (çeyrek sonundan açıklamaya gün), IO (kurumsal sahiplik / halka açık pay), B/M, BETA ([t-61, t-2]), PRERET ([t-61, t-2] al-tut - BIST-100).
- BİLDİRİLEN SAYILAR (Tablo 3 Panel B "PEAD at Different Horizons"; t değerleri parantezde):

| ölçü | PEAD[2,21] | PEAD[2,41] | PEAD[2,61] |
|---|---|---|---|
| SUETF | 0.0118 (3.75) | 0.0219 (4.44) | 0.0294 (4.26) |
| SUEAF | 0.0131 (3.09) | 0.0261 (4.39) | 0.0290 (3.63) |
| EAR | 0.00763 (2.17) | 0.0121 (2.61) | 0.0218 (3.88) |

  Özetteki %2,9 / %2,9 / %2,2 = PEAD[2,61] sütunu (SUETF / SUEAF / EAR). Kontrollü regresyonda ortalama şirket için PEAD[2,61]: SUETF
  %2,78, EAR %2,26 (Tablo 5-6). SUETF ile 12 yılın 11'inde, EAR ile 10'unda, SUEAF ile 9'unda artı.
  Aylık takvim portföyü alfaları (Tablo 7; Fama-French 3 faktör): SUETF %1,12, SUEAF %0,77, EAR %0,47.

## A. BİREBİR TEKRAR (makale tanımları; veri izin verdiği kadar)

A1. Veri: açıklama anı = KAP'ta o hisse - mali yıl - çeyrek için yayımlanan İLK 'Finansal Rapor' bildirimi (bildirim sınıfı FR;
    liste 2009-06-01 - 2026-08-31). Fiyat (bölünme ve temettü düzeltilmiş kapanış), piyasa değeri (TL ve USD), USD hacim, BIST-100: İş Yatırım
    günlük hisse verisi (2008-01-01 - 2026-08-31; kotasyondan çıkanlar dahil). Mali tablo: İş Yatırım çeyreklik tablolar (2008'den;
    grup sırası XI_29, UFRS, UFRS_K, XI_29K; ilk dolu grup).
A2. t = yayın gününe eşit ya da ondan sonraki ilk işlem günü (saat ayrımı yok; makalede Bloomberg günü). EAR penceresi [t-1, t+1]; CAR penceresi
    [t+2, t+N], N = 21, 41, 61; ana ufuk 61.
A3. E = net dönem kârının ana ortaklık payı (kalem 3Z); çeyreklik = birikimli(q) - birikimli(q-1) (Ç1 = 3 aylık). MV_q = çeyreğin son işlem
    günü piyasa değeri (TL). SUETF = (E_q - E_(q-4)) / MV_q.
A4. Portföyler: 2 büyüklük x 3 DD/PD kovası (eşit sayıda; bağımsız sıralama), Haziran sonu; özkaynağı <= 0 olan portföy dışı; bir portföyde o gün
    getirisi olan en az 5 hisse yoksa portföy getirisi yok. Olayın portföyü t günündeki atamadır (pencere boyunca sabit).
A5. Örneklem: mali çeyrek 2009Ç2 - 2018Ç4; E_q, E_(q-4), MV_q var; önceki mali yıl sonu piyasa değeri > 100 milyon USD; önceki
    yıl sonu özkaynak >= 0; t günü portföy ataması var; EAR, [t-61, t-2] ve CAR[2,61] pencerelerinde günlük getirilerin en az 2/3'ü var;
    1 <= açıklama - çeyrek sonu <= 150 gün. Getirisi olmayan günde hisse portföy getirisini alır.
A6. Tertil: mali çeyrek içinde sıra (eşitlik hisse koduyla); çeyrekte en az 30 olay yoksa çeyrek ölçülmez. CAR çeyrek içi %1 / %99 kırpılır.
A7. Ölçülenler: SUETF, EAR. VERİ YOK: SUEAF (ücretsiz tarihsel analist tahmini yok; tahmin uydurulmaz, vekil üretilmez).
A8. BAŞARI ÖLÇÜTÜ (önceden): bir ölçü 'YENİDEN ÜRETİLDİ' ⇔ PEAD[2,61] işareti makaledekiyle aynı VE nokta değeri makaledekinin ±1,5 puanı içinde
    (SUETF: %1,44 .. %4,44; EAR: %0,68 .. %3,68). Ölçü bazında ayrı ayrı. SUEAF: 'VERİ YOK,
    yeniden üretilemedi'. İşaret aynı ama aralık dışı: 'YÖN AYNI, BÜYÜKLÜK FARKLI'; işaret ters: 'YENİDEN ÜRETİLEMEDİ'. [2,21] ve [2,41] bilgi.
    Kontrollü regresyon (PUAN katsayısı; makale %2,78 / %2,26) aynı ±1,5 puan kuralıyla ayrıca yazılır (bilgi).

SAPMA listesi (veri yüzünden zorunlu; her biri sonucu etkileyebilir):
- SAPMA 1 (dönem): makale 2007Ç1-2018Ç4 (48 çeyrek). KAP 'Finansal Rapor' kayıtları Haziran 2009'da, İş Yatırım mali tabloları 2008/3'te başlıyor;
  tekrar örneklemi 2009Ç2-2018Ç4 (39 çeyrek). 2007Ç1-2009Ç1 (9 çeyrek; 2008 krizi dahil) YOK.
- SAPMA 2 (kaynak): Rasyonet / Bloomberg yerine İş Yatırım + KAP. Açıklama günü Bloomberg günü değil, KAP'taki ilk Finansal Rapor günü
  (bankalarda solo ve konsolide rapordan ilk gelen).
- SAPMA 3 (SUEAF): analist tahmini verisi yok; ölçü 2 ölçülmez.
- SAPMA 4 (IO): MKK kurumsal sahiplik verisi yok; örneklem şartında ve regresyonda yok.
- SAPMA 5 (ILLIQUIDITY): enflasyon düzeltmeli TL hacim yerine USD hacim (milyon USD).
- SAPMA 6 (sektör sabit etkisi): GICS yerine sektor_BIST.csv; listede olmayan (çoğu kotasyondan çıkmış) hisse 'BILINMIYOR' sınıfında.
- SAPMA 7 (Aralık mali yılı): özel hesap dönemli şirketlerin listesi yok; şart dolaylı: İş Yatırım'da 3/6/9/12. ay tablosu olması + açıklama
  gecikmesi 1-150 gün süzgeci (makalede bu süzgeç yok; REPORTLAG en büyük 785).
- SAPMA 8 (kazanç tanımı): makale 'reported earnings' der; burada net dönem kârı ana ortaklık payı; bankalarda solo tablo öncelikli (grup sırası).
- SAPMA 9 (yeniden sunum; KANITLI): İş Yatırım YILLIK (12 aylık) değerleri sonraki yılın raporundaki yeniden sunulmuş karşılaştırmalı değerle
  değiştirilmiş görünüyor. Kanıt (11 Kasım 2026, getiri hesabından önce): BIMAS 2022 birikimli net kâr 3 / 6 / 9 / 12 ay = 1,34 / 3,02 / 4,79 / 16,60
  milyar TL (12 aylık değer TMS 29 ile Aralık 2023 alım gücüne taşınmış; ilk açıklanan yaklaşık 8,2 milyar TL); 2024 / 12 değeri binliğe yuvarlı
  değil (24.328.622.067). Ara dönem (3 / 6 / 9 ay) değerleri ilk açıklandığı gibi duruyor. Sonuç: (a) mali 2022'den itibaren 4. çeyrek kazancı
  (birikimli 12 - birikimli 9) hem birim karışıklığı hem GELECEK BİLGİSİ içerir; (b) 2024 1.-3. çeyreklerde E_q enflasyon düzeltmeli, E_(q-4)
  nominaldir. Bu yüzden SUETF için mali çeyrek 2022Ç4, 2023Ç4, 2024Ç1, 2024Ç2, 2024Ç3, 2024Ç4, 2025Ç4 'KİRLİ' sayılır (B3, C1). (c) Haziran 2023 ve sonrasındaki portföy
  oluşumlarında DD/PD yeniden sunulmuş özkaynağı kullanır (sınıflamada küçük ileriye bakma; düzeltilemedi). (d) 2022 öncesinde de yıllık değerler
  sonradan düzeltilmiş olabilir (doğrulanamadı; A'da olası küçük sızıntı). Mali yılı Ocak'ta biten MAVI gibi 1-2 şirket gecikme süzgecinden geçer.
- SAPMA 10 (çok faktörlü modeller, Tablo 7-8): kapsam dışı; ölçülmez.
- SAPMA 11 (takvim çeyreği): makale 'takvim çeyreği içinde sıra' der; burada mali çeyrek (kümeleme de mali çeyrek).

## B. DÖNEM (aynı ölçüler, aynı yöntem)

B1. A'daki yöntem (makale tertili, CAR[2,N], aynı örneklem süzgeçleri) açıklama günü t şu aralıklarda olan olaylara ayrı ayrı uygulanır:
    2017-2021 (2017-01-01 .. 2021-12-31); 2022-2026 (2022-01-01 .. 2026-12-31); 2023-2026 (2023-01-01 .. 2026-12-31). Tertil ve kırpma mali çeyrek içinde, bütün tam örneklem üzerinden bir kez yapılır.
B2. Fon krizi kesiği: fiyatlar 2026-08-31'de kesilir (sonrası indirilmez); [t+2, t+61] penceresi bu tarihi aşan olay ölçülmez.
B3. TMS 29 (SAPMA 9): başlangıcı 2022 ve sonrası olan dönemlerde (2022-2026, 2023-2026) SUETF'in ANA satırı yalnız TEMİZ mali çeyreklerdir (kirli çeyrekler
    2022Ç4, 2023Ç4, 2024Ç1, 2024Ç2, 2024Ç3, 2024Ç4, 2025Ç4 hariç); bütün çeyrekleri içeren satır 'kirli, bilgi' diye ayrıca yazılır. EAR'da çeyrek ayıklanmaz. 2017-2021 etkilenmez.
B4. Okuma (önceden): bir dönem-ölçü 'TUTAR' ⇔ PEAD[2,61] > 0, kümeli p < 0,05 ve BH düzeltmesinden sonra da reddedilir (D3). Aksi 'TUTMAZ'.

## C. PROJE CETVELİ (FON_IZI FI_OLCUT; karar günü bilgisiyle)

C1. Olaylar: 'onsel' örneklem (A5'in karar gününde bilinen şartları; CAR penceresi şartı YOK). Sürpriz sınıfı GELECEĞE BAKMADAN: olayın değeri, önceki
    mali çeyreğin (karar günü bu olayın karar gününden geç olmayan) olaylarının 1/3 ve 2/3 dilim değerleriyle kıyaslanır (>= üst: Q3; <= alt: Q1);
    havuz < 30 ise olay sınıfsız. Karar günü = t+1 (EAR o günün kapanışında bilinir); GİRİŞ = t+2 işlem günü AÇILIŞI. SUETF'te TMS 29 kirli
    çeyreklerinin (B3) olayları sınıfsızdır ve havuz olamazlar; havuz en yakın önceki temiz çeyrektir (en çok 4 çeyrek geride; yoksa sınıfsız).
C2. Ölçüm: fi_olcut_panel / fi_olcut_olay / fi_olcut_hucre, V_BIST.pkl üzerinde (yalnız bugün işlem gören hisseler): r60 = 60. gün kapanışı / giriş açılışı - 1
    (kriz 2026-08-31'de kesik); EŞLİ FARK = r60 - aynı giriş günü aynı 60 gün momentum beşliği x likidite üçlüsündeki öteki hisselerin ortalama r60'ı.
C3. Hücre TUTAR (Q3, iyi sürpriz): n >= 30; ortalama eşli fark > 0 ve ay kümeli bootstrap %95 aralığının alt ucu > 0; ortalama hücre içi sıra > 0,50;
    10 yuvalı slot portföyü, 200 eşli rastgele portföyün %90'ından büyük. Q1 (kötü sürpriz) için AYNA (kaçınma): üst uç < 0, sıra < 0,50, portföy
    rastgele portföylerin %10'undan küçük. Hücreler: BIST 2023, BIST 2024-26 (FI_OLCUT dönemleri) + bilgi: 2017-2021, 2022-2026, 2023-2026.
C4. Aynı hissede 60 işlem günü içinde tekrarlanan olay tek olay (ilki), her ölçü x uç için ayrı.
C5. KARAR (CLAUDE.md 'Test ve bulgu standardı'): İZ için karar hücreleri ABD ve Avrupa'dır; K62 yalnız BIST'tir. Bu yüzden karar en fazla
    'BIST-BİLGİ: TUTAR' (BIST 2023 ve BIST 2024-26 hücrelerinin ikisi de tutarsa), aksi 'İZ DEĞİL'. İZ ya da ADAY denmez. Eşik oynatılmaz.

## D. PROTOKOL

D1. Tekilleştirme: makale örtüşen pencerelere izin verir (yıllık rapor ile 1. çeyrek arası ~45 işlem günü). A ve B'nin ana satırları makaledeki gibi
    tekilleştirmesizdir; aynı satırlar 60 işlem günü tekilleştirmesiyle de yazılır (bilgi). C'de tekilleştirme ana kuraldır.
D2. Her satırda birlikte: ortalama, medyan, eşli fark (CAR'ın kendisi eşleşen portföye göre farktır; C'de FI_OLCUT eşli farkı), %95 güven aralığı
    (mali çeyrek kümeli bootstrap, 2000 çekiliş, tohum 62), kümeli t ve p.
D3. Çoklu test: B ailesi = 2 ölçülen ölçü x 3 dönem x 3 sınama (Q3 ortalaması ≠ 0, Q1 ortalaması ≠ 0, PEAD ≠ 0; ufuk 61) = 18 sınama
    (SUEAF verisi olsaydı 27). Benjamini-Hochberg %10; Bonferroni bilgi (alfa 0.05 / sınama sayısı). A birebir tekrar olduğundan aileye girmez.
D4. İşlem maliyeti: BIST tek yön 30 bp. Net korunma getirisi = PEAD - 4 x maliyet; net uzun bacak = CAR(Q3) - 2 x maliyet; açığa satış
    maliyeti / kısıtı ayrıca hesaplanmaz (kısa bacak BIST'te pratikte kısıtlı; bilgi).
D5. Geleceğe bakma: C'de her bilgi tarihi <= karar günü (t+1 kapanışı); açıklama saati kullanılmaz, giriş her durumda t+2 açılışıdır (saat bilinmese de
    güvenli). A ve B makaledeki gibi çeyrek içi tertil ve kırpma kullanır (çeyreğin sonradan açıklayanlarına bakar); bu yüzden A / B tekrar ölçüsüdür,
    alınabilirlik ölçüsü C'dir.
D6. Yaşayan yanlılığı: A ve B'de İş Yatırım verisi kotasyondan çıkan hisseleri içerir (KAP listesindeki kodlardan fiyatı bulunanlar); kodu değişen ya
    da İş Yatırım'da bulunmayan eski hisseler eksik kalabilir (kapsamda sayılır). C yalnız bugün işlem gören V_BIST hisseleridir (yanlılık var; beyan).
D7. Sayım modu (`kapsam`) hiçbir getiri / sürpriz değeri üretmez; testte denetlenir.

## E. K28 KARŞILAŞTIRMA TABLOSU (şablon; Faz 2'de doldurulur)

| özellik | K28 (Ç100; FON_IZI fi_k28_*) | Makale | K62 A / B | K62 C |
|---|---|---|---|---|
| olay günü | KAP ilk Finansal Rapor; 18:00 sonrası ertesi gün | Bloomberg açıklama günü | KAP ilk Finansal Rapor günü (saat ayrımı yok) | aynı; karar t+1 |
| sürpriz ölçüsü | tepki: kapanış(D-1) -> kapanış(D+1) - bütün hisselerin medyanı | SUETF, SUEAF, EAR (2x3 portföye göre, [t-1, t+1]) | SUETF, EAR (SUEAF veri yok) | SUETF, EAR |
| gruplama | takvim çeyreği içinde üst / alt %20 | çeyrek içi tertil | mali çeyrek içi tertil | önceki çeyreğin tertil kesimleri |
| giriş | tepki bitişinden sonraki işlem günü açılışı | t+2 (kapanıştan kapanışa) | t+2 (kapanış t+1'den) | t+2 açılışı |
| getiri | r60: açılıştan 60. gün kapanışına | CAR[2,61] al-tut farkı | CAR[2,61] al-tut farkı | r60 |
| kıyas | aynı gün momentum beşliği x likidite üçlüsü ortalaması | 2x3 büyüklük-DD/PD portföyü | 2x3 büyüklük-DD/PD portföyü | momentum x likidite hücresi |
| örneklem | V_BIST'te olan bütün hisseler (boyut şartı yok) | > 100 mn USD, özkaynak >= 0, Aralık mali yılı | makaledeki süzgeçler (SAPMA'larla) | aynı süzgeçler, V_BIST'te olanlar |
| dönem | 2022-07 -> 2026 (ek: 2016-22 örneklem dışı) | 2007-2018 | 2009Ç2-2018Ç4; 2017-21; 2022-26; 2023-26 | 2023; 2024-26; + bilgi dönemleri |
| yaşayan yanlılığı | var (yalnız yaşayanlar) | dipnot 5 kuralı | kotasyondan çıkanlar dahil (bulunabilenler) | var |
| tekilleştirme | yok (hisse-dönem başına ilk rapor) | yok | ana: yok; bilgi: 60 gün | 60 gün |
| olay sayısı | (k28_ozet.csv) | 6471 / 2398 | (Faz 2) | (Faz 2) |
| sonuç | üst %20 eşli fark BIST 2023 +%5,0, 2024-26 +%1,0; alt %20 -%5,1 / -%3,0 | PEAD %2,9 / %2,9 / %2,2 | (Faz 2) | (Faz 2) |

## F. MÜHÜR

Eşik / parametre sözlüğü K62_ESIK ve FON_IZI FI_OLCUT birlikte kararlı JSON'a (anahtar sıralı) çevrilir; sha256'sı dosyanın başındaki MÜHÜR satırıdır
(`K62.k62_esik_sha()`). `kos` bu değeri yeniden hesaplar; tutmazsa durur. VERİ satırı önbellek dosyalarının (KAP pencereleri, hisse fiyat dosyaları,
mali tablo dosyaları) sha256 özetidir; koşudaki veri farklıysa `kos` durur (`--veri-yeniden` ile ve raporda açıkça yazılarak sürdürülebilir).

## G. VERİ VE KAPSAM (sayım; getiri yok)

- KAP: 106852 Finansal Rapor kaydı -> 29700 hisse-çeyrek açıklaması (ilk 2009-06-01 08:13:16, son 2026-08-31 21:51:07).
- Fiyat (İş Yatırım): 715 hisse, 4681 işlem günü (2008-01-02 .. 2026-08-31); son 21 işlem gününde fiyatı olmayan
  (kotasyondan çıkmış sayılan) 93 hisse; V_BIST'te de olan 580 / 581.
- Mali tablo (İş Yatırım): 682 hisse, 32607 hisse-çeyrek satırı (2008-2026); grup dağılımı {'UFRS': 26, 'XI_29': 643, 'XI_29K': 13}.

| bölüm / dönem | açıklama | hisse | SUETF girdisi var | > 100 mn USD | EAR penceresi var | onsel (C) | TAM örneklem | tam: hisse | tam: çeyrek | tam: kotasyondan çıkan hisse olayı | onsel ve V_BIST'te |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A (mali çeyrek 2009Ç2-2018Ç4) | 14957 | 479 | 13267 | 6014 | 12788 | 5434 | 5430 | 206 | 39 | 523 | 4895 |
| B 2017-2021 | 8034 | 494 | 7371 | 3115 | 7240 | 2953 | 2948 | 221 | 20 | 116 | 2829 |
| B 2022-2026 | 10267 | 626 | 9765 | 5395 | 9161 | 5057 | 4722 | 405 | 18 | 3 | 5042 |
| B 2023-2026 | 8388 | 625 | 8003 | 4601 | 7576 | 4327 | 3992 | 396 | 14 | 0 | 4316 |
| hepsi | 29700 | 708 | 27134 | 13134 | 25926 | 12124 | 11781 | 441 | 69 | 554 | 11535 |

Makale tam örneklemi 6471 gözlem / 48 çeyrek (çeyrek başına ~135); analist örneklemi 2398.

Veri fizibilitesi (11 Kasım 2026; gerçek istekle denendi; kişisel bilgi gönderilmedi):

| kaynak | sonuç | kapsam / alanlar | kısıt |
|---|---|---|---|
| Yahoo chart API (.IS) | çalışıyor (tarayıcı User-Agent ile) | 2005-01'den günlük; düzeltilmiş kapanış, temettü / bölünme; XU100.IS ve XU030.IS var | XUTUM.IS boş; denenen 15 kotasyondan çıkmış kodun 15'i 404 (ASYAB, KIPA, DENIZ, FINBN, BOYNR, ADANA, UNYEC, SODA, TRKCM, ANACM, ABANA, ALNTF, TEKST, BOLUC, BSHEV): yaşayan yanlılığı; K62'de kullanılmadı |
| İş Yatırım günlük hisse verisi | çalışıyor | 2000'lerden (KIPA 2000-01 .. 2018-08; ASYAB 2006-07 .. 2016-05); düzeltilmiş kapanış (temettü dahil; TUPRS Nisan 2018'de katsayı sıçraması Yahoo ile aynı), ham kapanış, piyasa değeri TL / USD, halka açık PD, hacim TL / USD, BIST-100, sermaye | açılış fiyatı yok (FI_OLCUT bu yüzden V_BIST'te); büyük yanıt kopuyor (4 yıllık parça + gzip) |
| V_BIST.pkl (islenmis-veri dalı) | var | 581 yaşayan hisse, OHLCV; 358'i 2015-06'dan | yalnız yaşayanlar; piyasa değeri yok. K28'in 2016-22 örneklem dışı koşusu fiyatı buradan aldı |
| KAP bildirim sorgusu (sınıf FR) | çalışıyor (403 yok; ara sıra 429) | 2009-06-01'den (öncesi 0 kayıt); yayın anı (saniye), mali yıl, dönem, kodlar; kotasyondan çıkanlar dahil | K28'in konu kodu süzgeci 2016 öncesi kayıt döndürmüyor (sınıf süzgeci kullanıldı); Haziran 2009 öncesi açıklama günü YOK |
| İş Yatırım mali tablo servisi | çalışıyor | 2008 / 3'ten (2007 boş); çeyreklik birikimli gelir tablosu ve bilanço; gruplar XI_29, UFRS, UFRS_K, XI_29K | yıllık değerlerde yeniden sunum sızıntısı (SAPMA 9); analist tahmini yok |
| Analist tahmini: Yahoo kazanç geçmişi | çalışıyor ama yetersiz | yalnız son 4 çeyrek; GARAN'da var, THYAO ve ALARK'ta boş | tarihsel değil |
| Analist tahmini: Investing takvimi, Fintables (site ve API) | 403 | — | bot engeli / üyelik |
| Analist tahmini: İş Yatırım, BigPara, Mynet beklenti sayfaları | 404 | — | sayfa yok |
| Analist tahmini: Ekofin konsensüs | yalnız güncel çeyrek | ~38 hisse | arşiv yok |
| Analist tahmini: Foreks / ForInvest, CNBC-E, Bloomberg HT anketleri | toplu veri yok | haber arşivinde çeyrek çeyrek tablolar (makale 2014'e kadar CNBC-E anketini kullandı) | elle derleme gerekir; tarihsel bütünlük doğrulanamaz |
| Analist tahmini: Rasyonet, Finnet, Matriks, Bloomberg, I/B/E/S (LSEG), FactSet | ücretli / kurumsal | tarihsel konsensüs var (makalenin kaynağı 2014'e kadar CNBC-E anketi, sonra Bloomberg anketi; muhasebe verisi Rasyonet) | fiyat yayımlanmıyor; bireysel erişim yok; denenmedi (K63 ile aynı sonuç) |
| Analist tahmini: EODHD, Alpha Vantage (EARNINGS_ESTIMATES) | ücretli (59,99 / 49,99 $ ay) | ABD'de donmuş çeyreklik konsensüs 2017-06'dan (K63) | BIST'te alanın dolu olduğu DOĞRULANAMADI; 2007-2018 makale dönemini zaten kapsamaz |

SUEAF için sonuç: VERİ YOK.

## H. BOŞLUK (makalede açık yazılmayan yerler; burada en dar / en mekanik yorum)

- BOŞLUK 1: 'kazanç' kalemi (bkz. SAPMA 8). BOŞLUK 2: 'önceki yıl' = mali çeyreğin yılından bir önceki takvim yılı sonu (piyasa değeri ve özkaynak).
- BOŞLUK 3: portföy kovaları eşit sayıda (medyan; üçte birler); hisse kendi portföyünün üyesidir; portföy t günü atamasıyla pencere boyunca sabit.
- BOŞLUK 4: günlük getiri = kapanış / önceki 5 işlem günü içindeki son kapanış - 1; o gün kapanışı yoksa getirisi yok sayılır ve hisse portföy
  getirisini alır; portföy getirisi de yoksa ikisi de 0.
- BOŞLUK 5: MV_q çeyrek sonuna eşit ya da önceki son işlem günü (en çok 10 takvim günü geride; 5 işlem günü ileri taşıma).
- BOŞLUK 6: tertil sınırı = kat(3 x sıra / n); çeyrekte en az 30 olay. Kırpma yalnız CAR ve regresyon değişkenlerine (tertil sırasını etkilemez).
- BOŞLUK 7: kümeli standart hata CR1 (G/(G-1) x (N-1)/(N-K)), p değeri t(G-1). Uç ortalamalarının t'si sabitli EKK'den.
- BOŞLUK 8: çok kodlu şirkette (pay grupları) fiyat verisi olan kodlardan toplam USD hacmi en büyük olan (bütün dönem hacmi; sınıf seçimi için
  küçük bir ileriye bakma içerir).
- BOŞLUK 9: CONCEARNINGS = aynı t gününe düşen bütün açıklamalar (örneklem dışı şirketler dahil; kendisi dahil). FRIDUM = t Cuma.
- BOŞLUK 10: regresyonda kontroller çeyrek içi kırpılıp bölüm örnekleminde standartlaştırılır; FRIDUM kırpılmaz; sabit etkiler kukla.
- BOŞLUK 11: C'de dönem = GİRİŞ günü (FI_OLCUT kuralı); B'de dönem = açıklama günü t.

## I. FAZ 2 KOMUTLARI

1. Ana oturum bu dosyayı ve K62.py / test_k62.py'yi denetler, git'e işler (ön kayıt commit'i ölçümden önce).
2. `python test_k62.py` (sentetik; geçmeli).  3. `python -I K62.py kos` (A + B + C + rapor; veri /tmp/k62_veri ve /tmp/veri/V_BIST.pkl).
4. `python K62.py rapor` (K62_RAPOR.md'yi çıktılardan yeniden yazar).
