# K55 — GELECEK BİLGİSİ SIZINTISI TESTLERİ

Kural (ONKAYIT_K55 bölüm 10): hepsi geçmeden Faz 1'e geçilmez.

- **a_kesme_testi**: GEÇTİ — hucre_hata: {'D01-S01': 0}; sembol: ['ACIW', 'FLL', 'PCT']
- **a2_kesme_dedektor**: GEÇTİ — gelecek_degisken_hata: 6; not: hata > 0 beklenir (dedektör çalışıyor)
- **d_olay_etiketi**: GEÇTİ — sinanan_olay: 3
- **b_olumlu_kontrol**: GEÇTİ — n_olay: 109; d: 1.3425887565719261; auc: 0.8460427653518795
- **c_olumsuz_kontrol**: GEÇTİ — n_olay: 109; d: 0.06479123343404225; d_alt: -0.109840827383574; d_ust: 0.22322385382120805; auc: 0.5262112511264802
- **e_eslesme**: GEÇTİ — kontrol: 65; hata: 0; kullanilan_sutunlar: ['dd250', 'vol60', 'log_dv20', 'r60', 'ar20', 'vd', 'lt', 'trend', 'rejim', 'sektor']; eslesmeyen_pay: 0.94

- SONUÇ: HEPSİ GEÇTİ
