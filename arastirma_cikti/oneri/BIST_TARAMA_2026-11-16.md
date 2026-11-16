# BIST CANLI TARAMA — 16 Kasım 2026 (öneri modülü TARAMA kapısı; ADAY sıralaması, öneri değil)

> ÖLÇÜLMÜŞ SİNYAL YOK. BIST'te ölçülmüş iz yok (IZ_DEFTERI). S6 / S5 göz aracıdır; sektör rüzgârı ABD'de EMARE, BIST'te ölçülmedi; üretim D13 İZ DEĞİL.
> Bu tablo bir aday sıralamasıdır; hiçbir satır 'al' ya da 'öneri' değildir.

## A. ÖN KAYIT (koşudan önce yazıldı: 2026-11-16 ~12:35 UTC; kural ve eşikler iş tanımından birebir, sonuç görüldükten sonra değişmez)

İş tanımı: arastirma_cikti/oneri/BIST_TARAMA_IS_TANIMI_2026-11-16.md. Koşu betiği: arastirma_cikti/oneri/tarama_kosu.py (sha256 raporun B bölümünde).

- Evren: sektor_BIST.csv'nin 583 sembolü + izleme listesinde olup CSV'de olmayanlar (TKNKA, SVGYO, KARCL) + '.IS'; XU100.IS bağlam için.
- Veri: yfinance, period 3y, interval 1d, auto_adjust=False (ekran fiyatı; Yahoo bölünme düzeltmeli OHLC, temettü düzeltmesi yok). Geçerli bar: H>L, V>0, C>0, O>0, sonlu (SY.sy_veri_hazirla süzgeci; kriz kesiği UYGULANMAZ: canlı tarama).
- Karar günü: bugünden (16 Kas, seans açık: 12:30 UTC = 15:30 TR) ÖNCEKİ son tam bar = 2026-11-13. Bütün ölçüler yalnız karar günü ve öncesi; 16 Kas barı yalnız BİLGİ sütunu.
- Ölçüler: iş tanımı §2 (1-8). S6 = S6_TABAN.s6_taban (varsayılan / seçilen eşikler, değişmez). S5 = SIKISMA_OBEK.so_s5(d, 'BIST') son 20 geçerli barda ev5. Rüzgâr = D9_YENIDEN.d9_ruzgar_ref(veri, alt_bist, tarih=karar). Fon lekesi = G.pkl'de hissenin son raporlu ayında FON_IZI.FI_TASFIYE_RE şirketlerinin lotu > 0. Uzak / MSCI listeleri iş tanımındaki gibi. Likidite = son 20 geçerli bar ort(C x V) TL; evrenin alt %20'si (ölçülebilen hisseler içinde 20. yüzdelik altı) HARİÇ.
- Sıçrama şüphesi (BİLGİ, puana girmez): son 260 geçerli barda tek günde |C/C_önceki - 1| > %11 (BIST günlük sınırı %10; bedelli / bölünme düzeltmesi eksik olabilir).
- ŞART (hepsi): LEKE yok, Uzak değil, likidite alt %20'de değil, son 10 barda S6 KIRILDI yok.
- PUAN: S6 açık bölge +2; S6 AL son 10 bar +2; S5 karar günü son 20 bar +1; sektör rüzgârı +1; tavana uzaklık [-%5, +%3] +1; 250 gün zirvesinden düşüş >= %30 +1; 20 günde en büyük hacimli gün getirisi >= +%5 +1. Eşitlikte 20 gün işlem değeri yüksek olan üstte. Hesaplanamayan ölçü 'HESAPLANAMADI' yazılır, puana girmez (0).
- Tavana uzaklık: açık bölge varsa açık bölgenin tavanı (kutu_ust), yoksa son 10 bardaki AL'ın kırdığı tavan (önceki barın TAVAN'ı); ikisi de yoksa HESAPLANAMADI.
- Çıktı: ilk 15 + izleme listesi (PNLSN, FORTE, GWIND, EUPWR, SEGMN, TKNKA, GIPTA, SVGYO, KARCL, YEOTK, HDFGS, SKBNK).

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt; HAYIR ya da boş = kos çalışmaz)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | canlı aday sıralaması; getiri / eş karşılaştırması yapılmıyor, iddia yok ('ölçülmüş sinyal yok') |
| K2 | geleceğe bakma | EVET | her hisse karar günü (13 Kas) barında kesilir (tarama_kosu.py kes()); 16 Kas barı yalnız bilgi sütunu; fon tablosu bilinme <= karar denetlenir; rüzgâr tarih=karar |
| K3 | geçerli bar | EVET | H>L, V>0, C>0, O>0 süzgeci (SY.sy_veri_hazirla ile aynı, kriz kesiksiz); yarım 16 Kas barı karardan atılır |
| K4 | tekilleştirme | EVET | hisse başına tek satır; S5 olayı so_s5 ev5 (20 bar ara); S6 AL / KIRILDI bölge başına bir kez (durum makinesi) |
| K5 | giriş fiyatı | UYGULANMAZ | giriş / getiri ölçülmüyor; DOSYA ve RİSK kapıları ayrı iş |
| K6 | veri birimi | EVET | tek kip: Yahoo auto_adjust=False (ekran fiyatı, bölünme düzeltmeli); işlem değeri TL = C x V (lot); mutlak günlük değişim > %11 sıçrama şüphesi sütunu |
| K7 | hayatta kalma | EVET | evren bugünün listesi (sektor_BIST.csv); canlı tarama için doğal, ölçüm iddiası yok; raporda yazılı |
| K8 | örneklem ve dönem | UYGULANMAZ | ölçüm / bulgu yok; tek gün kesiti aday sıralaması |
| K9 | ön kayıt | EVET | şart, puan ve eşikler iş tanımında ve bu A bölümünde koşudan önce; betik sha raporda; sonuçtan sonra yalnız gösterim |
| K10 | ayrıştırma | EVET | metin ayrıştırma yalnız son_rapor.txt BEKLE satırı (iş tanımı listesiyle mekanik kıyas); fon tablosu FI_TASFIYE_RE ile |
| K11 | yeniden üretim | EVET | ilk 2 adayın puanı ve 3 ölçüsü ham OHLC'den bağımsız kısa kodla yeniden üretilir (raporda) |
| K12 | ifade | EVET | 'aday', 'göz aracı', 'ölçülmüş sinyal yok' dili; al / öneri sözü yok; taban oranlar yazılı |
| K13 | süreç | EVET | yasak dosyalara dokunulmaz (git status raporda); modüller yalnız import; commit yok; e-posta / anahtar taraması çıktıda |
| K14 | boyut (gerçek para) | UYGULANMAZ | bu iş TARAMA kapısı; boyut / çıkış kuralları RİSK kapısında ana model yazar; taban oranlar (10x ~%1) raporda |

