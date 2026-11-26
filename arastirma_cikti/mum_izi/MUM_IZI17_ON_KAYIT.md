# MUM_IZI17 ÖN KAYIT (2026-11-26T12:59:45Z)

MUM_IZI11_ON_KAYIT ve MUM_IZI13_ON_KAYIT tanımları AYNEN (MUM_IZI_GOZ.py GZ_ESIK: ESIK11_SHA; MUM_IZI_GOZ2 G2_EK: EK13_SHA): giriş = bölgeden sonraki ilk geçerli barın açılışı; ufuk 15 mum; stop = bölge dibi x 0,98; dokunma; R30; CETVEL2 konum eşi; tablolar; permütasyonlar. Ek: set 6 = MUM_IZI14_ONAY_OLCEKLI 17 bölge (Cemal'in sonrasını görmeden, yüzde eksenli sayfada işaretlediği ilk set). Bu dosya set 6'nın getirileri hesaplanmadan ÖNCE commit edilir; getirisiz sayımlar aşağıda.

## Mühürler

KOD17_SHA: 3daca74abb5a4285b050cf7800a24bb0a78973b1b8fef5dd699ddf10561f08f1
EK17_SHA: 8759a8a5693cff75903d074e0d5367b3691cd05cc7bef9b93c8874ef1e2aa4dd
EK13_SHA: f87dc6955ebad9306d117a5815bc59f129b9332dcc1dd559c886cad247f93447
GZ_KOD_SHA: f0b0381a4eabe14a015dc6eb929fcc34a1d95d2a399412cc05a5620c4ffb68d5
ESIK11_SHA: ea7535ce7ba59c64e6c5e934aa3722cbedb3786ddfe1f52d05b676d8bb315d75
ISARET_SET6_SHA: c546b40dbf197581f57fec36f91b9a71eb24bfe9f28edd6521205058ae97852c
ANAHTAR_SET6_SHA: 7f783321f23e8fdd9b5cfd87af92e5fa4332aea9e00cd139be520a4d1b766474
OLCEKLI_SET6_SHA: e022af53a12921de30139abd60056d58915056c07c48a813ebc423c1571d0bf7
OLAY13_SHA: fc27c506ae981157f13b2aeb534e2c9c098a947ad0b158130f0c5845f73dcec8
SONUC13_SHA: e1530dacca602fe1be5e566fda0a7cfaa864c6a5983991c5bd53f111316c9be1

- MUM_IZI_GOZ2.py commit'i: 3a818cc4aaae5e4ea391fdd9d7c782a015b7f890 2026-11-26T12:58:37+00:00

## GETİRİSİZ SAYIM (getiri hesaplanmadı; yalnız işaret, zaman, veri kapıları)

Set 6: 17 bölge, ölçülebilen 17, ölçülemeyen 0 {}; pazar {"ABD": 14, "AVR": 3}; en geç 15. mum 2022-01-24; hakem sınıfı {"b": 10, "a": 7} (a = iki hakem EVET).

| Cemal | haftalık (ölçülebilen) | günlük (ölçülebilen) |
|---|---|---|
| BENZİYOR | 3 (3) | 1 (1) |
| KISMEN | 3 (3) | 4 (4) |
| BENZEMİYOR | 3 (3) | 3 (3) |

Birleşik set 1-6: 145 bölge, ölçülebilen 145, ölçülemeyen 0 {}; pazar {"ABD": 106, "AVR": 20, "BIST": 19}.

| Cemal | haftalık (ölçülebilen) | günlük (ölçülebilen) |
|---|---|---|
| BENZİYOR | 23 (23) | 17 (17) |
| KISMEN | 9 (9) | 14 (14) |
| BENZEMİYOR | 39 (39) | 43 (43) |

- Set 6'nın önceki setlerle ortak sembolü: 0 [] (bölge tekrarı yok: zaman + sembol + bölge sonu tekil, denetlendi).
- Eş sayısı (eşi < 5 / kovasız) hesapta belirlenir ve yazılır; eşsiz olay eşli tabloya girmez (GZ aynen).
- Set 6 BENZİYOR: haftalık 3, günlük 1 -> günlük BENZİYOR hücresi 'yalnız döküm'; haftalık BENZİYOR - BENZEMİYOR karşılaştırması n 3 / 3 ile (bilgi).

## Tablolar (önceden; sonuçtan sonra değişmez)

- (i) ÜÇÜNCÜ BAKIŞ = yalnız set 6: Cemal sınıfı x zaman dilimi: n, R15 ort / medyan, eş ort, eşli fark ort / medyan, artıda payı, eşinden iyi payı, +%5 / +%10 stop'tan önce payı, stop payı. +%5 haftalıkta GZ'de yoktu (haftalık hedefler +%10 / +%20): aynı dokunma kuralıyla BİLGİ olarak eklenir (d5_tum); GZ tabloları (haftalık +%10 / +%20) aynen ayrıca yazılır. BENZİYOR hücreleri (n 3 ve n 1): 'karşılaştırma yapılamaz / yalnız döküm'. 17 bölge tek tek döküm (sayfa, işaret, zaman, sembol, R15, eş ort, mum boyu %, oran).
- (ii) HAKEMİN SEÇTİKLERİ (BİLGİ): set 6'nın 17 bölgesi Cemal'in işaretinden bağımsız, zaman dilimine göre (haftalık, günlük, birlikte); karşılaştırma satırı set 5 (24, hakem v3, dokuzuncu ölçütsüz) aynı ölçülerle; ek bilgi satırı hakem sınıfı a / b.
- (iii) BİRLEŞİK = set 1-6 (145): MUM_IZI13 birleşik tablosunun aynısı (EVET / KISMEN / HAYIR / EVET+KISMEN x zaman; EVET - HAYIR ve (EVET + KISMEN) - HAYIR eşli fark farkı + permütasyon p; EVET - eş işaret çevirme p) + MUM_IZI13 birleşiğine göre değişim. Soru: iki bakıştaki yön (haftalıkta BENZİYOR eşlerin gerisinde; günlükte fark yok) üçüncüyle değişti mi: 'aynı yön' = farkın İŞARETİ; hesaplanamazsa 'karşılaştırma yapılamaz'.
- Set 1-5 satırları mum_izi13_olay.csv ile karşılaştırılır (R15, es_R15, fark, n_es): eş dışlama kümesi 145 olayla kurulduğu için eş değerleri değişebilir; değişen satır sayısı ve en büyük fark yazılır.
- OKUMA: bütün hücreler n < 30 (birleşik HAYIR hariç): etiket 'BİLGİ; ÖRNEKLEM YETERSİZ'. Eş sınırı: eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240).

