# SD ÖN KAYIT — benzer şekil benzer devam mı + verinin kendi desenleri (2026-11-27T05:38:33Z)

İş tanımı SD_IS_TANIMI.md (ana model). Bu dosya Z15 / R15 / HEDEF / AYNA HİÇBİR hücrede hesaplanmadan ÖNCE commit + push edilir; tanımlar, eşikler, hüküm kuralları sonra değişmez (değişirse SAPMA). K, küme sayısı, pencere uzunluğu için ikinci değer denenmez. Evren bugün yaşayan hisseler. KASA açılmaz (veri <= 2022-12-31).

## Mühürler

SD_KOD_SHA: 04c3bfd9e7962da3ce51517a225138e93140737aed8ccee16cc8c80ecf91f6de
SD_ESIK_SHA: 4d4cc8e4c7b3585aa01c0e9026cdf5bdbf79bdab40bcc2751503aec59d7622a1
DOSYA_ozellik_ABD.npz: 310f8ab209795618aeb9858f0fae4923062b607d34a4c0f9781792cccabcbae8
DOSYA_ozellik_AVR.npz: 9c428a1b267cd238b2779196b4f3ddba91ac6de7475a78612f7f1504b9c28c4e
DOSYA_cemal_tanim.pkl: fe47edf5e181b6cebf230b2f673c4c9ae0e358fb1cde9c1507a78695e667d740
SAYIM_SHA: d216fff7a25f68f2a3866ce14e4af1f99ef426019de35f977d7b99ca8f3d9a81
STANDART_SHA: 9faaf2c5903dcb49edb2779d35ea9995ba35dd4089c940fe8e8472c89a604269
IS_TANIMI_SHA: 76a4d808b2e3006ac79fd7afa4cd83371d42b1fa5b8b2a9bbb89c53f2049df79
YO_ozellik_ABD.pkl: 9e470d0658ccca89c17edc320b250397ce3d5f3c265e52dd831767cc46d84ca8
YO_ham_ABD.npz: 41f317fbd7e8928226215683444b4319f1e8301dbcc5ac549cd80c5b59ace234
YO_ozellik_AVR.pkl: daa33b4c6ba06dee2f1c300a1797f4a7e9d9e4ab113a865240d56fd44393e09f
YO_ham_AVR.npz: bf3dfcf27019a243c7281e069a04ec43c733bf8d915feb60e67021d2a6572c0b

- Panel dosyaları (repo dışı): /root/.kasa/ham/sekil_devam (ozellik_*.npz = pencere meta + tanımlayıcılar, sonuç sütunu YOK; cemal_tanim.pkl; sayim.json)

## GETİRİSİZ SAYIM (Z15 / R15 hesaplanmadı)

| hücre | L | pencere | geçerli | atılan (neden) | farklı ay | en kalabalık 3 ay payı | hisse |
|---|---|---|---|---|---|---|---|
| ABD d1619 | L10 | 400337 | 397651 | {'TANIMSIZ': 2659, 'KILITLI': 27} | 48 | 0,078 | 2705 |
| ABD d1619 | L20 | 400337 | 397090 | {'TANIMSIZ': 3216, 'KILITLI': 31} | 48 | 0,078 | 2694 |
| ABD d2022 | L10 | 391113 | 386370 | {'TANIMSIZ': 4686, 'KILITLI': 57} | 36 | 0,104 | 3713 |
| ABD d2022 | L20 | 391113 | 385364 | {'TANIMSIZ': 5661, 'KILITLI': 88} | 36 | 0,104 | 3706 |
| AVR d1619 | L10 | 80675 | 80432 | {'TANIMSIZ': 217, 'KILITLI': 26} | 48 | 0,071 | 479 |
| AVR d1619 | L20 | 80675 | 80391 | {'TANIMSIZ': 262, 'KILITLI': 22} | 48 | 0,071 | 478 |
| AVR d2022 | L10 | 64958 | 64790 | {'TANIMSIZ': 156, 'KILITLI': 12} | 36 | 0,094 | 515 |
| AVR d2022 | L20 | 64958 | 64755 | {'TANIMSIZ': 191, 'KILITLI': 12} | 36 | 0,094 | 515 |

