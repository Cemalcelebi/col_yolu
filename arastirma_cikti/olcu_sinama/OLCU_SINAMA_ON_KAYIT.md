# ÖLÇÜ SINAMASI — ÖN KAYIT (2026-11-22 09:19:21 UTC)

Sürüm: OLCU_SINAMA v1.0 (2026-11-22). İş tanımı: arastirma_cikti/olcu_sinama/OLCU_SINAMA_IS_TANIMI.md (sha 72ecb7633fac9d74df656361e6d04dccbc98a3e9f539c54fa93941e19e14b7ff).
Kod: OLCU_SINAMA.py git f7159eeddf73e98a7cada441e80f14b90b422b4c 2026-11-22T09:18:03+00:00. Bu dosya koşudan ÖNCE commit edilir; os_kapi git kaydını, değişmemişliği, sha'ları ve kontrol tablosunu denetler.

## SHA

| Ad | sha256 |
|---|---|
| OS_ESIK_SHA | `4bdc1d0617daed80531095f246e3d6c5e3c594374fd3021595c038b26bf441ab` |
| OS_KOD_SHA | `86c8402136e0b77f9e95d5f75556251728ae48f59647cc6f97d91cf38eead087` |
| OC_KOD_SHA | `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb` |
| CETVEL2_KOD_SHA | `2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6` |
| KASA_KOD_SHA | `3db7b60d44bee8234c7c41e42ba7a8c3a3fc43803222a1f7e06adc154d41805b` |
| IS_TANIMI_SHA | `72ecb7633fac9d74df656361e6d04dccbc98a3e9f539c54fa93941e19e14b7ff` |
| V_ABD_SHA | `7c343a5dcbb96d6d33a22096b48d6fb7223b6a7c0ae6eaaf43002193d9810c91` |
| V_AVR_SHA | `349ac0b0ec7bb2ff5498e6f8fb876a9e5bdcd3a9b88b11807ab7976a4f5f0830` |
| KASA_DURUM_SHA | `e603b2a1abdd85d207b523ad0479a4f42b53067fd309da9f7b6d0772fb8aafee` |
| SINIR_JSON_SHA | `fefc82566205194f00ea80882523b111d4d0414575db21943ef6ba523e4bb506` |
| PREFIX_JSON_SHA | `26a3e09e7269e000a15a731874c0b4d528116df9d277fa6d33fa4e808e4af84e` |

OS_ESIK_SHA: `4bdc1d0617daed80531095f246e3d6c5e3c594374fd3021595c038b26bf441ab`
OS_KOD_SHA: `86c8402136e0b77f9e95d5f75556251728ae48f59647cc6f97d91cf38eead087`

KASA açık kesik: 2023-12-31 (KASA_DURUM.json; veri yalnız /tmp/kasa/acik). Pazarlar: ABD, AVR (BIST kapsam dışı).

## Kova sınırları (giriş 2016-22 havuz hisse-günleri, getirisiz; sayı)

| Pazar | KV1 ATRP tercil | KV1 F15 çeyrek | KV2 ATRP ondalık | n KV1 / KV2 |
|---|---|---|---|---|
| ABD | 0.022686, 0.035981 | 0.285607, 0.617085, 0.877056 | 0.015316, 0.018612, 0.021692, 0.024850, 0.028336, 0.032604, 0.038163, 0.046302, 0.061210 | 1505817 / 1514092 |
| AVR | 0.019580, 0.028393 | 0.282130, 0.610447, 0.871114 | 0.014152, 0.016668, 0.018866, 0.021065, 0.023453, 0.026219, 0.029665, 0.034510, 0.043354 | 752978 / 754510 |

## Evren prefix testi (hazırlık; getirisiz; koşuda yeniden yapılmaz, os_prefix.json sha'sı yukarıda)

| Pazar | sonuç | gün (<= 2022-05-31) | havuz hisse-gün | hisse kısa / uzun | toplam fark | ok / H / KV1 / KV2 farkı | olay kümesi farkı |
|---|---|---|---|---|---|---|---|
| ABD | TUTTU | 1764 | 1406633 | 1349 / 1380 | 0 | 0 / 0 / 0 / 0 | 0 |
| AVR | TUTTU | 1903 | 754809 | 572 / 576 | 0 | 0 / 0 / 0 / 0 | 0 |

