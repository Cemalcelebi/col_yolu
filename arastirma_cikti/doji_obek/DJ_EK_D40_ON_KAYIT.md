# DJ EK ÖN KAYIT — KOL D40 (doji = gövde < 0,40 x boy; Cemal'in eski kodu) (2026-11-27T06:57:25Z)

Ana ön kayıt: DJ_ON_KAYIT.md (bütün öteki kurallar, eşikler, hüküm sırası oradaki gibi). Bu dosya D40 getirileri (R15 / U2 / D2 / çıkış) hesaplanmadan ÖNCE commit + push edilir. ANA ölçüm sonucu bu kayıttan önce yayımlandı; D40 eşiği ve basamakları iş tanımından (ana model mesajı) gelir, sonuca göre seçilmedi.

## Mühürler

D40_KOD_SHA: a6a511ccc57f0eb743325c7f7e391c00327d14ebca47dc1c639f3db632b6540f
D40_ESIK_SHA: a1cc669e6fec8aa298609595da03e7e1d9e0bbf75fd6156dee9b0bea8ca98179
DJ_ESIK_SHA: 94ffcc2e0b8f94f45ca2f40f6d2c6588b57b4ced9fdd3ca702c6e9fbfed589ac
DOSYA_olay_D40_ABD.pkl: 2c40e8abddd0d24bd84a00df38dc5740d07585a37ec89af12e7ebee392d6c45f
DOSYA_getiri_taban_ABD.pkl: 63860a2dacbbb3a3a3689358071a5a00667d23bea0d9be87330b03c6ab3a35b5
DOSYA_olay_D40_AVR.pkl: 10ce15b8ebedeef4b1e6c104d056a4daa7f51a2f5b5f9a4e930bf6ed4796994c
DOSYA_getiri_taban_AVR.pkl: f65c0262b7c4917cda61af7ba864c9cc52e82181f29a71b91bf4bb7769c5d1e5
D40_SAYIM_SHA: fae2ce3db1e0739a6e56f0befbbba9e5001a6cdf57ffefe106e200d01d8d1f8c

## Eşik sözlüğü (DJ_D40_ESIK)

```json
{
 "surum": "DJ-D40-1.0",
 "ana_esik_sha_ref": "DJ_ON_KAYIT.md DJ_ESIK_SHA (ana ölçümün bütün kuralları aynen)",
 "doji": "DOJİ_D40(t) <=> |C - O| < 0,40 x (H - L) (KATI küçüktür; GEN10_COL_OGREN v5 tanımı aynen) VE (H - L) >= 0,5 x ORT_BOY VE (H - L) > 0 VE fiyat adımına yapışmış değil (ANA ile aynı)",
 "govde": 0.4,
 "kati": true,
 "obek": "ANA ile aynı (sıra farkı <= 3, takvim satırı <= 6, seviye bandı 0,5 ATR20, sınır dahil)",
 "k": {
  "basamak": [
   1,
   2,
   3,
   4,
   5,
   7
  ],
  "tanim": "olay = öbeğin k'inci dojisinin barı; k = 1, 2, 3, 4 (öbeğin 4. dojisi), 5-6 (= öbeğin 5. dojisi; öbek >= 5), 7+ (= öbeğin 7. dojisi; öbek >= 7); her basamakta öbek başına en çok bir olay"
 },
 "olcu": "ANA ile aynı (R15, TOPLAM FARK, SEÇİM, U2 / D2, ASİMETRİ, BÜYÜKLÜK, ÇIKIŞ + DEVAM, DÖNÜŞ, bağlam); taban = ANA ölçümünün taban getiri dosyası (getiri_taban_*.pkl; aynı her 5. bar günleri; sonucu D40'tan bağımsız)",
 "hukum": "ANA ile aynı kural (DJ_ESIK['hukum']); BH ailesi 6 basamak x 8 ölçü = 48 satır; DOZ: 1 -> 2 -> 3 -> 4 -> 5-6 -> 7+ art arda farklar tek yönlü (iki ABD döneminde, aynı yönde) VE (k = 3 - 1) ya da (k = 4 - 1) aralığı iki dönemde sıfırı dışlıyor",
 "rastgele": {
  "seri": 300,
  "bar": 1000,
  "tohum": 2712,
  "tanim": "sentetik rastgele seri (C log-getiri N(0, 0,02); O = önceki C x exp(N(0, 0,008)); H = maks(O, C) x (1 + |N(0, 0,01)|); L = min(O, C) x (1 - |N(0, 0,01)|)); aynı doji / öbek kodu (uygunluk süzgeci yok); bin barda k basamağı sıklığı ANA ve D40 için; 'rastgele seride de gerçekteki kadar sık' ise öbek tespiti tek başına ayırt edici değildir (bilgi)"
 },
 "sira": "ANA ölçüm bitti (859ac7f) -> D40 getirisiz sayım + rastgele seri karşılaştırması -> DJ_EK_D40_ON_KAYIT.md commit + push -> ik_kontrol_kapisi -> D40 ölçüm (bir kez) -> DJ_RAPOR.md 'EK: D40' + dj_sonuc.json 'd40'"
}
```

