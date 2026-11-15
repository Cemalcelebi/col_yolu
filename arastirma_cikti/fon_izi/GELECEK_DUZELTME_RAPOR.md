# FON_IZI geleceğe bakma düzeltmesi: seri uzunluğu şartı karar günü konumuna alındı (rapor)

Yapan: alt ajan, 2026-11-15. İş tanımı: `arastirma_cikti/fon_izi/GELECEK_DUZELTME_IS_TANIMI.md` (git 9f0aa08, 10:06:05).
Eski kod: `git show 9b30436:FON_IZI.py` (sha256 ea0cc19f…ac7b). FON_IZI.py ve test_fon_izi.py 9b30436 ile şu anki HEAD (1860872) arasında değişmedi.

## 1. ÖZET
- 8 tarayıcıda (fi_k4_olaylar, fi_k4b_hacim_olaylar, fi_k6_evren, fi_k13_tara, fi_k14_esli, fi_k17_tara, fi_k23_parmak, fi_k24_tara) hisse atlama şartı artık serinin toplam uzunluğuna değil, karar günü konumuna bakıyor: t >= N-1 (N = 400 / 400 / 400 / 400 / 400 / 400 / L+200 / 200). Eşikler değişmedi.
- Testler: test_fon_izi 62/62 → 63/63 OK. Yeni test 63 (önek değişmezliği) eski kodda 8 fonksiyonun 8'inde KIRMIZI, yeni kodda YEŞİL.
- Gerçek veri (V_BIST 581, V_ABD 1.411 hisse, 31.08.2026 kesik): K24 kural sinyali BIST 3.114 → 2.905 (-209), ABD 6.802 → 6.287 (-515); K24 kural+eşli toplam -1.988. K13 -2, K14 eşli -205, K17 -102, K23 parmak (L=15) -398.400 pencere.
- Yeni sonuç eski sonucun tam alt kümesi DEĞİL (K13 ABD, K14, K17, K24'te 0-157 yeni satır): t < N-1 günü artık sinyal sayılmadığı için 'aynı hissede 60 bar içinde tek' ve 'aynı dip' durumlarına da girmiyor. Bu, iş tanımı tablosundaki 'döngü alt sınırı max(b1, 320, 399)' maddesinin doğrudan sonucu (SAPMA ve HATA bölümleri).
- İki dış test (test_intem_ileri, test_k24_yeniden) eski hatanın VAR OLDUĞUNU sınayan 'SAPMA-1 gerekçesi' bölümleri yüzünden çöküyor; bu iki dosya bu işin yetkisi dışında (HATA 2).

## 2. DEĞİŞEN SATIRLAR
Satır numaraları: eski = 9b30436, yeni = çalışma ağacı.

| # | Fonksiyon | Eski satır → yeni satır | Eski | Yeni |
|---|---|---|---|---|
| 1 | fi_k4_olaylar | 426-427 → 426 | `if len(d) < 400: continue` | silindi; `ok = (...).to_numpy() & (np.arange(len(d)) >= 400 - 1)` (tekrar durumundan önce) |
| 2 | fi_k4b_hacim_olaylar | 466-467 → 466-467 | `if len(d) < 400: continue` | silindi; olay döngüsünün başında `if i < 400 - 1: continue` (tekrar durumundan önce) |
| 3 | fi_k6_evren | 825-826, 831 → 827 | `if len(d) < 400: continue` | silindi; `gecerli = (d.index >= bas) & (np.arange(len(d)) >= 400 - 1)` (taban ve bütün sinyaller, tekrar süzgecinden önce: K1 taban ile sinyal aynı kural) |
| 4 | fi_k13_tara | 2528, 2535 → 2524, 2531 | `if n < 400: continue`; `range(max(b1, 320), n)` | `if n < b1 - b0 + 1: continue` (teknik: sliding_window_view penceresi kurulamaz); `range(max(b1, 320, 400 - 1), n)` |
| 5 | fi_k14_esli | 2845-2846, 2851 → 2845 | `if n < 400: continue`; `range(max(b1, 320), n)` | şart silindi; `range(max(b1, 320, 400 - 1), n)` (K13 ile aynı konum kuralı, K1) |
| 6 | fi_k17_tara | 3329, 3336 → 3323, 3330 | `if n < 400: continue`; `range(max(b1, 320), n)` | `if n < b1 - b0 + 1: continue` (teknik); `range(max(b1, 320, 400 - 1), n)` |
| 7 | fi_k23_parmak | 4626-4628, (yeni 4671) | `def fi_k23_parmak(d, L)`; `if n < L + 200: return boş` | `def fi_k23_parmak(d, L, gecmis=None)`; `if n < L: return boş` (teknik: pencere kurulamaz); dönüşten önce `F = F[F["i"] >= (L + 200 if gecmis is None else gecmis) - 1]` |
| 7b | fon_izi_k23 hedef | 4704 → 4701 | `fi_k23_parmak(d, L)` | `fi_k23_parmak(d, L, gecmis=L)` (bölge hedefi; bkz. SAPMA 2) |
| 7c | fi_k26_ortak hedef | 5470 → 5467 | `fi_k23_parmak(d, L)` | `fi_k23_parmak(d, L, gecmis=L)` (aynı gerekçe) |
| 8 | fi_k24_tara | 4777, 4786 → 4774, 4783 | `if n < 200: return boş`; `for t in np.flatnonzero(seri == k)` | `if n < 21: return boş` (teknik: SMA20 kurulamaz); `for t in np.flatnonzero((seri == k) & (np.arange(n) >= 200 - 1))` |
| - | FI_SURUM | 81 | v1.39 | `FON_IZI v1.40 (2026-11-15, geleceğe bakma düzeltmesi: ...)` + eski metin aynen sonda |

Teknik alt sınırlar (yalnız pencere kurulamadığında boş dönüş; hiçbiri karar günü konumundan sıkı değil, yani geleceğe bakmaz): K13 / K17 `n < b1 - b0 + 1` (51 / 96), K23 `n < L`, K24 `n < 21`. K4 / K4b / K6 / K14 için gerekmedi (kısa seride rolling NaN, döngü boş). Ayrı denetim: 5 / 30 / 300 barlık serilerde 8 fonksiyonun hiçbiri hata ya da 'atlandi' uyarısı vermedi; satır yalnız fi_k23_parmak'ta 300 barda (86 pencere, konum >= 214).
Her değişen satırda yorum: `# 15 Kas: toplam uzunluk değil karar günü konumu (geleceğe bakma, H satırı 14 Kas)`. Satır 1110 (`_fi_metne`) dokunulmadı. Çakışma kapısı yerinde (test 5 geçiyor). Mevcut try/except blokları korundu.

## 3. SAPMA
1. Davranış değişikliği (beklenen): t < N-1 günündeki sinyal / ölçü artık üretilmez; uzun serilerin ilk N-1 barındaki satırlar düşer (gerçek veride hepsi 2015-2016 başı). Kısa seriden (n < N) zaten satır çıkmaz (karar günü yok).
2. fi_k23_parmak'a `gecmis` parametresi eklendi ve iki hedef çağrısı (fon_izi_k23 bölge hedefleri, fi_k26_ortak örnekleri) `gecmis=L` ile çağrıldı. Gerekçe: iş tanımındaki 'çıktı satırları e >= L+199'a süzülür' kuralı tek başına uygulansaydı BINBN 21.01.2025 hedefi (FI_K23 bölge 3 ve FI_K26 örneği; seride konum 70 < 214) `F.loc[son_g]` ile KeyError verirdi (fon_izi_k23 ve fi_k26_ortak çökerdi). Hedef penceresi Cemal'in işaretlediği tek penceredir, evren taraması değildir; `gecmis=L` ile ölçüler yalnız t ve öncesinden gelir (önek değişmez) ve eski kodla birebir aynıdır: gerçek veride 4 bölge hedefi (MANAS 1, 2, S; BINBN 3) eski ve yeni kodda np.allclose = True. K44 (INTEM, konum 2.890) ve BBIO hedefleri varsayılanla zaten ölçülüyor, dokunulmadı.
3. Tekrar / aynı dip durumu: iş tanımı tablosu (döngü alt sınırı max(b1, 320, 399)) uygulandı, yani t < N-1 günü sinyal adayı sayılmaz ve 'son_olay' / 'gorulen' / 'son' durumlarına da girmez. Aynı kural K24, K4, K4b, K6'da da tutarlı uygulandı. Sonuç: yeni çıktı eski çıktının 't >= N-1' süzülmüş hâliyle birebir aynı değil; eskiden t < N-1'deki bir sinyalin bastırdığı sonraki sinyal artık çıkabiliyor (ve zincirleme olarak sonraki bir eski sinyal bastırılabiliyor). Sayılar bölüm 6'da. Bu yolun seçilme nedeni: (a) iş tanımı tablosunun harfi; (b) K64 sözleşmesi ('tekrar = 0 çıktısından 60 gün tekilleştirme = FI_K24 tekrar = 60 çıktısı') yalnız bu yolla tutuyor: önce denediğim 'durumu koru, yalnız satırı yazma' sürümünde test_k64 '3) tekil K24 olayları fi_k24_tara çıktısıyla aynı değil' ile KIRMIZI oldu, bu sürümde 15/15 geçiyor.
4. Eski karar kayıtlarına etki: yok. Eski çalışmaların (Ç75-Ç78, Ç96 / Ç113 / Ç118, Ç124 ve K24_YENIDEN / DIP_COL_AYRIM / INTEM_ILERI) kararları değiştirilmedi, yeniden koşulmadı; getiri, cetvel, karar ölçülmedi. Not: K24_YENIDEN (Ç178) ve DIP_COL_AYRIM kendi SAPMA-1 süzgeçlerini fi_k24_tara / fi_k13_tara / fi_k17_tara ÇIKTISINA sonradan uyguluyordu; bu modüller yeni FON_IZI ile yeniden koşulursa sinyal kümesi bölüm 6'daki 'yeni olup eskide olmayan' kadar (K24 kural BIST 3 / ABD 18, K17 BIST 6 / ABD 21) farklı olur. INTEM_ILERI ii_pencereler (fi_k23_parmak + i >= L+199) birebir aynı kalır (K23 satırında yeni = eski[t >= N-1], fark 0).