## Bölüm 2-5 (iş tanımından AYNEN)

## 2. PANEL (nedensel; iki bilinen geleceğe bakma DÜZELTİLMİŞ; arastirma_cikti/cetvel2/KENAR_ETKISI_DENETIM.md'yi oku)
OLCU_SINAMA kendi panelini kurar (ORTAK_CETVEL içe alınabilir ama şu iki kural yeniden yazılır): (a) hisse evrene KENDİ 80. geçerli barından sonra girer (veri sonuna kadarki bar sayısı kullanılmaz); (b) bölünme şüphesi yalnız d-1'e kadarki barlarla; son 10 barda büyük sıçrama varsa kalıcılığı henüz bilinmediği için o hisse-gün havuz DIŞI (tutucu). Geçerli bar, likidite alt %20 dışlama, giriş t+1 açılış aynı. EVREN PREFIX TESTİ (zorunlu): veri iki farklı tarihte kesilir (2022-06-30 ve 2023-12-29); sinyal günü <= 2022-05-31 olan bütün hisse-günlerde havuz üyeliği, kova ve olay kümeleri BİREBİR aynı olmalı (son giriş şeridi hariç tutulmaz; fark 0 beklenir); tutmazsa dur ve nedenini yaz.

## 3. KONTROL KARTLARI (bilinen etkiler; ay sonu olayları; ABD ve AVR; alt dönem d1 2016-19, d2 2020-23)
- MOM: 12-1 momentum üst onda (+) ve alt onda (−; 0'ı kesmesi yeter). Beklenen ufuk: 30-60.
- STREV: son 21 işlem günü getirisi ALT onda (+) ve ÜST onda (−) (kısa vadeli dönüş; Jegadeesh 1990; beklenen ufuk 15-30). Not: yaşayan evren alt ondayı yukarı yanlı gösterir; yazılır.
- HIGH52: kapanış / 252 gün en yüksek üst onda (+).
- PLASEBO: rastgele etiket (200 tohum) ve YAPAY İZ (+%1 / +%2 / +%3 / +%5 sürüklenme; n 100 / 300 / 1000; 20 tohum).

## 4. ADAY ÖLÇÜLER (hepsi giriş E0 = t+1 açılış; H ∈ {15, 30, 60}; eş = aynı giriş günü, aynı pazar, olay kümesi dışı, en az 5 eş)
EŞ KOVALARI iki sürüm, yan yana: KV1 = CETVEL2 kovası (ATRP tercili x likidite üçlüsü x F15 çeyreği); KV2 = oynaklık ince + konumsuz (ATRP ONDALIĞI x likidite üçlüsü; F15 yok). Sınırlar 2016-22'den sabit.
- O1 ortalama getiri farkı: R_H − eş ortalaması (CETVEL2 ile aynı; H 60 eklendi).
- O2 sıra: R_H'nin eş dağılımındaki yüzdeliği − 0,5 (aykırı değere dayanıklı).
- O3 hedefe dokunma: T10_H = H bar içinde High >= E0 x 1,10 (ve T5_H); olay payı − eş payı.
- O4 oynaklığa göre ölçekli asimetri: A_H = [(maks High − E0) − (E0 − min Low)] / (E0 x ATRP14(t)); olay − eş ortalaması.
- O5 önce-hedef, oynaklık ölçekli: +1,5 x ATRP hedefi −1,5 x ATRP stop'tan önce görüldü mü (H bar; aynı barda ikisi birden ise stop sayılır); olay payı − eş payı.
İstatistik (hepsi için aynı): hücre = pazar x alt dönem; ay kümeli bootstrap %95 (B 2000), ay kümeli işaret permütasyon p, L3O; TUTAR = n >= 30, fark beklenen yönde, boot alt ucu > 0 (yön − ise üst ucu < 0), L3O aynı işaret.

## 5. ÖLÇÜ SEÇİM KURALI (önceden yazılı; sonuç görülmeden)
Bir (ölçü, kova, H) üçlüsü GEÇER ancak hepsi tutarsa: (i) PLASEBO: ABD ve AVR'nin dört hücresinde ortalama fark ~0 (|fark| ölçünün hücre içi standart sapmasının %3'ünden küçük) ve yön başına tutar payı <= %7; (ii) YAPAY İZ: +%2 sürüklenme n <= 1000'de dört hücrede >= %80 yakalanır; (iii) OYNAKLIK ÖDÜLÜ YOK: MOM alt onda ve STREV üst onda (beklenen −) hiçbir hücrede beklenenin TERSİ yönde tutmaz; (iv) BİLİNEN ETKİYİ GÖRÜR: en az bir kontrol kartının + bacağı (MOM üst, STREV alt ya da HIGH52 üst) ABD'nin İKİ alt döneminde de TUTAR (AVR bilgi). Geçenler arasında sıralama: (1) Cemal'in kuralına yakın ufuk (15 < 30 < 60 tercih sırası: önce 15, sonra 30, sonra 60); (2) daha çok kontrol kartı gören; (3) yapay izde daha küçük n. Hiçbiri geçmezse: 'bu evren ve eş kurulumunda 15-60 mum ölçüsü bilinen etkiyi göremiyor' diye raporlanır; ek tanı: aynı kontrol kartları EŞSİZ (ham kesit: üst onda − alt onda aylık getiri farkı, klasik portföy yöntemi, H 21 / 63 gün) görünüyor mu (evren mi, eş kurulumu mu sorumlu).

