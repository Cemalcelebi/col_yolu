# K55 — FAZ 0 RAPORU (K55-20261030-115506-8bed3ef)

- Kod K55 v0.2 (2026-10-30, Faz 0 + ön kayıt v1.2: purge = ufuk, embargo, güçlü koşu kimliği, çıktı yolu denetimi, blok bootstrap, FDR ailesi); commit 8bed3ef; kilit sha 142d57ec3ef0; ayar sha 1f994b8d8ea9; kod dosyası sha 18 adet, veri dosyası sha 8 adet (K55_KOSU.json); evren sürümü 811989df4fda; örnek: tam evren; veri paketleri: {}.
- Faz 0 amacı altyapıyı kanıtlamaktır; hücre sonuçları iskele denetimidir, iz iddiası değildir (optimize edilmedi).

## Cemal'in 7 sorusu

1. Kaç hisse eksiksiz işlendi? 3012 / 3260 (eksiksiz = ≥ 260 gün, boşluksuz, sıfır hacim payı ≤ %20, OHLC hatasız, yinelenen tarih yok; sert hareket bayrağı bilgi, eksiksizliğe girmez).
2. Kaç hissede tarihsel veri eksik? 242 (boşluklu 86, kısa seri 0, sıfır hacim yüksek 179); yükleyici dışı kısa geçmişli (< 320 gün, VERİ YETERSİZ, K55_EVREN_DISI_KISA.csv) 60; özellik için yeterli (≥ 320 gün) 3260; sert hareketli (bilgi, bölünme değil) 738, aşırı getirili 704, OHLC hatalı 9.
3. Kaç sembol şirketle güvenilir eşleştirildi? CIK eşleşen 3259 / 3260; sektör bilinen 3235; K54 sınıfı olmayan (doğrulanamayan) semboller evren dışı.
4. Delist olmuş şirketler nasıl ele alındı? Seri erken biten 266; sınıf dağılımı {1: 2994, 2: 19, 3: 159, 4: 9, 5: 79}; seri sonu işlemi {'k51': 3082, 'd0': 159, 'd100': 19} (d100 = iflas −%100, d0 = birleşme bedeli, k51 = son kapanış ve negatifse −%30); 4b kod yeniden kullanımı kesimi uygulandı; sınıf 6 dışarıda; olay tanımında tam pencere şartı (seri sonunu aşan pencere tanımsız).
5. Gelecek bilgisi sızıntısı testleri geçti mi? EVET — a_kesme_testi: geçti; a2_kesme_dedektor: geçti; d_olay_etiketi: geçti; b_olumlu_kontrol: geçti; c_olumsuz_kontrol: geçti; e_eslesme: geçti.
6. Denemede bütün modüller doğru çalıştı mı? EVET — evren: 3260 sembol; veri_kalitesi: eksiksiz 3012 / 3260; panel: 4909423 satır, 3291650 likit; olaylar: 22502 olay, tekillik geçti; sizinti: hepsi geçti; hucre_motoru: 3 satır (A / B / C), hata yok.
7. Tam evren koşusunun tahmini süresi ve kaynağı: {'sembol': 3260, 'panel_satir_tahmini': 4909423, 'bellek_GB_tahmini': 0.59, 'panel_sn': 69.0, 'olaylar_sn': 7.0, 'sizinti_sn': 31.0, 'hucre_basina_sn_tahmini': 27.0, 'isci': 4, 'not': 'Faz 1 = 80 OHLCV hücresi × (5 pencere) × 3 yöntem; bootstrap 2.000'}.

## Süreler (sn)

- veri_sha: 0.3
- evren: 10.7
- kalite: 56.4
- panel: 69.2
- olaylar: 6.7
- sizinti: 31.4
- hucre_iskele: 27.4

## Panel