## 4. KONTROL LİSTESİ
| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | Eşli kutu (fi_k14_esli) K13 ile aynı konum kuralı t >= 399 (döngü alt sınırı aynı); K6 taban (_TABAN) sinyallerle aynı `gecerli` maskesi; K24 kural ve eşli aynı döngü şartı. Getiri / eş portföy ölçümü bu işte yok. |
| K2 | geleceğe bakma | EVET | Test 63 (T1): 8 fonksiyon, sentetik 660 / 602 bar, kesikler 390 / 420 / 470 (+K24 195 / 220, K23 205, K4/K4b 640); yeni kod 63/63 OK, eski kod 8/8 fonksiyonda kırmızı (bölüm 5 çıktısı). |
| K3 | geçerli bar | UYGULANMAZ | Bar geçerlilik kuralları (H>L, V>0) bu işte değiştirilmedi; yalnız konum şartı değişti. |
| K4 | tekilleştirme | EVET | 60 bar / aynı dip / g_tekrar kuralları değişmedi; t < N-1 adayları tekilleştirmeye girmez (SAPMA 3); test_k64 '60 gün tekil = tekrar 60 çıktısı' 15/15 geçti. |
| K5 | giriş fiyatı | UYGULANMAZ | Giriş / sonuç mekaniği değişmedi; sonuç sütunları (yon60, yon20, r120, x2_once, r60...) karşılaştırma dışı. |
| K6 | veri birimi | UYGULANMAZ | Fiyat verisi değiştirilmedi; sayımda V_BIST / V_ABD paket verisi (manifest sha256 ile açıldı) olduğu gibi. |
| K7 | hayatta kalma | UYGULANMAZ | Getiri ölçümü yok; sayım V_ABD 1.411 hisse (k34 batanları yok) ile yapıldı, raporda yazılı (bölüm 6, 1.430 kıyası). |
| K8 | örneklem ve dönem | UYGULANMAZ | Bulgu / iz iddiası yok; yalnız sinyal sayımı. |
| K9 | ön kayıt | EVET | İş tanımı git 9f0aa08 10:06:05; ilk kod değişikliği ondan sonra (veri açma logu 10:06:05, ilk test koşusu 10:07:09); eşikler (400, L+200, 200) değişmedi. |
| K10 | ayrıştırma | UYGULANMAZ | Ham metin ayrıştırması yok. |
| K11 | yeniden üretim | EVET | Sayım iki ayrı süreçte (eski kod / yeni kod) yapıldı, kıyas üçüncü betikle satır anahtarlarından (sembol, tarih, konum); K23 hedefleri eski / yeni np.allclose. |
| K12 | ifade | EVET | 'Düşen sinyal' sayıları fiyat / getiri yorumu olmadan verildi; iz / emare sözü yok. |
| K13 | süreç | EVET | Çakışma kapısı korundu (test 5); yasak dosyalar (IZ_DEFTERI, IZ_KARNE, CLAUDE, COL_OZET, ONERI_DEFTERI) değişmedi; commit / stash yok; e-posta / anahtar taraması diff'te 0 eşleşme. Colab: kod değişti, çalışma zamanı yeniden başlatılmalı. |
| K14 | boyut (gerçek para) | UYGULANMAZ | Öneri / gerçek para işi değil. |

