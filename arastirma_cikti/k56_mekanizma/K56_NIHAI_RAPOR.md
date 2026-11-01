# K56 / K55 NİHAİ RAPOR — BAĞIMSIZ DOĞRULAMA 2024-26 (1 Kasım 2026)

## KARAR

**K55 NİHAİ: İZ YOK.** K55'in 125 KEŞİF satırı (25 hücre, 64 varyant) üç dönemde (KEŞİF 2016-21, İÇ 2022-23, BAĞIMSIZ 2024-26) seçimsiz
kontrolle sınandı; hiçbir dönemde gerçek etki hücresi yok. K55 B yöntemi (eşleşmiş ileri getiri) İÇ'te 64 / 64, BAĞIMSIZ'da 64 / 64 TUTMAZ.
K55 farkları olay tanımının seçim / ağırlık mekaniği. Karar yeni eşikle kurtarılmaz (Cemal, madde 9).

## Cemal'in 9 maddesi ve karşılığı

| Madde | Yapılan | Kayıt |
|---|---|---|
| 1. BAĞIMSIZ yalnız ön kayıtlı testler | Tek açılış K55_125_B: 125 satır + B1 / B2 / B3 + A2 / A3; ayrışma, PBO ve EVREN2 BAĞIMSIZ'da koşulmadı (ön kayıt v1.3-D) | bagimsiz/K56-BAG-20261031-231920-f993f1f |
| 2. Kod sabit, ön kayıt, hash, kilit, dolaylı erişim yok | Kod a6cbe6a; kilit K56-BAG-KILIT-20261031-231806 (kilit commit 711a17b uzak dalda); sızıntı PASS | K56_BAGIMSIZ_KILIT.json, sizinti/K56-SIZ-20261031-213309-a6cbe6a |
| 3. Yeni keşif / eşik / gösterge yok | Eşik sha kilitte; BAĞIMSIZ'da yalnız kilitli kod | ön kayıt v1.3-D |
| 4. (iii) / bütün günler ayrışması, kümelenme, yapay veri | KEŞİF + İÇ, olay düzeyi kümeler (ay, sembol·yıl, blok60; olay, zincir), 6 yapay spek | ayrisma/K56-AYR-20261031-202454-a6cbe6a |
| 5. 125 satır + B bir kez, olduğu gibi | Açılış kaydı BAŞLADI → TAMAMLANDI (sonuç sha'larıyla), asıl sonuç duyarlılıktan önce commit | K56_BAGIMSIZ_ACILIS.csv |
| 6. Tiingo 490 aday, yeni evren, ayrı doğrulama | AÇIK: indirme 1 Kasım 06:00 UTC'den itibaren (Kasım kotası), doğrulama ve evren v2 1-2 Kasım | evren_v2/ (Ç142) |
| 7. K51-K55 değişmez, yeni evren etkisi ayrı | K51-K55 dosyalarına yazılmadı (test 15); EVREN2 ayrı rapor | — |
| 8. Drive ve nihai kayıt | IZ_KARNE Ç143-Ç146, görev günlüğü, indeks; Drive OUTPUT/K56_MEKANIZMA | bu rapor |
| 9. K55 nihai karar | İZ YOK korunur | Ç146 |

## Sayılar

| Dönem | B2 satır sınıfları (125) | Hücre (25) | d(i) → d(ii) medyan | B1 geçen | B3 (64) |
|---|---|---|---|---|---|
| KEŞİF (K56-F1A) | MEKANİK 116, TERS 7, KISMEN 2, GERÇEK 0 | MEKANİK 22, TERS 2, KISMEN 1 | -0,265 → -0,014 | — | — |
| İÇ (K56-IC) | MEKANİK 112, KISMEN 10, TERS 3, GERÇEK 0 | MEKANİK 21, KISMEN 2, TERS 1, BELİRSİZ 1 | -0,369 → -0,007 | 119 | TUTMAZ 64 |
| BAĞIMSIZ (asıl) | MEKANİK 62, TERS 56, KISMEN 3, GERÇEK 4 | TERS 12, MEKANİK 10, KISMEN 2, BELİRSİZ 1 | -0,175 → +0,008 | 64 | TUTMAZ 64 |
| BAĞIMSIZ-B (duyarlılık) | MEKANİK 62, TERS 61, KISMEN 2, GERÇEK 0 | TERS 13, MEKANİK 10, KISMEN 1, BELİRSİZ 1 | -0,187 → +0,007 | 73 | TUTMAZ 64 |

- BAĞIMSIZ'daki 4 "GERÇEK ETKİ" satırı hep D06-S03 (Y120 / Y250): d(i) ≈ 0, d(ii) +0,14..+0,21; hücre çoğunluğu değil, KEŞİF / İÇ'te yok,
  duyarlılık-B'de 0. Dağınık, iz sayılmaz.
- TERS KALINTI: seçimsiz etiketle K55 yönünün tersine küçük kalıntı (TERS satırlarda d(ii) medyanı +0,041). K55'i desteklemez.
- B1 (K55 A, ilk geçiş) BAĞIMSIZ'da 64 / 125 geçti (hücre 13 tekrarladı, 12 tutmadı): ilk geçiş etiketi seçim etkisini her dönemde yeniden üretir;
  belirleyici B2'dir (ön kayıt v1.2-B).
- (iii) olay dizisinden rastgele gün: 116 satırda "GERÇEK ETKİ" etiketi, ama (iii) seçimsiz kontrol değildir (sıfır etkili yapay veride d(iii) ≈ d(i)).

## Ayrışma (Ç143), PBO / DSR (Ç144), sızıntı (Ç145)

- Ayrışma: KEŞİF 107 / 125, İÇ 97 / 125 satır mekanik; E1 / E2 / G medyanları KEŞİF -0,278 / -0,020 / +0,280, İÇ -0,340 / -0,081 / +0,250.
  Dizinin ilk günleri en düşük (-0,30 / -0,38), 21. günden sonra pozitif (+0,12 / +0,15). Yapay veri aynı deseni üretiyor: (iii) ile (ii) arasındaki
  fark olay başına eşit ağırlığın kısa dizilerin ilk günlerini öne çıkarmasından geliyor (ağırlık mekaniği), bilgi değil.
- PBO / DSR (KEŞİF + İÇ, 64 yapı, 87 ay): A yönü PBO 0,332 / DSR 0,665; kayıt yönü PBO 0,236 / DSR 0,390. K51 H8 (PBO < 0,5 VE DSR >= 0,95)
  tutmuyor: aşırı uyum riski yüksek.
- Sızıntı: T0 K55 panel (4.909.423 satır) ve olay tablosu (22.502) baştan birebir üretildi; T1 (fiyat / endeks / SEC 2023-12-31'de kesik) İÇ
  S / H / B3, bileşim (tam SEC özetiyle), ayrışma İÇ ve PBO / DSR birebir; T2a / T2b (evren de kesik) en büyük d farkı 0,0015 / 0,0104, sınıf
  değişimi yok. Karar: İÇ hesaplarında 2023-12-31 sonrası bilgiye dolaylı erişim YOK. Beklenen fark: İÇ A3 bileşim tablosu başvuru geçmişini tam
  SEC özetinden okuyor (açıklayıcı tablo; Y60 2731 → 2711 olay, bir satırın sınıfı değişir).

## Kilit ve hash'ler

- Etiket K56-BAG-KILIT-20261031-231806 (yerel), kod commit a6cbe6a785b3; kilit commit 711a17b (uzak dalda doğrulandı); kilit dosyası sha f99431a9ef9a.
- Ön kayıt sha 2d3814e1aa2e, eşik sha 974690af3e42, hipotez sha f1b4b5b5a4d6; panel 955e13dd7d6d (içerik a88f5696084e), olay 01decf291cf7,
  veri c5f346f77576, ek veri 7981b521c6e2, evren sürümü 0d00d2c97608; ortam python 3.13.16 / numpy 2.5.3 / pandas 3.0.5.
- Açılış: K56-BAG-20261031-231920-f993f1f, BAŞLADI 23:19:20 → TAMAMLANDI 00:16:09; sonuç sha: SATIR d0200331d9e1, HUCRE abb512e470bc,
  B3 5adddc8fcf25, BİLEŞİM 47c0c04b268a; B_SATIR e02a1f3fd95e, B_HUCRE 6288cc1b95a5, B_B3 f81f839fb230, B_BİLEŞİM e621c7731139.

## Sapmalar (hepsi BAĞIMSIZ açılmadan, sonuç görülmeden; ön kayıt v1.3-c / v1.3-d)

- İlk iki tam sızıntı denemesi test hatasıyla geçersiz (ayrışma tohum etiketi; yapay karar sütunları), NOT.md ile saklandı. Düzeltme: tek etiket
  sabiti, ortak satır kararı fonksiyonu, kimlik_fark özdeşlik olarak, ayrışma karşılaştırmasında 1e-12 (CSV son bit okuması).
- Bu ortamın git vekili etiket push'unu reddediyor (403): kilidin uzak çapası etiket yerine çalışma dalı (kilit commit'i push + ls-remote; açılışta
  kilit commit'inin uzak dalda olduğu denetlenir). Kod değiştiği için ayrışma, PBO ve sızıntı yeniden koşuldu (sonuçlar önceki koşularla birebir).

## Açık

- EVREN2 (Ç142): Tiingo 490 aday (Ö1 199 + Ö2 291) 1 Kasım 06:00 UTC'den itibaren bekçiyle iner; kimlik, adi hisse, fiyat kapsamı, son işlem,
  delist sınıfı ayrı ayrı doğrulanır; evren v2 etkisi KEŞİF / İÇ'te ayrı rapor. K51-K55 ve bu karar değişmez; BAĞIMSIZ yeniden açılmaz.

## Dosyalar

- Ön kayıt: K56/ONKAYIT_K56.md (v1.3, v1.3-a..d), K56/ONKAYIT_K56_SATIRLAR.csv
- BAĞIMSIZ: arastirma_cikti/k56_mekanizma/bagimsiz/K56-BAG-20261031-231920-f993f1f/ (RAPOR_ASIL.md, RAPOR_DUYARLILIK_B.md, K56BAG_*.csv,
  K56BAG_K55_NIHAI_KARAR.md)
- Kilit ve açılış kaydı: arastirma_cikti/k56_mekanizma/K56_BAGIMSIZ_KILIT.json, K56_BAGIMSIZ_ACILIS.csv
- Ayrışma / PBO / sızıntı: arastirma_cikti/k56_mekanizma/{ayrisma,pbo_dsr,sizinti}/SON.json