- sure_sn: 69.2
- sembol: 3260
- satir: 4909423
- likit_satir: 3291650
- r60_tanimli_likit: 3168880
- donem_t0: {'KESIF': 1223817, 'BAGIMSIZ': 1146915, 'IC_DOGRULAMA': 800167, 'DISI': 120751}
- donem60_purge_embargo: {'KESIF': 1140437, 'BAGIMSIZ': 1005755, 'IC_DOGRULAMA': 683574, 'PURGE': 303056, 'DISI': 120751, 'EMBARGO': 29989, 'TANIMSIZ': 8088}
- donem250_purge_embargo: {'KESIF': 937262, 'PURGE': 811871, 'BAGIMSIZ': 621558, 'TANIMSIZ': 405934, 'IC_DOGRULAMA': 364285, 'DISI': 120751, 'EMBARGO': 29989}
- ozelliksiz_satir_toplam: 847600
- atlanan: 0

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

- K55_VERI_KALITESI.csv, K55_VERI_KAPSAMI.md, K55_EVREN.csv, K55_EVREN_DISI_KISA.csv, K55_OLAYLAR.csv.gz, K55_SIZINTI_TESTI.md, K55_HUCRE_ISKELE.csv, K55_COKLU_TEST.csv, K55_KOSU.json (kod / veri / ayar sha), panel/ pickle (repoya girmez).

## 9. Notlar (koşudan sonra, Claude; ön kayıt v1.2 ile yeniden koşu; kararlar ve kilit değişmedi)

- Bu koşu Cemal'in 9 maddelik denetiminden sonra v1.2 kodla (commit 8bed3ef, git ağacı temiz, kilit sha 142d57ec…, ayar sha 1f994b8d…, 18 kod ve 8 veri dosyası sha256'sı K55_KOSU.json'da) yapıldı; önceki koşu (c5304ae) geçersiz sayılır.
- Purge / embargo etkisi: likit satırların Y60 için 303.056'sı PURGE, 29.989'u EMBARGO; Y250 için 811.871 PURGE. Olaylar: Y60 KEŞİF 4.292 (PURGE 1.427), Y120 KEŞİF 2.062 (PURGE 937), Y250 KEŞİF 895 (PURGE 570). Dönem sınırını aşan pencereler hiçbir döneme girmiyor.
- Eksiksiz 3.012 / 3.260: v1.2'de "sert hareket" bayrağı (738 sembol; bölünme değil haber günü hareketi) eksiksizlik tanımından çıkarıldı, bilgi sütunu oldu. Kalan eksikler: sıfır hacim payı yüksek 179 (çoğu Tiingo / pembe tahta), boşluklu 86, OHLC hatalı 9. Yükleyici dışı kısa geçmişli 60 sembol K55_EVREN_DISI_KISA.csv'de (silinmedi; VERİ YETERSİZ).
- Sızıntı testleri geçti: olumlu kontrol d +1,18 / AUC 0,83; olumsuz kontrol d −0,003, aralık sıfırı kapsıyor, AUC 0,50 (tohumlu, tekrar üretilebilir); kesme testi 0 hata; eşleşmeler tolerans içinde (eşleşmeyen pay %17; purge sonrası havuz küçüldü, 50 hisselik denemede %94).
- Hücre iskelesi D01-S01 (KEŞİF, Y60, purge sonrası): A ETKİ YOK (d +0,02; ay ve blok aralıkları sıfırı kapsıyor), C ETKİ YOK (lift 1,02), B TUTMAZ. Pipeline denetimi; iz sonucu değil. Çoklu test yükü bu koşuda 1 test (iskele); Faz 1'de aile başına yük K55_COKLU_TEST.csv'de.
- Süre: 3,5 dk (veri sha 0,3 sn, evren 11 sn, kalite 56 sn, panel 69 sn, olaylar 7 sn, sızıntı 31 sn, iskele 27 sn); panel 4,9 M satır, 0,6 GB. Faz 1 tahmini: 80 hücre × 5 pencere × 3 yöntem ≈ 27 s / varyant → ~3 saat (KEŞİF), 4 işçi, 16 GB yeter.
- BAĞIMSIZ dönem açılmadı; İÇ DOĞRULAMA yalnız sentetik kontrol değişkenlerinde kullanıldı; Tiingo indirme kapalı (ağdan veri çekilmedi); K51-K54 çıktı klasörüne yazılmadı (yol denetimi).
