# YAPI_HEDEF — ÖN KAYIT 2 (2. tur: Y6 / Y7 / Y8 + Y8B bilgi)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo; 2. tur eklendi (YAPI_HEDEF_2_IS_TANIMI.md)

- YH_ESIK_SHA: `d4ab206a2d2cf8ed25f2c3fd7f30c7122f6460a40040255788ea62ff9cdfbbe1` (2. tur denemeleri dahil)
- ESIK_TUR1_SHA: `adf680258917f69edee2d4eeacfe35bff281f2cbb48f9ee9312c54ab0f3d6f7b` (YH_ESIK'ten Y6-Y8B çıkarılınca; = ON_KAYIT.md YH_ESIK_SHA = güç tablosu yh_esik_sha: Y1-Y5 eşikleri AYNEN)
- YH_KOD_SHA: `1d547ae8a4e4224f9337ba9c3aae859f50037d33e07f45246d37c6a19b2a74ab` (YAPI_HEDEF.py)
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb` (ORTAK_CETVEL.py)
- S6_KOD_SHA: `ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d` (S6_TABAN.py)
- FV_KOD_SHA: `c62b736a3da17c33b380d38a59c9b69487c4d78b3a3dd37ae7e019c8ea47cd5e` (FITIL_V2.py)
- GUC_SHA: `b7b63dbdbbf6305744e226d4095cc2154c14fbbe8b2ca84545cab8b27436a913` (guc_tablosu.json; 1. turun güç tablosu, aynı kural)
- Y2_OLAY_SHA: `ac6f4a72550e4aecea9ba6de9bc8469adaf6f004a9531cc9653d9734fdb134ea` (değişmedi; 2. turda kullanılmaz)
- ON_KAYIT_1: git 84490eadee, 2026-11-17T11:01:51+00:00
- IS_TANIMI_2: git 074087ee3a, 2026-11-17T12:41:11+00:00
- ZAMAN (UTC): `2026-11-17 13:18:37 UTC`

Bu dosya 2. tur ölçümünden ÖNCE yazıldı. Y6 / Y7 / Y8 / Y8B için hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri hesaplanmadı ve okunmadı (yalnız aşağıdaki getirisiz huni ve olay sayımı; E5a sayımı yalnız giriş açılışını kullanır). `kos --deneme Y6,Y7,Y8` bu dosyanın kontrol listesini, sha'larını, git kaydını ve Y1-Y5 eşik mührünü denetler; biri tutmazsa durur. Eşikler sonuç görüldükten sonra değişmez.

UYARI (K2 / K9 benzeri, önceden): Y6-Y8 şartları Cemal'in 17 Kas değerlendirmesinden (CEMAL_DEGERLENDIRME_2026-11-17.md E1-E11) yazıldı; o değerlendirme 1. tur örnek grafiklerinin SONUCU görülerek yapıldı (30 örnek). Bu yüzden bu ölçüm o 30 örneği de içeren veride yapılır ve tek başına bağımsız kanıt değildir; TUTAR çıkan hücre ileri testle (kriz sonrası veri) yeniden ölçülür.

## Ölçü, kontrol grupları, karar kuralı

1. turla AYNI (ON_KAYIT.md; YH_ESIK 'olcu', 'kontrol', 'kat', 'karar', 'etiket', 'guc' bölümleri değişmedi, ESIK_TUR1_SHA kanıtı):
- Ufuk: giriş barı (bar 0) dahil hissenin ilk 15 geçerli barı; bu 15 bar giriş gününden itibaren en çok 30 birleşik takvim günü içinde olmalı, yoksa (seyrek işlem / kriz kesiği / veri sonu) o hisse o gün ölçülmez (olay, eş, taban, plasebo aynı kural).
- Stop / hedef: bar k: (1) kapanış, bar k-1 sonundaki stop'un ötesinde (yön +: altında) -> STOP (çıkış bar k+1 açılışı); (2) değilse +%5 / +%10 kapanışla görüldü mü işaretlenir (bilgi: High >= hedef; aynı barda kapanış stop'u -> stop önce); (3) stop güncellenir: stop = max(stop, giriş x 1,02 [+%5 görüldüyse], giriş x 1,07 [+%10 görüldüyse], en yüksek kapanış x 0,93). Yön -: min ve aynası (giriş x 0,98 / 0,93, en düşük kapanış x 1,07).
- EŞ: aynı giriş günü d, aynı OC kovası (H[d]), havuzda (ok[d]), olay hissesi hariç, 15 barı ölçülebilir; stop0 = giriş_eş x (1 - d) (yön -: 1 + d), aynı hedefler, aynı takip kuralı.
- PLASEBO: olay başına 1: aynı hisse, aynı dönem (giriş günü dönemi), havuzda (ok), olay gününden farklı rastgele giriş günü; aynı d, aynı kural; ölçülemezse yeniden çekilir (en çok 50); rastgelelik tohum [1717, deneme no, pazar no, d, j].
- Karar: hücre TUTAR = (1) n >= 30 (h5 ve eş h5 ölçülebilir olay) VE (2) KAT5 (eş) %95 alt uç > 1 VE (3) P(stop önce) olay < eş (nokta) VE (4) plasebo KAT5 %95 alt uç > 1 (plasebosu ölçülebilir olaylar).
- Hücre durumu: n < 30 -> ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 YA DA güç(n, KAT 1,25) >= %80) -> DESTEKLENMEDİ; değilse ÖLÇÜLEMEDİ.
- Genel etiket (deneme başına): dört karar hücresi TUTAR -> İZ (BIST iki hücre de TUTAR ise 'İZ + BIST'); 2-3 karar hücresi TUTAR (tek pazarın iki dönemi dahil) -> EMARE (hücreler); 1 karar hücresi TUTAR -> öteki üç karar hücresi DESTEKLENMEDİ ise 'DESTEKLENMEDİ (tek hücre tuttu: ...)', değilse 'ÖLÇÜLEMEDİ (tek hücre tuttu: ...)'; 0 -> dördü DESTEKLENMEDİ ise DESTEKLENMEDİ, değilse ÖLÇÜLEMEDİ. 'İz değil' sözü yazılmaz.
- Y8B bilgi satırıdır: etiketi yazılır, karar değildir. BH (bilgi) yalnız Y6 / Y7 / Y8 x 4 karar hücresi (12 p; 1. turun BH'si ayrı ve korunur).

## Denemeler (sonuç görülmeden sabit; YAPI_HEDEF_2_IS_TANIMI.md §3)

- **Y6 Y1 + HAT NET + GERÇEK KIRILIM + STOP YAKIN + BÜYÜK DESEN**: Y1 olayı t (S6 'al' günü; hat ve tavan Y1'deki gibi) + dört şart. BÖLGE = durum AL ise [kutu_sol_i(t), t-1] (açık S6 bölgesinin as-of t kutusu, t hariç), AL_BOLGESIZ ise t-1 taban penceresi [bas_i(t-1), t-1]. (a) HAT NET (E2): bölgede Low <= hat x 1,015 olan bar sayısı >= 3 VE son dokunuşun Low'u >= ilk dokunuşun Low'u x 0,99 (eğim aşağı değil); (b) GERÇEK KIRILIM (E3): C_t > tavan x 1,01 (tavan = Y1 TAVAN(t-1)) VE (H_t - L_t) >= bölge içi (H - L) medyanı; (c) STOP UZAKLIĞI (E5a): sinyalde C_t / hat - 1 <= 0,10 (ön eleme), ölçümde gerçek giriş (t+1 açılış) / hat - 1 <= 0,10 yeniden denetlenir, aşan olay ölçülmez ve 'stop_uzak' sayımına düşer; (d) BÜYÜK DESEN ALÇALAN DEĞİL (E1): [t-250, t-1] 250 geçerli bar, ardışık 10 parça x 25 bar, her parçanın min Low'u; bu 10 noktaya doğru (en küçük kareler, x = 0..9); eğim = uyum(9) / uyum(0) - 1 >= -0,05 (uyum(0) <= 0 ise şart tutmaz); t'den önce 250 geçerli bar yoksa (d) UYGULANMAZ (şart geçer, ek sütunda 'buyuk_desen=NA'). stop0 = hat x 0,98 (1. turla aynı). Bilgi (E5b): stop0b = max(hat x 0,98, giriş x 0,95) ile olay ve eş (aynı gün aynı kova, aynı d_b) hedef / stop payları ayrı sütun (b_*); karar satırı değil.
- **Y7 Y3 + KAZAN ŞARTLARI + STOP YAKIN**: Y3 olayı t (Y3'ün seçtiği EN BÜYÜK n ile pencere W = [t-n, t-1], hat = dip(W)) + dört şart, aynı W üzerinde (Y7 ⊆ Y3 sinyalleri). Üçte birler: ilk = W[0 : n//3], orta = W[n//3 : 2n//3] (Y3'teki orta ile aynı), son = W[2n//3 : n]. (a) İKİ KENAR: min L(ilk) >= min L(orta) x 1,05 VE min L(son) >= min L(orta) x 1,05; (b) DİPTE KÜÇÜK MUM: orta üçte birde mum boyu (H - L) / C medyanı <= 0,90 x ATR250, ATR250 = pencereden ÖNCEKİ 250 geçerli barın ortalama TR / C_önceki'si (S6 refOnce ile aynı birim; 250 yoksa en az 120 bar, 120 de yoksa şart tutmaz); (c) DİP SAVUNMASI: W'de Low <= dip(W) x 1,015 olan bar sayısı >= 3; (d) E5a: sinyalde C_t / hat - 1 <= 0,10, ölçümde giriş / hat - 1 <= 0,10 (aşan 'stop_uzak'). Bilgi E5b Y6 gibi.
- **Y8 Y6 + CEMAL HAFIZASI (patlamış yapı yok)**: Y6 olayı t ve [t-250, t-1] içinde durum KIRILDI ile biten S6 bölgesi (kapanış < dip x 0,98; S6 kirTol 0,02) YOK -> olay; varsa düşer (yalnız geçmiş; Y4'teki KIRILDI sayımıyla aynı aralık).
- **Y8B Y6 + patlamış yapı VAR (bilgi, aleyhte)**: Y8'in tersi: Y6 olayı ve [t-250, t-1] içinde KIRILDI ile biten S6 bölgesi >= 1 (karşılaştırma için bilgi satırı; etiket yazılır ama karar değildir). `kos --deneme ...Y8` Y8B'yi kendiliğinden ekler.

## Yorumlar (iş tanımında açık bırakılan noktalar; koşudan önce sabit)

- YORUM-1 (Y6 bölge): 'bölge içi' = durum AL ise açık S6 bölgesinin as-of t kutusu [kutu_sol_i(t), t-1] (hat = kutu_alt), AL_BOLGESIZ ise t-1 taban penceresi [bas_i(t-1), t-1] (hat = DİP(t-1)); kırılım günü t bölgeye girmez.
- YORUM-2 (Y6 (b) tavan): Y1'in kırılım tavanı TAVAN(t-1) (C_t > TAVAN(t-1) Y1 tanımı); mum boyu mutlak H - L, bölge medyanı aynı birimde.
- YORUM-3 (Y6 (d)): 250 bar = [t-250, t-1] (t hariç); 10 parça x 25; doğru en küçük kareler; eğim = uyum(son) / uyum(ilk) - 1.
- YORUM-4 (Y7): şartlar Y3'ün seçtiği EN BÜYÜK n penceresinde sınanır (Y7 ⊆ Y3 sinyalleri; başka n aranmaz). ATR250 birimi TR / C_önceki (S6 refOnce), mum birimi (H - L) / C; ATR penceresi W'den önceki 250 geçerli bar (en az 120).
- YORUM-5 (E5a): sinyalde C_t / hat ön elemesi, ölçümde gerçek giriş açılışıyla denetim; denetim OC tekilleştirmesinden SONRA (aşan olay düşer, aynı 60 günde başka olay yerine konmaz); 'stop_uzak' sayımı raporda.
- YORUM-6 (Y8): 'patlamış yapı' = durum KIRILDI (bölgeli; KIRILDI_BOLGESIZ değil) [t-250, t-1] içinde; Y4'ün KIRILDI sayımıyla aynı.
- YORUM-7 (E5b bilgi): stop0b = max(hat x 0,98, giriş x 0,95); olay ve eşler aynı d_b; plasebo yok; karar satırı değil.

## Huni ve getirisiz olay sayımı (sinyal: sinyal günü; olay: OC tekil sonrası, giriş dönemi)

### Y6 hunisi

| Aşama | ABD sinyal (tümü) | ABD olay 2016-22 / 2023 / 2024-26 | AVR sinyal (tümü) | AVR olay 2016-22 / 2023 / 2024-26 | BIST sinyal (tümü) | BIST olay 2016-22 / 2023 / 2024-26 |
|---|---|---|---|---|---|---|
| Y1 (S6 AL) | 37969 | 8686 / 2042 / 4153 | 18783 | 4496 / 815 / 1743 | 10242 | 2588 / 381 / 1759 |
| + (a) hat net (>= 3 dokunuş, eğim) | 20720 | 6093 / 1500 / 2958 | 10683 | 3313 / 597 / 1274 | 5432 | 1761 / 223 / 1162 |
| + (b) gerçek kırılım (%1 + mum) | 7999 | 3046 / 876 / 1650 | 3426 | 1532 / 328 / 596 | 3539 | 1300 / 164 / 856 |
| + (c) stop <= %10 (C_t ön eleme) | 2153 | 1117 / 242 / 435 | 1420 | 723 / 119 / 248 | 327 | 155 / 8 / 84 |
| + (d) büyük desen alçalan değil = Y6 | 1738 | 930 / 181 / 347 | 1100 | 557 / 83 / 201 | 219 | 110 / 7 / 48 |
| Y6 + hafıza temiz = Y8 | 1256 | 737 / 103 / 214 | 862 | 449 / 54 / 153 | 118 | 59 / 5 / 27 |
| Y6 + patlamış yapı var = Y8B (bilgi) | 482 | 195 / 78 / 134 | 238 | 108 / 29 / 49 | 101 | 51 / 2 / 22 |

Tek başına düşürdüğü taban sinyali (şart tutmayan): ABD: f_hat 17249, f_kir 23016, f_stop 22664, f_buyuk 8961, kir250>0 14525, büyük desen NA 0; AVR: f_hat 8100, f_kir 12545, f_stop 8903, f_buyuk 4387, kir250>0 5160, büyük desen NA 0; BIST: f_hat 4810, f_kir 3638, f_stop 8720, f_buyuk 2861, kir250>0 5193, büyük desen NA 0.

### Y7 hunisi

| Aşama | ABD sinyal (tümü) | ABD olay 2016-22 / 2023 / 2024-26 | AVR sinyal (tümü) | AVR olay 2016-22 / 2023 / 2024-26 | BIST sinyal (tümü) | BIST olay 2016-22 / 2023 / 2024-26 |
|---|---|---|---|---|---|---|
| Y3 (KAZAN + DÖNÜŞ) | 30010 | 4189 / 940 / 2039 | 7632 | 1537 / 190 / 476 | 9560 | 1348 / 432 / 1078 |
| + (a) iki kenar (%5) | 6023 | 1125 / 283 / 542 | 937 | 276 / 34 / 79 | 1759 | 268 / 196 / 259 |
| + (b) dipte küçük mum (0,9 ATR) | 2056 | 321 / 169 / 198 | 163 | 36 / 17 / 24 | 978 | 128 / 79 / 190 |
| + (c) dip savunması (>= 3) | 317 | 43 / 45 / 31 | 31 | 7 / 6 / 4 | 182 | 19 / 14 / 56 |
| + (d) stop <= %10 (C_t ön eleme) = Y7 | 0 | 0 / 0 / 0 | 0 | 0 / 0 / 0 | 0 | 0 / 0 / 0 |

Tek başına düşürdüğü taban sinyali (şart tutmayan): ABD: f_kenar 23987, f_mum 16882, f_dok 21317, f_stop 29683; AVR: f_kenar 6695, f_mum 5452, f_dok 4541, f_stop 7404; BIST: f_kenar 7801, f_mum 2885, f_dok 6207, f_stop 9491.

| Deneme | Pazar | hisse | olay 2016-22 / 2023 / 2024-26 (E5a sonrası) | stop_uzak 2016-22 / 2023 / 2024-26 |
|---|---|---|---|---|
| Y6 | ABD | 752 | 867 / 163 / 314 | 63 / 18 / 33 |
| Y6 | AVR | 434 | 522 / 80 / 184 | 35 / 3 / 17 |
| Y6 | BIST | 163 | 87 / 5 / 42 | 23 / 2 / 6 |
| Y7 | ABD | 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Y7 | AVR | 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Y7 | BIST | 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Y8 | ABD | 594 | 694 / 93 / 198 | 43 / 10 / 16 |
| Y8 | AVR | 366 | 426 / 52 / 139 | 23 / 2 / 14 |
| Y8 | BIST | 100 | 46 / 4 / 24 | 13 / 1 / 3 |
| Y8B | ABD | 342 | 175 / 70 / 116 | 20 / 8 / 18 |
| Y8B | AVR | 167 | 96 / 28 / 45 | 12 / 1 / 4 |
| Y8B | BIST | 82 | 41 / 1 / 18 | 10 / 1 / 4 |

Güç: 1. turun güç tablosu (GUC_TABLOSU.md; aynı dört şartlı kural, ABD 2023-26 rastgele hisse-gün). Hücre n < 1.000 ve güç < %80 ise tutmayan hücre ÖLÇÜLEMEDİ yazılır (1. turla aynı).

## Önceden bilinen sınırlar (getirisiz sayımdan; sonuç görülmeden)

- Y6: ABD 2023 en çok 163 olay (güç %11); ABD 2024-26 en çok 314 olay (güç %57); AVR 2023 en çok 80 olay (güç %2); AVR 2024-26 en çok 184 olay (güç %11). Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır.
- Y7: karar hücrelerinde OLAY YOK (ABD 2023 en çok 0 olay (güç %0); ABD 2024-26 en çok 0 olay (güç %0); AVR 2023 en çok 0 olay (güç %0); AVR 2024-26 en çok 0 olay (güç %0)). Ön eleme şartları birlikte hiç olay bırakmadı (huni son aşaması): Y7 ÖLÇÜLEMEDİ (n = 0) olur. Eşik değiştirilmedi (ön kayıt kuralı; değişiklik ana model kararıdır).
- Y8: ABD 2023 en çok 93 olay (güç %2); ABD 2024-26 en çok 198 olay (güç %11); AVR 2023 en çok 52 olay (güç %2); AVR 2024-26 en çok 139 olay (güç %11). Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır.
- n üst sınırdır: 15 bar ölçülemeyen ve eşi < 3 olan olaylar ölçümde ayrıca düşer.

## YH_ESIK 2. tur girdileri (tam metin; geri kalanı ON_KAYIT.md ile aynı)

```json
{
 "Y6": {
  "ad": "Y1 + HAT NET + GERÇEK KIRILIM + STOP YAKIN + BÜYÜK DESEN",
  "buyuk_egim": -0.05,
  "buyuk_gun": 250,
  "buyuk_parca": 25,
  "dokunus_egim": 0.99,
  "dokunus_min": 3,
  "e5b": {
   "giris_carpan": 0.95,
   "hat_carpan": 0.98
  },
  "hat_bant": 0.015,
  "kir_pay": 0.01,
  "stop_uzak": 0.1,
  "taban": "Y1",
  "tanim": "Y1 olayı t (S6 'al' günü; hat ve tavan Y1'deki gibi) + dört şart. BÖLGE = durum AL ise [kutu_sol_i(t), t-1] (açık S6 bölgesinin as-of t kutusu, t hariç), AL_BOLGESIZ ise t-1 taban penceresi [bas_i(t-1), t-1]. (a) HAT NET (E2): bölgede Low <= hat x 1,015 olan bar sayısı >= 3 VE son dokunuşun Low'u >= ilk dokunuşun Low'u x 0,99 (eğim aşağı değil); (b) GERÇEK KIRILIM (E3): C_t > tavan x 1,01 (tavan = Y1 TAVAN(t-1)) VE (H_t - L_t) >= bölge içi (H - L) medyanı; (c) STOP UZAKLIĞI (E5a): sinyalde C_t / hat - 1 <= 0,10 (ön eleme), ölçümde gerçek giriş (t+1 açılış) / hat - 1 <= 0,10 yeniden denetlenir, aşan olay ölçülmez ve 'stop_uzak' sayımına düşer; (d) BÜYÜK DESEN ALÇALAN DEĞİL (E1): [t-250, t-1] 250 geçerli bar, ardışık 10 parça x 25 bar, her parçanın min Low'u; bu 10 noktaya doğru (en küçük kareler, x = 0..9); eğim = uyum(9) / uyum(0) - 1 >= -0,05 (uyum(0) <= 0 ise şart tutmaz); t'den önce 250 geçerli bar yoksa (d) UYGULANMAZ (şart geçer, ek sütunda 'buyuk_desen=NA'). stop0 = hat x 0,98 (1. turla aynı). Bilgi (E5b): stop0b = max(hat x 0,98, giriş x 0,95) ile olay ve eş (aynı gün aynı kova, aynı d_b) hedef / stop payları ayrı sütun (b_*); karar satırı değil",
  "tur": 2,
  "yon": 1
 },
 "Y7": {
  "ad": "Y3 + KAZAN ŞARTLARI + STOP YAKIN",
  "atr_gun": 250,
  "atr_min": 120,
  "dip_bant": 0.015,
  "dokunus_min": 3,
  "e5b": {
   "giris_carpan": 0.95,
   "hat_carpan": 0.98
  },
  "kenar": 1.05,
  "mum_k": 0.9,
  "stop_uzak": 0.1,
  "taban": "Y3",
  "tanim": "Y3 olayı t (Y3'ün seçtiği EN BÜYÜK n ile pencere W = [t-n, t-1], hat = dip(W)) + dört şart, aynı W üzerinde (Y7 ⊆ Y3 sinyalleri). Üçte birler: ilk = W[0 : n//3], orta = W[n//3 : 2n//3] (Y3'teki orta ile aynı), son = W[2n//3 : n]. (a) İKİ KENAR: min L(ilk) >= min L(orta) x 1,05 VE min L(son) >= min L(orta) x 1,05; (b) DİPTE KÜÇÜK MUM: orta üçte birde mum boyu (H - L) / C medyanı <= 0,90 x ATR250, ATR250 = pencereden ÖNCEKİ 250 geçerli barın ortalama TR / C_önceki'si (S6 refOnce ile aynı birim; 250 yoksa en az 120 bar, 120 de yoksa şart tutmaz); (c) DİP SAVUNMASI: W'de Low <= dip(W) x 1,015 olan bar sayısı >= 3; (d) E5a: sinyalde C_t / hat - 1 <= 0,10, ölçümde giriş / hat - 1 <= 0,10 (aşan 'stop_uzak'). Bilgi E5b Y6 gibi",
  "tur": 2,
  "yon": 1
 },
 "Y8": {
  "ad": "Y6 + CEMAL HAFIZASI (patlamış yapı yok)",
  "gun": 250,
  "stop_uzak": 0.1,
  "taban": "Y6",
  "tanim": "Y6 olayı t ve [t-250, t-1] içinde durum KIRILDI ile biten S6 bölgesi (kapanış < dip x 0,98; S6 kirTol 0,02) YOK -> olay; varsa düşer (yalnız geçmiş; Y4'teki KIRILDI sayımıyla aynı aralık)",
  "tur": 2,
  "yon": 1
 },
 "Y8B": {
  "ad": "Y6 + patlamış yapı VAR (bilgi, aleyhte)",
  "bilgi": true,
  "gun": 250,
  "stop_uzak": 0.1,
  "taban": "Y6",
  "tanim": "Y8'in tersi: Y6 olayı ve [t-250, t-1] içinde KIRILDI ile biten S6 bölgesi >= 1 (karşılaştırma için bilgi satırı; etiket yazılır ama karar değildir). `kos --deneme ...Y8` Y8B'yi kendiliğinden ekler",
  "tur": 2,
  "yon": 1
 }
}
```

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş / taban / plasebo 1. turla AYNI kod (yh_olay_olc, yh_sim): aynı giriş günü, aynı OC kovası, AYNI d, aynı hedef / takip / 15 bar; yeni şartlar yalnız olay seçimini değiştirir; E5a stop uzaklığı şartı d'yi küçültür ama eşlere AYNI d verilir (mekanik stop farkı dışlandı); E5b bilgi satırında da eşlere aynı d_b; Y8B (aleyhte) karşılaştırma satırı; güç tablosu 1. turunki (aynı kural) |
| K2 | geleceğe bakma | EVET | Y6 bölgesi [sol, t-1] ve hat / tavan t ve öncesi (S6 durum makinesi nedensel); büyük desen [t-250, t-1]; Y7 W = [t-n, t-1], ATR pencere öncesi; Y8 KIRILDI sayımı [t-250, t-1]; E5a ölçüm denetimi giriş açılışı (karar anında bilinir); test_yapi_hedef 'geleceğe bakma' Y6 / Y7 / Y8 / Y8B kesik seri = tam seri; koşuda her deneme x pazar 5 rastgele olay kesik veriyle (yh_gelecek_denetimi, DURUR) |
| K3 | geçerli bar | EVET | aynı geçerli bar süzgeci (OC.oc_veri_hazirla + SY.sy_veri_hazirla: H>L, V>0, O/H/L/C>0); dokunuş / medyan mum / büyük desen / ATR yalnız geçerli barlarda |
| K4 | tekilleştirme | EVET | OC.oc_olay_hazirla aynı hissede 60 takvim günü tekil (deneme başına); stop_uzak düşmesi tekilden SONRA (sayımda); n = bağımsız olay; getiri ortalama + medyan |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (OC); E5a ölçümde gerçek giriş açılışıyla yeniden denetlenir (C_t ön elemesi yalnız sinyal günü bilgisi) |
| K6 | veri birimi | EVET | aynı V_*.pkl tek kip; bütün yeni şartlar oran (dokunuş bandı, kırılım payı, eğim, iki kenar, mum / ATR oran birimi); AVR yerel para (oran birimden bağımsız) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; eş ve plasebo aynı evrenden; rapora yazılır |
| K8 | örneklem ve dönem | EVET | şartlar olay sayısını düşürür: huni ön kayıtta (getirisiz); n < 30 ÖLÇÜLEMEDİ, DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; Y6 / Y7 / Y8 x 4 karar hücresi BH q 0,10 (bilgi, 1. tur BH'si ayrı); küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | ON_KAYIT_2.md: YH_ESIK sha (yeni), ESIK_TUR1_SHA (Y6-Y8B çıkarılınca 1. tur mührü = ON_KAYIT.md ve güç tablosu sha'sı; Y1-Y5 eşikleri değişmedi kanıtı), kod / OC / S6 / FV / güç / Y2 sha; yh_kapi(tur 2) hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt ayrı commit, ölçüm ikinci commit; eşikler Cemal'in değerlendirmesinden (sonuç görülerek) yazıldı: bu ölçüm bağımsız kanıt değil, ileri test gerekir (raporda) |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV |
| K11 | yeniden üretim | EVET | olay_Y6..Y8B.csv.gz satır dosyaları; RAPOR_2.md 'YENİDEN ÜRETİM' iki hücre bağımsız komutla; Y1 ABD 2023 regresyonu (n 2040, KAT5 0,9752) yeni kodla yeniden üretildi |
| K12 | ifade | EVET | etiket yalnız YH_ESIK['etiket'] kuralıyla; Y8B 'bilgi' (karar değil); 'iz değil' yazılmaz; sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_ / YH_ önekli); yasak defter dosyalarına dokunulmadı (git diff); e-posta / anahtar taraması; push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm |

## SAPMALAR

(yok)

## Test

`python test_yapi_hedef.py` (1. tur testleri aynen + 2. tur: hat dokunuş sayımı, kırılım payı, iki kenar, büyük desen eğimi, Y8 hafızası, Y6 / Y7 / Y8 / Y8B geleceğe bakma (prefix), ESIK_TUR1_SHA = 1. tur mührü, 2. tur uçtan uca kos + kapı).
