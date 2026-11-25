# MUM_IZI EK 5 İŞ TANIMI — Cemal'in 24 işareti + sözlü öncelik: bant koordinatında mum dizisi benzerliği (v3), işaretlerle sınama, en benzer 24 bölge (25 Kasım 2026)

Yazan: ana model. Cemal (25 Kas, işaretli MUM_IZI4_ONAY): "hepsi de birebir aynı değil, biraz benzeyen var sadece"; "asıl benzemesinin sebeplerinde en çoğu: mumların SMA ile üst / alt / orta banda konumları, İLK NEREDE SONRA NEREDE KALIYOR; bir de birbirlerine göre açılış kapanışları ve fitil."

İşaretler (sonnet okudu, ana model 3 sayfa doğruladı; kutudaki X = seçim): BENZİYOR 7 (sayfa 6, 10, 19, 21, 22, 23, 24), BENZEMİYOR 16, işaretsiz 1 (sayfa 5). Ön kayıtlı eşik 19 / 24 idi: v2 TESPİT GEÇERSİZ (7 / 23 = %30). Dosya: cemal_mum_izi4_onay.json (ALT AJAN BU DOSYAYI VE YUKARIDAKİ SAYFA NUMARALARINI v3 TANIMI COMMIT EDİLENE KADAR KULLANMAZ; v3 yalnız Cemal'in sözünden kurulur).

## Kurallar
- MUM_IZI_IS_TANIMI.md ve CLAUDE.md 'Tespit geçerliliği' kuralları aynen: yasak defter dosyaları, yalnız kendi yollarını commit, veri <= 2022-12-31, KASA açılmaz, GETİRİ / SONRASI HESAPLANMAZ VE GÖSTERİLMEZ. v1 / v2 dosyaları değişmez. Yeni kod: MUM_IZI_V3.py + test_mum_izi5.py.
- Sıra ve mühür: (1) v3 tanımı + sentetik + ön kayıt MUM_IZI5_ON_KAYIT.md commit (işaretlere bakmadan; KONTROL LİSTESİ dolu; kapı) -> (2) işaretlerle sınama (C) -> (3) koşula göre evren taraması ve onay seti (D). (2)'den sonra v3 tanımı DEĞİŞMEZ; değiştirme önerisi raporda 'ÖNERİ' diye yazılır, uygulanmaz.

## A. v3: bant koordinatında dizi benzerliği (Cemal'in üç ailesi)
Koordinat: her mum kendi günündeki Bollinger (20, 2) ile b = (fiyat - SMA20) / (üst bant - SMA20): SMA = 0, üst bant = +1, alt bant = -1 (yalnız o güne kadarki barlarla; K2). Mumun O, H, L, C'si b birimine çevrilir. Pencere uzunluğu 16-24 mum; konum oranıyla 20 konuma eşlenir (doğrusal yeniden örnekleme; şablon 20 mum). Şablon = Cemal'in kalıbı (mum_izi_sablon / mum_izi_mumlar; bantları görüntüden).
- F1 KONUM DİZİSİ (en önemli: 'ilk nerede, sonra nerede kalıyor'): konum başına bC (kapanış), bO (açılış), bH, bL farklarının mutlak ortalaması (b birimi). Ek olarak üç evre özeti: ilk / orta / son üçte birde ortalama bC ve gövdenin SMA'nın üstünde / altında kalma payı (şablonla fark). F1 = dizi farkı ve evre farkının eşit ağırlıklı ortalaması.
- F2 MUMLARIN BİRBİRİNE GÖRE AÇILIŞ / KAPANIŞI: konum başına (b birimi) açılışın önceki kapanışa göre yeri (O_i - C_{i-1}), kapanış değişimi (C_i - C_{i-1}), gövde (C_i - O_i), açılışın önceki gövdenin içinde olup olmadığı; şablonla mutlak fark ortalaması + işaret uyum payı (yön aynı mı). F2 = ikisinin eşit ağırlıklı ortalaması (uyum payı 1 - pay olarak).
- F3 FİTİL: konum başına üst fitil ve alt fitil, hem b biriminde hem mum boyuna oranla; şablonla mutlak fark ortalaması + 'uzun üst fitil (>= boyun yarısı) aynı konumlarda mı' uyum payı.
- Normalizasyon: her aile kendi tau'suyla (gerçek açık veriden rastgele 20.000 pencerenin medyan uzaklığı; günlük ve haftalık ayrı; tohum ön kayıtta) bölünür.
- TELAFİ YASAĞI: bir pencerenin 'aday' olması için üç ailenin HER BİRİ rastgele pencere dağılımının en iyi %20'sinde olmalı (yüzdelik <= 0,20; dağılım aynı zaman dilimi).
- Sıralama puanı: D3 = 0,5 x F1 / tau1 + 0,25 x F2 / tau2 + 0,25 x F3 / tau3 (ağırlıklar Cemal'in sözünden: konum en çok; sonuca göre değişmez). Küçük D3 = daha benzer.
- Geçerli bar (H > L, V > 0), haftalıkta eksik haftalı pencere atılır, tekil olay = kümenin en küçük D3'lü hizası (aynı hissede 15 mum).

## B. Sentetik (kural: pozitif + negatif), getirisiz
Pozitif: gömülü şablon (%0 / 10 / 20 gürültü, 200 tohum, üç bağlam). Negatif: n1 fitilsiz büyük gövde, n2 fitiller ters, n3 mumlar 2 kat, n4 AYNI mum dizisi ama bant farklı (sert düşüşten hemen sonra: bant geniş ve çöküyor; bant koordinatı kayar), n5 aynı mumlar yatay gidiş, rastgele (blok + rastgele yürüyüş). Ölçü: pozitiflerin ve negatiflerin D3 dağılımı; 'aday' kuralını geçen pay. KABUL ÖLÇÜTÜ (önceden): %10 gürültüde pozitif aday payı >= %70; n1-n5 her birinde aday payı <= %5; rastgele seride 1.000 barda aday <= 0,5. Geçmezse yazılır; tanım gevşetilmez / sıkılaştırılmaz.

## C. Cemal'in işaretleriyle sınama (ön kayıt commit'inden SONRA)
- 23 işaretli sayfa (anahtar: mum_izi4_onay_anahtar.json; işaret: cemal_mum_izi4_onay.json) için D3 ve F1 / F2 / F3; BENZİYOR sayfalarının D3'ü BENZEMİYOR'lardan küçük mü: AUC (Mann-Whitney), tam permütasyon p'si, bootstrap %95 (B 5000). Aynı tablo v1 S ve v2 için (bilgi) ve aile aile (hangi aile ayırıyor).
- HÜKÜM (önceden): AUC >= 0,80 'Cemal'in gözüyle UYUMLU (iç örnek, 23 etiket; aralık geniş)'; 0,65-0,80 KISMEN; < 0,65 UYUMSUZ. 7'ye 16 etiketle kesinlik yok: aralık raporda.
- Sayfa sayfa tablo: sayfa | Cemal | D3 sırası (23 içinde) | F1 / F2 / F3 yüzdeliği | aday mı.

## D. Evren taraması ve yeni onay seti (yalnız C hükmü UYUMLU ya da KISMEN ise; UYUMSUZ ise D yapılmaz, rapor yazılır)
- Tarama: günlük 2016-22 ve haftalık 2001-22; ABD / AVR P2 havuzu, BIST (geçerli bar; işlem değeri o günkü BIST medyanının üstünde). Sayım: aday sayısı (pazar x zaman dilimi); 'Cemal'in BENZİYOR dediği sayfaların medyan D3'ünden daha benzer' aday sayısı = bu kalıbın veride kaç kez göründüğü.
- MUM_IZI5_ONAY.pdf: sayfa 1 düz dil özet (işaretlerinle yeni ölçünün uyumu: 'benziyor dediğin 7 sayfanın kaçı yeni ölçüde en benzer yarıda'; veride kaç aday var; 'birebir aynısı yok: en benzerleri bunlar'); sonra EN BENZER 24 aday (en küçük D3; hisse başına bir; günlük 12 + haftalık 12; BIST dilim başına en çok 3), sayfa sırası KARIŞIK (tohum), hisse / tarih / sonrası YOK. Her sayfa: üstte solda 'Senin kalıbın', sağda bölge (fiyat grafiği, bölge öncesi 15 mum, Bollinger 20 + SMA20, bölge sonunda kesik); altta tek panel 'aynı ölçekte üst üste': bant koordinatında (alt bant -1, SMA 0, üst bant +1 yatay çizgi) şablonun mumları gri, bölgenin mumları renkli, konum konum yan yana; en altta ✓ benziyor / × benzemiyor kutuları. Telefonda okunur. Anahtar mum_izi5_onay_anahtar.json'da (sıra ve D3 dahil), PDF'e girmez.
- Onay eşiği (önceden): 24'ün >= 19'u ✓ -> tespit GEÇERLİ; değilse v3 de geçersiz ve bu kalıp 'veride tekrar etmiyor / tarif yetersiz' diye kapanmaya adaydır (karar Cemal'in).

## Çıktılar
arastirma_cikti/mum_izi/: MUM_IZI5_ON_KAYIT.md, MUM_IZI5_RAPOR.md (v3 TANIM, SENTETİK, İŞARETLERLE SINAMA, SAYIM, ONAY SETİ, KONTROL LİSTESİ, HATA, SAPMA, ÖNERİ, ÖNERİLEN DEFTER SATIRLARI), mum_izi5_sonuc.json, mum_izi5_sinama.csv, MUM_IZI5_ONAY.pdf, mum_izi5_onay_anahtar.json.
