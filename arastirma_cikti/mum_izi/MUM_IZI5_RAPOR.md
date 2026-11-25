# MUM_IZI5 RAPOR (2026-11-25): v3 bant koordinatında mum dizisi benzerliği, Cemal'in işaretleriyle sınama

İş tanımı: MUM_IZI5_IS_TANIMI.md (36a4686). Ön kayıt: MUM_IZI5_ON_KAYIT.md (04389a9; SAPMA ek 4a3146a). Kod: MUM_IZI_V3.py, test_mum_izi5.py (12 / 12).
Getiri / sonrası HESAPLANMADI. Veri <= 2022-12-31 (sınamadaki 24 pencerenin en geç sonu 2022-04-07).

## SONUÇ (tek bakışta)

- Sentetik kabul ölçütü GEÇMEDİ: pozitif %10 gürültüde %70,2 (ölçüt >= %70: geçti); negatiflerin hiçbiri <= %5 değil (n1 %6,5; n2 %26; n3 %59; n4 %98; n5 %13); rastgele seride 17-20 tekil aday / 1.000 bar (ölçüt <= 0,5).
- Cemal'in 24 işaretiyle (7 benziyor / 17 benzemiyor): D3 AUC 0,630 (%95 0,38-0,87; tam permütasyon p 0,175) -> önceden yazılı hükümle UYUMSUZ (< 0,65). v1 S AUC 0,664; v3 v1'i geçmiyor.
- C hükmü UYUMSUZ olduğu için D (evren taraması, sayım, MUM_IZI5_ONAY.pdf) iş tanımı gereği YAPILMADI.
- Karar etiketi: TESPİT GEÇERSİZ / ÖLÇÜLEMEDİ (v1, v2, v3 üçü de). 'İz değil' yazılmaz; kalıp hakkında hüküm yok.

## v3 TANIM (uygulamada verilen kararlar)

Koordinat b = (fiyat - SMA20) / (üst bant - SMA20); her mum kendi gününe kadarki Bollinger (20, 2) ile; şablonda bantlar görüntüden. Kararlar (ön kayıtta 12 madde):
1. Yalnız 'tam' şablon (20 mum); pencere 16 / 18 / 20 / 22 / 24, bir sonda en küçük D3.
2. Mum başına b ölçüleri pencerenin kendi m mumunda, sonra 20 konuma doğrusal yeniden örnekleme (ardışık ilişkiler 19); 'uzun üst fitil' bayrağı en yakın konumla.
3. Evre: konum oranı < 1/3, orta, >= 2/3; 'gövde SMA üstünde' = (bO + bC) / 2 > 0.
4. F1 = (|bC, bO, bH, bL| konum farkı ortalaması + 6 evre değeri farkı ortalaması) / 2.
5. F2 = (açılış - önceki kapanış, kapanış değişimi, gövde, açılış önceki gövdenin içinde mi: fark ortalaması + (1 - işaret uyumu)) / 2.
6. F3 = (üst / alt fitil b biriminde ve mum boyuna oranla: fark ortalaması + (1 - uzun üst fitil aynı konumda payı)) / 2.
7. tau ve %20 eşiği: 20.000 rastgele gerçek pencere (her uzunluk 4.000; ABD + AVR + BIST); günlük 2016-22 tohum 25112051 + L, haftalık 2001-22 tohum 25112052 + L.
   - günlük tau 0,686 / 0,445 / 0,367; q20 0,487 / 0,398 / 0,329; haftalık tau 0,680 / 0,436 / 0,364; q20 0,487 / 0,389 / 0,328.
   - Aile korelasyonu düşük (F1-F2 0,22-0,24; F1-F3 ~0; F2-F3 ~0,05): üç aile gerçekten ayrı bilgi.
8. Aday = üç aile de q20 altında (telafi yasağı); rastgele gerçek pencerelerin %1,26'sı aday (iki zaman diliminde aynı).
9. D3 = 0,5 F1 / tau1 + 0,25 F2 / tau2 + 0,25 F3 / tau3; tekil = < 15 mum zincirinin en küçük D3'ü.

## SENTETİK (işaretlerden önce; kök 25112053, 200 tohum x 2 üretici x bağlam x gürültü)

