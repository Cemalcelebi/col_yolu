# MUM_IZI26 — iki bölge: kod hangisini kalıba yakın bulur? (tanılama; getiri / sonrası yok)

Soru (Cemal, 26 Kas): geçmişli onay setinde (MUM_IZI22_ONAY_GECMISLI.pdf) bir sayfada iki bölgeyi daire içine aldı: "kod bu iki bölge için 'hangisi kalıba daha çok benziyor, neden' sorusuna nasıl cevap verir?"
Görsel: `MUM_IZI26_IKI_BOLGE.png`. Tanılama betikleri repo dışında (/tmp/claude-0/iki_bolge/: b3.py ölçü, fig.py görsel). Veri <= 2022-12-31; her ölçü yalnız pencerenin son barına kadarki veriden (bant dahil).

## Sayfa ve pencereler
- Ekran görüntüsündeki sayfa **Sayfa 25** (başlık soldan kırpılmış: "5:" görünüyor). Anahtar: yeni_sayfa 25 = **APPN** (ABD, günlük), bölge 2021-08-16 .. 2021-09-07, 16 mum, oran 0,634, hakem KISMEN (5), Cemal işareti ✓ benziyor. (Sayfa 5 = KLMSN; grafik onunla uyuşmuyor, bkz. HATA.)
- Uzak görünüm: 2021-02-24 .. 2021-09-07 (önceki 120 + 16 = 136 mum), HK._hk_sayfa_gecmis ile aynı dilim; ekran görüntüsüyle eşleme: kesik mum işareti = 13.05.2021 dibi (uzak bar 55), büyük yeşil = 08.06.2021 (bar 72).
- **SOL** = 2021-05-07 .. 2021-06-07, **21 mum** (dip bölgesine inen ilk mum .. büyük yeşilden önceki mum). Çıkış mumu dahil: 2021-05-07 .. 2021-06-08, 22 mum.
- **SAĞ** = 2021-08-16 .. 2021-09-07, **16 mum** (anahtardaki bölge).