<!-- KOSU SONUCU BU SATIRDAN SONRA (tarama_kosu.py yazar) -->

## B. ÖZET (karar günü 2026-11-13; bulgu dili)

- Taranan: 586 hisse indirildi, 586 ölçüldü; indirme hatası 0. ŞARTI GEÇEN: 284.
- Şartı geçenlerde puan dağılımı: 6 puan: 1, 5 puan: 2, 4 puan: 8, 3 puan: 21, 2 puan: 45, 1 puan: 184, 0 puan: 23.
- İlk 5: EYGYO (6 puan); MACKO (5 puan); PRKME (5 puan); LILAK (4 puan); VBTYZ (4 puan).
- Piyasa (XU100, 2026-11-13): 60 gün -17,7%, 120 gün -14,2%, 250 gün +11,4%; 250 gün zirvesinden -21,7% (zirve 2026-05-11). 16 Kas (yarım bar, bilgi): +0,2%.
- Sektör rüzgârı: rüzgârlı hisse 0 (60 gün piyasa medyanı -32,9%); üretim raporu 13 Kas: rüzgârlı sektör 0, piyasa medyanı 60 g -%33,3.
- BIST fon krizi: 31 Ağu 2026 sonrası olağanüstü dönem (tasfiye fonları, tedbirler); 250 gün ölçüleri bu dönemi içerir. Mart 2027 fon tasfiye sonu.
- Üretim D13 BEKLE (son_rapor.txt, sha 4938651cf4f5): ONCSM, METRO, ALBRK, HUNER, EGEGY, ULUFA — iş tanımı listesiyle AYNI.
- Likidite eşiği (alt %20, 20 gün ort işlem değeri): 8,31 mn TL; 5.900 TL'lik alım için şartı geçen hiçbir hissede fiili likidite sorunu yok (en düşük şartı geçen > 8,3 mn TL/gün).
- Koşu: kod sha256 `c9b813c9b559cc70ec641b85ed7e69777b03725b97dffd8351d9c652fb4692d0`; indirme 2026-11-16T12:33:23.736340Z.