| tür | aday payı | gürültü 0 / 0,1 / 0,2 | bağlam |
|---|---|---|---|
| pozitif (gömülü şablon) | %68,9 | 72,1 / 70,2 / 64,5 | dip %95, yatay %76, tepe %36 |
| n1 fitilsiz büyük gövde | %6,5 | 2,3 / 4,8 / 12,3 | |
| n2 fitiller ters | %26,1 | 29,9 / 24,4 / 23,9 | |
| n3 mumlar 2 kat | %59,1 | 61,5 / 60,6 / 55,2 | |
| n4 sert düşüş sonrası aynı mumlar | %98,0 | 98 / 99 / 97 | |
| n5 aynı mumlar, yatay yol | %13,0 | 15,2 / 12,7 / 11,2 | |
| rastgele (tekil / 1.000 bar) | blok 17,2; ry 19,8 | | |

- Ölçüt: pozitif >= %70 GEÇTİ (kıl payı); n1-n5 <= %5 hiçbiri; rastgele <= 0,5 hiçbiri -> GEÇMEDİ. Tanım gevşetilmedi / sıkılaştırılmadı.
- Okuma 1: 'her ailede en iyi %20' eşiği gevşek; rastgele gerçek pencerelerin %1,26'sı geçiyor, 5 uzunluk x her bar ile seride binde 17-20 tekil aday çıkıyor. Bu 'aday' kuralı ayırt etmiyor.
- Okuma 2 (n4): sert düşüşten sonra gömülen aynı mumların b dizisi, dip bağlamındaki pozitifle neredeyse aynı (örnek tohum: bC -0,84 -> +0,93 / dip -0,85 -> +0,93). Kalıbın kendi yükselişi bandı kendisi belirliyor; önceki düşüş b koordinatını kaydırmıyor. Yani n4 bu kurguyla bant konumu için gerçek bir negatif olmadı (HATA 4).
- Okuma 3: n3 (2 kat mum) %59: b biriminde mum boyu bant genişliğiyle birlikte büyüdüğü için F3 / F2 farkı küçük kalıyor (şablonla F3 0,07). Mumun banda göre büyüklüğü v3'te zorunlu kapı değil; bu yüzden ayırmıyor.

## İŞARETLERLE SINAMA (C; işaret dosyası ön kayıt commit'inden sonra açıldı)

24 sayfa (PDF s. 3-26; sayfa 5 sözlü yanıtla 'benzemiyor'): 7 benziyor, 17 benzemiyor, 0 işaretsiz. AUC = P(benziyor sayfanın puanı daha benzer).

| ölçü | AUC | %95 (bootstrap 5000) | tam permütasyon p |
|---|---|---|---|
| D3 (v3) | 0,630 | 0,38-0,87 | 0,175 |
| F1 konum | 0,706 | 0,45-0,92 | 0,065 |
| F2 açılış / kapanış | 0,487 | 0,23-0,76 | 0,549 |
| F3 fitil | 0,639 | 0,35-0,90 | 0,159 |
| v1 S (= v2 sıralama puanı) | 0,664 | 0,40-0,89 | 0,117 |
| v1 gidiş (dizi) | 0,605 | 0,36-0,82 | 0,228 |
| v1 bant | 0,664 | 0,39-0,90 | 0,117 |
| v1 mum özellikleri | 0,429 | 0,19-0,69 | 0,712 |

- HÜKÜM: UYUMSUZ (0,630 < 0,65; önceden yazılı). v2: 24 sayfanın hepsini kabul etmişti (kapıların hepsi geçti), kabul / ret olarak ayırt edemez; v2'nin sıralama puanı v1 S'dir (AUC 0,664).
- Benziyor dediği 7 sayfanın 4'ü D3'te en benzer yarıda (12 / 24); en benzer 2 sayfa (19, 24; ikisi haftalık) ikisi de 'benziyor'. Ama 6, 10, 22 sayfaları 24 içinde 17., 19., 16. sırada.
- Aday kuralı: 24'ün 3'ü aday (16, 19, 26): benziyor 1 / 7, benzemiyor 2 / 17.
- Kısıt: 24 sayfanın hepsi v1 / v2'nin seçtiği bölgeler; hepsinde F1 zaten rastgele dağılımın en iyi %16'sında. AUC önceden süzülmüş dar bir kümede ölçüldü; evrende ayırt gücü bundan farklı olabilir (K8).
- Yeniden üretim: AUC scipy Mann-Whitney ile aynı (D3 0,6303, F1 0,7059); 3 sayfanın F1 / F2 / F3'ü düz döngüyle (v3_duz) aynı; csv'deki v1 S anahtardaki S ile aynı (en büyük fark 5e-6): pencereler doğru (K10).

