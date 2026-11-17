# YAPI_HEDEF — ÖN KAYIT

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo

- YH_ESIK_SHA: `adf680258917f69edee2d4eeacfe35bff281f2cbb48f9ee9312c54ab0f3d6f7b`
- YH_KOD_SHA: `82acfd2957b85dab6ee2a7c761a1d77eac8aff84ab1edcfe41c122201a977250` (YAPI_HEDEF.py)
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb` (ORTAK_CETVEL.py)
- OC_CETVEL_SHA (bilgi): `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
- S6_KOD_SHA: `ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d` (S6_TABAN.py)
- FV_KOD_SHA: `c62b736a3da17c33b380d38a59c9b69487c4d78b3a3dd37ae7e019c8ea47cd5e` (FITIL_V2.py)
- GUC_SHA: `b7b63dbdbbf6305744e226d4095cc2154c14fbbe8b2ca84545cab8b27436a913` (guc_tablosu.json)
- Y2_OLAY_SHA: `ac6f4a72550e4aecea9ba6de9bc8469adaf6f004a9531cc9653d9734fdb134ea` (fitil_v2/olay_TAM_DIP.csv.gz)
- IS_TANIMI: git 9ee2f7a4ed, 2026-11-17T10:36:38+00:00
- ZAMAN (UTC): `2026-11-17 11:01:36 UTC`

Bu dosya ölçümden ÖNCE yazıldı. Hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri hesaplanmadı ve okunmadı (yalnız aşağıdaki getirisiz olay sayımı ve güç simülasyonu: rastgele hisse-gün, sinyal değil). `kos` kontrol listesini, yukarıdaki sha'ları ve bu dosyanın git kaydını denetler; biri tutmazsa durur. Eşikler sonuç görüldükten sonra değişmez; zorunlu sapma SAPMA-n olarak koşudan ÖNCE buraya yazılır.

## Ölçü (Cemal'in yeni test standardı; CLAUDE.md 'YENİ TEST STANDARDI', 'UFUK 15 MUM')

