# S7 — BÖLGE İÇİNDEN ÖLÇÜLEN SIKIŞMA KUTUSU: TASARIM SINAMASI VE SAYIM

S7 v1.0 (2026-11-16): bölge içinden ölçülen sıkışma kutusu (Z1-Z6 + DİP / YOL ÜSTÜ; nedensel açılış, geriye uzatma, kırılım / sönme)

Göz aracıdır: getiri / kazanç ölçülmez, iddia yoktur. Pine: COL_S7_BOLGE.pine; Python ikizi: SIKISMA_OBEK.py so_s7_bolgeler.

## ÖN YAZIM (s7tasarim koşmadan ÖNCE yazıldı; bu blok sonradan değişmez)

- ZAMAN (UTC): `2026-11-16 19:05:52 UTC`
- ÖN YAZIM MÜHÜR (so_s7_muhur sha256): `5f9503527288378f3e625cd536d8c47ed252a1a5fb0af281165dbfddaee699c3`
- Varsayılan: k_m 0.75, bb 0.2, Lmin 8, Lmax 80, bant BIST %8 / ABD-AVR %6, eğim [-3%, +8%].
- R (normal gün) = bölge başlangıcı s'den ÖNCEKİ 250 geçerli barın (H-L) / önceki kapanış MEDYANI (bölge ve sonrası girmez).
- Geçerli bar: H > L, V > 0, O > 0, C > 0, sonlu (SY.sy_veri_hazirla; Python'da 31.08.2026 kriz kesiği). İlk 290 geçerli barda (indeks < 290) onay yok; en erken başlangıç s >= 269.
- Kırılım payı %1; bölge bitince (kırılım mumu ya da sönmeyi tetikleyen bar = kilit barı) yeni bölgenin başlangıcı s > kilit (onay e >= kilit + Lmin).
- Z5 bölünmesi: n_son = floor(2L / 5), n_ilk = L - n_son.

### Kural tablosu (KURAL MOTORU, SO7_KURAL / SO7_SINIF)

| şart | eşik | yön | açıkken yeniden sınanır | açıklama |
|---|---|---|---|---|
| Z1 | k_m | <= | EVET | küçük mum: bölgedeki en büyük 1 mum (zıplama) hariç (H-L)/C medyanı <= k_m x R |
| Z2a | z2_zipla_haric | < | EVET | dev mum yok: zıplama hariç en büyük mum (2. büyük) < 2 x R |
| Z2b | z2_hepsi | < | EVET | dev mum yok: zıplama dahil en büyük mum < 3 x R |
| Z3 | bant | <= | hayır | bant: bölge kapanışlarından bandı en çok daraltan 1 uç gün çıkarılır; max/min - 1 <= bant |
| Z4a | egim[0] | >= | hayır | yataylık: ln(C) ~ gün EKK eğimi x L >= eğim alt |
| Z4b | egim[1] | <= | hayır | yataylık: ln(C) ~ gün EKK eğimi x L <= eğim üst |
| Z5 | z5_R | >= | hayır | dip savunması: son floor(2L/5) barın en düşük Low'u >= ilk barların en düşük Low'u x (1 - 0,5 x R) |
| Z6 | bb | <= | EVET | Bollinger: bölgedeki EN DAR BBW (20, 2σ, nüfus std, 4σ/SMA20); s'den önceki 250 BBW içinde payı (<=) <= bb |
| DIP:D1 | dip_konum | <= | hayır (onayda sabit) | konum = (bölge medyan C - min C[s-120..e]) / (max - min) <= 0,30 |
| DIP:D2 | dip_tepe | >= | hayır (onayda sabit) | max C[s-120..s-1] / bölge medyan C - 1 >= %10 |
| YOL:Y1 | - | > | hayır (onayda sabit) | bölge medyan C > SMA50(e) |
| YOL:Y2 | sma_egim_gun | > | hayır (onayda sabit) | SMA50(e) > SMA50(e-20) |
| YOL:Y3 | yol_konum | >= | hayır (onayda sabit) | konum >= 0,60 (Z5 ayrıca bütün bölgelerde şart) |

Bölge = Z1..Z6 VE (DİP ya da YOL ÜSTÜ). Sınıfsız bölge kutu olmaz.

### Algoritma

- BOŞTA: her geçerli bar e'de [e-Lmin+1, e] sınanır. Geçerse bölge AÇILIR; başlangıç s' = s-1 .. max(e-Lmax+1, en erken s, kilit+1) arasında bütün şartları geçen EN ERKEN s' (tamamı taranır). Onay günü = e. Sınıf, R, BBW referansı s'ye göre ve onayda sabit.
- AÇIK: her yeni barda önce kırılım (kapanış > üst x 1,01 YUKARI; < alt x 0,99 AŞAĞI; kırılım mumu bölgeye girmez). Yoksa bar eklenir, Z1, Z2, Z6 yeniden sınanır; bozulursa bölge son geçerli günde 'sönme' ile biter. Üst / alt = Z3'teki 1 uç gün hariç bant (her eklemede yeniden). Lmax aşılırsa bölge sürer, başlangıç sabit.
- Bölge bitince yeni bölge için bitiş barından (kırılım mumu / sönmeyi tetikleyen bar) SONRA en az Lmin yeni bar gerekir.

### Izgara ve seçim (ölçümden önce)

- Izgara: k_m [0.65, 0.75, 0.85] x bb [0.15, 0.2, 0.25] x Lmin [8, 10] x bant BIST [0.08, 0.1] x eğim [[-0.03, 0.08], [-0.02, 0.06]] = 72 nokta. bant ızgarası BIST değeriyle seçilir; ABD / AVR eşi S5 ızgarasındaki gibi (BIST %8 -> %6, BIST %10 -> %8).
- Seçim kuralı: (1) 8 sınamanın (3 seçmeli + 5 seçmemeli, V_BIST) hepsini tutan noktalar. (2) Aralarından varsayılana (k_m 0,75, bb 0,20, Lmin 8, bant BIST %8, eğim [-%3, +%8]) en az farklı parametre sayısı. (3) Eşitlikte SIKI olan: sıra anahtarı (k_m küçük, bb küçük, Lmin büyük, bant dar, eğim aralığı dar). (4) Hiçbir nokta 8/8 değilse en çok tutanlar arasında (2)-(3); kaçanlar açıkça yazılır. Eşik bu sonuçtan sonra OYNANMAZ.
- Örnek kuralı: SEÇMELİ tutar: örnek aralığıyla (geçerli bar) kesişimi en büyük S7 bölgesi [s, bitiş] (eşitlikte erken olan) için kesişim / örnek uzunluğu >= 0,5 VE sınıfı beklenen. Başlangıç farkı = s - örnek ilk barı, bitiş farkı = bitiş - örnek son barı (geçerli bar). SEÇMEMELİ tutar: [örnek ilk - 5 geçerli bar, örnek son + 5 geçerli bar] ile kesişen hiçbir S7 bölgesi [s, bitiş] yok. Fiyat V_BIST (düzeltilmiş).

| örnek | hisse | aralık | tür | beklenen sınıf |
|---|---|---|---|---|
| FENER-E | FENER | 2025-10-14 .. 2025-11-07 | SEÇMELİ | DIP |
| CCOLA-E | CCOLA | 2025-10-02 .. 2025-10-20 | SEÇMELİ | DIP |
| ENJSA-T | ENJSA | 2025-07-28 .. 2025-08-15 | SEÇMELİ | YOL |
| FENER-A | FENER | 2025-12-03 .. 2025-12-16 | SEÇMEMELİ (±5 bar) | - |
| CCOLA-T | CCOLA | 2025-07-29 .. 2025-08-29 | SEÇMEMELİ (±5 bar) | - |
| ENJSA-O | ENJSA | 2025-01-20 .. 2025-02-14 | SEÇMEMELİ (±5 bar) | - |
| ENJSA-A | ENJSA | 2025-12-30 .. 2026-01-27 | SEÇMEMELİ (±5 bar) | - |
| ENJSA-V | ENJSA | 2026-07-06 .. 2026-07-17 | SEÇMEMELİ (±5 bar) | - |

- Örnek sayısı 3 + 5: aşırı uyum riski yüksek; sonuç 'bulgu' değildir, Cemal'in gözüyle sınanır.
- Bilgi (karar yok): kalibre_etiketler.csv (çöl + olumsuz etiketler; uzun çöller, farklı ölçek) her etikette S7 örtüşmesi.
- Sayım (seçilen noktayla, getiri YOK): BIST / ABD / AVR; 100 hisse-yılda bölge, uzunluk medyan / çeyrek, sınıf ve bitiş türü payı, 1-4 günlük bölge payı; S5 kutuları (N = 1) ve S6 varsayılanı aynı evrende yan yana.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | getiri / sonuç ölçülmüyor; yalnız bölge sayımı ve 8 örnekte göz sınaması; kıyas S5 / S6 kutularıyla aynı evren ve aynı geçerli bar |
| K2 | geleceğe bakma | EVET | so_s7_bolgeler nedensel: e'de yalnız [s, e] ve s öncesi 250 bar (R, BBW payı), sınıf [s-120, e], SMA50(e), SMA50(e-20); geriye uzatma yalnız e'ye kadarki barlarla; test_sikisma_obek.py önek değişmezliği (3 hisse x 5 kesim: s, e, sınıf, R aynı) mekanik |
| K3 | geçerli bar | EVET | SY.sy_veri_hazirla: H>L, V>0, O>0, C>0, sonlu olmayan bar atılır; bütün pencereler geçerli bar sayar; Pine'da aynı 'gecerli' süzgeci |
| K4 | tekilleştirme | UYGULANMAZ | getiri yok; bölge tekilleştirmesi tanımda (kilit: yeni bölge s > önceki bölgenin bitiş / kırılım barı) |
| K5 | giriş fiyatı | UYGULANMAZ | getiri / giriş fiyatı yok; kutuda kazanç etiketi YOK |
| K6 | veri birimi | EVET | tek fiyat kipi V_BIST / V_ABD / V_AVR düzeltilmiş (fi_k1_veri); mum ve R yüzde (oran); BIST bölünme sıçraması bir kapanışla bandı kırar ya da Z2 (3 x R) ile bölge açılmaz; Pine'da TradingView fiyatı (kuruş farkı yazılı) |
| K7 | hayatta kalma | EVET | evren bugünün listesi (V_*.pkl): batan / kottan çıkan hisse yok; sayım tablosunda ve raporda yazılı |
| K8 | örneklem ve dönem | EVET | tasarım 3 seçmeli + 5 seçmemeli örnekle (aşırı uyum riski yazılı; 'bulgu' denmez); sayım üç pazar, bütün dönem, betimsel |
| K9 | ön kayıt | EVET | bu ön yazım (ızgara + seçim kuralı + örnek kuralı + eşikler, mühür sha256 + UTC zaman) s7tasarim koşmadan ÖNCE yazıldı; s7tasarim mührü yeniden hesaplar, tutmazsa durur; commit ana modelde |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber ayrıştırma yok; yalnız OHLCV |
| K11 | yeniden üretim | EVET | en az 2 sayı bağımsız kodla (rapor dışı betik, ayrı hesap) yeniden üretilir: bir örnek bölgesinin Z ölçüleri ve BIST bölge sayısı |
| K12 | ifade | EVET | göz aracı; 'iz / emare' sözü yok, getiri / kazanç iddiası yok; Pine'da getiri etiketi yok |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_so korunur (S7 adları önekli, öteki modüllerle ad kesişimi testte); yasak dosyalara dokunulmaz; e-posta / anahtar taraması testte; ağdan veri yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; gösterge aday gösterir |

<!-- S7_ON_YAZIM_SONU -->

**SAPMA NOTU (yalnız dosya taşıma, mantık aynı; 16 Kas 2026, ana model denetimi):** ön yazımda 'Python ikizi: SIKISMA_OBEK.py so_s7_bolgeler' yazar; S7 kodu S5 ön kaydının KOD sha kapısını bozmamak için SIKISMA_S7.py dosyasına taşındı (SIKISMA_OBEK.py HEAD ile bayt bayt aynı). Komutlar `python SIKISMA_S7.py s7tasarim | s7sayim | s7pine | s7md`. Eşik, ızgara, kural ve örnekler aynı: ön yazım mührü (so_s7_muhur) yeniden hesaplandı ve tuttu; tasarım ve sayım yeni modülle yeniden koşuldu, sayılar taşımadan önceki koşuyla birebir aynı.

## TASARIM SONUCU (ön yazımdan sonra koşuldu; V_BIST)

- Koşu (UTC): `2026-11-16 19:24:32 UTC`; ön yazım zamanı `2026-11-16 19:05:52 UTC`.
- En çok tutan 7 / 8; 8/8 tutan nokta 0 / 72; en çok tutan nokta 8.
- **SEÇİLEN:** k_m 0.75, bb 0.15, Lmin 8, bant BIST %8 / ABD-AVR %6, eğim [-3%, +8%]. Kaçan: CCOLA-E.
- Varsayılan noktada tutan 6 / 8.

| örnek | tür | sonuç | bulunan bölge (başlangıç .. bitiş, onay) | sınıf | örtüşme | başlangıç farkı (bar) | bitiş farkı (bar) |
|---|---|---|---|---|---|---|---|
| FENER-E 2025-10-14..2025-11-07 | SEÇ DIP | TUTTU | 2025-10-22 .. 2025-11-10 (onay 2025-11-03, YUKARI) | DIP | %67 | 6 | 1 |
| CCOLA-E 2025-10-02..2025-10-20 | SEÇ DIP | KAÇTI | 2025-09-08 .. 2025-10-02 (onay 2025-10-02, sönme) | DIP | %8 | -18 | -12 |
| ENJSA-T 2025-07-28..2025-08-15 | SEÇ YOL | TUTTU | 2025-07-16 .. 2025-08-12 (onay 2025-08-07, YUKARI) | YOL | %80 | -8 | -3 |
| FENER-A 2025-12-03..2025-12-16 | SEÇME (±5) | TUTTU | tampondaki bölge: yok | - | - | - | - |
| CCOLA-T 2025-07-29..2025-08-29 | SEÇME (±5) | TUTTU | tampondaki bölge: yok | - | - | - | - |
| ENJSA-O 2025-01-20..2025-02-14 | SEÇME (±5) | TUTTU | tampondaki bölge: yok | - | - | - | - |
| ENJSA-A 2025-12-30..2026-01-27 | SEÇME (±5) | TUTTU | tampondaki bölge: yok | - | - | - | - |
| ENJSA-V 2026-07-06..2026-07-17 | SEÇME (±5) | TUTTU | tampondaki bölge: yok | - | - | - | - |

### Bütün ızgara (tutan / 8, varsayılandan fark, kaçanlar)

| k_m | bb | Lmin | bant BIST | eğim | tutan | fark | kaçan |
|---|---|---|---|---|---|---|---|
| 0.65 | 0.15 | 8 | 0.08 | [-0.03, +0.08] | 6 | 2 | CCOLA-E, ENJSA-T |
| 0.65 | 0.15 | 8 | 0.08 | [-0.02, +0.06] | 6 | 3 | CCOLA-E, ENJSA-T |
| 0.65 | 0.15 | 8 | 0.10 | [-0.03, +0.08] | 6 | 3 | CCOLA-E, ENJSA-T |
| 0.65 | 0.15 | 8 | 0.10 | [-0.02, +0.06] | 6 | 4 | CCOLA-E, ENJSA-T |
| 0.65 | 0.15 | 10 | 0.08 | [-0.03, +0.08] | 6 | 3 | CCOLA-E, ENJSA-T |
| 0.65 | 0.15 | 10 | 0.08 | [-0.02, +0.06] | 6 | 4 | CCOLA-E, ENJSA-T |
| 0.65 | 0.15 | 10 | 0.10 | [-0.03, +0.08] | 6 | 4 | CCOLA-E, ENJSA-T |
| 0.65 | 0.15 | 10 | 0.10 | [-0.02, +0.06] | 6 | 5 | CCOLA-E, ENJSA-T |
| 0.65 | 0.2 | 8 | 0.08 | [-0.03, +0.08] | 6 | 1 | CCOLA-E, ENJSA-T |
| 0.65 | 0.2 | 8 | 0.08 | [-0.02, +0.06] | 6 | 2 | CCOLA-E, ENJSA-T |
| 0.65 | 0.2 | 8 | 0.10 | [-0.03, +0.08] | 6 | 2 | CCOLA-E, ENJSA-T |
| 0.65 | 0.2 | 8 | 0.10 | [-0.02, +0.06] | 6 | 3 | CCOLA-E, ENJSA-T |
| 0.65 | 0.2 | 10 | 0.08 | [-0.03, +0.08] | 6 | 2 | CCOLA-E, ENJSA-T |
| 0.65 | 0.2 | 10 | 0.08 | [-0.02, +0.06] | 6 | 3 | CCOLA-E, ENJSA-T |
| 0.65 | 0.2 | 10 | 0.10 | [-0.03, +0.08] | 6 | 3 | CCOLA-E, ENJSA-T |
| 0.65 | 0.2 | 10 | 0.10 | [-0.02, +0.06] | 6 | 4 | CCOLA-E, ENJSA-T |
| 0.65 | 0.25 | 8 | 0.08 | [-0.03, +0.08] | 6 | 2 | CCOLA-E, ENJSA-T |
| 0.65 | 0.25 | 8 | 0.08 | [-0.02, +0.06] | 6 | 3 | CCOLA-E, ENJSA-T |
| 0.65 | 0.25 | 8 | 0.10 | [-0.03, +0.08] | 6 | 3 | CCOLA-E, ENJSA-T |
| 0.65 | 0.25 | 8 | 0.10 | [-0.02, +0.06] | 6 | 4 | CCOLA-E, ENJSA-T |
| 0.65 | 0.25 | 10 | 0.08 | [-0.03, +0.08] | 6 | 3 | CCOLA-E, ENJSA-T |
| 0.65 | 0.25 | 10 | 0.08 | [-0.02, +0.06] | 6 | 4 | CCOLA-E, ENJSA-T |
| 0.65 | 0.25 | 10 | 0.10 | [-0.03, +0.08] | 6 | 4 | CCOLA-E, ENJSA-T |
| 0.65 | 0.25 | 10 | 0.10 | [-0.02, +0.06] | 6 | 5 | CCOLA-E, ENJSA-T |
| 0.75 | 0.15 | 8 | 0.08 | [-0.03, +0.08] | 7 | 1 | CCOLA-E |
| 0.75 | 0.15 | 8 | 0.08 | [-0.02, +0.06] | 7 | 2 | CCOLA-E |
| 0.75 | 0.15 | 8 | 0.10 | [-0.03, +0.08] | 7 | 2 | CCOLA-E |
| 0.75 | 0.15 | 8 | 0.10 | [-0.02, +0.06] | 7 | 3 | CCOLA-E |
| 0.75 | 0.15 | 10 | 0.08 | [-0.03, +0.08] | 7 | 2 | CCOLA-E |
| 0.75 | 0.15 | 10 | 0.08 | [-0.02, +0.06] | 7 | 3 | CCOLA-E |
| 0.75 | 0.15 | 10 | 0.10 | [-0.03, +0.08] | 7 | 3 | CCOLA-E |
| 0.75 | 0.15 | 10 | 0.10 | [-0.02, +0.06] | 7 | 4 | CCOLA-E |
| 0.75 | 0.2 | 8 | 0.08 | [-0.03, +0.08] | 6 | 0 | FENER-E, CCOLA-E |
| 0.75 | 0.2 | 8 | 0.08 | [-0.02, +0.06] | 6 | 1 | FENER-E, CCOLA-E |
| 0.75 | 0.2 | 8 | 0.10 | [-0.03, +0.08] | 6 | 1 | FENER-E, CCOLA-E |
| 0.75 | 0.2 | 8 | 0.10 | [-0.02, +0.06] | 6 | 2 | FENER-E, CCOLA-E |
| 0.75 | 0.2 | 10 | 0.08 | [-0.03, +0.08] | 6 | 1 | CCOLA-E, CCOLA-T |
| 0.75 | 0.2 | 10 | 0.08 | [-0.02, +0.06] | 6 | 2 | CCOLA-E, CCOLA-T |
| 0.75 | 0.2 | 10 | 0.10 | [-0.03, +0.08] | 6 | 2 | CCOLA-E, CCOLA-T |
| 0.75 | 0.2 | 10 | 0.10 | [-0.02, +0.06] | 6 | 3 | CCOLA-E, CCOLA-T |
| 0.75 | 0.25 | 8 | 0.08 | [-0.03, +0.08] | 6 | 1 | FENER-E, CCOLA-E |
| 0.75 | 0.25 | 8 | 0.08 | [-0.02, +0.06] | 6 | 2 | FENER-E, CCOLA-E |
| 0.75 | 0.25 | 8 | 0.10 | [-0.03, +0.08] | 6 | 2 | FENER-E, CCOLA-E |
| 0.75 | 0.25 | 8 | 0.10 | [-0.02, +0.06] | 6 | 3 | FENER-E, CCOLA-E |
| 0.75 | 0.25 | 10 | 0.08 | [-0.03, +0.08] | 6 | 2 | CCOLA-E, CCOLA-T |
| 0.75 | 0.25 | 10 | 0.08 | [-0.02, +0.06] | 6 | 3 | CCOLA-E, CCOLA-T |
| 0.75 | 0.25 | 10 | 0.10 | [-0.03, +0.08] | 6 | 3 | CCOLA-E, CCOLA-T |
| 0.75 | 0.25 | 10 | 0.10 | [-0.02, +0.06] | 6 | 4 | CCOLA-E, CCOLA-T |
| 0.85 | 0.15 | 8 | 0.08 | [-0.03, +0.08] | 5 | 2 | FENER-A, CCOLA-T, ENJSA-V |
| 0.85 | 0.15 | 8 | 0.08 | [-0.02, +0.06] | 5 | 3 | FENER-A, CCOLA-T, ENJSA-V |
| 0.85 | 0.15 | 8 | 0.10 | [-0.03, +0.08] | 5 | 3 | FENER-A, CCOLA-T, ENJSA-V |
| 0.85 | 0.15 | 8 | 0.10 | [-0.02, +0.06] | 5 | 4 | FENER-A, CCOLA-T, ENJSA-V |
| 0.85 | 0.15 | 10 | 0.08 | [-0.03, +0.08] | 5 | 3 | FENER-A, CCOLA-T, ENJSA-V |
| 0.85 | 0.15 | 10 | 0.08 | [-0.02, +0.06] | 5 | 4 | FENER-A, CCOLA-T, ENJSA-V |
| 0.85 | 0.15 | 10 | 0.10 | [-0.03, +0.08] | 5 | 4 | FENER-A, CCOLA-T, ENJSA-V |
| 0.85 | 0.15 | 10 | 0.10 | [-0.02, +0.06] | 5 | 5 | FENER-A, CCOLA-T, ENJSA-V |
| 0.85 | 0.2 | 8 | 0.08 | [-0.03, +0.08] | 4 | 1 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.2 | 8 | 0.08 | [-0.02, +0.06] | 4 | 2 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.2 | 8 | 0.10 | [-0.03, +0.08] | 4 | 2 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.2 | 8 | 0.10 | [-0.02, +0.06] | 4 | 3 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.2 | 10 | 0.08 | [-0.03, +0.08] | 4 | 2 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.2 | 10 | 0.08 | [-0.02, +0.06] | 4 | 3 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.2 | 10 | 0.10 | [-0.03, +0.08] | 4 | 3 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.2 | 10 | 0.10 | [-0.02, +0.06] | 4 | 4 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.25 | 8 | 0.08 | [-0.03, +0.08] | 4 | 2 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.25 | 8 | 0.08 | [-0.02, +0.06] | 4 | 3 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.25 | 8 | 0.10 | [-0.03, +0.08] | 4 | 3 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.25 | 8 | 0.10 | [-0.02, +0.06] | 4 | 4 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.25 | 10 | 0.08 | [-0.03, +0.08] | 4 | 3 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.25 | 10 | 0.08 | [-0.02, +0.06] | 4 | 4 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.25 | 10 | 0.10 | [-0.03, +0.08] | 4 | 4 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |
| 0.85 | 0.25 | 10 | 0.10 | [-0.02, +0.06] | 4 | 5 | FENER-A, CCOLA-T, ENJSA-A, ENJSA-V |

Not: 3 + 5 örnek; aşırı uyum riski yüksek. Seçilen nokta Cemal'in gözüyle (TradingView) ileri sınanır; eşik bu sonuçtan sonra oynanmaz.

## BİLGİ: kalibre_etiketler.csv (karar yok; uzun çöller, farklı ölçek)

| hisse | aralık | etiket | durum | bar | S7 bölgesi | kapsama | en iyi örtüşme | sınıflar | bölgeler |
|---|---|---|---|---|---|---|---|---|---|
| TEHOL | 2024-10-07..2024-12-12 | COL | ok | 48 | 2 | %44 | %23 | DIP | 2024-10-31..2024-11-14 DIP YUKARI; 2024-11-22..2024-12-05 DIP YUKARI |
| TEHOL | 2026-02-03..2026-04-03 | COL | ok | 43 | 2 | %65 | %33 | DIP | 2026-01-23..2026-02-20 DIP YUKARI; 2026-03-16..2026-04-03 DIP YUKARI |
| INVES | 2025-05-08..2025-06-20 | COL | ok | 29 | 0 | %0 | %0 | - | - |
| BURVA | 2025-06-26..2025-07-21 | COL | ok | 17 | 2 | %88 | %53 | DIP | 2025-06-27..2025-07-09 DIP YUKARI; 2025-07-11..2025-07-23 DIP YUKARI |
| EYGYO | 2025-05-28..2025-07-10 | COL | ok | 30 | 0 | %0 | %0 | - | - |
| BASCM | 2025-03-02..2025-07-01 | COL | ok | 76 | 1 | %9 | %9 | DIP | 2025-06-23..2025-07-02 DIP YUKARI |
| SEYKM | 2025-04-15..2025-07-16 | COL | ok | 61 | 2 | %57 | %44 | DIP | 2025-04-11..2025-05-26 DIP AŞAĞI; 2025-05-28..2025-06-10 DIP YUKARI |
| GEDZA | 2024-10-15..2024-12-02 | COL | ok | 34 | 2 | %88 | %59 | DIP | 2024-10-17..2024-11-14 DIP YUKARI; 2024-11-18..2024-11-29 DIP sönme |
| SUNTK | 2024-08-27..2024-11-11 | COL | ok | 53 | 0 | %0 | %0 | - | - |
| HDFGS | 2025-04-22..2025-06-12 | COL | ok | 33 | 0 | %0 | %0 | - | - |
| INFO | 2025-03-26..2025-05-20 | COL | ok | 35 | 0 | %0 | %0 | - | - |
| KATMR | 2025-04-16..2025-07-16 | COL | ok | 60 | 0 | %0 | %0 | - | - |
| OTTO | 2024-07-02..2024-09-12 | COL | ok | 43 | 1 | %56 | %56 | DIP | 2024-07-31..2024-09-12 DIP YUKARI |
| TUKAS | 2024-10-02..2024-12-02 | COL | ok | 43 | 3 | %88 | %47 | DIP | 2024-10-03..2024-10-31 DIP YUKARI; 2024-11-06..2024-11-19 DIP AŞAĞI; 2024-11-21..2024-12-04 DIP YUKARI |
| ORCAY | 2024-10-05..2024-11-18 | COL | ok | 30 | 2 | %93 | %67 | DIP | 2024-10-07..2024-11-04 DIP AŞAĞI; 2024-11-06..2024-11-15 DIP YUKARI |
| TATGD | 2024-05-30..2024-07-15 | COL | ok | 29 | 3 | %86 | %34 | DIP | 2024-05-27..2024-06-06 DIP AŞAĞI; 2024-06-10..2024-06-26 DIP YUKARI; 2024-06-28..2024-07-10 DIP YUKARI |
| TATGD | 2024-08-05..2024-11-04 | COL | ok | 64 | 1 | %22 | %22 | DIP | 2024-08-21..2024-09-10 DIP AŞAĞI |
| EUREN | 2025-10-01..2025-11-03 | COL | ok | 23 | 0 | %0 | %0 | - | - |
| VRGYO | 2025-08-14..2025-09-22 | COL | ok | 28 | 0 | %0 | %0 | - | - |
| VESTL | 2024-11-05..2024-12-02 | COL | ok | 20 | 1 | %45 | %45 | DIP | 2024-11-05..2024-11-15 DIP YUKARI |
| VESTL | 2025-06-02..2025-08-11 | COL | ok | 48 | 1 | %19 | %19 | DIP | 2025-07-30..2025-08-20 DIP YUKARI |
| ARZUM | 2024-08-06..2024-09-23 | COL | ok | 34 | 2 | %47 | %24 | DIP | 2024-08-26..2024-09-05 DIP YUKARI; 2024-09-09..2024-09-18 DIP YUKARI |
| EMNIS | 2025-04-14..2025-05-19 | COL | ok | 22 | 1 | %36 | %36 | YOL | 2025-05-07..2025-05-28 YOL sönme |
| SKTAS | 2024-07-10..2024-08-11 | COL | ok | 22 | 0 | %0 | %0 | - | - |
| SMRTG | 2024-11-21..2024-12-29 | COL | ok | 27 | 2 | %96 | %74 | DIP | 2024-11-13..2024-11-28 DIP sönme; 2024-12-02..2024-12-31 DIP YUKARI |
| ODAS | 2024-06-06..2024-07-15 | COL | ok | 24 | 1 | %21 | %21 | DIP | 2024-07-08..2024-07-30 DIP AŞAĞI |
| BINBN | 2026-02-25..2026-04-15 | COL | ok | 35 | 1 | %40 | %40 | DIP | 2026-03-27..2026-04-16 DIP YUKARI |
| BINBN | 2024-12-17..2025-01-21 | COL | ok | 25 | 0 | %0 | %0 | - | - |
| ESCAR | 2025-09-19..2025-12-11 | COL | ok | 59 | 2 | %51 | %29 | DIP | 2025-09-16..2025-10-13 DIP AŞAĞI; 2025-10-20..2025-11-06 DIP AŞAĞI |
| PEKER | 2025-02-27..2025-06-10 | COL | veri yok | - | - | - | - | - | - |
| PAPIL | 2025-11-12..2025-12-09 | OLUMSUZ | ok | 20 | 1 | %100 | %100 | DIP | 2025-11-11..2025-12-10 DIP YUKARI |
| GEDIK | 2025-09-15..2025-10-31 | OLUMSUZ | ok | 34 | 0 | %0 | %0 | - | - |
| SEYKM | 2026-03-08..2026-04-27 | OLUMSUZ | ok | 34 | 1 | %26 | %26 | DIP | 2026-04-06..2026-04-16 DIP YUKARI |
| ALTNY | 2025-10-23..2026-01-08 | OLUMSUZ | ok | 54 | 2 | %52 | %33 | DIP | 2025-11-07..2025-12-02 DIP sönme; 2025-12-04..2025-12-17 DIP YUKARI |
| TUREX | 2026-03-30..2026-08-24 | OLUMSUZ | ok | 99 | 0 | %0 | %0 | - | - |
| SDTTR | 2024-03-28..2024-05-07 | OLUMSUZ | ok | 23 | 0 | %0 | %0 | - | - |
| GARFA | 2026-07-31..2026-09-14 | OLUMSUZ | ok | 22 | 1 | %100 | %100 | DIP | 2026-07-24..2026-08-31 DIP AÇIK |
| ERCB | 2025-06-13..2025-11-14 | OLUMSUZ | ok | 109 | 0 | %0 | %0 | - | - |

- COL: 29 etiket; en az bir S7 bölgesi olan 19; kapsama medyanı %36.

- OLUMSUZ: 8 etiket; en az bir S7 bölgesi olan 4; kapsama medyanı %13.

## SAYIM (seçilen nokta; getiri YOK; evren bugünün listesi, 31.08.2026 kesiği, likidite süzgeci yok)

- Koşu (UTC): `2026-11-16 19:24:35 UTC`; süre 115.2 sn.
- S5 kutusu = COL_S6_TASLAK.pine 'S5 (ölçüm)' ön ayarı (N = 1; Cemal'in grafikte gördüğü S5 kutuları). S5 ölçüm bölgesi = so_s5 ev5 .. bölge sonu (20 bar birleştirme; ölçümde kullanılan). S6 = taslak varsayılanı (N = 5). Uzunluk = bölgenin geçerli bar sayısı (kırılım mumu hariç).

| pazar | tanım | hisse | hisse-yıl | bölge | 100 hisse-yılda | uzunluk medyan [Ç1-Ç3] | 1-4 günlük payı | 1 günlük | DİP / YOL | YUKARI / AŞAĞI / sönme / AÇIK |
|---|---|---|---|---|---|---|---|---|---|---|
| BIST | S5 kutusu (N=1) | 581 | 4102 | 20807 | 507.2 | 1 [1-2] | %95 | %62 | %66 / %34 | %45 / %42 / %13 / %0 |
| BIST | S5 ölçüm bölgesi | 581 | 4102 | 7443 | 181.4 | 6 [2-14] | %44 | %19 | %59 / %41 | - |
| BIST | S6 varsayılan | 581 | 4102 | 1646 | 40.1 | 5 [5-7] | %0 | %0 | %70 / %30 | %44 / %30 / %25 / %1 |
| BIST | S7 | 581 | 4102 | 10597 | 258.3 | 12 [9-17] | %0 | %0 | %69 / %31 | %50 / %32 / %18 / %0 |
| ABD | S5 kutusu (N=1) | 1410 | 11674 | 34225 | 293.2 | 1 [1-2] | %93 | %59 | %21 / %79 | %38 / %36 / %25 / %0 |
| ABD | S5 ölçüm bölgesi | 1410 | 11674 | 15034 | 128.8 | 4 [2-12] | %50 | %22 | %23 / %77 | - |
| ABD | S6 varsayılan | 1410 | 11674 | 2860 | 24.5 | 6 [5-7] | %0 | %0 | %12 / %88 | %34 / %27 / %39 / %0 |
| ABD | S7 | 1410 | 11674 | 24466 | 209.6 | 11 [9-17] | %0 | %0 | %27 / %73 | %40 / %28 / %31 / %0 |
| AVR | S5 kutusu (N=1) | 579 | 5725 | 19748 | 344.9 | 1 [1-3] | %91 | %54 | %19 / %81 | %35 / %33 / %31 / %0 |
| AVR | S5 ölçüm bölgesi | 579 | 5725 | 8564 | 149.6 | 5 [2-12] | %48 | %22 | %21 / %79 | - |
| AVR | S6 varsayılan | 579 | 5725 | 1738 | 30.4 | 6 [5-7] | %0 | %0 | %12 / %88 | %33 / %25 / %42 / %0 |
| AVR | S7 | 579 | 5725 | 12658 | 221.1 | 12 [9-20] | %0 | %0 | %21 / %79 | %37 / %24 / %39 / %0 |

| pazar | S7 onay öncesi uzunluk medyanı (s..e) | onaydan sonra süre medyanı (bar) | onaydan sonra <= 3 barda biten payı |
|---|---|---|---|
| BIST | 9 | 1 | %72 |
| ABD | 9 | 1 | %74 |
| AVR | 9 | 1 | %70 |

- S7'de 1-4 günlük bölge TANIM GEREĞİ yoktur (L >= Lmin); kısa ömür ölçüsü 'onaydan sonra <= 3 barda biten payı'dır.
- Hayatta kalma: yalnız bugün işlem gören hisseler (V_*.pkl).

