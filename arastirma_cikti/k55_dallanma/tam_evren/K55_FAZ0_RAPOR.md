# K55 — FAZ 0 RAPORU (K55-20261030-093902-c5304ae)

- Kod K55 v0.1 (2026-10-30, Faz 0: evren, veri kalitesi, ortak panel, olay tanımları, sızıntı testleri, hücre iskelesi A / B / C); commit c5304ae; kilit sha 0563ff3c7d0f; evren sürümü 811989df4fda; örnek: tam evren; veri paketleri: {}.
- Faz 0 amacı altyapıyı kanıtlamaktır; hücre sonuçları iskele denetimidir, iz iddiası değildir (optimize edilmedi).

## Cemal'in 7 sorusu

1. Kaç hisse eksiksiz işlendi? 2411 / 3260 (eksiksiz = ≥ 260 gün, boşluksuz, sıfır hacim payı ≤ %20, OHLC hatasız, bölünme sıçraması yok, yinelenen tarih yok).
2. Kaç hissede tarihsel veri eksik? 242 (boşluklu 86, kısa seri 0, sıfır hacim yüksek 179); sıçramalı 738, aşırı getirili 704, OHLC hatalı 9.
3. Kaç sembol şirketle güvenilir eşleştirildi? CIK eşleşen 3259 / 3260; sektör bilinen 3235; K54 sınıfı olmayan (doğrulanamayan) semboller evren dışı.
4. Delist olmuş şirketler nasıl ele alındı? Seri erken biten 266; sınıf dağılımı {1: 2994, 2: 19, 3: 159, 4: 9, 5: 79}; seri sonu işlemi {'k51': 3082, 'd0': 159, 'd100': 19} (d100 = iflas −%100, d0 = birleşme bedeli, k51 = son kapanış ve negatifse −%30); 4b kod yeniden kullanımı kesimi uygulandı; sınıf 6 dışarıda; olay tanımında tam pencere şartı (seri sonunu aşan pencere tanımsız).
5. Gelecek bilgisi sızıntısı testleri geçti mi? EVET — a_kesme_testi: geçti; a2_kesme_dedektor: geçti; d_olay_etiketi: geçti; b_olumlu_kontrol: geçti; c_olumsuz_kontrol: geçti; e_eslesme: geçti.
6. Denemede bütün modüller doğru çalıştı mı? EVET — evren: 3260 sembol; veri_kalitesi: eksiksiz 2411 / 3260; panel: 4909423 satır, 3291650 likit; olaylar: 22502 olay, tekillik geçti; sizinti: hepsi geçti; hucre_motoru: 3 satır (A / B / C), hata yok.
7. Tam evren koşusunun tahmini süresi ve kaynağı: {'sembol': 3260, 'panel_satir_tahmini': 4909423, 'bellek_GB_tahmini': 0.59, 'panel_sn': 55.0, 'olaylar_sn': 4.0, 'sizinti_sn': 18.0, 'hucre_basina_sn_tahmini': 31.0, 'isci': 4, 'not': 'Faz 1 = 80 OHLCV hücresi × (5 pencere) × 3 yöntem; bootstrap 2.000'}.

## Süreler (sn)

- evren: 9.7
- kalite: 59.8
- panel: 54.7
- olaylar: 3.6
- sizinti: 18.3
- hucre_iskele: 30.6

## Panel

- sure_sn: 54.7
- sembol: 3260
- satir: 4909423
- likit_satir: 3291650
- r60_tanimli_likit: 3168880
- donem: {'KESIF': 1223817, 'BAGIMSIZ': 1146915, 'IC_DOGRULAMA': 800167, 'DISI': 120751}
- atlanan: 0

## Olay tekilliği

- {'yineleme': 0, 'ortusme': 0, 'olay': 22502, 'gecti': True}

## Hücre iskelesi (D01-S01 + olumlu / olumsuz kontrol; yalnız pipeline denetimi)

