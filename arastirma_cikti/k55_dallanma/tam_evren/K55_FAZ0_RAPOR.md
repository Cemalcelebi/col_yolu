# K55 — FAZ 0 RAPORU (K55-20261030-131453-8e47761)

- Kod K55 v0.2 (2026-10-30, Faz 0 + ön kayıt v1.2: purge = ufuk, embargo, güçlü koşu kimliği, çıktı yolu denetimi, blok bootstrap, FDR ailesi); commit 8e47761; kilit sha 87bf7f6c0777; ayar sha 1f994b8d8ea9; kod dosyası sha 18 adet, veri dosyası sha 8 adet (K55_KOSU.json); evren sürümü 0d00d2c97608; örnek: tam evren; veri paketleri: {}.
- Faz 0 amacı altyapıyı kanıtlamaktır; hücre sonuçları iskele denetimidir, iz iddiası değildir (optimize edilmedi).

## Cemal'in 7 sorusu

1. Kaç hisse eksiksiz işlendi? Veri hatası ve veri yetersizliği olmayan (kullanılabilir) 3012 / 3260. Veri hatalı 9 (sırasız 0, yinelenen işlem günü 0, takvim dışı satır 0, NaN fiyat 0, sıfır / negatif fiyat 0, negatif hacim 0, OHLC ilişki 2 / 7 / 0); veri yetersiz 242; olağan piyasa davranışı (bilgi, hata değil) 1067; şüpheli sıçrama 499 (muhtemel bölünme 352, açıklanamayan 317; kurumsal işlem verisi YOK, kesin sınıflandırma yapılmadı).
2. Kaç hissede tarihsel veri eksik? Fiyat yok 0, boş seri 0, kısa seri (< 320) 0, ciddi boşluklu (> 5 işlem günü) 86 (boşluklu 162, eksik işlem günü toplam 18007, en uzun 849; ABD işlem takvimi, tatiller eksik sayılmaz), eksik hacim payı yüksek 0, sıfır hacim payı yüksek 179; K54 kesilmiş seri 9; yükleyici dışı kısa geçmişli 60 (K55_EVREN_DISI.csv); özellik penceresi yeterli 3260, sonuç penceresi yeterli Y60 3260 / Y120 3235 / Y250 3129; olay penceresi eksik 0; dönem kapsamı {'KESIF': 2978, 'IC_DOGRULAMA': 3143, 'BAGIMSIZ': 3126}.
3. Kaç sembol şirketle güvenilir eşleştirildi? CIK geçerli 3259 / 3260 (boş 1, geçersiz 0, bir CIK'ye birden fazla sembol 8, sembol yeniden kullanımı (4b) 9); şirket adı boş 1; sektör bilinen 3098 (boş / NaN 162); seri_erken geçersiz 0; EV yinelenen 0; V'de fazla 0.
3b. Evren dışı kalanlar (kategori ayrı; K55_EVREN_DISI.csv): {'kisa_seri_yukleyici': 60, 'fon_evren_disi': 7, 'eslesme_yok_cik': 1}. V / EV çift yönlü tutarlılık: {'ev_serisiz': [], 'v_fazla': [], 'bos_seri': [], 'kesim_sonrasi_satir': [], 'gecti': True}.
4. Delist olmuş şirketler nasıl ele alındı? Seri erken biten 266; sınıf dağılımı {1: 2994, 2: 19, 3: 159, 4: 9, 5: 79} (4a 0, 4b 9); seri sonu işlemi (d100 = iflas −%100, d0 = birleşme bedeli, k51 = son kapanış ve negatifse −%30); 4b kod yeniden kullanımı kesimi uygulandı; sınıf 6 dışarıda; olay tanımında tam pencere şartı (seri sonunu aşan pencere tanımsız).
5. Gelecek bilgisi sızıntısı testleri geçti mi? EVET — a_kesme_testi: geçti; a2_kesme_dedektor: geçti; d_olay_etiketi: geçti; b_olumlu_kontrol: geçti; c_olumsuz_kontrol: geçti; e_eslesme: geçti.
6. Denemede bütün modüller doğru çalıştı mı? EVET — evren: 3260 sembol; dışlama {'kisa_seri_yukleyici': 60, 'fon_evren_disi': 7, 'eslesme_yok_cik': 1}; 4b kesim 9; V/EV tutarlılık geçti; panel: 4909423 satır, 3291650 likit; olaylar: 22502 olay, tekillik geçti; veri_kalitesi: kullanılabilir 3012 / 3260; veri hatalı 9; veri yetersiz 242; sizinti: hepsi geçti; hucre_motoru: 3 satır (A / B / C), hata yok.
7. Tam evren koşusunun tahmini süresi ve kaynağı: {'sembol': 3260, 'panel_satir_tahmini': 4909423, 'bellek_GB_tahmini': 0.59, 'panel_sn': 59.0, 'olaylar_sn': 4.0, 'sizinti_sn': 46.0, 'hucre_basina_sn_tahmini': 31.0, 'isci': 4, 'not': 'Faz 1 = 80 OHLCV hücresi × (5 pencere) × 3 yöntem; bootstrap 2.000'}.

## Süreler (sn)

- veri_sha: 1.5
- evren: 11.6
- panel: 58.7
- olaylar: 4.2
- kalite: 127.2
- sizinti: 45.9
- hucre_iskele: 31.1

## Panel

- sure_sn: 58.7
- sembol: 3260
- satir: 4909423
- likit_satir: 3291650
- r60_tanimli_likit: 3168880
- donem_t0: {'KESIF': 1223817, 'BAGIMSIZ': 1146915, 'IC_DOGRULAMA': 800167, 'DISI': 120751}
- donem60_purge_embargo: {'KESIF': 1140437, 'BAGIMSIZ': 1005755, 'IC_DOGRULAMA': 683574, 'PURGE': 303056, 'DISI': 120751, 'EMBARGO': 29989, 'TANIMSIZ': 8088}
- donem250_purge_embargo: {'KESIF': 937262, 'PURGE': 811871, 'BAGIMSIZ': 621558, 'TANIMSIZ': 405934, 'IC_DOGRULAMA': 364285, 'DISI': 120751, 'EMBARGO': 29989}
- ozelliksiz_satir_toplam: 847600
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

## Olay tekilliği ve dönem (purge / embargo) dağılımı

- {'yineleme': 0, 'ortusme': 0, 'olay': 22502, 'gecti': True}
- olay × ufuk × dönem: {('Y120', 'BAGIMSIZ'): 2223, ('Y120', 'EMBARGO'): 33, ('Y120', 'IC_DOGRULAMA'): 946, ('Y120', 'KESIF'): 2062, ('Y120', 'PURGE'): 937, ('Y250', 'BAGIMSIZ'): 680, ('Y250', 'EMBARGO'): 19, ('Y250', 'IC_DOGRULAMA'): 243, ('Y250', 'KESIF'): 895, ('Y250', 'PURGE'): 570, ('Y60', 'BAGIMSIZ'): 5149, ('Y60', 'EMBARGO'): 110, ('Y60', 'IC_DOGRULAMA'): 2916, ('Y60', 'KESIF'): 4292, ('Y60', 'PURGE'): 1427}

## Çoklu test yükü (aile = dal × yöntem × dönem; hücre içi Holm, aile içinde BH q = 0,10)

| dal | yontem | donem | hucre | varyant | test | ret |
|---|---|---|---|---|---|---|
| D01 | A | KESIF | 1 | 1 | 1 | 0 |
| D01 | B | KESIF | 1 | 1 | 1 | 0 |

## Hücre iskelesi (D01-S01 + olumlu / olumsuz kontrol; yalnız pipeline denetimi)

| hucre | yontem | donem | ufuk | n_olay | n | n_degisim | d | d_alt | d_ust | d_alt_blok | d_ust_blok | auc | fark | fark_alt | fark_alt_blok | fark_alt_hisse_ceyrek | net_fark | slot_rastgele_yuzdelik | lift | eksik_pay | karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01-S01 | A | KESIF | Y60 | 4292 |  |  | +0.020 | -0.023 | +0.066 | -0.023 | +0.062 | +0.492 |  |  |  |  |  |  |  | +0.000 | ETKİ YOK |
| D01-S01 | C | KESIF | Y60 |  |  | 164484 |  |  |  |  |  |  |  |  |  |  |  |  | +1.019 | +0.000 | ETKİ YOK |
| D01-S01 | B | KESIF |  |  | 3868 |  |  |  |  |  |  |  | -0.002 | -0.010 | -0.010 | -0.010 | -0.002 | +0.135 |  | +0.000 | TUTMAZ |

## Çıktılar

- K55_VERI_KALITESI.csv, K55_VERI_KAPSAMI.md, K55_EVREN.csv, K55_EVREN_DISI.csv (kategori ayrı), K55_KESIM.csv, K55_K54_TUTARLILIK.csv, K55_ORNEKLEM.csv, K55_OLAYLAR.csv.gz, K55_SIZINTI_TESTI.md, K55_HUCRE_ISKELE.csv, K55_COKLU_TEST.csv, K55_KOSU.json (kod / veri / ayar sha), panel/ pickle (repoya girmez).