## Tablo
| ölçü | SOL (21) | SOL+çıkış (22) | SAĞ (16) | nerede | SOL / SAĞ |
|---|---|---|---|---|---|
| Y çıkış yeri k (3 .. floor(0,6 m)) | 15 (sınır 12) | 15 (sınır 13) | 9 (sınır 9) | aday kuralı | KALDI / GEÇTİ |
| G1 ön kısım bC ort <= -0,3; yön değişimi >= 2 | -0,62; 11 | -0,62; 11 | -0,45; 5 | aday kuralı | ham geçer* / GEÇTİ |
| G2 yeşil çıkış, sonra >= %80 SMA üstü | 1,00 | 1,00 | 1,00 | aday kuralı | ham geçer* / GEÇTİ |
| T Spearman >= 0,5; son bC >= 0,6 | 0,60; 0,96 | 0,77; 1,71 | 0,83; 0,77 | aday kuralı | ham geçer* / GEÇTİ |
| I bC <= 1,05 payı >= 0,60 | 1,00 | 0,83 | 0,83 | aday kuralı | ham geçer* / GEÇTİ |
| m1 gövde / boy ort <= 0,45 | 0,445 | 0,468 | 0,447 | aday kuralı (M) | GEÇTİ (22'de kaldı) / GEÇTİ |
| m2 alt fitil / boy <= 0,25 | 0,269 | 0,257 | 0,220 | aday kuralı (M) | KALDI / GEÇTİ |
| m3 üst fitil / boy >= 0,33 | 0,285 | 0,275 | 0,333 | aday kuralı (M) | KALDI / GEÇTİ (sınırda) |
| m4 üst / alt fitil toplamı >= 1,5 | 1,42 | 1,45 | 1,75 | aday kuralı (M) | KALDI / GEÇTİ |
| ORAN = bölge boy medyanı / önceki 120 (<= 0,70) | 0,95 (7,06 / 7,41 %) | 0,96 | 0,63 (4,13 / 6,52 %) | mum boyu kapısı | KALDI / GEÇTİ |
| v1 benzerlik S (>= 0,59) | 0,525 | 0,525 | 0,628 | tekilleştirme / R2, R8 (R4'te yok) | altında / üstünde |
| önceki 20 mum tepesinden pencere dibine | -47 % | -47 % | -28 % | kodda yok | — |
| Bollinger genişliği baş -> son | -55 % | -28 % | -43 % | kodda yok | — |
| son 1/3 bant koordinatı medyanı | 0,54 | 0,58 | 0,60 | kodda yok | — |
| gövde / boy medyanı | 0,42 | 0,45 | 0,42 | kodda yok (M ortalamayla bakar) | — |
| SMA20'yi geçen mum boyu / pencere medyanı | 1,48 (28.05) | 1,37 | 1,65 (27.08) | kodda yok | — |
| pencere dibinden son kapanışa | +26 % | +48 % | +20 % | kodda yok | — |
| **v5M aday?** | HAYIR | HAYIR | **EVET** | | |

\* SOL'da k = 15 > 12 olduğu için Y kalır ve R4'ün bütün parçaları "yok" sayılır; "ham geçer" = parça pencerenin kendi k'sıyla hesaplanınca eşiği geçerdi. F (üst fitil > alt fitil payı >= 0,5) SOL'da 0,40 (R4'te yok).

## SOL havuzda var mı?
- MUM_IZI8 taramasında (R4, 16-24 mum) SOL'un hemen yanında **R4 olayı VAR**: 2021-06-09, 16 mum (2021-05-18 .. 06-09), k = 8, evren içi. 2021-06-08 .. 06-23 arasındaki 12 sonda R4 VAR (59 pencere).
- Ama **R4+M (v5M) yok**: 59 R4 penceresinin hiçbirinde M geçmiyor; m3 (üst fitil / boy) en çok 0,24 (eşik 0,33), m4 en çok 1,18 (eşik 1,5), m1 0,49-0,58 (eşik 0,45). Ayrıca bu pencerenin ORAN'ı 0,85 (kapı 0,70). Yani SOL hakem havuzuna da onay setine de giremezdi: **sebep mum yapısı (üst fitil kısa) ve mum boyu (önceki 120 mumdan küçük değil)**.

## KODUN CEVABI
1. Kod SAĞ'ı kalıba daha yakın bulur: SAĞ aday kuralının bütün parçalarını (Y, G1, G2, T, I) ve dört mum kapısını (M) geçer, mum boyu kapısında da geçer (ORAN 0,63); SOL hiçbirinin bütününü geçmez. (aday kuralında var / kapıda var)
2. SOL'u kod aday olarak görmedi; yanında 16 mumluk bir R4 olayı buldu ama M kapısında düştü: SOL'un mumlarında üst fitil boyun %24-29'u (şart %33), üst / alt fitil oranı 1,1-1,4 (şart 1,5). (aday kuralında var)
3. İkinci ayıran şart mum boyu: SOL'un mumları önceki 120 mumla aynı boyda (ORAN 0,95), SAĞ'ınkiler %37 küçük (0,63). Bunun sebebi SOL'dan önceki 120 mumun da zaten büyük mumlu bir çöküş olması: kod mumu "o hissenin olağanına göre" ölçer. (kapıda var)
4. Cemal'in çizdiği 21 mumluk SOL penceresinde kod bir de çıkış yerini beğenmez: SMA20 üstü ilk kapanış 15. mumda (28 Mayıs, küçük bir yeşil), kural en geç 12. mumu ister; yani SOL'da dip kısmı uzun, çıkış sonrası kısa. (aday kuralında var)
5. Kodun gördüğü en büyük üç fark: (a) üst fitil payı ve üst / alt fitil oranı (0,29 / 1,42 karşı 0,33 / 1,75), (b) mum boyu oranı (0,95 karşı 0,63), (c) v1 benzerlik puanı (0,525 karşı 0,628; şablona yakınlık SAĞ'da yüksek).
6. Gel-git (G1), yeşil çıkış ve SMA üstünde kalma (G2), tırmanış (T), bant içinde kalma (I) iki bölgede de var: kod "dipte sıkışıp yukarı dönüş" iskeletini ikisinde de görüyor; ayıran yalnız mumların biçimi ve boyu.
7. SAĞ'ın geçişi ince: m1 0,447 (sınır 0,45) ve m3 0,333 (sınır 0,33) eşiğin hemen üstünde; küçük bir oynama SAĞ'ı da dışarıda bırakırdı.

Kodun HİÇ ölçmediği ama grafikte göze çarpanlar (kodda yok, yalnız bu tanılama için hesaplandı / görüldü):
- SOL 120 mumluk görünümün mutlak dibi; öncesinde -47 %'lik şelale düşüş var (Mart tepesinden çok basamaklı çöküş). SAĞ ise bir yükselişin ardından gelen -28 %'lik, daha yavaş bir geri çekilme ve SOL dibinin üstünde (yükselen dip).
- SOL'un sonunda Cemal'in gördüğü "büyük yeşil çıkış" 8 Haziran mumu (boyu SOL medyanının ~2,1 katı, %15); kod bunu çıkış mumu saymaz, SMA'yı ilk geçen küçük 28 Mayıs mumunu sayar. Çıkış mumunun büyüklüğü kodda ayrı bir ölçü değil (B gövde tavanı onu tersine cezalandırır: SOL+çıkışta B_max 1,11 > 0,9).
- Bollinger daralması (SOL -55 %, SAĞ -43 %) ve bölge dibinin önceki dibe göre konumu kodda yok.
- SOL'dan sonra grafikte görülen (+40 % civarına çıkış) yalnız grafikte görülen; ölçülmedi.

## HATA
- İş tanımı sayfayı "5. sayfa / yeni_sayfa 5 (KLMSN)" diye verdi; ekran görüntüsü **Sayfa 25 (APPN)**. Başlık soldan kırpıldığı için "Sayfa 25" "5:" olarak okunmuş. Tanılama APPN ile yapıldı; KLMSN sayfası grafikle uyuşmuyor (KLMSN uzak görünümünde -20 % dip başta, kutu -15 .. 0; ekran görüntüsünde dip ortada, bant kesik işaretleri 55. mumda). Cemal sayfa 25'e de ✓ koymuş (işaretli PDF).
- SOL'un başlangıcı ekran görüntüsünden elle seçildi (dip bölgesine inen ilk mum 07.05.2021); bir-iki mum kaydırmak k sınırını ve M değerlerini az değiştirir (16-24 mumluk 59 R4 penceresinin hiçbirinde M geçmiyor; sonuç pencere seçimine duyarlı değil).
