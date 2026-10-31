# GEÇERSİZ KOŞU (karar vermez) — K56-SIZ-20261031-164553-efe0f88

Koşu T1 PBO aşamasında durduruldu (31 Ekim 2026, 17:20 UTC). Sonuç dosyası K56_KOSU_SIZ.json yok.

- T0 birebir; T1b S / H / B3 birebir; T1b bileşim farkı beklenen türden (önceki koşuyla aynı 144 hücre); T1a bileşim birebir.
- T1 ayrışma: bütün sayısal sütunlar birebir (tohum düzeltmesi işledi), ama AYR çıktısındaki yapay karar sütunları (karar, sent_siniflar, sent_cogunluk,
  G_sent_ort) karşılaştırma tarafında hesaplanmadığı için 4 "tek tarafta sütun" farkı — TEST HATASI.
- Düzeltme (ön kayıt v1.3-c ek): satır kararı tek fonksiyonda (surucu._ayr_satir_karar), sızıntı T1 kararı kesik veride yeniden hesaplar ve bütün
  sütunları karşılaştırır. Yerel sınama: AYR dosyalarından kurulan tablo birebir, karar değişikliği yakalanıyor.