| hucre | yontem | donem | ufuk | n_olay | n | n_degisim | d | d_alt | d_ust | auc | fark | fark_alt | net_fark | slot_rastgele_yuzdelik | lift | eksik_pay | karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01-S01 | A | KESIF | Y60 | 4482 |  |  | +0.021 | -0.021 | +0.066 | +0.489 |  |  |  |  |  | +0.000 | ETKİ YOK |
| D01-S01 | C | KESIF | Y60 |  |  | 170881 |  |  |  |  |  |  |  |  | +1.027 | +0.000 | ETKİ YOK |
| D01-S01 | B | KESIF |  |  | 4199 |  |  |  |  |  | -0.000 | -0.009 | -0.000 | +0.180 |  | +0.000 | TUTMAZ |

## Çıktılar

- K55_VERI_KALITESI.csv, K55_VERI_KAPSAMI.md, K55_EVREN.csv, K55_OLAYLAR.csv.gz, K55_SIZINTI_TESTI.md, K55_HUCRE_ISKELE.csv, K55_KOSU.json, panel pickle (veri klasörü, repoya girmez).

## 9. Notlar (koşudan sonra, Claude; kararlar ve kilit değişmedi)

- Eksiksiz 2.411 / 3.260 sayısı sıkı tanımdan gelir. Eksik türleri: sıfır hacim payı > %20 → 179 (çoğu Tiingo batan / pembe tahta serileri), boşluk → 86, "bölünme sıçraması" bayrağı → 738. Bu bayrak |günlük hareket| > %80 ve ters yönlü hacim koşuludur; fiyatlar Yahoo / Tiingo'da bölünme düzeltmeli olduğundan bunların çoğu bölünme değil, küçük hisselerde haber günü hareketidir. Bayrak dışlama değil işarettir: Faz 1 başında 30 örnek elle bakılıp bayrak tanımı gerekirse daraltılır (veri kalitesi kuralı; ölçüt değil). OHLC hatalı 9 sembol-gün satırı ölçü dışı.
- Olay sayıları yıllara göre artıyor (Y60: 2016'da 356, 2025'te 2.752). Sebep evrenin kuruluşu: V_ABD ve K34 Yahoo bugünkü sembollerdir (hayatta kalanlar), K34 şirketleri evrene ilk SEC bildirimiyle (2021+) girer; 2020 ve 2025 piyasa tepeleri de eklenir. Bu yüzden taban oranı yıl yıl değişir; A yöntemi aynı gün içinde, B yöntemi aynı gün eşleşmiş karşılaştırma yapar; yıllar arası tekrar ölçütü de bu yüzden işaret tutarlılığıdır, olay sayısı değil.
- Sızıntı testleri tam evrende de geçti: olumlu kontrol (t+60 getirisi) d = +1,19, AUC 0,83; olumsuz kontrol (rastgele) d = −0,001, aralık sıfırı kapsıyor, AUC 0,50; kesme testi 0 hata; geleceğe bakan değişken kesme testinde kaldı (dedektör çalışıyor); olay etiketi pencere dışı değişiklikten etkilenmiyor; eşleşmiş kontroller tarih toleransı içinde, hisse farklı, eşleşmeyen pay %10,7 (50 hisselik denemede %94: eşleştirme havuzu için tam evren şart).
- Hücre iskelesi D01-S01 (KEŞİF, Y60): A ETKİ YOK (d +0,02), C ETKİ YOK (lift 1,03), B TUTMAZ (fark 0,000). Bu bir iz sonucu değil, pipeline denetimidir; Faz 1'de aynı hücre pencere varyantlarıyla ve FDR ile koşar.
- Tam evren maliyeti: Faz 0 koşusu 3,2 dk (evren 10 sn, kalite 60 sn, panel 55 sn, olaylar 4 sn, sızıntı 18 sn, iskele 31 sn); panel 4,9 M satır, 0,6 GB. Faz 1 tahmini: 80 OHLCV hücresi × 5 pencere × (A + B + C, KEŞİF) ≈ 31 s / varyant → ~3,5 saat; 4 işçi, 16 GB yeter.
- Faz 1'e geçiş şartları (Cemal'in listesi): 7 soru cevaplandı; sızıntı testleri geçti; 50 hisselik deneme ve tam evren koşusu aynı kodla, aynı kilitle (sha b4b69219…) çalıştı; BAĞIMSIZ dönem hiç açılmadı; İÇ DOĞRULAMA yalnız sentetik kontrol değişkenlerinde kullanıldı.