## C. İLK 15 (şartı geçenler; puan, eşitlikte likidite)

Sütunlar: S6 açık = karar gününde açık taban bölgesi (bölge gün sayısı, açılış sınıfı); AL10 = son 10 barda S6 AL; S5 20 = son 20 barda S5 karar günü (sınıf); Rüzgâr = D9 bayrağı (ruz = sepet - piyasa medyanı, 60 g); Tavana = C / tavan - 1; Zirve250 = C / 250 g en yüksek kapanış - 1; Hacim günü = son 20 barın en yüksek hacimli günü (bilanço tepkisi vekili); H5/60 = son 5 gün / 60 gün ort hacim; ATR% = 250 g ort TR / C_önceki.

| # | Hisse | Puan | Şart | S6 açık (gün, sınıf) | S6 AL10 | S5 20 | Rüzgâr (ruz) | Tavana | Zirve250 | Hacim günü getiri | r60 | r120 | r250 | Konum120 | ATR% | H5/60 | Likidite (mn TL) | Leke / Uzak / MSCI / D13 | Not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | EYGYO | 6 | E | E (8g, DIP) | - | E 2026-11-13 DIP | - +8% | -4,3% | -64% | +9,6% (2026-10-20) | -30% | -30% | -60% | 0,11 | +5,3% | 0,64 | 10,2 | - |  |
| 2 | MACKO | 5 | E | - | E 2026-11-04 | E 2026-11-03 DIP | - -11% | -4,3% | -49% | -2,2% (2026-11-06) | -31% | -46% | -41% | 0,05 | +4,9% | 0,70 | 11,9 | - | sıçrama 1 |
| 3 | PRKME | 5 | E | E (8g, DIP) | - | - | - -0% | -3,8% | -54% | +6,7% (2026-11-04) | -36% | -32% | -28% | 0,08 | +4,9% | 0,30 | 11,4 | - |  |
| 4 | LILAK | 4 | E | E (8g, DIP) | - | - | - -4% | -3,5% | -55% | +0,6% (2026-11-02) | -35% | -45% | -30% | 0,09 | +4,1% | 0,62 | 62,7 | - |  |
| 5 | VBTYZ | 4 | E | E (8g, DIP) | - | - | - -11% | -4,5% | -46% | +1,0% (2026-11-04) | -41% | -15% | +25% | 0,11 | +5,6% | 0,87 | 23,2 | - |  |
| 6 | MERKO | 4 | E | E (8g, DIP) | - | - | - -2% | -3,2% | -95% | -2,0% (2026-10-21) | -33% | -56% | -93% | 0,05 | +4,7% | 0,71 | 20,3 | - | sıçrama 1 |
| 7 | GARFA | 4 | E | E (8g, DIP) | - | - | - -1% | -6,1% | -38% | +5,0% (2026-10-21) | -17% | -24% | -12% | 0,15 | +4,0% | 0,66 | 19,8 | - |  |
| 8 | KZGYO | 4 | E | E (8g, DIP) | - | - | - +8% | -2,6% | -48% | -2,8% (2026-10-22) | -18% | -32% | -35% | 0,15 | +4,6% | 0,24 | 14,8 | - | sıçrama 1 |
| 9 | PNSUT | 4 | E | E (8g, DIP) | - | - | - -2% | -3,5% | -48% | +2,0% (2026-10-28) | -12% | -33% | -17% | 0,12 | +4,2% | 0,26 | 12,4 | - |  |
| 10 | GOODY | 4 | E | E (11g, DIP) | - | - | - -1% | -4,5% | -52% | +1,0% (2026-11-04) | -29% | -33% | -30% | 0,02 | +3,6% | 0,77 | 12,1 | - |  |
| 11 | FADE | 4 | E | E (8g, DIP) | - | - | - -2% | -4,6% | -46% | +3,0% (2026-11-09) | -34% | -38% | -25% | 0,09 | +4,1% | 0,79 | 8,4 | - |  |
| 12 | ENERY | 3 | E | E (8g, YOL) | - | - | - -3% | -0,2% | +0% | -9,0% (2026-10-21) | +65% | +69% | +54% | 1,00 | +4,2% | 0,51 | 589,1 | - |  |
| 13 | MIATK | 3 | E | E (8g, DIP) | - | - | - -12% | -5,6% | -58% | -6,6% (2026-10-16) | -20% | -48% | -41% | 0,07 | +5,8% | 0,38 | 536,1 | - | sıçrama 2 |
| 14 | AKSA | 3 | E | - | E 2026-11-13 | - | - -1% | +2,0% | -15% | -0,6% (2026-10-26) | -2% | +5% | +3% | 0,38 | +3,3% | 0,97 | 168,7 | - |  |
| 15 | ATATP | 3 | E | - | E 2026-11-06 | - | - -11% | -12,4% | -43% | -4,7% (2026-11-13) | -41% | -4% | +31% | 0,00 | +5,8% | 1,14 | 138,2 | - | sıçrama 1 |

