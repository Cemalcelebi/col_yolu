# K55 — GELECEK BİLGİSİ SIZINTISI TESTLERİ

Kural (ONKAYIT_K55 bölüm 10): hepsi geçmeden Faz 1'e geçilmez.

- **a_kesme_testi**: GEÇTİ — hucre_hata: {'D01-S01': 0}; sembol: ['AEHL', 'GDC', 'ONB']
- **a2_kesme_dedektor**: GEÇTİ — gelecek_degisken_hata: 6; not: hata > 0 beklenir (dedektör çalışıyor)
- **d_olay_etiketi**: GEÇTİ — sinanan_olay: 3
- **b_olumlu_kontrol**: GEÇTİ — n_olay: 121; d: 1.16919393717593; auc: 0.8228242386870822
- **c_olumsuz_kontrol**: GEÇTİ — n_olay: 121; d: -0.08244828740194876; d_alt: -0.27905030083323723; d_ust: 0.09157998798600293; auc: 0.48603036175710596
- **e_eslesme**: GEÇTİ — kontrol: 57; hata: 0; kullanilan_sutunlar: ['dd250', 'vol60', 'log_dv20', 'r60', 'ar20', 'vd', 'lt', 'trend', 'rejim', 'sektor']; eslesmeyen_pay: 0.9466666666666667

- SONUÇ: HEPSİ GEÇTİ
