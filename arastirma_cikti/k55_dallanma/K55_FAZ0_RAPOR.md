# K55 — FAZ 0 RAPORU (K55-20261030-093840-c5304ae)

- Kod K55 v0.1 (2026-10-30, Faz 0: evren, veri kalitesi, ortak panel, olay tanımları, sızıntı testleri, hücre iskelesi A / B / C); commit c5304ae; kilit sha 0563ff3c7d0f; evren sürümü 811989df4fda; örnek: 50; veri paketleri: {}.
- Faz 0 amacı altyapıyı kanıtlamaktır; hücre sonuçları iskele denetimidir, iz iddiası değildir (optimize edilmedi).

## Cemal'in 7 sorusu

1. Kaç hisse eksiksiz işlendi? 42 / 50 (eksiksiz = ≥ 260 gün, boşluksuz, sıfır hacim payı ≤ %20, OHLC hatasız, bölünme sıçraması yok, yinelenen tarih yok).
2. Kaç hissede tarihsel veri eksik? 1 (boşluklu 0, kısa seri 0, sıfır hacim yüksek 1); sıçramalı 7, aşırı getirili 8, OHLC hatalı 0.
3. Kaç sembol şirketle güvenilir eşleştirildi? CIK eşleşen 50 / 50; sektör bilinen 50; K54 sınıfı olmayan (doğrulanamayan) semboller evren dışı.
4. Delist olmuş şirketler nasıl ele alındı? Seri erken biten 12; sınıf dağılımı {1: 38, 2: 4, 3: 4, 4: 2, 5: 2}; seri sonu işlemi {'k51': 42, 'd100': 4, 'd0': 4} (d100 = iflas −%100, d0 = birleşme bedeli, k51 = son kapanış ve negatifse −%30); 4b kod yeniden kullanımı kesimi uygulandı; sınıf 6 dışarıda; olay tanımında tam pencere şartı (seri sonunu aşan pencere tanımsız).
5. Gelecek bilgisi sızıntısı testleri geçti mi? EVET — a_kesme_testi: geçti; a2_kesme_dedektor: geçti; d_olay_etiketi: geçti; b_olumlu_kontrol: geçti; c_olumsuz_kontrol: geçti; e_eslesme: geçti.
6. Denemede bütün modüller doğru çalıştı mı? EVET — evren: 50 sembol; veri_kalitesi: eksiksiz 42 / 50; panel: 79161 satır, 59989 likit; olaylar: 322 olay, tekillik geçti; sizinti: hepsi geçti; hucre_motoru: 3 satır (A / B / C), hata yok.
7. Tam evren koşusunun tahmini süresi ve kaynağı: {'sembol': 3260, 'panel_satir_tahmini': 5161297, 'bellek_GB_tahmini': 0.62, 'panel_sn': 65.0, 'olaylar_sn': 7.0, 'sizinti_sn': 20.0, 'hucre_basina_sn_tahmini': 72.0, 'isci': 4, 'not': 'Faz 1 = 80 OHLCV hücresi × (5 pencere) × 3 yöntem; bootstrap 2.000'}.

## Süreler (sn)

- evren: 9.2
- kalite: 0.6
- panel: 1.0
- olaylar: 0.1
- sizinti: 0.3
- hucre_iskele: 1.1

## Panel

- sure_sn: 1.0
- sembol: 50
- satir: 79161
- likit_satir: 59989
- r60_tanimli_likit: 58184
- donem: {'KESIF': 25095, 'BAGIMSIZ': 18865, 'IC_DOGRULAMA': 14259, 'DISI': 1770}
- atlanan: 0

## Olay tekilliği

- {'yineleme': 0, 'ortusme': 0, 'olay': 322, 'gecti': True}

## Hücre iskelesi (D01-S01 + olumlu / olumsuz kontrol; yalnız pipeline denetimi)

| hucre | yontem | donem | ufuk | n_olay | n | n_degisim | d | d_alt | d_ust | auc | fark | fark_alt | net_fark | slot_rastgele_yuzdelik | lift | eksik_pay | karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01-S01 | A | KESIF | Y60 | 60 |  |  | +0.144 | -0.064 | +0.441 | +0.562 |  |  |  |  |  | +0.000 | ETKİ YOK |
| D01-S01 | C | KESIF | Y60 |  |  | 3560 |  |  |  |  |  |  |  |  | +1.095 | +0.000 | ETKİ YOK |
| D01-S01 | B | KESIF |  |  | 3 |  |  |  |  |  | -0.016 | -0.064 | -0.015 | +0.000 |  | +0.000 | VERİ YETERSİZ |

## Çıktılar

- K55_VERI_KALITESI.csv, K55_VERI_KAPSAMI.md, K55_EVREN.csv, K55_OLAYLAR.csv.gz, K55_SIZINTI_TESTI.md, K55_HUCRE_ISKELE.csv, K55_KOSU.json, panel pickle (veri klasörü, repoya girmez).