## GETİRİSİZ SAYIM (D40)

Doji payı (bütün geçerli barlar): ABD %40,8, AVR %41,2 (ANA kolunda yaklaşık %10).

| hücre | uygun hisse-gün | k | olay | bin hisse-günde | farklı ay | en kalabalık 3 ay payı | hisse |
|---|---|---|---|---|---|---|---|
| ABD|d1619 | 2003073 | k=1 (tek doji) | 450579 | 224,94 | 48 | 0,076 | 2729 |
| ABD|d1619 | 2003073 | k=2 | 236592 | 118,11 | 48 | 0,074 | 2695 |
| ABD|d1619 | 2003073 | k=3 | 105955 | 52,90 | 48 | 0,079 | 2651 |
| ABD|d1619 | 2003073 | k=4 | 44321 | 22,13 | 48 | 0,083 | 2564 |
| ABD|d1619 | 2003073 | k=5-6 | 17885 | 8,93 | 48 | 0,087 | 2426 |
| ABD|d1619 | 2003073 | k=7+ | 2775 | 1,39 | 48 | 0,098 | 1490 |
| ABD|d2022 | 1958918 | k=1 (tek doji) | 451821 | 230,65 | 36 | 0,099 | 3748 |
| ABD|d2022 | 1958918 | k=2 | 218503 | 111,54 | 36 | 0,102 | 3726 |
| ABD|d2022 | 1958918 | k=3 | 89050 | 45,46 | 36 | 0,110 | 3661 |
| ABD|d2022 | 1958918 | k=4 | 33972 | 17,34 | 36 | 0,121 | 3549 |
| ABD|d2022 | 1958918 | k=5-6 | 12086 | 6,17 | 36 | 0,130 | 3199 |
| ABD|d2022 | 1958918 | k=7+ | 1530 | 0,78 | 36 | 0,156 | 1155 |
| AVR|d1619 | 402902 | k=1 (tek doji) | 89975 | 223,32 | 48 | 0,070 | 480 |
| AVR|d1619 | 402902 | k=2 | 45826 | 113,74 | 48 | 0,073 | 475 |
| AVR|d1619 | 402902 | k=3 | 19520 | 48,45 | 48 | 0,081 | 468 |
| AVR|d1619 | 402902 | k=4 | 7818 | 19,40 | 48 | 0,088 | 459 |
| AVR|d1619 | 402902 | k=5-6 | 2994 | 7,43 | 48 | 0,110 | 441 |
| AVR|d1619 | 402902 | k=7+ | 398 | 0,99 | 47 | 0,131 | 246 |
| AVR|d2022 | 325208 | k=1 (tek doji) | 73887 | 227,20 | 36 | 0,100 | 514 |
| AVR|d2022 | 325208 | k=2 | 35735 | 109,88 | 36 | 0,097 | 512 |
| AVR|d2022 | 325208 | k=3 | 14285 | 43,93 | 36 | 0,109 | 506 |
| AVR|d2022 | 325208 | k=4 | 5265 | 16,19 | 36 | 0,122 | 498 |
| AVR|d2022 | 325208 | k=5-6 | 1849 | 5,69 | 36 | 0,134 | 467 |
| AVR|d2022 | 325208 | k=7+ | 217 | 0,67 | 34 | 0,180 | 166 |

