# MACD_UYUM — U1bm ÖN KAYIT (bariz fiyat dibi + belirgin MACD farkı, temiz eşle; sonuçtan ÖNCE)

Tarih: 2026-11-25. Yazan: ana model. Bu dosya commit edilmeden ve ik_kontrol_kapisi geçmeden sonuç hesaplanmaz.

## Kaynak
Cemal'in UYUM_B_SONRA20 işaretleri (25 Kas; 'doğru okumuşsun' teyidi): 15 sayfa DOĞRU; 5 sayfa (5, 6, 7, 17, 18) 'Belirgin değil', beşinde de MACD dipleri daire içinde. Ayrıca Cemal (25 Kas): 'belki de seçilen eşlerin içinde aynı uyumsuzluk vardı'.

## Tanım (değiştirilmez)
- MR = (MACD(L2) − MACD(L1)) / |MACD(L1)| = F66 / |F66m − F66| (uyum_olay.csv.gz U1 satırları).
- ANA: U1bm = U1 ∧ F65 <= -0,05 ∧ MR >= 0,20. Fiyatın ikinci dibi en az %5 aşağıda, MACD ikinci dipte en az %20 daha yukarıda.
- Eşik gerekçesi (getirisiz): 'Belirgin değil' 5 sayfanın MR'si 0,03-0,20 (5 / 5 eşiğin altı); DOĞRU 15 sayfanın 9'u eşiğin üstü; kural-Cemal uyumu 14 / 20 (kappa 0,43). BARIZ olaylarda MR medyanı 0,20; getirisiz sayım: ABD 244 / 460, AVR 90 / 140, BIST 146 / 72.
- KONTROL (bilgi): U1bz = U1 ∧ F65 <= -0,05 ∧ MR < 0,20.
- Bilgi: U1 ∧ MR >= 0,20 (fiyat şartsız); MR >= 0,35.

## Ölçüm (değiştirilmez)
- Veri: es_satir.csv.gz (Ç220 eş kirliliği koşusu; r15, es_r15_temiz, sira_temiz = K20 temiz eş; es_r15, sira = Ç217 eski eş).
- ANA hüküm TEMİZ eşle: C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum, plasebo hariç. Eski eşle aynı tablo bilgi.
- Doğrulama: betik önce BARIZ ABD 2016-19 temiz eş değerini (n 502, FARK -0,16) üretir; üretmezse DUR.
- Hücreler: ABD ve AVR x d1619 / d2022 = 4 karar; BIST bilgi.
- Karar: AÇIK VERİDE TUTTU ⇔ 4 karar hücresinin hepsinde U1bm TUTAR VE (U1bm − U1bz) FARK farkı dördünde de > 0. Aksi TUTMADI / ÖLÇÜLEMEDİ / ÇELİŞKİLİ (Ç217 kuralı: gücü yeterli hücrede tutmuyorsa TUTMADI; hepsi güçsüzse ÖLÇÜLEMEDİ).
- Çoklu bakış: K47 için aynı açık veriye 5. bakış; TUTTU çıksa bile keşif, kesin hüküm yalnız KASA körü.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt; HAYIR ya da boş = kos çalışmaz)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | CETVEL2 v2.2 konum eşleri (Ç217 satır dosyası: aynı giriş günü, aynı kova, en az 5 eş); ANA ölçü K20 TEMİZ eş (ES_ON_KAYIT; son 20 barda ham U1 durumu taşıyan eşler dışarıda); mekanik etki için BARIZ ∧ MR < 0,20 karşılaştırması; plasebo alt küme için koşulmuyor (yazılı) |
| K2 | geleceğe bakma | EVET | F65, F66, F66m yalnız t'ye kadar bilinen dip değerlerinden (Ç217 prefix denetimi 90 / 90); eşik sonuca bakmadan bu dosyada sabit |
| K3 | geçerli bar | EVET | Ç217 satır dosyası ge_hazir barlarından (H > L, V > 0) |
| K4 | tekilleştirme | EVET | Ç217 olayları: her L2 bir olay, aynı hissede en az 15 bar; bu iş yalnız alt küme alır |
| K5 | giriş fiyatı | EVET | R15 girişi t+1 açılış (Ç217 CETVEL2 v2.2) |
| K6 | veri birimi | EVET | oran ölçüleri (F65, R15, SIRA); satır dosyası sha denetimi |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler; dipteki olaylarda sonuç yukarı yanlı, raporda yazılır |
| K8 | örneklem ve dönem | EVET | iki dönem ayrı hücre, ABD + AVR karar; güç c2_hucre eğrisiyle; n < 30 ya da güç < 0,80 ÖLÇÜLEMEDİ; aynı açık veriye 5. bakış yazılı |
| K9 | ön kayıt | EVET | bu dosya commit edilmeden hesap yok; ik_kontrol_kapisi hesaptan önce çağrılır |
| K10 | ayrıştırma | UYGULANMAZ | haber / metin ayrıştırması yok; yalnız satır dosyası |
| K11 | yeniden üretim | EVET | betik önce Ç217 U1 ABD 2016-19 değerlerini yeniden üretir; üretmezse DUR |
| K12 | ifade | EVET | hüküm yalnız önceden yazılı kuralla; bilgi dilimlerinde hüküm yok; 'iz' sözü yalnız KASA körüyle |
| K13 | süreç | EVET | hesap yasak defter dosyalarını yazmaz; defter kaydı ayrı commit; push yok (izin yok) |
| K14 | boyut (gerçek para) | UYGULANMAZ | alım-satım önerisi yok; ölçüm |