- Cetvel: ORTAK_CETVEL v1.0: oc_veri (geçerli bar, kriz kesiği, ETF dışı), oc_panel (havuz 'gecmis': likidite alt %20 dışı, geçmiş bölünme şüphesi dışı, 5 momentum x 3 likidite kovası), oc_olay_hazirla (giriş t+1 açılış, 60 gün tekil), dönem = giriş günü.
- Ufuk: giriş barı (bar 0) dahil hissenin ilk 15 geçerli barı; bu 15 bar giriş gününden itibaren en çok 30 birleşik takvim günü içinde olmalı, yoksa (seyrek işlem / kriz kesiği / veri sonu) o hisse o gün ölçülmez (olay, eş, taban, plasebo aynı kural).
- d: d = 1 - stop0 / giriş (yön +), stop0 / giriş - 1 (yön -); d <= 0 (giriş açılışı stop'un ötesinde) -> olay ölçülmez (sayım 'giris_stop_otesi'; karar giriş anında bilinir).
- Stop / hedef: bar k: (1) kapanış, bar k-1 sonundaki stop'un ötesinde (yön +: altında) -> STOP (çıkış bar k+1 açılışı); (2) değilse +%5 / +%10 kapanışla görüldü mü işaretlenir (bilgi: High >= hedef; aynı barda kapanış stop'u -> stop önce); (3) stop güncellenir: stop = max(stop, giriş x 1,02 [+%5 görüldüyse], giriş x 1,07 [+%10 görüldüyse], en yüksek kapanış x 0,93). Yön -: min ve aynası (giriş x 0,98 / 0,93, en düşük kapanış x 1,07).
- Göstergeler: {"h5": "+%5 kapanışla stop'tan önce, 15 barda", "h10": "+%10 kapanışla stop'tan önce, 15 barda", "st5": "stop, +%5'ten önce, 15 barda (P(stop önce))", "h5H / h10H": "aynı, High ile (bilgi)"}.
- Takip stoplu getiri ve çıkış (bilgi): takip stoplu getiri (bilgi, yalnız olay): 60 geçerli bara kadar; çıkış = stop (ertesi açılış) YA DA yeni TERS OLUŞUM (yön +: girişten sonra oluşmuş son n barda bant max H / min L - 1 <= %6 ve kapanış < min L x 0,98; n 10..30 aralığında var olması n = 10'da var olmasına eşittir [bant n ile büyür, min L küçülür] -> n = 10; pencere giriş barından önceye taşmaz; çıkış ertesi açılış; yön -: kapanış > max H x 1,02) YA DA 60. bar kapanışı (zaman). Veri biterse son kapanış ('kesik'). Getiri = yön x (çıkış / giriş - 1); komisyon yok.

## Kontrol grupları (K1)

- EŞ: aynı giriş günü d, aynı OC kovası (H[d]), havuzda (ok[d]), olay hissesi hariç, 15 barı ölçülebilir; stop0 = giriş_eş x (1 - d) (yön -: 1 + d), aynı hedefler, aynı takip kuralı.
- TABAN: aynı gün bütün havuz (olay hissesi hariç, ölçülebilir), aynı d (bilgi).
- PLASEBO: olay başına 1: aynı hisse, aynı dönem (giriş günü dönemi), havuzda (ok), olay gününden farklı rastgele giriş günü; aynı d, aynı kural; ölçülemezse yeniden çekilir (en çok 50); rastgelelik tohum [1717, deneme no, pazar no, d, j].
- KAT: KAT = Σ olay göstergesi / Σ eş oranı (ORTAK_CETVEL.oc_kat ile aynı; ay kümeli bootstrap 2000, tohum 27); p = bootstrap KAT <= 1 payı (tek taraflı, bilgi; BH q = 0,10 karar hücrelerinde 5 deneme x 4 hücre, bilgi).

## Karar kuralı (önceden yazılı; DEĞİŞMEZ)

- hücre TUTAR = (1) n >= 30 (h5 ve eş h5 ölçülebilir olay) VE (2) KAT5 (eş) %95 alt uç > 1 VE (3) P(stop önce) olay < eş (nokta) VE (4) plasebo KAT5 %95 alt uç > 1 (plasebosu ölçülebilir olaylar).
- Hücre durumu: n < 30 -> ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 YA DA güç(n, KAT 1,25) >= %80) -> DESTEKLENMEDİ; değilse ÖLÇÜLEMEDİ.
- Güç bakışı: güç tablosunda (yön aynı) hücre n'inden küçük ya da eşit en büyük n satırı, d ızgarasının EN KÜÇÜK gücü (muhafazakâr).
- Genel etiket (deneme başına): dört karar hücresi TUTAR -> İZ (BIST iki hücre de TUTAR ise 'İZ + BIST'); 2-3 karar hücresi TUTAR (tek pazarın iki dönemi dahil) -> EMARE (hücreler); 1 karar hücresi TUTAR -> öteki üç karar hücresi DESTEKLENMEDİ ise 'DESTEKLENMEDİ (tek hücre tuttu: ...)', değilse 'ÖLÇÜLEMEDİ (tek hücre tuttu: ...)'; 0 -> dördü DESTEKLENMEDİ ise DESTEKLENMEDİ, değilse ÖLÇÜLEMEDİ. 'İz değil' sözü yazılmaz.
- Karar hücreleri: ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26; bilgi: BIST 2023, BIST 2024-26, her pazarın 2016-22'si.

## Denemeler (sonuç görülmeden sabit)