Öbek son uzunluğu dağılımı (BİLGİ): ABD|d1619: {'1': 213763, '2': 130537, '3': 61660, '4': 26561, '5': 10761, '6': 4464, '7': 1761, '8+': 1072}; ABD|d2022: {'1': 233192, '2': 129321, '3': 55211, '4': 21981, '5': 7794, '6': 2815, '7': 966, '8+': 541}; AVR|d1619: {'1': 44084, '2': 26291, '3': 11751, '4': 4834, '5': 1878, '6': 732, '7': 246, '8+': 159}; AVR|d2022: {'1': 38123, '2': 21441, '3': 9030, '4': 3432, '5': 1196, '6': 446, '7': 143, '8+': 76}

## Rastgele seri karşılaştırması (getirisiz; bin barda)

Sentetik rastgele seri (300 seri x 1000 bar): doji payı ANA %4,6, D40 %29,3.

| kol | kaynak | k=1 (tek doji) | k=2 | k=3 | k=4 | k=5-6 | k=7+ |
|---|---|---|---|---|---|---|---|
| ANA | rastgele seri | 42,02 | 3,77 | 0,30 | 0,02 | 0,00 | 0,00 |
| D40 | rastgele seri | 178,99 | 75,98 | 26,63 | 8,28 | 2,46 | 0,22 |
| D40 | gerçek ABD|d1619 | 224,94 | 118,11 | 52,90 | 22,13 | 8,93 | 1,39 |
| D40 | gerçek ABD|d2022 | 230,65 | 111,54 | 45,46 | 17,34 | 6,17 | 0,78 |

## Yorum noktaları (ölçümden önce)

