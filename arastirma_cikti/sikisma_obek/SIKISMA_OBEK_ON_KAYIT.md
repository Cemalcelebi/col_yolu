# SIKISMA_OBEK (S5, öbek sıkışması) — ÖN KAYIT

SIKISMA_OBEK v1.0 (2026-11-15): öbek sıkışması S5 (öbek + zıplama hariç küçük mum + Bollinger şart; DİP / YOL ÜSTÜ sınıfı) -> büyük hareket

- MÜHÜR (SO_ESIK sha256): `de384bbd246bb4896246a140b84597324d8c9c5162ed33c73043bafa6a938e32`
- KOD (SIKISMA_OBEK.py sha256): `dcebf41d3ec39c9d2d62d3c2bab30ad453a7e9a1abc9f04b7385d7100e5be7d8`
- SC_KOD (SIKISMA_CEMAL.py sha256): `f5c5fd4749dc10b00113bcc8d93224a4d5be990091654dfe963241f9c7561ec8`
- SY_KOD (SIKISMA_YENIDEN.py sha256): `ecc369cd01edacfcf965713dddb18cf9baeacca32a4d3994558c58ebc6cd19ae`
- ZAMAN (UTC): `2026-11-15 09:14:25 UTC`
- Tasarım sınaması commit: `886a8d03227fedb07fa331e408297d11d0954ad0` (2026-11-15T09:10:15+00:00); SIKISMA_OBEK_TASARIM.md.
- Bu dosya ölçümden ÖNCE yazılır ve commit + push edilir; `kos` OC.oc_kapi (kontrol + cetvel sha + git) ve kendi kapısı (mühür, üç kod sha, git'e işlenmiş ve değişmemiş) geçmezse durur.

## Cetvel mühür satırları (ORTAK_CETVEL; aynen)

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`

## Soru
Cemal'in üç grafikle düzelttiği öbek sıkışması (S5; DİP ve YOL ÜSTÜ sınıfı) bitince 20 günde hissenin olağan ölçüsüne göre büyük hareket (B1 tek gün, BH2 çok gün) eşlerden sık mı; ne zaman, hangi yöne; sıkışma mumunun 2x / 3x mumu ne sıklıkla geliyor. 60 gün getiri ve yönsüz işlem bilgi.

## Tanım (SO_ESIK['S5']; seçilen ızgara noktası DONDU)

- Seçilen: p = 15, k_m = 0.75, bant BIST %8 / ABD %6 / AVR %6, bb = 0.2, uzunluk 'p'.
- (a) pencerenin en büyük 1 (H-L)/C değeri çıkarılır; kalan p-1 değerin medyanı <= k_m x ATR250% (t-249..t ort TR/C_önceki)
- (b) pencere kapanışlarından en yüksek YA DA en düşük 1 gün (bandı en çok daraltan) çıkarılır; max/min - 1 <= bant
- (c) ln C ~ gün doğrusal eğimi (EKK) x p, [-%2, +%10] içinde
- (d) pencerede O < önceki geçerli barın C'si olan günlerin payı <= %50
- (e) BBW_t = 4 x std20(C, ddof 0) / SMA20(C); pay(BBW_t-250..t-1 <= BBW_t) <= bb
- (f) 'p': ek şart yok (pencere yeter); '10': (a)&(b)&(e) t'de biten en az 10 ardışık geçerli barda doğru
- (DIP) konum120 = (C_t - min C t-119..t) / (max - min) <= 0,25 VE C_t / max C t-119..t - 1 <= -%10
- (YOL) C_t > SMA50_t VE SMA50_t > SMA50_t-20 VE konum120 >= 0,60 VE min C (pencere) >= min C (pencerenin ilk 5 günü) x 0,99
- (olay) S5 günü = (a)..(f) VE (DIP ya da YOL); olay = S5 günü ve önceki 19 barda S5 günü yok (bölge ilk günü = karar günü); bölge sonu = 20 bardan kısa aralarla süren S5 günlerinin sonuncusu; sınıf = karar günü sınıfı
- Geçmiş: en az 290 geçerli bar. Uygunluk: SY 'uygun' ile aynı (likidite alt %20 dışı, σ250 / ATR250 / likidite tanımlı, 20 gün gelecek barı var, dönem içinde) + en az 290 geçerli bar + bölünme şüphesi [t-260, t] içinde yok (yalnız geçmiş).
- Bölünme şüphesi: SY.sy_bolunme_supheli ANA, pencere [-260, 0] (yalnız geçmiş).
- Izgara (tasarımda ayarlandı): {"p": [15, 20], "k_m": [0.65, 0.75, 0.85], "bant": [{"BIST": 0.08, "ABD": 0.06, "AVR": 0.06}, {"BIST": 0.1, "ABD": 0.08, "AVR": 0.08}], "bb": [0.15, 0.2, 0.25], "uzunluk": ["p", "10"]}.
- Seçim kuralı: (1) 7 örnek x 2 fiyat kaynağı (ekran / V_BIST) = 14 sınamanın hepsini tutan noktalar; yoksa en çok tutan noktalar. (2) Aralarından EN SADE: orta noktadan (p 15, k_m 0,75, bant 8/6, bb 0,20, uzunluk 'p') farklı parametre sayısı en az. (3) Eşitlikte sıra: p küçük, |k_m - 0,75| küçük, bant dar, |bb - 0,20| küçük, uzunluk 'p'; yine eşitse SIKI olan (k_m küçük, bb küçük).

## Tasarım sınaması (ön kayıttan önce; getirisiz)

En çok tutan 14 / 14 sınama (7 örnek x 2 fiyat kaynağı); 14/14 tutan nokta 16; seçilen nokta yukarıda. Kaçan: YOK.

| örnek | kaynak | beklenen | S5 sonucu | (a) mum | (b) öbek | (c) eğim | (d) aşağı açılış | (e) BB | (f) uzunluk | (a-f) hep | DİP | YOL | tutar | en iyi gün ölçüleri (mum/ATR, öbek, eğim, BB yüzdelik, konum120, 120 gün tepeden) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FENER-E 10-14..11-07 | ekran | SEÇ DIP | S5 2025-10-31 (DIP), 6 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.62, %3.8, %+2.2, 0.16, 0.01, %-83 (2025-10-31) |
| FENER-E 10-14..11-07 | V_BIST | SEÇ DIP | S5 2025-10-31 (DIP), 6 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.69, %3.8, %+2.2, 0.16, 0.12, %-30 (2025-10-31) |
| CCOLA-E 10-02..10-20 | ekran | SEÇ DIP | S5 2025-10-02 (DIP), 10 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.62, %5.4, %-1.7, 0.08, 0.2, %-15 (2025-10-02) |
| CCOLA-E 10-02..10-20 | V_BIST | SEÇ DIP | S5 2025-10-02 (DIP), 10 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.62, %5.4, %-1.7, 0.08, 0.2, %-15 (2025-10-02) |
| ENJSA-T 07-10..08-14 | ekran | SEÇ YOL | S5 2025-08-06 (YOL), 5 gün | E | E | E | E | E | E | E | - | E | TUTTU | 0.65, %4.2, %+0.6, 0.17, 0.93, %-2 (2025-08-06) |
| ENJSA-T 07-10..08-14 | V_BIST | SEÇ YOL | S5 2025-08-06 (YOL), 5 gün | E | E | E | E | E | E | E | - | E | TUTTU | 0.65, %4.2, %+0.6, 0.17, 0.93, %-2 (2025-08-06) |
| FENER-A 12-03..12-16 | ekran | SEÇME | S5 yok | E | - | - | E | - | E | - | E | - | TUTTU | 0.70, %19.1, %-20.9, 0.53, 0.02, %-79 (2025-12-05) |
| FENER-A 12-03..12-16 | V_BIST | SEÇME | S5 yok | E | - | - | E | - | E | - | E | - | TUTTU | 0.73, %20.9, %-23.3, 0.75, 0.06, %-32 (2025-12-10) |
| CCOLA-T 07-29..08-29 | ekran | SEÇME | S5 yok | E | E | E | E | E | E | E | - | - | TUTTU | 0.61, %5.5, %+1.3, 0.05, 0.28, %-15 (2025-07-29) |
| CCOLA-T 07-29..08-29 | V_BIST | SEÇME | S5 yok | E | E | E | E | E | E | E | - | - | TUTTU | 0.67, %5.5, %+1.3, 0.05, 0.28, %-15 (2025-07-29) |
| ENJSA-O 01-20..02-14 | ekran | SEÇME | S5 yok | E | E | E | E | E | E | E | - | E | TUTTU | 0.69, %3.7, %-0.6, 0.02, 0.82, %-3 (2025-02-14) |
| ENJSA-O 01-20..02-14 | V_BIST | SEÇME | S5 yok | E | E | E | E | E | E | E | - | E | TUTTU | 0.69, %3.7, %-0.6, 0.02, 0.82, %-3 (2025-02-14) |
| ENJSA-A 12-30..01-27 | ekran | SEÇME | S5 yok | E | E | E | E | E | E | - | - | E | TUTTU | 0.75, %6.5, %+7.1, 0.2, 1.0, %+0 (2026-01-09) |
| ENJSA-A 12-30..01-27 | V_BIST | SEÇME | S5 yok | E | E | E | E | E | E | - | - | E | TUTTU | 0.75, %6.5, %+7.1, 0.2, 1.0, %+0 (2026-01-09) |

## Sonuçlar (SIKISMA_CEMAL / SIKISMA_YENIDEN içe alınır)

- **B1**: SC / SY B1 aynen: t+1..t+20 içinde bir günün TR/C_önceki >= 3 x ATR250%
- **BH2**: SC BH2 (SY B2) aynen: max_k |ln(C_t+k / C_t)|, k=1..20 >= max(%15, 3 x σ250 x √20)
- **B1k2**: t+1..t+20 içinde bir günün TR/C_önceki >= 2 x ATR250% (yıllık ATR'nin 2 katı)
- **BH2k2**: max_k |ln(C_t+k / C_t)| >= max(%15, 2 x σ250 x √20)
- **B0**: t+1..t+20 içinde bir günün TR/C_önceki >= 3 x pencere ort TR/C_önceki (göreli; tanımsal, bilgi)
- **M2**: t+1..t+20 içinde bir günün (H-L)/C_önceki >= 2 x sıkışma mumu (t'deki (a) ölçüsü: zıplama hariç medyan mum) (Cemal'in sorusu)
- **M3**: aynı, 3 x sıkışma mumu
- Bölge sonu (Cemal'in sorusu, BİLGİ): olay bölgesinin SON günü e'den sonraki 20 günde A3 (= B1), A2 (= B1k2), M2, M3 (sıkışma mumu e'deki (a) ölçüsü); eş = e günü, aynı pazar, σ250 ondalığı x likidite üçlüsü (e günündeki hücre), uygun, e'de S5 günü değil. Bölge sonu bilgisi geleceğe aittir: yalnız BİLGİ (Cemal'in sorusu); karar ölçüsü değildir.
- Yön: B1 ilk büyük günün kapanıştan kapanışa getirisinin işareti; BH2 eşiği ilk aşan günde ln(C_t+k/C_t) işareti.
- Zaman: ilk büyük günün t'den uzaklığı k (1..20); pencereler [1,5] [6,10] [11,15] [16,20].
- Eş 1: aynı gün, aynı pazar, σ250 ondalığı x likidite üçlüsü (SY hucA), uygun, S5 günü değil.
- Eş 2: aynı gün, aynı pazar, (pencere ort TR/C_önceki / ATR250) 20'liği x likidite üçlüsü, uygun, S5 günü değil (mekanik düşük oynaklık dengesi).
- olay her eş kümesinde ayrı ayrı en az 3 eşle kalır; bootstrap SY.sy_oran_boot: 2000 tekrar, ay kümeli (olay ayı), %95, tohum 1414 + crc32(etiket) % 1000.
- Tanımlar: {'S5': 'ev5 (iki sınıf birleşik)', 'S5_DIP': 'ev5 VE sınıf DİP', 'S5_YOL': 'ev5 VE sınıf YOL ÜSTÜ'}.
- (C) 60 gün: ORTAK_CETVEL.oc_olc: S5, S5_DIP, S5_YOL olayları ayrı ayrı [sembol, tarih, pazar] (tarih = karar günü t); BİLGİ (yön tahmini yok).
- (C) işlem: SY.sy_olc_C aynen (10 gün bandı %1 taşma kapanışı -> ertesi açılış, stop öteki kenar, 20 bar; eş aynı t momentum beşliği x likidite üçlüsü, S5 dışı; FI_OLCUT dört şart); olay = S5 / S5_DIP / S5_YOL olayı. BİLGİ.
- Dönemler [['2016-22', '2016-01-01', '2022-12-31'], ['2023', '2023-01-01', '2023-12-31'], ['2024-26', '2024-01-01', '2026-08-31']]; karar hücreleri ABD / AVR x 2023 / 2024-26; BIST ve 2016-22 bilgi.
- Hücre kararı: SC ile aynı: KAT alt95 > 1 hem eş 1 hem eş 2'de ve n >= 30 (iki eş kümesinin küçük n'i) -> GEÇER; n < 30 -> ÖLÇÜLEMEDİ; n >= 1000 ve eş 1 ya da eş 2 üst95 < 1 -> TERS; n >= 1000 ve geçmez -> TUTMADI; 30 <= n < 1000 ve geçmez -> ÖLÇÜLEMEDİ (güç).
- Etiket: her tanım (S5, S5_DIP, S5_YOL) ve ana sonuç (B1, BH2) için ayrı: dört karar hücresi (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26) GEÇER -> 'ÖBEK SIKIŞMASI BÜYÜK HAREKET HABERCİSİ'; en az biri GEÇER -> EMARE; hiçbiri geçmez ve dördü TUTMADI / TERS -> 'HABERCİ DEĞİL' (dördü TERS ise '(TERS)'); aksi ÖLÇÜLEMEDİ. k2 / B0 / M2 / M3 / bölge sonu / BIST / 2016-22 bilgi..

## Eşik sözlüğü (SO_ESIK, kararlı JSON)

```json
{
 "C": "SY.sy_olc_C aynen (10 gün bandı %1 taşma kapanışı -> ertesi açılış, stop öteki kenar, 20 bar; eş aynı t momentum beşliği x likidite üçlüsü, S5 dışı; FI_OLCUT dört şart); olay = S5 / S5_DIP / S5_YOL olayı. BİLGİ.",
 "OC": "ORTAK_CETVEL.oc_olc: S5, S5_DIP, S5_YOL olayları ayrı ayrı [sembol, tarih, pazar] (tarih = karar günü t); BİLGİ (yön tahmini yok).",
 "S5": {
  "ara": 20,
  "asagi_acilis_pay": 0.5,
  "atr_gun": 250,
  "bb_dagilim": 250,
  "bb_ddof": 0,
  "bb_gun": 20,
  "bb_k": 2.0,
  "dip_dusus": -0.1,
  "dip_konum": 0.25,
  "egim": [
   -0.02,
   0.1
  ],
  "konum_gun": 120,
  "secilen": {
   "bant": {
    "ABD": 0.06,
    "AVR": 0.06,
    "BIST": 0.08
   },
   "bb": 0.2,
   "k_m": 0.75,
   "p": 15,
   "uzunluk": "p"
  },
  "sma_egim_gun": 20,
  "sma_gun": 50,
  "taban_ilk": 5,
  "taban_pay": 0.99,
  "tanim": {
   "DIP": "konum120 = (C_t - min C t-119..t) / (max - min) <= 0,25 VE C_t / max C t-119..t - 1 <= -%10",
   "YOL": "C_t > SMA50_t VE SMA50_t > SMA50_t-20 VE konum120 >= 0,60 VE min C (pencere) >= min C (pencerenin ilk 5 günü) x 0,99",
   "a": "pencerenin en büyük 1 (H-L)/C değeri çıkarılır; kalan p-1 değerin medyanı <= k_m x ATR250% (t-249..t ort TR/C_önceki)",
   "b": "pencere kapanışlarından en yüksek YA DA en düşük 1 gün (bandı en çok daraltan) çıkarılır; max/min - 1 <= bant",
   "c": "ln C ~ gün doğrusal eğimi (EKK) x p, [-%2, +%10] içinde",
   "d": "pencerede O < önceki geçerli barın C'si olan günlerin payı <= %50",
   "e": "BBW_t = 4 x std20(C, ddof 0) / SMA20(C); pay(BBW_t-250..t-1 <= BBW_t) <= bb",
   "f": "'p': ek şart yok (pencere yeter); '10': (a)&(b)&(e) t'de biten en az 10 ardışık geçerli barda doğru",
   "olay": "S5 günü = (a)..(f) VE (DIP ya da YOL); olay = S5 günü ve önceki 19 barda S5 günü yok (bölge ilk günü = karar günü); bölge sonu = 20 bardan kısa aralarla süren S5 günlerinin sonuncusu; sınıf = karar günü sınıfı"
  },
  "uc_gun_cikar": 1,
  "uzunluk_gun": 10,
  "yol_konum": 0.6,
  "zipla_cikar": 1
 },
 "bilgi_pazar": [
  "BIST"
 ],
 "birlesik": {
  "2023+": [
   "2023",
   "2024-26"
  ]
 },
 "bolunme_gecmis": [
  -260,
  0
 ],
 "bootstrap": "SY.sy_oran_boot: 2000 tekrar, ay kümeli (olay ayı), %95, tohum 1414 + crc32(etiket) % 1000",
 "donem": [
  [
   "2016-22",
   "2016-01-01",
   "2022-12-31"
  ],
  [
   "2023",
   "2023-01-01",
   "2023-12-31"
  ],
  [
   "2024-26",
   "2024-01-01",
   "2026-08-31"
  ]
 ],
 "es": {
  "es1": "aynı gün, aynı pazar, σ250 ondalığı x likidite üçlüsü (SY hucA), uygun, S5 günü değil",
  "es2": "aynı gün, aynı pazar, (pencere ort TR/C_önceki / ATR250) 20'liği x likidite üçlüsü, uygun, S5 günü değil (mekanik düşük oynaklık dengesi)",
  "min_es": 3,
  "olay_secimi": "olay her eş kümesinde ayrı ayrı en az 3 eşle kalır",
  "oran_kova": 20
 },
 "gecmis_min": 290,
 "gelecek_denetimi_n": 40,
 "karar": {
  "etiket": "her tanım (S5, S5_DIP, S5_YOL) ve ana sonuç (B1, BH2) için ayrı: dört karar hücresi (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26) GEÇER -> 'ÖBEK SIKIŞMASI BÜYÜK HAREKET HABERCİSİ'; en az biri GEÇER -> EMARE; hiçbiri geçmez ve dördü TUTMADI / TERS -> 'HABERCİ DEĞİL' (dördü TERS ise '(TERS)'); aksi ÖLÇÜLEMEDİ. k2 / B0 / M2 / M3 / bölge sonu / BIST / 2016-22 bilgi.",
  "hucre": "SC ile aynı: KAT alt95 > 1 hem eş 1 hem eş 2'de ve n >= 30 (iki eş kümesinin küçük n'i) -> GEÇER; n < 30 -> ÖLÇÜLEMEDİ; n >= 1000 ve eş 1 ya da eş 2 üst95 < 1 -> TERS; n >= 1000 ve geçmez -> TUTMADI; 30 <= n < 1000 ve geçmez -> ÖLÇÜLEMEDİ (güç)",
  "n_guc": 1000,
  "n_min": 30
 },
 "karar_donem": [
  "2023",
  "2024-26"
 ],
 "karar_pazar": [
  "ABD",
  "AVR"
 ],
 "liste": {
  "ardisik": 3,
  "bas": "2025-01-01",
  "en_iyi": 10,
  "fiyat": "ekran fiyatı = Yahoo kapanış x sonraki bölünme çarpanı (TAVAN_SERISI.ts_fiyatlar); tespit Yahoo bölünme düzeltmeli oranlarla",
  "pazar": "BIST",
  "rastgele_hisse": 7,
  "sicrama": 0.11,
  "sicrama_tanim": "pencere başı .. bölge sonu + 20 gün içinde tek günde |C/C_önceki - 1| > %11 olan bölge 'bedelli / bölünme şüphesi': en iyi / en kötü 10'a girmez, satırında işaretli",
  "son": "2026-08-31",
  "tohum": 27
 },
 "sonuc": {
  "ana": [
   "B1",
   "BH2"
  ],
  "bilgi": [
   "B1k2",
   "BH2k2",
   "B0",
   "M2",
   "M3"
  ],
  "bolge_sonu": {
   "olcu": [
    "A3",
    "A2",
    "M3",
    "M2"
   ],
   "tanim": "olay bölgesinin SON günü e'den sonraki 20 günde A3 (= B1), A2 (= B1k2), M2, M3 (sıkışma mumu e'deki (a) ölçüsü); eş = e günü, aynı pazar, σ250 ondalığı x likidite üçlüsü (e günündeki hücre), uygun, e'de S5 günü değil. Bölge sonu bilgisi geleceğe aittir: yalnız BİLGİ (Cemal'in sorusu); karar ölçüsü değildir."
  },
  "tanim": {
   "B0": "t+1..t+20 içinde bir günün TR/C_önceki >= 3 x pencere ort TR/C_önceki (göreli; tanımsal, bilgi)",
   "B1": "SC / SY B1 aynen: t+1..t+20 içinde bir günün TR/C_önceki >= 3 x ATR250%",
   "B1k2": "t+1..t+20 içinde bir günün TR/C_önceki >= 2 x ATR250% (yıllık ATR'nin 2 katı)",
   "BH2": "SC BH2 (SY B2) aynen: max_k |ln(C_t+k / C_t)|, k=1..20 >= max(%15, 3 x σ250 x √20)",
   "BH2k2": "max_k |ln(C_t+k / C_t)| >= max(%15, 2 x σ250 x √20)",
   "M2": "t+1..t+20 içinde bir günün (H-L)/C_önceki >= 2 x sıkışma mumu (t'deki (a) ölçüsü: zıplama hariç medyan mum) (Cemal'in sorusu)",
   "M3": "aynı, 3 x sıkışma mumu"
  },
  "yon": {
   "B1": "ilk büyük günün kapanıştan kapanışa getirisinin işareti",
   "BH2": "eşiği ilk aşan günde ln(C_t+k/C_t) işareti"
  },
  "zaman": "ilk büyük günün t'den uzaklığı k (1..20); pencereler [1,5] [6,10] [11,15] [16,20]"
 },
 "tanimlar": {
  "S5": "ev5 (iki sınıf birleşik)",
  "S5_DIP": "ev5 VE sınıf DİP",
  "S5_YOL": "ev5 VE sınıf YOL ÜSTÜ"
 },
 "tohum": 1616,
 "uygun": "SY 'uygun' ile aynı (likidite alt %20 dışı, σ250 / ATR250 / likidite tanımlı, 20 gün gelecek barı var, dönem içinde) + en az 290 geçerli bar + bölünme şüphesi [t-260, t] içinde yok (yalnız geçmiş)"
}
```

## Veri

- V_BIST.pkl sha256: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`
- V_ABD.pkl sha256: `82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e`
- V_AVR.pkl sha256: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2`

## Olay SAYIMI (sonuç / getiri hesaplanmadan; uygun hisse-gün)

| Pazar | Tanım | 2016-22 | 2023 | 2024-26 |
|---|---|---|---|---|
| BIST | S5 | 3358 | 350 | 2002 |
| BIST | S5_DIP | 1613 | 190 | 1345 |
| BIST | S5_YOL | 1745 | 160 | 657 |
| BIST | S1 | 3192 | 326 | 2492 |
| ABD | S5 | 8172 | 1633 | 2900 |
| ABD | S5_DIP | 1432 | 579 | 649 |
| ABD | S5_YOL | 6740 | 1054 | 2251 |
| ABD | S1 | 9004 | 3470 | 2385 |
| AVR | S5 | 4593 | 918 | 1471 |
| AVR | S5_DIP | 802 | 292 | 389 |
| AVR | S5_YOL | 3791 | 626 | 1082 |
| AVR | S1 | 5438 | 1575 | 1263 |

| Pazar | S5 günü payı (2016-22 / 2023 / 2024-26) | koşul payı (a / b / c / d / e / f / a-f / DİP / YOL) | hisse | uygun gün |
|---|---|---|---|---|
| BIST | %4.96 / %1.61 / %4.80 | %40.9 / %30.7 / %37.5 / %96.7 / %20.9 / %100.0 / %8.8 / %25.5 / %26.8 | 581 | 814094 |
| ABD | %3.63 / %3.28 / %1.92 | %41.1 / %34.4 / %50.1 / %64.5 / %21.4 / %100.0 / %5.6 / %22.5 / %28.2 | 1410 | 2293546 |
| AVR | %3.75 / %4.82 / %2.53 | %40.1 / %50.4 / %58.2 / %62.7 / %21.7 / %100.0 / %6.6 / %21.3 / %29.3 | 579 | 1140163 |

## Sınırlar (önceden)
- Evren bugünün listesi: batan / kottan çıkan hisseler yok (hayatta kalma yanlılığı).
- Tanım 7 BIST örneğine göre kaba ızgarada ayarlandı (aşırı uyum riski); ölçüm ABD / AVR ve öteki BIST hisselerinde ileri sınamadır.
- Bilanço takvimi yok: büyük günlerin bir kısmı bilanço günüdür.
- Komisyon, kayma, açığa satış maliyeti yok.
- BIST ölçümü düzeltilmiş fiyatla (V_BIST); liste ve tasarım ekran fiyatıyla da. BIST ±%10 sınırı B1'i kısar (BH2 ikinci ana ölçü).
- Güç sınırlı hücreler (n < 1000) ÖLÇÜLEMEDİ yazılır, 'yok' denmez.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş 1 = aynı gün/pazar σ250 ondalığı x likidite üçlüsü (SY hucA), S5 günü değil; eş 2 = aynı gün (pencere ort TR/C / ATR250) 20'liği x likidite üçlüsü, S5 dışı: sıkışmanın ATR250'yi düşürmesinden gelen mekanik üstünlüğü dengeler; aynı B tanımı eşlere; B0 ve M2/M3 tanımsal göreli (bilgi); bölge sonu ölçüsünde eş e gününde aynı hücreden; 60 gün getiri ve plasebo yalnız OC.oc_olc; işlem eşleri SY.sy_olc_C |
| K2 | geleceğe bakma | EVET | so_s5 yalnız t'ye kadar (ATR250 t-249..t, BBW yüzdeliği t-250..t-1 dağılımı, konum120 / SMA50 t'ye kadar, likidite t-1'e kadar); olay = önceki 19 barda S5 yok (geçmiş); bölge sonu yalnız sonuç tarafında (bilgi); bölünme şüphesi yalnız [t-260, t]; kos'ta so_gelecek_denetimi 40 olay/pazar seriyi t'de kesip aynı tespiti mekanik denetler; test kesme + gelecek bozma |
| K3 | geçerli bar | EVET | SY.sy_veri_hazirla: H>L ve V>0 olmayan bar atılır (bayat fiyat sayılmaz); 'önceki C' önceki GEÇERLİ bar; günlük veri, kesik 31.08.2026 |
| K4 | tekilleştirme | EVET | aynı hissede yeni S5 olayı bölge sonundan en az 20 bar sonra (önceki 19 barda S5 günü yok); n = olay (bölge) sayısı; OC kendi 60 gün tekilleştirmesi; ay kümeli bootstrap; zaman medyan + %25-75 |
| K5 | giriş fiyatı | EVET | KAT olasılık ölçüsü (t kapanışı karar anı); 60 gün getiri OC: giriş t sonrası ilk geçerli açılış; işlem SY (C): kırılım kapanışı sonrası açılış |
| K6 | veri birimi | EVET | ölçüm tek kip: fi_k1_veri düzeltilmiş fiyat (V_*); tasarım ve liste ekran fiyatı ayrı (tespit Yahoo bölünme düzeltmeli oranla); mum ve ATR yüzde; AVR likidite EUR (Kur); bölünme şüphesi SY.sy_bolunme_supheli; liste >%11 tek gün süzgeci (BIST marjı %10) |
| K7 | hayatta kalma | EVET | evren bugünün listesi (V_*.pkl; OC'de ABD + k34): batanlar yok; raporda yazılı; büyük hareket olasılığı olay ve eşte birlikte etkilenir |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem x 3 tanım (S5, DİP, YOL); n < 30 ÖLÇÜLEMEDİ, 30-999 güç sınırlı ÖLÇÜLEMEDİ (HABERCİ DEĞİL yalnız n >= 1000); iki doğrulama dönemi ayrı; ana sonuç 2 (B1, BH2) x 2 eş; k2 / B0 / M / bölge sonu / BIST bilgi; tasarım 7 örneğe göre ayarlandı (aşırı uyum riski yazılı; ızgara kaba ve ön kayıtta) |
| K9 | ön kayıt | EVET | tasarım sınaması (getirisiz) ön kayıttan ÖNCE commit; SO_ESIK sha mühür + SIKISMA_OBEK.py / SIKISMA_CEMAL.py / SIKISMA_YENIDEN.py sha + OC üç satır ön kayıtta; olay sayımı getirisiz; commit + push sonra kos; kos OC.oc_kapi + kendi git / sha kapısı; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV. Ham veriden 3 bölge (7 tasarım örneği dahil) elle doğrulanır |
| K11 | yeniden üretim | EVET | 2 hücre KAT /tmp/sikisma_obek satır CSV'sinden bağımsız kodla yeniden üretilir; 3 bölge ham veriden elle |
| K12 | ifade | EVET | 'HABERCİ / EMARE' yalnız karar kuralı geçince; büyük hareket olasılığı, 60 gün getiri ve işlem getirisi ayrı tablolarda; komisyon yok yazılır |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_so; yasak dosyalara dokunulmaz (git diff denetimi); e-posta taraması ön kayıt + testte; ücretli veri yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; yalnız ölçüm (yön tahmini yok, öneri yok) |
