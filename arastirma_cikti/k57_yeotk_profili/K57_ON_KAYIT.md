# K57 ÖN KAYIT — YEOTK profili ('sıkı dosya') geçmiş testi

Yazım zamanı: 2026-11-09 15:29:00 UTC (2026-11-09 18:29 TR) (ölçümden ÖNCE; sonuç görülmedi). Sürüm: K57 v1.0 (2026-11-09): YEOTK profili ön kayıtlı geçmiş testi (BIST bilgi, ABD karar, Avrupa verisi yok)
ESIK_SHA256: 2a6cc6f6d1fd52e7dc9e7711f580c145a3c87f59369b12e40c4052fe1ce4b1f0
(K57_ESIK + FI_OLCUT + pazar atlamalarının sha256'sı. `python K57.py kos` bu mühürle başlar; eşik değişirse koşu durur.)

## 1. Soru ve kaynak
Cemal (9 Kas 2026, tek ve son talimat): YEOTK gibi 'sıkı dosya' hisseleri BIST'te ve özellikle ABD'de eşlerini geçiyor mu?
YEOTK 9A26 (5 Kas 2026): satış +%31, FAVÖK +%103, 3Ç satışı ≈ 9,2 milyar TL (ilk yarı toplamından fazla), 3Ç net kâr ≈ 864 milyon TL
(ilk yarı 670 milyon), 24 ayda nakit seyrelme yok, raporlu fon payı %0,4, fiyat Mayıs 2026 tepesinin %54 altında, 90 günde -%38;
ertesi gün tavan açılış. Bu olay örneklemde değildir (fiyat 31.08.2026'da kesik, temel_duz 2026/6'ya kadar).

## 2. Olay, giriş, getiri (K28 ile aynı kurgu; FON_IZI fi_k28_olaylar modül olarak çağrılır)
- Açıklama günü D. BIST: KAP 'Finansal Rapor' listesi (islenmis-veri pead/liste_bist), hisse-yıl-dönemin ilk raporu, 18:00 sonrası
  yayın ertesi gün (K28). temel_duz 'aciklama' sütunu gerçek gün değil, yasal süre vekili (çeyrek sonu + 50 / 70 gün; temel.py) olduğu
  için olay günü olarak kullanılmaz; KAP kaydı olmayan dönemde yalnız bilgi tarihi yedeği olur.
  ABD: 2022-12-01'den itibaren Nasdaq bilanço takvimi (K28 listesi); 2021-01-01 .. 2022-11-30 arası SEC finansal tablo özütlerindeki
  10-Q / 10-K başvuru günü (filed; Nasdaq listesi o dönemi kapsamıyor).
- TEPKİ (K28): D'den önceki son işlem günü kapanışından D'den sonraki ilk işlem günü kapanışına getiri ('ham') ve aynı pencerede
  piyasa medyanı düşülmüş tepki ('ear'). BIST akşam, ABD açılış öncesi / kapanış sonrası açıklamalarını kapsar (YEOTK: 5 Kas akşam,
  6 Kas tavan). Tepki günü = bu pencerenin son günü.
- GİRİŞ = tepki gününden sonraki ilk işlem günü AÇILIŞI. r60 = 60. gün kapanışı / giriş - 1 (FI_OLCUT, fiyatlar 2026-08-31'de kesik).
- Ölçüt FI_OLCUT (değiştirilmeden): eşli fark = r60 - aynı gün aynı 60 gün momentum beşliği x 20 gün likidite üçlüsündeki öteki
  hisselerin ortalama r60'ı; ay kümeli bootstrap (2000) %95 aralık; hücre içi sıra; 10 yuvalı slot portföyü vs 200 eşli
  rastgele portföy. HÜCRE TUTAR: n >= 30, ortalama eşli fark > 0 ve aralık alt ucu > 0, sıra > 0,50, portföy > rastgele %90.

## 3. Süzgeçler (yalnız tepki gününde bilinen bilgi; her temel değerin bilgi tarihi <= D)
- F1 büyüme: ABD çeyrek satışı yıllık >= +%25. BIST: satış yıllık büyümesi, D'ye kadar son 92 günde
  açıklayanların üst %40'ı (eşik o ana kadar bilinenlerden; en az 30 değer; enflasyondan bağımsız).
- F2 ivme: bu çeyrek satış >= 1.4 x önceki iki çeyrek ortalaması VE bu çeyrek net kâr > 0 VE > önceki çeyrek net kâr.
- F3 bilanço: özkaynak > 0 ve BIST net borç / özkaynak < 2.0; ABD yükümlülük <= 3.0 x özkaynak
  (Liabilities yoksa LiabilitiesAndStockholdersEquity - StockholdersEquity).
- F4 seyrelme yok (ABD): pay sayısı 4 çeyrekte <= +%10 (FON_IZI fi_k31_finansal, SEC özütleri: bilanço pay sayısı,
  yoksa ağırlıklı ortalama; başvuru günü <= D olan en son bildirim). Oran bir tamsayıya ±%3 yakınsa bölünme
  sayılır (geçer). Veri yoksa geçmez. BIST'te ATLANIR (bedelsiz sermaye artırımları seyrelme değil; ayrım verisi yok).
- F5 temiz sahiplik (BIST): K25 raporlu fon payı < %2 (fi_k25_pay_tablo; yayın anı D'den önce olan en son ay; rapor
  yoksa pay 0 = alt sınır). ABD'de ATLANIR.
- F6 sevilmeyen fiyat: D öncesi son kapanış 250 günlük en yüksekten %30-%70 aşağıda
  VE 60 günlük getirisi o gün pazarın medyanının altında.
- F7 güçlü tepki: 'ear' D'ye kadar son 92 günde tepki günü biten olayların üst %20'ında (yalnız o ana
  kadar bilinenler; K28'in çeyrek içi diliminde görülen etiket sızıntısı böyle önlenir) VE ham tepki >= +%5.
  K28'in çeyrek içi 'ust' etiketi olaylar dosyasında bilgi olarak kalır.

## 4. Varyantlar ve hücreler
- V0 = F7 (K28 tabanı); V1 = F7+F1+F2+F3; V2 = V1+F6; V3 = V2+F4+F5 (TAM YEOTK PROFİLİ, ana sonuç); V4 = F1+F2+F3+F6 (tepkisiz).
- Hücreler (giriş gününe göre): BIST 2022-23 ve BIST 2024-26 = BİLGİ; ABD 2021-22 = BİLGİ; ABD 2023 ve ABD 2024-26 = KARAR.
- Karar (FON_IZI _fi_olcut_karar_ortak, karar pazarları ABD + AVR): iki ABD karar hücresi tutarsa en fazla 'ABD-ADAY (AVRUPA VERİSİ YOK)'
  (Avrupa'da bilanço olay verisi bedava yok); BIST de tutuyorsa '+ BIST' bilgisi. Aksi 'İZ DEĞİL'.

## 5. Veri durumu ve önceden yazılı yedek kural
- ABD temel verisi (F1-F3) SEC XBRL frames API'sinden gelir (Revenues > RevenueFromContractWithCustomerExcludingAssessedTax >
  SalesRevenueNet: gereken çeyreklerin hepsini taşıyan ilk etiket, etiket karıştırılmaz; NetIncomeLoss; StockholdersEquity,
  Liabilities anlık; 4. çeyrek = yıllık - üç çeyrek, dönemler hizalıysa). Frames kayıtlarında 'filed' yok; bilgi tarihi = çeyrek sonundan
  sonraki ilk Nasdaq açıklama günü ya da SEC özütlerindeki ilk 10-Q / 10-K başvuru günü (hangisi önce), ikisi de yoksa çeyrek sonu
  + 90 gün. Frames değerleri son başvurudaki (gerekirse düzeltilmiş) değerdir: küçük bir geriye dönük düzeltme etkisi.
- Ön kayıt anında durum: SEC, istenen kimlik satırıyla (User-Agent 'col-yolu-arastirma/1.0 (+https://github.com/cemalcelebi/col_yolu)', e-posta yok)
  9 Kas 2026'da 403 ('Undeclared Automated Tool') döndürdü. Başka kimlikle deneme yapılmaz.
- YEDEK KURAL: ABD karar hücrelerindeki olayların en az %50'ında F1-F3 hesaplanamıyorsa ABD'de F1-F3 ATLANIR ve
  o satırlar 'ABD TEMEL VERİSİ YOK' diye işaretlenir; F1-F3 içeren varyantların (V1-V4, D1, D3) kararı 'ÖLÇÜLEMEDİ (ABD TEMEL VERİSİ YOK)'
  olur, İZ / ABD-ADAY denemez. Fiyat + pay kısmı (F7, F6, F4) yine ölçülür ve 'kısmi karar' bilgi olarak yazılır. BIST tam profille ölçülür.

## 6. Beklenti (önceden)
K28: iyi bilanço tepkisi BIST'te artı, ABD 2023'te artı, ABD 2024-26'da eksi (-%1,4) çıkmıştı; çöl + güçlü tepki örneklem dışında
tersine dönmüştü. Beklenti: V0 tutmaz; temel süzgeçler n'yi çok küçültür (BIST V3 hücre başına muhtemelen < 30); profilin iki ABD
hücresinde birden tutma olasılığı düşük. Sonuç ne olursa olsun eşik değişmez.

## 7. İz çıkmazsa sıradaki 3 deneme (önceden yazıldı; sonuç görülmeden; HEPSİ KOŞULUR, ayrı etiketle)
- D1 'F2 1,2 kat': F2'de 1,4 yerine 1,2 (V1-V4).
- D2 '120 gün ufuk': aynı varyantlar (V0-V4), FI_OLCUT ufku 120 gün (portföy tutma da 120 gün; kriz kesiği aynı).
- D3 'art arda iki ivmeli çeyrek': F2 hem bu çeyrekte hem bir önceki çeyrekte (önceki çeyrek satışı >= 1,4 x ondan önceki iki çeyrek,
  önceki çeyrek kârı > 0 ve kendinden önceki çeyrekten büyük) (V1-V4).
Devamlar aynı karar kuralıyla okunur; çoklu deneme nedeniyle yalnız ana varyantın (V3) iki ABD karar hücresi kanıt sayılır, devamlar aday üretir.
