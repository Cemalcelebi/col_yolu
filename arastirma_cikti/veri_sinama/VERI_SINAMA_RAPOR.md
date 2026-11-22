# Veri sınaması (22 Kasım 2026): göz PDF'i ve Tiingo karşılaştırması

## Bulgu özeti
- İŞ 1 TAMAM: `VERI_SINAMA_GOZ.pdf` (15 sayfa: kapak + 14 hisse; 293 KB). Cemal TradingView ile karşılaştıracak.
- İŞ 2 YARIM: Tiingo, 36 örnek isteğin hepsine "aylık 500 sembol sorgu kotası doldu" döndürdü (HTTP 200, gövdede hata). Saatlik 20 dakika beklemek çözmez; kota AYLIK. 36 hissenin kendisi karşılaştırılamadı. **EVREN HÜKMÜ: VERİLEMEDİ** (33/36 şartı sınanamadı). Bu bir "VERİ SORUNLU" kararı değildir.
- Karşılaştırılabilen tek hisse AAPL (kota öncesi sorgulanmış sembol, 2016-2023, 2.012 ortak gün): getiri korelasyonu 0,99999996; |fark| > %1 gün sayısı 0; bizim Kapanış / Tiingo adjClose oranı ortalama 1,0007, değişim katsayısı 6,3e-5 (sabit); bizim Kapanış / Tiingo ham close oranı CV 0,67 (bölünme + temettü nedeniyle sabit değil, beklenen); açılış farkı payı %0,15; yüksek ve düşük farkı payı %0; hacim oranı medyanı 1,0000 (adjVolume ile; ham hacimle 4,0 = 4:1 bölünme); eksik/fazla gün 0/0. AAPL TEMİZ. Tek hisse hüküm değildir.
- Sonuç: ABD fiyatları BÖLÜNME + TEMETTÜ AYARLI (Tiingo adjClose ile aynı). Bu yalnız AAPL ile bağımsız doğrulandı (n = 1); Yahoo kaynaklı kontrol (MSFT 02.01.2018 kapanış 78,55 vs ham 85,95) aynı yönde.

## Veri kipi tespiti (iş 1, kapağa yazıldı)
| Pazar | Kip | Kanıt |
|---|---|---|
| ABD (V_ABD) | bölünme VE temettü ayarlı | AAPL 02.01.2018 kapanış 40,23; ham 172,26, yalnız 4:1 ayarlı 43,07; 31.08.2020'de süreklilik (123,2 -> 128,7 sıçrama yok); Tiingo adjClose ile oran sabit |
| BIST (V_BIST) | Yahoo ham kapanış (auto_adjust=False), bölünme/bedelsiz kodla ayarlı (`fi_duzelt`, `fi_k1_veri`), temettü ayarı YOK | FON_IZI.py başlığı ve `fi_k1_veri` okuması; bağımsız kaynakla DOĞRULANMADI (BIST için Tiingo yok) |
| AVR (V_AVR) | temettü ayarı TESPİT EDİLEMEDİ | BATS.L 02.01.2018 kapanış 4.909 pens ham fiyata yakın görünür, RCO.PA 97,72 € ayarlı olabilir; kod okumasında auto_adjust belirtisi yok. Cemal'in göz karşılaştırması bunu da gösterecek |

## İş 1: seçim (tohum 20261122)
Evren: yalnız 29.12.2023'te işlem gören, >= 400 bar; son 20 gün medyan işlem değeri (Close x Hacim, AVR'de x Kur) evren medyanının üstünde. Hareket günü: 2018-2023'te tek günde |getiri| > %15 olan gün, pencerenin ortasına yerleştirildi. Pencere 120 işlem günü. Geçersiz bar (H<L, hacim 0) atıldı.

| Sayfa | Hisse (TradingView) | Tür | Pencere |
|---|---|---|---|
| 1 | NTLA | büyük hareket (17.03.2020 +%22,7) | 17.12.2019 - 09.06.2020 |
| 2 | CROX | büyük hareket | 31.01.2023 - 24.07.2023 |
| 3 | WTRG | büyük hareket (Mart 2020) | 18.12.2019 - 10.06.2020 |
| 4 | SNPS | rastgele | 18.08.2022 - 08.02.2023 |
| 5 | ABT | rastgele | 17.01.2020 - 09.07.2020 |
| 6 | CAT | rastgele | 14.04.2020 - 01.10.2020 |
| 7 | LSE:BATS | rastgele | 13.06.2019 - 28.11.2019 |
| 8 | OMXSTO:TEL2_B | rastgele | 11.12.2018 - 11.06.2019 |
| 9 | EURONEXT:RCO | rastgele | 09.01.2019 - 28.06.2019 |
| 10 | BIST:BURCE | büyük hareket | 16.04.2019 - 14.10.2019 |
| 11 | BIST:LIDFA | büyük hareket | 10.10.2018 - 28.03.2019 |
| 12 | BIST:AVHOL | büyük hareket (12.03.2020 -%16,3) | 17.12.2019 - 10.06.2020 |
| 13 | BIST:TRMET | rastgele | 21.03.2018 - 14.09.2018 |
| 14 | BIST:ENJSA | rastgele | 20.01.2022 - 14.07.2022 |

