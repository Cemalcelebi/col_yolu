# K56 — K51-K55 ETKİ VE MEKANİZMA ARAŞTIRMASI: FAZ 0 RAPORU (K56-FAZ0-20261030-175944-13cb4be)

- Kod K56 v0.1 (2026-10-30, Faz 0: etki envanteri, mekanizma hipotezleri, veri kaynakları, küçük örneklem erişim testi, seçim etkisi sentetik sınaması); commit 13cb4be; kilit sha b21541dc479b. K51-K55 dosyaları yalnız okundu (K56_KAYNAK_KAYDI.csv: dosya, sha256, amaç).
- Faz 0: envanter, hipotezler, veri kaynakları, küçük örneklem erişim testi ve M01 sentetik yöntem sınaması. Bütün evrene mekanizma testi YOK; büyük indirme YOK.
- Sınıflar ön sınıftır (Faz 0); kesin sınıf Faz 1 testleriyle (ONKAYIT_K56 3). K51 İZ DEĞİL ve K55 İZ YOK kararları değişmedi.

## 0. Özet

- **M01 seçim etkisi (aday)**: bilgisiz yapay veride (4 evren × 400 hisse) K55'in olay tanımı ve aynı kod, 25 KEŞİF hücresinin Y60'ta 21'inde gerçek A farkının en az yarısını aynı işaretle üretiyor (oran medyanı 1.18); 4 hücre BELİRSİZ, MEKANİK İZ YOK 0. Yön uyumlu 5 hücre dahil. Ters yönlü KEŞİF sayısı 20 (IZ_KARNE'deki 19, D03-S02 vekil sayıldığı için).
- KEŞİF'i sağlayan (varyant, ufuk) satırlarında (v1.1-3, 125 satır, 64 varyant): satır kararları {'MEKANIK_ACIKLAR': 109, 'BELIRSIZ': 10, 'MEKANIK_IZ_YOK': 5, 'KISMEN_MEKANIK': 1}; hücre çoğunluğu MEKANİK AÇIKLAR 18 / 25.
- Y60 ile KEŞİF ufku ayrışan hücreler: D01-S10 (Y60 MEKANIK_ACIKLAR, KEŞİF ufku BELIRSIZ), D02-S06 (Y60 MEKANIK_ACIKLAR, KEŞİF ufku BELIRSIZ), D05-S03 (Y60 MEKANIK_ACIKLAR, KEŞİF ufku BELIRSIZ), D06-S04 (Y60 BELIRSIZ, KEŞİF ufku MEKANIK_ACIKLAR), D10-S10 (Y60 MEKANIK_ACIKLAR, KEŞİF ufku KISMEN_MEKANIK). Ön sınıf ön kayda göre Y60'tan verildi (v1.1-3); bu hücrelerin KEŞİF'i Y120 / Y250'den geldiği için kesin karar seçimsiz kontrolde.
- Bağımsız denetçinin ön kayıt dışı kontrolü (K55 tam paneli, KEŞİF, Y60): olay etiketi seçimsiz kurulunca (eşiği aşan BÜTÜN günler) gerçek d -0,016 .. -0,049'a iniyor (ilk geçiş etiketiyle -0,25 .. -0,43): ters yönlü farkların ~%90'ı olay tanımından. Küçük, aynı yönlü bir kalıntı kalıyor (kısa dönem tersine dönüş adayı, M02). t0 günü kapanışı düşen olay payı gerçek 0,743 / sentetik 0,736.
- Anlamı: K55'in ters yönlü KEŞİF'leri bir piyasa davranışı değil, olay tanımının (t0 = ileri pencerenin +%30'u ilk yakaladığı gün, giriş t0+1) eseri olmaya ADAY. Kesin sınıf ön kayıtlı seçimsiz kontrolle (v1.1-2; uygulama sırası 1; yerel, indirme yok). Gecikme (t0−k) yalnız Y60'ta söner; Y250'de ayırt edici değil.
- **Faz 0 sonucu**: mekanizması aranacak sağlam etki çok az. K51-K54'te kaynakta desteklenen ve eser adayı olmayan bulgu YOK (desteklenen tek bulgu K52 H4: olumlu analist revizyonlarının yarısı fiyat yükseldikten sonra geliyor = ALTERNATİF AÇIKLAMA, M19). 'İLİŞKİ VAR, NEDEN BELİRSİZ' kalan 4 bulgu: K55-D01-S05, K55-D02-S05, K55-D04-S04, K55-D06-S04 (K55'te sentetik sınamada belirsiz). Büyük veri indirmeleri ancak Faz 1 adım 1-3'ten sonra gerçek etki kalırsa anlamlı.
- Envanter: 265 bulgu (K51 90, K52 34, K53 22, K54 52, K55 67); ön sınıf: ETKİ YOK (başarısız kalır; açıklanacak etki yok) 103, ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) 49, YÖNTEM DENETİMİ (bulgu değil) 39, VERİ YETERSİZ 29, YANLIŞ BULGU ADAYI (M01) 21, BETİMLEYİCİ (kaynakta karar yok) 18, İLİŞKİ VAR, NEDEN BELİRSİZ 4, ALTERNATİF AÇIKLAMA 1, YANLIŞ BULGU ADAYI (tanımsal) 1.
- Açıklanmamış listesi: VERİ YETERSİZ (ölçülemedi) 29, ADAY AÇIKLAMA (Faz 1 doğrulaması bekliyor) 23, BETİMLEYİCİ (karar yok) 18, AÇIKLANMADI 4.
- Mekanik denetim: 30 kayıt (uyuşmazlık, K55 sınıf kuralı farkı, kürasyon düzeltmesi; K56_ENVANTER_DENETIMI.csv; sessiz düzeltme yok).
- Erişim testi: GECTI 27, KISMI 9, ATLANDI 1.
- Bağımsız denetim: 45 bulgu (K56_DENETIM_BULGULARI.csv); düzeltme durumu aşağıda 'Denetim' bölümünde.

## 0b. Talimatın süzgeçten geçirilmesi