## D. İZLEME LİSTESİ (Cemal; aynı ölçüler, puanlı; '#' = genel sıra)

| # | Hisse | Puan | Şart | S6 açık (gün, sınıf) | S6 AL10 | S5 20 | Rüzgâr (ruz) | Tavana | Zirve250 | Hacim günü getiri | r60 | r120 | r250 | Konum120 | ATR% | H5/60 | Likidite (mn TL) | Leke / Uzak / MSCI / D13 | Not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 71 | PNLSN | 2 | E | - | - | - | - +3% | HESAPLANAMADI | -41% | +5,9% (2026-11-11) | -26% | -25% | -18% | 0,31 | +4,6% | 1,17 | 11,7 | - |  |
| 126 | FORTE | 1 | E | - | - | - | - -11% | HESAPLANAMADI | -35% | -1,4% (2026-11-10) | -33% | +4% | +20% | 0,30 | +5,0% | 0,88 | 64,5 | - |  |
| 143 | GWIND | 1 | E | - | - | - | - -1% | HESAPLANAMADI | -39% | +3,5% (2026-11-10) | -16% | -26% | -18% | 0,25 | +3,4% | 0,98 | 44,3 | - |  |
| 33 | EUPWR | 2 | E | - | - | - | - -2% | HESAPLANAMADI | -61% | +10,0% (2026-11-13) | -56% | -41% | +48% | 0,07 | +6,6% | 1,50 | 803,2 | - | sıçrama 1 |
| 136 | SEGMN | 1 | E | - | - | - | - -1% | HESAPLANAMADI | -78% | +2,7% (2026-10-16) | -72% | -73% | -22% | 0,08 | +7,6% | 1,31 | 50,7 | - | sıçrama 1 |
| 265 | TKNKA | 0 | E | - | - | - | - HESAPLANAMADI | HESAPLANAMADI | HESAPLANAMADI | +0,3% (2026-11-11) | HESAPLANAMADI | HESAPLANAMADI | HESAPLANAMADI | - | HESAPLANAMADI | - | 131,4 | - | sıçrama 1; HESAPLANAMADI (250 geçerli bar yok); HESAPLANAMADI (290 geçerli bar yok) |
|  | GIPTA | 2 | H | - | - | - | - -3% | HESAPLANAMADI | -71% | +7,1% (2026-11-06) | -60% | -65% | -67% | 0,12 | +7,3% | 0,46 | 49,7 | LEKE | sıçrama 2 |
| 270 | SVGYO | 0 | E | - | - | - | - HESAPLANAMADI | HESAPLANAMADI | HESAPLANAMADI | -3,3% (2026-10-19) | -76% | -82% | HESAPLANAMADI | 0,07 | HESAPLANAMADI | 0,45 | 66,2 | - | sıçrama 4; HESAPLANAMADI (250 geçerli bar yok); HESAPLANAMADI (290 geçerli bar yok) |
| 263 | KARCL | 0 | E | - | - | - | - HESAPLANAMADI | HESAPLANAMADI | HESAPLANAMADI | +1,9% (2026-10-23) | HESAPLANAMADI | HESAPLANAMADI | HESAPLANAMADI | - | HESAPLANAMADI | - | 354,7 | - | sıçrama 1; HESAPLANAMADI (250 geçerli bar yok); HESAPLANAMADI (290 geçerli bar yok) |
|  | YEOTK | 1 | H | - | - | - | - -8% | HESAPLANAMADI | -47% | -0,7% (2026-11-10) | -23% | -42% | +79% | 0,21 | +5,8% | 1,29 | 327,6 | LEKE |  |
| 98 | HDFGS | 1 | E | - | - | - | - -12% | HESAPLANAMADI | -72% | -9,4% (2026-10-19) | -49% | -59% | -75% | 0,19 | +7,1% | 1,14 | 116,8 | - | sıçrama 1 |
|  | SKBNK | 1 | H | - | - | - | - +23% | HESAPLANAMADI | -81% | -1,8% (2026-11-10) | -39% | -73% | -54% | 0,05 | +4,8% | 0,98 | 251,4 | LEKE | sıçrama 2 |

