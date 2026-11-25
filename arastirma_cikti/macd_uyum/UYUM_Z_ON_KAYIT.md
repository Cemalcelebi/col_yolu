# MACD_UYUM — ZİNCİR ÖN KAYIT (devam eden uyumsuzluk; sonuçtan ÖNCE)

Kaynak: Cemal (25 Kas 08:30): 'tutmayan uyumsuzluğun devamı oluyor; ikinci dip daha derin, üçüncü ve dördüncü daha derin ve her seferinde uyumsuzluk devam ediyor; bazen ikideki uyumsuzluktan döner, bazen sonraki diplerden'.

## Tanım (değiştirilmez)
- ZİNCİR SIRASI: aynı hissede U1 olayları sinyal günü sırasıyla. Bir olayın sırası = önceki U1 olayı en çok 60 geçerli bar önceyse VE bu olayın Low(L2)'si öncekinin Low(L2)'sinden düşükse önceki sıra + 1; değilse 1. Yalnız geçmiş olaylar kullanılır (K2). Dosya: uyum_zincir.csv.gz (getirisiz üretildi; sayım: zincir 1 / 2 / 3+ tablosu commit'te).
- ANA: Z2 = sıra >= 2 (devam eden uyumsuzluk). KONTROL: Z1 = sıra 1. BİLGİ: sıra 2, sıra 3+ ayrı; Z2 ∧ F65 <= -0,05.
- BETİMSEL (hüküm yok, sonradan bakma): sıra 1 olayından sonra 60 bar içinde daha derin dipte yeni uyumsuzluk gelme payı; gelen ve gelmeyen ilk olayların r15 ve +%5 / stop payları.

## Ölçüm
- es_satir.csv.gz (K20 temiz eş): C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum, plasebo hariç. h5 / stop payları uyum_satir.csv.gz'den.
- Doğrulama: BARIZ ABD 2016-19 temiz n 502, FARK -0,16; üretmezse DUR.
- Karar: AÇIK VERİDE TUTTU ⇔ 4 karar hücresinde (ABD, AVR x d1619, d2022) Z2 TUTAR VE (Z2 − Z1) FARK farkı dördünde > 0. Gücü yeterli hücrede tutmuyorsa TUTMADI; hepsi güçsüzse ÖLÇÜLEMEDİ.
- K47 için aynı açık veriye 6. bakış: TUTTU çıksa bile keşif; kesin hüküm KASA körü.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt; HAYIR ya da boş = kos çalışmaz)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | CETVEL2 v2.2 konum eşleri (Ç217 satır dosyası: aynı giriş günü, aynı kova, en az 5 eş); ANA ölçü K20 TEMİZ eş (ES_ON_KAYIT; son 20 barda ham U1 durumu taşıyan eşler dışarıda); mekanik etki için zincir sırası 1 karşılaştırması; plasebo alt küme için koşulmuyor (yazılı) |
| K2 | geleceğe bakma | EVET | zincir sırası yalnız önceki olaylardan (i ve low_L2 <= t); t'ye kadar bilinen dip değerlerinden (Ç217 prefix denetimi 90 / 90); eşik sonuca bakmadan bu dosyada sabit |
| K3 | geçerli bar | EVET | Ç217 satır dosyası ge_hazir barlarından (H > L, V > 0) |
| K4 | tekilleştirme | EVET | Ç217 olayları: her L2 bir olay, aynı hissede en az 15 bar; bu iş yalnız alt küme alır |
| K5 | giriş fiyatı | EVET | R15 girişi t+1 açılış (Ç217 CETVEL2 v2.2) |
| K6 | veri birimi | EVET | oran ölçüleri (F65, R15, SIRA); satır dosyası sha denetimi |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler; dipteki olaylarda sonuç yukarı yanlı, raporda yazılır |
| K8 | örneklem ve dönem | EVET | iki dönem ayrı hücre, ABD + AVR karar; güç c2_hucre eğrisiyle; n < 30 ya da güç < 0,80 ÖLÇÜLEMEDİ; aynı açık veriye 6. bakış yazılı |
| K9 | ön kayıt | EVET | bu dosya commit edilmeden hesap yok; ik_kontrol_kapisi hesaptan önce çağrılır |
| K10 | ayrıştırma | UYGULANMAZ | haber / metin ayrıştırması yok; yalnız satır dosyası |
| K11 | yeniden üretim | EVET | betik önce Ç217 U1 ABD 2016-19 değerlerini yeniden üretir; üretmezse DUR |
| K12 | ifade | EVET | hüküm yalnız önceden yazılı kuralla; bilgi dilimlerinde hüküm yok; 'iz' sözü yalnız KASA körüyle |
| K13 | süreç | EVET | hesap yasak defter dosyalarını yazmaz; defter kaydı ayrı commit; push yok (izin yok) |
| K14 | boyut (gerçek para) | UYGULANMAZ | alım-satım önerisi yok; ölçüm |
