# K51 — TEKRAR ÜRETİM (v1.2)

- Kod: COL_YOLU_ABD.py CY v1.2 (2026-10-29, K51 sonrası bağımsız denetim: veri bütünlüğü, kırılganlık, eşleşmiş kontrollerle H-A..H-E; v1.1 K51 ABD Çöl Yolu: üçlü bariyer (sabit + oynaklık), meta-etiketleme, model merdiveni LR/GBM/CNN/LSTM, PBO/DSR, batanlar dahil); git commit 228bf5c; ön kayıt commit 8e99902; eski kod kıyası b3835d8.
- Veri sürümü: islenmis-veri dalı (V_ABD.pkl, k34_yahoo.pkl), k34_evren.csv (main), Tiingo CSV 449 dosya (lisans gereği repoda yok), endeks.pkl (yfinance SPY/IWM/^STOXX/XU100).
- Veri sha256 (ilk 16): V_ABD.pkl=82871d2c7c28ca93, k34_yahoo.pkl=eab8e2147cd13ecc, k34_evren.csv=e138026a00492c25, endeks.pkl=7c0dba41ee59d9bf
- Parametreler: CY (K51 ile aynı) + CY_V12 = {"tohum": 512, "boot": 2000, "k": 5, "k_es": 3, "dd_tol": 0.1, "gun_tol": 10, "fark_esik": 0.05, "n_min": 30, "uzak": ["dd250", "vol60", "log_dv20", "r60", "ar20"], "delist_senaryo": [-0.3, 0.0, -1.0], "eski_commit": "b3835d8", "kes_gun": 120, "donem": [["2016-22", "2016-01-01", "2022-12-31"], ["2023", "2023-01-01", "2023-12-31"], ["2024-26", "2024-01-01", "2026-06-05"]], "yillar": [[2023, "2023-01-01", "2023-12-31"], [2024, "2024-01-01", "2024-12-31"], [2025, "2025-01-01", "2025-12-31"], [2026, "2026-01-01", "2026-06-05"]], "batma_r60": -0.5, "batma_fiyat": 1.0, "ileri_dogrulama": "2026-09-01"}
- Rastgelelik: tohum 512 (eşleştirme sırası ve bootstrap), bootstrap 2000; eşleştirme deterministik (stable argsort).
- Örneklem: panel 3175671 likit hisse-gün, 2752 hisse; eşleşmiş kontrol satırı 21708; süre 10.6 dk.
- Adımlar: (1) `exec(open('.../COL_YOLU_ABD.py').read()); R = cy_v12_calistir()` (veri klasörü CY_VERI; Tiingo CSV'leri CY_TIINGO ya da veri/tiingo); (2) çıktılar CY_CIKTI altına yazılır; (3) `python test_col_yolu_abd.py` 17/17.
- Çıktı özetleri (sha256 ilk 16): K51_VERI_DENETIMI.md=8e795b7fe8e1252b, K51_KIRILGANLIK.md=ba5915fb23bd772c, K51_ESLESMIS_KONTROL.csv.gz=7cbc71d3013125da, K51_HIPOTEZ_KARARLARI.csv=e644c9a9d2b7ec02, K51_EVREN_PIT.csv=ecca4f6d810c4fa2
- Holm (aile = 5 hipotez, 2023-26 tek yönlü bootstrap p): {"H-A": 0.0275, "H-E": 0.098, "H-C": 0.098, "H-B": 0.5737, "H-D": 0.6272}