YEOTK (Cemal'in pozisyonu / tezi): kapanış 27,86 TL; r60 -22,7%, r120 -42,0%, r250 +78,6%; 250 g zirveden -46,8%; konum120 0,21; S6 durum taban yok (açık -, AL10 -, KIRILDI10 -); S5 20 -; rüzgâr -; hacim günü 2026-11-10 -0,7%; puan 1; şart H.

## E. HARİÇ TUTULANLAR

- LEKE (fon tablosunda son raporlu ayda tasfiye fonu pozisyonu): 211
- Uzak listesi: 11 (MANAS, SKYLP, TEHOL, DSTKF, OZATD, TRHOL, ODINE, IEYHO, PEKGY, ANELE, GUNDG)
- Likidite alt %20: 117
- Son 10 barda S6 KIRILDI: 0
- Birden çok neden çakışabilir; şartı geçmeyen toplam 302. MSCI çıkarma bayrağı (şart değil): LYDHO, TEHOL, ODINE, IEYHO, PEKGY, ALKLC.
- Son barı karar gününden eski (işlem görmüyor / durdurulmuş olabilir): 9 (LYDHO, LYDYE, HOROZ, TEHOL, OZATD, ALVES, MEGAP, DUNYH, TERA)
- İşlem görmüyor (son geçerli bar karar gününden 5 iş gününden eski; ölçü HESAPLANAMADI, şart dışı): 2 (DUNYH, TERA)
- BİLGİ (şart değişmedi): LEKE'lilerin 33'i son raporlu ayı 2026-07'den eski olan hisseler (fonlar o aydan sonra tutmamış olabilir); bunlardan leke dışında şartı geçip puanı >= 3 olan: ETILR (3), BAYRK (3).

## F. VERİ NOTU

- Kaynak yfinance (Yahoo), 3 yıl günlük, auto_adjust=False (ekran fiyatı; bölünme düzeltmeli, temettü düzeltmesiz). Karar günü 2026-11-13 (son TAM bar). 16 Kas barı seans açıkken indirildi (YARIM): yalnız 'bilgi_16kas_*' sütunlarında, hiçbir ölçüye girmedi.
- İndirme hatası 0: yok
- Son 260 barda tek günde |%11| üstü sıçrama olan hisse: 181 (bedelli / bölünme düzeltme eksiği olabilir; S6 / S5 ölçüsünü bozabilir; puana girmez, tabloda 'sıçrama' notu).
- Fon tablosu G.pkl: KAP aylık portföy raporları, en geç rapor ayı 2026-09 (bilinme <= 12 Eki); tasfiye fonları sonradan haftalık rapor verir, bu tabloda yok: LEKE alt sınırdır.
- Hayatta kalma: evren bugünün listesi; canlı tarama için doğal.

## G. ÖLÇÜLMÜŞ SİNYAL YOK — taban oranlar

Bu sıralamanın hiçbir puanı getiri için ölçülmedi. S6 / S5 göz araçları; sektör rüzgârı ABD'de EMARE, BIST'te ölçülmedi; D13 İZ DEĞİL.
Taban oranlar (ONERI_DEFTERI risk süzgeci): BIST'te 12 ayda ikiye katlanma %4-7, yarıya inme %6-7; oynak havuzda %9-16 / %17-21. 3 yılda 10x: ABD mikro-cap ~%1, BIST USD ~%1,85.
Claude yatırım danışmanı değildir; alım-satım kararı Cemal'indir.

## H. DOSYA KAPISI İÇİN İLK 5 (KAP'ta bakılacaklar)

- EYGYO (6 puan, XGMYO): 3Ç26 gelir / kâr ivmesi (hacim günü 2026-10-20 +9,6%), isimli sözleşme / iş ilişkisi, nakit, borç, seyrelme / bedelli (sıçrama 0), going concern, fon / tedbir / SPK lekesi.
- MACKO (5 puan, XBLSM): 3Ç26 gelir / kâr ivmesi (hacim günü 2026-11-06 -2,2%), isimli sözleşme / iş ilişkisi, nakit, borç, seyrelme / bedelli (sıçrama 1), going concern, fon / tedbir / SPK lekesi.
- PRKME (5 puan, XMADN): 3Ç26 gelir / kâr ivmesi (hacim günü 2026-11-04 +6,7%), isimli sözleşme / iş ilişkisi, nakit, borç, seyrelme / bedelli (sıçrama 0), going concern, fon / tedbir / SPK lekesi.
- LILAK (4 puan, XKAGT): 3Ç26 gelir / kâr ivmesi (hacim günü 2026-11-02 +0,6%), isimli sözleşme / iş ilişkisi, nakit, borç, seyrelme / bedelli (sıçrama 0), going concern, fon / tedbir / SPK lekesi.
- VBTYZ (4 puan, XBLSM): 3Ç26 gelir / kâr ivmesi (hacim günü 2026-11-04 +1,0%), isimli sözleşme / iş ilişkisi, nakit, borç, seyrelme / bedelli (sıçrama 0), going concern, fon / tedbir / SPK lekesi.

## I. K11 BAĞIMSIZ YENİDEN ÜRETİM (koşudan sonra, ham pkl'den ayrı kodla)

- EYGYO: 250 g zirveden -%63,77 (csv -0,637652), hacim günü 2026-10-20 +%9,58 (csv 0,0958084), likidite 10,2 mn TL; S6 Pine aynası (s6_pine_ayna, döngü uygulaması) son barda açık bölge n=8, kutu üst 1,87 -> tavana -%4,28 (csv -0,0427808); AL10 / KIRILDI10 yok. Puan 6 tuttu.
- MACKO: 250 g zirveden -%49,36, hacim günü 2026-11-06 -%2,20, likidite 11,9 mn TL; Pine aynası AL10 var, açık bölge yok, KIRILDI10 yok (csv ile aynı). Puan 5 tuttu.
- Evren denetimi: son 10 barda S6 KIRILDI 0 hisse; 150 hissede 3 yılda 445 KIRILDI var, en sonuncusu 2026-10-30 (karar penceresi 31 Eki - 13 Kas dışında): ölçü çalışıyor, pencere boş.

## J. HATA / SAPMA

- H1 (süreç, ön kayıt gösterimi): KONTROL LİSTESİ K6 satırındaki '|günlük|' yazımı tablo ayracını bozdu, kapı K6'yı 'eksik' saydı ve koşu durdu. Metin 'mutlak günlük değişim' yapıldı (anlam aynı); kural / eşik değişmedi.
- H2 (geçerli bar, K3 — SAPMA): ilk koşuda işlem görmeyen 2 hisse (TERA son geçerli bar 2026-09-16; DUNYH 2025-10-06) eski barlarla ölçüldü, TERA şartı geçip 12. sıraya girdi (likidite 3,16 mlr TL eylül verisi). Düzeltme: son geçerli bar karar gününden 5 iş gününden eskiyse ölçü HESAPLANAMADI ve şart dışı (BT_ESIK bayat_isgunu = 5; D9 RUZ_BAYAT ile aynı). Etki: ilk 15'e ATATP girdi (15.), ilk 11 değişmedi. Puan kuralı ve eşikler değişmedi.
- H3 (tanım belirsizliği, bilgi): 'son raporda tasfiye fonu payı > 0' ön kayıtta 'hissenin son raporlu ayı' diye okundu; LEKE'li 211 hissenin 33'ünün son raporlu ayı 2026-07'den eski. Kural koşudan önce yazıldığı için değiştirilmedi; leke dışında şartı geçip puanı >= 3 olacak 2 hisse (ETILR, BAYRK) E bölümünde bilgi olarak yazılı.
- H4 (veri kipi, bilgi): S6 / S5 tasarımı V_BIST (temettü düzeltmeli) ile yapıldı; bu tarama iş tanımı gereği auto_adjust=False (temettüsüz ekran fiyatı). Temettü günlerinde küçük fark; 183 hissede son 260 barda |%11| üstü tek gün sıçrama var (bedelli / bölünme düzeltmesi eksik olabilir), puana girmez, tabloda not.
- H5 (iş tanımı listesi): izleme listesindeki TKNKA, SVGYO, KARCL sektor_BIST.csv'de yok; ayrıca indirildi, sektörleri yok (rüzgâr HESAPLANAMADI), 250 geçerli bar olmadığından S6 / S5 HESAPLANAMADI (yeni halka arz).