- **Y1 S6 TABAN AL** (yön +): S6_TABAN.s6_taban (SY.sy_veri_hazirla girdisi) 'al' günleri (AL ve AL_BOLGESIZ) = taban kırılım mumu (C_t > TAVAN(t-1)); hat = bölge dibi: durum AL ise kutu_alt (açık bölgenin as-of t alt kenarı), AL_BOLGESIZ ise DİP(t-1) (bir önceki barın taban penceresinin en düşük Low'u).
- **Y2 S+ v2 TAM_DIP** (yön +): arastirma_cikti/fitil_v2/olay_TAM_DIP.csv.gz (sembol, pazar, tarih) olayları; hat = FITIL_V2.fv_olcu HAT (t dahil son 10 geçerli barın en düşük Low'u; yeniden hesaplanır); giriş dosyadaki 'giris' ile aynı olmalı (sayım).
- **Y3 KAZAN + DÖNÜŞ** (yön +): t için pencere W = [t-n, t-1] (n geçerli bar, t hariç), n = 20..60: (a) Low serisine 2. derece en küçük kareler uyumunun x^2 katsayısı a > 0; (b) sağ kenar dibi min L(son 5 bar of W) > orta üçte bir dibi min L(W[n//3 : 2n//3]) x 1,03; (c) son kapanış C_{t-1} > dip + (tavan - dip) / 2, dip = min L(W), tavan = max H(W); (d) kırılım C_t > tavan. (a)-(d) tutan EN BÜYÜK n seçilir; hat = dip(W). Bağlam: C_t <= max(C, t dahil son 120 geçerli bar) x 0,85.
- **Y4 Y1 + KAĞIT HAFIZASI** (yön +): Y1 olayı t, hafıza = (son 250 barda [t-250, t-1] AL ile biten S6 bölgelerinden (durum AL; a + 15 <= t, sonucu t'de bilinen) a+1 .. a+15 kapanışlarından biri >= açılış(a+1) x 1,05 olanlar) - (son 250 barda KIRILDI ile biten bölgeler); hafıza >= 0 -> Y4 (yalnız geçmiş, t'ye kadar).
- **Y5 DÜZ TAVAN SAT** (yön -): TAVAN(t-1): pencere W = [t-n, t-1], n = 8..70: bant max H / min L - 1 <= 0,12; net |C_{t-1} / C_{t-n} - 1| <= 0,03; yüksekler düz (S6 dip savunmasının aynası): max H(ikinci yarı) <= max H(ilk yarı, n//2 bar) x 1,05; önceki yükseliş: C_{t-n-1} / min C(son 60 bar, t-n-1 dahil) - 1 >= 0,20; tutan EN BÜYÜK n. Konum: (C_{t-1} - min C120) / (max C120 - min C120) >= 0,75 (t-1 dahil 120 geçerli kapanış). SAT_t = C_t < min L(W) x 0,98. stop0 = max H(W) x 1,02; hedef -%5 / -%10 (yön -).

S6 parametreleri (v1.1 varsayılan): `{"atrGun": 250, "bantMax": 0.12, "bbDagilim": 250, "bbEsik": 0.3, "bbGun": 20, "bbK": 2.0, "bbSart": true, "daralmaGun": 60, "daralmaOran": 0.0, "dipDusus": -0.1, "dipKonum": 0.25, "dipTol": 0.05, "hacimGun": 20, "kM": 0.9, "kirTol": 0.02, "konumGun": 120, "nMax": 70, "nMin": 8, "netMax": 0.03, "refGun": 250, "refMin": 120, "refOnce": true, "smaEgimGun": 20, "smaGun": 50, "surTol": -1}`

## Getirisiz olay sayımı (sinyal günü, sinyal dönemi / OC sonrası tekil olay, giriş dönemi)

| Deneme | Pazar | hisse | sinyal 2016-22 / 2023 / 2024-26 | olay 2016-22 / 2023 / 2024-26 | düşme (giriş yok / geç / havuz dışı / tekil) |
|---|---|---|---|---|---|
| Y1 | ABD | 1383 | 22667 / 5384 / 9918 | 8686 / 2042 / 4153 | 5 / 0 / 5214 / 17869 |
| Y1 | AVR | 579 | 12174 / 2273 / 4336 | 4496 / 815 / 1743 | 10 / 0 / 2969 / 8750 |
| Y1 | BIST | 568 | 5494 / 728 / 4020 | 2588 / 381 / 1759 | 1 / 2 / 2460 / 3051 |
| Y2 | ABD | 388 | 283 / 47 / 212 | 283 / 47 / 212 | 0 / 0 / 0 / 0 |
| Y2 | AVR | 218 | 155 / 35 / 134 | 156 / 34 / 135 | 0 / 0 / 0 / 0 |
| Y2 | BIST | 391 | 296 / 101 / 483 | 296 / 101 / 483 | 0 / 0 / 0 / 0 |
| Y3 | ABD | 1380 | 17440 / 4406 / 7998 | 4189 / 940 / 2039 | 5 / 0 / 8250 / 14517 |
| Y3 | AVR | 544 | 5229 / 697 / 1500 | 1537 / 190 / 476 | 0 / 1 / 1214 / 4136 |
| Y3 | BIST | 564 | 4034 / 2149 / 3369 | 1348 / 432 / 1078 | 2 / 1 / 2142 / 4550 |
| Y4 | ABD | 1370 | 19002 / 4082 / 7771 | 7293 / 1550 / 3310 | 3 / 0 / 4002 / 14697 |
| Y4 | AVR | 579 | 10711 / 1855 / 3468 | 3913 / 665 / 1373 | 9 / 0 / 2552 / 7522 |
| Y4 | BIST | 559 | 4202 / 599 / 3006 | 1994 / 316 / 1348 | 1 / 1 / 1873 / 2274 |
| Y5 | ABD | 1116 | 2037 / 353 / 1211 | 1628 / 280 / 946 | 2 / 0 / 492 / 255 |
| Y5 | AVR | 419 | 588 / 106 / 338 | 473 / 86 / 274 | 1 / 0 / 149 / 58 |
| Y5 | BIST | 422 | 717 / 135 / 313 | 591 / 105 / 261 | 3 / 0 / 147 / 61 |

## Güç (gerçek ABD 2023-26 rastgele hisse-gün; dört şartlı hücre kuralı; ayrıntı GUC_TABLOSU.md)

Yön + (KAT_ref 1,25; d 3 / 6 / 10; etiket için en küçüğü):

| n | d %3 | d %6 | d %10 | KAT 1,00 (yanlış pozitif, en büyük) |
|---|---|---|---|---|
| 30 | %2 | %6 | %4 | %0 |
| 100 | %11 | %23 | %20 | %1 |
| 300 | %57 | %62 | %65 | %1 |
| 1000 | %97 | %98 | %99 | %1 |
| 3000 | %100 | %100 | %100 | %0 |

Yön - (KAT_ref 1,25; d 3 / 6 / 10; etiket için en küçüğü):

| n | d %3 | d %6 | d %10 | KAT 1,00 (yanlış pozitif, en büyük) |
|---|---|---|---|---|
| 30 | %2 | %5 | %4 | %1 |
| 100 | %10 | %18 | %18 | %2 |
| 300 | %52 | %58 | %56 | %2 |
| 1000 | %96 | %100 | %98 | %2 |
| 3000 | %100 | %100 | %100 | %0 |

## Sınırlar (önceden)

- Hayatta kalma: evren bugün işlem gören hisseler (ABD V_ABD 1.411; k34 / Tiingo yok); hedef payı yukarı, stop payı aşağı yanlı; eş ve plasebo aynı evrenden.
- Komisyon / kayma yok; stop çıkışı ertesi açılış (boşluk riski içerir).
- Takip stopu GEÇİCİ kural (Cemal: 'son kural değil'); getiri ve bar sayısı bilgi.
- Y2 olayları FITIL_V2'nin tekilleştirilmiş olaylarıdır (aynı OC kuralı, aynı veri); yeniden OC'den geçirilir.

## YH_ESIK (tam metin; mühürlü)

```json
{
 "cetvel": "ORTAK_CETVEL v1.0: oc_veri (geçerli bar, kriz kesiği, ETF dışı), oc_panel (havuz 'gecmis': likidite alt %20 dışı, geçmiş bölünme şüphesi dışı, 5 momentum x 3 likidite kovası), oc_olay_hazirla (giriş t+1 açılış, 60 gün tekil), dönem = giriş günü",
 "denemeler": {
  "Y1": {
   "ad": "S6 TABAN AL",
   "s6_prm": "S6_TABAN.S6_PRM varsayılan (v1.1)",
   "tanim": "S6_TABAN.s6_taban (SY.sy_veri_hazirla girdisi) 'al' günleri (AL ve AL_BOLGESIZ) = taban kırılım mumu (C_t > TAVAN(t-1)); hat = bölge dibi: durum AL ise kutu_alt (açık bölgenin as-of t alt kenarı), AL_BOLGESIZ ise DİP(t-1) (bir önceki barın taban penceresinin en düşük Low'u)",
   "yon": 1
  },
  "Y2": {
   "ad": "S+ v2 TAM_DIP",
   "tanim": "arastirma_cikti/fitil_v2/olay_TAM_DIP.csv.gz (sembol, pazar, tarih) olayları; hat = FITIL_V2.fv_olcu HAT (t dahil son 10 geçerli barın en düşük Low'u; yeniden hesaplanır); giriş dosyadaki 'giris' ile aynı olmalı (sayım)",
   "yon": 1
  },
  "Y3": {
   "ad": "KAZAN + DÖNÜŞ",
   "baglam_dusus": 0.15,
   "baglam_gun": 120,
   "n": [
    20,
    60
   ],
   "sag": 5,
   "sag_carpan": 1.03,
   "tanim": "t için pencere W = [t-n, t-1] (n geçerli bar, t hariç), n = 20..60: (a) Low serisine 2. derece en küçük kareler uyumunun x^2 katsayısı a > 0; (b) sağ kenar dibi min L(son 5 bar of W) > orta üçte bir dibi min L(W[n//3 : 2n//3]) x 1,03; (c) son kapanış C_{t-1} > dip + (tavan - dip) / 2, dip = min L(W), tavan = max H(W); (d) kırılım C_t > tavan. (a)-(d) tutan EN BÜYÜK n seçilir; hat = dip(W). Bağlam: C_t <= max(C, t dahil son 120 geçerli bar) x 0,85",
   "yon": 1
  },
  "Y4": {
   "ad": "Y1 + KAĞIT HAFIZASI",
   "esik": 0,
   "gun": 250,
   "hedef": 0.05,
   "tanim": "Y1 olayı t, hafıza = (son 250 barda [t-250, t-1] AL ile biten S6 bölgelerinden (durum AL; a + 15 <= t, sonucu t'de bilinen) a+1 .. a+15 kapanışlarından biri >= açılış(a+1) x 1,05 olanlar) - (son 250 barda KIRILDI ile biten bölgeler); hafıza >= 0 -> Y4 (yalnız geçmiş, t'ye kadar)",
   "ufuk": 15,
   "yon": 1
  },
  "Y5": {
   "ad": "DÜZ TAVAN SAT",
   "bant": 0.12,
   "konum": 0.75,
   "konum_gun": 120,
   "n": [
    8,
    70
   ],
   "net": 0.03,
   "sat": 0.98,
   "stop": 1.02,
   "tanim": "TAVAN(t-1): pencere W = [t-n, t-1], n = 8..70: bant max H / min L - 1 <= 0,12; net |C_{t-1} / C_{t-n} - 1| <= 0,03; yüksekler düz (S6 dip savunmasının aynası): max H(ikinci yarı) <= max H(ilk yarı, n//2 bar) x 1,05; önceki yükseliş: C_{t-n-1} / min C(son 60 bar, t-n-1 dahil) - 1 >= 0,20; tutan EN BÜYÜK n. Konum: (C_{t-1} - min C120) / (max C120 - min C120) >= 0,75 (t-1 dahil 120 geçerli kapanış). SAT_t = C_t < min L(W) x 0,98. stop0 = max H(W) x 1,02; hedef -%5 / -%10 (yön -)",
   "tavanTol": 0.05,
   "yon": -1,
   "yuk": 0.2,
   "yuk_gun": 60
  }
 },
 "etiket": {
  "genel": "dört karar hücresi TUTAR -> İZ (BIST iki hücre de TUTAR ise 'İZ + BIST'); 2-3 karar hücresi TUTAR (tek pazarın iki dönemi dahil) -> EMARE (hücreler); 1 karar hücresi TUTAR -> öteki üç karar hücresi DESTEKLENMEDİ ise 'DESTEKLENMEDİ (tek hücre tuttu: ...)', değilse 'ÖLÇÜLEMEDİ (tek hücre tuttu: ...)'; 0 -> dördü DESTEKLENMEDİ ise DESTEKLENMEDİ, değilse ÖLÇÜLEMEDİ. 'İz değil' sözü yazılmaz.",
  "guc_bak": "güç tablosunda (yön aynı) hücre n'inden küçük ya da eşit en büyük n satırı, d ızgarasının EN KÜÇÜK gücü (muhafazakâr)",
  "guc_esik": 0.8,
  "hucre": "n < 30 -> ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 YA DA güç(n, KAT 1,25) >= %80) -> DESTEKLENMEDİ; değilse ÖLÇÜLEMEDİ",
  "kat_ref": 1.25,
  "n_yeter": 1000
 },
 "gelecek_denetimi": {
  "n": 5,
  "tanim": "her deneme x pazar rastgele 5 olay: hissenin verisi t'de kesilir, sinyal yeniden üretilir; t'de aynı sinyal ve aynı hat / stop0 çıkmalı (yoksa koşu DURUR)",
  "tohum": 615
 },
 "guc": {
  "bas": "2023-01-01",
  "d": [
   0.03,
   0.06,
   0.1
  ],
  "havuz": 6000,
  "kat_ref": [
   1.0,
   1.25,
   1.5
  ],
  "n": [
   30,
   100,
   300,
   1000,
   3000
  ],
  "pazar": "ABD",
  "son": "2026-06-30",
  "tanim": "ABD giriş 2023-01-01 .. 2026-06-30 havuzda (ok, kova) rastgele hisse-gün (6.000, yerine koymadan); her biri için olay göstergeleri, eş oranları (aynı gün aynı kova, min 3) ve plasebo (aynı hisse aynı dönem rastgele gün) gerçek fiyatla ve sabit d ile hesaplanır. Tekrar: n olay çekilir; KAT_ref > 1 ise h5 = 0 olan olaylar q = (KAT_ref Σ eş - Σ h5) / (n - Σ h5) olasılıkla h5 = 1 (st5 = 0) yapılır; hücre TUTAR kuralı (4 şart; bootstrap ay kümeli 2000, vektör) uygulanır; güç = TUTAR payı. KAT_ref = 1,0 enjeksiyonsuz (yanlış pozitif payı).",
  "tekrar": 200,
  "tohum": 1477,
  "yon": [
   1,
   -1
  ]
 },
 "karar": {
  "hucre_bilgi": [
   [
    "BIST",
    "2023"
   ],
   [
    "BIST",
    "2024-26"
   ],
   [
    "*",
    "2016-22"
   ]
  ],
  "hucre_karar": [
   [
    "ABD",
    "2023"
   ],
   [
    "ABD",
    "2024-26"
   ],
   [
    "AVR",
    "2023"
   ],
   [
    "AVR",
    "2024-26"
   ]
  ],
  "n_esik": 30,
  "tanim": "hücre TUTAR = (1) n >= 30 (h5 ve eş h5 ölçülebilir olay) VE (2) KAT5 (eş) %95 alt uç > 1 VE (3) P(stop önce) olay < eş (nokta) VE (4) plasebo KAT5 %95 alt uç > 1 (plasebosu ölçülebilir olaylar)"
 },
 "kat": {
  "bootstrap": 2000,
  "guven": [
   0.025,
   0.975
  ],
  "kume": "giriş ayı",
  "tanim": "KAT = Σ olay göstergesi / Σ eş oranı (ORTAK_CETVEL.oc_kat ile aynı; ay kümeli bootstrap 2000, tohum 27); p = bootstrap KAT <= 1 payı (tek taraflı, bilgi; BH q = 0,10 karar hücrelerinde 5 deneme x 4 hücre, bilgi)",
  "tohum": 27
 },
 "kontrol": {
  "es": "aynı giriş günü d, aynı OC kovası (H[d]), havuzda (ok[d]), olay hissesi hariç, 15 barı ölçülebilir; stop0 = giriş_eş x (1 - d) (yön -: 1 + d), aynı hedefler, aynı takip kuralı",
  "min_es": 3,
  "plasebo": "olay başına 1: aynı hisse, aynı dönem (giriş günü dönemi), havuzda (ok), olay gününden farklı rastgele giriş günü; aynı d, aynı kural; ölçülemezse yeniden çekilir (en çok 50); rastgelelik tohum [1717, deneme no, pazar no, d, j]",
  "plasebo_deneme": 50,
  "plasebo_tohum": 1717,
  "taban": "aynı gün bütün havuz (olay hissesi hariç, ölçülebilir), aynı d (bilgi)"
 },
 "kriz": "2026-08-31",
 "olcu": {
  "cikis_bilgi": {
   "tanim": "takip stoplu getiri (bilgi, yalnız olay): 60 geçerli bara kadar; çıkış = stop (ertesi açılış) YA DA yeni TERS OLUŞUM (yön +: girişten sonra oluşmuş son n barda bant max H / min L - 1 <= %6 ve kapanış < min L x 0,98; n 10..30 aralığında var olması n = 10'da var olmasına eşittir [bant n ile büyür, min L küçülür] -> n = 10; pencere giriş barından önceye taşmaz; çıkış ertesi açılış; yön -: kapanış > max H x 1,02) YA DA 60. bar kapanışı (zaman). Veri biterse son kapanış ('kesik'). Getiri = yön x (çıkış / giriş - 1); komisyon yok.",
   "ters_bant": 0.06,
   "ters_kir": 0.02,
   "ters_n": 10,
   "ters_n_aralik": [
    10,
    30
   ],
   "zaman_tavani": 60
  },
  "d_tanim": "d = 1 - stop0 / giriş (yön +), stop0 / giriş - 1 (yön -); d <= 0 (giriş açılışı stop'un ötesinde) -> olay ölçülmez (sayım 'giris_stop_otesi'; karar giriş anında bilinir)",
  "hedef": [
   0.05,
   0.1
  ],
  "karar_hedef": 0.05,
  "karar_sutun": "kapanış (bilgi sütunu: High; yön -: Low)",
  "olay_gosterge": {
   "h10": "+%10 kapanışla stop'tan önce, 15 barda",
   "h5": "+%5 kapanışla stop'tan önce, 15 barda",
   "h5H / h10H": "aynı, High ile (bilgi)",
   "st5": "stop, +%5'ten önce, 15 barda (P(stop önce))"
  },
  "pencere_azami": 30,
  "stop": {
   "kilit10": 0.07,
   "kilit5": 0.02,
   "takip": 0.07,
   "tanim": "bar k: (1) kapanış, bar k-1 sonundaki stop'un ötesinde (yön +: altında) -> STOP (çıkış bar k+1 açılışı); (2) değilse +%5 / +%10 kapanışla görüldü mü işaretlenir (bilgi: High >= hedef; aynı barda kapanış stop'u -> stop önce); (3) stop güncellenir: stop = max(stop, giriş x 1,02 [+%5 görüldüyse], giriş x 1,07 [+%10 görüldüyse], en yüksek kapanış x 0,93). Yön -: min ve aynası (giriş x 0,98 / 0,93, en düşük kapanış x 1,07)."
  },
  "stop0": {
   "arti": "hat x 0,98",
   "eksi": "tavan x 1,02",
   "hat_carpan": 0.98,
   "tavan_carpan": 1.02
  },
  "ufuk": 15,
  "ufuk_tanim": "giriş barı (bar 0) dahil hissenin ilk 15 geçerli barı; bu 15 bar giriş gününden itibaren en çok 30 birleşik takvim günü içinde olmalı, yoksa (seyrek işlem / kriz kesiği / veri sonu) o hisse o gün ölçülmez (olay, eş, taban, plasebo aynı kural)"
 },
 "s6_prm": {
  "atrGun": 250,
  "bantMax": 0.12,
  "bbDagilim": 250,
  "bbEsik": 0.3,
  "bbGun": 20,
  "bbK": 2.0,
  "bbSart": true,
  "daralmaGun": 60,
  "daralmaOran": 0.0,
  "dipDusus": -0.1,
  "dipKonum": 0.25,
  "dipTol": 0.05,
  "hacimGun": 20,
  "kM": 0.9,
  "kirTol": 0.02,
  "konumGun": 120,
  "nMax": 70,
  "nMin": 8,
  "netMax": 0.03,
  "refGun": 250,
  "refMin": 120,
  "refOnce": true,
  "smaEgimGun": 20,
  "smaGun": 50,
  "surTol": -1
 },
 "surum": "1.0"
}
```

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü, aynı OC momentum beşliği x likidite üçlüsü kovası, olay hissesi hariç, AYNI giriş (t+1 açılış) / AYNI d ile stop0 / aynı hedefler / aynı takip kuralı / aynı 15 bar (yh_sim tek fonksiyon); taban = aynı gün bütün havuz; plasebo = aynı hisse rastgele gün aynı kural (hisse etkisi); mekanik üstünlük: d eşlere aynen verilir (stop uzaklığı farkı dışlandı), kırılım mumunun kendisi (t) ölçüye girmez (giriş t+1 açılış); güç simülasyonu KAT_ref 1,0 = yanlış pozitif payı |
| K2 | geleceğe bakma | EVET | sinyaller yalnız t ve öncesiyle (S6 durum makinesi nedensel; Y3 / Y5 pencereleri t-1'de biter, t yalnız kırılım kapanışı; Y4 hafızası a + 15 <= t şartıyla); test_yapi_hedef 'geleceğe bakma' bütün günlerde kesik seri = tam seri; koşuda her deneme x pazar 5 rastgele olay kesik veriyle yeniden üretilir (yh_gelecek_denetimi, tutmazsa DURUR); hedef / stop yalnız giriş ve sonrası fiyatla |
| K3 | geçerli bar | EVET | OC.oc_veri_hazirla + SY.sy_veri_hazirla: H>L, V>0, O/H/L/C>0 olmayan bar atılır; bütün pencereler geçerli bar dizisinde; 15 bar ve takip yalnız geçerli bar; sinyal günü geçersiz bar olamaz (veriden atılmış) |
| K4 | tekilleştirme | EVET | OC.oc_olay_hazirla: aynı hissede 60 birleşik takvim gününde tek olay (deneme başına); n = bağımsız olay; hücre tablosunda getiri ortalama + medyan |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC); eş ve plasebo da kendi giriş günlerinin açılışı; stop çıkışı ertesi açılış; test 'giriş ertesi açılış' |
| K6 | veri birimi | EVET | tek kip V_*.pkl (fi_k1_veri düzeltilmiş fiyat); hedef / stop / d oran (birimden bağımsız); AVR yerel para, likidite kovası EUR (OC Kur); bölünme şüphesi geçmiş penceresinde havuz dışı (OC); ileri 15 barda dışlama yok (OC kuralı: sonuca göre seçim olurdu) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD 1.411, k34 / Tiingo yok; V_AVR, V_BIST); batanlar yok -> hedef payı yukarı, stop payı aşağı yanlı; eş ve plasebo aynı evrenden olduğu için KAT'ta yanlılık kısmen birbirini götürür; rapora yazılır |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem (2016-22 / 2023 / 2024-26); n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80 (guc_tablosu.json); iki yarı KAT (bilgi); 5 deneme x 4 karar hücresi BH q 0,10 (bilgi); küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | YH_ESIK sha256 + YAPI_HEDEF.py / ORTAK_CETVEL.py / S6_TABAN.py / FITIL_V2.py sha256 + güç tablosu sha256 + Y2 olay dosyası sha256 ON_KAYIT.md'de; yh_kapi hepsini + ON_KAYIT ve kodun git'e işlenmiş / değişmemiş olmasını + IZ_KARNE.ik_kontrol_kapisi'ni denetler; ön kayıt ayrı commit (ölçümden önce); eşik sonuca göre oynanmaz; sapma SAPMA-n olarak koşudan önce |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV; Y2 olay dosyası FITIL_V2 kos çıktısı (sha ön kayıtta, giriş günü OC ile yeniden üretilir ve dosyadakiyle karşılaştırılır) |
| K11 | yeniden üretim | EVET | olay_Y*.csv.gz satır dosyaları (olay + eş + taban + plasebo göstergeleri); RAPOR.md 'YENİDEN ÜRETİM' bölümünde iki hücrenin KAT'ı satır dosyasından 5 satırlık bağımsız komutla; test KAT = OC.oc_kat |
| K12 | ifade | EVET | etiketler yalnız YH_ESIK['etiket'] kuralıyla (İZ / EMARE / DESTEKLENMEDİ / ÖLÇÜLEMEDİ); 'iz değil' yazılmaz; hedef payı fiyat dokunuşu, getiri komisyonsuz fiyat değişimi; sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_yh; yasak defter dosyalarına dokunulmaz (git diff ile denetim); e-posta / anahtar taraması (test + yazım öncesi _yh_sizinti); ücretli veri yok; push yok; kod değişirse 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm (yapı kuralları hedef payı) |

## SAPMALAR

(yok)

## Test

`python test_yapi_hedef.py` (sentetik: sinyaller elle, geleceğe bakma kesme testi, yh_sim hedef / stop / takip / yön -, eş = aynı kural, plasebo, KAT = OC.oc_kat, etiket kuralı, kapı, uçtan uca kos, e-posta / anahtar taraması, çakışma kapısı).
