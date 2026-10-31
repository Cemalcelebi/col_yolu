# GEÇERSİZ KOŞU (karar vermez) — K56-SIZ-20261031-152744-255ae9d

Koşu T2a aşamasında durduruldu (31 Ekim 2026, 16:50 UTC). Sonuç dosyası K56_KOSU_SIZ.json yok.

Bulunanlar (bilgi):
- T0 yeniden üretim: panel ve olay tablosu birebir.
- T1b (kesik fiyat + kesik SEC özeti) S / H / B3: İÇ koşusuyla birebir (tolerans 0).
- T1b bileşim (A3, açıklayıcı): beklenen fark (v1.3-G) — başvuru geçmişi sec_var kesik özetten; Y60 2731 → 2711, Y120 910 → 906, Y250 238 → 237 olay;
  bir satırın kararı değişti (Y120 once_8k_202: "fark yok" → "G1 > G7"). İÇ A3 bileşim tablosu tam SEC özetiyle hesaplanmıştı; bu tablo karar vermez.
- T1a bileşim (tam SEC özeti): birebir.
- T1 PBO / DSR (KEŞİF + İÇ): birebir (0 fark).
- T1 ayrışma (İÇ): 4.609 hücre farkı — TEST HATASI: karşılaştırma koşusu bootstrap tohumunu "T1" etiketiyle üretti, AYR koşusu "gercek" etiketiyle
  (tohum metni etiketi içerir). Nokta değerleri (E1, E2, G, n, bantlar, L) birebir; farklar yalnız güven aralıklarında (tohum) ve bir satırda kimlik_fark
  (1,94e-16, cebirsel özdeşlik kalıntısı; son bit).

Düzeltme (ön kayıt v1.3-c): ayrışma etiketi tek sabit (ayrisma.ETIKET_GERCEK); kimlik_fark özdeşlik olarak (iki tarafta |.| <= 1e-9), öteki sayısal
sütunlar 1e-12 içinde, sınıf / metin birebir. Kod değiştiği için sızıntı, ayrışma ve PBO / DSR yeniden koşulur (kilit şartı).
