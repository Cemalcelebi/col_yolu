# MUM_IZI19 ÖN KAYIT (2026-11-26T13:58:36Z)

MUM_IZI11 / 13 / 17 ön kayıtlarının tanımları AYNEN (MUM_IZI_GOZ.py GZ_ESIK: ESIK11_SHA; G2_EK: EK13_SHA; K17_EK: EK17_SHA): giriş = bölgeden sonraki ilk geçerli barın açılışı; ufuk 15 mum; stop = bölge dibi x 0,98; dokunma; R30; CETVEL2 konum eşi; d5_tum; tablolar; permütasyonlar. Ek: set 7 = MUM_IZI18_ONAY_OLCEKLI 12 bölge (mum boyu kapısından geçen bölgeler; Cemal sonrasını görmeden, yüzde eksenli sayfada işaretledi; iki yıldız). Bu dosya set 7'nin getirileri hesaplanmadan ÖNCE commit edilir; getirisiz sayımlar aşağıda.

## Mühürler

KOD19_SHA: cd6f7c000ffda856a22009b10ed31ee9e21d18a3609e78d34cb24364bea6e175
EK19_SHA: 3cbf5ea6d8ce41058193db168469fe30532f34a630ba09b3ec29b5b11b13ff90
EK17_SHA: 8759a8a5693cff75903d074e0d5367b3691cd05cc7bef9b93c8874ef1e2aa4dd
EK13_SHA: f87dc6955ebad9306d117a5815bc59f129b9332dcc1dd559c886cad247f93447
GZ_KOD_SHA: f0b0381a4eabe14a015dc6eb929fcc34a1d95d2a399412cc05a5620c4ffb68d5
ESIK11_SHA: ea7535ce7ba59c64e6c5e934aa3722cbedb3786ddfe1f52d05b676d8bb315d75
ISARET_SET7_SHA: d991a820f202191196ca90d63c13abab6b6f0343e74737dd930294875fa29aea
ANAHTAR_SET7_SHA: 6cd64e26baef9455e24273d9e86f326354484294e920f85edf22d992ed6f98e5
OLCEKLI_SET7_SHA: 3e039fc35816e9b16aeed9603038f7526e08a7baf2ea8574593e9d5eab5f9487
ISARET_SET6_SHA: c546b40dbf197581f57fec36f91b9a71eb24bfe9f28edd6521205058ae97852c
ANAHTAR_SET6_SHA: 7f783321f23e8fdd9b5cfd87af92e5fa4332aea9e00cd139be520a4d1b766474
OLAY17_SHA: c0daa3204d079abd152888850a649249b70a4f0296252b26fbeaa345ea2653dc
SONUC17_SHA: 674643c418407edc14f019ea9b3f7cfb24acbd0d59f76faab0319b41825d0052
SONUC13_SHA: e1530dacca602fe1be5e566fda0a7cfaa864c6a5983991c5bd53f111316c9be1

- MUM_IZI_GOZ2.py commit'i: e0d9e3513b35bf6636e8647eaad746622e2fb5e0 2026-11-26T13:57:19+00:00

## GETİRİSİZ SAYIM (getiri hesaplanmadı; yalnız işaret, zaman, veri kapıları)

Set 7: 12 bölge, ölçülebilen 12, ölçülemeyen 0 {}; pazar {"ABD": 9, "BIST": 3}; en geç 15. mum 2022-04-15. Hakem sınıfı {"c": 5, "b": 4, "a": 3}; katman {"KÜÇÜK": 12}; yıldız {"EVET|haftalik": 1, "EVET|gunluk": 1}.

| Cemal | haftalık (ölçülebilen) | günlük (ölçülebilen) |
|---|---|---|
| BENZİYOR | 1 (1) | 5 (5) |
| KISMEN | 0 (0) | 2 (2) |
| BENZEMİYOR | 0 (0) | 4 (4) |

Set 6 + 7 (gerçek ölçekle işaretlenenler): 29 bölge, ölçülebilen 29, ölçülemeyen 0 {}; pazar {"ABD": 23, "AVR": 3, "BIST": 3}; en geç 15. mum 2022-04-15.

