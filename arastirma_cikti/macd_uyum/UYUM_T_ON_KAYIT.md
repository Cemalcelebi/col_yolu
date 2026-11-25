# MACD_UYUM — TOPLAM UYUMSUZLUK ÖN KAYIT (zincir tek uyumsuzluk; sonuçtan ÖNCE)

Kaynak: Cemal (25 Kas 08:31): 'birbirinden farklı olaylar şeklinde değil; daha derin diplerde MACD uyumsuzluğu da daha derin oluyor'.

## Tanım (değiştirilmez)
- Zincir = UYUM_Z_ON_KAYIT tanımı. Zincirin İLK dibi = zincirin ilk olayının L1'i.
- PFc = Low(L2, bu olay) / Low(L1, zincirin ilk olayı) − 1 (fiyat ilk dipten toplam ne kadar aşağıda).
- MRc = (MACD(L2, bu olay) − MACD(L1, ilk olay)) / |MACD(L1, ilk olay)| (MACD ilk dipten toplam ne kadar yukarıda). MACD değerleri her olayın kendi t penceresinden (F66m, F66, close_L2); uygulama yorumu: pencere farkı küçük kabul edildi.
- Zincir sırası 1 olan olayda PFc = F65, MRc = MR (kendi değeri).
- ANA: T = PFc <= -0,10 ∧ MRc >= 0,30 ('derin toplam uyumsuzluk'). Eşikler getirisiz seçildi: PFc alt çeyreğe, MRc üst çeyreğe yakın yuvarlak sayılar. KONTROL: Tz = T dışındaki U1 olayları.
- BİLGİ (doz): PFc dilimleri (> -0,05; -0,05..-0,10; -0,10..-0,20; <= -0,20) ve MRc dilimleri (< 0,10; 0,10..0,30; 0,30..0,50; >= 0,50); her karar hücresinde FARK'ın dilim sırasıyla Spearman'ı; dördünde de > 0 ise 'derinlikle artıyor'.

## Ölçüm
- es_satir.csv.gz (K20 temiz eş); C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum, plasebo hariç. Doğrulama: BARIZ ABD 2016-19 temiz n 502, FARK -0,16.
- Karar: AÇIK VERİDE TUTTU ⇔ 4 karar hücresinde T TUTAR VE (T − Tz) dördünde > 0. Gücü yeterli hücrede tutmuyorsa TUTMADI; hepsi güçsüzse ÖLÇÜLEMEDİ.
- K47 için aynı açık veriye 7. bakış: TUTTU çıksa bile keşif.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt; HAYIR ya da boş = kos çalışmaz)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | CETVEL2 v2.2 konum eşleri (Ç217 satır dosyası: aynı giriş günü, aynı kova, en az 5 eş); ANA ölçü K20 TEMİZ eş (ES_ON_KAYIT; son 20 barda ham U1 durumu taşıyan eşler dışarıda); mekanik etki için zincir sırası 1 karşılaştırması; plasebo alt küme için koşulmuyor (yazılı) |
| K2 | geleceğe bakma | EVET | PFc / MRc yalnız önceki ve bu olaydan (i ve low_L2 <= t); t'ye kadar bilinen dip değerlerinden (Ç217 prefix denetimi 90 / 90); eşik sonuca bakmadan bu dosyada sabit |
| K3 | geçerli bar | EVET | Ç217 satır dosyası ge_hazir barlarından (H > L, V > 0) |
| K4 | tekilleştirme | EVET | Ç217 olayları: her L2 bir olay, aynı hissede en az 15 bar; bu iş yalnız alt küme alır |
| K5 | giriş fiyatı | EVET | R15 girişi t+1 açılış (Ç217 CETVEL2 v2.2) |
| K6 | veri birimi | EVET | oran ölçüleri (F65, R15, SIRA); satır dosyası sha denetimi |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler; dipteki olaylarda sonuç yukarı yanlı, raporda yazılır |
| K8 | örneklem ve dönem | EVET | iki dönem ayrı hücre, ABD + AVR karar; güç c2_hucre eğrisiyle; n < 30 ya da güç < 0,80 ÖLÇÜLEMEDİ; aynı açık veriye 7. bakış yazılı |
| K9 | ön kayıt | EVET | bu dosya commit edilmeden hesap yok; ik_kontrol_kapisi hesaptan önce çağrılır |
| K10 | ayrıştırma | UYGULANMAZ | haber / metin ayrıştırması yok; yalnız satır dosyası |
| K11 | yeniden üretim | EVET | betik önce Ç217 U1 ABD 2016-19 değerlerini yeniden üretir; üretmezse DUR |
| K12 | ifade | EVET | hüküm yalnız önceden yazılı kuralla; bilgi dilimlerinde hüküm yok; 'iz' sözü yalnız KASA körüyle |
| K13 | süreç | EVET | hesap yasak defter dosyalarını yazmaz; defter kaydı ayrı commit; push yok (izin yok) |
| K14 | boyut (gerçek para) | UYGULANMAZ | alım-satım önerisi yok; ölçüm |