| oneri | karar | gerekce |
|---|---|---|
| Etki envanteri (10 alan, bütün bulgular) | AYNEN | K51-K55'in bütün hipotez / hücre / denetim bulguları; K55 sayıları CSV'den otomatik, öteki metinler kaynakla mekanik denetimli |
| Her bulgu için mekanizma araştırması | DEĞİŞTİRİLDİ | etkisi olmayan ya da kaynakta tutmayan bulgular için mekanizma aranmaz (ETKİ YOK, ETKİ SAĞLAM DEĞİL); ölçüm hattı / evren denetimleri bulgu sayılmaz (YÖNTEM DENETİMİ); kararsız bilgi notları BETİMLEYİCİ. Bütün bulgular e |
| K55'in ters yönlü KEŞİF'leri özellikle (20; IZ_KARNE'de 19 yazılı, D03-S02 vekil sayılmıştı) | AYNEN + ÖNE ALINDI | önce mekanik açıklama (M01) sentetik sıfır sınamasıyla sınandı: bilgisiz veride etki yeniden üretiliyor (aday); kesin karar Faz 1'in ilk adımında gerçek veride seçimsiz kontrolle |
| Bağımsız veri kaynakları A-E | AYNEN + GENİŞLETİLDİ | 28 kaynak (kasıt kanıtı ve veri hatası kaynakları eklendi); erişim testleri; KEŞİF kapsamı açık alanla (tam / kısmi / yok); kapsam / gecikme / maliyet / lisans tablosu |
| 13F, Form 4, MIDAS gibi büyük indirmeler | ERTELENDİ (koşullu) | ancak yerel ve indirmesiz adımlardan (M01, M03, M04, M15, M16, M18) sonra AÇIKLANMAMIŞ gerçek etki kalırsa; bugün yalnız 4 K55 hücresi (sentetik sınamada belirsiz) bu durumda, K51-K54'te hiç yok |
| Ortalama getiri testleri (açığa satış, içeriden alım / satış, sulandırma, nakit, bilanço sürprizi) | YAPILMADI (zaten var) | Ç100, Ç102, Ç103, Ç107: hepsi İZ DEĞİL (dört şart tutmadı); bazı ortalama farklar sıfırdan büyük (Ç107 batanlar dahil +%2,8 / +%7,9; Ç102 çölde alım 2023 +%7,3); bu testler 2023 / 2024-26'da, KEŞİF'i kapsamıyor. Yeniden  |
| İşlem bazlı veri (TAQ, emir defteri) | YAPILMADI | ücretli; dağıtım / emilim ayrımına en yakın ücretsiz vekil MIDAS (işlem büyüklüğü, gizli emir) + 13F; ücretli veri yalnız Cemal kararıyla |
| Kasıtlı yanıltma | DAHA SIKI | kasıt kanıtı yalnız kesinleşmiş karar (mahkeme, SEC / FINRA idari karar, uzlaşma); askıya alma ve dava bülteni 'resmî kuşku kaydı'; K55 evreninde tarih şartlı 9 askıya alma eşleşmesi, hiçbiri panel penceresinde değil; fi |
| Karşıt örnekler (yükselmeyen, batan, düşen, sulanan, birleşen) | AYNEN | G1-G7 tasarımı; erişim örnekleminde G1 / G2 / G3 / G6 temsilcileri |
| Kanıt sınıfları (6) | AYNEN + 4 yardımcı etiket | karar kuralları ön kayıtta (ONKAYIT_K56 3, v1.1-4); Faz 0 sınıfı ön sınıftır; sentetik kanıt yalnız YANLIŞ BULGU ADAYI verir; ETKİ YOK / ETKİ SAĞLAM DEĞİL / BETİMLEYİCİ / YÖNTEM DENETİMİ mekanizma aranmayan bulgular için |
| Ayrı modül ve kimlik, tek giriş, Drive OUTPUT | AYNEN; Drive kopyası BEKLİYOR | K56/ (11 modül) + K56.py; çıktı yolu denetimi K51-K55 klasörlerine yazmayı engeller; bu ortamda çıktılar repoda, Drive OUTPUT/K56_MEKANIZMA'ya Colab'da 'python K56.py drive' ile sha doğrulamalı kopyalanır |
| Eski sonuçların keşif verisi olarak kullanımı kaydı | AYNEN | K56_KAYNAK_KAYDI*.csv (dosya, sha256, amaç); K55 KEŞİF yeniden kullanımı ön kayıtta işaretli |
| Doğrulama dönemi | ERTELENDİ (karar) | K55'in İÇ / BAĞIMSIZ dönemleri açılmadı; DOĞRULANMIŞ sınıf bunları gerektirir |

## 1. K51-K55 etki envanteri

Tam tablo (18 alan + ön sınıf + hipotezler): K56_ETKI_ENVANTERI.csv. Çalışma × ön sınıf:

| kaynak_calisma | ALTERNATİF AÇIKLAMA | BETİMLEYİCİ (kaynakta karar yok) | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | VERİ YETERSİZ | YANLIŞ BULGU ADAYI (M01) | YANLIŞ BULGU ADAYI (tanımsal) | YÖNTEM DENETİMİ (bulgu değil) | İLİŞKİ VAR, NEDEN BELİRSİZ |
|---|---|---|---|---|---|---|---|---|---|
| K51 | 0 | 12 | 32 | 31 | 6 | 0 | 0 | 9 | 0 |
| K52 | 1 | 5 | 7 | 11 | 8 | 0 | 0 | 2 | 0 |
| K53 | 0 | 1 | 4 | 14 | 1 | 0 | 1 | 1 | 0 |
| K54 | 0 | 0 | 6 | 10 | 12 | 0 | 0 | 24 | 0 |
| K55 | 0 | 0 | 0 | 37 | 2 | 21 | 0 | 3 | 4 |

Bütün bulgular (kısa):

| kimlik | ad | sinif | yon | buyukluk | faz0_on_sinif | mekanizma_hipotezleri |
|---|---|---|---|---|---|---|
| K51-B1 | P1 oynaklığa bağlı bariyerle rastgeleden iyi | KUCUK_ETKI | pozitif | 2023 +2,6 [alt -0,7]; 2024-26 +4,3 [+1,6], net +0,34 (sabit bariyerde -1,09); eğitim +2,2, doğrulama +1,3; ham p 0,0015, Holm p 0,126 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-B1-P2 | P2 oynaklığa bağlı bariyerle rastgeleden iyi | DONEM_CELISKILI | karisik | 2023 +2,1 [alt -0,7]; 2024-26 +3,4 [+0,7], net +0,37; eğitim -3,0 [-8,2], doğrulama -3,3 [-7,3]; Holm p 0,249 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-B1-belirsiz | P1 belirsiz mumlar (aynı gün hedef + stop) çıkarılınca | KUCUK_ETKI | pozitif | 2023 +2,5 [alt -0,6]; 2024-26 +2,4 [-0,0]; belirsiz payı P1 0,000; HT %5,2 / %2,1 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-B2 | Önceki aday 'ABD hacimli taban' (HT) üçlü bariyerde | DONEM_CELISKILI | negatif | 2023 0,276 / 0,331, -5,5 [alt -14,7], net -4,45; 2024-26 0,331 / 0,343, -1,2 [-5,9], net -2,74; eğitim +3,1, doğrulama +3,8; eski cetvel 2024-26 +%12,5 [-3,3] (önceki +%14,9) | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-B4-P1-CNN | P1: CNN sayısal modelin üstüne bilgi ekliyor | BASARISIZ | negatif | 2023 -0,013 [-0,065, +0,058]; 2024-26 -0,022 [-0,064, +0,027]; CNN tek - GBM -0,031 / -0,022 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08; M10 |
| K51-B4-P1-GBM | P1: ağaç modeli (GBM) lojistik modeli geçiyor | DONEM_CELISKILI | karisik | 2023 +0,008 [-0,038, +0,054]; 2024-26 -0,036 [-0,061, -0,011]; p_GBM AUC 0,542 / 0,504 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M08; M10 |
| K51-B4-P1-LR | P1: lojistik referans modeli adayları iyileştiriyor | DONEM_CELISKILI | karisik | 2023 seçilen 99, precision 0,404 (taban 0,318), AUC 0,534 [0,471], net fark +2,39 puan; 2024-26 134, 0,358 (0,359), AUC 0,539 [0,498], net -0,54; portföy +%9,5 (Sharpe 0,59) / -%22,9 (Sharpe -0,73) | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M08; M10 |
| K51-B4-P1-LSTM | P1: LSTM sayısal modelin üstüne bilgi ekliyor | KUCUK_ETKI | pozitif | 2023 +0,029 [-0,050, +0,098]; 2024-26 +0,021 [-0,022, +0,070]; [G,C,L]-[G,C] 2024-26 +0,021 [-0,005] p 0,073; lstm_p AUC 0,556 [0,513] / 0,524 [0,474] | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M08; M10 |
| K51-B4-P1-ZINCIR | P1: sisteme alınan en üst model basamağı | BASARISIZ | sifir | Hiçbir basamak kabul edilmedi; sistem = birincil kural | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08; M10 |
| K51-B4-P2-CNN | P2: CNN sayısal modelin üstüne bilgi ekliyor | BASARISIZ | sifir | 2023 -0,006 [-0,023, +0,012]; 2024-26 -0,006 [-0,020, +0,006]; cnn_p AUC 0,502 / 0,509 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-B4-P2-GBM | P2: ağaç modeli lojistik modeli geçiyor | BASARISIZ | pozitif | 2023 +0,025 [-0,034, +0,087]; 2024-26 +0,007 [-0,032, +0,050]; p_GBM AUC 0,620 [0,527] / 0,524 [0,463] | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-B4-P2-LR | P2: lojistik referans modeli adayları iyileştiriyor | DONEM_CELISKILI | karisik | 2023 seçilen 130, precision 0,392 (taban 0,286), AUC 0,595 [0,491], net fark +2,40; 2024-26 441, 0,338 (0,327), AUC 0,517 [0,460], net -0,14; portföy +%5,7 / -%51,9 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-B4-P2-LSTM | P2: LSTM sayısal modelin üstüne bilgi ekliyor | TERS_YONLU | negatif | 2023 -0,038 [-0,048, -0,026]; 2024-26 -0,005 [-0,021, +0,010]; ama LSTM tek AUC 2023 0,606 [0,563], 2024-26 0,524 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-B4-P2-ZINCIR | P2: sisteme alınan en üst model basamağı | BASARISIZ | sifir | Birincil kural; hiçbir model alınmadı | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-B5-P1-akis | P1 özellik grubu 'akış' (CMF, OBV, A/D, MFI) ek bilgi | BASARISIZ | sifir | 2023 -0,004 [-0,020], yalnız 0,504; 2024-26 -0,002 [-0,016], yalnız 0,496 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08; M10 |
| K51-B5-P1-col | P1 özellik grubu 'çöl ölçüleri' ek bilgi | BASARISIZ | karisik | 2023 -0,010 [-0,032], yalnız 0,514; 2024-26 +0,010 [-0,005], yalnız 0,489 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08; M10 |
| K51-B5-P1-hacim | P1 özellik grubu 'hacim' ek bilgi | BASARISIZ | negatif | 2023 -0,013 [-0,030], yalnız 0,473; 2024-26 +0,003 [-0,017], yalnız 0,484 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08; M10 |
| K51-B5-P1-likidite_piyasa | P1 özellik grubu 'likidite-piyasa' ek bilgi | KUCUK_ETKI | pozitif | 2023 +0,020 [-0,022], yalnız 0,562; 2024-26 +0,011 [-0,011], yalnız 0,522 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M08; M10 |
| K51-B5-P1-momentum_dusus | P1 özellik grubu 'momentum-düşüş' ek bilgi | KUCUK_ETKI | pozitif | 2023 +0,009 [-0,010], yalnız 0,503; 2024-26 +0,012 [-0,003] (p 0,050), yalnız 0,502 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M08; M10 |
| K51-B5-P1-mum | P1 özellik grubu 'mum' ek bilgi | BASARISIZ | sifir | 2023 -0,001 [alt -0,018], yalnız 0,506; 2024-26 -0,015 [-0,032], yalnız 0,490 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08; M10 |
| K51-B5-P1-oynaklik | P1 özellik grubu 'oynaklık' ek bilgi | BASARISIZ | sifir | 2023 +0,002 [-0,024], yalnız 0,482; 2024-26 +0,002 [-0,013], yalnız 0,512 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08; M10 |
| K51-B5-P1-trend | P1 özellik grubu 'trend' ek bilgi | KUCUK_ETKI | pozitif | 2023 +0,002 [-0,009], yalnız 0,529; 2024-26 +0,003 [-0,010], yalnız 0,521 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M08; M10 |
| K51-B5-P2-akis | P2 özellik grubu 'akış' ek bilgi | DONEM_CELISKILI | karisik | 2023 +0,023 [-0,009], yalnız 0,577; 2024-26 +0,013 [-0,013], yalnız 0,471 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-B5-P2-col | P2 özellik grubu 'çöl ölçüleri' ek bilgi | BASARISIZ | sifir | 2023 +0,006 [-0,021], yalnız 0,497; 2024-26 +0,003 [-0,019], yalnız 0,503 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-B5-P2-hacim | P2 özellik grubu 'hacim' ek bilgi | BASARISIZ | sifir | 2023 +0,003 [-0,016], yalnız 0,507; 2024-26 +0,001 [-0,017], yalnız 0,495 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-B5-P2-likidite_piyasa | P2 özellik grubu 'likidite-piyasa' ek bilgi | BASARISIZ | pozitif | 2023 +0,035 [-0,006], yalnız 0,520; 2024-26 +0,002 [-0,031], yalnız 0,523 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-B5-P2-momentum_dusus | P2 özellik grubu 'momentum-düşüş' ek bilgi | KUCUK_ETKI | pozitif | 2023 +0,024 [+0,002] (p 0,017), yalnız 0,496; 2024-26 +0,027 [-0,007] (p 0,083), yalnız 0,535 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-B5-P2-mum | P2 özellik grubu 'mum' ek bilgi | BASARISIZ | sifir | 2023 +0,001 [-0,028], yalnız 0,480; 2024-26 +0,005 [-0,025], yalnız 0,499 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-B5-P2-oynaklik | P2 özellik grubu 'oynaklık' ek bilgi | DONEM_CELISKILI | karisik | 2023 +0,020 [-0,000], yalnız 0,561; 2024-26 -0,011 [-0,036], yalnız 0,448 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-B5-P2-trend | P2 özellik grubu 'trend' ek bilgi | DONEM_CELISKILI | karisik | 2023 +0,017 [+0,003] (p 0,020), yalnız 0,517; 2024-26 -0,006 [-0,033], yalnız 0,483 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-B7-negatif | Kontrol: karışık etiket (AUC ~0,5 beklenir) | BASARILI | sifir | P1 0,536 [0,482, 0,574] / 0,506 [0,480, 0,541]; P2 0,546 [0,504, 0,577] / 0,519 [0,467, 0,559] | YÖNTEM DENETİMİ (bulgu değil) |  |
| K51-B7-plasebo | Kontrol: plasebo (aynı gün aynı oynaklık rastgele hisse) | BASARILI | sifir | Eğitim -3,2 [-6,6, +0,7]; doğrulama +0,3; 2023 -1,3 [-3,6, +1,6]; 2024-26 0,0 [-2,2, +2,0] | YÖNTEM DENETİMİ (bulgu değil) |  |
| K51-B7-pozitif | Kontrol: geleceği gören 5 gün getirisi (AUC yükselmeli) | BASARILI | pozitif | P1 AUC 0,784 [0,749, 0,819] / 0,828 [0,804, 0,849], net fark +10,4 / +10,5 puan; P2 0,784 / 0,785 | YÖNTEM DENETİMİ (bulgu değil) |  |
| K51-B8-Holm | Çoklu test: Holm sonrası anlamlı test | BASARISIZ | sifir | 0 / 84; en küçük Holm p 0,126 (ABD P1 oynak 2024-26, ham 0,0015), sonra 0,249 (P2 oynak 2024-26) | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-B8-PBO-model | Model x seçim payı seçiminde aşırı uyum riski düşük | BASARISIZ | negatif | PBO 0,57 (70 kombinasyon, logit medyan -0,194) | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-B9-HT_hepsi | Sıkı portföy: bütün hacimli taban (HT) | BASARISIZ | negatif | 2023 -%20,9 (MDD -25,3, Sharpe -2,15, beta 0,18, alfa -27,6); 2024-26 -%43,4 (MDD -49,7, Sharpe -1,58, beta 0,11, alfa -22,9) | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-B9-P1_Y_GC | Sıkı portföy: GBM + CNN yığma seçilmiş P1 | DONEM_CELISKILI | karisik | 2023 +%1,9 (MDD -27,6, beta 1,20, alfa -25,1); 2024-26 -%49,9 (MDD -54,6, beta 0,62, alfa -36,1) | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M08; M10 |
| K51-B9-P1_hepsi | Sıkı portföy: bütün P1 | BASARISIZ | negatif | 2023 -%2,6 (MDD -38,9, Sharpe 0,01, beta 1,24, alfa -30,4); 2024-26 -%48,3 (MDD -55,7, Sharpe -0,82, beta 0,85, alfa -39,1) | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08; M10 |
| K51-B9-P1_p_GBM | Sıkı portföy: GBM seçilmiş P1 | BASARISIZ | negatif | 2023 -%4,7 (MDD -33,7, beta 1,25, alfa -32,9); 2024-26 -%36,5 (MDD -47,1, beta 0,84, alfa -31,2) | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08; M10 |
| K51-B9-P2_hepsi | Sıkı portföy: bütün P2 | BASARISIZ | negatif | 2023 +%6,0 (MDD -23,8, Sharpe 0,38, beta 1,06, alfa -18,3); 2024-26 -%29,6 (MDD -36,2, Sharpe -0,47, beta 0,64, alfa -24,0) | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-B9-P2_p_GBM | Sıkı portföy: GBM seçilmiş P2 | BASARISIZ | negatif | 2023 +%4,8 (MDD -12,4, Sharpe 0,56, beta 0,19, alfa +0,6); 2024-26 -%27,6 (MDD -32,3, beta 0,33, alfa -17,7) | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-D1 | Kırılımdan sonra 10 gün kutu üstünde kalırsa 11. gün al | TERS_YONLU | negatif | ABD 2016-22 0,214 / 0,289, -7,5 [-14,7, -2,1], net fark -0,58; AVR 2016-26 +4,6 [-1,6, +12,0]; ABD 2023 +2,2 [-1,1, +5,9]; 2024-26 -0,8 [-5,8, +3,5]; BIST 2016-26 -0,1; BIST 2023 +11,9 (n 59) | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-DEN-IMZA | Denetçi: imza sayısı yönü (4 imza vs 3 imza) | TERS_YONLU | ters | -1,0 / -4,4 puan (aralık kaynakta yok) | BETİMLEYİCİ (kaynakta karar yok) | M13 |
| K51-DEN-OYNAKLIK | Denetçi: yüksek oynaklık üçte biri dönem dönüşü | DONEM_CELISKILI | karisik | 2023 artı, 2024-26 eksi (sayı kaynakta yok) | BETİMLEYİCİ (kaynakta karar yok) | M03; M13 |
| K51-DEN-PORTFOY | Denetçi: portföy kaybının kaynağı (stop, maliyet) | VEKIL | negatif | Olayların %61'i stopla çıkıyor (K54 alt oran 0,59-0,65); küçük hissede gidiş-dönüş %2,2-2,4; rastgele portföy 2024-26 -%19,2 | BETİMLEYİCİ (kaynakta karar yok) | M13 |
| K51-ES | İmzasız eş (ES) hücresi rastgeleden iyi mi | BASARISIZ | sifir | ABD +0,6 [-2,1] / +1,3 [-1,5] / -0,2 [-2,8] / +0,8 [-1,6]; batansız 2024-26 +0,2; AVR +2,7 / +4,4 [+0,2] / +0,7 / -0,4; BIST +1,0 / +1,3 / +1,0 / -0,6 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-ETIKET-KISA | Kısa etiket (+%8 / -%8 / 20 gün) bilgi hücreleri | KUCUK_ETKI | pozitif | P1 2023 +0,6 [-3,1], 2024-26 +3,0 [+0,7]; P2 +2,3 [-1,1] / -0,1 [-3,3]; ES +1,0 / +0,6 | BETİMLEYİCİ (kaynakta karar yok) |  |
| K51-FI-HT | Resmî ölçüt FI_OLCUT: hacimli taban r60 eşli fark | VERI_YETERSIZ | karisik | ABD 2023 +%4,10 [-12,6, +20,9]; 2024-26 +%12,48 [-3,33, +33,51], medyan +%1,08, sıra 0,551, portföy 1,391 vs p90 1,616; AVR -%4,13 / -%7,77; BIST -%18,1 [-26,1, -11,4] / -%35,4 [-43,7, -25,4], sıra 0,141 | VERİ YETERSİZ |  |
| K51-FI-P1 | Resmî ölçüt FI_OLCUT: P1 r60 eşli fark | KUCUK_ETKI | karisik | ABD 2023 ort +%3,05 [-0,28, +7,10], medyan -%2,13, sıra 0,510, kazanan 0,462, portföy 0,895 vs p90 0,629; 2024-26 +%4,79 [+0,15, +9,87], medyan -%6,82, sıra 0,498, portföy 0,835 vs p90 2,240; AVR -%1,79 / -%0,83; BIST +% | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M08; M10 |
| K51-FI-P2 | Resmî ölçüt FI_OLCUT: P2 r60 eşli fark | BASARISIZ | karisik | ABD +%1,29 [-0,97, +3,78], medyan -%1,62, sıra 0,502, portföy -0,036 vs p90 0,457; 2024-26 +%2,91 [-2,15, +8,83], medyan -%6,81, sıra 0,490, portföy 2,124 vs p90 2,599; AVR +%0,03 / -%2,69; BIST -%2,89 / -%2,20 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-H1 | P1 (Çöl Yolu oluşurken) aynı gün aynı oynaklıktaki rastgeleden iyi | KUCUK_ETKI | pozitif | 2023 isabet 0,313 / taban 0,288, fark +2,5 puan [alt -0,5]; 2024-26 0,357 / 0,333, +2,4 [alt +0,1]; net -%1,83 / -%1,09 (taban farkı +0,09 / -0,10 puan); eğitim +1,9, doğrulama +1,7 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M08 |
| K51-H10-BIST-META | BIST çoğaltma: ABD meta modeli seçimi | TERS_YONLU | negatif | 2023 -23,6 puan [alt -30,9]; 2024-26 -1,6 [-6,7]; P1_META isabet 0,375 / taban 0,414 (2023), 0,315 / 0,354 (2024-26) | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-H10-BIST-P1 | BIST çoğaltma: P1 rastgeleden iyi | DONEM_CELISKILI | karisik | 2023 0,611 / 0,579, +3,2 [alt -7,7], net +6,28 (taban farkı +0,92); 2024-26 0,332 / 0,346, -1,4 [-4,5], net -1,01 (-0,72); eğitim +3,2, doğrulama +0,6 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M08; M10 |
| K51-H10-BIST-P2 | BIST çoğaltma: P2 kırılım rastgeleden iyi | BASARISIZ | negatif | 2023 0,800 / 0,818, -1,8 [alt -25,2], net +11,96 (taban farkı -0,59); 2024-26 0,287 / 0,333, -4,6 [-10,3], net -2,96 (-1,90); eğitim -2,5, doğrulama -4,3 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-H10-META | Avrupa çoğaltma: ABD'de eğitilmiş meta model seçimi | DONEM_CELISKILI | karisik | 2023 -6,0 puan [alt -16,5]; 2024-26 +4,0 [-8,8] | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-H10-P1 | Avrupa çoğaltma: P1 rastgeleden iyi (donmuş kurallar) | BASARISIZ | karisik | 2023 0,207 / 0,149, +5,8 [alt -0,7], net -2,65 (taban farkı +0,29); 2024-26 0,227 / 0,201, +2,6 [-3,9], net -2,23 (-1,01); eğitim +9,2 [+2,5], doğrulama +5,8 [-2,5] | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08; M10 |
| K51-H10-P2 | Avrupa çoğaltma: P2 kırılım rastgeleden iyi | DONEM_CELISKILI | karisik | 2023 0,250 / 0,148, +10,2 [alt +3,4], net -1,53 (taban farkı +1,16); 2024-26 0,153 / 0,190, -3,8 [-11,7], net -5,30 (-3,06); eğitim +0,7, doğrulama -1,8 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-H2 | Sıkışma imzası fark yaratıyor (P1 - imzasız eş ES) | BASARISIZ | pozitif | 2023 +2,7 puan [-1,1, +6,5]; 2024-26 +1,6 [-1,9, +5,4] | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08 |
| K51-H3 | Kırılım (P2) rastgeleden iyi | BASARISIZ | sifir | 2023 0,286 / 0,276, +1,0 [alt -2,4]; 2024-26 0,324 / 0,318, +0,6 [-1,7]; net -%1,99 / -%2,09 (taban farkı +0,31 / -0,45); eğitim -2,8, doğrulama -0,1 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M08 |
| K51-H4 | Meta-etiketleme P1 seçimini iyileştiriyor | BASARISIZ | pozitif | 2023 seçilen 172/906, +6,6 puan [alt -2,1], net farkı +2,2 puan, AUC 0,533 [0,461]; 2024-26 452/1.316, +2,6 [-1,1], net +0,16, AUC 0,525 [0,482] | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-H5 | CNN (grafik resmi) P1 seçimini iyileştiriyor | BASARISIZ | sifir | 2023 617/906, +0,1 [alt -2,0], net -0,33 puan, AUC 0,511 [0,466]; 2024-26 893/1.316, -1,5 [-3,2], net -0,64, AUC 0,482 [0,449] | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-H6 | CNN ile sayısal model aynı adaylarda (AUC farkı) | TERS_YONLU | negatif | 2023 -0,050 [-0,124, +0,057]; 2024-26 -0,056 [-0,103, -0,005] | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-H7 | Meta portföyü maliyet sonrası piyasayı, rastgeleyi ve SPY'yi geçiyor | DONEM_CELISKILI | karisik | 2023 +%12,5 (MDD -19,9, 93 işlem, kazanma %44); 2024-26 -%29,5 (MDD -44,3, 308 işlem, %40) | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51-H8 | Aşırı uyum riski düşük (PBO < 0,5 ve DSR >= 0,95) | BASARISIZ | negatif | PBO 0,39 (12.870 bölünme, logit medyan 0,383); DSR 0,026 (SR -0,055, SR0 0,160, T 84, N 36); seçilen = ana yapı P1/-0.35/60/0.8/3. cy_izgara.csv'den sayıldı: 36 yapının 32'sinde iki test döneminde fark > 0, hiçbirinde ik | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-H9 | Hayatta kalma yanlılığı (batanlar çıkarılınca P1 farkı) | VEKIL | pozitif | 2023 dahil +2,5 (n 906), batansız +3,6 [+0,3] (n 864); 2024-26 +2,4 (1.316) / +2,4 [-0,4] (1.293); doğrulama +1,7 / +1,5 | VERİ YETERSİZ | M17 |
| K51-HAVUZ-AUC | Genel model havuzda öngörüyor, P1 içinde öngörmüyor | VEKIL | pozitif | Havuz genel 0,600 [0,546, 0,653] / 0,639 [0,621, 0,658]; CNN 0,565 / 0,530; P1 içinde genel 0,561 [0,486, 0,624] / 0,537 [0,495, 0,571] | BETİMLEYİCİ (kaynakta karar yok) |  |
| K51-KALIB | Model kalibrasyonu (olasılık ondalıkları) | KUCUK_ETKI | pozitif | P1 LR: en düşük ondalık 0,103 / 0,300, en yüksek 0,531 / 0,377; GBM 0,091 / 0,291 -> 0,519 / 0,381; Y_GC 0,244 / 0,368 -> 0,307 / 0,413 (U biçimi). P2 LR 0,052 / 0,261 -> 0,528 / 0,365; GBM 0,037 / 0,174 -> 0,525 / 0,374 | BETİMLEYİCİ (kaynakta karar yok) |  |
| K51-KIR-LIKIDITE | Kırılım: likidite üçte birine göre P1 | KUCUK_ETKI | pozitif | P1 düşük +1,7 [-0,6] (1.215), orta +3,1 [+0,6] (1.210), yüksek +2,3 [-0,3] (1.212); P2 +0,7 / -1,3 / +0,8; net hepsinde eksi | BETİMLEYİCİ (kaynakta karar yok) | M12 |
| K51-KIR-RUZGAR | Kırılım: sektör rüzgârına göre P1 ('rüzgâr yok +3,8') | VEKIL | karisik | P1 rüzgâr var +0,7 [-7,4] (n 88); yok +3,8 [+1,7] (2.518); bilinmiyor -1,0 [-3,2] (1.031); P2 +2,8 / +0,2 / -0,7 | BETİMLEYİCİ (kaynakta karar yok) | M18 |
| K51-KR-HISSE | Kırılganlık: hisse yoğunlaşması (en iyi 20, eşit ağırlık, katkı payı) | KUCUK_ETKI | karisik | P1 en iyi 20 çıkınca -0,5 / -0,2 / 0,0; eşit ağırlık +2,4 [-0,1] / +3,7 [+0,7, +6,7] / +2,4 [-0,5]; ilk 20 payı 1,39 / 0,89 / 0,96. P2 en iyi 20 çıkınca -5,5 [-9,4, -2,0] / -3,1 / -3,1 [-5,5, -0,3]; HT -9,3 / -31,8 / -12 | BETİMLEYİCİ (kaynakta karar yok) | M05; M14; M17; M18 |
| K51-KR-KAYNAK | Kırılganlık: P1 artısının veri kaynağına göre dağılımı | VEKIL | karisik | P1 V_ABD 2023 +5,3 [+1,9, +8,7] (n 644), 2024-26 +6,4 [+2,8, +10,2] (745); K34 Yahoo +0,6 / -2,3 [-5,5, +1,0]; Tiingo -9,2 [-18,9, -1,8] (69) / -3,6 (45); 2016-22 V_ABD +1,1, Yahoo +3,3, Tiingo +7,0. Denetçi: sıkıntılı + | BETİMLEYİCİ (kaynakta karar yok) | M05; M06; M13; M14; M17; M18 |
| K51-KR-YIL | Kırılganlık: yıl yıl P1 farkı | DONEM_CELISKILI | karisik | 2023 +2,5; 2024 +5,0 [+0,6, +9,8]; 2025 +2,9 [+0,4, +5,6]; 2026 -4,3 [-7,5, -2,3]; eğitim yılları 2016 +7,5, 2017 +5,7, 2018 -0,4, 2019 +2,7, 2020 -4,6, 2021 +3,4, 2022 +0,5 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M05; M14; M17; M18 |
| K51-META-ONEM | Meta modelin özellik önemi | VEKIL | karisik | piy_r60 166, piy_r20 125, col_savunma 105, ar1 102,2, ar20 97,2, col_konum 96,2, log_dv20 90,2; doji20 15,3; col_doji_ok 2,5, col_hacim_ok 0,67, col_imza 0,5, col_bb_ok 0 | BETİMLEYİCİ (kaynakta karar yok) |  |
| K51-P2-SUREN | Süren ve başarısız kırılım (gelecek bilgisiyle ayrılmış) | VEKIL | pozitif | Süren: eğitim +0,7 (109), doğrulama +16,1 [+9,1] (107), 2023 +12,6 [+6,9] (196), 2024-26 +19,0 [+12,9] (254). Başarısız: -5,4 / -9,0 / -7,0 / -10,6 (152 / 203 / 280 / 413) | YÖNTEM DENETİMİ (bulgu değil) |  |
| K51-SEKTOR | Sektör yoğunlaşması ve bilinmeyen sektör payı | VERI_YETERSIZ | karisik | P1 HHI 0,13-0,25; 2016-21 en büyük Healthcare %22-37 (2017 Basic Materials %28, 2018 Technology %23); 2022-26 bilinmiyor %29-45. HT HHI 0,18-0,54; Healthcare %23-56 (2016-21); bilinmiyor %57-72 (2022-26) | VERİ YETERSİZ | M18 |
| K51-SONUC | Çöl Yolu öngörü değeri (önceden yazılı birleşik kural) | BASARISIZ | sifir | ABD (H1/H3 ve H2): False; Avrupa (H10): False | ETKİ YOK (başarısız kalır; açıklanacak etki yok) |  |
| K51-V1 | Veri: sayı uzlaşması ve yinelenen semboller | BASARILI | sifir | 3.267 = 1.410 + 1.435 + 422; 2.752 likit; 515 hiç likit günü yok; panel 3.175.671 satır; 4 yinelenen K34 sembolü (BG, RDUS, SBGI, ZYME) farklı CIK, ikinci şirket atlandı | YÖNTEM DENETİMİ (bulgu değil) | M13 |
| K51-V3 | Veri: 2016-20 eğitim evreni yalnız hayatta kalanlar | VERI_YETERSIZ | pozitif | 2016-20 dönemi %100 bugün işlem görenler; doldurulmadı | VERİ YETERSİZ | M13 |
| K51-V4 | Veri: Tiingo 'batan' örnekleminin çıkış sınıflaması | VERI_YETERSIZ | negatif | Tiingo: batma benzeri 51, belirsiz 27, işlem görüyor 165 (153 SEC bildirimi sürmüyor), satın alma benzeri 179; kod yeniden kullanımı şüphesi 249 hisse | VERİ YETERSİZ | M13 |
| K51-V5 | Veri: delist getirisi duyarlılığı (-%30 / %0 / -%100) | BASARILI | sifir | Hücreler en çok 0,3 puan oynuyor; etkilenen olay 0 (seri sonunda çıkan olay P1 27 / 42 / 23) | YÖNTEM DENETİMİ (bulgu değil) | M13 |
| K51-V6 | Veri: ham ve düzeltilmiş fiyatla etiket uyumu | BASARILI | sifir | Satır uyumu 0,997; olay uyumu 0,996 | YÖNTEM DENETİMİ (bulgu değil) | M13 |
| K51-V7 | Veri: eski kod (b3835d8) ile yeni kod karşılaştırması | BASARILI | sifir | Olay sayıları birebir; P1 2023 +3,1 (eski) vs +2,5 (yeni), 2024-26 +2,5 vs +2,4; farklar <= 0,6 puan | YÖNTEM DENETİMİ (bulgu değil) | M13 |
| K51-V8 | Veri: kod yeniden kullanımı kesme senaryosu | BASARILI | sifir | P1 2023 n 905 +2,4; 2024-26 n 1.300 +2,2 [-0,3]; P2 2016-22 -1,6 (2 olay etkilendi); HT 2023 -6,1 | YÖNTEM DENETİMİ (bulgu değil) | M13 |
| K51-YY | Yükselen ve yükselmeyen P1'lerin özellik farkı | TERS_YONLU | ters | doji20 0,10 vs 0,15 (-0,73 sd); piy_r60 0,010 vs 0,027 (-0,24 sd); piy_r20 0,007 vs 0,018 (-0,20 sd); log_dv20 7,08 vs 7,17 (-0,13 sd); uw20 +0,12 sd; ar1 0,874 vs 0,820 (+0,09 sd); col_imza 3 vs 3 (0) | BETİMLEYİCİ (kaynakta karar yok) |  |
| K51v12-H-A | Sert düşüş + yataylaşma (ÇEK) > eşleşmiş genel kontrol | KUCUK_ETKI | pozitif | 2016-22 0,0 puan [-2,4, +2,3], net fark -0,16; 2023 +2,9 [-1,3, +6,8] (hisse x çeyrek [-0,3, +6,1]), net +0,90; 2024-26 +3,2 [+0,4, +5,6] ([+1,0, +5,4]), net +1,39 [+0,35, +2,40]; 2023-26 +3,1 [+0,8, +5,2], net +1,24; Ho | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51v12-H-B | P1 (küçük mum imzaları) > ÇEK içi imzasız eşler | DONEM_CELISKILI | karisik | 2016-22 -1,2 [-11,2, +8,5]; 2023 -1,5 [-7,7, +5,2]; 2024-26 +4,1 [-3,4, +12,2]; 2023-26 +2,1 [-3,2, +7,6]; Holm p 0,574; net fark ~0 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51v12-H-C | ÇEK + hacim kuruması > ÇEK hacim kurumasız | DONEM_CELISKILI | karisik | 2016-22 -3,2 [-15,6, +9,6], net -1,37; 2023 +6,1 [-10,2, +19,1], net +2,41; 2024-26 +9,3 [-1,4, +19,4], net fark +4,34 [+0,69, +8,17]; 2023-26 +8,3 [-0,7, +16,2], net +3,71 [+0,71, +6,71]; Holm p 0,098 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51v12-H-D | Hacimli taban (HT) > eşleşmiş genel kontrol | DONEM_CELISKILI | karisik | 2016-22 +9,2 [-3,1, +20,8], net +3,37; 2023 +2,7 [-9,7, +12,4], net +1,82; 2024-26 -3,0 [-10,9, +4,1], net -0,35; 2023-26 -1,6 [-7,7, +4,4]; Holm p 0,627; ÇEK öncesi payı %30,1 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K51v12-H-E-AYI | P1 AYI rejiminde (SPY < 200 gün ortalaması) > eşleşmiş kontrol | VERI_YETERSIZ | pozitif | 2016-22 +3,0 [-0,8, +7,9], net +0,76; 2023 +5,5 [-8,0, +16,7] (isabet 0,633 / 0,579), net +4,77; 2024-26 +1,3 [-12,3, +10,1] n 28 | VERİ YETERSİZ |  |
| K51v12-H-E-BOGA | P1 BOĞA rejiminde > eşleşmiş kontrol | KUCUK_ETKI | pozitif | 2016-22 +3,9 [-2,6, +9,4], net +0,88; 2023 +2,0 [-3,4, +7,3], net +0,80; 2024-26 +3,1 [-0,6, +7,0], net +0,34; 2023-26 +2,6 [-0,4, +5,9] | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) |  |
| K52-4G-DENGE | Dört grup dengesizliği: teyit alan izler önceden yükselmiş, daha çok takip edilen, daha likit hisseler | VEKIL | pozitif | P1 r60 G1 +0,082 / +0,097 / +0,118 vs G2a +0,006 / +0,021 / +0,023; P1 kapsama 15,1 / 33,2 / 25,7 vs 11,5 / 18,4 / 15,3; P1 log_dv20 7,37 / 7,64 / 7,35 vs 7,21 / 7,11 / 6,93; P2 kapsama 16,8 / 34,8 / 26,2 vs 10,0 / 19,2  | BETİMLEYİCİ (kaynakta karar yok) | M04; M19 |
| K52-4G-G3 | İz yokken analist teyidi (G3) teyitsiz günlerden (G4a) farklı değil | BASARISIZ | sifir | Taban-ayarlı G3 +0,001 / −0,004 / −0,003 vs G4a −0,000 / −0,003 / −0,002; net G3 −0,001 / −0,009 / −0,004 vs G4a −0,003 / −0,004 / −0,006 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M19 |
| K52-4G-IZNET | İz gruplarında (G1, G2a) taban üstü küçük isabet, maliyet sonrası net getiri sıfır / eksi | KUCUK_ETKI | karisik | P1 taban-ayarlı G1 +0,029 / +0,061 / +0,021, G2a +0,013 / +0,040 / +0,042; P1 net G1 −0,021 / −0,001 / −0,006, G2a −0,026 / −0,014 / −0,006; P2 net G1 +0,004 / +0,004 / +0,000, G2a −0,041 / −0,025 / −0,021 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M04; M19 |
| K52-4G-VERIYOK | Analist kaydı olmayan gruplar (G2b, G4b) tabanın altında kalıyor | VEKIL | negatif | Taban-ayarlı: P1 G2b +0,028 / −0,041 / −0,079; P2 G2b +0,044 / −0,002 / −0,159; G4b +0,002 / −0,021 / −0,043. Net: P1 G2b −0,030 / −0,041 / −0,043; G4b −0,012 / −0,021 / −0,021 | BETİMLEYİCİ (kaynakta karar yok) | M04; M19 |
| K52-DOG-P1 | DOG-P1: kurum geçmiş doğruluğu üst yarı vs alt yarı (G1 içinde), bilgi | BASARISIZ | sifir | Δ −0,036 [−0,129, +0,050] / −0,039 [−0,186, +0,160] / +0,016 [−0,100, +0,153]; 2023-26 −0,006 [−0,106, +0,110]; net fark −0,001 / −0,019 / +0,001 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M19 |
| K52-DOG-P2 | DOG-P2: kurum geçmiş doğruluğu üst yarı vs alt yarı (P2), bilgi | BASARISIZ | pozitif | Δ +0,066 [−0,108, +0,264] / +0,086 [−0,133, +0,324] / +0,018 [−0,114, +0,164]; 2023-26 +0,045 [−0,073, +0,172]; ham fark −0,004 / +0,127 / +0,001; net fark +0,014 / +0,018 / +0,008 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M19 |
| K52-H0-P1 | H0-P1: yeni olumlu analist revizyonu P1 (oluşan iz) üstüne ek bilgi katar mı (G1 vs G2a) | BASARISIZ | sifir | Δ +0,017 [−0,068, +0,109] / +0,021 [−0,082, +0,127] / −0,020 [−0,073, +0,042]; 2023-26 −0,004 [−0,058, +0,049]; net fark +0,001 / +0,015 / −0,004; p 0,386 / 0,338 / 0,744; Holm p 1,000 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M19 |
| K52-H0-P2 | H0-P2: yeni olumlu analist revizyonu P2 (kırılım) üstüne ek bilgi katar mı (G1 vs G2a) | DONEM_CELISKILI | pozitif | Δ +0,114 [+0,017, +0,208] / +0,055 [−0,077, +0,149] / +0,020 [−0,051, +0,113]; 2023-26 +0,034 [−0,030, +0,103]; net fark +0,033 / +0,019 / +0,020; p 0,007 / 0,187 / 0,311; Holm p 0,934 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M04; M19 |
| K52-H0b-P1 | H0b-P1: G1 vs G2b (sembolün d'den önce hiç analist kaydı yok), bilgi amaçlı | VEKIL | pozitif | Δ +0,002 [−0,098, +0,107] / +0,102 [−0,000, +0,223] / +0,100 [−0,002, +0,206]; 2023-26 +0,094 [+0,024, +0,173]; net fark −0,004 / +0,046 / +0,022; p 0,490 / 0,028 / 0,036 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M04; M19 |
| K52-H0b-P2 | H0b-P2: G1 vs G2b (veri yok), P2, bilgi amaçlı | VEKIL | pozitif | Δ +0,020 [−0,107, +0,171] / +0,058 [−0,061, +0,150] / +0,197 [+0,021, +0,352]; 2023-26 +0,105 [+0,004, +0,211]; net fark −0,024 / +0,022 / +0,057; p 0,348 / 0,155 / 0,007 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M04; M19 |
| K52-H1 | H1: yukarı EPS / kâr tahmini revizyonu ek bilgi katar | VERI_YETERSIZ | sifir | kaynakta yok (ölçülmedi) | VERİ YETERSİZ | M04; M19 |
| K52-H2-P1 | H2-P1: yalnız tavsiye teyidi vs yalnız hedef fiyat teyidi | VERI_YETERSIZ | karisik | Δ −0,018 [−0,141, +0,089] / +0,100 [−0,076, +0,281] / +0,048 [−0,124, +0,224]; 2023-26 +0,065 [−0,059, +0,194]; net fark −0,018 / +0,050 / +0,019; Holm p 1,000 | VERİ YETERSİZ | M04; M19 |
| K52-H2-P2 | H2-P2: yalnız tavsiye teyidi vs yalnız hedef fiyat teyidi (P2) | VERI_YETERSIZ | negatif | Δ −0,079 [−0,281, +0,126] / −0,001 [−0,355, +0,303] / −0,070 [−0,294, +0,162]; 2023-26 −0,048 [−0,232, +0,131]; net fark −0,046 / −0,017 / −0,005; Holm p 1,000 | VERİ YETERSİZ | M04; M19 |
| K52-H3-P1 | H3-P1: ≥ 2 farklı kurumdan olumlu teyit vs tek kurum | TERS_YONLU | negatif | Δ −0,084 [−0,243, +0,102] / −0,024 [−0,156, +0,125] / −0,072 [−0,199, +0,052]; 2023-26 −0,051 [−0,143, +0,037]; net fark −0,027 / −0,015 / −0,028; Holm p 1,000 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M04; M19 |
| K52-H3-P2 | H3-P2: ≥ 2 farklı kurumdan teyit vs tek kurum (P2) | BASARISIZ | sifir | Δ −0,011 [−0,168, +0,185] / +0,025 [−0,208, +0,224] / −0,032 [−0,191, +0,109]; 2023-26 −0,008 [−0,146, +0,116]; net fark −0,001 / +0,016 / −0,018; Holm p 1,000 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M19 |
| K52-H4-P1 | H4-P1 (fark): fiyattan ÖNCE gelen olumlu revizyon vs SONRA gelen | BASARISIZ | karisik | Δ +0,009 [−0,081, +0,119] / −0,120 [−0,326, +0,062] / −0,031 [−0,164, +0,134]; 2023-26 −0,067 [−0,173, +0,049]; ham fark 2023 −0,163; net fark −0,002 / −0,039 / −0,011; Holm p 1,000 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M19 |
| K52-H4-P2 | H4-P2 (fark): fiyattan ÖNCE gelen olumlu revizyon vs SONRA gelen (P2) | BASARISIZ | karisik | Δ +0,039 [−0,134, +0,222] / −0,037 [−0,312, +0,235] / −0,031 [−0,199, +0,133]; 2023-26 −0,034 [−0,173, +0,110]; net fark +0,002 / −0,017 / +0,004; Holm p 1,000 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M19 |
| K52-H4Z-P1 | H4-P1 (zamanlama): olumlu revizyonların pencere dibinden ≥ %10 yükseliş SONRASI gelen payı | BASARISIZ | negatif | pay 0,386, n 481 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M19 |
| K52-H4Z-P2 | H4-P2 (zamanlama): olumlu revizyonların pencere dibinden ≥ %10 yükseliş SONRASI gelen payı | BASARILI | pozitif | pay 0,504, n 310 | ALTERNATİF AÇIKLAMA | M04; M19 |
| K52-H5-P1 | H5-P1: G1 − eşleşmiş G2a (kapsama, sektör, oynaklık, likidite, düşüş, trend) | VERI_YETERSIZ | sifir | kaynakta yok (eşleşen olay n 7 / 8 / 12) | VERİ YETERSİZ | M04; M19 |
| K52-H5-P2 | H5-P2: G1 − eşleşmiş G2a (P2) | VERI_YETERSIZ | sifir | kaynakta yok (eşleşen olay n 4 / 6 / 3) | VERİ YETERSİZ | M04; M19 |
| K52-H6AYI-P1 | H6-P1 AYI: G1 vs G2a, SPY 200 gün altı rejim | VERI_YETERSIZ | karisik | Δ −0,024 [−0,203, +0,197] / +0,028 [−0,209, +0,619] / +0,156 [−0,514, +0,694]; 2023-26 +0,086 [−0,270, +0,543]; Holm p 1,000 | VERİ YETERSİZ | M04; M19 |
| K52-H6AYI-P2 | H6-P2 AYI: G1 vs G2a, AYI rejimi (P2) | VERI_YETERSIZ | pozitif | Δ +0,077 [−0,100, +0,302] / +0,551 [−0,347, +0,572] / +0,273 [−0,258, +1,002]; 2023-26 +0,206 [−0,154, +0,805]; Holm p 0,934 | VERİ YETERSİZ | M04; M19 |
| K52-H6BOGA-P1 | H6-P1 BOĞA: G1 vs G2a, SPY 200 gün üstü rejim | BASARISIZ | sifir | Δ +0,041 [−0,042, +0,130] / +0,022 [−0,081, +0,118] / −0,025 [−0,075, +0,034]; 2023-26 −0,007 [−0,057, +0,045]; net fark +0,005 / +0,015 / −0,005; Holm p 1,000 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M19 |
| K52-H6BOGA-P2 | H6-P2 BOĞA: G1 vs G2a, BOĞA rejimi (P2) | DONEM_CELISKILI | pozitif | Δ +0,135 [+0,014, +0,273] / +0,052 [−0,080, +0,146] / +0,014 [−0,059, +0,103]; 2023-26 +0,028 [−0,040, +0,094]; net fark +0,041 / +0,019 / +0,018; p 0,010 / 0,192 / 0,368; Holm p 1,000 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M04; M19 |
| K52-KIR-EN20-P1 | Kırılganlık P1: en iyi 20 hisse G1'den çıkınca Δ üç dönemde eksi | TERS_YONLU | negatif | Δ −0,018 [−0,111, +0,082] / −0,044 [−0,138, +0,049] / −0,061 [−0,121, +0,004]; net fark −0,009 / −0,003 / −0,015 | YÖNTEM DENETİMİ (bulgu değil) | M04; M05; M19 |
| K52-KIR-EN20-P2 | Kırılganlık P2: en iyi 20 hisse çıkınca 2016-22 tutmuyor | DONEM_CELISKILI | karisik | Δ +0,060 [−0,033, +0,163] / −0,038 [−0,182, +0,075] / −0,012 [−0,083, +0,076]; net fark +0,017 / −0,008 / +0,012 | YÖNTEM DENETİMİ (bulgu değil) | M04; M05; M19 |
| K52-KIR-KAYNAK-P1 | Kırılganlık P1: kaynak grubuna göre Δ (V_ABD artı, K34 Yahoo eksi) | BASARISIZ | karisik | V_ABD +0,014 [−0,035, +0,067], net +0,004; K34_yahoo −0,058 [−0,144, +0,041], net −0,009; K34_tiingo G1 n 0 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M19 |
| K52-KIR-KAYNAK-P2 | Kırılganlık P2: fark yalnız V_ABD (bugün işlem gören) evreninde anlamlı | VEKIL | pozitif | V_ABD +0,073 [+0,009, +0,139], net +0,029; K34_yahoo +0,020 [−0,109, +0,150], net +0,005; K34_tiingo −0,423 [−0,670, −0,090], net −0,199 | BETİMLEYİCİ (kaynakta karar yok) | M04; M19 |
| K52-KIR-YIL-P1 | Kırılganlık P1: yıl yıl Δ işaret değiştiriyor | DONEM_CELISKILI | karisik | 2023 +0,021 [−0,078, +0,119]; 2024 +0,057 [−0,057, +0,168]; 2025 −0,027 [−0,093, +0,075]; 2026 −0,069 [−0,229, +0,059]; net fark +0,015 / +0,028 / −0,009 / −0,023 | BETİMLEYİCİ (kaynakta karar yok) | M04; M19 |
| K52-KIR-YIL-P2 | Kırılganlık P2: 2023-25 artı, 2026 (kısmi) anlamlı eksi | DONEM_CELISKILI | karisik | 2023 +0,055 [−0,070, +0,149]; 2024 +0,064 [−0,071, +0,210]; 2025 +0,050 [−0,060, +0,220]; 2026 −0,089 [−0,172, −0,032]; net fark +0,019 / +0,044 / +0,031 / −0,030 | BETİMLEYİCİ (kaynakta karar yok) | M04; M19 |
| K52-TERS-P1 | TERS-P1: olumsuz teyit (olumsuz > olumlu) vs G2a, bilgi | TERS_YONLU | negatif | Δ −0,057 [−0,111, −0,009] / −0,024 [−0,074, +0,035] / −0,010 [−0,069, +0,047]; 2023-26 −0,017 [−0,059, +0,025]; net fark −0,013 / −0,005 / +0,000; p 0,992 / 0,787 / 0,639 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M04; M19 |
| K52-TERS-P2 | TERS-P2: olumsuz teyit vs G2a (P2), bilgi | BASARISIZ | karisik | Δ +0,039 [−0,029, +0,105] / −0,019 [−0,075, +0,036] / −0,054 [−0,139, +0,036]; 2023-26 −0,039 [−0,096, +0,016]; net fark +0,016 / −0,005 / −0,010 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M19 |
| K52-VERI-KAPSAMA | Yahoo analist not günlüğü kapsama ve alan doluluğu: hayatta kalana ve yeni yıllara yığılmış | VERI_YETERSIZ | karisik | Kapsama V_ABD 0,992 (1399 / 1410), K34_yahoo 0,748, K34_tiingo 0,100; kayıt 2017 7.176 → 2025 45.511; önceki tavsiye dolu 2012-22 0,20-0,39 (2018 0,835), 2023 0,606, 2024-26 0,922-0,943; hedef dolu 2016 0,612 → 2026 0,98 | VERİ YETERSİZ | M04; M19 |
| K53-BIL-fiyat_zayif | Olumlu habere zayıf fiyat tepkisi (BDS bileşeni tek başına) | BASARISIZ | karisik | Δ +0.006 [−0.005, +0.018] / −0.012 [−0.043, +0.017] / −0.008 [−0.022, +0.006]; net fark +0.002 / −0.008 / −0.005; 2023-26 Δ −0.008 [−0.021, +0.005], net −0.005 [−0.010, −0.0005]. Olaylarda pay %43,0. | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M09; M11; M19 |
| K53-BIL-oyn_dusuyor | Oynaklık düşüşü (BDS bileşeni tek başına) | BASARISIZ | negatif | Δ −0.004 [−0.018, +0.009] / −0.008 [−0.037, +0.026] / −0.012 [−0.027, +0.003]; net fark +0.001 / −0.004 / −0.002; 2023-26 Δ −0.011 [−0.024, +0.004]. Olaylarda pay %40,0. | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M09; M11; M19 |
| K53-BIL-satis_azaliyor | Satış baskısının azalması (BDS bileşeni tek başına) | BASARISIZ | sifir | Δ −0.001 [−0.012, +0.011] / +0.007 [−0.018, +0.033] / +0.004 [−0.011, +0.018]; net fark +0.002 / +0.002 / +0.002; 2023-26 Δ +0.004 [−0.009, +0.017]. Olaylarda pay %38,3; iyileşme ort G1 3.46/3.44/3.42 vs G2 1.84/1.89/1.7 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M09; M11; M19 |
| K53-EK-DENGE | Grup dengesi: G1 kontrol gruplarından sistematik farklı (EK 2 / 5) | VEKIL | karisik | G1 vs G2: dd250 −0.104, log_dv20 +0.142, r60 −0.098, kapsama +0.052, vd farkı −0.526; G1 vs G3: dd250 +1.558, vol60 −0.332, log_dv20 +1.233, kapsama +0.709, vd −2.562; G1 vs G4: dd250 +0.240, log_dv20 +0.727, kapsama +0. | YÖNTEM DENETİMİ (bulgu değil) | M04; M09; M11; M19 |
| K53-EK-G1-G5-eslesik | G1 − eşleşmiş G5 (negatif kontrol, EK 2) | VERI_YETERSIZ | karisik | 2016-22 n 71: 0.181 vs 0.220, Δ −0.039 [−0.171, +0.101] p 0.678; 2023 n 17 YETERSİZ; 2024-26 n 33: 0.273 vs 0.242, Δ +0.030 [−0.257, +0.280] p 0.456. Eşleşen pay %6,1 (121 olay). Eşleşince SMD dd250 +0.045, log_dv20 +0.0 | VERİ YETERSİZ | M04; M09; M11; M19 |
| K53-EK-KGS-sonra | KGS-sonra (başlangıç d0 kapanışı): geç − hızlı (EK 3, bilgi) | BASARISIZ | negatif | Δ −0.008 [−0.030, +0.012] / −0.033 [−0.077, +0.011] / −0.014 [−0.033, +0.006]; ham isabet geç 0.221/0.236/0.260 vs hızlı 0.296/0.320/0.320; 2023-26 Δ −0.018 [−0.037, +0.001]. Kova payları: geç %25,1 (8527), hızlı %18,1 ( | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M09; M11; M19 |
| K53-EK-KGS-sonra-b | KGS-sonra geç − ulaşmadı (EK 3, bilgi) | BASARISIZ | karisik | Δ −0.008 [−0.022, +0.007] / −0.013 [−0.051, +0.024] / +0.002 [−0.017, +0.021]; net fark −0.003 / −0.002 / +0.003; 2023-26 Δ −0.002 [−0.020, +0.016]. | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M09; M11; M19 |
| K53-KIRILGANLIK-T1 | T1 kırılganlık: en iyi 20 hisse, yıl yıl, veri kaynağı | DONEM_CELISKILI | karisik | En iyi 20 çıkınca Δ −0.011 [−0.034, +0.012] / −0.010 [−0.071, +0.053] / +0.003 [−0.029, +0.033]; yıl: 2023 −0.012, 2024 +0.018 [−0.018, +0.053], 2025 +0.048 [−0.019, +0.104] (net +0.014), 2026 kısmi −0.038 [−0.101, +0.00 | BETİMLEYİCİ (kaynakta karar yok) | M04; M09; M11; M19 |
| K53-T1 | BDS 3 (bilgi direnci) olayları vs BDS < 3 — birincil test | BASARISIZ | karisik | Δ +0.008 [−0.014, +0.033] / −0.012 [−0.073, +0.050] / +0.020 [−0.014, +0.053]; ham isabet G1 0.210/0.191/0.285 vs G2 0.216/0.219/0.268; net fark +0.005/+0.001/+0.003; 2023-26 Δ +0.012 p 0.222, Holm p 1.0. BDS 3 olay payı | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M02; M04; M09; M11; M19 |
| K53-T1b | Doz-yanıt: BDS 3 − BDS 0 | BASARISIZ | karisik | Δ +0.014 [−0.015, +0.045] / −0.015 [−0.083, +0.055] / +0.004 [−0.035, +0.045]; net fark +0.008 / −0.005 / −0.001; 2023-26 Δ −0.000 [−0.034, +0.035] p 0.532; Holm p 1.0. | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M02; M04; M09; M11; M19 |
| K53-T1c | Doz-yanıt: BDS 2 − BDS 0 (ters yönde) | TERS_YONLU | ters | Δ −0.000 [−0.020, +0.018] / −0.008 [−0.030, +0.019] / −0.026 [−0.048, −0.005] (p 0.992); 2024-26 net fark −0.006 [−0.012, −0.001]; 2023-26 Δ −0.021 [−0.040, −0.004], net −0.007 [−0.013, −0.002]; ham isabet BDS 2 0.207/0. | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M02; M04; M09; M11; M19 |
| K53-T2 | G1 − G3 (grafik izi var, revizyon yok) | BASARISIZ | sifir | Δ −0.001 [−0.031, +0.029] / −0.041 [−0.092, +0.010] / −0.000 [−0.030, +0.031]; ham fark −0.075 / −0.108 / −0.066 (G1 0.210/0.191/0.285 vs G3 0.286/0.298/0.351); net fark +0.011 [+0.001, +0.021] / +0.000 / +0.004; Holm p  | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M02; M04; M09; M11; M19 |
| K53-T3 | G1 − G4 (hiçbiri: rastgele likit gün) | BASARISIZ | karisik | Δ +0.004 [−0.021, +0.029] / −0.027 [−0.083, +0.026] / +0.014 [−0.020, +0.046]; ham fark −0.008 / −0.076 / +0.000; net fark +0.006 / −0.001 / +0.003; Holm p 1.0. | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M02; M04; M09; M11; M19 |
| K53-T4 | Çürütme A: G1 − G5 (aynı şekil BDS 3, bilgi yok) | DONEM_CELISKILI | karisik | Δ +0.012 [−0.022, +0.043] / −0.040 [−0.089, +0.024] / +0.035 [+0.000, +0.071] (p 0.032); net fark +0.007 / −0.003 / +0.007; 2023-26 Δ +0.015 [−0.019, +0.045] p 0.182; Holm p 1.0. | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M02; M04; M09; M11; M19 |
| K53-T4b | Desenin kendi etkisi: G5 (BDS 3 şekli, bilgi yok) − G4 (hiçbiri) | BASARISIZ | karisik | Δ −0.008 [−0.024, +0.009] / +0.013 [−0.014, +0.046] / −0.021 [−0.046, +0.004]; net fark −0.001 / +0.002 / −0.004; 2023-26 Δ −0.011 [−0.031, +0.010]. | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M02; M04; M09; M11; M19 |
| K53-T5 | KGS (karar gecikmesi): geç (6-20) − hızlı (1-5) | BASARISIZ | sifir | Δ −0.012 [−0.031, +0.008] / −0.003 [−0.035, +0.031] / −0.001 [−0.019, +0.017]; ham isabet geç 0.206/0.229/0.254 vs hızlı 0.283/0.280/0.308 (ham fark −0.077 / −0.052 / −0.054); net fark −0.002 / −0.002 / −0.001; Holm p 1. | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M02; M04; M09; M11; M19 |
| K53-T5b | KGS geç − yok (20 günde tepki yok; karar d0+20) | BASARISIZ | karisik | Δ −0.009 [−0.024, +0.008] / −0.013 [−0.039, +0.013] / +0.014 [−0.007, +0.037]; ham fark +0.034 / +0.023 / +0.033; net fark −0.002 / −0.000 / +0.001. 'Yok' kovası isabet / taban: 0.173/0.175, 0.210/0.209, 0.220/0.239. | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M02; M04; M09; M11; M19 |
| K53-T5c | KGS hızlı − yok | BASARISIZ | karisik | Δ +0.003 [−0.014, +0.020] / −0.009 [−0.034, +0.016] / +0.015 [−0.006, +0.036] (p 0.081); ham fark +0.111 / +0.075 / +0.087; net fark +0.001 / +0.002 / +0.002. | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M02; M04; M09; M11; M19 |
| K53-T6 | ADE (analist hedef fiyat dağınıklığı): üst − alt üçte bir | VEKIL | pozitif | Δ +0.024 [+0.002, +0.044] (p 0.008) / +0.028 [−0.012, +0.065] (p 0.075) / +0.025 [+0.006, +0.042] (p 0.0055); ham isabet üst 0.321/0.275/0.340 vs alt 0.162/0.150/0.178 (ham fark +0.160 / +0.125 / +0.162); net fark +0.001 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M02; M04; M09; M11; M19 |
| K53-T7 | Olumlu habere tepki vermeme: BDS 3 olaylarında KGS kova payları (bilgi) | TERS_YONLU | ters | BDS 3: hızlı %3,1, geç %23,0, yok %73,9; BDS 0: hızlı %52,1, geç %23,3, yok %24,6. 'Yok' kovası isabet / taban: 0.173/0.175, 0.210/0.209, 0.220/0.239. | YANLIŞ BULGU ADAYI (tanımsal) | M02; M04; M09; M11; M19 |
| K53-T7b | Geç tepki ∧ BDS 3 − geri kalan olaylar | DONEM_CELISKILI | karisik | Δ +0.069 [+0.009, +0.131] (p 0.018; net +0.018 [+0.001, +0.035]) / +0.072 [−0.047, +0.209] (p 0.130) / −0.001 [−0.080, +0.080]; 2023-26 Δ +0.013 [−0.054, +0.084]. | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M02; M04; M09; M11; M19 |
| K53-T8 | Çürütme B: G1 içinde revizyon yükselişten SONRA − ÖNCE gelen | BASARISIZ | sifir | Δ −0.007 [−0.057, +0.045] / −0.037 [−0.096, +0.022] / +0.003 [−0.059, +0.059]; ham isabet sonra 0.293/0.247/0.347 vs önce 0.166/0.164/0.246 (ham fark +0.128 / +0.084 / +0.101); net fark +0.012 / −0.008 / +0.019. | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M02; M04; M09; M11; M19 |
| K54-ANALIST | K52 / K53 analist kapsaması sınıf başına (seçim yanlılığı) | VERI_YETERSIZ | negatif | Analist payı sınıf 1 0,835; 2 0,000; 3 0,013; 4 0,778; 5 0,000. K52 olay sınıfları {1: 5189, 3: 130, 4: 23, 2: 5, 5: 4}, sınıf 2-6'da analist payı 0,099; K53 {1: 33896, 4: 53, 3: 6} | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-BBEMA | BB sıkışması / EMA deneyleri (K48, K49, K50, FON_IZI) | VERI_YETERSIZ | sifir | kaynakta yok (yeniden koşulmadı) | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-DL-P1 | Delist duyarlılığı P1: −%0 / −%30 / −%100 bandı | VERI_YETERSIZ | sifir | n 1415 / 906 / 1316; erken biten olay 27 / 42 / 23; isabet d0 = d30 = d100 = 0,286 / 0,313 / 0,357; yeni 0,286 / 0,311 / 0,356; bant 0,000 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-DL-P2 | Delist duyarlılığı P2: −%0 / −%30 / −%100 bandı | VERI_YETERSIZ | sifir | n 571 / 476 / 667; erken biten olay 9 / 25 / 13; isabet 0,255 / 0,286 / 0,324 (üç senaryoda aynı); yeni 0,255 / 0,283 / 0,325; bant 0,000 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-DL4A-P1 | P1 bandı, yalnız 4a doğrulanamayan | VERI_YETERSIZ | sifir | n 0 / 0 / 0 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-DL4A-P2 | P2 bandı, yalnız 4a doğrulanamayan | VERI_YETERSIZ | sifir | n 0 / 0 / 0 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-ETF | ETF temizliği: 7 fon evren dışı (evren_disi_ABD.csv) | KUCUK_ETKI | sifir | 7 fon: DBA, DBB, DBO, UNG, UNL, UUP (SIC 6221, Tiingo ETF) + BTCW; etkisi 11 belirsiz çıkarılınca P1 / P2 en çok 0,10 puan | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-ETIKET-ETKI | Etiket etkisi (C-yeni − C-eski): çıkış işlemi düzeltmesinin etkisi | KUCUK_ETKI | sifir | /etiket etkisi/ en çok 0,0006 (0,06 puan) | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-EVREN-ETKI | Evren etkisi (C-eski − A): satır çıkarmanın sonuca etkisi | KUCUK_ETKI | sifir | /evren etkisi/ en çok 0,0109 (1,1 puan, H-C 2023, 68 → 67 olay); 55 ana hücrenin 54'ü SAĞLAM, 1 ETKİLENMİŞ (P1 2024-26), 1 GEÇERSİZ (BB / EMA) | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-HAYATTA-KALMA | Hayatta kalma yanlılığının ölçülemeyen kısmı | VERI_YETERSIZ | sifir | 3267 sembolün 266'sı çıkmış ya da belirsiz; eski sembollü seriler yalnız 422 Tiingo örnekleminden (ağırlık 1,831); batanlardan örneğe girmeyen 374 şirket; etki büyüklüğü kaynakta yok | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-HB | H-B küçük mum: P1 − ES eşleşmiş kontrol (A / B / C) | BASARISIZ | karisik | A: −1,2 [−12,0, +8,5] / −1,5 [−7,9, +5,1] / +4,1 [−3,3, +11,9]; B: −1,2 [−11,2, +9,5] / −1,5 [−7,5, +5,2] / +4,1 [−3,4, +11,6]; n 235 / 135 / 249 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M06; M13; M15; M17 |
| K54-HC | H-C hacim kuruması: ÇEK + hacim_ok − ÇEK hacimsiz eşleşmiş | BASARISIZ | karisik | A: −3,2 [−15,2, +8,9] / +6,1 [−9,1, +19,7] / +9,3 [−1,2, +19,5]; B: −3,2 [−16,7, +9,2] / +5,0 [−10,6, +18,8] / +9,3 [−1,4, +20,0]; n 135→134 / 68→67 / 151 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M06; M13; M15; M17 |
| K54-HD | H-D hacimli taban (HT) − genel eşleşmiş kontrol | BASARISIZ | karisik | A: +9,2 [−3,6, +20,3] / +2,7 [−9,9, +12,5] / −3,0 [−10,2, +4,0]; B: +9,2 [−4,5, +20,4] / +2,7 [−10,2, +12,3] / −3,0 [−10,6, +3,9]; n 99 / 43 / 140 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M06; M13; M15; M17 |
| K54-K51CEK | K51 ÇEK (sert düşüş + dipte yataylaşma çekirdeği) taban-ayarlı isabet | KUCUK_ETKI | pozitif | A: +0,61 [−0,85, +1,92] / +0,68 [−0,91, +2,47] / +1,62 [−0,22, +3,57]; B: +0,63 [−0,75, +1,92] / +0,65 [−1,00, +2,48] / +1,60 [−0,27, +3,65]; n 4193→4192 / 1983→1982 / 4192→4187 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M06; M13; M15; M17 |
| K54-K51CEK-E20 | K51 ÇEK (en iyi 20 hisse çıkarıldı) | BASARISIZ | sifir | A: −0,48 [−1,91, +0,82] / −1,05 [−2,68, +0,96] / +0,55 [−1,37, +2,54]; B: −0,46 / −1,08 / +0,52; n 4051→4050 / 1924→1923 / 4086→4081 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-K51CEK-S6M100 | K51 ÇEK sınıf 6 −%100 dahil | VERI_YETERSIZ | pozitif | +0,63 [−0,72, +2,02] / +0,65 [−1,03, +2,59] / +1,60 [−0,32, +3,69] | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-K51CEK-S6M30 | K51 ÇEK sınıf 6 −%30 dahil | VERI_YETERSIZ | pozitif | +0,63 [−0,76, +2,01] / +0,65 [−1,03, +2,46] / +1,60 [−0,33, +3,62] | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-K51ES | K51 ES (ÇEK içinde imza ≤ 1, eş) taban-ayarlı isabet | BASARISIZ | karisik | A: +1,03 [−0,94, +2,96] / −0,25 [−2,80, +2,14] / +0,83 [−1,52, +3,17]; B: +0,99 / −0,25 / +0,86; n 2316→2315 / 896 / 2382→2377 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M06; M13; M15; M17 |
| K54-K51ES-E20 | K51 ES (en iyi 20 hisse çıkarıldı) | TERS_YONLU | negatif | A: −0,42 [−2,55, +1,48] / −2,87 [−5,47, −0,55] / −0,60 [−3,09, +1,72]; B: −0,47 / −2,88 [−5,47, −0,42] / −0,58; n 2228→2227 / 857 / 2316→2311 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-K51ES-S6M100 | K51 ES sınıf 6 −%100 dahil | VERI_YETERSIZ | karisik | +0,99 [−0,98, +2,95] / −0,25 [−2,88, +2,18] / +0,86 [−1,53, +3,18] | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-K51ES-S6M30 | K51 ES sınıf 6 −%30 dahil | VERI_YETERSIZ | karisik | +0,99 [−1,09, +2,90] / −0,25 [−2,93, +2,20] / +0,86 [−1,59, +3,23] | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-K51HT | K51 HT (hacimli taban: hacim ≥ 20× medyan, gün ≤ −%9,5) | BASARISIZ | karisik | A: +3,54 [−5,38, +11,66] / −5,49 [−14,66, +3,26] / −1,23 [−5,96, +4,10]; B: +3,54 [−5,13, +11,75] / −5,47 [−14,22, +3,71] / −1,23 [−6,07, +4,06]; n 163 / 58 / 191 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M06; M13; M15; M17 |
| K54-K51HT-E20 | K51 HT (en iyi 20 hisse çıkarıldı) | TERS_YONLU | ters | A: −9,30 [−16,24, −2,53] / −31,82 [−39,69, −23,52] / −12,14 [−17,05, −6,64]; B aynı (−9,30 / −31,82 / −12,14); n 140 / 37 / 167; 2023'te 37 olayda üst oran 0 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-K51HT-S6M100 | K51 HT sınıf 6 −%100 dahil | VERI_YETERSIZ | karisik | +3,54 [−5,34, +11,66] / −5,47 [−15,02, +3,09] / −1,23 [−6,08, +4,19] | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-K51HT-S6M30 | K51 HT sınıf 6 −%30 dahil | VERI_YETERSIZ | karisik | +3,54 [−4,53, +12,70] / −5,47 [−14,84, +3,78] / −1,23 [−6,04, +4,35] | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-K51P1 | K51 P1 (ÇEK + ≥3 imza, oluşurken) taban-ayarlı isabet: eski / düzeltilmiş / ortak evren | KUCUK_ETKI | pozitif | A: +1,76 [−0,39, +4,24] / +2,46 [−0,57, +6,07] / +2,39 [+0,02, +4,98] puan; B: +1,75 [−0,47, +4,15] / +2,40 [−0,78, +5,87] / +2,30 [−0,02, +4,92]; n 1415 / 906→905 / 1316→1314 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M06; M13; M15; M17 |
| K54-K51P1-E20 | K51 P1 (en iyi 20 hisse çıkarıldı) | BASARISIZ | sifir | A: −0,53 [−2,82, +1,90] / −0,21 [−3,59, +3,47] / +0,01 [−2,16, +2,44]; B: −0,54 / −0,28 / −0,09; n 1355 / 848→847 / 1256→1254 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-K51P1-S1B | K51 P1 sınıf 1 belirsiz (11 sembol) çıkarıldı | KUCUK_ETKI | pozitif | +1,75 [−0,52, +4,18] / +2,54 [−0,56, +6,02] / +2,39 [−0,03, +4,85]; n 1415 / 901 / 1310 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M06; M13; M15; M17 |
| K54-K51P1-S6M100 | K51 P1 sınıf 6 −%100 dahil varyantı | VERI_YETERSIZ | pozitif | +1,75 [−0,35, +4,21] / +2,40 [−0,62, +5,80] / +2,30 [−0,18, +4,83] | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-K51P1-S6M30 | K51 P1 sınıf 6 −%30 dahil varyantı | VERI_YETERSIZ | pozitif | +1,75 [−0,42, +4,15] / +2,40 [−0,91, +5,72] / +2,30 [−0,15, +4,81]; n 1415 / 905 / 1314 | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-K51P2 | K51 P2 (kırılım) taban-ayarlı isabet: A / B / C | BASARISIZ | karisik | A: −1,32 [−4,48, +1,88] / +0,95 [−2,41, +5,34] / +0,61 [−1,77, +3,41]; B: −1,31 [−4,60, +1,92] / +0,81 [−2,70, +5,70] / +0,67 [−1,74, +3,66]; n 571 / 476→475 / 667→666 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M06; M13; M15; M17 |
| K54-K51P2-E20 | K51 P2 (en iyi 20 hisse çıkarıldı) | TERS_YONLU | ters | A: −5,51 [−9,27, −2,12] / −3,11 [−5,83, +0,88] / −3,10 [−5,49, −0,47]; B: −5,50 [−9,20, −2,02] / −3,28 [−5,98, +0,64] / −3,06 [−5,41, −0,07]; n 537 / 455→454 / 627→626 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-K51P2-S1B | K51 P2 sınıf 1 belirsiz çıkarıldı | KUCUK_ETKI | karisik | −1,31 [−4,38, +2,02] / +0,86 [−2,62, +5,79] / +0,72 [−1,79, +3,70]; n 571 / 474 / 665 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M06; M13; M15; M17 |
| K54-K51P2-S6M100 | K51 P2 sınıf 6 −%100 dahil | VERI_YETERSIZ | karisik | −1,31 [−4,72, +2,06] / +0,81 [−2,77, +5,63] / +0,67 [−1,74, +3,52] | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-K51P2-S6M30 | K51 P2 sınıf 6 −%30 dahil | VERI_YETERSIZ | karisik | −1,31 [−4,69, +1,83] / +0,81 [−2,70, +5,46] / +0,67 [−1,68, +3,63] | VERİ YETERSİZ | M06; M13; M15; M17 |
| K54-K51TAHMIN | K51'in eski çıkış türü tahmini (r60 / fiyat sezgisi) SEC kanıtına göre | VEKIL | karisik | 'batma benzeri' 51 → iflas 19, birleşme 21, belirsiz 11; 'satın alma / birleşme benzeri' 179 → birleşme 115, belirsiz 64; 'belirsiz çıkış' 27 → birleşme 23, belirsiz 4 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-K52H0-P1 | K52 H0 P1: G1 (P1 + olumlu analist teyidi) − G2a (kaydı var, teyit yok) | BASARISIZ | karisik | A: +1,7 [−6,9, +11,0] / +2,1 [−7,5, +11,9] / −2,0 [−7,2, +4,2]; B: +1,7 [−6,8, +10,8] / +2,3 [−7,5, +12,7] / −1,8 [−7,1, +4,2]; n G1 178 / 122 / 197, G2a 990 / 626→625 / 985→983 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M06; M13; M15; M17 |
| K54-K52H0-P2 | K52 H0 P2: G1 − G2a (kırılım + olumlu analist teyidi) | DONEM_CELISKILI | pozitif | A: +11,4 [+2,3, +22,1] / +5,5 [−7,4, +14,8] / +2,0 [−5,3, +11,0]; B: +11,4 [+2,2, +22,0] / +5,7 [−7,4, +15,0] / +2,0 [−5,0, +11,8]; n G1 108 / 79 / 128, G2a 377 / 320→319 / 493→492 | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M06; M13; M15; M17 |
| K54-K53T1 | K53 T1: BDS 3 − BDS < 3 (bilgi direnci) | BASARISIZ | karisik | A: +0,8 [−1,5, +3,3] / −1,2 [−7,6, +5,3] / +2,0 [−1,2, +5,2]; B: +0,8 [−1,5, +3,2] / −1,2 [−7,6, +5,0] / +2,0 [−1,3, +5,3]; n 1007 / 235→234 / 749 vs 15602 / 4114→4108 / 12248→12220 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M06; M13; M15; M17 |
| K54-K53T5 | K53 T5: KGS geç − hızlı (karar gecikmesi) | BASARISIZ | negatif | A: −1,2 [−3,1, +0,8] / −0,3 [−3,4, +3,0] / −0,1 [−1,9, +1,7]; B: −1,2 [−3,0, +0,8] / −0,5 [−3,7, +2,6] / −0,2 [−1,9, +1,7]; n 3999 / 920→919 / 2904→2895 vs 4185 / 1291→1287 / 4032→4022 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M06; M13; M15; M17 |
| K54-K53T6 | K53 T6: ADE (analist dağınıklığı) üst − alt üçte bir | VEKIL | pozitif | A: +2,4 [+0,3, +4,3] / +2,8 [−1,4, +6,4] / +2,5 [+0,6, +4,2]; B: +2,4 [+0,3, +4,4] / +3,0 [−1,3, +6,7] / +2,5 [+0,7, +4,4]; n 2617 / 1199→1197 / 3260→3254 vs 3259 / 933 / 2885→2881; ham isabet 0,32 vs 0,16 (Ç136) | ETKİ SAĞLAM DEĞİL (kaynakta başarısız / zayıf / dönem çelişkili; mekanizma aranmaz) | M06; M13; M15; M17 |
| K54-ML | Sessiz ML: LightGBM meta-etiketleme P1, yıl yıl ileri 2019-26 (A / B / C) | BASARISIZ | sifir | A: n 3410, AUC 0,512, üst +2,4 [−0,3, +5,3], alt +2,0, fark +0,3; B: n 3407, AUC 0,513, üst +2,1 [−0,6, +4,9], alt +1,7, fark +0,4; yıllık AUC 0,559 / 0,546 / 0,506 / 0,495 / 0,520 / 0,461→0,449 / 0,549→0,557 / 0,448→0,4 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M06; M13; M15; M17 |
| K54-S1 | Sınıf 1 halen işlem gören: 3001 sembol ve doğrulama türü | BASARILI | sifir | 3001 (V_ABD 1408, K34 Yahoo 1435, K34 Tiingo 158); Tiingo + SEC 2831, yalnız Tiingo 159, belirsiz 11; analist payı 0,835; panel 3116066 satır; P1 3530, P2 1659 olay; son kapanış medyanı 13,40 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-S1-BELIRSIZ | Sınıf 1 belirsiz 11 sembol (yalnız SEC / Tiingo çelişkisi) | KUCUK_ETKI | sifir | 11: BOXL, CIRC, DBA, DBB, DBO, FIEE, NGTF, SNBRQ, UNG, UNL, UUP; 10 'yalnız SEC, Tiingo'da yok', 1 (CIRC) 'Tiingo bitiş çelişiyor' (2026-07-01); çıkarılınca P1 / P2 en çok 0,10 puan | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-S1-OTC | Sınıf 1 içinde OTC / pembe tahta ve 'Q' ekli semboller (CSV'den sayıldı) | VERI_YETERSIZ | sifir | 303 (PINK 236, OTCMKTS 62, OTCD 2, OTCQB 2, OTCQX 1; K34 Yahoo 194, K34 Tiingo 105, V_ABD 4); 'Q' ekli 53 (örn. SPWRQ, TWOUQ, EXPRQ, NVTAQ, FSRNQ); analist payı 0,241 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-S2 | Sınıf 2 iflas / tasfiye: 19 sembol | VERI_YETERSIZ | negatif | 19 (hepsi K34 Tiingo); Tiingo borsa PINK 15, EXPM 3, NYSE MKT 1; son kapanış medyanı 0,009; panel 1644 satır; P1 5, P2 0 olay; analist payı 0 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-S2-KRONO | İflas kronolojisi: 8-K 1.03 son işlemden (T) önce | BASARILI | negatif | T'den önce 18, aynı gün 1 (ID), sonra 0; fark en az −322, medyan −174, en çok 0 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-S3 | Sınıf 3 birleşme / satın alma: 159 sembol | KUCUK_ETKI | sifir | 159 (hepsi K34 Tiingo); panel 46121 satır; P1 85, P2 46 olay; son kapanış medyanı 10,50; analist payı 0,013; SEC adında 'Acquisition' 11 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-S4A | Sınıf 4a sembol değişimi: 0 kayıt | VERI_YETERSIZ | sifir | n = 0 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-S4B | Sınıf 4b kod yeniden kullanımı: 9 sembol, seri kesimi | KUCUK_ETKI | sifir | 9: ARIS, UNIT (V_ABD); AXP, BG, KNDI, ZYME, NE, LOGC, HCIC (Tiingo); panel 8226 satır; P1 15, P2 8 olay; analist payı 0,778; A 3175671 → B 3171992 satır (sınıf 6 = 0 olduğundan fark kesimden) | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-S5 | Sınıf 5 belirsiz (veri sağlayıcısında kaybolan): 79 sembol | VERI_YETERSIZ | sifir | 79 (hepsi Tiingo); kayıt dışı (15-12G vb.) 70, 25-NSE 66; son kapanış medyanı 10,19, çeyrekler 9,98-10,51, 52'si 9,5-11 arası; SEC adında 'Acquisition' 31; P1 2, P2 2 olay; panel 3614; analist 0 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K54-S6 | Sınıf 6 işlem geçmişi doğrulanamayan: 0 | VERI_YETERSIZ | sifir | 0 (3262 CIK'in hepsi indi, hata 0); sınıf 6 varyantlarında B'ye göre en büyük değişim +0,0000 | YÖNTEM DENETİMİ (bulgu değil) | M06; M13; M15; M17 |
| K55-D01-S01 | D01-S01: Dip ne kadar sürede oluştu? (250 günde dip bandında geçirilen gün) | BASARISIZ | sifir | A en iyi D01-S01/tek: d +0.020, AUC 0.492, q 1.000; C lift en çok 1.13 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17 |
| K55-D01-S02 | D01-S02: Düşüş hızı değişiyor mu? (son p gün eğimi − önceki p gün eğimi) | TERS_YONLU | ters | A en iyi D01-S02/5: d -0.251, AUC 0.429, q 0.015; C lift en çok 1.33; vekil kıyası: en yakın dd250 ρ +0.04, dd250 katmanlı d -0.231 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17 |
| K55-D01-S03 | D01-S03: Dip kaç kez test edilip savunuldu? (120 gün) | BASARISIZ | sifir | A en iyi D01-S03/tek: d +0.074, AUC 0.515, q 1.000; C lift en çok 0.99 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17 |
| K55-D01-S04 | D01-S04: Alt fitiller büyüyor mu? (p gün alt / üst fitil) | BASARISIZ | sifir | A en iyi D01-S04/5: d +0.044, AUC 0.514, q 0.096; C lift en çok 1.06 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17 |
| K55-D01-S05 | D01-S05: Getiri asimetrisi (p gün çarpıklık) | TERS_YONLU | ters | A en iyi D01-S05/20: d -0.121, AUC 0.464, q 0.015; C lift en çok 1.03; vekil kıyası: en yakın r20 ρ +0.34, dd250 katmanlı d -0.099 | İLİŞKİ VAR, NEDEN BELİRSİZ | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17 |
| K55-D01-S06 | D01-S06: Dar alanda kalma süresi (20 gün aralığı 250 gün en düşük %10'unda ardışık gün) | BASARISIZ | sifir | A en iyi D01-S06/tek: d +0.033, AUC 0.501, q 1.000; C lift en çok 1.39; vekil kıyası: en yakın ar20 ρ -0.60, dd250 katmanlı d +0.001 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17 |
| K55-D01-S07 | D01-S07: Mum dizisinin düzeni (p gün yön dizisi entropisi; düşük = düzenli) | KUCUK_ETKI | negatif | A en iyi D01-S07/5: d -0.126, AUC 0.456, q 0.015; C lift en çok 1.03; vekil kıyası: en yakın r20 ρ -0.02, dd250 katmanlı d -0.107 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17 |
| K55-D01-S08 | D01-S08: Son sert düşüşün geri alınan payı (p gün) | TERS_YONLU | ters | A en iyi D01-S08/20: d -0.215, AUC 0.434, q 0.015; C lift en çok 1.01; vekil kıyası: en yakın r20 ρ +0.63, dd250 katmanlı d -0.204 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17 |
| K55-D01-S09 | D01-S09: Direnç aşınması: p gün tepesine %3 yaklaşma sayısı | BASARISIZ | sifir | A en iyi D01-S09/20: d -0.108, AUC 0.457, q 0.037; C lift en çok 1.01 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17 |
| K55-D01-S10 | D01-S10: Hisse kendi normalinden saptı mı? (son p gün getirisi vs önceki 120 gün, KS) | KUCUK_ETKI | pozitif | A en iyi D01-S10/20: d +0.123, AUC 0.537, q 0.015; C lift en çok 1.22; vekil kıyası: en yakın ar20 ρ +0.15, dd250 katmanlı d +0.096 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17 |
| K55-D02-S01 | D02-S01: Hacim fiyattan önce mi değişiyor? (p / 120 gün hacim oranı, fiyat hareketi cezalı) | BASARISIZ | sifir | A en iyi D02-S01/60: d -0.111, AUC 0.458, q 0.011; C lift en çok 1.04 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M06; M07; M08; M10; M14; M15; M16; M17 |
| K55-D02-S02 | D02-S02: Aşağı günlerin hacim payı (p gün; düşük = satıcı zayıf) | TERS_YONLU | ters | A en iyi D02-S02/5: d +0.319, AUC 0.592, q 0.011; C lift en çok 1.03; vekil kıyası: en yakın r20 ρ -0.35, dd250 katmanlı d +0.275 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M06; M07; M08; M09; M10; M11; M14; M15; M16; M17 |
| K55-D02-S03 | D02-S03: Aynı hacme fiyat tepkisi değişiyor mu? (Amihud p / 120) | BASARISIZ | sifir | A en iyi D02-S03/60: d -0.026, AUC 0.498, q 1.000; C lift en çok 1.22 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M06; M07; M08; M10; M11; M12; M14; M15; M16; M17 |
| K55-D02-S04 | D02-S04: Yukarı / aşağı gün medyan hacim oranı (p gün) | BASARISIZ | sifir | A en iyi D02-S04/20: d -0.057, AUC 0.478, q 0.073; C lift en çok 1.05 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M06; M07; M08; M10; M11; M14; M15; M16; M17 |
| K55-D02-S05 | D02-S05: Hacim zamana nasıl yayılmış? (p gün Gini; düşük = yayılmış) | TERS_YONLU | ters | A en iyi D02-S05/20: d +0.110, AUC 0.528, q 0.011; C lift en çok 1.07; vekil kıyası: en yakın hacim_orani ρ +0.36, dd250 katmanlı d +0.105 | İLİŞKİ VAR, NEDEN BELİRSİZ | M01; M02; M03; M04; M06; M07; M08; M10; M11; M14; M15; M16; M17 |
| K55-D02-S06 | D02-S06: Olağan dışı hacim günleri sayısı (p gün; > 2 × 20 gün medyan) | KUCUK_ETKI | pozitif | A en iyi D02-S06/5: d +0.144, AUC 0.509, q 0.011; C lift en çok 1.13; vekil kıyası: en yakın hacim_orani ρ +0.15, dd250 katmanlı d +0.136 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M06; M07; M08; M10; M11; M14; M15; M16; M17 |
| K55-D02-S07 | D02-S07: Emilim: hacim artıyor, fiyat ilerlemiyor (p gün) | BASARISIZ | sifir | A en iyi D02-S07/60: d -0.114, AUC 0.460, q 0.011; C lift en çok 1.05 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M06; M07; M08; M10; M11; M14; M15; M16; M17 |
| K55-D02-S08 | D02-S08: Satıcı tükenmesi: hacim azalıyor, fiyat düşmüyor (p gün) | TERS_YONLU | ters | A en iyi D02-S08/5: d -0.386, AUC 0.392, q 0.011; C lift en çok 1.20; vekil kıyası: en yakın hacim_orani ρ -0.54, dd250 katmanlı d -0.343 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M06; M07; M08; M10; M11; M14; M15; M16; M17 |
| K55-D02-S09 | D02-S09: Hacim–oynaklık bağı değişimi (p gün − 120 gün korelasyon) | BASARISIZ | sifir | A en iyi D02-S09/20: d +0.092, AUC 0.528, q 0.011; C lift en çok 1.04 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M06; M07; M08; M10; M14; M15; M16; M17 |
| K55-D02-S10 | D02-S10: Evren içinde ilgi artıyor mu? (işlem değeri yüzdeliğinin p gün değişimi; kesitsel) | BASARISIZ | sifir | A en iyi D02-S10/20: d +0.044, AUC 0.512, q 0.105; C lift en çok nan | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M06; M07; M08; M10; M14; M15; M16; M17 |
| K55-D03-S01 | D03-S01: Kısa vol uzun vole göre nerede? (vol p / vol 250) | BASARISIZ | sifir | A en iyi D03-S01/5: d +0.089, AUC 0.526, q 0.017; C lift en çok 1.18 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D03-S02 | D03-S02: Aşağı / yukarı yarı-varyans oranı (p gün; düşük = aşağı sakin) | VEKIL | ters | A en iyi D03-S02/20: d +0.220, AUC 0.579, q 0.017; C lift en çok 1.09; vekil kıyası: en yakın r20 ρ -0.87, dd250 katmanlı d +0.165 | YANLIŞ BULGU ADAYI (M01) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D03-S03 | D03-S03: Vol kümelenmesi (/getiri/ 1. gecikme otokorelasyonu, p gün) | BASARISIZ | sifir | A en iyi D03-S03/60: d +0.095, AUC 0.528, q 0.159; C lift en çok 1.07 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D03-S04 | D03-S04: Daralma hızı (vol20 ardışık kaç gündür düşüyor) | BASARISIZ | sifir | A en iyi D03-S04/tek: d -0.118, AUC 0.475, q 0.013; C lift en çok 1.07 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D03-S05 | D03-S05: Aralık değişimi /getiri/den önce mi? (60 gün, ±5 gün öncü-gecikme farkı) | BASARISIZ | sifir | A en iyi D03-S05/tek: d +0.036, AUC 0.511, q 0.079; C lift en çok 1.03 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D03-S06 | D03-S06: Hareket verimliliği (p gün gerçek aralık toplamı / net hareket; düşük = verimli) | BASARISIZ | sifir | A en iyi D03-S06/5: d -0.090, AUC 0.463, q 0.017; C lift en çok 1.07 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D03-S08 | D03-S08: Boşluk volatilitesi payı (p gün açılış boşluğu varyansı / kapanış varyansı) | BASARISIZ | sifir | A en iyi D03-S08/40: d -0.061, AUC 0.482, q 0.040; C lift en çok 1.07 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D03-S09 | D03-S09: Uzun düşük vol süresi (vol20 250 gün yüzdeliği < 10 ardışık gün) | BASARISIZ | sifir | A en iyi D03-S09/tek: d -0.067, AUC 0.536, q 0.091; C lift en çok 1.32 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D03-S10 | D03-S10: Aşağı vol zamanla azalıyor mu? (aşağı yarı-varyans 60 / 120) | BASARISIZ | sifir | A en iyi D03-S10/tek: d +0.187, AUC 0.571, q 0.220; C lift en çok 1.22 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D04-S01 | D04-S01: Düşüş süresi / dipten bugüne süre (250 gün) | VERI_YETERSIZ | sifir | A en iyi D04-S01/tek: d +0.129, AUC 0.531, q 0.004; C lift en çok 2.05 | VERİ YETERSİZ | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D04-S02 | D04-S02: Toparlanma yavaşlığı (250 günde tepenin %80 altında geçirilen gün; yaklaşım) | BASARISIZ | sifir | A en iyi D04-S02/tek: d +0.038, AUC 0.517, q 0.730; C lift en çok 1.14 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D04-S03 | D04-S03: Dip testleri sıklaşıyor mu? (son aralık / önceki aralıklar; < 1 sıklaşma) | VERI_YETERSIZ | sifir | A en iyi D04-S03/tek: d +0.042, AUC 0.476, q 0.078; C lift en çok 1.23 | VERİ YETERSİZ | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D04-S04 | D04-S04: Büyük hareketler arası boşluk (son büyük hareketten bu yana süre × sıklık) | TERS_YONLU | ters | A en iyi D04-S04/tek: d -0.105, AUC 0.462, q 0.004; C lift en çok 1.30; vekil kıyası: en yakın hacim_orani ρ -0.28, dd250 katmanlı d -0.108 | İLİŞKİ VAR, NEDEN BELİRSİZ | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D04-S05 | D04-S05: Önce hacim mi fiyat mı? (60 günde ilk hacim olayı − ilk fiyat olayı, gün) | BASARISIZ | sifir | A en iyi D04-S05/tek: d +0.095, AUC 0.522, q 0.017; C lift en çok nan | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D04-S06 | D04-S06: Kanalda bekleme süresi (son 20 gün kanal kırılımından bu yana gün) | TERS_YONLU | ters | A en iyi D04-S06/tek: d -0.196, AUC 0.443, q 0.004; C lift en çok 1.04; vekil kıyası: en yakın r20 ρ -0.12, dd250 katmanlı d -0.184 | YANLIŞ BULGU ADAYI (M01) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D04-S07 | D04-S07: Haftanın günü (bilgi; tek başına iz değil) | BASARISIZ | sifir | A en iyi nan: d +nan, AUC nan, q nan; C lift en çok nan | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D04-S08 | D04-S08: Uzun hareketsizlik süresi (/r20/ < %5 ve dar aralık ardışık gün) | BASARISIZ | sifir | A en iyi D04-S08/tek: d -0.049, AUC 0.534, q 0.015; C lift en çok 1.14 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D04-S09 | D04-S09: Değişimlerin sırası (hacim -> aralık -> fiyat CUSUM; tamamlanmadan bu yana gün, negatif) | BASARISIZ | sifir | A en iyi D04-S09/tek: d +0.117, AUC 0.524, q 0.266; C lift en çok nan | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D05-S01 | D05-S01: Kapanış gün içi nerede? ((C−L)/(H−L), p gün ortalama) | TERS_YONLU | ters | A en iyi D05-S01/5: d -0.324, AUC 0.406, q 0.011; C lift en çok 0.98; vekil kıyası: en yakın r20 ρ +0.32, dd250 katmanlı d -0.278 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M09; M10; M12; M14; M15; M16; M17 |
| K55-D05-S02 | D05-S02: Gövde yönü ve payı ((C−O)/(H−L), p gün) | TERS_YONLU | ters | A en iyi D05-S02/5: d -0.396, AUC 0.387, q 0.011; C lift en çok 1.00; vekil kıyası: en yakın r20 ρ +0.35, dd250 katmanlı d -0.345 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M09; M10; M12; M14; M15; M16; M17 |
| K55-D05-S03 | D05-S03: Gün içi aralık (p / 120 gün) | TERS_YONLU | ters | A en iyi D05-S03/5: d +0.177, AUC 0.548, q 0.011; C lift en çok 1.23; vekil kıyası: en yakın ar20 ρ +0.44, dd250 katmanlı d +0.170 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M09; M10; M12; M14; M15; M16; M17 |
| K55-D05-S04 | D05-S04: Kapanışa doğru davranış VEKİLİ (C > (H+L)/2 günlerin payı, p gün) | TERS_YONLU | ters | A en iyi D05-S04/5: d -0.268, AUC 0.420, q 0.011; C lift en çok 0.98; vekil kıyası: en yakın r20 ρ +0.28, dd250 katmanlı d -0.229 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M09; M10; M12; M14; M15; M16; M17 |
| K55-D05-S05 | D05-S05: Boşluklar (p günde yukarı − aşağı %2 açılış boşluğu sayısı) | BASARISIZ | sifir | A en iyi D05-S05/20: d -0.049, AUC 0.475, q 0.230; C lift en çok 1.34 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M09; M10; M12; M14; M15; M16; M17 |
| K55-D05-S06 | D05-S06: Fiyat etkisi VEKİLİ (60 gün /getiri/ ~ log işlem değeri eğimi; Kyle λ benzeri) | BASARISIZ | sifir | A en iyi D05-S06/tek: d -0.066, AUC 0.481, q 0.011; C lift en çok 1.17 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M09; M10; M11; M12; M14; M15; M16; M17 |
| K55-D05-S07 | D05-S07: Yüksek hacimli güne (> 1,5 × medyan) ertesi gün tepki (devam = +1; p gün ortalama, bir gün gecikmeli) | BASARISIZ | sifir | A en iyi D05-S07/40: d +0.037, AUC 0.510, q 0.042; C lift en çok 1.01 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M09; M10; M12; M14; M15; M16; M17 |
| K55-D05-S08 | D05-S08: Alış–satış dengesizliği VEKİLİ (işaretli hacim payı, p gün) | TERS_YONLU | ters | A en iyi D05-S08/5: d -0.336, AUC 0.402, q 0.011; C lift en çok 1.00; vekil kıyası: en yakın r20 ρ +0.30, dd250 katmanlı d -0.293 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M09; M10; M11; M12; M14; M15; M16; M17 |
| K55-D05-S10 | D05-S10: Gün içi tersine dönüş payı (açılış yönü ≠ kapanış yönü, p gün) | BASARISIZ | sifir | A en iyi D05-S10/5: d -0.049, AUC 0.484, q 0.177; C lift en çok 1.04 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M09; M10; M12; M14; M15; M16; M17 |
| K55-D06-S01 | D06-S01: Göreli güç ivmesi (p gün RS − 60 gün RS'nin p payı) | TERS_YONLU | ters | A en iyi D06-S01/5: d -0.433, AUC 0.374, q 0.015; C lift en çok 1.22; vekil kıyası: en yakın r20 ρ +0.26, dd250 katmanlı d -0.393 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17; M18 |
| K55-D06-S02 | D06-S02: Piyasa düşerken direnç (SPY < −%1 günlerinde hisse ortalama getirisi, p gün) | BASARISIZ | sifir | A en iyi D06-S02/120: d -0.081, AUC 0.470, q 0.457; C lift en çok 1.48 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17; M18 |
| K55-D06-S03 | D06-S03: Sektörden ayrışma (hisse − sektör sepeti, p gün) | TERS_YONLU | ters | A en iyi D06-S03/5: d -0.391, AUC 0.385, q 0.015; C lift en çok 1.17; vekil kıyası: en yakın r20 ρ +0.32, dd250 katmanlı d -0.346 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17; M18 |
| K55-D06-S04 | D06-S04: Sektör içi sıra değişimi (r60 sektör yüzdeliğinin p gün değişimi; kesitsel) | TERS_YONLU | ters | A en iyi D06-S04/20: d -0.159, AUC 0.454, q 0.015; C lift en çok nan; vekil kıyası: en yakın r20 ρ +0.46, dd250 katmanlı d -0.124 | İLİŞKİ VAR, NEDEN BELİRSİZ | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17; M18 |
| K55-D06-S05 | D06-S05: Endeksten önce dip (60 gün: SPY dip günü − hisse dip günü) | TERS_YONLU | ters | A en iyi D06-S05/tek: d -0.174, AUC 0.445, q 0.015; C lift en çok 1.03; vekil kıyası: en yakın r60 ρ +0.41, dd250 katmanlı d -0.038 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17; M18 |
| K55-D06-S06 | D06-S06: Göreli güç değişim noktası (CUSUM; son yukarı değişimden bu yana gün, negatif) | BASARISIZ | sifir | A en iyi D06-S06/tek: d -0.024, AUC 0.496, q 1.000; C lift en çok nan | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17; M18 |
| K55-D06-S07 | D06-S07: Düşüşte sınırlı kayıp (aşağı beta, 120 gün; düşük = dirençli) | BASARISIZ | sifir | A en iyi D06-S07/tek: d +0.085, AUC 0.527, q 0.233; C lift en çok 1.07 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17; M18 |
| K55-D06-S08 | D06-S08: Yükselişte güçlenen tepki (yukarı beta − aşağı beta, 120 gün) | BASARISIZ | sifir | A en iyi D06-S08/tek: d -0.060, AUC 0.483, q 0.407; C lift en çok 1.07 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17; M18 |
| K55-D06-S09 | D06-S09: Küçüklere göre konum (IWM'ye göre p gün) | TERS_YONLU | ters | A en iyi D06-S09/20: d -0.278, AUC 0.415, q 0.015; C lift en çok 1.11; vekil kıyası: en yakın r20 ρ +0.79, dd250 katmanlı d -0.208 | YANLIŞ BULGU ADAYI (M01) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17; M18 |
| K55-D06-S10 | D06-S10: Korelasyon kopuşu (hisse–SPY 60 gün − 250 gün korelasyon) | BASARISIZ | sifir | A en iyi D06-S10/tek: d +0.044, AUC 0.510, q 0.407; C lift en çok 1.06 | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17; M18 |
| K55-D10-S01 | D10-S01: Fiyat düşerken hacim farklı (r20 düşük VE aşağı gün hacim payı düşük) | BASARISIZ | sifir | A en iyi D10-S01/tek: d -0.054, AUC 0.478, q 0.182; C lift en çok nan | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M04; M07; M10; M14; M15; M17 |
| K55-D10-S02 | D10-S02: Vol düşerken göreli güç yükseliyor (D03-S01 düşük VE D06-S01 yüksek) | TERS_YONLU | ters | A en iyi D10-S02/tek: d -0.177, AUC 0.445, q 0.002; C lift en çok nan; vekil kıyası: en yakın r20 ρ +0.36, dd250 katmanlı d -0.166 | YANLIŞ BULGU ADAYI (M01) | M01; M04; M07; M10; M14; M15; M17 |
| K55-D10-S03 | D10-S03: Piyasa düşerken hisse yatay (D06-S02 yüksek VE dar alan süresi uzun) | BASARISIZ | sifir | A en iyi D10-S03/tek: d -0.210, AUC 0.429, q 0.200; C lift en çok nan | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M04; M07; M10; M14; M15; M17 |
| K55-D10-S04 | D10-S04: Uzun hareketsizlik + hacim yapısı değişimi (D04-S08 uzun VE Gini 20 gün düşüşü) | BASARISIZ | sifir | A en iyi D10-S04/tek: d -0.088, AUC 0.490, q 0.002; C lift en çok nan | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M01; M04; M07; M10; M14; M15; M17 |
| K55-D10-S09 | D10-S09: Lider–takipçi gecikmesi (sektör liderleri 20 gün getirisi − hisse 20 gün getirisi) | BASARILI | pozitif | A en iyi D10-S09/tek: d +0.252, AUC 0.578, q 0.002; C lift en çok 1.11; vekil kıyası: en yakın r20 ρ -0.79, dd250 katmanlı d +0.189 | YANLIŞ BULGU ADAYI (M01) | M01; M04; M07; M10; M14; M15; M17; M18 |
| K55-D10-S10 | D10-S10: Çok değişkenli sapma (8 temel ölçünün kendi 250 gün geçmişine köşegen Mahalanobis uzaklığı) | KUCUK_ETKI | pozitif | A en iyi D10-S10/tek: d +0.140, AUC 0.535, q 0.002; C lift en çok 1.14; vekil kıyası: en yakın hacim_orani ρ +0.24, dd250 katmanlı d +0.129 | YANLIŞ BULGU ADAYI (M01) | M01; M04; M07; M10; M14; M15; M17 |
| K55-F0-EVREN | Faz 0 evren kurulumu ve dışlamalar | VERI_YETERSIZ | sifir | 3260 sembol (V_ABD 1410, K34_yahoo 1428, K34_tiingo 422); dışlama: kisa_seri_yukleyici 60, fon_evren_disi 7, eslesme_yok_cik 1 (evrende kalır); sınıf {1: 2994, 2: 19, 3: 159, 4: 9, 5: 79}; 4b kesim 9 (ARIS, UNIT, AXP, BG | YÖNTEM DENETİMİ (bulgu değil) | M04; M07; M10; M13; M14; M15; M17 |
| K55-F0-KALITE | Faz 0 veri kalitesi (hatalı 9 / yetersiz 242 / şüpheli sıçrama 499) | VERI_YETERSIZ | sifir | Kullanılabilir 3012/3260; veri hatalı 9 (OHLC high_dusuk 2, low_yuksek 7; hepsi K34_yahoo sınıf 1: CDIX, CFOR, COSG, EMED, HCMC, MMEX, NGTF, OZSC, PGOL); veri yetersiz 242 (sıfır hacim payı > %20: 179, ciddi boşluk > 5 g | YÖNTEM DENETİMİ (bulgu değil) | M04; M07; M10; M13; M14; M15; M17 |
| K55-F0-SIZINTI | Faz 0 gelecek bilgisi sızıntısı testleri | BASARILI | sifir | Olumlu kontrol (t+60 getirisi) d 1.178, AUC 0.825; olumsuz kontrol (rastgele) d -0.0026 [-0.0265, +0.0203], AUC 0.499; kesme testi hata 0 (D01-S01); dedektör gelecek değişkende 6 hata; olay etiketi 3 olay; eşleşme hata 0 | YÖNTEM DENETİMİ (bulgu değil) | M04; M07; M10; M13; M14; M15; M17 |
| K55-SONUC | K55 Faz 1 genel karar (63 OHLCV hücresi, KEŞİF 2016-21) | BASARISIZ | sifir | KEŞİF 25, REDDEDİLDİ 36, VERİ YETERSİZ 2; B 0 / 164 TUTMAZ | ETKİ YOK (başarısız kalır; açıklanacak etki yok) | M04; M07; M10; M14; M15; M17 |

## 2. Açıklanmamış bulgular

Etkisi olan her bulgu; hiçbiri 'açıklandı' sayılmadı. ADAY AÇIKLAMA = Faz 1 doğrulaması bekleyen (M01 eseri / vekil).

| faz0_durum | kaynak_calisma | n |
|---|---|---|
| ADAY AÇIKLAMA (Faz 1 doğrulaması bekliyor) | K52 | 1 |
| ADAY AÇIKLAMA (Faz 1 doğrulaması bekliyor) | K53 | 1 |
| ADAY AÇIKLAMA (Faz 1 doğrulaması bekliyor) | K55 | 21 |
| AÇIKLANMADI | K55 | 4 |
| BETİMLEYİCİ (karar yok) | K51 | 12 |
| BETİMLEYİCİ (karar yok) | K52 | 5 |
| BETİMLEYİCİ (karar yok) | K53 | 1 |
| VERİ YETERSİZ (ölçülemedi) | K51 | 6 |
| VERİ YETERSİZ (ölçülemedi) | K52 | 8 |
| VERİ YETERSİZ (ölçülemedi) | K53 | 1 |
| VERİ YETERSİZ (ölçülemedi) | K54 | 12 |
| VERİ YETERSİZ (ölçülemedi) | K55 | 2 |

| kimlik | ad | sinif | buyukluk | faz0_gerekce | mekanizma_hipotezleri |
|---|---|---|---|---|---|
| K55-D01-S05 | D01-S05: Getiri asimetrisi (p gün çarpıklık) | TERS_YONLU | A en iyi D01-S05/20: d -0.121, AUC 0.464, q 0.015; C lift en çok 1.03; vekil kıyası: en yakın r20 ρ +0.34, dd250 katmanlı d -0.099 | M01 sentetik Y60 dört spek: MEKANIK_IZ_YOK;MEKANIK_IZ_YOK;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR (çoğunluk yok); KEŞİF ufkunda: BELIRSIZ 3/3; M03 / M01 Faz 1'de | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17 |
| K55-D02-S05 | D02-S05: Hacim zamana nasıl yayılmış? (p gün Gini; düşük = yayılmış) | TERS_YONLU | A en iyi D02-S05/20: d +0.110, AUC 0.528, q 0.011; C lift en çok 1.07; vekil kıyası: en yakın hacim_orani ρ +0.36, dd250 katmanlı d +0.105 | M01 sentetik Y60 dört spek: MEKANIK_IZ_YOK;MEKANIK_IZ_YOK;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR (çoğunluk yok); KEŞİF ufkunda: MEKANIK_IZ_YOK 2/3; M03 / M01 Faz 1'de | M01; M02; M03; M04; M06; M07; M08; M10; M11; M14; M15; M16; M17 |
| K55-D04-S04 | D04-S04: Büyük hareketler arası boşluk (son büyük hareketten bu yana süre × sıklık) | TERS_YONLU | A en iyi D04-S04/tek: d -0.105, AUC 0.462, q 0.004; C lift en çok 1.30; vekil kıyası: en yakın hacim_orani ρ -0.28, dd250 katmanlı d -0.108 | M01 sentetik Y60 dört spek: MEKANIK_IZ_YOK;MEKANIK_IZ_YOK;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR (çoğunluk yok); KEŞİF ufkunda: MEKANIK_IZ_YOK 1/1; M03 / M01 Faz 1'de | M01; M03; M04; M07; M10; M14; M15; M16; M17 |
| K55-D06-S04 | D06-S04: Sektör içi sıra değişimi (r60 sektör yüzdeliğinin p gün değişimi; kesitsel) | TERS_YONLU | A en iyi D06-S04/20: d -0.159, AUC 0.454, q 0.015; C lift en çok nan; vekil kıyası: en yakın r20 ρ +0.46, dd250 katmanlı d -0.124 | M01 sentetik Y60 dört spek: KISMEN_MEKANIK;MEKANIK_ACIKLAR;KISMEN_MEKANIK;MEKANIK_ACIKLAR (çoğunluk yok); KEŞİF ufkunda: MEKANIK_ACIKLAR 6/6; M03 / M01 Faz 1'de | M01; M02; M03; M04; M05; M07; M10; M14; M15; M16; M17; M18 |

## 3. Mekanizma hipotezleri

Önceden yazılı tahmin ve çürütme ölçütü; tam metin K56_HIPOTEZLER.csv. Her bulgu için en az üç yarışan açıklama envanterde (olasi_aciklamalar).

| kimlik | ad | tur | dogruysa | yanlissa | curutme | oncelik | faz0 |
|---|---|---|---|---|---|---|---|
| M01 | Olay başlangıcı seçim etkisi (mekanik eser) | yontem | bilgisiz yapay veride aynı tanım + aynı kod gerçek d'nin >= %50'sini aynı işaretle üretir; gerçek veride seçimsiz etiketle d küçülür (/d(seçimsiz)/ <= 0,2 × /d(ilk geçiş)/); seçimsiz ileri ölçüde (K55 B) etki yok | yapay veride /d/ < 0,05; gerçek veride seçimsiz etiketle (bütün nitelikli günler) etki >= ilk geçiş etkisinin yarısı ve aralık 0'ı dışlıyor | ONKAYIT_K56 v1.1-2: /d(seçimsiz)/ >= 0,5 × /d(ilk geçiş)/ ve aralık 0'ı dışlıyor -> GERÇEK ETKİ KALIYOR (M01 açıklamaz) | 1 | sentetik sınama yapıldı (Y60: 25 KEŞİF'in 21'i YANLIŞ BULGU ADAYI; KEŞİF ufkunda ayrıca raporlanır); Faz 1: v1.1-2 seçimsiz kontrol protokolü |
| M02 | Kısa dönem tersine dönüş / likidite sağlama (gerçek fiyat baskısı) | piyasa | M01 gecikme denetiminden sonra kalan ters etki yüksek spread / düşük derinlik (Corwin-Schultz, MIDAS gizli emir ve tek lot altı payı) grubunda büyük; 8-K haberi yok; seçimsiz ileri getiride (sinyal günü sabit) zayıf kapa | kalan etki likiditeyle değişmez ya da ileri getiri sıfır | yüksek spread üçlüsünde 20 gün eşli fark aralığı 0'ı kapsıyor | 2 | veri erişimi: spread vekili yerel; MIDAS 2012+ (REIT / yabancı / BDC yok); Reg SHO hacmi tesis dosyalarıyla 2009-08+ |
| M03 | Oynaklık / risk seçimi (oynaklık ondalığı denetimi yetersiz) | yontem | yalnız GARCH'lı yapay evrende mekanik iz (BELİRSİZ hücreler); ince oynaklık denetimi (yüzdelik, koşullu oynaklık, beta) gerçek d'yi >= %50 küçültür | ince denetim d'yi değiştirmez | küçülme < %25 | 1 | sentetik Y60: 4 KEŞİF hücresi BELİRSİZ (D01-S05, D02-S05, D04-S04 yalnız GARCH spekinde mekanik; D06-S04 her spekte kısmen / tam mekanik); oynaklık / hacim hücrelerinin sınıfı DGP'ye duyarlı |
| M04 | Haber / bilanço / kurumsal olay kaynaklı sıçrama | sirket | G1 olaylarının G2'den belirgin büyük payında [t0−5, t0+10] içinde 8-K var (madde koduyla); haber türüne koşullu iken olay öncesi fark küçülür | 8-K sıklığı G1 ve G2'de aynı | fark aralığı 0'ı kapsıyor | 1 | veri yerel (sec_ozet: 8-K madde kodu dolu pay 1,0); indirme yok |
| M05 | Açığa satış sıkışması | yatirimci | G1'de t0 öncesi açığa satış / dolaşım ve kapatma gün sayısı G2'den yüksek; t0 sonrası pozisyon düşer; FTD artar | açığa satış ölçüleri G1 ve G2'de aynı | fark aralığı 0'ı kapsıyor | 2 | KAPSAM: açığa satış POZİSYONU (FINRA SI API) 2017-12-29+ -> KEŞİF'in 2016-01..2017-11'i yok; açığa satış HACMİ (Reg SHO tesis dosyaları) 2009-08+ tam; FTD 2004+ |
| M06 | Sulandırma / finansman döngüsü (hisse ihracı) | sermaye | G5 (12 ayda > %20 hisse artışı) ve ihraç başvurusu G4 / G3'te ve G1'in olay SONRASI penceresinde sık; G1 olay öncesinde değil | ihraç sıklığı gruplar arasında aynı | fark aralığı 0'ı kapsıyor | 2 | XBRL hisse sayısı bölünmeye göre düzeltilmemiş ve birleşme artışını ayırmıyor (TRMB 2013 2:1 bölünme, EXR 2023 birleşme, IRM 2016 satın alma; TLGTQ 2020-21 artışı ters bölünme SONRASI gerçek sulandırma): pencere KEŞİF'le |
| M07 | Temel iyileşme / bozulma | sirket | G1'de t0 sonrası ilk bildirimde (filed) satış / FNA iyileşmesi G2'den büyük; t0 öncesi bildirimlerde fark yok | temel değişim farkı yok | aralık 0'ı kapsıyor | 2 | companyfacts 12/12 indi; yabancı ihraççı (IFRS) ve CIK değişimi boşluk bırakıyor |
| M08 | Kurumsal birikim (13F pozisyon artışı) | yatirimci | olay ya da P1 öncesi çeyrekte (bildirim tarihine göre) kurumsal sahiplik payı ve sahip sayısı artışı G1'de G2'den büyük | artış farkı yok ya da sonra geliyor | fark aralığı 0'ı kapsıyor | 2 | 13F 2013q2+, KEŞİF ~1,1 GB; CUSIP -> sembol OpenFIGI 9/10 (süzgeç gerekli); 45 gün gecikme |
| M09 | Kurumsal / içeriden dağıtım (pozisyon azaltma) | yatirimci | plansız (10b5-1 dışı) içeriden S ve 13F azaltımı G4'te ve G2'de G1'den sık | fark yok | aralık 0'ı kapsıyor | 2 | Form 4 2006q1+; KEŞİF ~248 MB (ham zipler bu oturumun karalama klasöründe); 10b5-1 işareti fiilen 2023q2+ ('1' ve 'true'); öncesi dipnot / açıklama metni vekili: S içeren Form 4'lerin %43,5'i (2016q1) |
| M10 | İçeriden bilgi (açık piyasa alımı) | yatirimci | t0 öncesi 90 günde P alımı G1'de G2'den sık | fark yok | aralık 0'ı kapsıyor | 3 | K30 özeti (k30_alim) yalnız 2022-01..2026-03: KEŞİF YOK; KEŞİF için Insider DS'teki P kodları kullanılır |
| M11 | Emilim (büyük satışın başka alıcılarca karşılanması) | yatirimci | satış baskılı günlerde işlem başına hacim (MIDAS TradeVol / Trades) ve gizli / ATS payı artar; aynı çeyrekte 13F sahip sayısı ya da 13D / 13G başvurusu artar; fiyat etkisi (Amihud) düşer | işlem büyüklüğü ve kurumsal sahiplik değişmez (o zaman dağıtım ya da likidite) | fark aralığı 0'ı kapsıyor | 2 | MIDAS günlük hisse × borsa 2012+ (çeyrek ~87 MB); FINRA ATS genel API yakın geçmiş (KEŞİF yok) |
| M12 | Likidite / piyasa derinliği değişimi | piyasa | olay öncesi spread / Amihud / iptal-işlem oranı G1'de G2'den farklı ve bu fark olay öncesi farkı açıklar | fark yok | aracılık < %25 ve fark aralığı 0'ı kapsıyor | 3 | spread vekili yerel (dolu pay 0,99); MIDAS erişilebilir |
| M13 | Veri / fiyat düzeltmesi / evren kaynaklı yanlış görüntü | veri | etki sağlayıcıya göre işaret değiştirir (K51 P1: V_ABD +, Tiingo −); olay günleri bölünme / sembol değişimi tarihlerine yığılır; ikinci sağlayıcı (Tiingo) sıçramayı doğrulamaz | etki sağlayıcıdan bağımsız; olaylar bölünme tarihlerinden bağımsız | etkileşim aralığı 0'ı kapsıyor ve çakışma payı taban kadar | 1 | V_ABD bölünme günlerinde düzeltilmiş (AAPL / TSLA / NVDA gece oranı ~1); XBRL hisse sayısı düzeltilmemiş |
| M14 | Kasıtlı yanıltma (manipülasyon / pompala-boşalt) | kasit | G1 olaylarının sembol + tarih eşleşmeli kesinleşmiş kararla çakışma payı G2'den büyük (resmî kuşku kaydı ayrı sütun) | çakışma payı aynı ya da sıfır (kasıt kanıtı yok) | kayıt yok -> KASIT KANITI YOK | 3 | SEC askıya alma 1995-2026 (resmî kuşku kaydı; sembol yok): tarih şartlı ad eşlemesi erişim testinde; tarih şartsız 10 eşleşmenin 1'i yanlış, hiçbiri K55 panel penceresinde değil |
| M15 | Birleşme / satın alma teklifi | sirket | G1'in [t0, t0+60] içinde SC TO-T / DEFM14A / 425 / 8-K 1.01-2.01 başvurusu payı G2'den büyük; birleşmeli olaylar çıkarılınca olay öncesi fark küçülür | pay farkı yok | aralık 0'ı kapsıyor | 2 | veri yerel (sec_ozet) |
| M16 | Toplu piyasa dibi / beta (2020 Mart gibi) | piyasa | olaylar ay bazında kümelenir; 2020-03..06 çıkarılınca ya da beta denetlenince d küçülür | değişmez | küçülme < %25 | 2 | veri yerel |
| M17 | Hayatta kalma yanlılığı (evren) | veri | batan şirketler eklendikçe ters etki ve P1 artısı küçülür / işaret değiştirir | değişmez | değişim < ölçüm aralığı | 2 | K54: 266 çıkış / 3.267; eksik batanlar Tiingo kotasıyla (ayda 500) eklenebilir (Cemal kararı) |
| M18 | Tema / sektör rüzgârı (tema rallisi) | piyasa | olaylar sektör × hafta kümelenir; sektör × gün sabit etkisiyle olay öncesi fark küçülür | değişmez | küçülme < %25 | 2 | K35-K37 rüzgâr çalışmaları var (Ç108-Ç111) |
| M19 | Bilgi gecikmesi: analist fiyatı izler | bilgi | revizyonların çoğu pencere dibinden >= %10 yükseliş SONRASI (K52 H4 zamanlama payı); revizyon sonrası eşli fark sıfır | revizyon yükselişten önce gelir ve sonrası pozitif | zamanlama payı < 0,3 | 3 | bilinen sonuç test sayılmaz; M19 yeni dönem verisiyle sınanır (Cemal kararı) |

## 4. Hipotez başına gerekli veri

| hipotez | kaynak | kesif_kapsam | kesif_not | maliyet | erisim_durumu |
|---|---|---|---|---|---|
| M01 | YEREL_K55_PANEL | kısmi | 2020-10 öncesi batanlar yok | - | YEREL |
| M01 | SENTETIK | tam | - | - | YEREL |
| M02 | OHLC_SPREAD_VEKIL | tam | fiyat kadar (vekil) | ücretsiz | GECTI |
| M02 | SEC_MIDAS | kısmi | 2016q1'de işlemdeki K55 hisselerinin ~%66'sı; REIT / yabancı / BDC yok | ücretsiz | KISMI |
| M02 | FINRA_REGSHO | tam | tesis dosyaları 2009-08+ (yalnız borsa dışı hacim) | ücretsiz | GECTI |
| M02 | SEC_SUBMISSIONS_OZET | tam | yerel | ücretsiz, indirme yok | GECTI |
| M03 | YEREL_K55_PANEL | kısmi | 2020-10 öncesi batanlar yok | - | YEREL |
| M04 | SEC_SUBMISSIONS_OZET | tam | yerel | ücretsiz, indirme yok | GECTI |
| M05 | FINRA_SI | kısmi | 2017-12-29+ | ücretsiz | KISMI |
| M05 | FINRA_REGSHO | tam | tesis dosyaları 2009-08+ (yalnız borsa dışı hacim) | ücretsiz | GECTI |
| M05 | SEC_FTD | tam | 2004+ | ücretsiz | GECTI |
| M06 | SEC_COMPANYFACTS | kısmi | XBRL var; CIK değişimi ve IFRS'li yabancılar boşluk | ücretsiz | KISMI |
| M06 | SEC_SUBMISSIONS_OZET | tam | yerel | ücretsiz, indirme yok | GECTI |
| M07 | SEC_COMPANYFACTS | kısmi | XBRL var; CIK değişimi ve IFRS'li yabancılar boşluk | ücretsiz | KISMI |
| M07 | SEC_FS_DS | tam | indirme gerekir (2016-20 ~1,6 GB) | ücretsiz | GECTI |
| M08 | SEC_13F_DS | tam | 2013q2+ | ücretsiz (kamu verisi) | GECTI |
| M08 | OPENFIGI | kısmi | güncel sembol | ücretsiz | GECTI |
| M09 | SEC_INSIDER_DS | tam | 2006q1+ | ücretsiz | KISMI |
| M09 | SEC_13F_DS | tam | 2013q2+ | ücretsiz (kamu verisi) | GECTI |
| M10 | SEC_INSIDER_DS | tam | 2006q1+ | ücretsiz | KISMI |
| M10 | K30_ALIM | yok | 2022-01+ | - | KISMI |
| M11 | SEC_MIDAS | kısmi | 2016q1'de işlemdeki K55 hisselerinin ~%66'sı; REIT / yabancı / BDC yok | ücretsiz | KISMI |
| M11 | SEC_13F_DS | tam | 2013q2+ | ücretsiz (kamu verisi) | GECTI |
| M11 | SEC_SUBMISSIONS_OZET | tam | yerel | ücretsiz, indirme yok | GECTI |
| M11 | FINRA_ATS | yok | genel API yakın geçmiş; tarihsel dosya elle | ücretsiz (kullanım koşulu) | KISMI |
| M12 | OHLC_SPREAD_VEKIL | tam | fiyat kadar (vekil) | ücretsiz | GECTI |
| M12 | SEC_MIDAS | kısmi | 2016q1'de işlemdeki K55 hisselerinin ~%66'sı; REIT / yabancı / BDC yok | ücretsiz | KISMI |
| M13 | YAHOO_SPLITS | kısmi | yalnız bugün yaşayan semboller | ücretsiz (resmî olmayan API; kullanım koşulu belirsiz) | KISMI |
| M13 | SEC_SUBMISSIONS_OZET | tam | yerel | ücretsiz, indirme yok | GECTI |
| M13 | TIINGO_BATAN | kısmi | kota: ayda 500 sembol | ücretsiz hesap kota; ücretli plan sınırsız | TEST EDİLMEDİ (belgeden) |
| M14 | SEC_ASKIYA_ALMA | tam | resmî kuşku kaydı | ücretsiz | GECTI |
| M14 | SEC_DAVA | tam | resmî kuşku kaydı | ücretsiz | GECTI |
| M15 | SEC_SUBMISSIONS_OZET | tam | yerel | ücretsiz, indirme yok | GECTI |
| M16 | YEREL_K55_PANEL | kısmi | 2020-10 öncesi batanlar yok | - | YEREL |
| M17 | TIINGO_BATAN | kısmi | kota: ayda 500 sembol | ücretsiz hesap kota; ücretli plan sınırsız | TEST EDİLMEDİ (belgeden) |
| M17 | SEC_SUBMISSIONS_OZET | tam | yerel | ücretsiz, indirme yok | GECTI |
| M18 | YEREL_K55_PANEL | kısmi | 2020-10 öncesi batanlar yok | - | YEREL |
| M18 | SEC_SUBMISSIONS_OZET | tam | yerel | ücretsiz, indirme yok | GECTI |
| M19 | YEREL_ANALIST | kısmi | Yahoo, yaşayanlar | - | YEREL |

## 5. Veri kaynakları: kapsam, gecikme, maliyet (erişim testiyle)

| kimlik | ad | kapsam | kesif_kapsam | gecikme | maliyet | boyut | eslesme | erisim_durumu | projede |
|---|---|---|---|---|---|---|---|---|---|
| SEC_13F_DS | SEC Form 13F veri setleri (INFOTABLE, SUBMISSION, COVERPAGE) | 2013q2 -> 2026; KEŞİF tam | tam | çeyrek sonundan 45 güne kadar; point-in-time için başvuru tarihi | ücretsiz (kamu verisi) | KEŞİF 24 çeyrek ~1,1 GB zip (INFOTABLE çeyrek başına ~160 MB açık) | CUSIP (9) -> sembol OpenFIGI; FIGI sütunu 2016'da çoğu boş | GECTI | yok (Ç103'te CUSIP eşlemesinde tıkandı) |
| OPENFIGI | OpenFIGI eşleme API'si | GÜNCEL referans: eski CUSIP için bugünkü sembolü döndürür (tarihli değil) | kısmi | - | ücretsiz | - | ID_CUSIP -> ticker, securityType, exchCode (CUSIP başına onlarca listeleme; Common Stock / REIT + US süzgeci şart); kapanmış eski CUSIP'ler (yeniden yapılanma, satın alma) bulunamıyor | GECTI | yok |
| SEC_NPORT_DS | SEC Form N-PORT veri setleri (fon portföyleri) | 2019q4 -> 2026; KEŞİF yalnız 2019q4-2021q4 | kısmi | çeyrek sonu + 60 gün (yayın) | ücretsiz | çeyrek ~440 MB zip | CUSIP / ISIN / sembol | GECTI | yok |
| SEC_INSIDER_DS | SEC Insider Transactions Data Sets (Form 3 / 4 / 5) | 2006q1 -> 2026q3; KEŞİF tam | tam | işlemden bildirime medyan 2 gün (2016q1), %90'ı <= 10 gün | ücretsiz | KEŞİF 24 çeyrek ~248 MB zip (2016q1 13 MB) | ISSUERCIK (+ sembol); yabancı özel ihraççı Form 4 vermez; ortak dosyalamada çift sayım riski | KISMI | K30 P özeti (k30_alim); K31 S satışları; ham zipler 2016q1-2026q1 bu oturumun karalama klasöründe (kalıcı değil) |
| SEC_COMPANYFACTS | SEC XBRL companyfacts API | XBRL 2009-11+; KEŞİF çoğu şirket tam | kısmi | her değer 'filed' (bildirim) tarihinden sonra; 10-Q ~40-45 gün | ücretsiz | 3.260 şirket ~5 GB JSON (indirme sırasında özetlenir) | CIK (yeniden yapılanmada CIK değişir: APO); IFRS'li yabancılar ayrı ad alanı | KISMI | secfs 2021q1+ özütü |
| SEC_FS_DS | SEC Financial Statement Data Sets | 2009q1 -> 2026; projede 2021q1+ | tam | başvuru tarihi | ücretsiz | eksik 2016-20: 20 çeyrek ~1,6 GB zip | CIK, adsh | GECTI | islenmis-veri secfs 2021q1-2026q3 |
| SEC_SUBMISSIONS_OZET | SEC başvuru geçmişi özeti (form, tarih, 8-K madde kodu) | 3.262 CIK, bütün başvurular 1990'lar -> 2026-10-30; KEŞİF tam | tam | başvuru tarihi (kabul günü) | ücretsiz, indirme yok | 105 MB (xz 6,6 MB) | CIK = K55 evreninin %100'ü | GECTI | VAR (K54) |
| YAHOO_SPLITS | Yahoo bölünme listesi (yfinance) | uzun geçmiş; batan sembollerde boş | kısmi | - | ücretsiz (resmî olmayan API; kullanım koşulu belirsiz) | küçük | sembol | KISMI | V_ABD (Yahoo, düzeltilmiş) |
| TIINGO_BATAN | Tiingo günlük fiyat (batanlar, splitFactor, divCash) | uzun geçmiş, batanlar dahil | kısmi | - | ücretsiz hesap kota; ücretli plan sınırsız | sembol başına küçük | sembol + Tiingo listesi (başlangıç / bitiş) | TEST EDİLMEDİ (belgeden) | 450 batan (repoya konmaz, lisans) |
| SEC_MIDAS | SEC MIDAS 'Metrics by Individual Security and Exchange' | 2012q1 -> 2026q2; KEŞİF tam; günlük × hisse (ayrıca hisse × borsa); evren CRSP SHRCD 10/11 + ETP: REIT ve yabancı hisse YOK (IRM, EXR, BNS örneklemde yok) | kısmi | çeyrek sonrası yayın | ücretsiz | hisse dosyası çeyrek ~15-22 MB -> KEŞİF ~0,4 GB (borsa kırılımlı ~2 GB) | Ticker + Date (CIK yok; batanlarda o günkü sembol gerekir: TLGT değil TLGTQ değil) | KISMI | yok |
| FINRA_REGSHO | FINRA Reg SHO günlük açığa satış hacmi (borsa dışı) | tesis dosyaları (FNYX, FNSQ) 2009-08 -> bugün: KEŞİF tam; konsolide CNMS 2018-08 -> | tam | ertesi gün | ücretsiz | gün ~0,3 MB | sembol | GECTI | yok (FINRA koşulu: ham veri dağıtılmaz) |
| FINRA_SI | FINRA konsolide açığa satış pozisyonu (API) | API'de ~2017-12 -> bugün (2017 boş): KEŞİF'in 2016-01..2017-11'i EKSİK | kısmi | ödeme gününden ~1 hafta sonra yayın (ayda iki kez) | ücretsiz | küçük | sembol | KISMI | K31: 2022-11 -> 2026-08 (Ç103) |
| FINRA_ATS | FINRA OTC Transparency ATS / OTC haftalık hacim | genel API'de KEŞİF boş; tarihsel dosyalar 2014 (ATS) / 2016 (OTC) sonrası, elle | yok | 2-4 hafta | ücretsiz (kullanım koşulu) | orta | sembol | KISMI | yok |
| SEC_FTD | SEC başarısız teslim (Fails-to-Deliver) | 2004 -> 2026; KEŞİF tam | tam | yayın ~1 ay | ücretsiz | yarım ay ~1 MB -> KEŞİF ~150 MB | sembol + CUSIP | GECTI | yok |
| OHLC_SPREAD_VEKIL | Günlük OHLC'den spread tahmini (Corwin-Schultz 2012, Abdi-Ranaldo 2017) | fiyat serisi kadar | tam | - | ücretsiz | - | sembol | GECTI | fiyat verisi var |
| TAQ_ITCH_UCRETLI | Gün içi işlem / kote / emir defteri (NYSE TAQ, Nasdaq ITCH, Polygon, Databento) | uzun geçmiş | tam | - | ücretli: Faz 0'da istek yok; fiyat kaynak araştırmasında | çok büyük (TB) | sembol | ATLANDI | yok |
| SEC_ASKIYA_ALMA | SEC işlem askıya alma bültenleri | 1995-10 -> 2026-10; 1.349 şirket satırı (bültenlerde birden çok şirket olabilir; 'et al.' emirlerinde ötekiler PDF'te) | tam | askıya alma günü | ücretsiz | ~3 MB HTML | SEMBOL YOK: tarih şartlı ad eşlemesi (CIK'in ilk başvurusu ve adın geçerlilik aralığı) -> K55 evreninde 9 şirket, hiçbiri panel penceresinde değil | GECTI | yok |
| SEC_DAVA | SEC dava bültenleri (litigation releases) ve idari kararlar | uzun geçmiş | tam | olaydan yıllar sonra | ücretsiz | küçük-orta (metin) | kişi / şirket adı; sembol metinde | GECTI | yok |
| SEC_13F_LISTE | SEC 'Official List of Section 13(f) Securities' (CUSIP + ihraççı adı) | 1996q1 -> 2026 | tam | çeyrek başı | ücretsiz (CUSIP lisans tartışması: repoya konmaz) | küçük | CUSIP -> ihraççı adı (tarihli) | TEST EDİLMEDİ (belgeden) | yok |
| SEC_FORM144 | Form 144 (satış niyeti bildirimi) | elektronik zorunluluk 2023-04-13; öncesi çoğu kâğıt (2021'de ~30.000'in ~234'ü elektronik) | yok | satışla aynı gün | ücretsiz | küçük | CIK | TEST EDİLMEDİ (belgeden) | yok |
| NASDAQ_HALT | Nasdaq işlem durdurma geçmişi | 2016 ve 2025 günleri denendi, veri var | tam | aynı gün | ücretsiz (yeniden dağıtım koşulu doğrulanmadı) | küçük | sembol | TEST EDİLMEDİ (belgeden) | yok (belgeden; bu koşuda istek yok) |
| DOJ_FINRA_AAER | DOJ basın bültenleri, FINRA disiplin kararları, SEC AAER | DOJ 2009+, FINRA 2005+, AAER 1982+ | tam | olaydan yıllar sonra | ücretsiz | metin | ad (sembol metinde) | TEST EDİLMEDİ (belgeden) | yok |
| NYSE_SI_UCRETLI | NYSE / Compustat tarihsel açığa satış pozisyonu | NYSE 1988+, Compustat yarım aylık 2007+ | tam | yarım ay | ücretli (kurumsal lisans; fiyat yayımlanmıyor) | orta | sembol / GVKEY | TEST EDİLMEDİ (belgeden) | yok |
| POLYGON_DATABENTO | Massive (Polygon) / Databento gün içi işlem verisi | Polygon Advanced 20+ yıl; Databento Nasdaq ITCH 2018-05+ | kısmi | - | Polygon Starter 29 $/ay (5 yıl), Advanced 199 $/ay (bireysel kullanım); Databento kullanım bazlı (yeni hesaba kredi) | çok büyük | sembol | TEST EDİLMEDİ (belgeden) | yok |
| YEREL_K55_PANEL | K55 ortak paneli + olay tablosu | 2016-2026; işlemdeki hisse 2016-06: 943, 2020-06: 1.131, 2021-06: 2.816 (K34 batanları 2020-10'dan); KEŞİF olaylarının tamamı V_ABD (bugün yaşayan) | kısmi | - | - | - | - | YEREL | VAR |
| YEREL_ANALIST | Yahoo analist not günlüğü (K52) | K52 veri kapsamı raporu | kısmi | - | - | - | sembol | YEREL | VAR |
| SENTETIK | Bilgisiz yapay evren (K56/mekanizma) | - | tam | - | - | - | - | YEREL | VAR |
| K30_ALIM | K30 açık piyasa alımları özeti | 2022-01 .. 2026-03 (7.821 satır): KEŞİF YOK | yok | - | - | - | sembol | KISMI | VAR |

Erişim testi ayrıntısı (K56_VERI_ERISIM_TESTI.csv; örneklem K56_ERISIM_ORNEKLEM.csv; istek günlüğü K56_ISTEK_GUNLUGU.csv):

| modul | kaynak | test | durum | olcu | deger | ayrinti |
|---|---|---|---|---|---|---|
| kurumsal_sahiplik | OPENFIGI | örneklem CUSIP'i (FTD 2016-01) -> sembol geri eşleme | GECTI | doğru / bulunan | 5/7 | AERI:00771V108->nan; APO:037612306->nan; BNS:064149107->BNS; EXR:30225T102->EXR; TRMB:896239100->TRMB; ABT:002824100->ABT; IRM:46284V101->IRM; bulunamayanlar: yeniden yapılanma / satın almayla kapanmış eski CUSIP (APO 20 |
| kurumsal_sahiplik | SEC_13F_DS | liste | GECTI | zip sayısı | 54 | en eski 2013q2; en yeni 01jun2026..31aug2026 |
| kurumsal_sahiplik | SEC_13F_DS | KEŞİF 2016-21 boy | GECTI | toplam MB | 1109.5 | 24 çeyrek, HEAD hatası 0; çeyrek ort. 46.2 MB |
| kurumsal_sahiplik | SEC_13F_DS | zip içeriği (Range) | GECTI | dosya | 9 | COVERPAGE.tsv 1.1 MB; INFOTABLE.tsv 161.2 MB; OTHERMANAGER.tsv 0.3 MB; OTHERMANAGER2.tsv 0.2 MB; SIGNATURE.tsv 0.7 MB; SUBMISSION.tsv 0.4 MB; SUMMARYPAGE.tsv 0.2 MB; FORM13F_metadata.json 0.0 MB; FORM13F_readme.htm 0.4 M |
| kurumsal_sahiplik | SEC_13F_DS | INFOTABLE kısmi okuma | GECTI | satır | 14347 | sütunlar: ACCESSION_NUMBER, INFOTABLE_SK, NAMEOFISSUER, TITLEOFCLASS, CUSIP, FIGI, VALUE, SSHPRNAMT, SSHPRNAMTTYPE, PUTCALL, INVESTMENTDISCRETION, OTHERMANAGER, VOTING_AUTH_SOLE, VOTING_AUTH_SHARED |
| kurumsal_sahiplik | OPENFIGI | 13F adi hisse CUSIP'i -> ABD sembolü (10 kimlik, anahtarsız) | GECTI | adi hisse / REIT + exchCode US eşleşen / 10 | 9 | 651229106->NWL; 65339F101->NEE; 655844108->NSC; 666807102->NOC; 67066G104->NVDA; 67103H107->ORLY; 674599105->OXY; 68389X105->ORCL; 693475105->PNC; NOT: OpenFIGI GÜNCEL sembolü döndürür (tarihli değil); tarihli ad için SE |
| kurumsal_sahiplik | SEC_NPORT_DS | liste + boy | GECTI | zip sayısı | 28 | en eski 2019q4; bir çeyrek 441 MB (KEŞİF'in yalnız 2019q4-2021q4'ünü kapsar) |
| iceriden_islemler | SEC_INSIDER_DS | liste | GECTI | zip sayısı | 83 | çeyrek 2006q1 .. 2026q3 |
| iceriden_islemler | SEC_INSIDER_DS | KEŞİF 2016-21 boy | GECTI | toplam MB | 247.5 | 24 çeyrek |
| iceriden_islemler | SEC_INSIDER_DS | 2016q1 indirme + ayrıştırma | GECTI | başvuru / işlem | 68776 / 98625 | 13.0 MB; tablolar ['DERIV_HOLDING.tsv', 'DERIV_TRANS.tsv', 'FOOTNOTES.tsv', 'NONDERIV_HOLDING.tsv', 'NONDERIV_TRANS.tsv', 'OWNER_SIGNATURE.tsv', 'REPORTINGOWNER.tsv', 'SUBMISSION.tsv', 'insider_transactions_metadata.json |
| iceriden_islemler | SEC_INSIDER_DS | evren eşleşmesi (CIK, 2016q1) | GECTI | K55 evreni CIK payı | 0.84 | 2016q1'de işlemde olan 931 CIK; eşleşmeyenler: o çeyrekte bildirim yok, yeni CIK (yeniden yapılanma sonrası güncel CIK), yabancı özel ihraççı (Form 4 yok) |
| iceriden_islemler | SEC_INSIDER_DS | işlem kodları + gecikme (2016q1, bütün) | GECTI | medyan bildirim gecikmesi (gün) | 2.0 | kod payları {'A': 0.242, 'F': 0.215, 'S': 0.164, 'M': 0.136, 'P': 0.121, 'G': 0.037, 'J': 0.037, 'D': 0.029}; gecikme %90 10.0 gün; P = açık piyasa alımı payı 0.121 |
| iceriden_islemler | SEC_INSIDER_DS | 10b5-1 dipnot vekili (2016q1, S içeren Form 4) | KISMI | plan geçen pay | 0.435 | 7867 satışlı bildirim; 2023 öncesi işaret sütunu yok, plan yalnız dipnot / açıklama metninden (olumsuz cümleleri de yakalar) |
| iceriden_islemler | SEC_INSIDER_DS | örneklem: olay çeyreğinde işlem | KISMI | işlemi olan sembol | 7/12 | APO(G1) 2017q1: 0 işlem {}; NTLA(G1) 2017q3: 7 işlem {'S': 7}; DOCU(G1) 2019q2: 30 işlem {'A': 13, 'S': 10, 'F': 5}; IRM(G1) 2020q2: 17 işlem {'A': 9, 'S': 4, 'M': 2}; BNS(G2) 2017q1: 0 işlem {}; ABT(G2) 2017q3: 51 işlem |
| iceriden_islemler | SEC_INSIDER_DS | 10b5-1 işareti (2026q1, S içeren Form 4) | GECTI | işaretli pay | 0.442 | 10015 satışlı Form 4; değerler {'0': 4323, '1': 3395, 'false': 1266, 'true': 1031}; işaret fiilen 2023q2+ (2023q1 çoğu boş) |
| iceriden_islemler | K30_ALIM | projede mevcut özet | KISMI | kapsam | 2022-01-03 .. 2026-03-31, 7821 satır; KEŞİF 2016-21: 0 satır | yalnız P (açık piyasa alımı) özeti; satış / M / F / 10b5-1 yok; KEŞİF için Insider DS P kodları |
| finansal_mekanizma | SEC_COMPANYFACTS | örneklem indirme | GECTI | başarılı | 12/12 | hepsi indi |
| finansal_mekanizma | SEC_COMPANYFACTS | kavram kapsamı KEŞİF 2016-21 (>= 8 dönem) | KISMI | kavram -> şirket sayısı | {"hisse_sayisi_kapak": 9, "hisse_agirlikli": 8, "satis": 8, "faaliyet_kari": 9, "net_kar": 8, "faaliyet_nakit": 9, "yatirim_harcamasi": 8, "hisse_ihraci": 5, "nakit": 9, "uzun_borc": 3} | APO(G1) ilk_filed 2022-05-10 ifrs False; NTLA(G1) ilk_filed 2016-06-03 ifrs False; DOCU(G1) ilk_filed 2018-06-08 ifrs False; IRM(G1) ilk_filed 2010-05-10 ifrs False; BNS(G2) ilk_filed 2018-11-27 ifrs True; ABT(G2) ilk_fi |
| finansal_mekanizma | SEC_COMPANYFACTS | point-in-time: filed − end (kapak hisse sayısı) | GECTI | medyan gün | 7.0 | her değer bildirim tarihinden sonra kullanılabilir (bilgi gecikmesi) |
| finansal_mekanizma | SEC_COMPANYFACTS | sulandırma ölçüsü HAM (KEŞİF bildirimleri; G5 adayı > %20) | KISMI | G5 adayı (ham) | 4 | NTLA(G1) +0.34; DOCU(G1) +0.12; IRM(G1) +0.25; BNS(G2) +0.00; ABT(G2) +0.18; TRMB(G2) +0.02; EXR(G2) +0.04; TLGTQ(G3) +16.21; AERI(G6) +0.30; CHRA(G6) +0.11; bölünme oranı kavramı olan şirket 4/10; HAM: bölünme / birleşm |
| finansal_mekanizma | SEC_FS_DS | projede 2021q1+; eksik 2016-20 boyu | GECTI | eksik 20 çeyrek MB | 1621.2 | yerel özüt fs_2021q1.csv.gz .. fs_2026q3.csv.gz (23 dosya); HEAD hatası 0 |
| kurumsal_olaylar | SEC_SUBMISSIONS_OZET | yerel kapsam (islenmis-veri k55) | GECTI | K55 evreni CIK eşleşmesi | 1.0 | 3262 CIK; ilk başvuru medyanı 2009-06-08; 8-K 554482, madde kodu dolu pay 1.0; yeniden indirme gerekmez |
| kurumsal_olaylar | SEC_SUBMISSIONS_OZET | örneklem olayları 2016-26 | GECTI | olaylı sembol | 12 | APO(G1) ihraç 18 13D 41 13G 6 3.02 1 1.03 0 2.01 0 25/15 2; NTLA(G1) ihraç 22 13D 10 13G 50 3.02 3 1.03 0 2.01 0 25/15 0; DOCU(G1) ihraç 5 13D 0 13G 19 3.02 1 1.03 0 2.01 2 25/15 0; IRM(G1) ihraç 6 13D 0 13G 44 3.02 1 1. |
| kurumsal_olaylar | SEC_SUBMISSIONS | canlı tazelik (APO) | GECTI | son başvuru canlı / yerel | 2026-10-30 / 2026-10-27 | recent 747 kayıt + eski dosya 0 |
| kurumsal_olaylar | SEC_SUBMISSIONS | canlı tazelik (NTLA) | GECTI | son başvuru canlı / yerel | 2026-10-28 / 2026-10-28 | recent 719 kayıt + eski dosya 0 |
| kurumsal_olaylar | YAHOO_SPLITS | bölünme listesi + V_ABD düzeltme denetimi (yalnız V_ABD sembolleri) | KISMI | düzeltilmemiş sıçrama | 0 | AAPL: 1.0 bölünme [4.0] V_ABD gece oranı [1.022]; TSLA: 2.0 bölünme [5.0, 3.0] V_ABD gece oranı [1.004, 1.018]; NVDA: 2.0 bölünme [4.0, 10.0] V_ABD gece oranı [0.997, 0.996]; V_ABD yüklü; batan / K34 sembolleri (TLGTQ, S |
| kurumsal_olaylar | SEC_ASKIYA_ALMA | liste + tarih şartlı ad eşlemesi (RESMÎ KUŞKU KAYDI, kasıt kanıtı değil) | GECTI | satır / bülten / eşleşen / belirsiz / panel penceresinde | 1349 / 1349 / 9 / 0 / 0 | tarih 1995-10-13 .. 2026-10-15; sembol YOK; şart: askıya alma günü CIK'in ilk başvurusundan sonra ve ad o tarihte geçerli; birden çok CIK'e düşen ad belirsiz; 'et al.' emirlerinde ilk şirketten sonrakiler PDF'te; eşleşen |
| kurumsal_olaylar | SEC_DAVA | ilk sayfa | GECTI | bülten no (ilk sayfa) | 100 | başlıklarda kişi / şirket adı; sembol yok; ayrıntı metinde |
| islem_davranisi | SEC_MIDAS | liste | GECTI | zip sayısı | 58 | çeyrek 2012q1 .. 2026q2 |
| islem_davranisi | SEC_MIDAS | hisse dosyası 2016q1: K55 evreni kapsamı | KISMI | 2016q1'de işlemde olan K55 hissesi payı | 0.663 | 934 hisse; en düşük sektör kapsamı {'Real Estate': 0.04, 'Basic Materials': 0.48, 'Energy': 0.57, 'BILINMIYOR': 0.66}; MIDAS evreni CRSP adi hisse (SHRCD 10/11) + ETP: REIT, yabancı, BDC / MLP yok |
| islem_davranisi | SEC_MIDAS | örneklem G1 / G2: olay çeyreğinde | GECTI | bulunan / uygun | 5/8 | APO(G1) 2017q1: var; NTLA(G1) 2017q3: var; DOCU(G1) 2019q2: var; IRM(G1) 2020q2: yok; BNS(G2) 2017q1: yok; ABT(G2) 2017q3: var; TRMB(G2) 2019q2: var; EXR(G2) 2020q2: yok; G3 / G6 (batan, birleşen) olay çeyrekleri 2022-23 |
| islem_davranisi | FINRA_REGSHO | günlük açığa satış hacmi (konsolide + tesis) | GECTI | HTTP | {"CNMS 20160104": 403, "CNMS 20180801": 200, "FNYX 20160104": 200, "FNSQ 20160104": 200} | KEŞİF tesis dosyalarıyla (FNYX + FNSQ [+ FORF], 2009-08+) kapsanır, konsolide CNMS 2018-08'den; 2016-01-04 tesis dosyalarında örneklemden 7 sembol; yalnız borsa dışı (TRF / ADF / ORF) hacim, pozisyon değil; FINRA koşulu: |
| islem_davranisi | FINRA_SI | API geçmiş derinliği (örneklem sembolleri) | KISMI | dönem -> sembol | {"2017-06": 0, "2018-01": 8, "2019-06": 10, "2021-06": 10} | 2017 boş: API ~2017-12'den başlıyor -> KEŞİF'in 2016-01..2017-11'i eksik; öncesi için borsa (NYSE / Nasdaq) ücretli dosyaları |
| islem_davranisi | FINRA_ATS | haftalık ATS / OTC hacmi (genel API, 4 sembol) | KISMI | dönem -> kayıt | {"2016-06": 0, "2019-06": 0, "2021-06": 0, "2023-06": 50} | genel API yalnız yakın geçmişi veriyor (KEŞİF boş); 2014 / 2016 sonrası tarihsel dosyalar otctransparency.finra.org'dan elle / kullanım koşuluyla |
| islem_davranisi | SEC_FTD | örneklem: olay yarım ayında başarısız teslim kaydı | GECTI | kaydı olan / örneklem | 8/12 | 437 dosya listede; APO(G1) cnsfails201701b: var; NTLA(G1) cnsfails201707a: var; DOCU(G1) cnsfails201906b: var; IRM(G1) cnsfails202005a: var; BNS(G2) cnsfails201701b: var; ABT(G2) cnsfails201707a: var; TRMB(G2) cnsfails20 |
| islem_davranisi | OHLC_SPREAD_VEKIL | Corwin-Schultz / Abdi-Ranaldo (yerel) | GECTI | sembol | 8 | APO: CS medyan 55 bp, AR medyan 64 bp, dolu 0.99; NTLA: CS medyan 145 bp, AR medyan 156 bp, dolu 0.99; DOCU: CS medyan 83 bp, AR medyan 104 bp, dolu 0.99; IRM: CS medyan 41 bp, AR medyan 48 bp, dolu 0.99; BNS: CS medyan  |
| islem_davranisi | TAQ_ITCH_UCRETLI | gün içi işlem / emir defteri | ATLANDI | istek | 0 | ücretli (NYSE TAQ / WRDS, Nasdaq ITCH, Polygon, Databento); Faz 0'da istek yok, fiyatı rapor |

## 6. Doğrulama ve çürütme yöntemleri

- Karşıt örnekler (her mekanizma): G1 olay, G2 aynı belirti yükseliş yok, G3 iflas, G4 büyük düşüş, G5 hisse sayısı > %20 artan, G6 birleşme, G7 sektör × likidite eşli rastgele; yanlış pozitif oranı = P(yükseliş yok | mekanizma var), kesinlik, etki ve ay kümeli %95 aralık.
- Aracılık (mediation): mekanizma değişkeni denetlenince asıl etkinin küçülme payı (bootstrap aralığı); >= %50 DOĞRULANMIŞ / GÜÇLÜ için şart.
- Sentetik sıfır sınaması: bilgisiz yapay evrende aynı tanım ve aynı kod (M01, M03); gerçek etkinin >= %50'sini üreten bulgu YANLIŞ BULGU adayı.
- Seçimsiz kontrol (v1.1-2): aynı ölçü, eşiği aşan BÜTÜN günlerle / epizotta rastgele günle; ilk geçiş farkının ne kadarının kaldığı karar ölçütüdür. Gecikme (t0−k) yalnız bilgi (Y250'de mekanik eser k ile sönmez).
- Sağlayıcı / evren duyarlılığı: V_ABD / K34 Yahoo / Tiingo ayrı; batan evren genişletme (M13, M17).
- Point-in-time: bütün SEC / FINRA verisi bildirim / yayın tarihinden sonra kullanılır (13F 45 gün, Form 4 ~2 gün, 10-Q ~40 gün).
- Kasıt: üç sütun (gözlenen davranış / olası mekanizma / kasıt kanıtı); kanıt yalnız sembol + tarih doğrulanmış resmî kayıt.

M01 sentetik sınama (K56_SECIM_SENTETIK_OZET.csv; satırlar K56_SECIM_SENTETIK.csv):

| hucre | durum_k55 | varyant | d_gercek_Y60 | d_sent_Y60 | oran_Y60 | karar | d_sent_gecikme1 | d_sent_gecikme5 | d_sent_gecikme20 |
|---|---|---|---|---|---|---|---|---|---|
| D01-S02 | KEŞİF | D01-S02/5 | -0.251 | -0.273 | 1.088 | MEKANIK_ACIKLAR | -0.133 | -0.046 | -0.015 |
| D01-S05 | KEŞİF | D01-S05/20 | -0.121 | -0.047 | 0.388 | BELIRSIZ | -0.021 | -0.010 | 0.013 |
| D01-S07 | KEŞİF | D01-S07/5 | -0.126 | -0.202 | 1.610 | MEKANIK_ACIKLAR | -0.078 | -0.016 | 0.000 |
| D01-S08 | KEŞİF | D01-S08/20 | -0.215 | -0.236 | 1.096 | MEKANIK_ACIKLAR | -0.171 | -0.078 | 0.004 |
| D01-S10 | KEŞİF | D01-S10/20 | 0.123 | 0.164 | 1.333 | MEKANIK_ACIKLAR | 0.086 | 0.009 | -0.005 |
| D02-S02 | KEŞİF | D02-S02/5 | 0.319 | 0.433 | 1.356 | MEKANIK_ACIKLAR | 0.263 | 0.102 | 0.003 |
| D02-S05 | KEŞİF | D02-S05/20 | 0.110 | 0.062 | 0.565 | BELIRSIZ | 0.010 | -0.015 | -0.047 |
| D02-S06 | KEŞİF | D02-S06/5 | 0.144 | 0.138 | 0.955 | MEKANIK_ACIKLAR | 0.036 | -0.000 | -0.010 |
| D02-S08 | KEŞİF | D02-S08/5 | -0.386 | -0.530 | 1.373 | MEKANIK_ACIKLAR | -0.242 | -0.073 | 0.003 |
| D03-S02 | KEŞİF | D03-S02/20 | 0.220 | 0.367 | 1.670 | MEKANIK_ACIKLAR | 0.220 | 0.070 | -0.037 |
| D04-S04 | KEŞİF | D04-S04/tek | -0.105 | -0.063 | 0.602 | BELIRSIZ | -0.002 | 0.011 | 0.021 |
| D04-S06 | KEŞİF | D04-S06/tek | -0.196 | -0.248 | 1.265 | MEKANIK_ACIKLAR | -0.105 | -0.013 | -0.009 |
| D05-S01 | KEŞİF | D05-S01/5 | -0.324 | -0.383 | 1.182 | MEKANIK_ACIKLAR | -0.229 | -0.079 | 0.000 |
| D05-S02 | KEŞİF | D05-S02/5 | -0.396 | -0.447 | 1.128 | MEKANIK_ACIKLAR | -0.266 | -0.089 | -0.001 |
| D05-S03 | KEŞİF | D05-S03/5 | 0.177 | 0.141 | 0.798 | MEKANIK_ACIKLAR | 0.016 | -0.028 | -0.048 |
| D05-S04 | KEŞİF | D05-S04/5 | -0.268 | -0.349 | 1.301 | MEKANIK_ACIKLAR | -0.214 | -0.072 | 0.001 |
| D05-S08 | KEŞİF | D05-S08/5 | -0.336 | -0.431 | 1.284 | MEKANIK_ACIKLAR | -0.258 | -0.096 | 0.002 |
| D06-S01 | KEŞİF | D06-S01/5 | -0.433 | -0.480 | 1.110 | MEKANIK_ACIKLAR | -0.285 | -0.119 | -0.019 |
| D06-S03 | KEŞİF | D06-S03/5 | -0.391 | -0.468 | 1.196 | MEKANIK_ACIKLAR | -0.273 | -0.114 | -0.011 |
| D06-S04 | KEŞİF | D06-S04/20 | -0.159 | -0.091 | 0.570 | BELIRSIZ | -0.032 | 0.011 | 0.025 |
| D06-S05 | KEŞİF | D06-S05/tek | -0.095 | -0.066 | 0.698 | MEKANIK_ACIKLAR | -0.001 | 0.056 | 0.043 |
| D06-S09 | KEŞİF | D06-S09/20 | -0.278 | -0.328 | 1.182 | MEKANIK_ACIKLAR | -0.211 | -0.088 | 0.029 |
| D10-S02 | KEŞİF | D10-S02/tek | -0.177 | -0.202 | 1.141 | MEKANIK_ACIKLAR | -0.105 | -0.030 | 0.063 |
| D10-S09 | KEŞİF | D10-S09/tek | 0.252 | 0.308 | 1.226 | MEKANIK_ACIKLAR | 0.200 | 0.089 | -0.029 |
| D10-S10 | KEŞİF | D10-S10/tek | 0.140 | 0.170 | 1.213 | MEKANIK_ACIKLAR | 0.071 | -0.002 | -0.040 |
| D01-S01 | REDDEDİLDİ | D01-S01/tek | 0.020 | -0.016 | -0.792 | MEKANIK_IZ_YOK | -0.022 | -0.029 | -0.032 |
| D01-S03 | REDDEDİLDİ | D01-S03/tek | -0.008 | -0.002 | 0.248 | MEKANIK_IZ_YOK | -0.010 | -0.021 | -0.017 |
| D01-S04 | REDDEDİLDİ | D01-S04/5 | 0.044 | -0.015 | -0.346 | MEKANIK_IZ_YOK | -0.008 | -0.003 | 0.013 |
| D01-S06 | REDDEDİLDİ | D01-S06/tek | -0.007 | 0.015 | -2.111 | MEKANIK_IZ_YOK | 0.026 | 0.029 | 0.036 |
| D01-S09 | REDDEDİLDİ | D01-S09/20 | -0.051 | -0.060 | 1.184 | MEKANIK_ACIKLAR | -0.048 | -0.011 | 0.057 |
| D02-S01 | REDDEDİLDİ | D02-S01/60 | -0.056 | 0.001 | -0.013 | MEKANIK_IZ_YOK | -0.025 | -0.033 | -0.014 |
| D02-S03 | REDDEDİLDİ | D02-S03/60 | -0.026 | -0.050 | 1.942 | MEKANIK_IZ_YOK | -0.060 | -0.061 | -0.045 |
| D02-S04 | REDDEDİLDİ | D02-S04/20 | -0.057 | -0.087 | 1.544 | MEKANIK_ACIKLAR | -0.053 | -0.023 | 0.006 |
| D02-S07 | REDDEDİLDİ | D02-S07/60 | -0.057 | 0.023 | -0.407 | MEKANIK_IZ_YOK | -0.024 | -0.029 | -0.010 |
| D02-S09 | REDDEDİLDİ | D02-S09/20 | 0.067 | 0.042 | 0.617 | BELIRSIZ | 0.005 | -0.008 | -0.008 |
| D02-S10 | REDDEDİLDİ | D02-S10/20 | 0.044 | 0.009 | 0.195 | MEKANIK_IZ_YOK | -0.003 | 0.021 | 0.057 |
| D03-S01 | REDDEDİLDİ | D03-S01/5 | 0.089 | 0.027 | 0.304 | BELIRSIZ | -0.042 | -0.039 | -0.049 |
| D03-S03 | REDDEDİLDİ | D03-S03/60 | -0.004 | -0.005 | 1.294 | MEKANIK_IZ_YOK | -0.008 | -0.008 | -0.010 |
| D03-S04 | REDDEDİLDİ | D03-S04/tek | -0.118 | -0.091 | 0.778 | MEKANIK_ACIKLAR | 0.004 | -0.003 | -0.006 |
| D03-S05 | REDDEDİLDİ | D03-S05/tek | 0.036 | 0.008 | 0.226 | MEKANIK_IZ_YOK | 0.010 | 0.013 | 0.015 |
| D03-S06 | REDDEDİLDİ | D03-S06/5 | -0.090 | -0.142 | 1.579 | MEKANIK_ACIKLAR | -0.041 | -0.005 | -0.016 |
| D03-S08 | REDDEDİLDİ | D03-S08/40 | -0.030 | -0.010 | 0.321 | MEKANIK_IZ_YOK | 0.028 | 0.043 | 0.081 |
| D03-S09 | REDDEDİLDİ | D03-S09/tek | 0.006 | 0.034 | 5.331 | MEKANIK_IZ_YOK | 0.049 | 0.044 | 0.045 |
| D03-S10 | REDDEDİLDİ | D03-S10/tek | -0.018 | -0.019 | 1.030 | MEKANIK_IZ_YOK | -0.055 | -0.071 | -0.066 |
| D04-S02 | REDDEDİLDİ | D04-S02/tek | 0.038 | 0.024 | 0.640 | MEKANIK_IZ_YOK | 0.024 | 0.023 | 0.026 |
| D04-S05 | REDDEDİLDİ | D04-S05/tek | 0.055 | 0.033 | 0.610 | BELIRSIZ | 0.028 | 0.027 | 0.005 |
| D04-S07 | REDDEDİLDİ | D04-S07/tek |  |  |  | TANIMSIZ |  |  |  |
| D04-S08 | REDDEDİLDİ | D04-S08/tek | -0.049 | -0.072 | 1.464 | MEKANIK_ACIKLAR | -0.025 | 0.017 | 0.016 |
| D04-S09 | REDDEDİLDİ | D04-S09/tek | -0.018 | -0.026 | 1.490 | MEKANIK_IZ_YOK | -0.029 | -0.028 | -0.025 |
| D05-S05 | REDDEDİLDİ | D05-S05/20 | -0.049 | 0.055 | -1.125 | BELIRSIZ | 0.029 | 0.006 | 0.010 |
| D05-S06 | REDDEDİLDİ | D05-S06/tek | -0.066 | 0.041 | -0.615 | MEKANIK_IZ_YOK | 0.004 | 0.012 | 0.027 |
| D05-S07 | REDDEDİLDİ | D05-S07/40 | 0.037 | 0.027 | 0.729 | MEKANIK_IZ_YOK | 0.003 | -0.011 | -0.001 |
| D05-S10 | REDDEDİLDİ | D05-S10/5 | -0.049 | -0.016 | 0.326 | MEKANIK_IZ_YOK | -0.002 | 0.010 | -0.003 |
| D06-S02 | REDDEDİLDİ | D06-S02/120 | -0.081 | -0.019 | 0.230 | MEKANIK_IZ_YOK | -0.008 | 0.004 | 0.008 |
| D06-S06 | REDDEDİLDİ | D06-S06/tek | 0.004 | 0.004 | 0.953 | MEKANIK_IZ_YOK | 0.004 | 0.006 | 0.003 |
| D06-S07 | REDDEDİLDİ | D06-S07/tek | 0.085 | -0.008 | -0.099 | MEKANIK_IZ_YOK | -0.010 | -0.009 | -0.005 |
| D06-S08 | REDDEDİLDİ | D06-S08/tek | -0.060 | -0.007 | 0.124 | MEKANIK_IZ_YOK | -0.006 | -0.004 | -0.009 |
| D06-S10 | REDDEDİLDİ | D06-S10/tek | 0.044 | 0.007 | 0.157 | MEKANIK_IZ_YOK | 0.013 | 0.018 | 0.017 |
| D10-S01 | REDDEDİLDİ | D10-S01/tek | -0.054 | -0.146 | 2.692 | MEKANIK_ACIKLAR | -0.081 | -0.003 | -0.003 |
| D10-S03 | REDDEDİLDİ | D10-S03/tek | -0.046 | 0.009 | -0.192 | MEKANIK_IZ_YOK | 0.030 | 0.035 | 0.033 |
| D10-S04 | REDDEDİLDİ | D10-S04/tek | -0.088 | -0.080 | 0.917 | MEKANIK_ACIKLAR | -0.035 | 0.006 | 0.014 |
| D04-S01 | VERİ YETERSİZ | D04-S01/tek | 0.129 | 0.329 | 2.544 | MEKANIK_ACIKLAR | 0.166 | 0.057 | -0.011 |
| D04-S03 | VERİ YETERSİZ | D04-S03/tek | 0.042 | 0.017 | 0.418 | MEKANIK_IZ_YOK | 0.017 | 0.025 | 0.017 |

Karar × K55 durumu:

| durum_k55 | BELIRSIZ | MEKANIK_ACIKLAR | MEKANIK_IZ_YOK | TANIMSIZ |
|---|---|---|---|---|
| KEŞİF | 4 | 21 | 0 | 0 |
| REDDEDİLDİ | 4 | 7 | 24 | 1 |
| VERİ YETERSİZ | 0 | 1 | 1 | 0 |

KEŞİF'i sağlayan (varyant, ufuk) satırlarında sentetik sınama (v1.1-3; K56_SECIM_SENTETIK_KESIF.csv):

| hucre | varyant | ufuk | d_gercek | d_sent | oran | spek_siniflari | karar |
|---|---|---|---|---|---|---|---|
| D01-S02 | D01-S02/10 | Y120 | -0.281 | -0.279 | 0.994 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S02 | D01-S02/10 | Y250 | -0.378 | -0.291 | 0.770 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S02 | D01-S02/10 | Y60 | -0.289 | -0.273 | 0.943 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S02 | D01-S02/20 | Y120 | -0.211 | -0.285 | 1.352 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S02 | D01-S02/20 | Y250 | -0.306 | -0.277 | 0.905 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S02 | D01-S02/20 | Y60 | -0.235 | -0.254 | 1.079 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S02 | D01-S02/40 | Y120 | -0.221 | -0.279 | 1.263 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S02 | D01-S02/5 | Y120 | -0.255 | -0.281 | 1.100 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S02 | D01-S02/5 | Y250 | -0.360 | -0.321 | 0.891 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S02 | D01-S02/5 | Y60 | -0.251 | -0.273 | 1.088 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S02 | D01-S02/60 | Y120 | -0.235 | -0.253 | 1.076 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S05 | D01-S05/20 | Y250 | -0.218 | -0.099 | 0.453 | MEKANIK_IZ_YOK;MEKANIK_IZ_YOK;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | BELIRSIZ |
| D01-S05 | D01-S05/40 | Y250 | -0.246 | -0.087 | 0.352 | MEKANIK_IZ_YOK;MEKANIK_IZ_YOK;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | BELIRSIZ |
| D01-S05 | D01-S05/60 | Y250 | -0.236 | -0.102 | 0.430 | MEKANIK_IZ_YOK;MEKANIK_IZ_YOK;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | BELIRSIZ |
| D01-S07 | D01-S07/10 | Y250 | -0.224 | -0.216 | 0.963 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S07 | D01-S07/5 | Y250 | -0.218 | -0.208 | 0.956 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S08 | D01-S08/20 | Y250 | -0.230 | -0.368 | 1.601 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S08 | D01-S08/20 | Y60 | -0.215 | -0.236 | 1.096 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D01-S10 | D01-S10/20 | Y250 | 0.303 | 0.157 | 0.516 | KISMEN_MEKANIK;MEKANIK_ACIKLAR;MEKANIK_IZ_YOK;MEKANIK_ACIKLAR | BELIRSIZ |
| D02-S02 | D02-S02/10 | Y120 | 0.282 | 0.454 | 1.614 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S02 | D02-S02/10 | Y250 | 0.375 | 0.512 | 1.366 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S02 | D02-S02/10 | Y60 | 0.292 | 0.378 | 1.294 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S02 | D02-S02/20 | Y120 | 0.212 | 0.402 | 1.895 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S02 | D02-S02/20 | Y250 | 0.312 | 0.491 | 1.572 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S02 | D02-S02/20 | Y60 | 0.213 | 0.299 | 1.405 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S02 | D02-S02/40 | Y250 | 0.256 | 0.455 | 1.778 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S02 | D02-S02/5 | Y120 | 0.285 | 0.492 | 1.729 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S02 | D02-S02/5 | Y250 | 0.363 | 0.538 | 1.483 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S02 | D02-S02/5 | Y60 | 0.319 | 0.433 | 1.356 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S05 | D02-S05/20 | Y250 | 0.263 | 0.060 | 0.229 | KISMEN_MEKANIK;MEKANIK_IZ_YOK;KISMEN_MEKANIK;MEKANIK_IZ_YOK | BELIRSIZ |
| D02-S05 | D02-S05/40 | Y250 | 0.226 | 0.002 | 0.007 | MEKANIK_IZ_YOK;MEKANIK_IZ_YOK;MEKANIK_IZ_YOK;MEKANIK_IZ_YOK | MEKANIK_IZ_YOK |
| D02-S05 | D02-S05/60 | Y250 | 0.209 | -0.030 | -0.144 | MEKANIK_IZ_YOK;TERS_ISARET;MEKANIK_IZ_YOK;MEKANIK_IZ_YOK | MEKANIK_IZ_YOK |
| D02-S06 | D02-S06/10 | Y250 | 0.317 | 0.102 | 0.323 | KISMEN_MEKANIK;MEKANIK_IZ_YOK;MEKANIK_ACIKLAR;KISMEN_MEKANIK | BELIRSIZ |
| D02-S06 | D02-S06/20 | Y250 | 0.335 | 0.066 | 0.197 | KISMEN_MEKANIK;MEKANIK_IZ_YOK;KISMEN_MEKANIK;MEKANIK_IZ_YOK | BELIRSIZ |
| D02-S06 | D02-S06/40 | Y250 | 0.307 | 0.036 | 0.117 | MEKANIK_IZ_YOK;MEKANIK_IZ_YOK;KISMEN_MEKANIK;MEKANIK_IZ_YOK | MEKANIK_IZ_YOK |
| D02-S06 | D02-S06/60 | Y250 | 0.283 | 0.016 | 0.057 | MEKANIK_IZ_YOK;TERS_ISARET;KISMEN_MEKANIK;MEKANIK_IZ_YOK | BELIRSIZ |
| D02-S08 | D02-S08/10 | Y120 | -0.401 | -0.589 | 1.468 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S08 | D02-S08/10 | Y250 | -0.631 | -0.640 | 1.015 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S08 | D02-S08/10 | Y60 | -0.364 | -0.485 | 1.333 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S08 | D02-S08/20 | Y120 | -0.316 | -0.535 | 1.691 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S08 | D02-S08/20 | Y250 | -0.583 | -0.608 | 1.042 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S08 | D02-S08/20 | Y60 | -0.280 | -0.407 | 1.453 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S08 | D02-S08/40 | Y120 | -0.220 | -0.426 | 1.933 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S08 | D02-S08/40 | Y250 | -0.502 | -0.576 | 1.147 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S08 | D02-S08/5 | Y120 | -0.411 | -0.606 | 1.473 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S08 | D02-S08/5 | Y250 | -0.650 | -0.631 | 0.971 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S08 | D02-S08/5 | Y60 | -0.386 | -0.530 | 1.373 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D02-S08 | D02-S08/60 | Y250 | -0.456 | -0.506 | 1.109 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D03-S02 | D03-S02/20 | Y120 | 0.252 | 0.493 | 1.958 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D03-S02 | D03-S02/20 | Y250 | 0.375 | 0.609 | 1.621 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D03-S02 | D03-S02/20 | Y60 | 0.220 | 0.367 | 1.670 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D03-S02 | D03-S02/40 | Y250 | 0.370 | 0.536 | 1.451 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D03-S02 | D03-S02/60 | Y250 | 0.328 | 0.489 | 1.490 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D04-S04 | D04-S04/tek | Y250 | -0.264 | -0.063 | 0.239 | MEKANIK_IZ_YOK;MEKANIK_IZ_YOK;MEKANIK_ACIKLAR;MEKANIK_IZ_YOK | MEKANIK_IZ_YOK |
| D04-S06 | D04-S06/tek | Y120 | -0.211 | -0.295 | 1.397 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D04-S06 | D04-S06/tek | Y250 | -0.315 | -0.237 | 0.751 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S01 | D05-S01/10 | Y120 | -0.277 | -0.373 | 1.347 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S01 | D05-S01/10 | Y250 | -0.371 | -0.438 | 1.182 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S01 | D05-S01/10 | Y60 | -0.274 | -0.324 | 1.181 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S01 | D05-S01/20 | Y120 | -0.224 | -0.319 | 1.421 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S01 | D05-S01/5 | Y120 | -0.304 | -0.410 | 1.352 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S01 | D05-S01/5 | Y250 | -0.405 | -0.466 | 1.153 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S01 | D05-S01/5 | Y60 | -0.324 | -0.383 | 1.182 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S02 | D05-S02/10 | Y120 | -0.350 | -0.436 | 1.246 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S02 | D05-S02/10 | Y250 | -0.453 | -0.509 | 1.125 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S02 | D05-S02/10 | Y60 | -0.336 | -0.377 | 1.122 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S02 | D05-S02/20 | Y120 | -0.260 | -0.377 | 1.450 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S02 | D05-S02/20 | Y60 | -0.240 | -0.295 | 1.230 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S02 | D05-S02/5 | Y120 | -0.391 | -0.479 | 1.226 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S02 | D05-S02/5 | Y250 | -0.494 | -0.554 | 1.121 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S02 | D05-S02/5 | Y60 | -0.396 | -0.447 | 1.128 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S03 | D05-S03/10 | Y250 | 0.389 | 0.086 | 0.222 | KISMEN_MEKANIK;MEKANIK_IZ_YOK;KISMEN_MEKANIK;MEKANIK_IZ_YOK | BELIRSIZ |
| D05-S03 | D05-S03/20 | Y250 | 0.345 | 0.059 | 0.172 | KISMEN_MEKANIK;MEKANIK_IZ_YOK;MEKANIK_IZ_YOK;MEKANIK_IZ_YOK | MEKANIK_IZ_YOK |
| D05-S03 | D05-S03/5 | Y250 | 0.410 | 0.147 | 0.357 | KISMEN_MEKANIK;MEKANIK_IZ_YOK;MEKANIK_ACIKLAR;KISMEN_MEKANIK | BELIRSIZ |
| D05-S04 | D05-S04/10 | Y120 | -0.235 | -0.329 | 1.404 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S04 | D05-S04/10 | Y250 | -0.317 | -0.401 | 1.266 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S04 | D05-S04/10 | Y60 | -0.237 | -0.297 | 1.252 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S04 | D05-S04/5 | Y120 | -0.242 | -0.361 | 1.495 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S04 | D05-S04/5 | Y250 | -0.336 | -0.419 | 1.245 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S04 | D05-S04/5 | Y60 | -0.268 | -0.349 | 1.301 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S08 | D05-S08/10 | Y120 | -0.302 | -0.427 | 1.417 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S08 | D05-S08/10 | Y250 | -0.348 | -0.517 | 1.485 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S08 | D05-S08/10 | Y60 | -0.286 | -0.372 | 1.303 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S08 | D05-S08/20 | Y120 | -0.219 | -0.379 | 1.726 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S08 | D05-S08/5 | Y120 | -0.333 | -0.467 | 1.401 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S08 | D05-S08/5 | Y250 | -0.390 | -0.547 | 1.404 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D05-S08 | D05-S08/5 | Y60 | -0.336 | -0.431 | 1.284 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S01 | D06-S01/10 | Y120 | -0.346 | -0.443 | 1.279 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S01 | D06-S01/10 | Y250 | -0.456 | -0.459 | 1.006 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S01 | D06-S01/10 | Y60 | -0.382 | -0.414 | 1.084 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S01 | D06-S01/20 | Y120 | -0.233 | -0.362 | 1.557 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S01 | D06-S01/20 | Y250 | -0.350 | -0.372 | 1.062 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S01 | D06-S01/20 | Y60 | -0.270 | -0.324 | 1.200 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S01 | D06-S01/5 | Y120 | -0.394 | -0.502 | 1.275 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S01 | D06-S01/5 | Y250 | -0.527 | -0.534 | 1.013 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S01 | D06-S01/5 | Y60 | -0.433 | -0.480 | 1.110 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/10 | Y120 | -0.335 | -0.499 | 1.492 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/10 | Y250 | -0.432 | -0.589 | 1.363 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/10 | Y60 | -0.339 | -0.405 | 1.193 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/20 | Y120 | -0.235 | -0.441 | 1.876 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/20 | Y250 | -0.372 | -0.556 | 1.494 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/20 | Y60 | -0.248 | -0.313 | 1.263 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/40 | Y120 | -0.220 | -0.341 | 1.552 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/40 | Y250 | -0.334 | -0.517 | 1.546 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/5 | Y120 | -0.388 | -0.538 | 1.387 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/5 | Y250 | -0.499 | -0.627 | 1.257 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/5 | Y60 | -0.391 | -0.468 | 1.196 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S03 | D06-S03/60 | Y250 | -0.254 | -0.452 | 1.776 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S04 | D06-S04/20 | Y120 | -0.265 | -0.298 | 1.127 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S04 | D06-S04/20 | Y250 | -0.305 | -0.347 | 1.136 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S04 | D06-S04/40 | Y120 | -0.238 | -0.281 | 1.182 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S04 | D06-S04/40 | Y250 | -0.316 | -0.338 | 1.069 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S04 | D06-S04/60 | Y120 | -0.236 | -0.252 | 1.068 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S04 | D06-S04/60 | Y250 | -0.306 | -0.327 | 1.067 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S05 | D06-S05/tek | Y250 | -0.279 | -0.409 | 1.464 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S09 | D06-S09/20 | Y120 | -0.281 | -0.457 | 1.623 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S09 | D06-S09/20 | Y250 | -0.435 | -0.569 | 1.308 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S09 | D06-S09/20 | Y60 | -0.278 | -0.328 | 1.182 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S09 | D06-S09/60 | Y120 | -0.205 | -0.274 | 1.336 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D06-S09 | D06-S09/60 | Y250 | -0.363 | -0.464 | 1.278 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D10-S02 | D10-S02/tek | Y250 | -0.254 | -0.171 | 0.672 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;KISMEN_MEKANIK | MEKANIK_ACIKLAR |
| D10-S09 | D10-S09/tek | Y120 | 0.230 | 0.444 | 1.930 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D10-S09 | D10-S09/tek | Y250 | 0.371 | 0.595 | 1.606 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D10-S09 | D10-S09/tek | Y60 | 0.252 | 0.308 | 1.226 | MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR;MEKANIK_ACIKLAR | MEKANIK_ACIKLAR |
| D10-S10 | D10-S10/tek | Y250 | 0.350 | 0.138 | 0.395 | MEKANIK_ACIKLAR;KISMEN_MEKANIK;KISMEN_MEKANIK;KISMEN_MEKANIK | KISMEN_MEKANIK |

## 7. Veri eksiklikleri ve teknik riskler

| risk | ayrinti | etki | onlem |
|---|---|---|---|
| Olay tanımı seçim etkisi (M01) | K55 A farkları ilk geçiş etiketinin eseri olmaya aday: bilgisiz veride aynı fark; denetçi kontrolünde seçimsiz etiketle gerçek d ~%90 küçülüyor (Y60) | yüksek | mekanizma testlerinde olay günü etiketi yerine seçimsiz / sinyal sabit tasarım; her testte sentetik sıfır koşusu (ONKAYIT_K56 v1.1-2) |
| Sentetik sınama DGP'ye duyarlı | oran oynaklık düzeyi ve GARCH / kaldıraç spekine bağlı; oynaklık / hacim hücrelerinin sınıfı spekle değişiyor; sentetik Y60 olay oranı gerçeğin ~2 katı | orta | gerçeğe kalibre oynaklık, GJR kaldıraç, sıçrama spekleri; olay oranını rapora yaz |
| Varyant ve ufuk seçimi | v1.0 her hücrede en kısa pencere ve Y60'ı sınadı; 12 hücrenin KEŞİF'i Y120 / Y250'den; Y250'de gecikme ölçütü mekanik eseri ayırmıyor | orta | KEŞİF'i sağlayan bütün (varyant, ufuk) satırları (v1.1-3); gecikme yalnız bilgi |
| Keşif verisinin yeniden kullanımı | K56 hipotezleri K55 KEŞİF 2016-21 sonuçlarından üretildi; aynı dönemde doğrulama döngüseldir | yüksek | DOĞRULANMIŞ sınıfı için İÇ / BAĞIMSIZ dönem gerekir (Cemal kararı); yeniden kullanım kaydı (K56_KAYNAK_KAYDI) |
| KEŞİF'te hayatta kalma | K55 KEŞİF olaylarının tamamı bugün yaşayan V_ABD hisselerinden; K34 batanları 2020-10'dan önce yok | yüksek | M17: batan evren genişletme (Tiingo kotası, Cemal kararı); sonuçlar 'yaşayanlar içinde' diye sınırlanır |
| Açığa satış POZİSYONU KEŞİF'i tam kapsamıyor | FINRA SI API 2017-12-29+; hacim (Reg SHO tesis dosyaları) 2009-08+ tam | orta | M05 pozisyon ölçüsü 2018-21 alt döneminde; 2016-17 için ücretli borsa dosyaları |
| 13F eşleme ve gecikme | CUSIP -> sembol (OpenFIGI GÜNCEL sembol döndürür; CUSIP başına onlarca listeleme), 45 gün gecikme, yalnız 100 mn $ üstü yöneticiler | orta | Common Stock + US süzgeci, SEC 13(f) listesiyle tarihli ad; başvuru tarihi point-in-time |
| CIK değişimi | yeniden yapılanmada yeni CIK (APO 2022): companyfacts / Form 4 eski dönemi kaçırır | orta | SEC eski ad / CIK zinciri (formerNames, 8-K 2.01 / 425) ile CIK geçmişi |
| Yabancı özel ihraççılar ve REIT | 20-F / 40-F (BNS): Form 4 yok, IFRS; MIDAS'ta REIT / yabancı / BDC yok (2016q1 K55 kapsamı ~%66) | orta | ayrı alt grup; kapsam payını her testte raporla |
| XBRL hisse sayısı ham | bölünme ve birleşme artışını ayırmaz (TRMB 2013 bölünmesi, EXR 2023 birleşmesi, IRM 2016 satın alma); TLGTQ 2020-21 artışı ters bölünme sonrası gerçek sulandırma | yüksek (M06 için) | bölünme katsayısı (XBRL / Tiingo splitFactor) ve 8-K 2.01 / DEFM14A ile ayırma; pencereyi olaya bağla |
| İhraç formu hisse / borç ayırmıyor | 424B2 çoğunlukla banka notu (BNS); 424B5 ATM, halka arz ya da doğrudan satış olabilir | orta | hisse sayısı artışıyla ya da EDGAR metin aramasıyla doğrulama |
| 10b5-1 planı 2023 öncesi işaretsiz | işaret fiilen 2023q2+ ('1' / 'true'); öncesi dipnot / açıklama metni vekili (2016q1 S içeren Form 4'lerin %43,5'i) | orta | dipnot vekili + 2023q2+ işaretle duyarlılık; olumsuz cümleleri ayıklama |
| Kasıt kanıtı kapsamı | askıya alma ve dava bülteni kasıt kanıtı değil (resmî kuşku kaydı); kesinleşmiş karar gerekir; ad eşlemesi tarih şartlı ve 'et al.' emirleri eksik | yüksek (M14) | üç sütun: gözlenen davranış / olası mekanizma / kasıt kanıtı; kayıt yoksa 'KASIT KANITI YOK' |
| Gün içi veri yok | dağıtım / emilim işlem sırası düzeyinde ayrılamaz; MIDAS yalnız günlük toplam | yüksek (M09 / M11) | MIDAS + 13F + Reg SHO üçlemesi; ücretli TAQ yalnız Cemal kararıyla |
| İndirme hacmi ve süre | 13F ~1,1 GB, MIDAS hisse ~0,4 GB, FS 2016-20 ~1,6 GB, Form 4 ~0,25 GB, companyfacts ~5 GB | orta | Drive önbelleği, sürümlü özet (islenmis-veri), bir kez indir |
| Yahoo erişim kararsızlığı | yfinance crumb 401 / 429 (bu ortamda bir kez); batanlar yok | düşük | Tiingo splitFactor ile çapraz |
| Çoklu test | 19 hipotez × gruplar × dönemler | orta | aile = hipotez × dönem; BH q 0,10; önceden yazılı birincil ölçü |
| Lisans | Tiingo fiyatları ve FINRA ham verisi dağıtılmaz; SEC verisi kamu malı | düşük | yalnız türetilmiş özet + manifest sha |

## 8. Önerilen uygulama sırası

İlk üç adım yerel ve indirmesizdir; büyük indirmeler (5-7) yalnız 1-3'ten sonra AÇIKLANMAMIŞ etki kalırsa anlamlıdır.

| sira | adim | icerik | donem | maliyet_sure | karar_gerekir | ne_kazanilir |
|---|---|---|---|---|---|---|
| 1 | M01 gerçek veri seçimsiz kontrol (v1.1-2) | K55 paneli: KEŞİF'i sağlayan 125 (varyant, ufuk) satırında d(ilk geçiş), d(bütün nitelikli günler), d(epizotta rastgele gün); kalibre sentetik spekler | KEŞİF (yeniden kullanım kayıtlı) | yerel, indirme yok, ~30 dk | hayır | MEKANİK çıkan hücreler kesin YANLIŞ BULGU; kalan küçük aynı yönlü etki (Y60 ~-0,02..-0,05) ayrı bulgu olarak M02'ye |
| 2 | M03 / M16 / M18 yerel denetimler | ince oynaklık + GARCH, 2020-03 dışlama + beta, sektör × gün: yalnız 1. adımda kalan etki için | KEŞİF | yerel, ~15 dk | hayır | kalan etkinin oynaklık / piyasa / tema bileşeni |
| 3 | M04 / M15 haber ve birleşme bileşimi | yerel SEC başvuru özetiyle G1 / G2 / G7'de [t0−5, t0+60] 8-K maddeleri, SC TO, DEFM14A | KEŞİF | yerel, ~10 dk | hayır | büyük yükselişlerin ne kadarının ayrık habere bağlı olduğu (mekanizmanın kendisi) |
| 4 | M13 / M17 evren ve sağlayıcı (K51 P1, K52) | K51 P1 artısının yalnız V_ABD'de olması: sağlayıcı × etki; batan evren genişletme | K51'in 2023 / 2024-26 dönemleri = K55 İÇ / BAĞIMSIZ ile örtüşür | yerel + Tiingo kotası | EVET (dönem açma + Tiingo kotası) | K51 küçük artısının hayatta kalma eseri olup olmadığı |
| 5 | M09 / M10 Form 4 (yalnız 1-3'ten sonra AÇIKLANMAMIŞ gerçek etki kalırsa) | Insider DS KEŞİF (ham zipler yerelde); plansız S, P | KEŞİF | yerel / ~250 MB | hayır (SEC izni var) | dağıtım / içeriden bilgi |
| 6 | M08 / M11 13F + OpenFIGI (yalnız kalan etki varsa) | 13F KEŞİF ~1,1 GB, CUSIP eşleme (Common Stock + US) | KEŞİF | indirme ~1,1 GB + eşleme ~1-2 saat | EVET (Drive alanı / süre) | kurumsal birikim / emilim |
| 7 | M02 / M11 / M12 MIDAS (yalnız kalan etki varsa) | MIDAS hisse dosyası KEŞİF ~0,4 GB; işlem büyüklüğü, gizli / tek lot altı pay | KEŞİF | indirme ~0,4 GB | EVET | likidite / emilim (REIT / yabancı hariç) |
| 8 | M05 açığa satış (yalnız kalan etki varsa) | Reg SHO tesis dosyaları (2016+), FINRA SI (2017-12+), FTD | KEŞİF (pozisyon 2018-21) | küçük-orta indirme | hayır | sıkışma |
| 9 | M14 resmî kayıt eşlemesi | kesinleşmiş kararlar (mahkeme, SEC / FINRA idari karar, uzlaşma) + resmî kuşku kayıtları; tarih şartlı ad + CIK eşleme | KEŞİF | küçük | hayır | kasıt yalnız kesinleşmiş kararla |
| 10 | Doğrulama dönemi | kalan her GÜÇLÜ AÇIKLAMA için İÇ 2022-23 (ve BAĞIMSIZ 2024-26) | İÇ / BAĞIMSIZ | - | EVET (dönem açma) | DOĞRULANMIŞ MEKANİZMA sınıfı için zorunlu |

## Denetim: bağımsız gözden geçirme bulguları ve durumu

Dört denetçi (sentetik geçerlilik, envanter doğruluğu, veri kaynakları, ön kayıt / aşırı iddia); tam metin K56_DENETIM_BULGULARI.csv.

| mercek | ciddiyet | baslik | durum | nasil |
|---|---|---|---|---|
| sentetik | orta | Ufuk uyumsuzluğu: 12 KEŞİF hücresinin KEŞİF'i Y250/Y120'den geliyor, sentetik karar ise yalnız Y60'tan | DÜZELTİLDİ | v1.1-3: KEŞİF'i sağlayan bütün (varyant, ufuk) satırlarında ek sentetik sınama (K56_SECIM_SENTETIK_KESIF.csv) |
| sentetik | orta | Gecikme ölçütü mekanik eseri gerçek etkiden ayırmıyor; Y250'de geçersiz | DÜZELTİLDİ | v1.1-2: karar ölçütü seçimsiz kontrol; gecikme yalnız bilgi |
| sentetik | dusuk | Oran 'gerçek etkinin payı' değil, DGP'ye bağlı bir büyüklük; gerçek veride küçük ama sıfır olmayan aynı yönlü bilgi var | KISMEN | rapor seçimsiz kontrol bilgisini ve DGP duyarlılığını yazıyor; kalibre spekler Faz 1'de (v1.1-2) |
| sentetik | dusuk | '4 BELİRSİZ hücre yalnız GARCH'lı evrende mekanik' ifadesi D06-S04 için yanlış | DÜZELTİLDİ | BELİRSİZ gerekçesi spek sınıflarından üretiliyor; M03 metni düzeltildi |
| sentetik | dusuk | 'En iyi varyant' fiilen p tabanındaki ilk satır (en kısa pencere) | DÜZELTİLDİ | v1.1-3 ek sınama bütün KEŞİF varyantlarını kapsıyor |
| sentetik | dusuk | Önkayıtta iç çelişki: sentetik sonuç tek başına YANLIŞ BULGU mu, aday mı | DÜZELTİLDİ | v1.1-1 |
| envanter | kritik | 'İLİŞKİ VAR, NEDEN BELİRSİZ' ön sınıfı, kaynakta başarısız ya da kararsız olan 61 bulguya veriliyor | DÜZELTİLDİ | mekanik kural (ONKAYIT v1.1-4): kaynakta başarısız -> ETKİ SAĞLAM DEĞİL; İLİŞKİ VAR yalnız DESTEKLENİYOR / KEŞİF |
| envanter | orta | Aynı ölçüm farklı satırlarda farklı sınıf alıyor (kürasyon tutarsız) | DÜZELTİLDİ | sınıf artık kaynak kararından mekanik; kürasyon sınıfı yalnız ETKİ YOK / VERİ YETERSİZ için kullanılıyor |
| envanter | orta | 'En iyi 20 hisse çıkarıldı' satırları yapı gereği eksi çıkıyor ama 'ilişki' sayılıyor | DÜZELTİLDİ | E20 / EN20 satırları YÖNTEM DENETİMİ (sonuca göre seçilmiş alt küme) |
| envanter | orta | K53-T7 tanım gereği ortaya çıkan bir örüntü ama 'İLİŞKİ VAR' sayılıyor | DÜZELTİLDİ | YANLIŞ BULGU ADAYI (tanımsal) |
| envanter | orta | D06-S04 için 'M01 yalnız GARCH'lı evrende mekanik' gerekçesi yanlış | DÜZELTİLDİ | BELİRSİZ gerekçesi spek sınıflarından üretiliyor; M03 metni düzeltildi |
| envanter | orta | K56_ACIKLANMAMIS_BULGULAR mantığı listeyi şişiriyor | DÜZELTİLDİ | liste: AÇIKLANMADI / ADAY / VERİ YETERSİZ / BETİMLEYİCİ ayrı; ETKİ YOK, ETKİ SAĞLAM DEĞİL, YÖNTEM DENETİMİ dışarıda |
| envanter | orta | K51-H1'in 'K54 evren düzeltmesinde değişmiyor' iddiası K54 ile çelişiyor | DÜZELTİLDİ | kürasyon düzeltmesi (K54 ETKİLENMİŞ yazıldı; envanter denetimine kayıt) |
| envanter | dusuk | VEKIL → 'ALTERNATİF AÇIKLAMA' gerekçesi kanıtsız ve hiç test yapılmadan veriliyor | DÜZELTİLDİ | ALTERNATİF AÇIKLAMA yalnız hesaplanmış vekil ya da gerekçeli atama |
| envanter | dusuk | Mekanik envanter denetiminde eşleştirme hatası var, karar karşılaştırması eksik | DÜZELTİLDİ | önce tam kimlik, sonra eşleme tablosu, sonra en kısa önek; K51v12 / K52 / K53 karar sözcükleri de denetleniyor |
| envanter | dusuk | Küçük tutarsızlıklar: ters yön sayısı, D06-S05 oranı, eksik K55 sonuç satırı, sızıntı iddiası | DÜZELTİLDİ | ters yönlü 20 (19 + D03-S02); K55-SONUC satırı eklendi; D06-S05 oranı Y60 diye yazılıyor |
| kaynak | orta | 10b5-1 payı raporda kendi içinde çelişkili; 2023 sonrası işaret ölçüsü yanlış kodlanmış | DÜZELTİLDİ | %2,7 metinleri kaldırıldı; işaret '1' + 'true', payda S içeren Form 4, tam dosya |
| kaynak | orta | Askıya alma ad eşlemesi: 10 eşleşmenin biri yanlış pozitif, hiçbiri panel penceresine düşmüyor; 'şirket satırı' tanımı yanlış | DÜZELTİLDİ | tarih şartlı eşleme (ilk başvuru, ad geçerliliği), belirsiz ad ayrı; 9 eşleşme, panelde 0; 'et al.' emirleri AÇIK |
| kaynak | orta | K30_ALIM KEŞİF dönemini hiç kapsamıyor ama kesif_eksik=False | DÜZELTİLDİ | kapsam 2022-01..2026-03, KEŞİF YOK; M10 için Insider DS P kodları |
| kaynak | orta | MIDAS hisse dosyası K55 evreninin yaklaşık üçte birini kapsamıyor; 'KEŞİF tam' ifadesi ve kesif_eksik=False aşırı | DÜZELTİLDİ | KEŞİF kapsamı 'kısmi' (2016q1 K55 kapsamı ölçülüyor); REIT / yabancı / BDC yok |
| kaynak | orta | OpenFIGI 9/10 sonucu adi hisse eşlemesini kanıtlamıyor | DÜZELTİLDİ | test adi hisse CUSIP'leri + örneklem geri eşlemesiyle; Common Stock + US süzgeci; güncel sembol notu |
| kaynak | orta | Sulandırma ölçüsü: bölünme düzeltmesi yok, pencere KEŞİF değil, birleşme ayrılmıyor; TLGTQ yanlış etiketli | DÜZELTİLDİ | KEŞİF bildirimleriyle sınırlı, HAM diye işaretli; TLGTQ yorumu düzeltildi; bölünme / birleşme ayrımı Faz 1 |
| kaynak | dusuk | Açığa satış kapsamı rapor içinde çelişkili (Reg SHO 2018-08+ ile 2009-08+) | DÜZELTİLDİ | hacim 2009-08+ (tesis) / pozisyon 2017-12+ ayrımı bütün metinlerde |
| kaynak | dusuk | kesif_eksik sütunu anahtar kelimeyle hesaplanıyor: YAHOO yanlış True, K55 panel kapsamı yanıltıcı | DÜZELTİLDİ | açık KESIF_KAPSAM alanı (tam / kısmi / yok); K55 paneli yıl bazında hisse sayısı |
| kaynak | dusuk | Durum birleştirmesi ATLANDI'yı KISMI yapıyor; kayıtsız 'denendi' iddiası | DÜZELTİLDİ | ATLANDI ayrı; NASDAQ_HALT 'belgeden, istek yok' |
| kaynak | dusuk | İstek günlüğü yalnız son koşuyu içeriyor; 'indirilen 2,1 MB' gerçek trafiği göstermiyor | DÜZELTİLDİ | temiz önbellekle yeniden koşu; yöntem sütunu; HEAD boyları indirilen sayılmıyor |
| kaynak | dusuk | Bölünme denetimi yalnız 3 seçilmiş dev hisseye bakıyor; örneklemdeki batanlar V_ABD'de yok | KISMEN | durum KISMI ve sınır yazıldı; batanlar için XBRL / fiyat çapraz denetimi Faz 1 |
| kaynak | dusuk | K56_ERISIM_SEC_FS_DS.csv aslında companyfacts tablosu | DÜZELTİLDİ | tablo companyfacts satırına bağlandı |
| kaynak | dusuk | SEC User-Agent sunucu denetimi alt dize karşılaştırmasıyla yapılıyor (gerçekleşmiş sızıntı yok) | DÜZELTİLDİ | sunucu adı sec.gov ile bitmeli; SEC dışına yönlendirme durdurur; test 10c |
| kural | kritik | 'İLİŞKİ VAR, NEDEN BELİRSİZ' 65 bulgunun 46'sı kaynakta başarısız: aşırı iddia | DÜZELTİLDİ | aynı kural (v1.1-4) |
| kural | orta | YANLIŞ BULGU sınıfı (21) yalnız sentetik kanıta dayanıyor; ön kayıt kendi içinde çelişkili | DÜZELTİLDİ | YANLIŞ BULGU ADAYI (M01); ön kayıt v1.1-1 3-1(a) ile 6. bölümü uzlaştırdı |
| kural | orta | M01'in gerçek veride 'kesinleşme' kuralı tanımsız, sıra 1'e kayıtsız yeni olay tanımı eklenmiş | DÜZELTİLDİ | v1.1-2 seçimsiz kontrol protokolü; gecikme yalnız bilgi; kayıtsız yeni olay tanımı sıra 1'den çıkarıldı |
| kural | orta | '4 BELİRSİZ hücre yalnız GARCH evreninde mekanik' iddiası D06-S04 için yanlış | DÜZELTİLDİ | BELİRSİZ gerekçesi spek sınıflarından üretiliyor; M03 metni düzeltildi |
| kural | orta | Talimat süzgecinde önceki testler yanlış özetlenmiş ('Ç100, Ç102, Ç103, Ç107: hepsi sıfır') | DÜZELTİLDİ | Ç100 / Ç102 / Ç103 / Ç107 özeti düzeltildi |
| kural | orta | Hipotez kaydı sonuçlar görüldükten sonra yazıldı, kilitsiz; bazı 'önceden yazılı' tahminler zaten bilinen sonuçlar | DÜZELTİLDİ | kayıt v1.1 olarak donduruldu, sürüm ve on_kanit alanı; bilinen sayılar test sayılmıyor |
| kural | orta | Uygulama sırası K51-K54 bulgularının İÇ / BAĞIMSIZ dönem gerektirdiğini işaretlemiyor | DÜZELTİLDİ | dönem sütunu; K51-K54 adımı 'EVET (dönem açma)'; sıra 5-8 koşullu |
| kural | orta | Kasıt kanıtı tanımı geniş: SEC askıya alması ve dava bülteni kasıt kanıtı değildir | DÜZELTİLDİ | v1.1-5: kasıt yalnız kesinleşmiş karar; askıya alma / dava = resmî kuşku kaydı |
| kural | dusuk | Ters yönlü KEŞİF sayısı 19 değil 20 | DÜZELTİLDİ | 20 (IZ_KARNE'deki 19 açıklandı) |
| kural | dusuk | Sentetik özet hesaplanamayan hücreyi TANIMSIZ değil BELİRSİZ sınıflıyor | DÜZELTİLDİ | boş / hatalı satır TANIMSIZ (HATA); test 9c |
| kural | dusuk | Erişim örneklemi ön kayıttan sapıyor, eşleşme oranları bilgi vermiyor | DÜZELTİLDİ | v1.1-7 sapma kaydı; eşleşme olay çeyreğinde ölçülüyor; GECTI için >= %60 |
| kural | dusuk | 10b5-1 dipnot payı eski kalmış (%2,7 ile 0,435 çelişiyor) | DÜZELTİLDİ | %2,7 metinleri kaldırıldı; işaret '1' + 'true', payda S içeren Form 4, tam dosya |
| kural | dusuk | Ön sınıf kuralları ve iki yeni etiket ön kayıt eki olmadan sonuçtan sonra eklenmiş | DÜZELTİLDİ | v1.1-4 ön kayıt eki |
| kural | dusuk | Kaynak kaydı eksik: sentetik koşunun K55_VARYANTLAR okuması çıktı klasöründe yok | DÜZELTİLDİ | sentetik kaynak kaydı çıktı klasörüne kopyalanıyor |
| kural | dusuk | Açık işler: çıktılar commit'lenmemiş, IZ_KARNE satırı ve Drive kopyası yok | DÜZELTİLDİ | commit + IZ_KARNE + indeks bu görevde; Drive kopyası Colab komutu (python K56.py drive) AÇIK |
| kural | dusuk | Sentetik kalibrasyon ve 'bilgisiz veri' varsayımı sınanmamış | KISMEN | belge cümlesi 'yön bilgisi yok' diye düzeltildi; olay oranı / oynaklık kalibrasyonu Faz 1 (v1.1-2) |

## Ek: envanter denetimi uyuşmazlıkları

| tur | kimlik | kaynak | ayrinti |
|---|---|---|---|
| karar_eksik_sozcuk | K51v12-H-E-AYI | K51_HIPOTEZ_KARARLARI.csv | kaynak kararları DESTEKLENMİYOR / TUTMAZ / YETERSİZ ÖRNEKLEM; envanterde geçmeyen: ['DESTEKLENMİYOR'] |
| karar_eksik_sozcuk | K52-H0b-P1 | K51_ANALIST_EK_KATKI_TESTI.csv | kaynak kararları DESTEKLENMİYOR / TUTAR / TUTMAZ; envanterde geçmeyen: ['TUTAR'] |
| karar_eksik_sozcuk | K52-H4-P1 | K51_ANALIST_EK_KATKI_TESTI.csv | kaynak kararları DESTEKLENMİYOR / H4 DESTEKLENMİYOR / TUTMAZ; envanterde geçmeyen: ['H4 DESTEKLENMİYOR'] |
| karar_eksik_sozcuk | K52-H6AYI-P1 | K51_ANALIST_EK_KATKI_TESTI.csv | kaynak kararları DESTEKLENMİYOR / TUTMAZ / YETERSİZ ÖRNEKLEM; envanterde geçmeyen: ['DESTEKLENMİYOR'] |
| karar_eksik_sozcuk | K52-H4-P2 | K51_ANALIST_EK_KATKI_TESTI.csv | kaynak kararları DESTEKLENMİYOR / H4 DESTEKLENİYOR (çoğu sonra, H0 desteklenmiyor) / TUTMAZ; envanterde geçmeyen: ['H4 DESTEKLENİYOR (çoğu sonra, H0 desteklenmiyor)'] |
| karar_eksik_sozcuk | K52-H6AYI-P2 | K51_ANALIST_EK_KATKI_TESTI.csv | kaynak kararları DESTEKLENMİYOR / TUTAR / TUTMAZ / YETERSİZ ÖRNEKLEM; envanterde geçmeyen: ['DESTEKLENMİYOR', 'TUTAR'] |
| karar_eksik_sozcuk | K53-T6 | K53_HIPOTEZ_TESTI.csv | kaynak kararları DESTEKLENMİYOR / TUTMAZ / bilgi; envanterde geçmeyen: ['bilgi'] |
| k55_sinif_kurali | K55-D01-S04 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu KUCUK_ETKI -> kural BASARISIZ |
| k55_sinif_kurali | K55-D01-S09 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu TERS_YONLU -> kural BASARISIZ |
| k55_sinif_kurali | K55-D02-S01 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu TERS_YONLU -> kural BASARISIZ |
| k55_sinif_kurali | K55-D02-S03 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu KUCUK_ETKI -> kural BASARISIZ |
| k55_sinif_kurali | K55-D02-S04 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu TERS_YONLU -> kural BASARISIZ |
| k55_sinif_kurali | K55-D02-S07 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu TERS_YONLU -> kural BASARISIZ |
| k55_sinif_kurali | K55-D03-S01 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu TERS_YONLU -> kural BASARISIZ |
| k55_sinif_kurali | K55-D03-S04 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu TERS_YONLU -> kural BASARISIZ |
| k55_sinif_kurali | K55-D03-S05 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu KUCUK_ETKI -> kural BASARISIZ |
| k55_sinif_kurali | K55-D03-S06 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu KUCUK_ETKI -> kural BASARISIZ |
| k55_sinif_kurali | K55-D03-S08 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu TERS_YONLU -> kural BASARISIZ |
| k55_sinif_kurali | K55-D03-S09 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu TERS_YONLU -> kural BASARISIZ |
| k55_sinif_kurali | K55-D03-S10 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu TERS_YONLU -> kural BASARISIZ |
| k55_sinif_kurali | K55-D04-S05 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu KUCUK_ETKI -> kural BASARISIZ |
| k55_sinif_kurali | K55-D04-S07 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu VERI_YETERSIZ -> kural BASARISIZ |
| k55_sinif_kurali | K55-D04-S08 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu KUCUK_ETKI -> kural BASARISIZ |
| k55_sinif_kurali | K55-D05-S05 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu KUCUK_ETKI -> kural BASARISIZ |
| k55_sinif_kurali | K55-D05-S06 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu KUCUK_ETKI -> kural BASARISIZ |
| k55_sinif_kurali | K55-D05-S07 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu KUCUK_ETKI -> kural BASARISIZ |
| k55_sinif_kurali | K55-D06-S02 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu KUCUK_ETKI -> kural BASARISIZ |
| k55_sinif_kurali | K55-D10-S04 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu KUCUK_ETKI -> kural BASARISIZ |
| k55_sinif_kurali | K55-D10-S09 | K55_HUCRE_SONUC + K55_VEKIL | okuyucu VEKIL -> kural BASARILI |
| kurasyon_duzeltmesi | K51-H1 | K54_ESKI_YENI_TEST_KARSILASTIRMA.csv (K51 P1, 2024-26) | gecen_testler: envanter denetçisi: 'K54 evren düzeltmesinde değişmiyor' iddiası K54 ile çelişiyor (ETKİLENMİŞ) |