| Cemal | haftalık (ölçülebilen) | günlük (ölçülebilen) |
|---|---|---|
| BENZİYOR | 4 (4) | 6 (6) |
| KISMEN | 3 (3) | 6 (6) |
| BENZEMİYOR | 3 (3) | 7 (7) |

Birleşik set 1-7: 157 bölge, ölçülebilen 157, ölçülemeyen 0 {}; pazar {"ABD": 115, "BIST": 22, "AVR": 20}; en geç 15. mum 2022-12-30.

| Cemal | haftalık (ölçülebilen) | günlük (ölçülebilen) |
|---|---|---|
| BENZİYOR | 24 (24) | 22 (22) |
| KISMEN | 9 (9) | 16 (16) |
| BENZEMİYOR | 39 (39) | 47 (47) |

- Set 7'nin önceki setlerle ortak sembolü: 0 [] (bölge tekrarı yok: zaman + sembol + bölge sonu tekil, denetlendi).
- Eş sayısı (eşi < 5 / kovasız) hesapta belirlenir ve yazılır; eşsiz olay eşli tabloya girmez (GZ aynen).
- Set 7 haftalık yalnız 1 bölge (BENZİYOR, yıldızlı): haftalık hücreler 'yalnız döküm'; haftalık karşılaştırma yapılamaz. Günlük BENZİYOR 5 / BENZEMİYOR 4 / KISMEN 2.

## Tablolar (önceden; sonuçtan sonra değişmez)

- (i) DÖRDÜNCÜ BAKIŞ = yalnız set 7: Cemal sınıfı x zaman (haftalık, günlük, birlikte): n, R15 ort / medyan, eş ort, eşli fark ort / medyan, artıda payı, eşinden iyi payı, +%5 / +%10 stop'tan önce payı, stop payı (k17 hücresi) + GZ tabloları + EVET - eş (işaret çevirme). 12 bölgenin dökümü (sayfa, işaret, yıldız, zaman, sembol, R15, eş ort, mum boyu %, oran); yıldızlı iki bölge işaretli.
- (ii) KAPIDAN GEÇENLER (BİLGİ): set 7'nin 12 bölgesi Cemal'in işaretinden bağımsız ('mumları belirgin küçük bölgeler eşlerinden iyi gitti mi'): aynı ölçüler, zaman dilimine göre ve birlikte; ek satır yıldızlı 2; karşılaştırma satırı set 6'nın 17 bölgesi.
- (iii) GERÇEK ÖLÇEKLE İŞARETLENENLER = set 6 + set 7 (29): Cemal sınıfı (ve BENZİYOR + KISMEN) x zaman (haftalık, günlük, birlikte); BENZİYOR - BENZEMİYOR ve (BENZİYOR + KISMEN) - BENZEMİYOR eşli fark farkı, iki örneklem permütasyonu (iki yönlü, 10.000, tohum 19); iki grupta eşli n >= 2 değilse 'karşılaştırma yapılamaz'.
- (iv) BİRLEŞİK = set 1-7 (157): MUM_IZI17 birleşik tablosunun aynısı (GZ tabloları, EVET - eş, k17 hücresi, duyarlılık) + MUM_IZI17 birleşiğine göre değişim.
- YÖN (k19_yon): dördüncü bakış önceki üç bakışla aynı yönde mi (EVET - HAYIR eşli ve EVET - eş İŞARETİ). DÜZELTME (EK 17 HATA): her değer ancak ilgili her grupta eşli n >= 2 ise kullanılır; değilse 'karşılaştırma yapılamaz'. k17_yon ve mum_izi17_sonuc.json değişmez.
- Set 1-6 satırları mum_izi17_olay.csv ile karşılaştırılır (R15, es_R15, fark, n_es, es_neden): eş dışlama kümesi 157 olayla kurulduğu için eş değerleri değişebilir; değişen satır sayısı ve en büyük fark yazılır.
- OKUMA: set 7 ve set 6 + 7 hücrelerinin hepsi n < 30: etiket 'BİLGİ; ÖRNEKLEM YETERSİZ'. Eş sınırı: eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240).

## Ek tanımlar (K19_EK; sha yukarıda)

