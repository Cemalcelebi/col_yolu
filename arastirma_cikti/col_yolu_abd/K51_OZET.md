# K51 — ABD'de Çöl Yolu formasyonu: sonuç ve plan karşılaştırması (29 Ekim 2026)

**Sonuç:** Çöl Yolu formasyonu ABD'de, maliyet sonrası alınabilir bir öngörü avantajı göstermedi. Önceden yazılı kurala göre **İZ DEĞİL**.

- Resmi ölçüt (FI_OLCUT eşli fark) de İZ DEĞİL diyor.
- Akademik yöntemler (meta-etiketleme, CNN, LSTM) bağımsız testte ölçülebilir ek katkı sağlamadı.

Kod: `COL_YOLU_ABD.py` (CY v1.1, tek dosya, Colab'da çalışır). Test: `test_col_yolu_abd.py` (11/11). Ayrıntılı tablolar: `cy_rapor.md` ve `cy_*.csv`.

## 1. Veri

| Pazar | Hisse | Hisse-gün | Dönem | Not |
|---|---|---|---|---|
| ABD | 2.752 (likit) | 3,18 milyon | 2016-06 → 2026-07 | Bugün işlem gören 1.411 + nakdi biten 1.435 + batan 422 (Tiingo). Erken biten 101 hisse olaylarda var. |
| Avrupa | 561 | 1,14 milyon | 2016 → 2026-06 | Yalnız bugün işlem görenler |
| BIST | 574 | 0,84 milyon | 2016 → 2026-06 | Ayrı rapor |

- Fiyatlar bölünme ve temettüye göre düzeltilmiş (Yahoo auto-adjust, Tiingo adj).
- 31.08.2026'da kesilir (fon krizi kuralı).
- Batan ve küçük şirketler evrene ilk SEC nakit pisti bildiriminden itibaren girer. Bu, o gün bilinen bilgidir.
- **Kısıt:** 2016-2020 eğitim döneminde yalnız bugün işlem gören hisseler var (hayatta kalma yanlılığı). Batan örneklemi 2020-10 sonrası ve yalnız nakdi biten şirketlerden; ağırlık 1,83.

## 2. Olay sayıları (ABD)

| Küme | Eğitim 2016-20 | Doğrulama 2021-22 | Test 2023 | Test 2024-26 |
|---|---|---|---|---|
| P1 oluşurken | 505 | 910 | 906 | 1.316 |
| P2 kırılım | 261 | 310 | 476 | 667 |
| ES eş (imzasız) | 782 | 1.534 | 896 | 2.382 |
| HT hacimli taban | — | — | 58 | 191 |

## 3. Hipotez kararları (ABD; eşik: rastgeleden +5 puan, aralık artı, net artı, iki test döneminde)

| Kod | Hipotez | Karar | Önemli sayı |
|---|---|---|---|
| H1 | Çöl Yolu oluşurken (P1) rastgeleden iyi | DESTEKLENMİYOR | +2,5 / +2,4 puan. Net getiri tabanla aynı; işlem başına −%1,1 ile −%1,8. |
| H2 | Küçük mum imzası fark yaratıyor (P1 − ES) | DESTEKLENMİYOR | +2,7 / +1,6 puan, aralık 0'ı içeriyor |
| H3 | Kırılım (P2) rastgeleden iyi | DESTEKLENMİYOR | +1,0 / +0,6 puan |
| H4 | Meta-etiketleme seçimi iyileştiriyor | DESTEKLENMİYOR | +6,6 / +2,6 puan, aralık 0'ı içeriyor |
| H5 / H6 | CNN seçimi iyileştiriyor / sayısal modelden iyi | DESTEKLENMİYOR | CNN − sayısal AUC −0,05 / −0,06 |
| H7 | Meta portföyü piyasayı, rastgeleyi ve SPY'yi geçiyor | DESTEKLENMİYOR | 2023: +%12,5 (SPY +%26,7). 2024-26: −%29,5 (SPY +%67,7). |
| H8 | Aşırı uyum riski düşük | DESTEKLENMİYOR | PBO 0,39 ama DSR 0,03 |
| H10 | Avrupa'da tekrar ediyor | DESTEKLENMİYOR | P2 2023 +10 puan, 2024-26 −4 puan |
| B1 | Oynaklığa bağlı bariyerle P1 | DESTEKLENMİYOR (en yakın aday) | 2023: +2,6 puan [−0,7]. 2024-26: +4,3 [+1,6]. |
| B2 | Önceki aday "hacimli taban" | DESTEKLENMİYOR | −5,5 / −1,2 puan. Eski cetvelde 2024-26 +%12,5 [−3,3]: önceki +%14,9 tekrarlanmadı. |
| B4 | LR → GBM → CNN → LSTM merdiveni | Hiçbir basamak geçmedi | Sisteme alınan: birincil kural |
| B5 | Özellik grupları (mum, oynaklık, hacim, akış, trend, momentum, likidite, çöl) | Hiçbiri ek bilgi taşımıyor | AUC farkları ±0,03 |
| B7 | Kontroller (negatif, pozitif, plasebo) | Üçü de beklendiği gibi | Karışık etiket AUC ~0,5; geleceği gören özellik AUC 0,78-0,83; plasebo 0 |
| B9 | Sıkı portföy (piyasa + eşleşik rastgele %90 + SPY) | Hiçbiri geçmedi | P1 bütün adaylar 2024-26 −%48 (MDD −%56) |
| D1 | Kırılımdan 10 gün sonra hâlâ kutu üstündeyse al | İZ DEĞİL | ABD 2016-22 −7,5 puan. Avrupa +4,6 puan, aralık 0'ı içeriyor. |

Resmi ölçüt (CLAUDE.md, FI_OLCUT: ABD + Avrupa dört hücre) P1, P2 ve HT için İZ DEĞİL verdi:
- P1 ABD +%3,0 / +%4,8 r60 eşli fark, ama sıra ≤ 0,51 ve portföy eşli %90'ın altında.
- Avrupa'da fark eksi.

## 4. Senin planınla karşılaştırma

| Plan maddesi | Yapılan | Sonuç / ders |
|---|---|---|
| Meta-labeling Sharpe/Calmar'ı garanti etmez, test edilmeli | Birincil, meta ve birleşim aynı dönemde: işlem sayısı, precision, net, MDD, Sharpe, Calmar | Planın uyarısı doğru çıktı: meta 2023'te yardım etti gibi (+6,6 puan), 2024-26'da etmedi. |
| Sabit ve oynaklığa bağlı bariyer karşılaştırılsın | İkisi aynı örneklerde | Oynak bariyer biraz daha iyi ayırıyor (2024-26 +4,3), ama iki dönemde tutmuyor. |
| Aynı gün hedef ve stop: sıra uydurulmasın | Belirsizler işaretlendi, çıkarılarak ayrıca karar verildi (taban da belirsizsiz) | P1'de belirsiz yok, hacimli tabanda %1,7. Sonuç değişmiyor. |
| Önce basit model, karmaşık ancak basiti geçerse | Merdiven + zincir kuralı | Lojistik bile birincil kuralı iki dönemde geçemedi. GBM, CNN ve LSTM alınmadı. |
| CNN'in sayısal modelin üstüne kattığı bilgi | Doğrulamada yığma, testte AUC farkı | Katkı yok; CNN tek başına sayısal modelden kötü. |
| LSTM yalnız ek katkı verirse | Aynı yığma testi | Katkı yok. |
| Özellik grupları ayrı ayrı | 8 grup çıkarma / yalnız-grup; akış (CMF, OBV, A/D, MFI) hacimden ayrı | Hiçbir grup ek bilgi taşımıyor. Akış olumlu değil (önceki ABD bulgusuyla uyumlu). |
| Safha 2 tespitinde safha 3 mumu kullanılmasın | Bütün ölçüler o gün ve öncesi; testle denetlendi | Sızıntı testi geçti. Pozitif kontrol hattın sinyal görebildiğini gösterdi. |
| Hacimli taban adayı yeniden | Üçlü bariyer + eski cetvel + Avrupa + BIST | Tekrarlanmadı. BIST'te belirgin kötü (−%35). |
| Purging/embargo, walk-forward, PBO, final test seçimde kullanılmasın | Hepsi; PBO hem ızgara hem model × pay | Izgara PBO 0,39, model PBO 0,57. Model seçimi aşırı uyum riski taşıyor. |
| Aynı gün sinyaller bağımsız değil | Ay kümeli ve hisse × çeyrek kümeli aralık; portföyde beta/alfa; sektör HHI | P1 portföyünün betası 0,85-1,24, alfası eksi. Sektör yoğunlaşması orta (HHI 0,13-0,25). |
| Yıl, rejim, likidite kırılımları | Hepsi + sektör rüzgârı | Etki küçük ve dağınık. En iyi yıllar 2023-25 (+3-5 puan); 2018, 2020 ve 2026 eksi. |
| BIST ayrı | Ayrı | BIST'te hiçbir küme tutmuyor. |

**Planda olup bugün yapılamayan:** tam batan evreni. Tiingo ücretsiz kotası dolu; Kasım'da kalan yaklaşık 374 batan şirket indirilebilir.

## 5. Bağımsız denetim

Üç ayrı denetçi çalıştırıldı: kod denetimi, plan uyumu, sonuç denetimi ("ters düz"). Bulunan hatalar sonuç görülmeden düzeltildi (commit 3346f03):
- batan ağırlığı
- piyasa kıyasının kuyruğu
- belirsizsiz taban
- eşleşik rastgele portföy
- Holm p değeri
- model PBO'su
- batan bayrağı

Sonuç denetçisinin bulguları aşağıdaki bölümdedir.

### Sonuç denetçisinin bulguları (bağımsız yeniden hesap)

Karar doğrulandı. Ham fiyatlardan kurulan üçlü bariyer, 6.892 test olayında etiketle %100 eşleşti; H1 sayıları birebir tuttu. Kararı tersine çevirecek bir hata yok. Rapora eklenmesi gerekenler:

1. **Küçük artı etkinin tamamı bugün hâlâ işlem gören hisselerden geliyor.**

   | Kaynak | 2023 | 2024-26 |
   |---|---|---|
   | Bugün işlem gören (V_ABD) | +5,3 puan | +6,4 puan |
   | Sıkıntılı + batmış (K34) | −3,2 puan | −2,5 puan |
   | Yalnız batmış (Tiingo) | −9,7 puan | −5,9 puan |

   - "Bugün işlem görüyor" bilgisi sinyal günü bilinemez. Yani bu ayrım gelecekle yapılmış bir seçimdir, alınabilir değildir.
   - Kırılım tablosundaki "rüzgâr yok +3,8" satırı da aynı ayrımdır: sektörü bilinmeyen hisseler tam olarak K34 hisseleridir. Sektör rüzgârının bir etkisi değildir.
   - Resmi ölçüt dosyası `cy_fi_olcut.csv` yalnız bugün işlem görenlerle hesaplandı (FON_IZI eşli panel; betik: oturum betiği k51olcut). Buna rağmen tutmuyor: medyan fark eksi, 2023 alt uç −0,3 puan, 2024-26 sıra 0,498.
2. **+2,4 puan birkaç hisseye dayanıyor.** En çok katkı veren 20 hisse çıkarılınca fark sıfır oluyor. 2026'da yön dönüyor (−4,3 puan). Yüksek oynaklık üçte biri 2023'te artı, 2024-26'da eksi.
3. **İmza yönü ters.** Dört imzanın hepsi olan olaylar, üç imzalılardan kötü (−1,0 / −4,4 puan). Modellerin en yüksek olasılık verdiği adaylar en düşüklerden iyi değil.
4. **Portföy kaybının sebebi.** Gidiş-dönüş maliyeti küçük hisselerde %2,2-2,4. Olayların %61'i stopla çıkıyor. Aynı kurallarla rastgele portföy de 2024-26'da −%19. SPY'nin altında kalmak sinyalden çok −%10 stop ve maliyet kuralından geliyor. Göreli sonuç (taban kadar) değişmiyor.
5. **"Belirsiz" bayrağı doğru.** P1'de %30'dan büyük gün içi aralık 235 kez var, ama hepsinde bariyer o günden önce değmiş.
6. **Önceki "hacimli taban" adayının artısı da yalnız hayatta kalanlarda.** Bugün işlem görenlerde 2024-26 +7,5 puan; sıkıntılı ve batmışlarda −5,4 puan.

**Ders.** Bugün işlem gören hisselerle yapılan testler (eski K38, FI_OLCUT panelleri) küçük hisse ve düşüş sonrası formasyonlarda iyimser çıkar. Batmış şirketler eklenince artı kaybolur.
