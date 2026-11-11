# İz arama operasyonlarının analizi ve yol haritası (11 Kasım 2026)

Yazan: ana model (iş tanımı + denetim). Yapan: alt ajanlar. Dayanak: IZ_KARNE Ç118-Ç151, K58 (Ç151) güç ölçümü.

## 1. Tek ölçüt: bir operasyon iz bulabilir miydi?
K58: olay cetveli (FI_OLCUT, 60 gün, eşli, dört hücre) 60 günde +%2'lik gerçek bir etkiyi 300 olayda %11, 3.000 olayda %21 olasılıkla görüyor; dört hücre birden ~%0,2. Sağlam etkiler %1-3 büyüklüğünde. Bu yüzden her operasyon iki soruyla sınıflanır: (a) olay sayısı ve cetveli gerçek bir etkiyi görebilir miydi, (b) aradığı şeyin arkasında ekonomik bir neden var mıydı.

## 2. Operasyon operasyon

| Grup | Çalışmalar | Hüküm | Neden |
|---|---|---|---|
| Şekil / parmak izi (tek örnekten kalıp) | INTEM K44-K45 (Ç123-124), ECOGR / BBIO K47 (Ç126), çöl P1 / P2 K51 (Ç132-133), TEHOL / MANAS / KZBGY bölgeleri | YANLIŞ YOL | Tek grafikten çıkan 8-9 ölçülü kalıp: serbestlik çok, eşleşme az (n 12-300), ekonomik neden yok. Cetvel bu n'de %10 altı etkiyi göremez; görse de kalıp o örneğe uydurulmuştur. Yeniden açılmaz. |
| Makine, çok özellik | K46, K46-B, K48, K48-B, K49, K50 (Ç125, Ç127-131) | YARIM YOL | Makine bir şey öğreniyor (AUC ABD 0,59-0,70, karışık etikette 0,50: sızıntı yok) ama öğrendiği büyük ölçüde oynaklık; 166 ek özellik bilgi katmadı; portföyde piyasayı geçmedi. Eksik: hedef 'piyasaya göre fazla getiri' olmalıydı, '+%8 önce' değil; özellikler fiyat dışı (kârlılık, ihraç) içermeliydi. |
| Dallanmalı geniş arama | K55, K56 (Ç138-146) | SÜREÇ DOĞRU, HEDEF YANLIŞ | Ön kayıt, kilit, sızıntı ve seçimsiz kontrol örnek süreç. Ama 'büyük yükselişten önce ne vardı' sorusu seçim yanlılığı üretir (bulunan farklar mekanik çıktı); 63 hücre x varyant çok deneme (PBO yüksek). Süreç korunur, soru biçimi bırakılır. |
| Olay süzgeçleri, dar profil | K27 içeriden alım, K28 bilanço, K29-K31, K35-K41, çöl + olay (Ç118), YEOTK profili K57 / B / C (Ç148-150) | DOĞRU FİKİR, YANLIŞ CETVEL | Fikirlerin çoğunun ekonomik nedeni var (bilgi yavaş yayılır). Ama her eklenen şart n'yi küçülttü (K57 V3: n 2-5); cetvel bu n'de kördü. 'İZ DEĞİL' kararlarının n < 1.000 olanları aslında 'ÖLÇÜLEMEDİ'. Bunlar portföy cetveliyle, sürekli sinyal olarak yeniden ölçülmeli. |
| Bilinen etkiler ve hat kontrolü | K42 (Ç121), ölçüm hattı kontrolü (Ç120), K43 (Ç122) | DOĞRU YOL, YARIM KALDI | Hat bilinen etkileri ham ölçüde görüyor; eşli cetvel momentum ve likiditeyi tasarım gereği siliyor. Burada durulmamalıydı: cetvelin gücü o gün ölçülseydi iki hafta kazanılırdı. |
| Cetvel sağlaması | K58 (Ç151) | DOĞRU YOL | Aracı bilinen izle ve plaseboyla sınadı. Eksikleri: beta düzeltmesi yok, evren yalnız yaşayanlar, momentum kabulü sınırda (t 2,10). |
| Evren / batanlar | K34, K54, EVREN2 (Ç137, Ç142) | DOĞRU YOL, AÇIK | Hayatta kalma yanlılığı gerçek (küçüklük etkisi batanlarla üçte bire iniyor). Tiingo fiyatları repoda yok, anahtar oturumda yok: Cemal'in anahtarı gerekir. |
| Sıçrama kovalamak | Kripto +%100 (Ç147), tavan günü | YANLIŞ YOL | Olay nadir (< %1), sonrası eksi. Kapalı. |
| Şirket araştırması | ABD 10x, BIST 10x raporları | DOĞRU AMA BAŞKA İŞ | Aday eleme ve risk (seyrelme, finansman) için değerli; 'iz' üretmez. Pozisyon kararlarında kullanılır. |
| Çıkış / boyut | K19, T10, stop testleri | EKSİK | Ölçülmüş tek kalıcı sonuç: kayıplar sinyalden değil boyuttan (PAPIL, QMLS, TERA). Boyut kuralı bir 'iz' kadar değerli; yazılı kural yok. |

## 3. Eksikler (yapılmayanlar)
1. Portföy düzeyinde, aylık, maliyetli, beta düzeltmeli ölçüm (K58'de kalibre edildi, kullanılmadı).
2. Basit, nedeni bilinen, sürekli sinyaller: momentum, bilanço tepkisi (PEAD), kârlılık, düşük hisse ihracı, 52 hafta zirvesine yakınlık, düşük oynaklık. Bunlar binlerce hissede her ay ölçülebilir; n sorunu yok.
3. Zayıf sinyalleri birleştirmek: tek tek %1-2'lik etkiler sıralama ortalamasıyla birleşince görünür olur. Biz hep şart ekleyip daralttık (VE); doğrusu puan toplamak (ortalama sıra).
4. Çoklu deneme muhasebesi: 150 çalışma yapıldı; yeni keşifte eşik t > 3, bilinen etkinin yinelemesinde t > 2.
5. Batanlar dahil evren (Tiingo anahtarı).
6. 'İz' için hedef büyüklük: maliyet sonrası piyasaya göre yılda kaç puan yeterli? Öneri: en az +%4.

## 4. Yol (sıra ve sorumlu)
- Y1 (alt ajan, şimdi): K59 = portföy cetveli v2 (K58 C + beta düzeltmeli alfa) ile 9 basit sinyal + önceden yazılı 4'lü bileşik (momentum + PEAD + kârlılık + düşük ihraç), ABD iki evren (V_ABD, geniş Yahoo), BIST bilgi. Ön kayıt -> ana model commit -> koşu -> ana model denetim.
- Y2 (alt ajan, şimdi): batanlar dahil evren için seçenek notu (eldeki veri, Tiingo ihtiyacı, bedava seçenekler).
- Y3 (K59 tutarsa): bileşiğin güncel üst %10 listesi = Cemal'in grafik okuyacağı aday listesi (tarayıcı), aylık yenilenir.
- Y4 (K59 tutmazsa): önceden yazılı 3 devam: (a) yalnız küçük-orta hisseler, (b) 3 aylık tutma, (c) French verisinde 2000-2026 aynı bileşik (yanlılıksız).
- Y5 (Cemal'in kararı): portföy cetveli v2 standart olsun mu; hedef büyüklük; Tiingo anahtarı; yazılı boyut kuralı.
- BIRAKILANLAR: şekil / parmak izi, sıçrama kovalama, şart ekleyerek daraltma, 'büyük yükselişten geriye bakma'.