```
{
 "surum": "K19-1.0",
 "tanim": "MUM_IZI_GOZ GZ_ESIK aynen (ESIK11_SHA) + G2_EK aynen (EK13_SHA) + K17_EK aynen (EK17_SHA): giriş, ufuk 15 mum, stop = bölge dibi x 0,98, CETVEL2 konum eşi, dokunma, d5_tum, k17 hücresi, tablolar, permütasyonlar, işaret çevirme",
 "set7": "MUM_IZI18_ONAY_OLCEKLI (s2-13): sayfa -> bölge mühürlü MUM_IZI18_onay_anahtar.json 'yeni_sayfa' (zaman, pazar, sembol, bolge_bas = ilk barın tarihi, bolge_son, pencere, sinif, katman); işaret cemal_mum_izi18_onay.json (EVET / KISMEN / HAYIR; yildiz true / false); üç dosyada sayfa kümesi ve zaman aynı olmalı (değilse DUR); yildiz bool olmalı (değilse DUR); mum boyu / olağan / oran MUM_IZI18_onay_olcekli.json'dan aynen (yeniden hesaplanmaz)",
 "birlesik": "set 1-7 (157 bölge); eş dışlama kümesi 157 olayla kurulur; set 1-6 değerleri mum_izi17_olay.csv ile karşılaştırılır (R15, es_R15, fark, n_es, es_neden): değişen satır sayısı ve en büyük mutlak fark yazılır",
 "gecit": "k17_gecit aynen (gz_olc_bir kapıları; getiri hesaplamaz); hesapta gz_olc ile birebir aynı olmalı (değilse DUR)",
 "tablolar": {
  "dorduncu_bakis": "yalnız set 7: Cemal sınıfı (EVET / KISMEN / HAYIR) x zaman (haftalık, günlük, birlikte) k17 hücresi (n, n_es, R15 ort / medyan, eş ort, eşli fark ort / medyan, artıda payı, eşinden iyi payı, +%5 / +%10 stop'tan önce payı, stop payı) + gz_tablolar + g2_evet_es; 12 bölgenin dökümü (yıldızlılar işaretli)",
  "kapi": "BİLGİ: set 7'nin 12 bölgesi Cemal'in işaretinden bağımsız (mum boyu kapısından geçen bölgeler): zaman (haftalık, günlük, birlikte) k17 hücresi; ek satır: yıldızlı 2 bölge; karşılaştırma satırı set 6'nın 17 bölgesi aynı ölçülerle",
  "olcekli": "set 6 + set 7 (29; Cemal sonrasını görmeden yüzde eksenli sayfada işaretledi): Cemal sınıfı (EVET, KISMEN, HAYIR, EVET+KISMEN) x zaman (haftalık, günlük, birlikte) k17 hücresi; EVET - HAYIR ve (EVET+KISMEN) - HAYIR eşli fark farkı her zaman diliminde (birlikte dahil): iki örneklem permütasyonu (iki yönlü, 10.000, tohum 19), her iki grupta eşli n >= 2 değilse 'karşılaştırma yapılamaz'; R15 farkı bilgi; + gz_tablolar + g2_evet_es",
  "birlesik": "set 1-7 (157): gz_tablolar (MUM_IZI13 / 17 birleşik tablosunun aynısı) + g2_evet_es + k17 hücresi + duyarlılık (son işaret); MUM_IZI17 birleşiği (mum_izi17_sonuc.json) ile fark: karşılaştırma satırları, EVET - eş, hücre n / R15 / eşli fark",
  "yon": "k19_yon: dördüncü bakış önceki üç bakışla aynı yönde mi (EVET - HAYIR eşli fark farkı ve EVET - eş İŞARETİ; dilim başına); DÜZELTME (EK 17 HATA): bir değer ancak ilgili her grupta eşli n >= 2 ise kullanılır (EVET - HAYIR: n_es_a ve n_es_b >= 2; EVET - eş: n_es >= 2), değilse 'karşılaştırma yapılamaz'; önceki bakışların değerleri de aynı korumayla okunur (üçüncü bakış günlük EVET n 1 -> yapılamaz); k17_yon ve mum_izi17_sonuc.json değişmez"
 },
 "karsilastirma": {
  "n_min": 2,
  "perm": 10000,
  "tohum": 19
 },
 "etiket": "BİLGİ; ÖRNEKLEM YETERSİZ (set 7 ve set 6+7 hücrelerinin hepsi n < 30)",
 "es_siniri": "eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240): aynı gün aynı kova konum eşi",
 "pdf": "MUM_IZI17_SONRASI düzeni (k17_sayfa aynen): kapakta düz dil özet tablo (set 7 Cemal sınıfı x zaman; set 6+7 Cemal sınıfı x zaman) + kapı / set 6+7 farkı / birleşik birer satır; sonra 12 bölgenin hepsi: BENZİYOR (yıldızlılar önce), KISMEN, BENZEMİYOR (her sınıfta önce haftalık, sonra bölge sonu sırası); yıldızlı sayfada 'yıldız koydun' satırı"
}
```