## 5. TEST
T1 tasarımı (test_fon_izi.py, test 63, satır 790'dan itibaren):
- `seri63` (660 bar, 2016-01-04'ten): çöküş + toparlanma (K24 olayı t ≈ 193 < 199), istikrarlı yükseliş (K4 / K4b olayı t ≈ 249-289 < 399), çöküş + küçük mumlu taban (K13 / K14 olayı t ≈ 348-349 < 399), ikinci çöküş + taban (K13 olayı t ≈ 449), yükseliş (K4 / K4b olayları t ≈ 499-576), gürültülü kuyruk. `seri63b` (602 bar): test 24 deseninin iki kopyası (K17 olayları t ≈ 339 ve 445).
- Her fonksiyon için tam seri sonucu ile `d.iloc[:T]` önek sonucu, T-1 günü ve öncesi satırlar (K4 / K4b'de sonucu önekte dolan satırlar: T-1-ufuk, ufuk = 60) sonuç sütunları hariç birebir karşılaştırılır. Kesikler: genel 390 / 420 / 470; K24 ek 195 / 220; K23 (L=15) ek 205; K4 / K4b ek 640. K6 (toplam sayaç döndürür): `donem_siniri` = kesik günü yapılır, '2016-21' satırlarının sinyal başına n'i tam seri ile önekte aynı olmalı. Her fonksiyonda en az bir satırın karşılaştırıldığı ayrıca denetlenir (boş test geçmez).
- Uygulanamayan fonksiyon yok (8/8).

T2 (eski kod KIRMIZI, ayrı süreç): yeni test_fon_izi.py + `git show HEAD:FON_IZI.py` aynı geçici dizinde, `PYTHONPATH=repo` (IZ_KARNE için), `python test_fon_izi.py` (çıkış kodu 1):
```
HATA:
 - 63) önek değişmezliği (geleceğe bakma) bozuk: fi_k13_tara T=390: tam seri 1 satır, önek 0 satır; fi_k14_esli T=390: tam seri 1 satır, önek 0 satır; fi_k17_tara T=390: tam seri 1 satır, önek 0 satır; fi_k24_tara T=195: tam seri 1 satır, önek 0 satır; fi_k23_parmak T=205: tam seri 191 satır, önek 0 satır; fi_k4_olaylar T=390: tam seri 1 satır, önek 0 satır; fi_k4b_hacim_olaylar T=390: tam seri 3 satır, önek 0 satır; fi_k6_evren T=390: tam seri 210 sinyal günü, önek 0
```
Eski kodla 62 eski testin hepsi geçiyor; kırmızı olan yalnız 63. Yeni kod (repo kökünde, çıkış kodu 0):
```
test_fon_izi: 63/63 OK
```
Test 30 (d30, 300 bar, t=226) yeni şartla geçiyor (226 >= 214).

T3 (FON_IZI'yi içe alan / kullanan bütün testler, yeni kod):

| Test | Sonuç | Not |
|---|---|---|
| test_fon_izi.py | 63/63 OK | |
| test_bofa_izi.py | geçti (19 bölüm) | |
| test_dip_col_ayrim.py | 11 test GEÇTİ | |
| test_k58.py | 11/11 | |
| test_k62.py | 13/13 | |
| test_k62b.py | 12/12 | fi_k24_tara dolaylı |
| test_k64.py | 15/15 | fi_k24_tara dolaylı (SAPMA 3) |
| test_k66.py | 12/12 | dolaylı |
| test_k67.py | 17/17 | |
| test_genis_kesit.py | geçti | fi_k24_tara dolaylı |
| test_ortak_cetvel.py | 14/14 | |
| test_vdyt.py / test_vdyt2.py / test_vdyt2b.py / test_vdyt_grafik.py | 14/14, 16/16, geçti, 11/11 | |
| test_sessiz_ml.py | KOŞMADI | `lightgbm` kurulu değil (eski kodda da aynı); VERİ / BAĞIMLILIK YOK |
| test_intem_ileri.py | ÇÖKTÜ (IndexError, bölüm 3) | HEAD kopyasında 10/10. Bölüm 3 'SAPMA-1 gerekçesi' fi_k23_parmak tam seride L+100 konumlu pencere bekliyor (eski hata). Bu bölüm atlanınca (yalnız geçici kopyada) 10/10 GEÇTİ, `sapma1_erken: 0`. HATA 2. |
| test_k24_yeniden.py | ÇÖKTÜ (TypeError, bölüm 3) | HEAD kopyasında 10/10. Bölüm 2 'SAPMA-1 örneği yok (t < 199 sinyali beklenirdi)' ve bölüm 3 gerekçe örneği eski hatanın varlığını sınıyor. Bölüm 3 atlanınca yalnız bu gerekçe satırı kırmızı; 'ky_tara = FON_IZI kural satırları' eşitliği tutuyor. HATA 2. |

Toplam sayaç: test_fon_izi 62/62 → 63/63.

## 6. GERÇEK VERİ SAYIMI
Veri: islenmis-veri dalı `veri/` (git archive ile geçici dizine, `python FON_IZI.py vpac` ile açıldı; dal değişmedi). V_BIST 581 hisse (1 tanesi < 400 bar), V_ABD 1.411 hisse (1 tanesi < 400 bar). Kriz kuralı: her seri 31.08.2026'da kesildi. Eşikler: FI_K13_ESIK, FI_K17_ESIK, FI_K24, fi_k23_parmak L=15; fi_k14_esli K13 olaylarıyla. Eski ve yeni kod ayrı süreçlerde; anahtar (sembol, tarih).

| Fonksiyon | Pazar | Eski n | Yeni n | Düşen n | Düşen % | Eskide t < N-1 | Yeni = eski[t >= N-1] | Yeni olup eskide olmayan | Eskinin t >= N-1 satırı olup yenide olmayan |
|---|---|---|---|---|---|---|---|---|---|
| fi_k13_tara | BIST | 178 | 178 | 0 | 0,0 | 0 | evet | 0 | 0 |
| fi_k13_tara | ABD | 158 | 156 | 2 | 1,3 | 4 | hayır | 2 | 0 |
| fi_k14_esli | BIST | 1.512 | 1.466 | 46 | 3,0 | 47 | hayır | 1 | 0 |
| fi_k14_esli | ABD | 4.479 | 4.320 | 159 | 3,5 | 172 | hayır | 14 | 1 |
| fi_k17_tara | BIST | 731 | 710 | 21 | 2,9 | 27 | hayır | 6 | 0 |
| fi_k17_tara | ABD | 2.413 | 2.332 | 81 | 3,4 | 102 | hayır | 21 | 0 |
| fi_k24_tara kural | BIST | 3.114 | 2.905 | 209 | 6,7 | 211 | hayır | 3 | 1 |
| fi_k24_tara kural | ABD | 6.802 | 6.287 | 515 | 7,6 | 532 | hayır | 18 | 1 |
| fi_k24_tara eşli | BIST | 5.543 | 5.238 | 305 | 5,5 | 333 | hayır | 39 | 11 |
| fi_k24_tara eşli | ABD | 11.707 | 10.748 | 959 | 8,2 | 1.061 | hayır | 157 | 55 |
| fi_k23_parmak L=15 | BIST | 1.242.677 | 1.126.477 | 116.200 | 9,4 | 116.200 | evet | 0 | 0 |
| fi_k23_parmak L=15 | ABD | 3.363.147 | 3.080.947 | 282.200 | 8,4 | 282.200 | evet | 0 | 0 |

- Yeni çıktıda en küçük konum: K13 / K14 / K17 399, K24 199, K23 214 (= N-1). Hiçbir hissede hata / atlama yok.
- Beklenti 'yeni <= eski her hücrede': sayı olarak TUTTU (12/12 hücrede yeni n <= eski n). 'Alt küme': K13 BIST ve K23'te tuttu, öteki 9 hücrede TUTMADI (yeni satır 1-157; SAPMA 3, HATA 1).
- Beklenti 'K24 düşen ~1.430': bu sayımda K24 kural düşen BIST 209 + ABD 515 = 724 (kural+eşli 1.988). 1.430'un kaynağı K24_YENIDEN_RAPOR 'SAPMA-1 düşen' (BIST 214 + ABD 1.156 + AVR 60; yalnız kural). BIST yakın (214 / 211: veri OC temiz veri ile V_BIST farkı). ABD farkı evrenden: K24_YENIDEN ABD 2.876 hisse (k34 batanları dahil), burada V_ABD 1.411; AVR burada sayılmadı. Fark veri evreninden, kural farkından değil.
- K4 / K4b / K6 gerçek veride sayılmadı (iş tanımı istemiyordu; sentetik T1 kapsıyor).

## 7. HATA
1. İş tanımı iç çelişkisi: tablo K13 / K17 / K14 için 'döngü alt sınırı max(b1, 320, 399)' diyor (t < 399 günü aynı dip / 60 bar durumuna girmez), bölüm 2 ise 'yeni kod eski kodun ALT KÜMESİNİ verir' ve K24 için 'K24_YENIDEN satır 205 ile birebir aynı anlam' (K24_YENIDEN, eski çıktıyı SONRADAN süzüyordu; durum t < 199 sinyallerini içeriyordu). İkisi birlikte tutmaz. Tablonun harfi uygulandı (K64 sözleşmesi de bunu gerektiriyor); gerçek veride alt küme 9 hücrede bozuldu (bölüm 6). Etki: K24_YENIDEN / DIP_COL_AYRIM yeni FON_IZI ile yeniden koşulursa sinyal kümesi biraz değişir (K24 kural +3 / +18 yeni, -1 / -1 bastırılan). Karar: ana model (eski kararlar değişmez).
2. İki dış test eski hatayı 'gerekçe' olarak sınıyor ve düzeltmeden sonra çöküyor: test_intem_ileri.py satır 93-96 (`P0["i"] == L + 100` penceresini tam seride bekliyor → IndexError) ve test_k24_yeniden.py satır 81-91 + 108-115 (t < 199 kural sinyali bekliyor → 'SAPMA-1 örneği yok' + TypeError). Bu dosyalar bu işin yetkisi dışında, dokunulmadı. Öneri: bu bölümler 'FON_IZI v1.40'tan beri tam seri = kesik seri; t < N-1 satırı yok' sınamasına çevrilmeli (ayrı iş). Gerekçe bölümleri atlanınca ikisinin de geri kalanı geçiyor.
3. İş tanımı fi_k23_parmak maddesi (satır süzgeci) tek başına uygulansa fon_izi_k23 bölge 3 ve fi_k26_ortak BINBN örneği çökerdi (BINBN 21.01.2025 konum 70 < 214, KeyError). `gecmis=L` ile çözüldü (SAPMA 2); hedef ölçüleri eski kodla aynı.
4. İş tanımı beklentisi '~1.430' ile bu sayım farklı evrende (bölüm 6); sayı farkı veri evreninden (V_ABD 1.411 vs OC ABD 2.876, AVR yok).
5. Kendi sürecimde: ilk uygulamada (durumu koru, yalnız satırı yazma) test_k64 kırmızı oldu (2 HATA); tablo harfine dönülerek düzeltildi. Geçici `rsync` yokluğu yüzünden bir test turu yanlış dizinde koştu; sonuçlar ayrıştırıldı, rapora yalnız doğru dizin sonuçları girdi.
6. Süreç notu: ana model iş tanımını ben çalışırken commit etti (HEAD 9b30436 → 1860872); FON_IZI.py / test_fon_izi.py bu iki commit arasında aynı (git diff boş), eski kod kıyası geçerli.

## 8. ÖNERİLEN DEFTER METNİ (ana model işler)
- IK_HATA 2026-11-14 (H178) satırına DÜZELTME notu: "15 Kas: FON_IZI v1.40'ta düzeltildi. 8 tarayıcı (fi_k4 / k4b / k6 / k13 / k14 / k17 / k23_parmak / k24) karar günü konumu t >= N-1 ile çalışıyor; test_fon_izi 63 (önek değişmezliği) eski kodda 8/8 kırmızı, yeni kodda yeşil. Gerçek veri (V_BIST + V_ABD, 31.08.2026 kesik): K24 kural -209 / -515, K13 -0 / -2, K17 -21 / -81, K14 eşli -46 / -159, K23 L15 -116.200 / -282.200 pencere. t < N-1 günü tekrar / aynı dip durumuna da girmediği için K13 ABD, K14, K17, K24'te 1-157 yeni satır var (eski çıktının alt kümesi değil). Eski kararlar değişmedi. test_intem_ileri bölüm 3 ve test_k24_yeniden bölüm 2-3 (SAPMA-1 gerekçesi) güncellenmeli."
- Yeni IK_HATA satırı önerisi: "2026-11-15 | GELECEK_DUZELTME iş tanımı | 'döngü alt sınırı 399' ile 'alt küme / K24_YENIDEN ile birebir anlam' birlikte tutmaz; ayrıca fi_k23 satır süzgeci BINBN bölge hedefini (konum 70) kırıyordu | süreç / ölçüt | alt ajan | sayım alt kümesi 9 hücrede bozuldu; hedef için gecmis=L | tablonun harfi uygulandı | konum şartının tekilleştirme durumundan önce mi sonra mı uygulanacağı iş tanımında açık yazılır; hedef ölçüm çağrıları evren taramasından ayrı düşünülür."
- IK_GOREV satırı önerisi: "2026-11-15 | FON_IZI geleceğe bakma düzeltmesi (H178) | FON_IZI v1.40: 8 tarayıcıda seri uzunluğu şartı karar günü konumuna; fi_k23_parmak gecmis parametresi (bölge hedefleri gecmis=L); test_fon_izi 63/63 (yeni test 63 önek değişmezliği, eski kodda kırmızı); gerçek veri sayımı K24 kural -724; rapor arastirma_cikti/fon_izi/GELECEK_DUZELTME_RAPOR.md | AÇIK: test_intem_ileri ve test_k24_yeniden SAPMA-1 gerekçe bölümleri güncellenecek."
- Colab hatırlatması: "FON_IZI.py değişti (v1.40); Colab'da çalışma zamanını yeniden başlat."

## 9. DOKUNULAN DOSYALAR
`git status --short` (rapor yazıldıktan sonra):
```
 M FON_IZI.py
 M test_fon_izi.py
?? arastirma_cikti/fon_izi/GELECEK_DUZELTME_RAPOR.md
```
Geçici dosyalar (eski kod kopyası, HEAD arşivi, veri, sayım çıktıları) yalnız scratchpad altında: /tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad
