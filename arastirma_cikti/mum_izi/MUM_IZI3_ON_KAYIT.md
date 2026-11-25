# MUM_IZI3 ÖN KAYIT (2026-11-25T10:30:00Z)

Haftalık tarama ve sonrası bu dosya commit edildikten SONRA koşar (`mh_kapi`). Bu ana kadar haftalık barda hiçbir pencere puanlanmadı; yalnız kesikli günlük kopyalar hazırlandı (getirisiz).

## Mühürler

KOD3_SHA: f637e98a9022153093079fcebd5f851ea1368cf56f5fbe75bc01b0b12fcf107b
ESIK3_SHA: 2b4074791bc09a6c47fa4c73820d0cd5ddaefef28b542b9bc823e1bb77f7783b
MI_KOD_SHA: 370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9
SABLON_SHA: 86ff7603dea2602d10c4710f362b0d7185c9dc4d95ade7b580f8eb7240cdb612
SENTETIK_SHA: e49f24acc9cfa21554560997b61748f3f0d5963c6d8561aaa46e4b8b1d2c5b77
VERI3_SHA: 4c3d262449bba1791ea7e22772e49695cbe38a6831b343c948d508cacb204ebd

- MUM_IZI_HAFTALIK.py commit'i: 8e66f8b4d4014082e0a98cf7fe51c9a450ca4283 2026-11-25T10:30:00+00:00
- Veri: ABD tam 4450 hisse (2000-01-03..2022-12-30), P1 3034; AVR tam 572, P1 515; BIST 475 (2015-06-01..); KASA kapısı kesik 2022-12-31

## Tanımlar (MH_ESIK; sha yukarıda; sonuca göre DEĞİŞMEZ)

