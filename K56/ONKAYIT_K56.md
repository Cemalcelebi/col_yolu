# K56 — K51-K55 ETKİ VE MEKANİZMA ARAŞTIRMASI: ÖN KAYIT (KİLİT)

Sürüm v1.0 — 30 Ekim 2026. Cemal'in "K51–K55 Etki ve Mekanizma Araştırması, Faz 0" talimatı. Bu belge mekanizma testlerinden ÖNCE commit'lenir;
sonuç görüldükten sonra eşik, tanım ya da sınıflama kuralı değiştirilmez. Değişiklik yalnız yeni sürüm eki + gerekçeyle (sonuç görülmeden) yapılır.

## 1. Amaç, sınır ve bağımsızlık
- Amaç yeni sinyal / gösterge değil: K51-K55'te ölçülen belirtilerin arkasındaki gerçek mekanizmayı (sermaye, şirket, yatırımcı davranışı ya da
  veri / yöntem eseri) bağımsız veriyle ayırmak. Bulgu başarısızsa başarısız kalır; neden bilinmiyorsa "bilinmiyor" yazılır.
- K51 İZ DEĞİL, K52 / K53 kararları, K54 sağlamlık kararı ve K55 Faz 1 İZ YOK DEĞİŞMEZ. K51-K55 kodu, ön kaydı, çıktısı DEĞİŞTİRİLMEZ;
  yalnız okunur. K56 ayrı paket (K56/), ayrı giriş (K56.py), ayrı çıktı (Drive COLAB_VERILER/OUTPUT/K56_MEKANIZMA; repoda
  arastirma_cikti/k56_mekanizma). Çıktı yolu denetimi K51-K55 klasörlerine yazmayı engeller (K56/ortak.cikti_dogrula).
- Yeniden kullanım kaydı: K51-K55 çıktılarının her okunuşu (dosya, sha256, amaç: envanter / hipotez üretimi / örneklem seçimi / veri / kıyas)
  K56_KAYNAK_KAYDI.csv'ye yazılır. K55 KEŞİF (2016-21) verisi K56 hipotezlerinin KAYNAĞIDIR: bu dönemde yapılan mekanizma testi
  "keşif verisi yeniden kullanımı" diye işaretlenir ve tek başına DOĞRULANMIŞ MEKANİZMA veremez.

## 2. Dönem politikası
- Dönem sınırları K55 ile aynı: KEŞİF 2016-01-01..2021-12-31, İÇ 2022-01-01..2023-12-31, BAĞIMSIZ 2024-01-01..2026-06-05; fon krizi
  kesimi 31.08.2026 (sonrası ölçülmez).
- K55'in İÇ ve BAĞIMSIZ dönemleri K55'te AÇILMADI. K56 bu dönemleri Cemal'in açık kararı olmadan açmaz. Karar verilene kadar K56 mekanizma
  testleri KEŞİF'te (yeniden kullanım işaretli) ve veri kaynağı yalnız sonraki dönemi kapsıyorsa (ör. FINRA açığa satış API'si) "KAPSAM
  DIŞI / KARAR BEKLİYOR" diye bekletilir.

## 3. Kanıt sınıfları (her bulgu ve her mekanizma için tek sınıf; kurallar sırayla uygulanır)
1. YANLIŞ BULGU: etki bir eserdir. Ölçüt (biri yeter): (a) sentetik sıfır sınamasında (bilgisiz yapay veri, aynı tanım + aynı kod) gerçek
   etkinin >= %50'si aynı işaretle yeniden üretilir (bölüm 6); (b) etki, veri hatası / kurumsal işlem düzeltmesi / evren hatası düzeltilince
   aralığı sıfırı kapsayacak kadar küçülür; (c) etki kaynak tabloda yoktur ya da yanlış aktarılmıştır.
