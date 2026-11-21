# CETVEL2 yeniden koşu: bağımsız denetim (21 Kasım 2026)

Denetçi kendi kodunu yazdı (düz pandas / düz döngü); rapordaki sayılara güvenmedi. Satır dosyaları, ham V_ABD.pkl ve yeniden_kosu.json'dan sayıldı.

## (a) Sıra: TUTTU
- Commit sırası (UTC, 21 Kas): 3471f1c kod 09:13 -> 62c16c9 ön kayıt v2.0 09:14 -> 6f9eabc kod v2.1 09:31 -> a533c9b ön kayıt v2.1 09:33 -> 2d5e027 pozitif kontrol v2.1 09:46 -> 77a8503 yeniden koşu ön kaydı 10:04 -> 9d2d87b koşu 10:50 -> 860d975 yalnız gösterim 10:51.
- `git diff a533c9b HEAD` (CETVEL2_ON_KAYIT_v2.1.md, esik / guc / prefix v2.1, CETVEL2.py, test_cetvel2.py): fark yok. `git diff 77a8503 HEAD` (YENIDEN_KOSU_ON_KAYIT.md, c2_yeniden_kosu.py, yk_huni.json): fark yok. v2.0 ön kayıt dosyaları 62c16c9'dan beri değişmedi. CETVEL2.py son değişim 6f9eabc (v2.1 ön kaydından ÖNCE; ön kayıt kodu sha ile eşit).
- v2.1 eşik / güç dosyaları v2.0'dan yalnız 'surum' alanında farklı (kova sınırları ve güç eğrisi içeriği birebir aynı).
- yeniden_kosu.json parça kapıları: git_onkayit 77a8503, c2_git_onkayit a533c9b, kontrol True.
- 860d975 yalnız YENIDEN_KOSU.md'de 1 satır (kontrol listesi K1 sayım gösterimi).

## (b) Yasak dosyalar: TUTTU
- 4505d5c..HEAD: IZ_KARNE.py ve IZ_DEFTERI.md yalnız 5db2f83 (ana model); CLAUDE.md yalnız 0f22f28 ve f370698 (ana model); COL_OZET.md, YAPI_HEDEF.py, DUSUS_SONRASI.py, ORTAK_CETVEL.py değişmedi.
- POZITIF_KONTROL.py bu aralıkta YENİ dosya (+1189 satır, silme yok), yalnız Ç203 pozitif kontrol işinin kendi commit'leri 3b614aa ve 3092fc7'de; CETVEL2 / KASA / bölge commit'leri dokunmadı (CETVEL2_IS_TANIMI.md "POZITIF_KONTROL.py değiştirilmez"; sonraki commit'lerde değişmedi).
- `git status`: çalışma ağacı temiz.

## (c) Yeniden üretim, hücre: TUTTU (7 / 7 istenen hücre; ek olarak 735 / 735)
n = bayrak == 1 ve fark_<kod> dolu satırlar; ort FARK ve ort SIRA düz pandas. json ile en büyük fark < 1e-15, n birebir aynı.

| Ç | kod | pazar x dönem | n | ort FARK | ort SIRA |
|---|---|---|---|---|---|
| C201 | Y13 | ABD sınama | 606 | -0,00255113 | 0,489650 |
| C196 | A_S7 (tek süzgeç) | ABD eğitim | 4885 | -0,00019765 | 0,499464 |
| C196 | G2 (dip grubu) | AVR sınama | 72 | +0,00663240 | 0,520999 |
| C202 | DS28 | ABD sınama | 1791 | +0,01205199 | 0,503033 |
| C202 | DS06 | ABD sınama | 238 | +0,00212657 | 0,515647 |
| C197 | P_C_ust20 | AVR sınama | 461 | +0,00794335 | 0,531400 |
| C198 | D1_W1_A | ABD sınama | 1300 | +0,00508610 | 0,523043 |

