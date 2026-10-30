# K55 — FAZ 0 RAPORU (K55-20261030-123258-7ce1627)

- Kod K55 v0.2 (2026-10-30, Faz 0 + ön kayıt v1.2: purge = ufuk, embargo, güçlü koşu kimliği, çıktı yolu denetimi, blok bootstrap, FDR ailesi); commit 7ce1627; kilit sha 87bf7f6c0777; ayar sha 1f994b8d8ea9; kod dosyası sha 18 adet, veri dosyası sha 8 adet (K55_KOSU.json); evren sürümü 0d00d2c97608; örnek: 50; veri paketleri: {}.
- Faz 0 amacı altyapıyı kanıtlamaktır; hücre sonuçları iskele denetimidir, iz iddiası değildir (optimize edilmedi).

## Cemal'in 7 sorusu

1. Kaç hisse eksiksiz işlendi? 46 / 50 (eksiksiz = ≥ 260 gün, boşluksuz, sıfır hacim payı ≤ %20, OHLC hatasız, yinelenen tarih yok; sert hareket bayrağı bilgi, eksiksizliğe girmez).
2. Kaç hissede tarihsel veri eksik? 4 (boşluklu 0, kısa seri 0, sıfır hacim yüksek 4); yükleyici dışı kısa geçmişli (< 320 gün, VERİ YETERSİZ, K55_EVREN_DISI_KISA.csv) 60; özellik için yeterli (≥ 320 gün) 50; sert hareketli (bilgi, bölünme değil) 15, aşırı getirili 12, OHLC hatalı 0.
3. Kaç sembol şirketle güvenilir eşleştirildi? CIK eşleşen 50 / 50; sektör bilinen 49; K54 sınıfı olmayan (doğrulanamayan) semboller evren dışı.
3b. Evren dışı kalanlar (kategori ayrı; K55_EVREN_DISI.csv): {'kisa_seri_yukleyici': 60, 'fon_evren_disi': 7, 'eslesme_yok_cik': 1}. V / EV çift yönlü tutarlılık: {'ev_serisiz': [], 'v_fazla': [], 'bos_seri': [], 'kesim_sonrasi_satir': [], 'gecti': True}.
4. Delist olmuş şirketler nasıl ele alındı? Seri erken biten 12; sınıf dağılımı {1: 38, 2: 4, 3: 4, 4: 2, 5: 2}; seri sonu işlemi {'k51': 40, 'd100': 4, 'd0': 4, 'kes': 2} (d100 = iflas −%100, d0 = birleşme bedeli, k51 = son kapanış ve negatifse −%30); 4b kod yeniden kullanımı kesimi uygulandı; sınıf 6 dışarıda; olay tanımında tam pencere şartı (seri sonunu aşan pencere tanımsız).
5. Gelecek bilgisi sızıntısı testleri geçti mi? EVET — a_kesme_testi: geçti; a2_kesme_dedektor: geçti; d_olay_etiketi: geçti; b_olumlu_kontrol: geçti; c_olumsuz_kontrol: geçti; e_eslesme: geçti.
6. Denemede bütün modüller doğru çalıştı mı? EVET — evren: 50 sembol; dışlama {'kisa_seri_yukleyici': 60, 'fon_evren_disi': 7, 'eslesme_yok_cik': 1}; 4b kesim 9; V/EV tutarlılık geçti; veri_kalitesi: eksiksiz 46 / 50; panel: 67098 satır, 45948 likit; olaylar: 352 olay, tekillik geçti; sizinti: hepsi geçti; hucre_motoru: 3 satır (A / B / C), hata yok.
7. Tam evren koşusunun tahmini süresi ve kaynağı: {'sembol': 3260, 'panel_satir_tahmini': 4374789, 'bellek_GB_tahmini': 0.52, 'panel_sn': 98.0, 'olaylar_sn': 0.0, 'sizinti_sn': 26.0, 'hucre_basina_sn_tahmini': 59.0, 'isci': 4, 'not': 'Faz 1 = 80 OHLCV hücresi × (5 pencere) × 3 yöntem; bootstrap 2.000'}.

## Süreler (sn)

- veri_sha: 2.2
- evren: 12.7
- kalite: 0.7
- panel: 1.5
- olaylar: 0.0
- sizinti: 0.4
- hucre_iskele: 0.9

## Panel

- sure_sn: 1.5
- sembol: 50
- satir: 67098
- likit_satir: 45948
- r60_tanimli_likit: 44150
- donem_t0: {'BAGIMSIZ': 16708, 'KESIF': 16304, 'IC_DOGRULAMA': 11170, 'DISI': 1766}
- donem60_purge_embargo: {'KESIF': 15342, 'BAGIMSIZ': 14691, 'IC_DOGRULAMA': 9547, 'PURGE': 4042, 'DISI': 1766, 'EMBARGO': 395, 'TANIMSIZ': 165}
- donem250_purge_embargo: {'KESIF': 12849, 'PURGE': 10938, 'BAGIMSIZ': 9212, 'TANIMSIZ': 5919, 'IC_DOGRULAMA': 4869, 'DISI': 1766, 'EMBARGO': 395}
- ozelliksiz_satir_toplam: 13000
- atlanan: 0

## 4b kod yeniden kullanımı kesimi (kesim öncesi / sonrası satır; kesim günü işlem günü mü)