## İşlemsel tanımlar (sonuç görülmeden; OS_ESIK tam metni aşağıda)

- O3 iki aday olarak ölçülür: O3a = T5_H, O3b = T10_H (iş tanımı 'T10_H (ve T5_H)').
- Kart sırası: aynı ay sonu t kesitinde, giriş günü havuzda olan ve değeri sonlu hisseler; üst onda > 0,90, alt onda <= 0,10 (pct rank first, sembol sırası).
- Eş dışlama ('olay kümesi dışı'): aynı bacağın tekilleştirme ÖNCESİ bütün ondalık üyeleri ve olayın kendisi.
- Tekil: bacak x H başına >= H birleşik takvim günü (CETVEL2 v2.2 tekil = H).
- Plasebo olayları: ay sonu giriş günü havuzundan %10 rastgele; GEÇER = |ort fark| < 0,03 SD VE TUTAR(+) payı <= %7 VE TUTAR(-) payı <= %7.
- Yapay iz: ay sonu giriş günleri havuzundan n hisse-gün (R_H, KV1, KV2 var); yol sürüklemesi; yakalama = TUTAR(+); n* tanımı OS_ESIK['secim']['ii'].
- Seçim şartı (iii) 'hiçbir hücre' = ABD ve AVR dört hücre; (iv) aynı bacak ABD d1 VE d2.
- Ek beraberlik bozucu (4) iş tanımında yok, sonuç görülmeden eklendi: O1 < O3a < O3b < O2 < O5 < O4, KV2 < KV1.
- Klasik portföy tanısı her durumda hesaplanır (seçimde kullanılmaz; 'hiçbiri geçmezse' tanısı olarak raporlanır).

## OS_ESIK (mühürlü; sha yukarıda)