## KONTROL LİSTESİ (`python IZ_KARNE.py kontrol`; K8: set 7 ve set 6 + 7 hücreleri n < 30)

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü aynı kova (CETVEL2 v2.2 konum eşi) aynı takvim aralığı aynı stop geometrisi (GZ aynen); eş dışlama 157 olayla; sınır: eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240) |
| K2 | geleceğe bakma | EVET | Cemal set 7'yi sonrasını görmeden işaretledi (ölçekli sayfa bölge sonunda kesik); işaret dosyası commit 5068fa8, bu ön kayıt set 7 getirilerinden önce; giriş bölgeden SONRAKİ barın açılışı; veri <= 2022-12-31 + KASA kapısı |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar (H > L, V > 0); haftalık barlar tamamlanmış ISO haftaları (MH / MV aynen) |
| K4 | tekilleştirme | EVET | 157 tekil bölge (zaman + sembol + bölge sonu; k19_ornek DUR); set 7'nin önceki setlerle ortak sembolü sayılıp yazılır |
| K5 | giriş fiyatı | EVET | giriş = bölgeden sonraki ilk geçerli barın açılışı (haftalıkta sonraki haftanın ilk günü); giriş <= stop olay ölçülmez (sayısı yazılır) |
| K6 | veri birimi | EVET | MI bölünme düzeltmeli fiyatlar (GZ aynen); getiriler oransal; ABD USD, AVR yerel para, BIST TL; pazarlar arası karşılaştırma eşli farkla |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç bilgi, kasa açılmaz |
| K8 | örneklem ve dönem | EVET | set 7 hücreleri n 0-5, set 6+7 hücreleri n < 30: etiket 'BİLGİ; ÖRNEKLEM YETERSİZ'; eşli n < 2 'karşılaştırma yapılamaz' (yön satırında da); 12 bölge tek tek listeli; tek dönem (<= 2022), BH yok (karar yok) |
| K9 | ön kayıt | EVET | MUM_IZI19_ON_KAYIT.md: KOD19 / EK19 / EK17 / EK13 / ESIK11 / işaret / anahtar / ölçekli / olay17 / sonuç17 sha + getirisiz sayımlar; set 7 getirilerinden önce commit + push; k19_kapi sha + commit + temiz ağaç + IZ_KARNE.ik_kontrol_kapisi |
| K10 | ayrıştırma | EVET | işaret şeması GZ.gz_isaret_oku (bilinmeyen değer DUR) + yildiz bool (DUR); üç set 7 dosyasında sayfa kümesi ve zaman aynı (DUR); bölge başı veriden yeniden hesaplanıp anahtarla denetlenir (k17_gecit) |
| K11 | yeniden üretim | EVET | getirisiz geçit hesapta gz_olc ile birebir (DUR); haftalık +%10 k17 dokunma fonksiyonuyla GZ d10'a eşit (DUR); set 1-6 satırları mum_izi17_olay.csv ile karşılaştırılır; >= 2 hücre olay csv'sinden bağımsız kodla yeniden üretilir (rapor öncesi, test_mum_izi19) |
| K12 | ifade | EVET | 'iz / tuttu / anlamlı' sözü yok; sayı ile yorum ayrı; n < 30 'örneklem yetersiz' |
| K13 | süreç | EVET | çakışma kapısı korunur; çalışan fonksiyonlar değişmez (test_mum_izi19 ast karşılaştırması, f218598'e göre); yasak defter / mühürlü dosyalara dokunulmaz; yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez |

## SAPMA

(ön kayıt anında yok)