| sembol | kesim | kesim_islem_gunu | etkin_kesim | once | sonra | atilan |
|---|---|---|---|---|---|---|
| ARIS | 2025-12-09 | True | 2025-12-09 | 2830 | 2649 | 181 |
| UNIT | 2025-11-28 | True | 2025-11-28 | 2830 | 2642 | 188 |
| AXP | 2022-02-25 | True | 2022-02-25 | 1485 | 354 | 1131 |
| BG | 2024-02-23 | True | 2024-02-23 | 1485 | 854 | 631 |
| KNDI | 2024-07-12 | True | 2024-07-12 | 1485 | 950 | 535 |
| ZYME | 2022-12-02 | True | 2022-12-02 | 1485 | 548 | 937 |
| NE | 2022-12-07 | True | 2022-12-07 | 1313 | 379 | 934 |
| LOGC | 2025-09-06 | False | 2025-09-05 | 1421 | 1185 | 236 |
| HCIC | 2023-03-09 | False | 2022-12-21 | 561 | 454 | 107 |

## Deneme örneklemi dağılımı (tabaka = kaynak × sınıf × likidite üçlüsü; eksik tabaka gizlenmez)

| tabaka | kota | aday | secilen | eksik | toplam_secilen | istenen | evren |
|---|---|---|---|---|---|---|---|
| V_ABD sınıf 1 lik 0 | 10 | 7 | 7 | 3 | 50 | 50 | 3260 |
| V_ABD sınıf 1 lik 1 | 10 | 455 | 10 | 0 | 50 | 50 | 3260 |
| V_ABD sınıf 1 lik 2 | 10 | 946 | 10 | 0 | 50 | 50 | 3260 |
| K34_yahoo sınıf 1 | 8 | 1428 | 8 | 0 | 50 | 50 | 3260 |
| K34_tiingo sınıf 2 | 4 | 19 | 4 | 0 | 50 | 50 | 3260 |
| K34_tiingo sınıf 3 | 4 | 159 | 4 | 0 | 50 | 50 | 3260 |
| K34_tiingo sınıf 5 | 2 | 79 | 2 | 0 | 50 | 50 | 3260 |
| K34_tiingo sınıf 4 | 2 | 7 | 2 | 0 | 50 | 50 | 3260 |
| tamamlama (eksik tabakalar yerine, tekrarsız) | 3 | 3213 | 3 | 0 | 50 | 50 | 3260 |

## Olay tekilliği ve dönem (purge / embargo) dağılımı

- {'yineleme': 0, 'ortusme': 0, 'olay': 352, 'gecti': True}
- olay × ufuk × dönem: {('Y120', 'BAGIMSIZ'): 33, ('Y120', 'EMBARGO'): 1, ('Y120', 'IC_DOGRULAMA'): 17, ('Y120', 'KESIF'): 36, ('Y120', 'PURGE'): 10, ('Y250', 'BAGIMSIZ'): 12, ('Y250', 'IC_DOGRULAMA'): 4, ('Y250', 'KESIF'): 16, ('Y250', 'PURGE'): 7, ('Y60', 'BAGIMSIZ'): 75, ('Y60', 'IC_DOGRULAMA'): 52, ('Y60', 'KESIF'): 69, ('Y60', 'PURGE'): 20}

## Çoklu test yükü (aile = dal × yöntem × dönem; hücre içi Holm, aile içinde BH q = 0,10)

| dal | yontem | donem | hucre | varyant | test | ret |
|---|---|---|---|---|---|---|
| D01 | A | KESIF | 1 | 1 | 1 | 0 |
| D01 | B | KESIF | 1 | 1 | 1 | 0 |

## Hücre iskelesi (D01-S01 + olumlu / olumsuz kontrol; yalnız pipeline denetimi)

| hucre | yontem | donem | ufuk | n_olay | n | n_degisim | d | d_alt | d_ust | d_alt_blok | d_ust_blok | auc | fark | fark_alt | fark_alt_blok | fark_alt_hisse_ceyrek | net_fark | slot_rastgele_yuzdelik | lift | eksik_pay | karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01-S01 | A | KESIF | Y60 | 69 |  |  | -0.006 | -0.211 | +0.203 | -0.176 | +0.156 | +0.493 |  |  |  |  |  |  |  | +0.000 | ETKİ YOK |
| D01-S01 | C | KESIF | Y60 |  |  | 2102 |  |  |  |  |  |  |  |  |  |  |  |  | +0.851 | +0.000 | ETKİ YOK |
| D01-S01 | B | KESIF |  |  | 2 |  |  |  |  |  |  |  | -0.385 | -0.531 | -0.531 | -0.531 | -0.385 | +0.000 |  | +0.000 | VERİ YETERSİZ |

## Çıktılar

- K55_VERI_KALITESI.csv, K55_VERI_KAPSAMI.md, K55_EVREN.csv, K55_EVREN_DISI.csv (kategori ayrı), K55_KESIM.csv, K55_K54_TUTARLILIK.csv, K55_ORNEKLEM.csv, K55_OLAYLAR.csv.gz, K55_SIZINTI_TESTI.md, K55_HUCRE_ISKELE.csv, K55_COKLU_TEST.csv, K55_KOSU.json (kod / veri / ayar sha), panel/ pickle (repoya girmez).
