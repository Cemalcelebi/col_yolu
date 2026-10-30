# K55 — GELECEK BİLGİSİ SIZINTISI TESTLERİ

Kural (ONKAYIT_K55 bölüm 10): hepsi geçmeden Faz 1'e geçilmez.

- **a_kesme_testi**: GEÇTİ — hucre_hata: {'D01-S01': 0}; sembol: ['ACIW', 'FLL', 'PCT']
- **a2_kesme_dedektor**: GEÇTİ — gelecek_degisken_hata: 6; not: hata > 0 beklenir (dedektör çalışıyor)
- **d_olay_etiketi**: GEÇTİ — sinanan_olay: 3
- **b_olumlu_kontrol**: GEÇTİ — n_olay: 94; d: 1.369353486034227; auc: 0.8533674769053634
- **c_olumsuz_kontrol**: GEÇTİ — n_olay: 94; d: 0.056083835904475694; d_alt: -0.15131681817671555; d_ust: 0.24276012882473103; auc: 0.5244148414173261
- **e_eslesme**: GEÇTİ — kontrol: 43; hata: 0; kullanilan_sutunlar: ['dd250', 'vol60', 'log_dv20', 'r60', 'ar20', 'vd', 'lt', 'trend', 'rejim', 'sektor']; eslesmeyen_pay: 0.9633333333333334

- SONUÇ: HEPSİ GEÇTİ
