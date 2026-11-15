# SIKISMA_CEMAL (S4) — ÖN KAYIT

SIKISMA_CEMAL v1.0 (2026-11-15): Cemal tanımlı sıkışma S4 (küçük mum + yatay + dar Bollinger + uzunluk) -> büyük hareket; ileri ölçüm

- MÜHÜR (SC_ESIK sha256): `2533e1f018f26165344e0e25e79e21c924bda5a7bdce2e2a00f7a2f4f9c8178b`
- KOD (SIKISMA_CEMAL.py sha256): `f5c5fd4749dc10b00113bcc8d93224a4d5be990091654dfe963241f9c7561ec8`
- SY_KOD (SIKISMA_YENIDEN.py sha256): `ecc369cd01edacfcf965713dddb18cf9baeacca32a4d3994558c58ebc6cd19ae`
- ZAMAN (UTC): `2026-11-15 08:12:09 UTC`
- Bu dosya ölçümden ÖNCE yazılır ve commit + push edilir; `kos` OC.oc_kapi (kontrol + cetvel sha + git) ve kendi kapısı (mühür, iki kod sha, git'e işlenmiş ve değişmemiş) geçmezse durur.

## Cetvel mühür satırları (ORTAK_CETVEL; aynen)

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`

## Soru
Cemal'in gözüyle tanımlanan sıkışma (küçük mum + yatay + dar Bollinger + en az 10 gün) bitince 20 günde hissenin olağan ölçüsüne göre büyük hareket (B1 tek gün, BH2 çok gün) eşlerden sık mı; ne zaman, hangi yöne. 60 gün getiri ve yönsüz işlem bilgi.

## Tanım (SC_ESIK['S4'])

- (i) ort((H-L)/C, t-p+1..t) <= m_p(s) değerlerinin %20 yüzdeliği, s = t-p-249..t-p (m_p = p günlük ort (H-L)/C; dağılım pencereden önce biter)
- (ii) BBW_t = 2 x 2 x std20(C, ddof 0) / SMA20(C) <= BBW(t-250..t-1) %20 yüzdeliği
- (iii) |C_t / C_t-(p-1) - 1| <= %3 VE (max C - min C) / min C (t-p+1..t) <= bant (BIST %8, ABD/AVR %6) VE pencerede 'aşağı açılış' (O < önceki geçerli barın C'si) günlerinin payı <= %50
- (iv) (i) VE (ii) t'de biten en az 10 ardışık geçerli barda doğru
- S4 = (i)..(iv) hepsi doğru; olay = koşulun doğru olduğu gün, aynı hissede yeni olay en az 20 bar sonra; bölge = t-p+1..t
- p = 20 duyarlılık: aynı eşikler (net %3, bant %8/%6, uzunluk 10) — p'ye göre ölçeklenmez
- Geçmiş: en az 290 geçerli bar. Uygunluk: SY 'uygun' ile aynı (likidite alt %20 dışı, σ250 / ATR250 / likidite tanımlı, 20 gün gelecek barı var, dönem içinde) + en az 290 geçerli bar + bölünme şüphesi [t-260, t] içinde yok (yalnız geçmiş).
- Bölünme şüphesi: SY.sy_bolunme_supheli ANA, pencere [-260, 0] (yalnız geçmiş). SY'nin [-260, +41] penceresiyle aynı ölçüm bilgi satırı (S4_supSY).

## Sonuçlar (SIKISMA_YENIDEN içe alınır)

- **B1**: SY B1 aynen: t+1..t+20 içinde bir günün TR/C_önceki >= 3 x ATR250% (t-249..t)
- **BH2**: SY B2 aynen: max_k |ln(C_t+k / C_t)|, k=1..20 >= max(%15, 3 x σ250 x √20)
- **B1k2**: t+1..t+20 içinde bir günün TR/C_önceki >= 2 x ATR250%
- **BH2k2**: max_k |ln(C_t+k / C_t)| >= max(%15, 2 x σ250 x √20)
- **B0**: t+1..t+20 içinde bir günün TR/C_önceki >= 3 x pencere (t-p+1..t) ort TR/C_önceki (göreli; tanımsal, yalnız bilgi)
- Yön: B1 ilk büyük günün kapanıştan kapanışa getirisinin işareti; BH2 eşiği ilk aşan günde ln(C_t+k/C_t) işareti.
- Zaman: ilk büyük günün t'den uzaklığı k (1..20); pencereler [1,5] [6,10] [11,15] [16,20].
- Eş 1: aynı gün, aynı pazar, σ250 ondalığı x likidite üçlüsü (SY hucA), uygun, S4(p) koşulu yanlış.
- Eş 2: aynı gün, aynı pazar, (ort TR/C_önceki t-p+1..t / ATR250) oranının gün içi 20'liği x likidite üçlüsü, uygun, S4(p) koşulu yanlış (sıkışmanın kendisinden gelen mekanik düşük oynaklığı dengeler).
- olay her eş kümesinde ayrı ayrı en az 3 eşle kalır; bootstrap SY.sy_oran_boot: 2000 tekrar, ay kümeli (olay ayı), %95, tohum 1414 + crc32(etiket) % 1000.
- (C) 60 gün: ORTAK_CETVEL.oc_olc: S4 (p 15) olayları [sembol, tarih, pazar] (tarih = t; giriş, tekilleştirme, eşler, olasılık tablosu cetvelin); BİLGİ (yön tahmini yok).
- (C) işlem: SY.sy_olc_C aynen (10 gün bandı %1 taşma kapanışı -> ertesi açılış, stop öteki kenar, 20 bar; eş aynı t momentum beşliği x likidite üçlüsü, S4 dışı; FI_OLCUT dört şart); yalnız olay = S4 olayı (p 15), eş = S4 koşulu yanlış. BİLGİ.
- Dönemler [['2016-22', '2016-01-01', '2022-12-31'], ['2023', '2023-01-01', '2023-12-31'], ['2024-26', '2024-01-01', '2026-08-31']]; karar hücreleri ABD / AVR x 2023 / 2024-26; BIST ve 2016-22 bilgi.
- Hücre kararı: KAT alt95 > 1 hem eş 1 hem eş 2'de ve n >= 30 (iki eş kümesinin küçük n'i) -> GEÇER; n < 30 -> ÖLÇÜLEMEDİ; n >= 1000 ve eş 1 ya da eş 2 üst95 < 1 -> TERS; n >= 1000 ve geçmez -> TUTMADI; 30 <= n < 1000 ve geçmez -> ÖLÇÜLEMEDİ (güç).
- Etiket: her ana sonuç (B1, BH2) için ayrı, p = 15: dört karar hücresi (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26) GEÇER -> 'CEMAL SIKIŞMASI BÜYÜK HAREKET HABERCİSİ'; en az biri GEÇER -> EMARE; hiçbiri geçmez ve dördü TUTMADI / TERS -> 'HABERCİ DEĞİL' (dördü TERS ise '(TERS)'); aksi ÖLÇÜLEMEDİ. p = 20, k = 2, B0, BIST ve 2016-22 bilgi..

## FENER MEKANİK DOĞRULAMA (tanı; sonuç / getiri ölçmez; eşikler bu kontrolden ÖNCE yazıldı ve oynanmadı)

MEKANİK DOĞRULAMA: S4 (p 15) FENER'de karar günü 14.10-07.11.2025 içinde EN AZ BİR S4 günü (s4c) üretmeli; 03-16.12.2025 içinde S4 günü üretmemeli. Ekran fiyatıyla (Yahoo) ve V_BIST ile. Tutmazsa eşik OYNANMAZ, düşen koşul raporlanır.

**Sonuç: TUTMADI**

| Kaynak | asıl bölge (14.10-07.11.2025) S4 günleri | yanlış bölge (03-16.12.2025) S4 günleri | S1 günleri (asıl / yanlış) | sonuç |
|---|---|---|---|---|
| ekran (Yahoo) | YOK | YOK | 0 / 1 | TUTMADI |
| V_BIST (düzeltilmiş) | YOK | YOK | 0 / 1 | TUTMADI |

- ekran (Yahoo), asıl (14.10-07.11.2025): (i)+(ii)+(iii) aynı gün doğru 4 gün; (i)+(ii) en uzun ardışık 3 gün ((iv) uzunluk DÜŞTÜ: < 10); hiç doğru olmayan koşul: yok.
- ekran (Yahoo), yanlış (03-16.12.2025): (i)+(ii)+(iii) aynı gün doğru 0 gün; (i)+(ii) en uzun ardışık 0 gün ((iv) uzunluk DÜŞTÜ: < 10); hiç doğru olmayan koşul: ii, iii.

- V_BIST (düzeltilmiş), asıl (14.10-07.11.2025): (i)+(ii)+(iii) aynı gün doğru 4 gün; (i)+(ii) en uzun ardışık 3 gün ((iv) uzunluk DÜŞTÜ: < 10); hiç doğru olmayan koşul: yok.
- V_BIST (düzeltilmiş), yanlış (03-16.12.2025): (i)+(ii)+(iii) aynı gün doğru 0 gün; (i)+(ii) en uzun ardışık 0 gün ((iv) uzunluk DÜŞTÜ: < 10); hiç doğru olmayan koşul: ii, iii.

Günlük koşullar — ekran (Yahoo) (i küçük mum, ii dar BB, iii yatay, run = (i)&(ii) ardışık gün):

| bölge | tarih | i | ii | iii | run | mum / q20 | BBW / q20 | BB yüzdelik | net | bant | aşağı açılış payı |
|---|---|---|---|---|---|---|---|---|---|---|---|
| asil | 2025-10-14 | E | - | - | 0 | 3.05 / 3.15 | 39.3 / 12.9 | 0.8 | -22.4 | 28.9 | 0.27 |
| asil | 2025-10-15 | - | - | - | 0 | 3.22 / 3.16 | 38.8 / 12.9 | 0.79 | -16.8 | 24.6 | 0.27 |
| asil | 2025-10-16 | - | - | - | 0 | 3.32 / 3.16 | 37.7 / 12.9 | 0.78 | -14.8 | 23.8 | 0.2 |
| asil | 2025-10-17 | - | - | - | 0 | 3.42 / 3.18 | 34.5 / 12.9 | 0.73 | -12.6 | 20.7 | 0.2 |
| asil | 2025-10-20 | - | - | - | 0 | 3.42 / 3.18 | 32.2 / 12.9 | 0.69 | -13.1 | 19.6 | 0.2 |
| asil | 2025-10-21 | - | - | - | 0 | 3.29 / 3.18 | 30.6 / 12.9 | 0.68 | -12.8 | 19.6 | 0.2 |
| asil | 2025-10-22 | - | - | - | 0 | 3.33 / 3.18 | 27.7 / 12.9 | 0.62 | -11.8 | 19.6 | 0.13 |
| asil | 2025-10-23 | - | - | - | 0 | 3.44 / 3.18 | 25.8 / 12.9 | 0.59 | -10.8 | 16.0 | 0.13 |
| asil | 2025-10-24 | - | - | - | 0 | 3.40 / 3.18 | 23.1 / 12.9 | 0.51 | -2.4 | 9.5 | 0.13 |
| asil | 2025-10-27 | - | - | - | 0 | 3.26 / 3.18 | 20.9 / 12.9 | 0.45 | -3.4 | 8.9 | 0.13 |
| asil | 2025-10-28 | - | - | E | 0 | 3.25 / 3.18 | 19.1 / 12.9 | 0.4 | -1.2 | 6.9 | 0.13 |
| asil | 2025-10-30 | - | - | E | 0 | 3.20 / 3.18 | 16.2 / 12.9 | 0.35 | 0.0 | 6.9 | 0.13 |
| asil | 2025-10-31 | E | E | E | 1 | 3.09 / 3.18 | 11.6 / 12.9 | 0.16 | 0.0 | 6.9 | 0.13 |
| asil | 2025-11-03 | - | E | - | 0 | 3.29 / 3.18 | 7.7 / 12.9 | 0.04 | 3.2 | 7.3 | 0.13 |
| asil | 2025-11-04 | - | E | - | 0 | 3.23 / 3.16 | 6.9 / 12.9 | 0.03 | 6.4 | 7.3 | 0.07 |
| asil | 2025-11-05 | E | E | E | 1 | 2.99 / 3.16 | 6.3 / 12.9 | 0.01 | 2.9 | 4.2 | 0.07 |
| asil | 2025-11-06 | E | E | E | 2 | 2.76 / 3.16 | 6.3 / 12.9 | 0.01 | 0.4 | 4.2 | 0.07 |
| asil | 2025-11-07 | E | E | E | 3 | 2.64 / 3.16 | 6.3 / 12.9 | 0.02 | -1.3 | 4.2 | 0.13 |
| yanlis | 2025-12-03 | - | - | - | 0 | 5.14 / 3.25 | 26.3 / 13.4 | 0.55 | -15.1 | 18.6 | 0.27 |
| yanlis | 2025-12-04 | - | - | - | 0 | 4.85 / 3.25 | 26.4 / 13.4 | 0.56 | -9.7 | 19.9 | 0.27 |
| yanlis | 2025-12-05 | - | - | - | 0 | 4.33 / 3.26 | 25.8 / 13.4 | 0.53 | -12.5 | 19.9 | 0.27 |
| yanlis | 2025-12-08 | - | - | - | 0 | 4.17 / 3.26 | 26.5 / 13.4 | 0.57 | -18.2 | 22.4 | 0.33 |
| yanlis | 2025-12-09 | - | - | - | 0 | 3.86 / 3.26 | 28.4 / 13.4 | 0.62 | -16.6 | 22.4 | 0.33 |
| yanlis | 2025-12-10 | - | - | - | 0 | 3.60 / 3.26 | 30.0 / 13.4 | 0.66 | -16.9 | 22.7 | 0.33 |
| yanlis | 2025-12-11 | - | - | - | 0 | 3.31 / 3.26 | 30.2 / 13.4 | 0.67 | -16.8 | 22.7 | 0.33 |
| yanlis | 2025-12-12 | E | - | - | 0 | 3.19 / 3.26 | 31.3 / 13.4 | 0.7 | -18.2 | 22.7 | 0.33 |
| yanlis | 2025-12-15 | E | - | - | 0 | 3.03 / 3.26 | 31.8 / 13.4 | 0.7 | -17.2 | 20.7 | 0.33 |
| yanlis | 2025-12-16 | E | - | - | 0 | 3.06 / 3.26 | 31.4 / 13.4 | 0.7 | -10.4 | 15.4 | 0.33 |

Günlük koşullar — V_BIST (düzeltilmiş) (i küçük mum, ii dar BB, iii yatay, run = (i)&(ii) ardışık gün):

| bölge | tarih | i | ii | iii | run | mum / q20 | BBW / q20 | BB yüzdelik | net | bant | aşağı açılış payı |
|---|---|---|---|---|---|---|---|---|---|---|---|
| asil | 2025-10-14 | E | - | - | 0 | 3.05 / 3.15 | 39.3 / 12.6 | 0.91 | -22.4 | 28.9 | 0.27 |
| asil | 2025-10-15 | - | - | - | 0 | 3.22 / 3.16 | 38.8 / 12.6 | 0.9 | -16.8 | 24.6 | 0.27 |
| asil | 2025-10-16 | - | - | - | 0 | 3.32 / 3.16 | 37.7 / 12.6 | 0.9 | -14.8 | 23.8 | 0.2 |
| asil | 2025-10-17 | - | - | - | 0 | 3.42 / 3.18 | 34.5 / 12.6 | 0.84 | -12.6 | 20.7 | 0.2 |
| asil | 2025-10-20 | - | - | - | 0 | 3.42 / 3.18 | 32.2 / 12.6 | 0.8 | -13.1 | 19.6 | 0.2 |
| asil | 2025-10-21 | - | - | - | 0 | 3.29 / 3.18 | 30.6 / 12.6 | 0.79 | -12.8 | 19.6 | 0.2 |
| asil | 2025-10-22 | - | - | - | 0 | 3.33 / 3.18 | 27.7 / 12.6 | 0.73 | -11.8 | 19.6 | 0.13 |
| asil | 2025-10-23 | - | - | - | 0 | 3.44 / 3.18 | 25.8 / 12.6 | 0.69 | -10.8 | 16.0 | 0.13 |
| asil | 2025-10-24 | - | - | - | 0 | 3.40 / 3.18 | 23.1 / 12.6 | 0.61 | -2.4 | 9.5 | 0.13 |
| asil | 2025-10-27 | - | - | - | 0 | 3.26 / 3.18 | 20.9 / 12.6 | 0.55 | -3.4 | 8.9 | 0.13 |
| asil | 2025-10-28 | - | - | E | 0 | 3.25 / 3.18 | 19.1 / 12.6 | 0.5 | -1.2 | 6.9 | 0.13 |
| asil | 2025-10-30 | - | - | E | 0 | 3.20 / 3.18 | 16.2 / 12.6 | 0.42 | 0.0 | 6.9 | 0.13 |
| asil | 2025-10-31 | E | E | E | 1 | 3.09 / 3.18 | 11.6 / 12.6 | 0.16 | 0.0 | 6.9 | 0.13 |
| asil | 2025-11-03 | - | E | - | 0 | 3.29 / 3.18 | 7.7 / 12.6 | 0.04 | 3.2 | 7.3 | 0.13 |
| asil | 2025-11-04 | - | E | - | 0 | 3.23 / 3.16 | 6.9 / 12.6 | 0.03 | 6.4 | 7.3 | 0.07 |
| asil | 2025-11-05 | E | E | E | 1 | 2.99 / 3.16 | 6.3 / 12.6 | 0.01 | 2.9 | 4.2 | 0.07 |
| asil | 2025-11-06 | E | E | E | 2 | 2.76 / 3.16 | 6.3 / 12.6 | 0.01 | 0.4 | 4.2 | 0.07 |
| asil | 2025-11-07 | E | E | E | 3 | 2.64 / 3.16 | 6.3 / 12.6 | 0.02 | -1.3 | 4.2 | 0.13 |
| yanlis | 2025-12-03 | - | - | - | 0 | 5.14 / 3.25 | 26.3 / 13.0 | 0.66 | -15.1 | 18.6 | 0.27 |
| yanlis | 2025-12-04 | - | - | - | 0 | 4.85 / 3.25 | 26.4 / 13.0 | 0.66 | -9.7 | 19.9 | 0.27 |
| yanlis | 2025-12-05 | - | - | - | 0 | 4.33 / 3.26 | 25.8 / 13.0 | 0.63 | -12.5 | 19.9 | 0.27 |
| yanlis | 2025-12-08 | - | - | - | 0 | 4.17 / 3.26 | 26.5 / 13.0 | 0.67 | -18.2 | 22.4 | 0.33 |
| yanlis | 2025-12-09 | - | - | - | 0 | 3.86 / 3.26 | 28.4 / 13.0 | 0.72 | -16.6 | 22.4 | 0.33 |
| yanlis | 2025-12-10 | - | - | - | 0 | 3.60 / 3.26 | 30.0 / 13.0 | 0.75 | -16.9 | 22.7 | 0.33 |
| yanlis | 2025-12-11 | - | - | - | 0 | 3.31 / 3.26 | 30.2 / 13.0 | 0.76 | -16.8 | 22.7 | 0.33 |
| yanlis | 2025-12-12 | E | - | - | 0 | 3.19 / 3.26 | 31.3 / 13.0 | 0.79 | -18.2 | 22.7 | 0.33 |
| yanlis | 2025-12-15 | E | - | - | 0 | 3.03 / 3.26 | 31.8 / 13.0 | 0.79 | -17.2 | 20.7 | 0.33 |
| yanlis | 2025-12-16 | E | - | - | 0 | 3.06 / 3.26 | 31.4 / 13.0 | 0.78 | -10.4 | 15.4 | 0.33 |

**Tanı (ölçümden önce yazıldı):** yanlış bölge (03-16.12.2025) doğru biçimde DIŞARIDA ((ii) dar BB ve (iii) yatay hiç doğru değil). Asıl bölgede (14.10-07.11.2025) S4 günü YOK: düşen koşul (iv) uzunluk. (i) küçük mum (15 günlük ortalama) ve (ii) dar Bollinger (20 gün) pencereleri bölgeden önceki düşüşü içerdiği için ancak 31 Ekim'den sonra doğru oluyor; 18 barlık bölgede (i)+(ii) en çok 3-4 gün ardışık. İş tanımı gereği eşik OYNANMADI; ölçüm bu S4 tanımıyla sürer. Sınır: S4, Cemal'in iki bölgesinden yanlışı dışlıyor ama asılı yakalamıyor; kısa (< ~25 bar) sıkışmalar S4'e girmez. Uzunluk koşulunun yeniden tanımı (ör. (iv)'ü bölge içi ölçülerle saymak) Cemal kararıdır ve yeni ön kayıt ister.

## Eşik sözlüğü (SC_ESIK, kararlı JSON)

```json
{
 "C": "SY.sy_olc_C aynen (10 gün bandı %1 taşma kapanışı -> ertesi açılış, stop öteki kenar, 20 bar; eş aynı t momentum beşliği x likidite üçlüsü, S4 dışı; FI_OLCUT dört şart); yalnız olay = S4 olayı (p 15), eş = S4 koşulu yanlış. BİLGİ.",
 "OC": "ORTAK_CETVEL.oc_olc: S4 (p 15) olayları [sembol, tarih, pazar] (tarih = t; giriş, tekilleştirme, eşler, olasılık tablosu cetvelin); BİLGİ (yön tahmini yok).",
 "S4": {
  "ana_pencere": 15,
  "ara": 20,
  "asagi_acilis_pay": 0.5,
  "bant": {
   "ABD": 0.06,
   "AVR": 0.06,
   "BIST": 0.08
  },
  "bb_ddof": 0,
  "bb_gun": 20,
  "bb_k": 2.0,
  "bb_yuzdelik": 0.2,
  "dagilim": 250,
  "mum_yuzdelik": 0.2,
  "net": 0.03,
  "pencere": [
   15,
   20
  ],
  "tanim": {
   "i": "ort((H-L)/C, t-p+1..t) <= m_p(s) değerlerinin %20 yüzdeliği, s = t-p-249..t-p (m_p = p günlük ort (H-L)/C; dağılım pencereden önce biter)",
   "ii": "BBW_t = 2 x 2 x std20(C, ddof 0) / SMA20(C) <= BBW(t-250..t-1) %20 yüzdeliği",
   "iii": "|C_t / C_t-(p-1) - 1| <= %3 VE (max C - min C) / min C (t-p+1..t) <= bant (BIST %8, ABD/AVR %6) VE pencerede 'aşağı açılış' (O < önceki geçerli barın C'si) günlerinin payı <= %50",
   "iv": "(i) VE (ii) t'de biten en az 10 ardışık geçerli barda doğru",
   "olay": "S4 = (i)..(iv) hepsi doğru; olay = koşulun doğru olduğu gün, aynı hissede yeni olay en az 20 bar sonra; bölge = t-p+1..t",
   "p20": "p = 20 duyarlılık: aynı eşikler (net %3, bant %8/%6, uzunluk 10) — p'ye göre ölçeklenmez"
  },
  "uzunluk": 10
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
  "es1": "aynı gün, aynı pazar, σ250 ondalığı x likidite üçlüsü (SY hucA), uygun, S4(p) koşulu yanlış",
  "es2": "aynı gün, aynı pazar, (ort TR/C_önceki t-p+1..t / ATR250) oranının gün içi 20'liği x likidite üçlüsü, uygun, S4(p) koşulu yanlış (sıkışmanın kendisinden gelen mekanik düşük oynaklığı dengeler)",
  "min_es": 3,
  "olay_secimi": "olay her eş kümesinde ayrı ayrı en az 3 eşle kalır",
  "oran_kova": 20
 },
 "fener": {
  "asil": [
   "2025-10-14",
   "2025-11-07"
  ],
  "sembol": "FENER",
  "tanim": "MEKANİK DOĞRULAMA: S4 (p 15) FENER'de karar günü 14.10-07.11.2025 içinde EN AZ BİR S4 günü (s4c) üretmeli; 03-16.12.2025 içinde S4 günü üretmemeli. Ekran fiyatıyla (Yahoo) ve V_BIST ile. Tutmazsa eşik OYNANMAZ, düşen koşul raporlanır.",
  "yanlis": [
   "2025-12-03",
   "2025-12-16"
  ]
 },
 "gecmis_min": 290,
 "gelecek_denetimi_n": 40,
 "karar": {
  "etiket": "her ana sonuç (B1, BH2) için ayrı, p = 15: dört karar hücresi (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26) GEÇER -> 'CEMAL SIKIŞMASI BÜYÜK HAREKET HABERCİSİ'; en az biri GEÇER -> EMARE; hiçbiri geçmez ve dördü TUTMADI / TERS -> 'HABERCİ DEĞİL' (dördü TERS ise '(TERS)'); aksi ÖLÇÜLEMEDİ. p = 20, k = 2, B0, BIST ve 2016-22 bilgi.",
  "hucre": "KAT alt95 > 1 hem eş 1 hem eş 2'de ve n >= 30 (iki eş kümesinin küçük n'i) -> GEÇER; n < 30 -> ÖLÇÜLEMEDİ; n >= 1000 ve eş 1 ya da eş 2 üst95 < 1 -> TERS; n >= 1000 ve geçmez -> TUTMADI; 30 <= n < 1000 ve geçmez -> ÖLÇÜLEMEDİ (güç)",
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
   "B0"
  ],
  "tanim": {
   "B0": "t+1..t+20 içinde bir günün TR/C_önceki >= 3 x pencere (t-p+1..t) ort TR/C_önceki (göreli; tanımsal, yalnız bilgi)",
   "B1": "SY B1 aynen: t+1..t+20 içinde bir günün TR/C_önceki >= 3 x ATR250% (t-249..t)",
   "B1k2": "t+1..t+20 içinde bir günün TR/C_önceki >= 2 x ATR250%",
   "BH2": "SY B2 aynen: max_k |ln(C_t+k / C_t)|, k=1..20 >= max(%15, 3 x σ250 x √20)",
   "BH2k2": "max_k |ln(C_t+k / C_t)| >= max(%15, 2 x σ250 x √20)"
  },
  "yon": {
   "B1": "ilk büyük günün kapanıştan kapanışa getirisinin işareti",
   "BH2": "eşiği ilk aşan günde ln(C_t+k/C_t) işareti"
  },
  "zaman": "ilk büyük günün t'den uzaklığı k (1..20); pencereler [1,5] [6,10] [11,15] [16,20]"
 },
 "sy_bolunme_bilgi": [
  -260,
  41
 ],
 "tohum": 1515,
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
| BIST | S4 | 1585 | 83 | 961 |
| BIST | S4_p20 | 1386 | 42 | 731 |
| BIST | S1 | 3192 | 326 | 2492 |
| ABD | S4 | 3153 | 843 | 787 |
| ABD | S4_p20 | 3217 | 807 | 796 |
| ABD | S1 | 9004 | 3470 | 2385 |
| AVR | S4 | 2078 | 513 | 479 |
| AVR | S4_p20 | 2171 | 524 | 559 |
| AVR | S1 | 5438 | 1575 | 1263 |

| Pazar | S1/S4 olay oranı (2016-22 / 2023 / 2024-26) | S4 olaylarının S1 günü olan payı | S1 olaylarının S4 günü olan payı | S4 gün payı | S1 gün payı | (i) / (ii) / (iii) gün payı | hisse | uygun gün |
|---|---|---|---|---|---|---|---|---|
| BIST | 2.0 / 3.9 / 2.6 | %40.2 / %60.2 / %41.6 | %9.9 / %1.8 / %6.8 | %2.22 / %0.34 / %1.88 | %4.35 / %1.90 / %5.70 | %23.0 / %20.9 / %11.4 | 581 | 814094 |
| ABD | 2.9 / 4.1 / 3.0 | %32.7 / %35.0 / %18.8 | %4.9 / %3.4 / %2.6 | %1.31 / %1.58 / %0.50 | %4.11 / %7.48 / %1.50 | %25.2 / %21.3 / %11.8 | 1410 | 2293546 |
| AVR | 2.6 / 3.1 / 2.6 | %30.9 / %34.3 / %16.1 | %5.8 / %4.8 / %3.7 | %1.63 / %2.41 / %0.81 | %4.68 / %8.67 / %1.86 | %25.8 / %21.6 / %17.4 | 579 | 1140163 |

## Sınırlar (önceden)
- Evren bugünün listesi: batan / kottan çıkan hisseler yok (hayatta kalma yanlılığı).
- Bilanço takvimi yok: büyük günlerin bir kısmı bilanço günüdür.
- Komisyon, kayma, açığa satış maliyeti yok.
- BIST ölçümü düzeltilmiş fiyatla (V_BIST); liste ekran fiyatıyla (Yahoo). BIST ±%10 sınırı B1'i kısar (BH2 bu yüzden ikinci ana ölçü).
- S4 S1'den çok daha seyrektir: güç sınırlı hücreler ÖLÇÜLEMEDİ yazılır, 'yok' denmez.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş 1 = aynı gün/pazar σ250 ondalığı x likidite üçlüsü (SY hucA), S4 dışı; eş 2 = aynı gün (pencere ort TR/C / ATR250) 20'liği x likidite üçlüsü, S4 dışı: sıkışmanın ATR250'yi düşürmesinden gelen mekanik üstünlüğü dengeler; aynı B tanımı eşlere; B0 tanımsal (bilgi); 60 gün getiri ve plasebo yalnız OC.oc_olc; işlem eşleri SY.sy_olc_C (aynı kural) |
| K2 | geleceğe bakma | EVET | sc_gecmis yalnız t'ye kadar (mum dağılımı pencereden önce, BBW dağılımı t-1'e kadar, likidite t-1'e kadar); bölünme şüphesi yalnız [t-260, t]; kos'ta sc_gelecek_denetimi 40 olay/pazar seriyi t'de kesip aynı tespiti mekanik denetler; test kesme + gelecek bozma testi |
| K3 | geçerli bar | EVET | SY.sy_veri_hazirla: H>L ve V>0 olmayan bar atılır (bayat fiyat sayılmaz); 'önceki C' önceki GEÇERLİ bar; günlük veri, kesik 31.08.2026 |
| K4 | tekilleştirme | EVET | aynı hissede S4 olayı en az 20 bar arayla; n = olay sayısı; OC kendi 60 gün tekilleştirmesi; ay kümeli bootstrap; zaman medyan + %25-75 |
| K5 | giriş fiyatı | EVET | KAT olasılık ölçüsü (t kapanışı karar anı); 60 gün getiri OC: giriş t sonrası ilk geçerli açılış; işlem SY (C): kırılım kapanışı sonrası açılış |
| K6 | veri birimi | EVET | ölçüm tek kip: fi_k1_veri düzeltilmiş fiyat (V_*); liste ekran fiyatı ayrı (tespit Yahoo bölünme düzeltmeli oranla); mum ve ATR yüzde; AVR likidite EUR (Kur); bölünme şüphesi SY.sy_bolunme_supheli |
| K7 | hayatta kalma | EVET | evren bugünün listesi (V_*.pkl; OC'de ABD + k34): batanlar yok; raporda yazılı; büyük hareket olasılığı olay ve eşte birlikte etkilenir |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ, 30-999 güç sınırlı ÖLÇÜLEMEDİ (HABERCİ DEĞİL yalnız n >= 1000); iki doğrulama dönemi ayrı; ana sonuç 2 (B1, BH2) x 2 eş; k2 / B0 / p20 / BIST bilgi |
| K9 | ön kayıt | EVET | SC_ESIK sha mühür + SIKISMA_CEMAL.py sha + SIKISMA_YENIDEN.py sha + OC üç satır ön kayıtta; olay sayımı getirisiz; commit + push sonra kos; kos OC.oc_kapi + kendi git / sha kapısı; FENER tanı kontrolü ön kayıtta yazılı, eşik oynanmadı |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV. Ham veriden 3 bölge (FENER Ekim-Kasım dahil) elle doğrulanır |
| K11 | yeniden üretim | EVET | 2 hücre KAT /tmp/sikisma_cemal satır CSV'sinden bağımsız kodla yeniden üretilir; 3 bölge ham veriden elle |
| K12 | ifade | EVET | 'HABERCİ / EMARE' yalnız karar kuralı geçince; büyük hareket olasılığı, 60 gün getiri ve işlem getirisi ayrı tablolarda; komisyon yok yazılır |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_sc; yasak dosyalara dokunulmaz (git diff denetimi); e-posta taraması ön kayıt + testte; ücretli veri yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; yalnız ölçüm (yön tahmini yok, öneri yok) |