```json
{
 "surum": "OS1.0",
 "veri": {
  "klasor": "/tmp/kasa/acik (= /tmp/veri = /tmp/veri2); başka fiyat kaynağı YOK",
  "kesik_tarih": "2023-12-31",
  "pazar": [
   "ABD",
   "AVR"
  ],
  "bist": "kapsam dışı (iş tanımı bölüm 3: ABD ve AVR)",
  "yukle": "OC.oc_veri(pazar, E: min_bar 1, abd_ek_aktif False; k34 YOK) = geçerli bar süzgeci (O/H/L/C > 0 sonlu, H > L, V > 0), ABD evren dışı (ETF / fon) listesi; ardından DS açılış kırpması (Open H-L dışındaysa [L, H]'ye kırpılır)",
  "kapi": "KASA.kasa_kapisi(V_ABD.pkl, V_AVR.pkl) + KASA_DURUM.json açık kesik = kesik_tarih değilse DURUR"
 },
 "evren": {
  "gec_bar": 80,
  "tanim": "hisse d gününde evrende <=> hissenin d'den ÖNCEKİ geçerli bar sayısı >= 80 (min_bar süzgeci yok; veri sonuna kadarki bar sayısı kullanılmaz)"
 },
 "bolunme": {
  "esik": 0.25,
  "geri_gun": 10,
  "geri_pay": 0.5,
  "oranlar": [
   1.5,
   2,
   3,
   4,
   5,
   6,
   8,
   10,
   15,
   20,
   25,
   30,
   40,
   50,
   100
  ],
  "oran_tol": 0.04,
  "pencere": 61,
  "tanim": "aday sıçrama (hissenin kendi geçerli kapanışları, bar i): |C_i / C_{i-1} - 1| > 0,25 VE önceki 10 bar düz (|ln C_{i-1} / C_{max(0, i-11)}| < 0,5 |ln r_i|) VE |ln r_i| bir bölünme oranının ln'ine +-0,04 yakın (yalnız geçmiş). KALICILIK (|ln C_{i+10} / C_{i-1}| >= 0,5 |ln r_i|) ancak bar i+10 d'den önceyse bilinir. Havuz dışı günler: kalıcı aday için birleşik takvimde [p_i + 1, max(p_i + 61, p_{i+10})], kalıcı olmayan için [p_i + 1, p_{i+10}] (bekleme: kalıcılık bilinene kadar), i+10 veri sonunu aşıyorsa veri sonuna kadar (p = birleşik takvim konumu)"
 },
 "likidite": {
  "gun": 20,
  "min_gun": 10,
  "alt_kesik": 0.2,
  "tanim": "C x V (x Kur, EUR) önceki 20 birleşik takvim gününün medyanı (shift 1, en az 10 gün); alt %20 kesiti = d günü evrende, geçerli barı ve sonlu likiditesi olan hisseler"
 },
 "havuz": {
  "mom": 60,
  "mom_kova": 5,
  "likit_kova": 3,
  "min_havuz": 30,
  "tanim": "ok = d günü geçerli bar VE evrende VE momentum60 (C(d-1) / C(d-61) - 1, birleşik takvim, 5 gün ileri taşıma) sonlu VE likidite sonlu VE alt %20 dışı VE bölünme dışı; havuzda >= 30 hisse varsa 5 momentum x 3 likidite (qcut, rank first); likidite üçlüsü LQ3 = H % 3 (ORTAK_CETVEL ile aynı)"
 },
 "giris": {
  "azami_bosluk": 10,
  "tanim": "t'den sonraki ilk geçerli bar (hissenin kendi takvimi) AÇILIŞI E0; t ile giriş arası <= 10 birleşik takvim günü; giriş günü havuzda (ok ve H >= 0)"
 },
 "kova": {
  "donem": [
   "2016-01-01",
   "2022-12-31"
  ],
  "atrp_gun": 14,
  "f15_gun": 120,
  "atrp_q": [
   0.3333333333333333,
   0.6666666666666666
  ],
  "f15_q": [
   0.25,
   0.5,
   0.75
  ],
  "atrp_onda": [
   0.1,
   0.2,
   0.3,
   0.4,
   0.5,
   0.6,
   0.7,
   0.8,
   0.9
  ],
  "KV1": "ATRP tercili x 12 + LQ3 x 4 + F15 çeyreği (CETVEL2 kovası; 36)",
  "KV2": "ATRP ondalığı x 3 + LQ3 (30; F15 yok)",
  "tanim": "ATRP_t = ort TR [t-13, t] / C_t (TR önceki kapanışla; ilk bar H-L), F15_t = (C_t - min) / (max - min) son 120 geçerli kapanış; t = hissenin d'den önceki son geçerli barı. Sınırlar pazar başına havuz hisse-günlerinden (giriş 2016-22, ok VE H >= 0 VE ATRP sonlu (KV1 için F15 de)) numpy quantile (doğrusal), getirisiz; os_sinir.json ve ön kayıtta sayı olarak; 2023 ve prefix testinde aynı sayılar"
 },
 "es": {
  "min": 5,
  "tanim": "aynı giriş günü d, aynı pazar, aynı kova (KV1 ya da KV2), havuzda, o ölçüde ölçülebilir; aynı bacağın o gün olay kümesindeki (tekilleştirme ÖNCESİ bütün ondalık üyeleri) hisseler ve olayın kendisi çıkarılır; en az 5 eş"
 },
 "ufuk": [
  15,
  30,
  60
 ],
 "pencere_kat": 2,
 "olcu": {
  "R": "R_H = H. geçerli barın (giriş barı 1.) kapanışı / E0 - 1; giriş satırından itibaren 2H birleşik takvim satırında H geçerli bar yoksa ölçülmez (CETVEL2 v2.2 c2_rh ile aynı)",
  "O1": "R_H - eş ortalaması R_H",
  "O2": "SIRA - 0,5; SIRA = (#eş R_H < olay + 0,5 #eş R_H = olay) / #eş",
  "O3a": "T5_H = H bar içinde maks High >= E0 x 1,05 (olay 0/1 - eş payı)",
  "O3b": "T10_H = H bar içinde maks High >= E0 x 1,10 (olay - eş payı)",
  "O4": "A_H = [(maks High - E0) - (E0 - min Low)] / (E0 x ATRP14(t)); olay - eş ortalaması (ATRP sonlu ve > 0 değilse ölçülmez)",
  "O5": "+1,5 x ATRP14(t) x E0 hedefi (High >=) -1,5 x ATRP14(t) x E0 stop'tan (Low <=) önce H bar içinde; aynı barda ikisi = stop; hiçbiri = 0; olay - eş payı",
  "bar": "H bar = giriş barı dahil H geçerli bar (High / Low giriş barının açılış sonrası)"
 },
 "hedef": {
  "T5": 0.05,
  "T10": 0.1,
  "o5_kat": 1.5
 },
 "donem": {
  "d1": [
   "2016-01-01",
   "2019-12-31"
  ],
  "d2": [
   "2020-01-01",
   "2023-12-31"
  ],
  "tarih": "giriş günü"
 },
 "kart": {
  "onda": 0.1,
  "ay_sonu": "t = birleşik takvimde ayın son günü; hissenin t'de geçerli barı olmalı (kendi bar indeksi k)",
  "MOM": "C_{k-21} / C_{k-252} - 1 (k >= 252)",
  "STREV": "C_k / C_{k-21} - 1 (k >= 21)",
  "HIGH52": "C_k / maks High_{k-251..k} (k >= 251)",
  "sira": "aynı t kesitinde, giriş günü havuzda olan (ok ve H >= 0) ve değeri sonlu hisseler arasında yüzde sıra (sembol sırasıyla rank first, pct): üst onda > 0,90; alt onda <= 0,10",
  "bacak": {
   "MOM+": "MOM üst onda (+)",
   "MOM-": "MOM alt onda (-)",
   "STREV+": "STREV alt onda (+)",
   "STREV-": "STREV üst onda (-)",
   "HIGH52+": "HIGH52 üst onda (+)"
  },
  "tekil": "bacak x H başına: aynı hissede olaylar giriş günü sırasıyla, birleşik takvimde >= H gün arayla (CETVEL2 v2.2: tekil = H); eş dışlama kümesi tekilleştirme öncesi bütün bacak üyeleri"
 },
 "boot": {
  "B": 2000,
  "tohum": 2261,
  "alt": 0.025,
  "ust": 0.975,
  "birim": "giriş ayı (ay toplamı ve sayısı yeniden örneklenir)"
 },
 "perm": {
  "R": 10000,
  "tohum": 2263,
  "tanim": "ay kümeli işaret permütasyonu; yön + / - tek yönlü"
 },
 "hucre": {
  "n_min": 30,
  "tutar": "TUTAR(+) = n >= 30 VE ort fark > 0 VE boot alt > 0 VE L3O(+) > 0; TUTAR(-) = n >= 30 VE ort fark < 0 VE boot üst < 0 VE L3O(-) < 0. L3O(+) = beklenen + için en olumlu 3 ay (çıkınca ortalamayı en çok düşüren) çıkınca ortalama; L3O(-) tersi. Hücre = pazar x dönem (d1 / d2)"
 },
 "plasebo": {
  "tohum_sayi": 200,
  "tohum": 2264,
  "pay": 0.1,
  "fark_sd_oran": 0.03,
  "tutar_pay": 0.07,
  "tanim": "rastgele etiket: her ay sonu giriş günü (t'den sonraki ilk birleşik takvim günü) havuzundan (ok, H >= 0) yerine koymadan %10 (round) rastgele hisse = olay; eş dışlama = çekilen küme; aynı ölçü / kova / H cetveli; 200 tohum. GEÇER (hücre) = |200 tohum ortalama fark| < 0,03 x SD (SD = hücrenin bütün tohumlardaki olay başı farklarının standart sapması) VE TUTAR(+) payı <= %7 VE TUTAR(-) payı <= %7 (yön başına)"
 },
 "yapay": {
  "delta": [
   0.0,
   0.01,
   0.02,
   0.03,
   0.05
  ],
  "n": [
   100,
   300,
   1000
  ],
  "tohum_sayi": 20,
  "tohum": 2265,
  "n_azami_pay": 0.6666666666666666,
  "karar_delta": 0.02,
  "karar_pay": 0.8,
  "tanim": "hücrenin ay sonu giriş günleri havuzundan (ok, H >= 0, R_H sonlu, KV1 >= 0, KV2 >= 0) yerine koymadan n hisse-gün; yol sürüklemesi: k. geçerli bar (k = 0 giriş barı) High / Low / Close x (1 + delta (k+1) / H), E0 ve ATRP değişmez (POZITIF_KONTROL pk_surukle); bütün ölçüler sürüklenmiş yoldan yeniden; eşler dokunulmaz; eş dışlama = çekilen küme; yakalama = TUTAR(+). n > 2/3 havuz ise ölçülmez"
 },
 "secim": {
  "i": "PLASEBO: ABD ve AVR'nin dört hücresinde (d1, d2) plasebo GEÇER",
  "ii": "YAPAY İZ: +%2 sürüklenmede dört hücrenin her birinde n <= 1000 olan bir n'de yakalama >= %80; n* = dört hücrede >= %80'e ulaşan en küçük n'lerin en büyüğü",
  "iii": "OYNAKLIK ÖDÜLÜ YOK: MOM- ve STREV- bacakları ABD / AVR dört hücrenin hiçbirinde TUTAR(+) değil",
  "iv": "BİLİNEN ETKİYİ GÖRÜR: MOM+, STREV+ ya da HIGH52+ bacaklarından en az biri ABD d1 VE ABD d2'de TUTAR(+) (AVR bilgi)",
  "sira": "(1) küçük H önce (15 < 30 < 60); (2) daha çok kontrol kartı bacağı gören (beş bacaktan ABD d1 ve d2'de beklenen yönde TUTAR olanların sayısı); (3) daha küçük n*; (4) EK BERABERLİK BOZUCU (sonuç görülmeden, iş tanımında yok): basit ölçü önce O1 < O3a < O3b < O2 < O5 < O4, sonra KV2 < KV1",
  "hicbiri": "'bu evren ve eş kurulumunda 15-60 mum ölçüsü bilinen etkiyi göremiyor' + klasik portföy tanısı"
 },
 "prefix": {
  "kisa": "2022-06-30",
  "uzun": "2023-12-29",
  "son": "2022-05-31",
  "tanim": "iki kesikte panel + kartlar; havuz / sinyal günü <= 2022-05-31 olan bütün hisse-günlerde ok, H (5x3), KV1, KV2 ve bütün bacak x H olay kümeleri (sembol, tarih, giriş) birebir; fark 0 beklenir, değilse DURUR"
 },
 "klasik": {
  "H": [
   21,
   63
  ],
  "tanim": "eşsiz ham kesit: ay sonu kart ondalıkları (tekilsiz, havuz evreni), giriş E0, R_H (2H satır kuralı); ay başına eşit ağırlıklı üst onda - alt onda (STREV: alt - üst) ortalama farkı; hücre ortalaması ve Newey-West t (gecikme ceil(H / 21))"
 },
 "yeniden": {
  "hucre": [
   [
    "MOM+",
    "ABD",
    "d2",
    "O1",
    "KV1",
    15
   ],
   [
    "STREV+",
    "ABD",
    "d1",
    "O3a",
    "KV2",
    30
   ],
   [
    "HIGH52+",
    "AVR",
    "d2",
    "O5",
    "KV1",
    60
   ]
  ],
  "olay": 30,
  "tohum": 2266,
  "tanim": "üç hücre satır dosyasından düz pandas (n, ort fark); 30 olayın R / T5 / T10 / A / O5 ölçüsü ham pkl'den düz döngüyle; tutmazsa koşu TUTMADI"
 }
}
```

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü, aynı pazar, aynı kova (KV1 ATRP x LQ3 x F15 / KV2 ATRP ondalığı x LQ3), bütün havuz, aynı geometri (aynı E0, aynı H, aynı ölçü tanımı olay ve eşte); bacak üyeleri ve olay eş dışı; >= 5 eş (os_es); taban rastgele olay sağlaması = plasebo 200 tohum (os_plasebo); mekanik üstünlük: O4 / O5 ATRP ölçekli, kova ATRP ile kurulu (oynaklık ödülü şartı iii) |
| K2 | geleceğe bakma | EVET | evren = kendi 80. geçerli barından sonra (min_bar yok); bölünme kalıcılığı yalnız d-1'e kadar (bilinmiyorsa havuz dışı); momentum / likidite / ATRP / F15 d-1'e kadar; kart değerleri t'de; EVREN PREFIX TESTİ (2022-06-30 vs 2023-12-29; <= 2022-05-31 ok / H / KV1 / KV2 / olay kümeleri fark 0, os_prefix.json; tutmazsa DURUR); KASA kapısı kesik 2023-12-31 |
| K3 | geçerli bar | EVET | OC.oc_veri_hazirla (O/H/L/C > 0 sonlu, H > L, V > 0) + açılış kırpması; ölçüler yalnız geçerli barlar (kendi takvimi); kart sinyali t'de geçerli bar ister |
| K4 | tekilleştirme | EVET | bacak x H başına aynı hissede >= H birleşik takvim günü arayla tek olay (örtüşmeyen H bar); n = ölçülen olay; boot / permütasyon birimi giriş ayı; medyan farkı tabloda |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (<= 10 gün boşluk); eşler aynı gün açılışı; test 'giriş' |
| K6 | veri birimi | EVET | V_*.pkl tek kip (fi_k1_veri düzeltilmiş; KASA bayt bayt bölünmüş açık kısım); ölçüler oran / ATRP ölçekli (birimsiz); likidite günlük kesit sırası, AVR x Kur; bölünme şüphesi (nedensel) havuz dışı |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD, V_AVR; batanlar yok): getiriler yukarı yanlı, STREV alt onda yukarı yanlı görünür; raporda yazılı; yanlılık olay ve eşte aynı evrende |
| K8 | örneklem ve dönem | EVET | iki alt dönem (d1 2016-19, d2 2020-23) x iki pazar ayrı hücre; n < 30 TUTMAZ; plasebo 200 tohum, yapay iz 20 tohum x 3 n x 5 delta; seçim kuralı dört şartın hepsi (çoklu karşılaştırma şart birleşimiyle; BH yok, yazılı) |
| K9 | ön kayıt | EVET | OLCU_SINAMA_ON_KAYIT.md: OS_ESIK sha, OLCU_SINAMA.py sha + kod commit, kova sınırları (sayı), prefix sonucu, OC / CETVEL2 / KASA / veri sha'ları, KASA açık kesik; os_kapi ön kaydın git'te işlenmiş + değişmemiş + sha eşit + ik_kontrol_kapisi; sıra kod commit -> ön kayıt commit -> koşu; seçim kuralı iş tanımından (df0a499) aynen |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / SEC ayrıştırması yok; yalnız OHLCV açık pkl; kart sinyalleri fiyattan |
| K11 | yeniden üretim | EVET | os_yeniden: üç hücre satır dosyasından düz pandas; 30 olayın ölçüleri ham pkl'den düz döngüyle; tutmazsa koşu TUTMADI |
| K12 | ifade | EVET | ölçü seçimi; 'iz' iddiası yok; fark, boot, p, tutar ayrı; sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_os; test); OC / CETVEL2 / KASA / kart / kasa / defter dosyalarına dokunulmadı; e-posta / anahtar taraması (_os_yaz); indirme yok; kod değişirse 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçü sınaması |