## Ek tanımlar (K17_EK; sha yukarıda)

```
{
 "surum": "K17-1.0",
 "tanim": "MUM_IZI_GOZ GZ_ESIK aynen (ESIK11_SHA) + G2_EK aynen (EK13_SHA): giriş, ufuk 15 mum, stop = bölge dibi x 0,98, CETVEL2 konum eşi, tablolar, permütasyonlar, işaret çevirme",
 "set6": "MUM_IZI14_ONAY_OLCEKLI (s2-18): sayfa -> bölge mühürlü MUM_IZI14_onay_anahtar.json 'yeni_sayfa' (zaman, pazar, sembol, bolge_bas = ilk barın tarihi, bolge_son, pencere); işaret cemal_mum_izi14_onay.json (EVET / KISMEN / HAYIR); üç dosyada sayfa kümesi ve zaman aynı olmalı (değilse DUR); mum boyu / olağan / oran MUM_IZI14_onay_olcekli.json'dan aynen (yeniden hesaplanmaz)",
 "birlesik": "set 1-6 (145 bölge); eş dışlama kümesi 145 olayla kurulur; set 1-5 değerleri mum_izi13_olay.csv ile karşılaştırılır (R15, es_R15, fark, n_es): değişen satır sayısı ve en büyük mutlak fark yazılır",
 "gecit": "getirisiz ölçülebilirlik: gz_olc_bir'in kapıları aynen (giris_yok, ufuk_kesik (15. mum > 2022-12-31), giris_stop_altinda); getiri hesaplamaz; hesapta gz_olc ile birebir aynı olmalı (değilse DUR)",
 "d5_tum": "BİLGİ ek ölçü: +%5 stop'tan önce (gz_olc_bir dokunma kuralı aynen: günlük sırayla High >= giriş x 1,05 olan ilk gün, Low <= stop olan ilk günden ÖNCE; aynı gün = stop önce); günlükte GZ d5 ile aynı; haftalıkta yeni (GZ haftalık hedefleri +%10 / +%20); aynı fonksiyonla hesaplanan haftalık +%10 GZ d10 ile aynı olmalı (değilse DUR); eşler için yok",
 "hucre": "n (ölçülen), n_es, R15 ort / medyan, eş ort, eşli fark ort / medyan, artıda payı (R15 > 0), eşinden iyi payı (fark > 0; eşi olanlarda), +%5 ve +%10 stop'tan önce payı (d5_tum, d10), stop payı",
 "tablolar": {
  "ucuncu_bakis": "yalnız set 6: Cemal sınıfı (EVET / KISMEN / HAYIR) x zaman (haftalık, günlük; birlikte bilgi) k17 hücresi + GZ tabloları (gz_tablolar) + g2_evet_es; BENZİYOR hücreleri n 3 / n 1: 'karşılaştırma yapılamaz / yalnız döküm'; 17 bölgenin tek tek dökümü",
  "hakem": "BİLGİ: set 6'nın 17 bölgesi Cemal'in işaretinden bağımsız, zaman dilimine göre (haftalık, günlük, birlikte) k17 hücresi; karşılaştırma satırı set 5'in 24 bölgesi (hakem v3) aynı ölçülerle; ek bilgi: set 6 hakem sınıfı a (iki hakem EVET) / b",
  "birlesik": "set 1-6 (145): GZ gz_tablolar (MUM_IZI13 birleşik tablosunun aynısı) + g2_evet_es + k17 hücresi (eşinden iyi payı, +%5); MUM_IZI13 birleşik (mum_izi13_sonuc.json) ile fark: EVET - HAYIR eşli fark farkı ve p, EVET - eş, hücre n / R15 / eşli fark",
  "yon": "üçüncü bakış iki bakışla aynı yönde mi: her dilimde EVET - HAYIR eşli fark farkının ve EVET - eş farkının İŞARETİ (MUM_IZI13 ilk / ikinci bakış ile); hesaplanamazsa 'karşılaştırma yapılamaz'"
 },
 "etiket": "BİLGİ; ÖRNEKLEM YETERSİZ (bütün hücreler n < 30)",
 "es_siniri": "eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240): aynı gün aynı kova konum eşi",
 "pdf": "kapak: set 6 düz dil özet tablo (Cemal sınıfı x zaman) + hakem ve birleşik birer satır; sonra set 6'nın 17 bölgesinin HEPSİ: BENZİYOR, KISMEN, BENZEMİYOR (her sınıfta önce haftalık sonra günlük, bölge sonu sırası); her sayfada işaret, hisse, tarih, öncesi 15 mum + bölge + sonrası 30 mum, giriş / stop / 15. mum çizgileri, sağda girişe göre yüzde ekseni (MUM_IZI_HAKEM adım kuralı), R15, eş ortalaması, en yüksek / en derin, R30, stop, mum boyu satırı (olcekli json)"
}
```

