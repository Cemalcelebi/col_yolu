# MACD_UYUM — U1b ÖN KAYIT (bariz derin ikinci dip; sonuçtan ÖNCE)

Tarih: 2026-11-24 (TR 22:4x). Yazan: ana model. Bu dosya commit edilmeden ve IZ_KARNE.ik_kontrol_kapisi geçmeden sonuç hesaplanmaz.

## Kaynak
Cemal (24 Kas 22:41): "Fitil boşver; en net dipler çok bariz aşağıda olsun; öyle azıcık bir fark boşver, onlar gürültü bence."

## Tanım (değiştirilmez)
- ANA: U1b = U1 VE F65 <= -0,05. İkinci dip birinciden en az %5 aşağıda.
- Gerekçe (sonuçtan önce): Cemal'in 'çok bariz' sözü. 20 sayfalık sette DOĞRU dediklerinin 8 / 11'i >= %4,76; yuvarlak eşik %5. Ç218'in (>= %1) içinde bir alt küme.
- BİLGİ (hüküm yok):
  - U1bb = U1 VE F65 <= -0,10 ('çok bariz').
  - Derinlik dilimleri: e (F65 > -%1), d1 (-%1 .. -%5), d2 (-%5 .. -%10), d3 (<= -%10). Her karar hücresinde FARK'ın dilim sırasıyla Spearman korelasyonu. Dört hücrede de > 0 ise 'derinlikle artıyor' denir.
- Fitil şartı YOK (Cemal: 'fitil boşver').

## Ölçüm (değiştirilmez; Ç218 ile aynı)
- Veri: Ç217 satır dosyası uyum_satir.csv.gz, U1 satırları (sha seçim dosyasıyla aynı olmalı, değilse DUR). Olay başına r15, es_r15, sira, giris aynen (CETVEL2 v2.2 konum eşleri, KASA açık kesik 2022-12-31).
- Hüküm: C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum. Plasebo kapısı alt küme için koşulmaz ('plasebo hariç'). Bir hücre öteki bütün şartlarla TUTARSA, iddiadan önce plasebo MACD_UYUM ile koşulur.
- Doğrulama: aynı betik önce Ç217 U1 ABD 2016-19'u üretir (n 1279, FARK -0,39, SIRA 0,481); üretmezse DUR.
- Hücreler: ABD ve AVR x d1619 / d2022 = 4 karar hücresi; BIST bilgi.
- Karar: AÇIK VERİDE TUTTU ⇔ 4 karar hücresinin hepsinde U1b TUTAR VE (U1b - U1e) FARK farkı 4 hücrede de > 0. Aksi: TUTMADI / ÖLÇÜLEMEDİ / ÇELİŞKİLİ.
- Çoklu bakış uyarısı: aynı açık veriye K47 için 3. bakış (Ç217, Ç218, Ç219). Açık veride TUTTU çıksa bile keşiftir; kesin hüküm yalnız KASA körüyle verilir.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt; HAYIR ya da boş = kos çalışmaz)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | CETVEL2 v2.2 konum eşleri (Ç217 satır dosyası: aynı giriş günü, aynı kova, en az 5 eş); mekanik etki için U1e (eşit dipler) karşılaştırması; plasebo alt küme için koşulmuyor (yazılı) |
| K2 | geleceğe bakma | EVET | F65 yalnız t'ye kadar bilinen dip değerlerinden (Ç217 prefix denetimi 90 / 90); eşik sonuca bakmadan bu dosyada sabit |
| K3 | geçerli bar | EVET | Ç217 satır dosyası ge_hazir barlarından (H > L, V > 0) |
| K4 | tekilleştirme | EVET | Ç217 olayları: her L2 bir olay, aynı hissede en az 15 bar; bu iş yalnız alt küme alır |
| K5 | giriş fiyatı | EVET | R15 girişi t+1 açılış (Ç217 CETVEL2 v2.2) |
| K6 | veri birimi | EVET | oran ölçüleri (F65, R15, SIRA); satır dosyası sha denetimi |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler; dipteki olaylarda sonuç yukarı yanlı, raporda yazılır |
| K8 | örneklem ve dönem | EVET | iki dönem ayrı hücre, ABD + AVR karar; güç c2_hucre eğrisiyle; n < 30 ya da güç < 0,80 ÖLÇÜLEMEDİ; aynı açık veriye 3. bakış yazılı |
| K9 | ön kayıt | EVET | bu dosya commit edilmeden hesap yok; ik_kontrol_kapisi hesaptan önce çağrılır |
| K10 | ayrıştırma | UYGULANMAZ | haber / metin ayrıştırması yok; yalnız satır dosyası |
| K11 | yeniden üretim | EVET | betik önce Ç217 U1 ABD 2016-19 değerlerini yeniden üretir; üretmezse DUR |
| K12 | ifade | EVET | hüküm yalnız önceden yazılı kuralla; bilgi dilimlerinde hüküm yok; 'iz' sözü yalnız KASA körüyle |
| K13 | süreç | EVET | hesap yasak defter dosyalarını yazmaz; defter kaydı ayrı commit; push yok (izin yok) |
| K14 | boyut (gerçek para) | UYGULANMAZ | alım-satım önerisi yok; ölçüm |