Notlar: (1) ABD ve BIST'te üçer "büyük hareket" penceresi var (şart: en az ikişer). (2) Hareket günleri piyasa çapında Mart 2020 çöküşüne denk gelenler gerçek harekettir; bölünme günü fiyat serisinden AYIRT EDİLEMEZ, çünkü seriler ayarlı (bölünme sıçraması zaten giderilmiş) ve pencerelerde bilinen bir bölünme yoktur. Bu yüzden sayfalarda "büyük hareket günü" etiketi kullanıldı; ayarın kendisini (bölünme düzeltmesi) AAPL (31.08.2020) Tiingo karşılaştırması sınadı. (3) Tür "rastgele" olanlarda büyük hareket şartı aranmadı. (4) "Bilinen hisse" şartı yalnız üst-yarı likiditeyle sağlandı; BURCE, LIDFA, NTLA gibi daha az tanınan isimler çıkabildi. Borsa kodu (BATS -> LSE, TEL2-B -> OMXSTO:TEL2_B, RCO -> EURONEXT) TAHMİNDİR; TradingView'da bulunamazsa Yahoo kodu başlıkta var.

## İş 2: Tiingo
Kaynak: api.tiingo.com daily prices, 2016-01-04..2023-12-29. Örnek (tohum 20261122, V_ABD'den 6 göz hissesi hariç 30 + 6 göz hissesi) 36 hisse. Betik: `veri_sinama_tiingo.py` (önbellek repo dışında, lisans).

| Sonuç | Sayı |
|---|---|
| İstenen | 36 |
| Veri dönen | 0 (hepsi aylık kota mesajı) |
| "YOK" (Tiingo'da yok) | 0 |
| Kota engeli | 36 (SON ASST DUK ARRY TGT CRSR CGAU EBAY EPAM ACVA SGML PEP RUN DPZ WEAV RYAM BMRN NTAP LNTH SSRM ESI SPRY VLTO ENB PCOR TREX ABTC DRH CPT SPG NTLA CROX WTRG SNPS ABT CAT) |
| Temiz / 36 | HÜKÜM VERİLEMEDİ |

Toplam atılan istek 39: 36 örnek + 1 başlangıç sondası (AAPL, kotadan önce; sonuç saklanmamıştı) + 1 KO (kotanın sürdüğünü doğrulama) + 1 AAPL (sonuç saklı). Sınır 45'i geçmedi. Sonraki adım: kota yenilenince (ay başı) aynı komutla (`python veri_sinama_tiingo.py indir` + `karsilastir`) 36 hisse koşulur; önbellek AAPL dışında hata yanıtı içerdiğinden `TIINGO_CACHE` dizini boş bir yola yönlendirilmeli.

## HATA
- H-a (süreç): Tiingo bir kota hatasını HTTP 200 ile döndürüyor; ilk koşuda betik bunu veri sandı ve önbelleğe yazdı (karşılaştırmada yakalandı; betik artık `detail` gövdesini KOTA sayar). Düzeltildi.
- H-b (varsayım): görev metni "saatte 50 istek" kotasını varsayıyordu; gerçek engel AYLIK 500 sembol sorgusu. 20 dakika bekleme işe yaramazdı.
- H-c (sınırlama): bölünme günü fiyat serisinden ayırt edilemedi (ayarlı seri), etiket "büyük hareket günü".

## KONTROL LİSTESİ (yalnız ilgili maddeler)
| Madde | Durum | Kanıt |
|---|---|---|
| K2 geleceğe bakma | UYGULANMAZ | Ölçüm yok; yalnız 2018-2023 geçmiş pencere, veri 29.12.2023'e kesik |
| K3 geçerli bar | EVET | H>=L, V>0, Close>0 olmayan bar hem seçimde hem grafikte atıldı (`veri_sinama_sec.py`, `veri_sinama_goz.py`) |
| K6 veri birimi | EVET | Kip tespiti yukarıda; ABD adjClose ile doğrulandı, AVR kipi açıkça "tespit edilemedi", BIST kod okumasıyla; Londra pens notu kapakta |
| K10 ayrıştırma | EVET | PDF tablosu (6 gün) goz_pencereler.json ve V_*.pkl ile aynı kodla üretildi; 2 sayfa görsel kontrol edildi (NTLA, AVHOL: tablo değerleri grafikle tutarlı) |
| K13 süreç | EVET | Defter / CLAUDE.md / mevcut modüllere dokunulmadı; anahtar yazılmadı, e-posta yok; kota 45 altında; kod değişmedi, yeniden başlatma gerekmez |