Geniş tarama: C194-C202 satır dosyalarındaki 744 dolu (kod x pazar x dönem) hücrenin tamamı (735 hücre; kalan 9'da json fark = None) n, FARK, SIRA için < 1e-6 ile eşit; uyuşmazlık 0.

## (d) Ham veriden R15: TUTTU (20 / 20)
V_ABD.pkl (sembol -> DataFrame Open / High / Low / Close / Volume). C201 satırlarından rastgele 20 olay (random_state 11): geçerli bar H > L ve V > 0, giriş gününden itibaren 1. geçerli bar açılışı = E0, 15. geçerli bar kapanışı / E0 - 1. R15 ve E0 satır dosyasıyla 20 / 20 aynı (fark < 1e-6; örnekler: ALKS +0,142132, BBIO -0,102473, SIRI -0,196334).

## (e) Pozitif kontrol B: TUTTU
c2_b_olay_v2.1.csv.gz'den satır dosyasıyla: momentum alt on (B1A, F_A == 1, kod B1) ABD eğitim n 6315, ort FARK +0,001196 (+0,12 puan), SIRA 0,49602; PEAD üst (B2U, F_U == 1, kod B2) ABD eğitim n 2199, FARK +0,008959 (+0,90 puan), SIRA 0,52005; ek: B1U ABD sınama n 4749, FARK +0,009637. Üçü de cetvel2_pozitif_kontrol_v2.1.json ile birebir eşit.

## (f) Sayım: TUTTU (52 doğru)
- 124 hipotez (C194-C202; TABAN / TABAN_DS / TUR hariç). Dağılım: C194 3, C195 3, C196 22, C197 4, C198 36, C199 20, C200 8, C201 3, C202 25.
- Dört karar hücresinin (ABD / AVR x eğitim / sınama) hepsinde güç >= 0,80 VE TUTAR hücre 0 VE ters hücre 0: **52**. Ç dağılımı: C196 9, C197 3, C198 16, C199 8, C200 3, C201 2, C202 11 (C194 ve C195 0). Kod listesi: /tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad/f_liste.txt ve aşağıda.
- En az bir karar hücresinde güç < 0,80 (güç None = n < 30 olan 7 hücre dahil): **63**.
- Güçlü ama en az bir TUTAR / ters hücresi olan: **9** (Y10c, P_C_ust20, D1_W1_A, D1_W3t_A, D3_W1_A, DS08, DS16, DS21, DS28). 52 + 63 + 9 = 124.
- Hücre bazında sınırda olanlar var (C196 G2 ABD güç 0,79986 ve 0,79996: eşiğin hemen altı); kod bazında (dört hücrenin en küçüğü) 0,79-0,80 aralığında kod yok.
- Toplam TUTAR hücre 15 (BİLGİ pazarı dahil), karar hücrelerinde 6; ters 3.

52 kod: C196: A_F14 A_S2 A_S3 A_S4 A_S5 A_S6 A_S7 A_S8 G1 | C197: P_AB_alt20 P_AB_ust20 P_C_alt20 | C198: D1_E1_A D1_E1t_A D1_E2_A D1_E2t_A D1_W1t_A D1_W2D_A D1_W2Dt_A D1_W2_A D1_W2t_A D1_W3_A D1_W4_A D1_W4t_A D1_W5a_A D1_W5b_A D1_W6_A D1_W6t_A | C199: D2_AYK_A D2_AY_A D2_DT_A D2_NR7_A D2_PP_A D2_W1_A D2_W2D_A D2_W2_A | C200: D3_AYK_A D3_NR7_A D3_W2D_A | C201: Y13 Y13c | C202: DS01 DS03 DS05 DS09 DS10 DS11 DS17 DS18 DS20 DS23 DS25.

Not: C196 G2 (dip grubu) bu listede değil (AVR güç 0,39 / 0,38; ABD güç 0,80 sınırında altında: 0,79986 ve 0,79996), yani ÖLÇÜLEMEDİ.

## (g) E-posta / anahtar taraması: TUTTU
CETVEL2.py, test_cetvel2.py, arastirma_cikti/cetvel2/ (gmail, @, AIza, sk-, Bearer; .gz dahil): gerçek e-posta / anahtar yok. İsabetler: c2_yeniden_kosu.py 141. satırdaki e-posta TARAYICI regex'i (kapı kodu) ve `noreply@anthropic.com` (atıf satırı); CETVEL2_IS_TANIMI.md'de atıf satırı örneği; c2_b_olay.csv.gz'de 'MAERSK-B' (yanlış pozitif, 'SK-B').

## (h) HATA
Sayı uyuşmazlığı yok. Gözlemler (hata değil, deftere düşülecek not):
1. Atıf satırları tutarsız: ca5d2a8 / 77a8503 / 9d2d87b / 860d975 / d6fb114 / 0f22f28 / f370698 / 5db2f83 'Fable 5.1'; 3471f1c, 62c16c9, 6f9eabc, 0fc7c95, a533c9b, 2d5e027, e3ae6d6 'Opus 5.5'; c1abf63 'Fable 5.2' (süreç, K13).
2. 7 hücrede güç = None (n < 30); (f) sayımında güç < 0,80 sayıldı, rapordaki 52 ile uyumlu.
3. test_cetvel2.py ortamda koşulmadı (pytest yok); bu denetimin kapsamı sayı yeniden üretimidir.
