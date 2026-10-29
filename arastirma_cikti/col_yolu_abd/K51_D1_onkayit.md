# K51-D1 ön kaydı (29 Ekim 2026, sonuç görülmeden)

Kaynak: K51 test hücrelerinde "kırılımdan sonra 10 gün kutu üstünde kalan P2" grubu belirgin iyi çıktı (+12,6 / +19,0 puan). Bu grup gelecek bilgisiyle ayrıldığı için alınabilir değildi. Bu deneme onu alınabilir hale getirir. **Veri esinlidir:** 2023 ve 2024-26 ABD hücreleri bu gözlemin yapıldığı dönemdir, bağımsız sayılmaz.

## Kural (D1)

- P2 kırılım günü j'dir. Sonraki 10 işlem gününün HER kapanışı, j günündeki kutu tavanının (dünkü tavan, kir_pay tanımı) üstünde kalır.
- Sinyal günü = j+10, giriş = j+11 açılışı.
- Etiket aynıdır: +%20 / -%10 / 60 gün üçlü bariyer, maliyet ve kayma dahil.
- Taban aynıdır: aynı gün, aynı oynaklık ondalığı.
- Hissede 40 günde tek sinyal.

## Bağımsız sınama hücreleri (karar)

| Hücre | Dönem | Not |
|---|---|---|
| ABD 2016-22 | eğitim + doğrulama | gözlem bu dönemde yapılmadı |
| AVR 2016-26 | tamamı | ABD dışı, görülmemiş |

Tutma şartı (her hücre): n >= 30, fark >= +5 puan, ay kümeli %95 alt uç > 0, net fark > 0.

- İki hücre de tutarsa: 'D1 ADAY' (ileriye dönük izlemeye alınır).
- Tutmazsa: İZ DEĞİL.
- Bilgi olarak ABD 2023 ve 2024-26 (esin dönemi) ile BIST de yazılır.