Sayfa sayfa (D3 sırası 24 içinde; yüzdelik = rastgele gerçek pencere dağılımında):

| sayfa | zaman | Cemal | D3 | D3 sırası | F1 / F2 / F3 yüzdelik | aday |
|---|---|---|---|---|---|---|
| 3 | günlük | benzemiyor | 0,731 | 18 | 0,14 / 0,01 / 0,37 | - |
| 4 | haftalık | benzemiyor | 0,634 | 4 | 0,01 / 0,13 / 0,78 | - |
| 5 | günlük | benzemiyor | 0,699 | 14 | 0,07 / 0,20 / 0,23 | - |
| 6 | günlük | BENZİYOR | 0,726 | 17 | 0,01 / 0,52 / 0,97 | - |
| 7 | haftalık | benzemiyor | 0,742 | 20 | 0,07 / 0,57 / 0,30 | - |
| 8 | haftalık | benzemiyor | 0,952 | 24 | 0,16 / 0,87 / 1,00 | - |
| 9 | haftalık | benzemiyor | 0,690 | 12 | 0,05 / 0,25 / 0,26 | - |
| 10 | günlük | BENZİYOR | 0,732 | 19 | 0,12 / 0,24 / 0,14 | - |
| 11 | haftalık | benzemiyor | 0,632 | 3 | 0,01 / 0,26 / 0,58 | - |
| 12 | günlük | benzemiyor | 0,805 | 22 | 0,13 / 0,29 / 0,78 | - |
| 13 | haftalık | benzemiyor | 0,684 | 11 | 0,09 / 0,36 / 0,01 | - |
| 14 | günlük | benzemiyor | 0,669 | 9 | 0,02 / 0,08 / 0,89 | - |
| 15 | haftalık | benzemiyor | 0,668 | 8 | 0,04 / 0,14 / 0,28 | - |
| 16 | haftalık | benzemiyor | 0,711 | 15 | 0,13 / 0,08 / 0,06 | evet |
| 17 | günlük | benzemiyor | 0,800 | 21 | 0,07 / 0,63 / 0,93 | - |
| 18 | haftalık | benzemiyor | 0,807 | 23 | 0,11 / 0,21 / 0,94 | - |
| 19 | haftalık | BENZİYOR | 0,529 | 1 | 0,00 / 0,05 / 0,05 | evet |
| 20 | günlük | benzemiyor | 0,691 | 13 | 0,05 / 0,35 / 0,28 | - |
| 21 | günlük | BENZİYOR | 0,668 | 7 | 0,02 / 0,02 / 0,92 | - |
| 22 | günlük | BENZİYOR | 0,723 | 16 | 0,09 / 0,24 / 0,26 | - |
| 23 | günlük | BENZİYOR | 0,672 | 10 | 0,05 / 0,30 / 0,20 | - |
| 24 | haftalık | BENZİYOR | 0,548 | 2 | 0,00 / 0,38 / 0,04 | - |
| 25 | günlük | benzemiyor | 0,650 | 6 | 0,01 / 0,31 / 0,49 | - |
| 26 | haftalık | benzemiyor | 0,650 | 5 | 0,06 / 0,06 / 0,09 | evet |

## SAYIM

YAPILMADI: C hükmü UYUMSUZ, iş tanımı D'yi yalnız UYUMLU / KISMEN'de koşturur. Bilgi için: rastgele gerçek pencerelerin %1,26'sı v3 adayı; sentetik rastgele seride binde 17-20 tekil aday. Bu sayılar 'kalıbın veride tekrar sayısı' diye OKUNMAZ.

## ONAY SETİ

YAPILMADI (aynı neden). MUM_IZI5_ONAY.pdf ve mum_izi5_onay_anahtar.json üretilmedi; seçim tohumu 25112055 kullanılmadı.

## KONTROL LİSTESİ (ön kayıttaki yanıtların gerçekleşmesi)

