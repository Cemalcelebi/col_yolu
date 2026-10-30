# K55 — FAZ 0 RAPORU (K55-20261030-115435-aed0ee4)

- Kod K55 v0.2 (2026-10-30, Faz 0 + ön kayıt v1.2: purge = ufuk, embargo, güçlü koşu kimliği, çıktı yolu denetimi, blok bootstrap, FDR ailesi); commit aed0ee4; kilit sha 142d57ec3ef0; ayar sha 1f994b8d8ea9; kod dosyası sha 18 adet, veri dosyası sha 8 adet (K55_KOSU.json); evren sürümü 811989df4fda; örnek: 50; veri paketleri: {}.
- Faz 0 amacı altyapıyı kanıtlamaktır; hücre sonuçları iskele denetimidir, iz iddiası değildir (optimize edilmedi).

## Cemal'in 7 sorusu

1. Kaç hisse eksiksiz işlendi? 49 / 50 (eksiksiz = ≥ 260 gün, boşluksuz, sıfır hacim payı ≤ %20, OHLC hatasız, bölünme sıçraması yok, yinelenen tarih yok).
2. Kaç hissede tarihsel veri eksik? 1 (boşluklu 0, kısa seri 0, sıfır hacim yüksek 1); yükleyici dışı kısa geçmişli (< 320 gün, VERİ YETERSİZ, K55_EVREN_DISI_KISA.csv) 60; özellik için yeterli (≥ 320 gün) 50; sert hareketli (bilgi, bölünme değil) 7, aşırı getirili 8, OHLC hatalı 0.
3. Kaç sembol şirketle güvenilir eşleştirildi? CIK eşleşen 50 / 50; sektör bilinen 50; K54 sınıfı olmayan (doğrulanamayan) semboller evren dışı.
4. Delist olmuş şirketler nasıl ele alındı? Seri erken biten 12; sınıf dağılımı {1: 38, 2: 4, 3: 4, 4: 2, 5: 2}; seri sonu işlemi {'k51': 42, 'd100': 4, 'd0': 4} (d100 = iflas −%100, d0 = birleşme bedeli, k51 = son kapanış ve negatifse −%30); 4b kod yeniden kullanımı kesimi uygulandı; sınıf 6 dışarıda; olay tanımında tam pencere şartı (seri sonunu aşan pencere tanımsız).
5. Gelecek bilgisi sızıntısı testleri geçti mi? EVET — a_kesme_testi: geçti; a2_kesme_dedektor: geçti; d_olay_etiketi: geçti; b_olumlu_kontrol: geçti; c_olumsuz_kontrol: geçti; e_eslesme: geçti.
6. Denemede bütün modüller doğru çalıştı mı? EVET — evren: 50 sembol; veri_kalitesi: eksiksiz 49 / 50; panel: 79161 satır, 59989 likit; olaylar: 322 olay, tekillik geçti; sizinti: hepsi geçti; hucre_motoru: 3 satır (A / B / C), hata yok.
7. Tam evren koşusunun tahmini süresi ve kaynağı: {'sembol': 3260, 'panel_satir_tahmini': 5161297, 'bellek_GB_tahmini': 0.62, 'panel_sn': 98.0, 'olaylar_sn': 7.0, 'sizinti_sn': 20.0, 'hucre_basina_sn_tahmini': 72.0, 'isci': 4, 'not': 'Faz 1 = 80 OHLCV hücresi × (5 pencere) × 3 yöntem; bootstrap 2.000'}.

## Süreler (sn)

- veri_sha: 0.3
- evren: 11.7
- kalite: 0.8
- panel: 1.5
- olaylar: 0.1
- sizinti: 0.3
- hucre_iskele: 1.1

## Panel

- sure_sn: 1.5
- sembol: 50
- satir: 79161
- likit_satir: 59989
- r60_tanimli_likit: 58184
- donem_t0: {'KESIF': 25095, 'BAGIMSIZ': 18865, 'IC_DOGRULAMA': 14259, 'DISI': 1770}
- donem60_purge_embargo: {'KESIF': 23543, 'BAGIMSIZ': 16626, 'IC_DOGRULAMA': 12216, 'PURGE': 4977, 'DISI': 1770, 'EMBARGO': 535, 'TANIMSIZ': 322}
- donem250_purge_embargo: {'KESIF': 19402, 'PURGE': 14491, 'BAGIMSIZ': 10480, 'TANIMSIZ': 6721, 'IC_DOGRULAMA': 6590, 'DISI': 1770, 'EMBARGO': 535}
- ozelliksiz_satir_toplam: 13000
- atlanan: 0

## Olay tekilliği ve dönem (purge / embargo) dağılımı

- {'yineleme': 0, 'ortusme': 0, 'olay': 322, 'gecti': True}
- olay × ufuk × dönem: {('Y120', 'BAGIMSIZ'): 36, ('Y120', 'IC_DOGRULAMA'): 18, ('Y120', 'KESIF'): 29, ('Y120', 'PURGE'): 15, ('Y250', 'BAGIMSIZ'): 7, ('Y250', 'EMBARGO'): 1, ('Y250', 'IC_DOGRULAMA'): 3, ('Y250', 'KESIF'): 7, ('Y250', 'PURGE'): 12, ('Y60', 'BAGIMSIZ'): 74, ('Y60', 'IC_DOGRULAMA'): 36, ('Y60', 'KESIF'): 58, ('Y60', 'PURGE'): 26}

## Çoklu test yükü (aile = dal × yöntem × dönem; hücre içi Holm, aile içinde BH q = 0,10)

| dal | yontem | donem | hucre | varyant | test | ret |
|---|---|---|---|---|---|---|
| D01 | A | KESIF | 1 | 1 | 1 | 0 |
| D01 | B | KESIF | 1 | 1 | 1 | 0 |

## Hücre iskelesi (D01-S01 + olumlu / olumsuz kontrol; yalnız pipeline denetimi)

| hucre | yontem | donem | ufuk | n_olay | n | n_degisim | d | d_alt | d_ust | d_alt_blok | d_ust_blok | auc | fark | fark_alt | fark_alt_blok | fark_alt_hisse_ceyrek | net_fark | slot_rastgele_yuzdelik | lift | eksik_pay | karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01-S01 | A | KESIF | Y60 | 58 |  |  | +0.159 | -0.072 | +0.468 | -0.072 | +0.436 | +0.565 |  |  |  |  |  |  |  | +0.000 | ETKİ YOK |
| D01-S01 | C | KESIF | Y60 |  |  | 3420 |  |  |  |  |  |  |  |  |  |  |  |  | +1.131 | +0.000 | ETKİ YOK |
| D01-S01 | B | KESIF |  |  | 3 |  |  |  |  |  |  |  | -0.016 | -0.064 | -0.064 | -0.064 | -0.015 | +0.000 |  | +0.000 | VERİ YETERSİZ |

## Çıktılar

- K55_VERI_KALITESI.csv, K55_VERI_KAPSAMI.md, K55_EVREN.csv, K55_EVREN_DISI_KISA.csv, K55_OLAYLAR.csv.gz, K55_SIZINTI_TESTI.md, K55_HUCRE_ISKELE.csv, K55_COKLU_TEST.csv, K55_KOSU.json (kod / veri / ayar sha), panel/ pickle (repoya girmez).