## KONTROL LİSTESİ (`python IZ_KARNE.py kontrol`; K8: set 6 hücreleri n < 30)

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü aynı kova (CETVEL2 v2.2 konum eşi) aynı takvim aralığı aynı stop geometrisi (GZ aynen); eş dışlama 145 olayla; sınır: eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240) |
| K2 | geleceğe bakma | EVET | Cemal set 6'yı sonrasını görmeden işaretledi (ölçekli sayfa bölge sonunda kesik; MUM_IZI_HAKEM yalnız t'ye kadar bar); işaret dosyası commit 0c6dfec, bu ön kayıt set 6 getirilerinden önce; giriş bölgeden SONRAKİ barın açılışı; veri <= 2022-12-31 + KASA kapısı |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar (H > L, V > 0); haftalık barlar tamamlanmış ISO haftaları (MH / MV aynen) |
| K4 | tekilleştirme | EVET | 145 tekil bölge (zaman + sembol + bölge sonu; k17_ornek DUR); setler arası sembol tekrarı sayılıp yazılır |
| K5 | giriş fiyatı | EVET | giriş = bölgeden sonraki ilk geçerli barın açılışı (haftalıkta sonraki haftanın ilk günü); giriş <= stop olay ölçülmez (sayısı yazılır) |
| K6 | veri birimi | EVET | MI bölünme düzeltmeli fiyatlar (GZ aynen); getiriler oransal; ABD USD, AVR yerel para; pazarlar arası karşılaştırma eşli farkla |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç bilgi, kasa açılmaz |
| K8 | örneklem ve dönem | EVET | set 6 hücreleri n 1-4, birleşik hücreler n < 30 (HAYIR hariç): etiket 'BİLGİ; ÖRNEKLEM YETERSİZ'; n < 2 'karşılaştırma yapılamaz'; 17 bölge tek tek listeli; tek dönem (<= 2022), BH yok (karar yok) |
| K9 | ön kayıt | EVET | MUM_IZI17_ON_KAYIT.md: KOD17 / EK17 / ESIK11 / EK13 / işaret / anahtar / ölçekli / olay13 / sonuç13 sha + getirisiz sayımlar; set 6 getirilerinden önce commit; k17_kapi sha + commit + temiz ağaç + IZ_KARNE.ik_kontrol_kapisi |
| K10 | ayrıştırma | EVET | işaret şeması GZ.gz_isaret_oku (bilinmeyen değer DUR); üç set 6 dosyasında sayfa kümesi ve zaman aynı (DUR); bölge başı veriden yeniden hesaplanıp anahtarla denetlenir (GZ K10) |
| K11 | yeniden üretim | EVET | getirisiz geçit hesapta gz_olc ile birebir (DUR); haftalık +%10 k17 dokunma fonksiyonuyla GZ d10'a eşit (DUR); set 1-5 satırları mum_izi13_olay.csv ile karşılaştırılır; tablo sayılarından >= 2 hücre olay csv'sinden bağımsız kodla yeniden üretilir (rapor öncesi) |
| K12 | ifade | EVET | 'iz / tuttu / anlamlı' sözü yok; sayı ile yorum ayrı; n < 30 'örneklem yetersiz' |
| K13 | süreç | EVET | çakışma kapısı korunur; çalışan fonksiyonlar değişmez (test_mum_izi17 ast karşılaştırması); yasak defter / mühürlü dosyalara dokunulmaz; yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez |

## SAPMA

(ön kayıt anında yok)
