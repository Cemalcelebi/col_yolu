# K55 — GELECEK BİLGİSİ SIZINTISI TESTLERİ

Kural (ONKAYIT_K55 bölüm 10): hepsi geçmeden Faz 1'e geçilmez.

- **a_kesme_testi**: GEÇTİ — hucre_hata: {'D01-S01': 0}; sembol: ['AAIC', 'FFIN', 'OSK']
- **a2_kesme_dedektor**: GEÇTİ — gelecek_degisken_hata: 6; not: hata > 0 beklenir (dedektör çalışıyor)
- **d_olay_etiketi**: GEÇTİ — sinanan_olay: 3
- **b_olumlu_kontrol**: GEÇTİ — n_olay: 7956; d: 1.1876935942821727; auc: 0.8274617505083
- **c_olumsuz_kontrol**: GEÇTİ — n_olay: 7956; d: -0.0009791774780770377; d_alt: -0.02482927119507203; d_ust: 0.021257669920268056; auc: 0.49962508301608166
- **e_eslesme**: GEÇTİ — kontrol: 1283; hata: 0; kullanilan_sutunlar: ['dd250', 'vol60', 'log_dv20', 'r60', 'ar20', 'vd', 'lt', 'trend', 'rejim', 'sektor']; eslesmeyen_pay: 0.10666666666666667

- SONUÇ: HEPSİ GEÇTİ