1. D40 kolu ANA ölçümün tanımını, ön kaydını ve sonucunu değiştirmez; ANA sonuç (859ac7f) bu ön kayıttan önce yayımlandı (D40 getirisi görülmedi).
2. Doji eşiği KATI küçüktür (< 0,40), eski kodla aynı; ANA kolu <= 0,10 idi. Öteki bütün kurallar ANA ile aynı kod yoluyla (dj_tara_hisse, kati=True).
3. Basamaklar: k = 4 satırı öbeğin 4. dojisi (ANA'daki '4+' ile aynı olay), k = 5-6 satırı öbeğin 5. dojisi, k = 7+ satırı öbeğin 7. dojisi; öbek başına her basamakta en çok bir olay; aynı öbek birden çok basamağa girer (bağımsız değil).
4. Taban (rastgele gün, T1, p_h, q_h, h_h, T10, dönüş tabanı) ANA ölçümünün taban getiri dosyasından okunur (getiri_taban_*.pkl; doji tanımından bağımsız).
5. DOZ kuralı 6 basamağın hepsinde art arda tek yön ister (n'ye bakmadan; küçük basamaklar gürültülüdür, kural önceden böyle).
6. Rastgele seri karşılaştırması BİLGİDİR: gerçek veri sıklığı uygun hisse-gün paydasıyla, rastgele seri ham bar paydasıyla; ikisi kabaca karşılaştırılır.
7. Hüküm etiketleri ANA ile aynı; n < 1.000 olan basamakta aralık sıfırı içerirse ÖLÇÜLEMEDİ.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban aynı hissenin aynı hücredeki rastgele (her 5. bar) günleri: TOPLAM FARK = R15 - T1, U2 / D2 / büyüklük için p_h / q_h / h_h aynı hisseden; ATR ölçekli eşikler (oynaklığın mekanik etkisi ATRP20 ile ölçeklenir); D2 aynası ve asimetri mekanik üstünlüğü ölçer; tek doji (k = 1) ve herhangi gün iki taban; k farkları aynı ay ağırlıklarıyla; SEÇİM = R15 - PİYASA(t) |
| K2 | geleceğe bakma | EVET | doji / öbek / k t barına kadarki barlarla (test: t + 1 ve sonrası bozulunca olaylar aynı); ORT_BOY t - 10 .. t - 1; ATR20 ve ADIM t'ye kadar; sonuç sütunları ayrı fonksiyonda, yalnız kapıdan sonra; olay dosyası ile getiri dosyası ayrı; öbeğin son uzunluğu yalnız sayımda (bilgi); veri <= 2022-12-31 assert |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli barları (H > L, V > 0, O/H/L/C sonlu > 0); ölü / fiyat adımına yapışmış bar doji sayılmaz (ADIM kuralı, test); öbekte takvim satırı farkı > 6 bağlanmaz; 15 bar <= 30 takvim satırı; giriş P2 evreninde |
| K4 | tekilleştirme | EVET | öbek başına her k satırında bir olay (4+ = 4. doji; sonrakiler olay değil); olaylar örtüşebilir, çıkarım ay kümeli bootstrap; n ve farklı ay ayrı yazılır; medyan R15 yazılır; taban her 5. bar |
| K5 | giriş fiyatı | EVET | giriş = t + 1 barının açılışı; çıkış devamı çıkış barından sonraki açılıştan (e + 1); P15 de giriş satırından |
| K6 | veri birimi | EVET | OS / MI bölünme düzeltmeli açık kopya (YO ile aynı depo); getiriler oransal, yerel para; pazar içi karşılaştırma; eşikler ATR oranlı (birimden bağımsız); fiyat adımı kuralı birimden bağımsız (kendi fiyat farklarından) |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı): sonuç yukarı yanlı; TOPLAM FARK aynı hisseye göre olduğu için yanlılık kısmen düşer; raporda yazılır; kasa açılmaz |
| K8 | örneklem ve dönem | EVET | n >= 1.000 değilse ÖLÇÜLEMEDİ; iki ABD + iki AVR dönemi; BH q 0,10 (48 satır aile); rastgele seri karşılaştırması sıklığın ayırt ediciliği için (bilgi) |
| K9 | ön kayıt | EVET | DJ_EK_D40_ON_KAYIT.md: D40_KOD_SHA, D40_ESIK_SHA, olay_D40 dosya sha'ları, D40 SAYIM_SHA; ana ön kayda atıf; D40 kapısı: kontrol + sha + commit + push + kod temiz; getiri_D40 dosyası varsa ikinci koşu DURUR; ana ölçümün tanımı / sonucu değişmez |
| K10 | ayrıştırma | EVET | doji / öbek kuralı sentetik pozitif / negatif serilerle (yakalama >= %95, yanlış kabul <= %5); uygunluk maskesi YO.yo_ornek_maske ile 5. barlarda birebir; dokunma YO.yo_ilk_dokunma; kaynak npz sha YO ön kaydıyla aynı; PDF'te gerçek örnekler gözle denetlenir |
| K11 | yeniden üretim | EVET | rapordan önce >= 3 satır olay + getiri dosyalarından bağımsız kısa kodla yeniden üretilir; rapordaki sayılar dj_sonuc.json'dan basılır |
| K12 | ifade | EVET | 'emare / etkili' sözü yalnız hüküm kuralıyla; ABD tek dönem 'TEK DÖNEM'; sayı ile yorum ayrı cümlede; evren bugün yaşayanlar; fiyat değişimi gerçek kâr değil (komisyon / kayma yok) |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_dj); mevcut modüller ve defter dosyaları değişmez (yalnız import; SEKIL_DEVAM / WEB_DESEN içe alınmaz); yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez, kasa açılmaz |

## SAPMA

(yok)