2. VERİ YETERSİZ: gerekli bağımsız veri yok, ücretli ve alınmadı, ya da olayların < %60'ı veriyle eşleşir, ya da n < 30.
3. DOĞRULANMIŞ MEKANİZMA: (a) bağımsız veri (fiyat / hacim dışı: 13F, Form 4, SEC finansal / olay kayıtları, FINRA / SEC işlem
   istatistikleri) önceden yazılı tahmini olay grubunda ve eşleşmiş karşıt grupta ayrı ayrı gösterir; olay − karşıt farkının ay kümeli %95
   aralığı sıfırı dışlar; (b) mekanizma değişkeni denetlenince asıl etki >= %50 küçülür (aracılık payı, bootstrap aralığıyla); (c) yarışan
   hipotezlerin önceden yazılı tahminleri tutmaz; (d) KEŞİF DIŞI en az bir dönemde (İÇ ya da BAĞIMSIZ; Cemal'in kararıyla açılmışsa)
   tekrarlanır; (e) yanlış pozitif oranı (mekanizma var ama yükseliş yok) ve karşıt örnek grupları raporlanır.
4. GÜÇLÜ AÇIKLAMA: 3(a)-(c) tutar ama yalnız KEŞİF'te (yeniden kullanım) ya da aracılık payı %25-%50.
5. ALTERNATİF AÇIKLAMA: veri tahminle uyumlu ama yarışan en az bir hipotezin tahminiyle de uyumlu (ayırt etmiyor) ya da aracılık < %25 ama
   aralığı sıfırı dışlıyor.
6. İLİŞKİ VAR, NEDEN BELİRSİZ: asıl etki sağlam (yanlış bulgu değil) ama sınanan hiçbir mekanizma 3-5'i karşılamıyor.
- Kasıtlı yanıltma: üç sütun ayrı yazılır — gözlenen davranış (fiyat / hacim), olası mekanizma, KASIT KANITI. Kasıt kanıtı yalnız bağımsız
  resmî kayıttır (SEC işlem askıya alma, SEC / DOJ dava ya da idari karar, mahkeme kararı, FINRA disiplin kararı) ve sembol + tarih eşleşmesi
  ister. Fiyat grafiği, hacim göstergesi ya da "manipülasyona benziyor" kanıt sayılmaz; kayıt yoksa sınıf "KASIT KANITI YOK" olur.

## 4. Hipotez kaydı kuralı
- Her mekanizma hipotezi (K56/mekanizma.py HIPOTEZLER) veriden önce şunlarla yazılır: hangi bulguları açıklar, doğruysa bağımsız veride ne
  görülmeli, yanlışsa ne görülmeli, gerekli veri kaynağı, karşıt grup, ölçü, çürütme eşiği, öncelik. Kayıt v1.1 ekiyle kilitlenir (Faz 1'den önce).
- Aynı bulgu için en az üç yarışan açıklama (mekanik / veri açıklaması dahil) yazılır. Fiyat yükselişi otomatik "birikim", düşüş + yüksek
  hacim otomatik "dağıtım" sayılmaz.
- Yeni hipotez, yeni veri ve yeni test ayrı ayrı kaydedilir (K56_HIPOTEZLER.csv sürüm sütunu; IZ_KARNE Ç satırı).

## 5. Karşıt örnekler (her mekanizma testinde zorunlu)
- G1 olay (büyük yükseliş, K55 tanımı), G2 aynı belirtiyi gösteren ama yükselmeyen (aynı gün, oynaklık ondalığı, likidite üçlüsü, sektör,
  belirti beşte biri eşleşmiş), G3 sonradan iflas / tasfiye (K54 sınıf 2), G4 büyük düşüş (60 günde −%30), G5 hisse sayısı yılda > %20 artan,
  G6 birleşme / satın alma (K54 sınıf 3), G7 sektör × likidite eşli rastgele.
- Raporlanan: n (olay, hisse), mekanizmanın gruplardaki sıklığı, yanlış pozitif oranı = P(yükseliş yok | mekanizma var), kesinlik, etki
  büyüklüğü, ay kümeli %95 aralık. Yalnız başarılı örneklerde görülen mekanizma kabul edilmez.

## 6. M01 olay başlangıcı seçim etkisi: sentetik sıfır sınaması (yöntem kalibrasyonu)
- Gerekçe: K55 olay günü t0 = ileri pencerenin +%30'u (Y60) İLK yakaladığı gün; giriş t0+1 açılışı. Etiket giriş fiyatına göre tanımlandığı
  için t0 öncesi düşüş tanım gereği seçilir. K55'in 25 KEŞİF'inin 19'u bu yönde (ters yönlü).
- Tasarım: dört yapay evren (gauss tohum 561 / 562, garch_t tohum 563 / 564), her biri 400 hisse × 1.600 işlem günü, sıfır beklenen getiri,
  beta × piyasa + 11 sektör + özel bileşen, gece / gün içi ayrımı, fitil, |getiri| ile ilişkili hacim (geleceğe bilgisiz). K55 olay tanımı
  (K55/olay_tanimlari.sembol_olaylari), K55 hücre değişkenleri (K55/dal*.py; her hücrenin K55 en iyi varyantı), K55 A ölçüsü (gün ×
  oynaklık ondalığı z; K55/hucre._z_gun_vd; ay kümeli bootstrap 400) AYNEN kullanılır. Ufuk Y60 birincil; Y120 / Y250 bilgi. Gecikme
  0 / 1 / 5 / 20 gün (değişken t0−k'da).
- Sınıf (spek başına, Y60, gecikme 0): |d_sentetik| < 0,05 ya da sentetik aralık 0'ı kapsıyor -> MEKANİK İZ YOK; oran = d_sentetik /
  d_gerçek >= 0,50 -> MEKANİK AÇIKLAR; 0,20-0,50 -> KISMEN MEKANİK; oran < 0 -> TERS İŞARET. Hücre kararı: dört spekin en az üçü aynı
  sınıf, yoksa BELİRSİZ. MEKANİK AÇIKLAR olan K55 bulgusu bölüm 3-1(a) gereği YANLIŞ BULGU (eser) sınıfına adaydır; kesin sınıf için
  gerçek veride gecikme sınaması (Faz 1: aynı hücreler t0−k'da) gerekir.
- AÇIKLAMA (dürüstlük): eşikler K56/mekanizma.py'de bu sürümden önce yazıldı; kod sınaması için 80 hisse × 900 gün, tek spek (gauss 11),
  4 hücreli bir DUMAN denemesi koşuldu ve sonucu görüldü (D01-S02, D01-S07, D05-S01, D06-S01'de sentetik d gerçek d kadar ya da büyük).
  Tam sınama (yukarıdaki dört spek, 400 hisse, bütün hücreler) bu kilitten sonra koşulur; duman denemesi karar vermez.

## 7. Faz 0 veri erişim testi kuralları
- Küçük örneklem (en çok 12 sembol; G1 / G2 / G3 / G5 / G6 temsilcileri). Tek dosya en çok 64 MB; zip'ler mümkünse HTTP Range ile yalnız
  içerik listesi okunur. Ham indirmeler önbelleğe (repo dışı) gider, repoya KONMAZ.
- SEC: User-Agent'taki iletişim e-postası yalnız SEC_EPOSTA ortam değişkeninden; saniyede < 7 istek. Tiingo kotası korunur (Faz 0'da Tiingo
  isteği yok). Ücretli kaynağa istek yok; yalnız belge / fiyat bilgisi.
- Erişim testi hiçbir hipotezi sınamaz; yalnız kapsam, gecikme, eşleşme oranı, alan dolu payı ölçer.
