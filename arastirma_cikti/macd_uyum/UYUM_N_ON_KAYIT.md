# MACD_UYUM — U1n ÖN KAYIT (net derin ikinci dip; sonuçtan ÖNCE)

Tarih: 2026-11-24 (TR 21:3x). Yazan: ana model. Sonuç (r15 / FARK / h5) bu dosya commit edilmeden hesaplanmadı; 20 sayfalık anahtar (uyum_ornek20_anahtar.json) açılmadı.

## Kaynak
Cemal'in UYUM_ORNEK20.pdf işaretleri (24 Kas 21:15; dosya 8aa0a2f3-UYUM_ORNEK201.pdf, PDF mürekkep notları ana model tarafından okundu):
- YANLIŞ 9: sayfa 1, 2, 17 ('Eşit'), 19 ('Eşit seviye'), 3 (dipleri gösteren ok), 13, 11 ('Net değil'), 15 ('Net değil', 2. dip uzun fitil), 6 (1. dip çarpı, MACD dipleri daire).
- DOĞRU 11: 4, 7, 8, 9, 10, 12, 14, 16, 18, 20; 5 işaretsiz ('diğerleri doğru' sözüyle DOĞRU).
- Cemal'in sözü: 'bazı ilk ve sonraki dipler eşit seviyede, neredeyse net değil; onlara yanlış dedim, diğerleri doğru'.

## Tanım (değiştirilmez)
- U1n = U1 VE F65 <= -0,01: ikinci dip birinciden EN AZ %1 aşağıda. K47 kodunun 'aynı' saydığı ±%1 bandı (Low(L2) <= Low(L1) x 1,01) artık dışarıda.
- U1e (bilgi) = U1 VE F65 > -0,01 ('eşit' dipler).
- Eşik seçimi: Cemal'in 20 işaretine UYDURULMADI. Uydurulsaydı %1,2 olurdu (sayfa 19 -%1,06 YANLIŞ, sayfa 7 -%1,22 DOĞRU). Kodun mevcut %1 toleransı ters çevrildi.
- Uyum (bilgi, n 20): U1n kuralı Cemal'le 16 / 20 (kappa 0,58). Uyuşmayan 4 sayfa: 6, 11, 15 başka nedenli (dip yeri, net değil, uzun fitil), 19 sınırda (-%1,06).
- ATR birimi seçilmedi: atrp_t satır dosyasında yalnız ABD'de var; ABD'de ayrım yüzdeden iyi değil (sayfa 3 0,21 / sayfa 7 0,25 ATR).

## Ölçüm (değiştirilmez)
- Veri: Ç217 satır dosyası uyum_satir.csv.gz (U1 satırları; sha256 seçim dosyasındaki 'satir_sha256' ile aynı olmalı, değilse DUR). Olay başına r15, es_r15, sira, giris aynen (CETVEL2 v2.2 konum eşleri, KASA açık kesik 2022-12-31).
- Hücre: MACD_UYUM ile aynı fonksiyonlar. C2.c2_hucre(r15, es_r15, sira, giris, '+', egri = C2._c2_egri22_al(pazar, hücre, 15, None)) + MU.mu_sira_boot + MU.mu_hukum.
- Plasebo kapısı alt küme için YENİDEN KOŞULMAZ. Hüküm 'plasebo hariç' yazılır. Bir hücre öteki bütün şartlarla TUTARSA, iddiadan önce plasebo MACD_UYUM ile koşulur.
- Doğrulama: aynı betik önce U1'in Ç217 değerlerini (ABD d1619 FARK -0,39, SIRA 0,481) yeniden üretmeli; üretmezse DUR.
- Hücreler: ABD ve AVR x d1619 / d2022 = 4 karar hücresi; BIST bilgi.
- Karar: AÇIK VERİDE TUTTU ⇔ 4 karar hücresinin hepsinde U1n TUTAR (plasebo hariç şartlarla) VE (U1n - U1e) FARK farkı 4 hücrede de > 0. Aksi: TUTMADI / ÖLÇÜLEMEDİ / ÇELİŞKİLİ (Ç217 kuralı).
- Bilgi: h5 / h10 / stop olay vs eş; r15 ortalama; Cemal'in 20 sayfasında DOĞRU vs YANLIŞ sonuçları (anahtar bu hesaptan SONRA açılır; n 20, bulgu değil).