Tanımlayıcı boyutu: L20: A 84, B 104, 0 3; L10: A 44, B 54, 0 3

| komşu havuzu | sorgu | ay | havuz en az | medyan | en çok |
|---|---|---|---|---|---|
| ABD L20 | 385364 | 36 | 388403 | 564666 | 769065 |
| ABD L10 | 386370 | 36 | 388948 | 565619 | 770623 |
| AVR L20 | 64755 | 36 | 78704 | 110024 | 142913 |
| AVR L10 | 64790 | 36 | 78744 | 110074 | 142989 |

Cemal bölgeleri (pazar, sınıf, durum, sayı): [['ABD', 'APPN_SAG', 'TAMAM', 1], ['ABD', 'APPN_SOL', 'TAMAM', 1], ['ABD', 'EVET', 'TAMAM', 23], ['ABD', 'HAYIR', 'TAMAM', 45], ['ABD', 'KISMEN', 'TAMAM', 20], ['AVR', 'EVET', 'TAMAM', 1], ['AVR', 'HAYIR', 'TAMAM', 8], ['AVR', 'KISMEN', 'TAMAM', 3], ['BIST', 'EVET', 'TAMAM', 12], ['BIST', 'HAYIR', 'TAMAM', 7], ['BIST', 'KISMEN', 'TAMAM', 3]]

## Yorum gerektiren noktalar (ölçümden ÖNCE sabit)