- K1 EVET: negatifler sentetikte sayıyla (n1-n5, rastgele); sınamada permütasyon ve bootstrap.
- K2 EVET (kısmen): b her mumun kendi gününe kadarki bantla; test_gelecege_bakmama (4 kesim noktası) geçti; gerçek veride v3_prefix (30 olay) D yapılmadığı için KOŞULMADI. İşaretler ön kayıt commit'inden sonra açıldı (sıra COMMIT'LER'de).
- K3 EVET: geçerli bar (MI.mi_veri), haftalıkta eksik haftalı pencere atıldı (dağılımda; test_eksik_hafta_penceresi).
- K4 EVET: tekil küme kuralı (test_tekil_kume); sınamada uygulanmadı (sayfa = tek pencere).
- K5 UYGULANMAZ: getiri yok.
- K6 EVET: b birimi ölçek bağımsız.
- K7 EVET: yaşayan evren; getiri yok, sayım yapılmadı.
- K8 EVET: 24 etiket; aralık 0,38-0,87 yazıldı; dar (önceden süzülmüş) küme kısıtı yazıldı.
- K9 EVET: ön kayıt sha'ları; v3_kapi (kontrol + sha + git) sınamadan önce geçti; ayrıştırıcı düzeltmesi SAPMA ile yeni KOD5_SHA.
- K10 EVET: v1 S = anahtar S (5e-6); şablon uzaklığı 0 (test).
- K11 EVET: vektör = düz döngü (6 pencere test + 3 gerçek sayfa); AUC iki yoldan + scipy aynı.
- K12 EVET: hüküm yalnız önceden yazılı eşikle; 'iz' sözü yok; ÖNERİ'deki alt ölçüler 'sonradan bakış' diye ayrıldı.
- K13 EVET: v1 / v2 / haftalık kod sha'ları değişmedi (370d5820 / 1bb586cb / 8f7440d1); defterler, kural_defteri, UC_IZ2 dokunulmadı.
- K14 UYGULANMAZ.

## HATA

1. (ayrıştırma; benim) İşaret ayrıştırıcısı dosyayı görmeden yazıldı ve gerçek biçimi (sayı anahtarlı sözlük, 'isaret' alanı) tanımadı; ilk sınama denemesinde değil, açılışta fark edildi. Düzeltme: 2 satır, SAPMA, yeni KOD5_SHA (4a3146a); tanım (ESIK5_SHA) aynı. Ders: mühürlü dosyanın ŞEMASI (alan adları, değer kümesi; içerik değil) iş tanımında verilmeli ya da ayrıştırıcı şema örneğiyle sınanmalı.
2. (ayrıştırma; benim; ön kayıttan önce yakalandı) 'BENZİYOR'.lower() Python'da 'benzi̇yor' (noktalı i) verir; ilk ayrıştırıcı büyük harfli Türkçe etiketi kaçırırdı. Test yakaladı, düzeltildi.
3. (süreç; ana model) Mühürlü işaret dosyasının commit mesajı (062f14b) bir etiketi açık yazıyordu ('işaretsiz sayfa 5 hiç benzemiyor'); 'git log' ile ön kayıttan önce görüldü. Etkisi: o anda v3 tanımı ve sentetik kod yazılmıştı; tanım değişmedi. Ders: mühürlü dosyanın commit mesajına etiket / sayı yazılmaz.
4. (kurgu; benim) n4 negatifinin kurgusu (10 bar x -%3 düşüş) bant koordinatını beklendiği gibi kaydırmadı: gömülen kalıbın kendi yükselişi bandı belirliyor, b dizisi dip pozitifiyle aynı kaldı. n4 %98 hem 'v3 bant bağlamını ayırmıyor' hem 'n4 gerçek negatif değil' diye okunabilir. Ders: negatif kurgusu önce kendi ölçüsünde sınanmalı (negatifin b dizisi şablondan gerçekten uzak mı).
5. (yorum sınırı) 24 sayfanın hepsi v1 / v2 seçimi; AUC dar kümede. Bu kümede 0,63 çıkması evrende ayırt gücü hakkında güçlü bir şey söylemez (ne iyi ne kötü).

## SAPMA