```
{
 "surum": "MH-1.0",
 "hafta": {
  "tanim": "ISO takvim haftası; O = haftanın ilk geçerli gününün açılışı, H = en yüksek, L = en düşük, C = son geçerli günün kapanışı, V = toplam; tarih = haftanın son geçerli günü. Geçerli günü olmayan hafta yok. Günlük girdi MI.mi_veri temiz barları (H > L, V > 0) olduğu için haftalık H > L her zaman sağlanır (denetlenir).",
  "tamamlanmis": "haftanın cuması <= veri sonu (2022-12-30, cuma): kesikteki son hafta tam; yarım hafta (cuması veri sonundan sonra) atılır",
  "bant": "Bollinger (20, 2) ve SMA20 haftalık kapanışlardan, yalnız o haftaya kadar (MI.mi_bant)"
 },
 "sablon": "MUM_IZI tam (L 20; pencere 16-24 hafta) ve tepesiz (L 17; 14-20 hafta) şablonu + kalibrasyon (tau, sd) AYNEN; S = MI.mi_tara_seri",
 "esik": {
  "tam": 0.59,
  "tepesiz": 0.56
 },
 "tam_uyan_ek": 0.1,
 "seviye": "ESIK: S >= eşik; TAM_UYAN: S >= eşik + 0,10. Her seviyede aynı hissede eşiği geçen hafta sonları 15 hafta tekil (ilk kalır) -> iki ayrı olay listesi",
 "veri": {
  "tam": [
   "2000-01-01",
   "2022-12-31"
  ],
  "p1": [
   "2000-01-01",
   "2016-12-31"
  ],
  "p2": "MUM_IZI açık kopya (2015-01-01..2022-12-30)",
  "bist": "V_BIST (2015-06..), yalnız p2"
 },
 "hucre": {
  "h0107": [
   "2001-01-01",
   "2007-12-31"
  ],
  "h0815": [
   "2008-01-01",
   "2015-12-31"
  ],
  "h1622": [
   "2016-01-01",
   "2022-12-31"
  ],
  "tanim": "bölge sonu t (son haftanın son geçerli günü); h0107 + h0815 = AYRI EVREN (günlük taramada kullanılmadı), h1622 = KARŞILAŞTIRMA",
  "panel": "h0107 / h0815 olaylarının sonrası p1 panelinde (2000-2016), h1622 p2 panelinde (2015-2022)"
 },
 "evren": {
  "ABD": "TEZGAH2 P2 (KART_TUR2.k2_panel + k2_P + _k2_oc tekil 1; giriş günü d'de; d'nin bilgisi t'ye kadar)",
  "AVR": "aynı",
  "BIST": "V_BIST, P2 yok (bilgi)"
 },
 "sonrasi": {
  "giris": "bölgenin son haftasından sonraki ilk geçerli günün açılışı (E0)",
  "ufuk_hafta": 15,
  "bilgi_hafta": 30,
  "R15h": "hissenin bölgeden sonraki 15. haftalık barının kapanışı / E0 - 1 (son günü <= 2022-12-30 olmalı; değilse ölçülmez, sayısı yazılır)",
  "max_min": "E0 günü .. 15. haftanın son günü arasında günlük en yüksek High / E0 - 1 ve en düşük Low / E0 - 1",
  "dokunma": "hedef +%5 / +%10 / +%20: günlük sırayla High >= E0 (1 + x) olan ilk gün, stop gününden ÖNCE (aynı gün = stop önce); stop = bölgenin en düşük Low'u x 0,98; E0 <= stop ise olay ölçülmez; stop payı = ufukta Low <= stop olan gün var",
  "hedef": [
   0.05,
   0.1,
   0.2
  ],
  "stop_carpan": 0.98
 },
 "es": {
  "tanim": "aynı giriş günü d, aynı kova (CETVEL2 v2.2 panel KV: ATRP tercili x likidite üçlüsü x F15 çeyreği; KV >= 0 havuz), aynı şablon ve seviyede o gün olayı olan hisseler dışı, d'de geçerli açılış; ölçüler AYNI takvim aralığında: R = olayın 15. hafta son günündeki (ya da öncesindeki son geçerli) kapanış / d açılışı - 1; max / min aynı satırlar; dokunma: eşin stop'u = olayın bölge takvim aralığında eşin en düşük Low'u x 0,98",
  "min": 5,
  "fark": "R15h - eş ortalaması",
  "sira": "(olaydan küçük eş + 0,5 eşit) / eş sayısı"
 },
 "hucre_ist": "C2.c2_hucre(R15h, eş ort, SIRA, giriş, '?', egri yok -> güç şartı yok, perm 10.000) : n, ort / medyan FARK, ay kümeli boot %95, SIRA, L3O, p; ayrıca olay / eş ortalama ve medyan R15h, max, min, dokunma ve stop payları",
 "plasebo": {
  "tohum_sayi": 200,
  "kok": 2522,
  "tanim": "her ölçülen olayın yerine aynı gün aynı kovadan rastgele bir eş (dışlanmamış) -> onun R15h'si ve öteki eşlerin ortalaması -> aynı c2_hucre (perm yok); 200 tohumda ort FARK dağılımı ve TUTAR (+ / -) payları = şans tabanı"
 },
 "etiket": "c2 hükmü (TUTAR + / TUTAR - / TUTMADI); n < 30 'örneklem yetersiz'; BH q 0,10 aile = (tam, tepesiz) x (ESIK, TAM_UYAN) x hücreler (pazar x dönem, n >= 30); 'iz' sözü yok (ikinci bakış, bilgi); K7 evren bugün yaşayanlar -> 2001-15 yukarı yanlı, olaya ve eşe aynı",
 "pdf": {
  "secim": "tam şablon, ESIK seviyesi, ABD / AVR'de P2'den geçen olaylar; S büyükten küçüğe; aynı hisse en çok bir kez (sayfa listesinde): AYRI EVREN (h0107 + h0815) ABD 10 + AVR 6; h1622 ABD 6 + AVR 4 + BIST 6; sonra bütün eşleşmelerden (iki şablon, iki seviye, bütün pazarlar; daha önce seçilen hisseler hariç) rastgele 8 (tohum 2523)",
  "sayfa": "sayfa başına tek haftalık mum grafiği (dikey A4): bölgeden önce 40 hafta, bölge kutulu, sonra 30 hafta (veri kesiği aşılmaz), Bollinger 20 + SMA20; başlıkta hisse + tarih açık, S, R15h ve eş ortalaması, en yüksek / en derin",
  "tohum": 2523,
  "adet": {
   "ayri_ABD": 10,
   "ayri_AVR": 6,
   "h1622_ABD": 6,
   "h1622_AVR": 4,
   "h1622_BIST": 6,
   "rastgele": 8
  },
  "once": 40,
  "sonra": 30
 },
 "bh_q": 0.1
}
```

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü, aynı CETVEL2 v2.2 kovası (>= 5), aynı gün kalıp olayı olan hisseler dışı, AYNI takvim aralığında aynı ölçüler (R15h, max, min, dokunma; eşin stop'u kendi bölge-aralığı dibi x 0,98); plasebo şans tabanı 200 tohum SAYIYLA (aynı gün aynı kova rastgele eş) |
| K2 | geleceğe bakma | EVET | haftalık bar yalnız o haftaya kadarki günlerden; bant haftalık kapanışla t'ye kadar; yarım hafta atılır; mh_prefix: 30 olayda günlük veri t'de kesilince S(t) aynı (assert); veri <= 2022-12-31 assert + KASA.kasa_kapisi; sonrası penceresi kesiği aşan olay ölçülmez |
| K3 | geçerli bar | EVET | günlük girdi MI.mi_veri geçerli bar süzgeci (H > L, V > 0); haftalık H > L denetlenir; eş d'de geçerli açılış |
| K4 | tekilleştirme | EVET | aynı hissede 15 hafta tekil (ilk kalır), seviye başına ayrı liste; plasebo / eş günlük panelde |
| K5 | giriş fiyatı | EVET | giriş = bölgenin son haftasından sonraki ilk geçerli günün AÇILIŞI; eşler aynı gün açılışı |
| K6 | veri birimi | EVET | TEZGAH2 bölünme düzeltmeli fiyat (yfinance auto_adjust); S ölçek bağımsız; AVR yerel para (oran ölçüleri); BIST bilgi |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler: 2001-15 AYRI EVREN'de hayatta kalma yanlılığı büyük (batanlar yok) -> sonrası yukarı yanlı; olaya ve eşe aynı biner; raporda yazılı |
| K8 | örneklem ve dönem | EVET | hücreler pazar x dönem (h0107, h0815, h1622) x şablon x seviye; n < 30 'örneklem yetersiz'; BH q 0,10; iki seviye ve iki dönem ayrı satır; ikinci bakış -> bilgi |
| K9 | ön kayıt | EVET | MUM_IZI3_ON_KAYIT.md: KOD3_SHA, ESIK3_SHA, MI_KOD_SHA, şablon / sentetik sha, veri sha'ları, PDF seçim kuralı ve tohumlar; ön kayıt commit'i taramadan önce; mh_kapi kontrol + sha + git |
| K10 | ayrıştırma | EVET | mh_elle: 3 rastgele olayın haftalık barı günlük veriden düz döngüyle yeniden kurulur (O / H / L / C / V birebir) ve raporda yazılır |
| K11 | yeniden üretim | EVET | mh_yeniden: 2 hücre olay satır dosyasından düz pandas (n, ort FARK, +%10 payı); 5 olayın R15h'si ve eş ortalaması ham günlük veriden düz döngüyle |
| K12 | ifade | EVET | 'iz' sözü kullanılmaz; sonuç bilgi; c2 hükmü ve BH yazılır; sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_mh); MUM_IZI.py / defterler / UC_IZ2 dosyaları değişmez; yalnız kendi yolları git add |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; kalıbın haftalık mumda gösterimi |

## SAPMA

(ön kayıt anında yok)
## Notlar (taramadan önce)

- Kuru koşu (sentetik 70 hisse / pazar, 2000-2022): hattın bütün dalları çalıştı (tarama, prefix 3 x 30 fark 0, P2, eş, hücre, PDF, rapor); sonuçları gerçek değildir, kullanılmaz.
- Eşikler MUM_IZI sentetik json'undan okunur ve MH_ESIK ile karşılaştırılır (test_mum_izi3.test_esik_ayni); haftalık için yeniden ayar yok.
- İş tanımında '33 ölçü' yazıyor; şablon ve S, MUM_IZI'deki 35 ölçünün 12'lik alt kümesini ve dizi / bant bileşenlerini AYNEN kullanır (değişiklik yok).
- K7: AYRI EVREN (2001-15) bugün yaşayan hisselerden kurulduğu için o dönemde batanlar yok: sonrası yukarı yanlı (olaya ve eşe aynı biner).