1. Pencere sonları YO örnek satırlarıdır (YO_ON_KAYIT yorum 1-4: k % 5 == 0, giriş k + 1 barı P2, giriş 2016-22, 15. bar kesik içinde); SEKIL_DEVAM yeni örneklem kurmaz, YO panel dosyalarını sha denetimiyle içe alır. L10 ve L20 aynı pencere sonlarını kullanır.
2. Bant koordinatı MI.mi_bant ile: sigma ddof 0 (MUM_IZI / UC / HAKEM ile aynı); b = (fiyat - SMA20) / (BU - SMA20); BU = SMA20 ise pencere TANIMSIZ.
3. Ek 4 sayı kırpılmaz (iş tanımı kırpmayı yalnız b ve göreli hacim için yazdı); 'pencere içi bant genişliği değişimi' = bw_k / bw_s - 1 (UC DARALMA tanımı); 'önceki 60 barın en yükseğinden pencere dibine düşüş (ATR birimi)' = (min L pencere - maks H önceki 60) / (ATRP20_k x C_k) (eksi = düşüş).
4. Göreli hacim: medyan önceki 60 barın (i hariç) hacmi; hacim sütunu MI.mi_veri açık kopyasında var (Volume; V > 0 geçerli bar şartı) -> TANIMLAYICI B koşulur.
5. Geçerlilik: A, B ve 0 aynı pencere kümesinde; bir pencerenin A'sı geçerli, B'si geçersiz olamaz (eşli IC farkı için); önceki 60 bar şartı (s - 60 >= 0).
6. Kilit kuralı: pencerenin takvim aralığında geçersiz bar payı > 0,20 -> KILITLI (UC_ESIK atma KILITLI; uc_kilitli_pay içe alınır). Cemal bölgelerine uygulanmaz.
7. Standartlaştırma ABD keşif (2016-19) geçerli pencerelerinin ortalama / std'si ile; AVR de aynı istatistiklerle (AVR'ye özel ölçek yok; yön sınaması).
8. Komşu havuzu (yalnız geçmiş): sorgular giriş ayına göre gruplanır; r0 = grubun en küçük pencere sonu satırı; havuz = t_row <= r0 - 20 VE 15. sonuç barının satırı < r0 VE başka hisse. Böylece her komşu her sorgudan >= 20 satır önce biter ve devamı sorgu gününden önce bilinir. Havuz ayda bir güncellenir; ABD doğrulamasının havuzu 2016'dan başlar (keşif pencereleri + doğrulamanın geçmiş pencereleri). Sorgular seyreltilmez (her 5 barda bir; hesap yetiyor).
9. Komşu araması tam (yaklaşık değil): float32 |y|^2 - 2xy sıralaması, argpartition; eşit uzaklıklar sırası belirsiz (etkisi yok sayılır).
10. IC: her giriş ayında >= 30 sorgu; aylık Spearman; IC = ayların eşit ağırlıklı ortalaması; bootstrap ayları yerine koyarak (B 10.000, tohum 271). IC farkları aynı ayların aylık farklarıyla.
11. ÜST / ALT: her giriş ayında TAHMİN'in kesit sırası (ortalama sıra / n) > 0,90 / <= 0,10 (aylık kesit: piyasa zamanlaması dışlanır); ölçüler pencere ağırlıklı (ay kümeli oran).
12. TOPLAM FARK = R15 - aynı hissenin aynı hücrede (pazar x dönem) bütün YO örnek pencerelerinin (tanımlayıcısı geçersizler dahil) R15 ortalaması (YO yorum 10 gibi).
13. AVR: SINAMA 1 sorguları AVR 2020-22 (havuz AVR 2016'dan; AVR'nin kendi geçmişi); SINAMA 2 AVR şartı AVR 2020-22 ortalama Z15 işareti (n >= 30); AVR 2016-19 bilgi. AVR'de TANIMLAYICI B koşulmaz (iş tanımı AVR için yalnız IC(A) istiyor; 0 ve rastgele bilgi).
14. Küme seçimi yalnız keşif Z15'iyle; aday n >= 1000 ve ay >= 12; L10 için de aynı seçim (5 / 5) yapılır ve SD_KESIM'e yazılır; PDF yalnız L20'nin 10 kümesi.
15. Doğrulamada bütün 60 kümenin sonucu bilgi olarak hesaplanır (Cemal bölgelerinin ve APPN'nin düştüğü kümelerin sonucunu yazmak için); hüküm yalnız seçilen 10'da.
16. Cemal bölgeleri: mum_izi23_olay.csv günlük satırları (EVET 36: ABD 23, BIST 12, AVR 1; KISMEN / HAYIR bilgi); pencere = bolge_son barında biten 20 bar (bölge 16-24 bar; sabit pencere uzunluğu iş tanımı gereği); APPN SOL = 2021-06-07'de biten 20 bar, SAĞ = 2021-09-07'de biten 20 bar. Atama keşifte (getirisiz).
17. PDF örnekleri keşif üyelerinden (tohum 274); çizim pencere sonu k'de biter (assert); hisse adı ve tarih yazılır (iş tanımı izin verdi).
18. Sentetik ek (koordinatörün iletisi, gerçek sonucu etkilemez): Cemal'in kalıbı (MV.mv_sablon 'tam' 20 mum) gömülü panel + N1 / N2 / N3; sonuçlar sd_sentetik.json ve SD_YAPAY_DESEN.pdf; sentetikte aday küme şartı n >= 30 ve ay >= 12.

## Tanımlar (SD_ESIK; sha yukarıda)

```
{
 "surum": "SD-1.0",
 "tohum": {
  "boot": 271,
  "kmeans": 272,
  "rastgele": 273,
  "ornek": 274,
  "sentetik": 275,
  "tanim": "np.random.default_rng([tohum, crc32(anahtar)]) (kmeans: default_rng(272) doğrudan); sıra bağımsız, tekrarlanabilir"
 },
 "pencere": {
  "L": [
   20,
   10
  ],
  "adim": 5,
  "tanim": "pencere sonu k = YO örnek satırı (YO ozellik_<pazar>.pkl: hissenin kendi geçerli bar indeksi k % 5 == 0, giriş k + 1 barı P2, giriş 2016-2022, 15. bar <= 2022-12-31, YO boşluk kuralları); pencere = k - L + 1 .. k (L20 ve L10 aynı pencere sonları)"
 },
 "bant": {
  "n": 20,
  "k": 2.0,
  "klip": 3.0,
  "tanim": "MI.mi_bant(C) (SMA20, std ddof 0, yalnız o bara kadarki kapanışlar); b = (fiyat - BO) / (BU - BO) = (fiyat - SMA20) / (2 sigma20); BU <= BO (sigma 0) ise tanımsız; [-3, +3] kırpılır"
 },
 "tanimlayici": {
  "A": "her bar i = k - L + 1 .. k için [b(O), b(H), b(L), b(C)] (bar sırasıyla, 4L sayı) + BW_DEG = bw_k / bw_s - 1 (bw = (BU - BA) / BO, s = pencere başı) + DUSUS = (min L[s..k] - maks H[s-60 .. s-1]) / (ATRP20_k x C_k) (ATR birimi; kırpılmaz) + KON_BAS = KONUM120[s] + KON_SON = KONUM120[k] (KONUM120 = OLCU_SINAMA._os_atrp_f15 'f15', YO ile aynı); ek 4 sayı kırpılmaz (iş tanımı kırpmayı yalnız b ve göreli hacim için yazdı)",
  "B": "A + her bar için RV = log(V_i / medyan(V_{i-60} .. V_{i-1})) [-3, +3] (L sayı; hacim MI.mi_veri açık kopya, geçerli barlar)",
  "0": "[b(C_k), F15 / ATRP20_k, KONUM120_k] (F15 = C_k / C_{k-15} - 1, YO tanımı)",
  "gecerli": "pencerenin bütün A, RV ve 0 sayıları sonlu VE s - 60 >= 0 (önceki 60 bar var); A / B / 0 AYNI pencere kümesinde (eşli karşılaştırma)",
  "standart": "her boyut KEŞİF (ABD 2016-19) geçerli pencerelerinin ortalaması / std'si (ddof 0) ile (getirisiz; sayım aşamasında; sha ön kayıtta); AVR de ABD keşif istatistikleriyle; std = 0 ise DUR"
 },
 "atma": {
  "sira": [
   "KILITLI",
   "TANIMSIZ"
  ],
  "KILITLI": 0.2,
  "tanim": "KILITLI = pencerenin takvim aralığında (s barının günü .. k barının günü) ham veride geçersiz günlük bar payı (MI.mi_veri 'gecersiz': kilitli / hacimsiz / H = L) > 0,20 (MUM_IZI_UC.uc_kilitli_pay; UC kuralı aynen); TANIMSIZ = geçerli şartı tutmuyor; ilk tutan neden"
 },
 "devam": {
  "ufuk": 15,
  "hedef": 2.0,
  "stop": 1.0,
  "tanim": "E0 = k + 1 açılışı; barlar k + 1 .. k + 15 (giriş barı dahil; YO ile aynı); R15 = C_{k+15} / E0 - 1; Z15 = R15 / (ATRP20_k x kök 15); YOL_j = (C_{k+j} / E0 - 1) / (ATRP20_k x kök 15), j = 1..15; HEDEF = High >= E0 (1 + 2 ATRP20_k) ilk barı Low <= E0 (1 - 1 ATRP20_k) ilk barından ÖNCE (aynı bar = stop önce -> 0; YO.yo_ilk_dokunma ATRP birimine çevrilmiş fiyatla); AYNA = Low <= E0 (1 - 2 ATRP) önce High >= E0 (1 + 1 ATRP) görmeden"
 },
 "komsu": {
  "K": 50,
  "ara": 20,
  "kume": "giriş ayı",
  "havuz": "sorgular giriş ayına göre gruplanır; r0 = grubun en küçük pencere sonu satırı (birleşik takvim); havuz = aynı pazarın geçerli pencereleri, t_row <= r0 - 20 VE 15. sonuç barının satırı < r0 (komşunun devamı sorgudan önce bilinir) VE başka hisse; ayda bir güncellenen havuz; uzaklık standart tanımlayıcıda Öklid (float32 BLAS, |y|^2 - 2xy sıralaması); TAHMİN = 50 komşunun ortalama Z15'i",
  "rastgele": "şans tabanı: aynı havuzdan (başka hisse) eşit olasılıkla 50 pencere (tohum 273, anahtar 'pazar|L|ay')"
 },
 "ic": {
  "ay_en_az": 30,
  "tanim": "her giriş ayında (>= 30 sorgu) TAHMİN ile Z15'in Spearman sıra ilişkisi (ortalama sıra); IC = ayların eşit ağırlıklı ortalaması; fark (A - 0, B - A) aynı ayların aylık farklarının ortalaması"
 },
 "uc": {
  "pay": 0.1,
  "tanim": "her giriş ayında TAHMİN'in kesit yüzdelik sırası (ortalama sıra / n): ÜST = > 0,90, ALT = <= 0,10"
 },
 "toplam_fark": "R15 - aynı hissenin aynı hücredeki (pazar x dönem) bütün YO örnek pencerelerinin (tanımlayıcısı geçersiz olanlar dahil) R15 ortalaması",
 "yol": "her sorgu için corr(YOL_sorgu, komşuların ortalama YOL'u) (15 nokta; sabitse yok); sorgular üzerinden ortalama; rastgele komşularla aynı",
 "boot": {
  "B": 10000,
  "kume": "giriş ayı (YYYY-AA)",
  "tanim": "ay kümeli bootstrap (aylar yerine koyarak; multinomial ağırlık); oran / ortalama = ağırlıklı toplam / ağırlıklı sayı; IC = ağırlıklı aylık IC ortalaması; %95 = 2,5 / 97,5 yüzdelik; ÜST - ALT aynı ağırlıklarla"
 },
 "kmeans": {
  "k": 60,
  "iter": 300,
  "tanim": "k-ortalama++ başlangıç (default_rng(272); tek başlangıç), Lloyd adımları atama değişmeyince ya da 300 adımda durur; boş küme önceki merkezini korur; KEŞİF standart A (L20 ve L10 ayrı) üzerinde; doğrulama / AVR / Cemal pencereleri en yakın merkeze atanır"
 },
 "secim": {
  "en_iyi": 5,
  "en_kotu": 5,
  "n_min": 1000,
  "ay_min": 12,
  "tanim": "aday küme = keşif n >= 1000 ve farklı ay >= 12; EN İYİ 5 = keşif ortalama Z15'i en büyük 5 (azalan), EN KÖTÜ 5 = en küçük 5 (artan); eşitlikte küçük küme no"
 },
 "bh_q": 0.1,
 "hucre": {
  "kesif": "ABD|d1619",
  "dogrulama": "ABD|d2022",
  "avr": "AVR|d2022",
  "avr_bilgi": "AVR|d1619",
  "tanim": "dönem giriş tarihine göre HV.hv_hucre_ad; AVR yön sınaması AVR 2020-22 sorguları (havuz AVR 2016'dan); AVR 2016-19 yalnız SINAMA 2'de bilgi"
 },
 "hukum": {
  "S1_TASIYOR": "ABD 2020-22'de IC(A) > 0 ve alt > 0 VE IC(A) - IC(0) > 0 ve alt > 0 VE ÜST - ALT Z15 > 0 ve alt > 0 VE AVR 2020-22 IC(A) > 0 -> 'ŞEKİL BİLGİ TAŞIYOR'",
  "S1_BASIT": "IC(A) > 0 ve alt > 0 ama IC(A) - IC(0) alt <= 0 -> 'BASİT KONUMDAN FAZLASI YOK'",
  "S1_TASIMIYOR": "IC(A) alt <= 0 (aralık sıfırı içeriyor ya da eksi) -> 'ŞEKİL BİLGİ TAŞIMIYOR'",
  "S1_ARA": "IC(A) alt > 0, IC(A) - IC(0) alt > 0 ama ÜST - ALT ya da AVR şartı tutmuyor -> 'ARA: <eksik şart>' (ŞEKİL BİLGİ TAŞIYOR denmez)",
  "HACIM": "IC(B) - IC(A) > 0 ve alt > 0 -> 'HACİM EKLİYOR'; değilse 'HACİM EKLEMİYOR'",
  "S2_IYI": "EN İYİ küme: doğrulamada Z15 > 0 ve alt > 0 VE TOPLAM FARK > 0 ve alt > 0 VE AVR 2020-22 ortalama Z15 > 0 (AVR n >= 30; değilse şart tutmamış) -> 'TUTTU'",
  "S2_KOTU": "EN KÖTÜ küme: Z15 < 0 ve üst < 0 VE TOPLAM FARK < 0 ve üst < 0 VE AVR ortalama Z15 < 0 -> 'TUTTU'",
  "DESEN": "'DESEN TUTTU' <=> keşif sırası 1 olan EN İYİ küme TUTTU (EN KÖTÜ 1 için ayrı satır); 10 küme için BH q 0,10 (tek yönlü bootstrap p: iyi (1 + #Z15* <= 0) / (B + 1), kötü (1 + #Z15* >= 0) / (B + 1))",
  "L10": "aynı kurallar L10 için ayrı (ERKEN EVRE)"
 },
 "cemal": {
  "sinif": "EVET",
  "zaman": "gunluk",
  "tanim": "mum_izi23_olay.csv günlük satırları: pencere = bolge_son barında biten 20 (ve 10) bar (Cemal'in bölgesi 16-24 bar; pencere uzunluğu sabit), ABD / AVR / BIST serisi MI.mi_veri açık kopyasından; P2 / kilit kuralı uygulanmaz (bilgi); EVET = BENZİYOR; KISMEN / HAYIR bilgi",
  "APPN": {
   "SOL": "2021-06-07",
   "SAG": "2021-09-07",
   "tanim": "MUM_IZI26_IKI_BOLGE: SOL 2021-05-07 .. 06-07, SAĞ 2021-08-16 .. 09-07; pencere = son barda biten 20 bar"
  }
 },
 "pdf": {
  "ornek": 6,
  "once": 40,
  "tanim": "her seçilen küme bir sayfa: merkez (bant koordinatında mum + Bollinger), keşif üyelerinden rastgele 6 gerçek örnek (tohum 274; pencere + önceki 40 bar; yüzde ekseni; SONRASI YOK: dilim k + 1'de biter, assert)"
 },
 "sentetik": {
  "hisse": 150,
  "bar": 2000,
  "olay_ara": [
   70,
   110
  ],
  "ilk": 200,
  "pay": {
   "POZ": 0.5,
   "N1": 0.25,
   "N2": 0.25
  },
  "gurultu": [
   0.0,
   0.1,
   0.2,
   0.3
  ],
  "olcek": [
   0.5,
   2.0
  ],
  "Z_ek": 0.5,
  "n_min": 30,
  "ay_min": 12,
  "tanim": "POZ = Cemal'in kalıbı (MV.mv_sablon()['tam'] 20 mum) bant ölçeğinde gömülür: fiyat = SMA20(s-1) + (şablon - şablon BO_0) x sigma20(s-1) / şablon sigma_0 x ölçek (log-düzgün 0,5..2), gürültü = düzey x ölçekli ortalama şablon mum boyu (O / H / L / C'ye ayrı normal), sonra giriş barından sonraki barda (k + 2) +0,5 Z'lik tek sıçrama (bilerek; sonraki pencerelerin devamına taşmasın diye); N1 = aynı kapanış yolu, iri gövdeli üst fitilsiz mum (gövde = şablon ortalama mum boyu), ilişki YOK; N2 = şablonun mum biçimi (O / H / L kapanışa göre), yatay ya da düşen kapanış yolu, ilişki YOK; N3 = gömülmemiş rastgele yürüyüş pencereleri; ilişkisiz panel = yalnız rastgele yürüyüş; kalıbın kümesi = POZ keşif pencerelerinin en çok düştüğü küme"
 }
}
```

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban = aynı pazar x dönem, aynı evren; IC aynı ay içinde (kesit) hesaplanır (zaman etkisi dışlanır); TAHMİN'in şans tabanı rastgele komşu (aynı havuz) ve basit taban TANIMLAYICI 0 (son bant konumu, F15 / ATRP, KONUM120: bilinen etkiler); Z15 ATRP20 ile oynaklıktan arındırılmış; TOPLAM FARK aynı hissenin aynı dönem ortalamasına göre; ÜST / ALT aynı ayın kesitinde; HEDEF ve AYNA iki yönde aynı kötümser kural |
| K2 | geleceğe bakma | EVET | tanımlayıcı yalnız k'ye kadarki barlardan (test: k + 1 ve sonrası bozulunca aynı); komşular yalnız geçmişten: t_row <= r0 - 20 ve 15. sonuç barı < r0, başka hisse (kodda maske + test); giriş k + 1 açılışı; sonuçlar ayrı fonksiyonda, keşif aşamasında yalnız ABD 2016-19 (assert); standartlaştırma ve kümeler yalnız keşiften; veri <= 2022-12-31 assert + KASA kapısı |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar (H > L, V > 0, sonlu > 0); kilitli / hacimsiz / H = L bar payı > 0,20 olan pencere atılır (UC kuralı); bant sigma 0 ise tanımsız; YO örneklem kuralları (giriş boşluğu <= 10 satır, 15 bar <= 30 satır) |
| K4 | tekilleştirme | EVET | her hissede her 5 barda bir pencere (örtüşme azaltılır, kalkmaz: 20 barlık pencereler örtüşür); çıkarım ay kümeli bootstrap (pencereler bağımsız sayılmaz); n pencere ve farklı ay ayrı yazılır; medyan Z15 bilgi; komşu başka hisseden |
| K5 | giriş fiyatı | EVET | giriş = pencere sonundan sonraki ilk geçerli bar açılışı (k + 1), k kapanışı değil |
| K6 | veri birimi | EVET | YO / OS bölünme düzeltmeli açık kopya; getiriler oransal, yerel para, pazar içi; tanımlayıcı birimsiz (bant koordinatı, ATR birimi, konum); hacim oranı hissenin kendi geçmişine göre; açık kopya kapanışları YO bar deposuyla birebir (assert) |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı): Z15 / R15 yukarı yanlı; ÜST - ALT ve IC kesit içi olduğu için yanlılık iki tarafa da biner; raporda yazılır; kasa açılmaz |
| K8 | örneklem ve dönem | EVET | n büyük (yüz binler; ay 36); küme hükmü n >= 1000 ve ay >= 12 kümelerde; 10 küme BH q 0,10; iki dönem (keşif / doğrulama) + iki pazar; en kalabalık 3 ay payı her küme satırında; Cemal bölgeleri (36 günlük EVET) yalnız sayım, sonuç değil |
| K9 | ön kayıt | EVET | SD_ON_KAYIT.md: SD_KOD_SHA, SD_ESIK_SHA, panel dosya sha'ları, SAYIM_SHA, YO panel sha'ları + yorum noktaları; keşif ön kayıt commit + push sonrası (kapı: kontrol + sha + commit + temiz ağaç); doğrulama sd_kesim.json commit'inden sonra (kapı); ikinci koşu durur; K, küme sayısı, pencere uzunluğu için ikinci değer denenmez |
| K10 | ayrıştırma | EVET | YO panel sha'ları YO_ON_KAYIT ile aynı (assert); açık kopya kapanışları bar deposuyla birebir; tanımlayıcı elle kurulmuş sentetik örnekte; KONUM120 / F15 yeniden hesabı YO panelindeki değerle aynı (assert); Cemal bölgesi bolge_son tarihi seride yoksa 'YOK' yazılır |
| K11 | yeniden üretim | EVET | küme merkezleri doğrulamada yeniden hesaplanır ve sd_kesim.json'la aynı olmalı (DUR); raporda >= 2 sayı satır dosyalarından bağımsız kısa kodla yeniden üretilir; komşu araması küçük örnekte saf çözümle karşılaştırılır (test) |
| K12 | ifade | EVET | hüküm yalnız önceden yazılı kurala göre; IC küçükse 'küçük' denir ve para karşılığı (ÜST - ALT R15 %, rastgele güne göre TOPLAM FARK) yanına yazılır; sayı ile yorum ayrı cümlede; 'iz' sözü kullanılmaz (önerme sınaması); evren bugün yaşayanlar |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_sd); mevcut modüller ve defter dosyaları değişmez (yalnız import); yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat; KNN / şekil ölçüsü kapalı konusu Cemal'in açık isteğiyle yalnız bu işte |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez, kasa açılmaz |

## SAPMA

(ön kayıt anında yok)