- Ön kayıttan önce: 062f14b ile etiket sayısı 23 -> 24 (ana model); ayrıştırıcı 'isaret' alanını önceleyecek biçimde değişti, metinlerde '23' kaldırıldı (ön kayıt SAPMA'sında).
- Ön kayıttan ve işaret açılışından sonra, sınamadan önce: ayrıştırıcıya 2 satır (HATA 1); ön kayda yeni KOD5_SHA satırı.
- Rapor (bu dosya) çıktı dosyalarından elle derlendi; koddaki v3_rapor kullanılmadı (D yapılmadığı için).
- Ön kayıttaki K11 '5 pencere' -> testte 6 pencere; K2'deki v3_prefix D yapılmadığı için koşulmadı.

## ÖNERİ (uygulanmadı; v3 tanımı değişmedi)

Aşağıdakiler aynı 24 etikete SONRADAN bakıştır (iç örnek, çoklu karşılaştırma); karar değildir, yeni etiketle sınanmadan kullanılmaz.
1. Cemal'in 'en çoğu konum' sözü veride en çok tutan: F1 konum AUC 0,71 (p 0,065); F1'in evre parçası 0,72 (p 0,050), konum dizisi parçası 0,68. F2 (açılış / kapanış ilişkisi) 0,49: bu 24 sayfada hiç bilgi yok; F3 fitil 0,64. Bir v4 yalnız konum + evre ile kurulabilir, ama yeni ve önceden süzülmemiş etiketlerle sınanmalı.
2. Zaman dilimi farkı: haftalık 12 sayfada AUC 1,00 (2 benziyor, ikisi en üstte), günlük 12 sayfada 0,54 (5 benziyor). Cemal'in 'benziyor'u günlükte başka bir şeye bakıyor olabilir; 2 pozitifle bu çok zayıf.
3. Aday kuralı: 'her ailede en iyi %20' gevşek (rastgele pencerelerin %1,26'sı). Bir dedektör önce sentetik negatiflerde (n1-n5, rastgele) ölçütü geçecek kadar sıkı kapılarla kurulmalı; özellikle mumun banda göre büyüklüğü (n3) zorunlu kapı olmalı.
4. Sınama tasarımı: yeni onay seti D3'ün bütün aralığından (en benzer, orta, uzak) rastgele seçilirse AUC gerçek ayırt gücünü ölçer; yalnız en benzerlerden seçilen set dar kümede kalır.
5. v1, v2, v3 üçü de Cemal'in gözüyle uyuşmadı. Sözlü tarif üç kez sayıya çevrildi ve tutmadı: Cemal'den 7 'benziyor' sayfasında 'benzeten mum / yer'i doğrudan işaretlemesi (2-3 mum daire içine) istenebilir.

## ÖNERİLEN DEFTER SATIRLARI (ana model işler)

- IK_KAYIT Ç231: MUM_IZI EK 5, v3 (bant koordinatında mum dizisi: F1 konum / F2 açılış-kapanış / F3 fitil, telafi yasağı, D3). Sentetik GEÇMEDİ (pozitif %70,2; negatifler %6,5-%98; rastgele binde 17-20). Cemal'in 24 işaretiyle D3 AUC 0,63 (0,38-0,87; p 0,175) -> UYUMSUZ; v1 S 0,66; F1 konum 0,71 (p 0,065). D (tarama, onay PDF) yapılmadı. Karar: TESPİT GEÇERSİZ / ÖLÇÜLEMEDİ (v1-v3). Getiri yok. Commit 27e440e / 04389a9 / 4a3146a / (sonuç).
- IK_GOREV: 25 Kas, MUM_IZI EK 5 v3 + sentetik + işaretlerle sınama: UYUMSUZ, D yapılmadı; açık: Cemal'in kararı (yeni tarif / doğrudan mum işareti / kapatma).
- IK_HATA (3 satır): (a) işaret ayrıştırıcısı mühürlü dosyanın biçimini görmeden yazıldı, açılışta 2 satır düzeltme (ayrıştırma; SAPMA; ders: şema iş tanımında verilsin); (b) mühürlü işaret dosyasının commit mesajı bir etiketi açık yazdı (süreç; ders: mühürlü dosya commit mesajına etiket yazılmaz); (c) n4 negatif kurgusu bant koordinatını kaydırmadı (kurgu; ders: negatif önce kendi ölçüsünde sınanır).
- IK_ACIK: Cemal karar: (1) 7 'benziyor' sayfasında benzeten mumları doğrudan işaretlemek, (2) v4 (yalnız konum + evre) yeni ve D3 aralığına yayılmış bir onay setiyle, ya da (3) bu kalıbı 'tarif sayıya çevrilemedi' diye kapatmak.
