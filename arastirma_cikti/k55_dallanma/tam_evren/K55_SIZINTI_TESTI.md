# K55 — GELECEK BİLGİSİ SIZINTISI TESTLERİ

Kural (ONKAYIT_K55 bölüm 10): hepsi geçmeden Faz 1'e geçilmez.

- **a_kesme_testi**: GEÇTİ — hucre_hata: {'D01-S01': 0}; sembol: ['AAIC', 'FFIN', 'OSK']
- **a2_kesme_dedektor**: GEÇTİ — gelecek_degisken_hata: 6; not: hata > 0 beklenir (dedektör çalışıyor)
- **d_olay_etiketi**: GEÇTİ — sinanan_olay: 3
- **b_olumlu_kontrol**: GEÇTİ — n_olay: 7208; d: 1.1781491827224382; auc: 0.8253499783583633
- **c_olumsuz_kontrol**: GEÇTİ — n_olay: 7208; d: -0.0025930635512801036; d_alt: -0.02652873854871577; d_ust: 0.020331134087113702; auc: 0.49898736670813915
- **e_eslesme**: GEÇTİ — kontrol: 1200; hata: 0; kullanilan_sutunlar: ['dd250', 'vol60', 'log_dv20', 'r60', 'ar20', 'vd', 'lt', 'trend', 'rejim', 'sektor']; eslesmeyen_pay: 0.17

- SONUÇ: HEPSİ GEÇTİ
