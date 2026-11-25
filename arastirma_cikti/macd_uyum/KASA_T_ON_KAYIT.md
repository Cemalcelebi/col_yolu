# MACD_UYUM — KASA KÖR SINAMASI ÖN KAYIT (T: derin toplam uyumsuzluk; KASA açılmadan ÖNCE)

Yazan: ana model, 2026-11-25 (TR 08:5x). Cemal'in onayı (25 Kas 08:47): "Aç".
Bu dosyanın ana bölümü (tanım, ölçü, karar) kasa açılmadan önce commit edilir ve sonra DEĞİŞMEZ. Teknik ek (sha'lar, kontrol tablosu, getirisiz sayımlar) alt ajan tarafından kasa açılmadan önce EK olarak eklenir.

## Hipotez (tek; değiştirilmez)
T = U1 olayı VE PFc <= -0,10 VE MRc >= 0,30.
- U1: Ç217 MACD_UYUM tanımı aynen (MU_ESIK, YH_ESIK8; DİPTE, Ş10, F68, olay günü kuralı, 15 bar tekil).
- Zincir: UYUM_Z_ON_KAYIT tanımı (önceki U1 olayı en çok 60 geçerli bar önce ve Low(L2) daha düşükse sıra + 1). Zincir 2022 ve öncesindeki (açık) olaylardan başlayabilir.
- PFc, MRc: UYUM_T_ON_KAYIT tanımı (zincirin ilk olayının L1 dibi ve o dipteki MACD'ye göre).
- Eş: CETVEL2 v2.2 konum eşi (aynı giriş günü, aynı pazar, ATRP x likidite x F15 kovası, kovadaki bütün hisseler, en az 5) + K20 temiz eş (ES_ON_KAYIT: eşin giriş gününden önceki 20 barda ham U1 durumu varsa dışarıda).
- Giriş t+1 açılış; R15 = 15. geçerli bar kapanışı / giriş − 1.

## Kasa
- Bloklar: 2023Q1 .. 2024Q4 (8 blok), hipotez adı MACD_UYUM_T, bir kez. 2025 blokları AÇILMAZ.
- Olay dönemi: giriş günü 2023-01-01 .. 2024-12-31 ve R15 penceresi 2024-12-31'i aşmayan olaylar.
- Hücreler: ABD (2023-24), AVR (2023-24) = karar; BIST bilgi. Yıl ayrımı (2023 / 2024) bilgi.

## Ölçüler
- Ö1 (ANA; Cemal 25 Kas: 'asıl iz, eşler içinde en çok zıplayanı bulmaktır'): ÜST10 = olayın temiz eşleri içindeki sırası >= 0,90 olan olay payı; ALT10 = sıra <= 0,10 payı. Ay kümeli bootstrap %95 (B 2000, giriş ayı).
- Ö2: R15 temiz eş FARK (olay − eş ortalaması), ay kümeli boot %95; SIRA ortalaması; C2.c2_hucre + MU.mu_hukum (plasebo hariç) hükmü.
- Ö3 (bilgi): piyasa yukarı (eş ortalaması > 0) ve aşağı günlerde ÜST10 / ALT10; +%5 hedef ve stop payları olay / eş; kontrol Tz (T dışındaki U1 olayları) aynı ölçüler.

## Karar kuralı (sonuçtan sonra değişmez)
- TUTTU ⇔ (a) ABD + AVR birleşik ÜST10 payının boot %95 alt ucu > 0,10 VE (b) birleşik ÜST10 > ALT10 VE (c) ABD'de ve AVR'de ayrı ayrı ÜST10 nokta payı > 0,10 VE (d) birleşik R15 FARK > 0.
- KISMEN ⇔ (b), (c), (d) tutuyor ama (a) tutmuyor (yön doğru, kanıt yetersiz).
- TUTMADI ⇔ aksi.
- Birleşik olay sayısı < 100 ise hüküm ÖLÇÜLEMEDİ (yön yine yazılır).
- Açık veri beklentisi (2016-22, ABD + AVR, n 669): ÜST10 %16,6 [13,7; 19,7], ALT10 %14,5, FARK +0,4 .. +1,6 puan. Bu sayılar keşiftir (7-8. bakış); kasa sonucu onlardan bağımsız okunur.
- Sonuç ne olursa olsun yazılır; kasa bu hipotez için ikinci kez açılmaz; tanım / eşik düzeltmesi yapılmaz.
- Evren yalnız bugün işlem görenler: sonuç yukarı yanlı (K7). Komisyon / kayma yok. Tek başına alım-satım kuralı değildir (tarayıcı yalnız aday bulur).
