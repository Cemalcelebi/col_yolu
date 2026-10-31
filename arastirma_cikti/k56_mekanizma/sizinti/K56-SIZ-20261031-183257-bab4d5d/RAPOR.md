# K56-SIZ İÇ → BAĞIMSIZ DOLAYLI ERİŞİM SINAMASI (K56-SIZ-20261031-183257-bab4d5d)

- commit bab4d5d; referans İÇ koşusu K56-IC-20261031-070828-d1922e5.

- T0 yeniden üretim: {'evren_surum': '0d00d2c976083737da1a60b71e9360ca543c2add2bb31c8db94136e5f4793524', 'panel_satir': 4909423, 'panel_satir_kilitli': 4909423, 'panel_esit': True, 'panel_sutun_farki': [], 'olay': 22502, 'olay_kilitli': 22502, 'olay_esit': True}
- T1b bileşim farkı (beklenen, v1.3-G: başvuru geçmişi sec_var kesik özetten; A3 açıklayıcı, karar vermez): 144 hücre; karar değişen satır ['Y120|once_8k_202']
- T1b (kesik fiyat + kesik başvuru özeti) vs İÇ: {'S': {'satir_ref': 125, 'satir_yeni': 125, 'fark_hucre': 0}, 'H': {'satir_ref': 25, 'satir_yeni': 25, 'fark_hucre': 0}, 'B3': {'satir_ref': 64, 'satir_yeni': 64, 'fark_hucre': 0}, 'Bl': {'satir_ref': 24, 'satir_yeni': 24, 'fark_hucre': 144}, 'birebir': {'S': True, 'H': True, 'B3': True, 'Bl': False}}
- T1a bileşim (tam başvuru özeti) vs İÇ: {'Bl': {'satir_ref': 24, 'satir_yeni': 24, 'fark_hucre': 0}, 'birebir': {'Bl': True}}
- T1 ayrışma (İÇ) vs AYR koşusu: {'S': {'satir_ref': 125, 'satir_yeni': 125, 'fark_hucre': 0}, 'birebir': {'S': True}, 'kimlik_ozdeslik': {'tutar': True, 'bozulan': 0, 'en_buyuk_mutlak': 2.220446049250313e-16}, 'en_buyuk_sayisal_fark': 1.1102230246251565e-16}
- T1 PBO / DSR vs PBO koşusu: yapı {'B3': {'satir_ref': 64, 'satir_yeni': 64, 'fark_hucre': 0}, 'birebir': {'B3': True}}, sonuç {'Bl': {'satir_ref': 2, 'satir_yeni': 2, 'fark_hucre': 0}, 'birebir': {'Bl': True}}
- T2a (kesik evren) vs T1b: {'S': {'satir_ref': 125, 'satir_yeni': 125, 'fark_hucre': 264}, 'H': {'satir_ref': 25, 'satir_yeni': 25, 'fark_hucre': 0}, 'B3': {'satir_ref': 64, 'satir_yeni': 64, 'fark_hucre': 88}, 'Bl': {'satir_ref': 24, 'satir_yeni': 24, 'fark_hucre': 0}, 'birebir': {'S': False, 'H': True, 'B3': False, 'Bl': True}, 'en_buyuk_d_farki': 0.0014530591053258934, 'sinif_degisimi': 0, 'yari_genislik_25_asan': 0, 'ihmal_edilebilir': True}
- T2b (kesik evren + kesim sonrası giren K34 dışarıda) vs T1b: {'S': {'satir_ref': 125, 'satir_yeni': 125, 'fark_hucre': 283}, 'H': {'satir_ref': 25, 'satir_yeni': 25, 'fark_hucre': 0}, 'B3': {'satir_ref': 64, 'satir_yeni': 64, 'fark_hucre': 90}, 'Bl': {'satir_ref': 24, 'satir_yeni': 24, 'fark_hucre': 0}, 'birebir': {'S': False, 'H': True, 'B3': False, 'Bl': True}, 'en_buyuk_d_farki': 0.010399975822467655, 'sinif_degisimi': 0, 'yari_genislik_25_asan': 0, 'ihmal_edilebilir': True}

## Karar: İÇ hesaplarında 2023-12-31 sonrası bilgiye dolaylı erişim YOK (T0 yeniden üretim + T1b S / H / B3 + T1a bileşim + ayrışma İÇ + PBO birebir; ayrışma v1.3-c toleransıyla)

Görünmeyen sınırlamalar (T1 / T2 ölçemez; beyan): hayatta kalma (evren 2026'da işlem görenler + K34), 2026 sürümü bölünme / temettü düzeltmesi, güncel sektör / CIK etiketleri; BAĞIMSIZ dönem K51-K54 programında test dönemi olarak kullanıldı.
