# K57-C ÖN KAYIT — geniş ABD evreninde önceden yazılı 3 deneme (YEOTK profili V1 çevresi, son tur)

Yazım zamanı: 2026-11-09 18:44:10 UTC (2026-11-09 21:44 TR) (K57-C ölçümünden ÖNCE; K57-C sonucu görülmedi; K57 ve K57-B sonuçları biliniyor). Sürüm: K57-C v1.0 (2026-11-09): geniş ABD evreninde önceden yazılı 3 deneme (C1 V1+F4, C2 likidite tabanı 5 milyon $, C3 'ear' üst %10)
K57C_SHA256: b81b5fb148be28a742ab90db2bac5eb8a213c3379cb4abbce22a53a74d1315f0
(K57C_ESIK + K57B_ESIK + FI_OLCUT + K57_ESIK + K57_ATLA sha256'sı. `python K57.py c_kos` bu mühürle başlar; biri değişirse koşu durur.)
K57 mührü (değişmeden): 2a6cc6f6d1fd52e7dc9e7711f580c145a3c87f59369b12e40c4052fe1ce4b1f0
K57B mührü (değişmeden): abc73b49f1df30c1d4fff698a154b08a9bef684e673d9dad7eaf801e77583457
Kaynak dosyalar (c_kos başında yeniden hesaplanır; biri farklıysa koşu durur):
Kaynak K57_ON_KAYIT.md sha256: 6adf522c49185b2010bfa1d35c2b6d3e790c207708ffd1b08833e652b973d1b2
Kaynak K57B_ON_KAYIT.md sha256: 5d7180dfdcbbdcabd4d219e89869655bf5f83a52648970445bdee2aa1d726f4e
Kaynak evren_b1.csv sha256: f57065c7a94475f517922839ce7d43c95475478bb7a3b01fef8e7ae54751dcf9
Kaynak olaylar_b1_abd.csv.gz sha256: 55b3888f40aeaf76936c7ade30c174215ef9543d4290e171f39af66d77fd9e10
Kaynak hucre_b.csv sha256: 0b2dd81bbb7d7007d43a44106e67953ece31715291e9acb07deec05f87fb61de

## 1. Neden ve kaynak
K57 (Ç148) ve K57-B (Ç149) İZ DEĞİL. K57B_ON_KAYIT.md §6'da, K57-B sonucu görülmeden şu üç deneme yazıldı (aynen):
- C1: V1 + F4 (seyrelme yok) geniş ABD evreninde, 60 gün.
- C2: V1 geniş ABD evreninde, likidite tabanı 5 milyon $.
- C3: V1 geniş ABD evreninde, F7 yerine yalnız 'ear' üst %10 (ham şartı aynı).
Bu dosya o tanımları DEĞİŞTİRMEZ; yalnız orada yazılı olmayan ayrıntıları ölçümden önce doldurur (aşağıda her biri 'BOŞLUK' diye işaretli).

## 2. Ortak kurgu (K57-B B1 ile aynı; değişmez)
- Evren, fiyat, olay, tepki, giriş, süzgeç tanımları: K57B_ON_KAYIT.md §2-§3 B1 (SEC frames'te gelir + kâr + özkaynak verisi ve borsa kodu olan
  şirketler, Yahoo düzeltmeli günlük fiyat 2026-08-31'de kesik; likidite = tepki gününde biten 20 işlem günlük medyan işlem
  değeri, Close x Volume). F1 ABD çeyrek satışı yıllık >= +%25; F2 satış >= 1.4 x önceki iki çeyrek ortalaması VE kâr > 0 VE
  > önceki çeyrek; F3 yükümlülük <= 3.0 x özkaynak; temel değerlerin bilgi tarihi <= D.
- Ölçüt FI_OLCUT (değiştirilmeden): eşli fark (aynı gün, 60 gün momentum beşliği x 20 gün likidite üçlüsü; eşler geniş evrenin bütün
  hisselerinden, tabana bağlı değil), ay kümeli bootstrap (2000) %95 aralık, hücre içi sıra, 10 yuvalı slot portföyü vs 200 eşli rastgele portföy.
  Ufuk 60 gün. Hücreler (giriş gününe göre): ABD 2021-22 BİLGİ, ABD 2023 KARAR, ABD 2024-26 KARAR.

## 3. Boşluk doldurma (K57B_ON_KAYIT.md'de yazılı değildi; ölçümden önce burada sabitlendi)
- BOŞLUK 1 — likidite tabanı: C1 ve C3'te B1'deki 1,000,000 $ aynen; C2'de 5,000,000 $. Her denemede taban altı olay
  olay kümesine hiç girmez.
- BOŞLUK 2 — C2'de F7 eşiği: B1 kuralı ('F7'nin kayan eşiği taban üstü olaylardan hesaplanır') yeni tabana uygulanır: eşik yalnız
  5,000,000 $ üstü olaylardan (D'ye kadar son 92 gün, en az 30 değer, üst %20), VE ham >= +%5.
- BOŞLUK 3 — C1'de F4: K57 tanımı aynen (K57_ON_KAYIT §3): yıllık pay değişimi <= +%10, başvuru günü <= D olan en son SEC
  bildirimi (FON_IZI fi_k31_finansal, SEC özütleri); oran bir tamsayıya ±%3 yakınsa bölünme (geçer); veri yoksa geçmez.
- BOŞLUK 4 — C3'te 'ear' üst %10: K57 F7'sinin aynı kayan kuralı, yalnız dilim %10: 'ear' D'ye kadar son 92 günde
  tepki günü biten (1,000,000 $ taban üstü) olayların üst %10'unda (en az 30 değer) VE ham >= +%5; F1, F2, F3 aynı.
- BOŞLUK 5 — veri: yeni SEC ve Yahoo isteği YAPILMAZ. Evren K57-B'nin evren_b1.csv'si; fiyatlar /tmp/k57b_fiyat/ önbelleğinden, SEC frames
  /tmp/secframes önbelleğinden okunur. c_kos önce önbellekten kurulan evrenin (sembol ve durum) evren_b1.csv ile aynı olduğunu, sonra B1 V1
  hücrelerinin (üç hücrede n ve ortalama eşli fark) hucre_b.csv ile, V1 olay kümesinin olaylar_b1_abd.csv.gz ile aynı çıktığını denetler; değilse durur.
  C1'in F7'si B1'in F7'siyle aynı olmalı (aynı taban, aynı dilim); değilse durur.
- BOŞLUK 6 — BIST: üç deneme de 'geniş ABD evreninde' tanımlı; BIST'te karşılığı yok, BIST hücresi ölçülmez ('uygulanmaz').
- BOŞLUK 7 — hat kapanış ölçütü (önceden): K57 (V0-V4, D1-D3), K57-B (B1-B3) ve K57-C (C1-C3) içinde hiçbir deneme iki ABD karar hücresinde
  birden dört şartı geçmediyse rapor YEOTK profili hattının yeni varyant açılmadan kapatılmasını ÖNERİR (karar ana oturumda). C'den ABD-ADAY
  çıkarsa kapanış önerilmez; aday yalnız canlı (örneklem dışı) izlemeye önerilir.

## 4. Karar (değişmez; K57B_ON_KAYIT §4 ile aynı)
Her deneme ayrı okunur: ABD 2023 ve ABD 2024-26 hücreleri FI_OLCUT dört şartıyla (n >= 30; ortalama eşli fark > 0 ve aralık alt ucu > 0;
sıra > 0,50; portföy > eşli rastgele %90). İkisi de tutarsa 'ABD-ADAY (AVRUPA VERİSİ YOK)' (Avrupa'da bilanço olay verisi yok,
İZ denemez). Aksi 'İZ DEĞİL'. Sonuç görüldükten sonra eşik değişmez. Çoklu deneme: K57 (5 varyant + 3 devam) + K57-B (3) + K57-C (3).

## 5. Beklenti (önceden)
- C1 ve C3, B1 V1 olaylarının alt kümesidir (C1'de F4 ek şart; C3'te aynı penceredeki %10 eşiği %20 eşiğinden düşük olamaz). B1'de ABD 2023
  n 16 idi: C1 ve C3'te ABD 2023 n <= 16 < 30, yani bu iki deneme yapısı gereği ABD 2023'te TUTAMAZ (önceden yazılı deneme olduğu için
  yine koşulur ve kayda geçer).
- C2: 5 milyon $ tabanı n'yi büyük olasılıkla küçültür (F7 eşiği yeniden hesaplandığı için tam alt küme değil); ABD 2023'te n >= 30 olasılığı çok düşük.
- Üçünün de İZ DEĞİL çıkması beklenir; bu tur YEOTK profili hattının kapanış kaydıdır.
