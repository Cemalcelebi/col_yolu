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

## v1.0-a (30 Ekim 2026, tam sentetik koşudan sonra; eşik ve tasarım DEĞİŞMEDİ)
- Hata düzeltmesi: yapay panelde K55 panelinin 'dv20' sütunu yoktu; kesitsel D02-S10 hücresi (REDDEDİLDİ) hesaplanamadı (TANIMSIZ). Sütun
  eklendi ve yalnız bu hücre aynı dört spekle yeniden koşuldu; öteki 62 hücrenin sonuçları değişmedi (aynı kod yolu).

## v1.1 (30 Ekim 2026; Faz 0 sonuçları ve bağımsız denetim GÖRÜLDÜKTEN SONRA, Faz 1'den ÖNCE; gerekçeli ek — v1.0 eşikleri değişmedi)
Gerekçe: dört bağımsız denetçi (sentetik geçerlilik, envanter doğruluğu, veri kaynakları, ön kayıt / aşırı iddia) Faz 0 çıktılarında sınıflama ve
özet katmanında aşırı iddia, ön kayıtta iç çelişki ve birkaç olgusal hata buldu. Aşağıdakiler bu yüzden eklendi; hepsi sonuç görüldükten sonra
yazıldığı için "v1.1 (sonuç sonrası)" diye işaretlidir ve Faz 1 testlerinden ÖNCE kilitlenir.
1. **3-1(a) ile 6. bölümün uzlaştırılması**: sentetik sıfır sınaması TEK BAŞINA yalnız "YANLIŞ BULGU ADAYI (M01)" verir. Kesin YANLIŞ BULGU
   için ayrıca gerçek veride SEÇİMSİZ KONTROL gerekir (aşağıda 2). v1.0'daki "biri yeter" ifadesi sentetik ölçüt için geçersizdir.
2. **M01 Faz 1 doğrulama protokolü** (KEŞİF verisi, yeniden kullanım işaretli): her K55 KEŞİF hücresinde KEŞİF ölçütünü geçen HER (varyant, ufuk)
   satırı için gerçek veride üç d: (i) K55 ilk geçiş etiketi, (ii) seçimsiz etiket = pencere eşiği aşan BÜTÜN nitelikli günler, (iii) her
   epizotta rastgele bir nitelikli gün (tohum 56). Sınıf: |d(ii)| <= 0,2 × |d(i)| ya da d(ii) aralığı 0'ı kapsıyor VE sentetik oran (aynı
   varyant, ufuk) >= 0,5 -> MEKANİK (kesin YANLIŞ BULGU); 0,2 < |d(ii)| / |d(i)| < 0,5 -> KISMEN MEKANİK (kalan etki ayrı bulgu, İLİŞKİ VAR
   adayı); >= 0,5 ve aralık 0'ı dışlıyor -> GERÇEK ETKİ KALIYOR. Gecikme (t0−k) ölçüsü yalnız bilgi; Y250'de mekanik eser k ile sönmediği için
   karar ölçütü değildir. Sentetik kalibrasyon genişletilir: gerçek panele eşlenmiş oynaklık düzeyi (yıllık ~%30), GJR kaldıraç ve sıçrama
   spekleri; olay oranı raporlanır.
3. **Sentetik sınama kapsamı**: v1.0 her hücrede K55'in seçtiği varyantı (en küçük p'de ilk satır = en kısa pencere) ve Y60'ı kullandı. Ek
   sınama: KEŞİF ölçütünü geçen bütün (varyant, ufuk) satırları aynı dört spek ve aynı eşiklerle; karar "KEŞİF ufkunda" ayrıca raporlanır.
   Y60 kararı (21 / 25) birincil kalır, KEŞİF ufku kararı yanına yazılır.
4. **Ek etiketler ve mekanik ön sınıf kuralı** (Faz 0 envanteri): ETKİ YOK (kaynakta BASARISIZ), ETKİ SAĞLAM DEĞİL (kaynak kararı DESTEKLENMİYOR /
   TUTMAZ / İZ DEĞİL / TERS YÖN / ÖLÇÜLEMEDİ / GEÇERSİZ içeriyor ve DESTEKLENİYOR içermiyor; küçük, ters ya da dönem çelişkili etkiler),
   BETİMLEYİCİ (kaynakta karar yok: bilgi / denetçi notu), YÖNTEM DENETİMİ (ölçüm hattı, evren, veri denetimi; sonuca göre seçilmiş alt kümeler,
   ör. 'en iyi 20 çıkarıldı'). İLİŞKİ VAR, NEDEN BELİRSİZ yalnız kaynak kararı DESTEKLENİYOR / KEŞİF olan ve YANLIŞ BULGU ADAYI olmayan
   bulgulara verilir. ALTERNATİF AÇIKLAMA yalnız hesaplanmış vekil (|ρ| > 0,8) ya da bulguya özel gerekçeli atama ile.
5. **Kasıt kanıtı daraltıldı**: kasıt kanıtı yalnız KESİNLEŞMİŞ karardır (mahkeme kararı, SEC / FINRA idari karar ya da uzlaşma). SEC işlem
   askıya alması (en çok 10 günlük, bilgi doğruluğu kuşkusu) ve dava bülteni (iddia duyurusu) "RESMÎ KUŞKU KAYDI" diye ayrı sütunda tutulur,
   kasıt kanıtı sayılmaz. Ad eşlemesi tarih şartlıdır (askıya alma günü CIK'in ilk başvurusundan sonra ve adın geçerli olduğu aralıkta; birden çok
   CIK'e düşen ad belirsiz).
6. **Hipotez kaydı v1.1 donduruldu**: K56/mekanizma.py HIPOTEZLER (sürüm alanı "v1.1"); Faz 0'da bilinen sayılar tahmin sütunundan ayrılıp
   "on_kanit" alanına taşındı; bu sayılar test sayılmaz (M19'un K52 zamanlama payı 0,504 bilinen sonuçtur, M19 yeni dönem verisiyle sınanır).
   Hipotez kaydının sha256'sı Faz 1 koşu kimliğine yazılır; Faz 1'de değişiklik = yeni sürüm.
7. **Erişim örneklemi sapması**: v1.0 G5 temsilcisi istedi; G5 ayrı seçilmedi, örneklem içinde companyfacts hisse sayısıyla belirlendi (bölünme /
   birleşme düzeltmesiz, ham). Eşleşme oranları olay çeyreğindeki dosyayla ölçülür; durum GECTI yalnız uygun sembollerin >= %60'ı eşleşirse.
8. **Denetçilerin ön kayıt dışı kontrolleri** (sentetik denetçi, K55 tam paneli, KEŞİF): seçimsiz etiketle gerçek d -0,016 .. -0,049 (Y60; ilk geçiş
   d'nin ~%5-11'i), t0 günü kapanış < 0 payı gerçek 0,743 / sentetik 0,736. Bunlar bilgi olarak raporlanır; resmî sınıf 2'deki protokolle verilir.

## v1.2 (31 Ekim 2026; Cemal'in Faz 1 kararları — üç ayrı çalışma; HİÇBİR koşudan önce commit'lenir)
Cemal: (1) ilk üç yerel analiz başlasın, yeni veri indirilmesin, haber / birleşme bilgisi geçmişe dönük sızıntı üretmesin; (2) İÇ 2022-23 açılabilir,
yalnız önceden belirlenmiş hipotez ve değişkenlerle; BAĞIMSIZ 2024-26 kapalı, açılmadan önce kod / hipotez / eşik / veri tanımı / ön kayıt hash ile
sabitlenir; K55 dönem sınırları değişmez; (3) Tiingo Kasım kotasıyla batan şirketler yeni evren sürümüne eklenir; (4) üç çalışma ayrı rapor, veri
sürümü ve kimlik taşır; başarısız sonuçlar korunur, eski sonuçların üzerine yazılmaz.

### A. Faz 1 yerel analizler (çalışma kimliği K56-F1A; KEŞİF 2016-21, keşif verisi yeniden kullanımı işaretli; indirme YOK)
- Girdiler: K55 Faz 0 tam evren paneli ve olay tablosu (evren sürümü 0d00d2c97608), K55 hücre tanımları (K55/dal*.py, degisken_hesapla), yerel SEC
  başvuru özeti (islenmis-veri k55/sec_ozet.json), V_ABD / K34 / Tiingo fiyatları (K55 ile aynı), endeks.pkl.
- Satırlar: K55'te KEŞİF ölçütünü geçen 125 (hücre, varyant, ufuk) satırı (K56/mekanizma.kesif_satirlari). Başka satır, varyant, pencere yok.
**A1 seçimsiz kontrol (M01, v1.1-2'nin uygulaması):**
- Nitelikli gün (ufuk h, eşik e): likit gün ve C[t+h] / O[t+1] − 1 >= e, pencere tam (K55/olay_tanimlari.ileri_getiri, seri_erken = False).
- Etiketler: (i) K55 olay tablosu (ilk geçiş); (ii) bütün nitelikli günler; (iii) her K55 olayı için t0'dan başlayan kesintisiz nitelikli likit gün
  dizisinden tek tip rastgele bir gün (tohum: sha256(hücre|varyant|ufuk|56)). Olay olmayan: (i) ve (iii)'te etiketsiz bütün satırlar (K55 gibi), (ii)'de
  nitelikli olmayan satırlar.
- Ölçü K55 A ile aynı: likit, donem{h} == KESIF, x tanımlı; z gün × vd (K55/hucre._z_gun_vd); Cohen d; ay kümeli bootstrap 2.000; AUC.
- Karar tablosu (satır): r = d(ii) / d(i) (aynı işaret için; ters işaret ayrı). (a) d(ii) aralığı 0'ı kapsıyor ya da 0 <= r <= 0,2 -> MEKANİK. Faz 0
  sentetik oranı (4 spek, aynı varyant + ufuk) >= 0,5 ise "MEKANİK (gerçek + sentetik)", < 0,5 ise "MEKANİK (gerçek veri; sentetik DGP yeniden
  üretmiyor)" — iki durum da kesin YANLIŞ BULGU (v1.1-2 bu ikinci durumu tanımsız bırakmıştı; seçimsiz kontrol seçimi doğrudan kaldıran sınamadır,
  sentetik oran kalibrasyondur). (b) 0,2 < r < 0,5 ve aralık 0'ı dışlıyor -> KISMEN MEKANİK (kalan etki d(ii)). (c) r >= 0,5 ve aralık 0'ı dışlıyor
  -> GERÇEK ETKİ KALIYOR. (d) d(ii) ters işaretli ve aralık 0'ı dışlıyor -> TERS KALINTI. (iii) duyarlılık olarak raporlanır; (ii) ile sınıfı farklıysa
  işaretlenir. Hücre sınıfı: KEŞİF satırlarının çoğunluğu; eşitlikte BELİRSİZ.
- Kalibre sentetik spekler (v1.1-2; duyarlılık, karar ölçütü değil): kalibre_gjr (yıllık oynaklık medyanı 0,30, GJR-GARCH α 0,05 γ 0,08 β 0,90,
  t(4)), kalibre_sicrama (aynı + günde %0,5 olasılıkla N(0, 5σ) sıçrama); 400 hisse × 1.600 gün; aynı 125 satırda oran ve olay oranı.
**A2 kalan etki denetimi (M03 / M16 / M18):** yalnız A1'de (b), (c) ya da (d) çıkan satırlarda, (ii) etiketiyle:
- M03a z gün × oynaklık yüzdeliği (50 kova); M03b z gün × vd × kısa oynaklık oranı üçlüsü (vol20 / vol60). M16a 2020-02-15..2020-06-30 dışlama;
  M16b z gün × vd × beta üçlüsü (250 gün, SPY). M18 z gün × sektör (grup >= 5; değilse gün içi).
- Küçülme = 1 − |d_denetim| / |d(ii)|: >= %50 AÇIKLAR (KEŞİF yeniden kullanımı: en çok GÜÇLÜ AÇIKLAMA adayı), %25-50 KISMEN, < %25 AÇIKLAMAZ.
**A3 haber ve birleşme bileşimi (M04 / M15):**
- G1 = K55 olayları (ufuk başına, KEŞİF). G7 = olay başına 5 eş: aynı gün, aynı sektör (bilinmiyorsa şartsız), aynı likidite üçlüsü, |vd farkı| <= 1,
  likit, pencere tanımlı, ±h gün içinde aynı ufukta olayı olmayan; tohum 56.
- ÖNCESİ (sızıntısız; yalnız t0'da bilinen): başvuru tarihi ∈ [t0−20, t0−1] (sec_ozet'te saat yok: t0 günü başvurusu ÖNCESİ'ye GİRMEZ): herhangi 8-K,
  8-K 2.02, hisse ihracı (S-1, S-3, S-3ASR, 424B1 / 4 / 5, 8-K 3.02), SC 13D / 13G (/A dahil).
- SONRASI (AÇIKLAYICI bileşim; öngörü ya da özellik DEĞİL, hiçbir sinyalde kullanılmaz): [t0+1, t0+10] 8-K 2.02; 8-K 1.01 / 7.01 / 8.01;
  [t0+1, t0+h] birleşme (SC TO-T, SC TO-I, SC 14D9, DEFM14A, 425, S-4, 8-K 2.01); hisse ihracı (yükselişe satış).
- Ölçü: pay(G1) − pay(G7), ay kümeli bootstrap %95. Destek: SONRASI farkının alt ucu > 0. Ayrıştırma (açıklayıcı): SONRASI haberi ya da birleşmesi
  olan olaylar çıkarılınca (ii) etiketli d.
- Sızıntı kapısı: ÖNCESİ'de kullanılan her başvuru tarihi <= t0 − 1 gün (kod denetimi + test); SONRASI sütunları ayrı tabloda ve 'aciklayici' adıyla.

### B. İÇ DOĞRULAMA (çalışma kimliği K56-IC; 2022-01-01..2023-12-31; K55 dönem ve purge / embargo etiketleri aynen)
- Yalnız önceden belirlenmiş olanlar sınanır: (B1) 125 KEŞİF satırı K55 A yöntemiyle (ilk geçiş); İÇ GEÇTİ = KEŞİF ile aynı işaret, |d| >= 0,20, ay
  kümeli %95 aralık 0'ı dışlar, AUC >= 0,56 ya da <= 0,44, 2022 ve 2023'te işaret aynı (n >= 10 olan yıllarda), İÇ ailesinde (125 satır) BH q <= 0,10.
  Hücre KEŞİF satırlarının çoğunluğu geçerse K55 durumu "DOĞRULAMA BEKLİYOR (A, ilk geçiş)". (B2) aynı satırlarda A1 seçimsiz kontrol (aynı karar
  tablosu); gerçek etki için belirleyici olan budur. (B3) K55 B yöntemi (eşleşmiş ileri, K55 eşikleri, yön kayıttan) 64 KEŞİF varyantında. (B4) A3
  bileşimi İÇ olaylarında; A2 yalnız B2'de kalan etki çıkan satırlarda.
- İÇ sonucuna göre yeni eşik, değişken, varyant, pencere türetilmez; sonuç yalnız durum etiketini değiştirir.
- BAĞIMSIZ (2024-01-01..2026-06-05) KAPALI: kod kapısı (K56/ortak.donem_kapisi) BAGIMSIZ etiketli satır ya da penceresi 2023-12-31'i aşan İÇ satırı
  kullanılırsa durur. Açılış ancak: Cemal kararı + K56_BAGIMSIZ_KILIT.json (kod dosyaları, ONKAYIT, hipotez kaydı, eşik sözlüğü, veri tanımları:
  evren sürümü, panel ve olay tablosu sha256) açılış anında yeniden hesaplanıp birebir eşleşir + K56_BAGIMSIZ_AC=1. Açılış tarihi ve commit
  K56_BAGIMSIZ_ACILIS.csv'ye. Kilit dosyası bu çalışmanın sonunda üretilir; üretmek dönemi açmaz.

### C. Batan şirketlerle yeni evren sürümü (çalışma kimliği K56-EVREN2; K51-K55 evren ve sonuçları DEĞİŞMEZ)
- Aday listesi (sonuç görmeden): Ö1 = K34 geçerli batan listesinden (SEC kapak sayfası eski kodu olan) Tiingo örnekleminde olmayanlar. Ö2 = KEŞİF dönemi
  (2016-01..2021-12) borsadan çıkanlar: SEC EDGAR tam metin aramasında 25-NSE başvuruları (görünen adda sembol olan), Tiingo listesinde aynı sembolün
  bitişi 25-NSE tarihinin ±45 günü içinde, assetType Stock, borsa NYSE / NASDAQ / NYSE MKT, seri >= 320 işlem günü, K55 evreninde olmayan; tohum 56
  ile rastgele, kota kalanı kadar (Ö1 + Ö2 <= 490, 10 yedek). Ö1 neden yetmez: K34 listesi SEC finansal veri setlerinden (2021+) geldiği için
  çoğu 2021-26'da çıkmış; KEŞİF dönemindeki hayatta kalma boşluğunu Ö2 kapatmaya çalışır.
- Tiingo yalnız Kasım kotasıyla (1 Kasım 2026'dan önce fiyat isteği yok); saatte en çok 45 istek; kaldığı yerden sürer; kota / 429 hatasında durur.
- Sınıflandırma: SEC başvuru geçmişi (Ö1 / Ö2 için data.sec.gov submissions, e-posta yalnız SEC_EPOSTA) + Tiingo listesi; K54 kuralı (COL_YOLU_ABD
  cy_v15_sinifla, içe aktarılarak, değiştirilmeden) + K56 alt ayrımı: İFLAS (8-K 1.03), TASFİYE (1.03 yok; ad LIQUIDAT / WIND DOWN / DISSOLUTION ya
  da varlık satışı 8-K 2.01 + birleşme belgesi yok + kayıt dışı 15-12), BİRLEŞME (sınıf 3), SEMBOL DEĞİŞİKLİĞİ (sınıf 4a / 4b), VERİ SAĞLAYICISI
  KAYBOLMASI (sınıf 5), DOĞRULANAMAYAN (sınıf 6).
- Getiri (asıl): seri bitince pencere TANIMSIZ; son işlem fiyatı tasfiye ödemesi sayılmaz; eksik delist getirisi uydurulmaz. Duyarlılık (ayrı etiketli):
  iflas −%100, birleşme son kapanış.
- Rapor: aday / indirilen / eksik sayıları, kaynak (Ö1 / Ö2), sınıf dağılımı, tarihsel kapsam, veri eksikleri. Etki (yeni evrende aynı kodla): olay
  sayıları dönem × ufuk; 125 KEŞİF satırının ilk geçiş ve seçimsiz d'si (KEŞİF ve İÇ; BAĞIMSIZ kapalı); eski / yeni farkı.

### v1.2-a (31 Ekim 2026, fiyat isteği ve sonuç görülmeden): Ö2 aday tanımı düzeltmesi (sapma kaydı)
- Bulgu (tanılama, fiyat yok): EFTS görünen adlarındaki sembol SEC'in GÜNCEL sembol tablosundan gelir; borsadan tamamen çıkan şirketin sembolü
  çoğunlukla yoktur. 2016-21 25-NSE'lerinin 652 sembollü satırından Tiingo'da eşleşen 432'nin bitiş − 25-NSE farkı medyan 2.376 gün: çoğu halen
  işlem gören şirketlerin başka menkul kıymetlerini (tahvil, imtiyazlı pay, borsa değişimi) çıkaran 25-NSE'ler. v1.2 Ö2 tanımı yalnız 3 aday verir.
- Yeni Ö2 tanımı: Tiingo listesinden assetType Stock, borsa NYSE / NASDAQ / NYSE MKT / AMEX, sembol 1-5 harf (imtiyazlı / varant / birim dışı), bitiş
  2016-01-01..2021-12-31, seri >= 465 takvim günü, aynı sembolün bitişten SONRA başlayan Tiingo satırı yok (sembol sonradan yeniden kullanılmamış;
  aksi hâlde Tiingo kod sorgusu yeni şirketin serisini döndürür), K55 evreninde ve Ö1'de olmayan; tohum 56 ile rastgele, kota kalanı kadar.
- CIK bağlama (indirmeden sonra, sabit kural): Tiingo meta adı (aynı sembol, kota sayısını artırmaz) normalize edilir (büyük harf, noktalama ve
  INC / CORP / CO / LTD / PLC / HOLDINGS / GROUP / LP / LLC / THE gibi ekler atılır); 25-NSE başvurularında (2015-11..2022-02) tarihi Tiingo
  bitişinin ±45 günü içinde ve normalize adı birebir aynı TEK CIK bağlanır; yoksa aynı pencerede EFTS sembolü Tiingo sembolüne eşit tek CIK; yoksa CIK
  BAĞLANAMADI -> sınıf DOĞRULANAMAYAN (K54 sınıf 6). K55 evren kuralı aynen uygulanır (K55/evren.evren_insa: sınıf 6 ve K54 tutarsızları evren dışı);
  bağlanamayanlar raporda ayrı sayılır (aynı gün düzeltme: ilk yazımdaki "fiyatı yine evrene girer" K55 kuralıyla çelişiyordu; sonuç görülmeden).
- Evren v2 inşası: K55 evren_insa / panel_kur / olaylar AYNEN, girdiye yeni seriler eklenerek (Tiingo düzeltilmiş OHLCV, COL_YOLU_ABD K34 okuma
  biçimi, _cy_temizle, >= 320 gün). Yeni şirketlerde seri_erken = False: pencere seri sonunu aşarsa TANIMSIZ (asıl). Sektör: SEC SIC bölümü (K34 ile
  aynı tablo), CIK yoksa 'bilinmiyor'. Duyarlılık (ayrı etiketli): yeni şirketlerde İFLAS -> d100 (−%100), BİRLEŞME -> d0 (son kapanış), diğerleri
  TANIMSIZ. K55 şirketlerinin seri sonu kuralı değişmez.
- İndirme sonrası seri denetimi (Ö1 ve Ö2): indirilen serinin son günü Tiingo listesindeki bitişten 10 iş gününden çok sapıyorsa "TIINGO SERİSİ
  UYUŞMADI" (sembol yeniden kullanımı ya da sağlayıcı hatası), evrene alınmaz, sayılır. Ö1'de 21 sembolün Tiingo'da birden çok satırı var (K34 kuralı
  değiştirilmedi; denetim bunları yakalar).
- Değişmeyenler: Ö1, kota (<= 490), saatlik 45 istek, Kasım başlangıcı, sınıflandırma kuralı, getiri kuralı (TANIMSIZ asıl), etki ölçümü.

### v1.2-b (31 Ekim 2026): bağımsız kod denetimi sonrası düzeltmeler (sapma kaydı)
KEŞİF / İÇ ilk koşusu (commit 6cf01ae, çıktılar faz1_yerel/kosu1_6cf01ae ve ic_dogrulama/kosu1_6cf01ae, silinmedi) görüldükten sonra yapıldı;
düzeltmeler sonuç sınıfına göre değil, önceden yazılı kuralın uygulanmasına göredir. Eşik, değişken, satır değişmedi.
1. Dönem sızıntısı: G7 eş elemesinde (±h içinde olayı olan eş) yalnız penceresi dönem sonunda ya da önce biten olaylar kullanılır; (iii) ve tanı
   dizisi dönem içinde kesilir. İlk kodda İÇ eş elemesi penceresi 2024'e taşan olayları (Y250'de 397) kullanıyordu: BAĞIMSIZ fiyatına dolaylı bağlılık.
2. SONRASI penceresi (gün(t0), gün(t0+k)]: t0'dan sonraki her başvuru (hafta sonu dahil), ayrıştırma dizileriyle aynı tanım. Birleşme / ihraç form
   listelerinde /A değişiklikleri aynı tür sayılır. ÖNCESİ değişmedi (t0 hariç).
3. BAĞIMSIZ kilidi: kod sha'sına bütün K55 modülleri, COL_YOLU_ABD.py, FON_IZI.py; veri tanımı (panel ve olay sha256, K55 evren sürümü) açılış anında
   dosyalardan yeniden hesaplanır (ilk kodda saklanan değer geri veriliyordu). Kirli kod denetimi aynı kapsamda.
4. Her koşu kendi klasörüne (<alt>/<kimlik>/) yazar, <alt>/SON.json geçerli koşuyu gösterir; EVREN2 kıyası SON.json'dan, yoksa durur.
5. EVREN2 (fiyat görülmeden, indirme öncesi): adi hisse olmayan menkul kıymetler (SPAC birimi / varant / hak: Tiingo -U, -WS, -R ya da NASDAQ 5. harf
   U / W / R) Ö1 ve Ö2'den, sembolü K55 evreninde başka şirkete ait Ö1 adayları indirilmez (K56_EVREN2_O1_DISLANAN.csv); boşalan kota Ö2'ye.
   CIK tekrarı (K55'te ya da yeni semboller arasında) evrene eklenmez. Ön denetim: her aday denenmeden, kota durumunda, SEC özeti eksikken ya da
   CIK'i olup SEC geçmişi olmayan adayda evren kurulmaz. Olay karşılaştırmasında K55 şirketlerinin olay değişimi ayrı sütun (likit eşiği ve
   sıralar kesitsel olduğu için yeni seriler K55 şirketlerini de etkiler). Yeni şirketin evren başlangıcı seri başı (K34'teki ilk nakit bildirimi
   şartı K34 sorusuna özgüydü; v2 genel evrendir).

### Genel
- Üç çalışma ayrı kimlik (K56-F1A-…, K56-IC-…, K56-EVREN2-…), ayrı alt klasör (faz1_yerel/, ic_dogrulama/, evren_v2/), ayrı rapor. Faz 0 çıktıları
  değiştirilmez; başarısız sonuçlar silinmez.

## v1.3 (31 Ekim 2026; Cemal'in BAĞIMSIZ dönem kararı — 9 madde; BAĞIMSIZ açılmadan, kilit üretilmeden ÖNCE commit'lenir)
Gerekçe ve kaynak: Cemal'in 31 Ekim kararı (BAĞIMSIZ 2024-26 yalnız mevcut ön kayıtlı testler için açılır; önce kod sabitlenir, ön kayıt yeniden üretilir,
kod / veri / evren / ayar hash'leri kaydedilir, kilit yeniden oluşturulur, İÇ'te dolaylı erişim olmadığı doğrulanır; BAĞIMSIZ'da yeni keşif / eşik / gösterge /
geriye dönük hipotez ayarı yok; ayrışma özel incelenir; 125 satır + B bir kez; EVREN2 adayları ayrı ayrı doğrulanır; eski sonuçlar değişmez; nihai K55
kararı, kurtarma yok). Tasarım dört bağımsız uzman raporu ve bir eleştirmenle yapıldı (iş akışı wf_9abc0e52); uzmanlar yalnız yapay veride küçük
koşular yaptı (ayrışma, T1 sentetik) ve BAĞIMSIZ olay sayılarını gördü (K55 Faz 0 raporunda zaten yayımlı); BAĞIMSIZ değişken / sonuç ilişkisi görülmedi.

### D. BAĞIMSIZ açılışı (çalışma kimliği K56-BAG; açılış adı K55_125_B; BİR KEZ)
- Testler yalnız v1.2-B'dekiler, ölçütler İÇ ile AYNEN (yeni eşik yok): B1 = 125 KEŞİF satırı K55 A (ilk geçiş): KEŞİF işaretiyle aynı, |d| >= 0,20, ay
  kümeli 2.000 bootstrap %95 aralığı 0'ı dışlar, |AUC − 0,5| >= 0,06, olay >= 10 ve olay dışı >= 10 olan BÜTÜN takvim yıllarında (kısmi yıl dahil) işaret
  KEŞİF'le aynı ve en az bir yıl, BH q <= 0,10 (aile = BAĞIMSIZ'daki 125 satır, ölçülemeyen p = 1). Hücre: satır çoğunluğu geçerse "BAĞIMSIZ'DA TEKRARLADI
  (A, ilk geçiş)", değilse "BAĞIMSIZ'DA TUTMADI". B2 = seçimsiz kontrol (v1.2-A karar tablosu aynen; gerçek etki için belirleyici). B3 = K55 B (yontem_B
  aynen; donem60; yön kayıttan; n >= 30, fark >= 0,05, alt uçlar > 0, net > 0, slot >= 0,90). B4 = bileşim (A3 kuralları; sec_var kuralı aynen) + A2
  (M16a COVID penceresi BAĞIMSIZ'da UYGULANAMAZ).
- Dönem etiketi (asıl): K55 kod etiketleri AYNEN (donem{h} = BAGIMSIZ: t0 ve pencere sonu 2024-01-15..2026-06-05; embargo 14 takvim günü). Gerekçe: K55
  sonuçları bu etiketlerle üretildi, v1.2-B "aynen" dedi, Cemal Faz 1 kararlarında (31 Ekim, madde 2) "mevcut K55 dönem sınırları geriye dönük
  değiştirilmesin" dedi. Bilinen çelişki K55 ön kaydının kendi içinde: v1.2-1 (pencere sonu dönem dışı -> PURGE; kod bunu uygular) ile v1.2-2
  ("2026-06-06..08-31 yalnız sonuç penceresi"); K55 sonuçları değişmez, çelişki sapma olarak kaydedilir.
- Duyarlılık (aynı tek açılışta, ayrı etiketli "DUYARLILIK-B"; karar tablosunda rolü yok): K55 ön kaydı v1.2-2 tanımı (BAGIMSIZ_B: t0
  2024-01-15..2026-06-05 ve pencere sonu <= 2026-08-31; olaylar da aynı kuralla). B1 / B2 / B3 aynı kodla. Koşu parametreleri: sinir yok, b3 = True.
- Ayrışma (E), PBO / DSR (F), açıklayıcı tanı sütunları ve EVREN2 BAĞIMSIZ'da KOŞULMAZ (yalnız mevcut testler). (iii) v1.2-A'nın mevcut duyarlılığı
  olarak hesaplanır, karar vermez. (iii) seçimsiz bir kontrol DEĞİLDİR: sıfır etkili yapay veride d(iii) ≈ d(i) (tasarım uzmanı ve eleştirmen yapay
  sınamaları); KEŞİF / İÇ'teki "(iii) GERÇEK ETKİ KALIYOR" etiketleri gerçek etki kanıtı sayılmaz. B3 kayıt yönüyle okunur; işareti çevrilerek
  (karşı uç) okunmaz.
- 125 satır listesi ve KEŞİF d'leri sha'lı ek: K56/ONKAYIT_K56_SATIRLAR.csv (sha256 f53683abc0d6...); kod sha'sına girer.
- Bir kez: açılış kaydı (K56_BAGIMSIZ_ACILIS.csv) hesaptan ÖNCE BAŞLADI satırıyla yazılır, commit + push edilir (push olmazsa hesap başlamaz); dönem kapısı
  BAĞIMSIZ için açık BAŞLADI kaydı + eşleşen kimlik ister; duman sınaması (sinir) BAĞIMSIZ'da reddedilir. Sonuç dosyaları yazılınca TAMAMLANDI (sonuç
  sha'larıyla) commit + push. Çökme: ÇÖKTÜ kaydı; koşu klasöründe sonuç dosyası yoksa gerekçeyle bir yeniden deneme; sonuç dosyası oluşmuşsa yeniden koşu
  yok. Rapor yalnız kaydedilmiş CSV'lerden üretilir.
- Kilit (kilit_uret komutu; açılış kaydı boşken): temiz git ağacı + etiket (K56-BAG-KILIT-<tarih>) + tam commit; kod sha (K56/*, K56.py, K55/*.py, K55.py,
  K55/ONKAYIT_K55.md, COL_YOLU_ABD.py, FON_IZI.py); ön kayıt sha (bu sürüm); hipotez sha; eşikler (K56 M, F1 ESIKLER, AYR, K55 AYARLAR, HUCRELER dökümü,
  CY, CY_V15); veri: panel dosya + içerik sha, olay tablosu sha, K55 evren sürümü, veri_sha (V_ABD, K34, Tiingo, endeks, sektör, K54) ve ek veri (sec_ozet,
  evren_disi, K55_VARYANTLAR, K55_EVREN, k35_sic, K56_SECIM_SENTETIK_KESIF); kıyas tabanı (F1A ve IC SON koşu kimlikleri + çıktı sha'ları); ortam
  (python / numpy / pandas, zorunlu). Açılışta hepsi yeniden hesaplanır; biri tutmazsa DonemKapali.

### E. Ayrışma incelemesi (çalışma kimliği K56-AYR; KEŞİF, İÇ ve yapay veri; Cemal madde 4)
- Tanımlar K56/ayrisma.py başlığındaki gibi: olay dizisi (dönem içinde kesik), u = z − c (c: aynı gün × vd grubunda dizi dışı satırların z ortalaması, grup
  < 5 ise gün içi), f_e (dizinin geçerli günlerinde u ortalaması), E1 olay ağırlıklı, E2 gün ağırlıklı, G = s (E1 − E2), s = KEŞİF d(i) işareti; kimlik
  E1 − E2 = −Cov(L, f) / ortalama L (1e-9 sınaması). Konum bantları 1 / 2-5 / 6-20 / 21+; uzunluk katmanları aynı; L dağılımı; gün eşit ağırlık; (iii)
  200 çekiliş (tohum 56-255) ortalaması = E1 sınaması. Kümeli bootstrap 2.000, bütün istatistikler aynı çekilişten: birincil ay(t0), ikinci sembol|yıl(t0);
  bilgi: olay, blok60.
- Yapay veri: dört Faz 0 spek (gauss 561 / 562, garch_t 563 / 564; karar) + kalibre_gjr 565, kalibre_sicrama 566 (duyarlılık); 400 hisse × 1.600 gün;
  aynı 125 satır; sentetik_sinif(G_s, aralık, G_gerçek) ve SPEK_UYUM 3 (mevcut sabitler 0,50 / 0,20 / 0,05).
- Etiket: bu protokol KEŞİF / İÇ'teki (iii) ve tanı sonuçları GÖRÜLDÜKTEN SONRA tasarlandı; betimleyicidir. Yeni karar kuralları (e2 ≈ 0 için 0,20 oranı,
  bantlar, katman n >= 30, çoğunluk) bu çalışmaya özgüdür, K55 kararına girmez. "isaret" = KEŞİF d(i) işareti (±1).
- Satır kararı (sırayla): f geçerli olay < 30 -> VERİ YETERSİZ; G'nin ay, sembol|yıl ya da blok60 aralıklarından biri 0'ı kapsıyor ya da G < 0,05 -> AYRIŞMA YOK; yapay
  çoğunluk MEKANIK_ACIKLAR -> "MEKANİK (yapay veri üretiyor)", KISMEN_MEKANIK -> "KISMEN MEKANİK" (ikisinde de E2 ≈ 0 ise başa "AĞIRLIK ETKİSİ +"; E2 ≈ 0 =
  E2 aralığı 0'ı kapsıyor ya da |E2| <= 0,20 |E1|); yapay sınıf yok / ters -> E2 ≈ 0 ise "AĞIRLIK ETKİSİ (gerçek veriye özgü, öngörü değil)", değilse
  "AÇIKLANMADI"; dört spekten üçü aynı değilse "BELİRSİZ (yapay)". Hücre: KEŞİF satırlarının çoğunluğu (dönem başına).
- Öngörü sorusunun ölçüsü (ii)'dir (bir günün nitelikli olacağını önceden bilmek; E1 / (iii) / (i) geleceğe bağlı ağırlık taşır); K55 B onun getiri biçimidir.
  Ayrışma sonucu hiçbir satırı "gerçek etki"ye çevirmez; K55 kararına girmez. Beyan: tasarım sırasında küçük yapay koşular görüldü (yalnız yapay veri).

### F. PBO / Deflated Sharpe (çalışma kimliği K56-PBO; K55 ön kaydı §7 "DOĞRULAMA BEKLİYOR adayları için PBO ve DSR"; yalnız KEŞİF + İÇ, açılıştan önce)
- Yapı başına (64 KEŞİF varyantı) aylık seri: K55 B seçimi (gün içi sıra >= 0,80 ya da <= 0,20; örtüşmez 60 gün), eşleşmiş net fark (r60 − maliyet − eş
  ortalaması, K55 eslestir k = 5), t0 ayı ortalaması; dönem donem60 ∈ {KEŞİF, İÇ}. Yön: asıl = KEŞİF A işareti (adayın keşfedilen yönü); bilgi = kayıt
  yönü. PBO = CSCV (COL_YOLU_ABD.cy_pbo, 16 blok, aylık), DSR = cy_dsr (en iyi IS yapı, N = 64 deneme). K51 H8 ölçütü aynen: PBO < 0,5 ve DSR >= 0,95 ->
  "aşırı uyum riski düşük"; değilse "aşırı uyum riski yüksek". Karar vermez; BAĞIMSIZ'da koşulmaz.

### G. İÇ → BAĞIMSIZ dolaylı erişim sınaması (çalışma kimliği K56-SIZ; açılıştan önce; K56/sizinti_denetimi.py)
- T0: K55 evren / panel / olay baştan kurulur; kilitli panel ve olay tablosuyla eşit olmalı. T1: aynı evren, fiyat / endeks / SEC özeti 2023-12-31'de
  kesik; İÇ motoru (B3 dahil): S, H, B3 TAM EŞİT (tolerans 0, NaN = NaN, süre hariç); bileşim tam başvuru özetiyle (T1a) eşit, kesik özetle (T1b) farkı
  kaydedilir (sec_var). Bir fark çıkarsa açıklanana kadar K56-IC geçersiz ve BAĞIMSIZ açılmaz; kilit yalnız T1 PASS iken üretilir. Meşru farklar
  (karşılaştırılmayan): panel indeks numaraları, panel bilgi sayıları, evren sürüm metni, penceresi kesimi aşan satırların PURGE -> TANIMSIZ etiketi.
  T2a: evren de kesik veriden (>= 320 gün, ALIVE_SINIR kesimden bir ay önce); T2b: ayrıca kesimden sonra evrene giren K34 sembolleri dışarıda; T1b'ye karşı
  fark "evren tasarımı etkisi" olarak raporlanır (ihlal değil): ihmal edilebilir = sınıf değişmez, en büyük d farkı <= 0,05 ve satır d farkı o satırın
  aralık yarı genişliğinin %25'ini aşmaz. Ek beyan: ilk İÇ koşusundaki sızıntı (6cf01ae) görüldü ve düzeltildi. Görünmeyen sınırlamalar beyan edilir: hayatta kalma (evren 2026'da işlem görenler + K34),
  2026 sürümü bölünme / temettü düzeltmesi, güncel sektör / CIK etiketleri; K51-K54 ABD 2024-26'yı test dönemi olarak kullandığı için BAĞIMSIZ araştırma
  programına göre görülmüş bir dönemdir (K55 hipotezlerine göre görülmemiş).

### H. K55 nihai karar eşlemesi (sonuç görülmeden; Cemal madde 9)
- Bugün: B2 GERÇEK ETKİ KEŞİF 0 / 125, İÇ 0 / 125; K55 B KEŞİF 0 TUTAR, İÇ 0 / 64.
- BAĞIMSIZ B2 hücre çoğunluğu MEKANİK -> "K55 NİHAİ: İZ YOK — ters yönlü farklar olay tanımının seçim eseri (üç dönemde)".
- Bazı satırlar GERÇEK ETKİ / KISMEN MEKANİK / TERS KALINTI ama hücre çoğunluğu değil -> aynı karar; satırlar raporlanır. KISMEN MEKANİK ve TERS
  KALINTI hiçbir durumda iz sayılmaz (kalan küçük etki ya da ters yönlü kalıntı; KEŞİF'te 2 / 7, İÇ'te 10 / 3 satır).
- Bir hücrenin çoğunluğu GERÇEK ETKİ KALIYOR -> İZ YOK korunur + "TEK DÖNEM SAPMASI" notu (KEŞİF ve İÇ'te seçimsiz etki yok; tek dönem tekrar sayılmaz;
  yeni hipotez ancak ayrı ön kayıtla ve K55 dışı veride).
- B1 geçerse destek sayılmaz ("seçim etkisi tekrarladı"; İÇ'te B1 119 / 125, B2 0). B3 TUTAR çıkarsa "tek dönemde tuttu: İZ DEĞİL" (yeni eşik aranmaz).
  BAĞIMSIZ ölçülemezse KEŞİF + İÇ'e göre İZ YOK. Ayrışma, PBO / DSR, duyarlılık pencere tanımı ve EVREN2 kararı değiştirmez. Üst sınır: Avrupa olmadan
  en fazla ABD-ADAY (CLAUDE.md); DOĞRULANDI için K55 ön kaydına göre AVR şart.

### I. EVREN2 v1.3 (fiyat görülmeden; 1 Kasım indirmesinden önce)
- İndirme öncesi sembol kuralları (Ö1 ve Ö2): NASDAQ / OTC 5 harf ve 5. harf G H I L M N O P R T U W X Z -> DIŞI; NYSE grubunda 5 harf ve son harf Q değil ->
  DIŞI; -U / -WS / -R -> DIŞI; 5. harf F / Y -> İŞARET; aynı sembolün aday bitişinden 14 günden fazla sonra biten başka Tiingo satırı -> DIŞI (API yeni varlığı
  döndürür) — istisna: aday bitişinden en çok 10 iş günü sonra başlayan devam satırı (aynı şirketin OTC devamı) -> İŞARET, seri sonu = devam satırının
  bitişi; 2015 başlangıçlı indirmede beklenen işlem günü < 320 -> DIŞI. Ö2 boşalanları aynı tohum-56 sırasının devamıyla doldurulur.
- İki aşama: (1) bütün adaylar için Tiingo meta; (2) fiyatsız doğrulama: meta başlangıç / bitişi liste satırından > 10 iş günü sapıyorsa DIŞI; ad / açıklama
  kuralı (WARRANT, RIGHT, PREFERRED, PFD, NOTE, DEBENTURE, BOND, SENIOR, SUBORDINATED, CUMULATIVE, PERPETUAL, CONTINGENT VALUE, CVR, ETF, ETN, EXCHANGE
  TRADED, % -> DIŞI; UNIT -> DIŞI, COMMON UNITS / LP -> İŞARET; DEPOSITARY -> DIŞI, AMERICAN DEPOSITARY -> İŞARET; TRUST / FUND / BDC ve açıklamada fon /
  boş çek -> İŞARET); Ö2 CIK: ad + tarih, sembol + tarih, ikinci kademe tek CIK Jaccard >= 0,80 ve ikinci en iyi < 0,50 ("benzer ad" işareti), yoksa sınıf 6;
  kimlik: Tiingo adı ile SEC adı / eski adları UYUMLU (birebir) / YAKIN (Jaccard >= 0,50 ya da oran >= 0,85; işaret) / UYUMSUZ (Ö1'de DIŞI); SEC kapsamı:
  listeli adayda son dönemsel rapor seri sonundan > 400 gün önce -> DIŞI (OTC'de işaret); ön ek: seri başı ilk SEC başvurusundan > 400 gün önce (ilk başvuru
  >= 2003) -> DIŞI; SPAC (SIC 6770 ya da ad) ve OTC -> İŞARET; ön sınıf. (3) yalnız DIŞI olmayanların fiyatı (divCash, splitFactor dahil).
- Fiyat aşaması: seri sonu Tiingo bitişinden > 10 iş günü sapıyorsa DIŞI (v1.2-a); temizlik sonrası < 320 gün DIŞI; K55 veri_kalitesi işaretleri,
  düzeltilmiş / ham oranı ve bölünme / temettü sayıları İŞARET; son işlem: listeli grupta en yakın çıkış belgesi (25-NSE, 15-12B / G, 15-15D, 8-K 2.01 /
  3.01) ±10 gün TUTARLI, ±45 YAKIN, değilse UYUMSUZ (işaret); OTC grubunda belge T+10'dan önce ve T, son 15-12 / dönemsel rapordan en çok 180 gün sonra
  ise TUTARLI, değilse "OTC KUYRUĞU" (işaret); ön / son sınıf çapraz tablosu (değişim işaret; son sınıf 6 / tutarsız K55 kuralıyla dışarıda). Getiriye
  dayalı dışlama yok. Aday doğrulama tablosu (K56_EVREN2_DOGRULAMA.csv) ve sha'sı evren sürümüne girer.
- Duyarlılık: işaretli alt kümeler (SPAC, OTC, ADR / yabancı, YAKIN kimlik, OTC kuyruğu) hariç ikinci evren; KEŞİF ve İÇ etkisi ayrı tabloda.
- EVREN2 BAĞIMSIZ'da KOŞULMAZ (v1.2-C aynen: etki KEŞİF ve İÇ'te; BAĞIMSIZ bir kez açılır — ikinci açılış Cemal'in 1. ve 5. maddesiyle çelişir).
  EVREN2 kodu kilide girer; açılıştan sonra yapılan EVREN2 düzeltmeleri BAĞIMSIZ sonucunu etkilemez.

### v1.3-a (31 Ekim 2026; çok merceğli kod incelemesi sonrası; BAĞIMSIZ açılmadan, EVREN2 fiyatı görülmeden)
İnceleme (iş akışı wf_36227bae; dört mercek + çekişmeli doğrulama) bulgularıyla eklenen / netleşen kurallar. Eşik değişmedi; yeni kurallar yalnız uygulama ve
güvenlik içindir.
1. Bir kez kuralı (kod): açılışta atomik kilit dosyası (K56_BAGIMSIZ.lock) + BAŞLADI satırında süreç kimliği ve makine; kapı yalnız o süreç ya da çocukları için
   açılır. Önceki denemede sonuç dosyası oluştuysa (K56BAG_* ya da ÇÖKTÜ notunda "SONUÇ DOSYASI OLUŞTU") gerekçe olsa da yeniden koşu YOK; en çok bir
   gerekçeli yeniden deneme. BAŞLADI / TAMAMLANDI commit'i ve push'u doğrulanır (uzak dal yeni commit'i göstermeli). Asıl sonuçlar ve K55 nihai kararı
   DUYARLILIK-B'den önce commit + push edilir; B ayrı denemede koşar, çökmesi asıl sonucu geçersiz kılmaz (not olarak yazılır).
2. Kilit: panel / olay yolu ve A ayarları (veri, k55, abd, cikti) kilitte; açılışta birebir. Etiket push edilemezse kilit yok; kilit dosyası commit'li ve
   değişmemiş olmalı. Kilit yalnız şu koşullarda üretilir: sızıntı sınaması PASS (T0 panel + olay eşit, T1b S / H / B3, T1a bileşim, T1 ayrışma İÇ ve T1
   PBO / DSR birebir) ve o PASS aynı veri tanımıyla (panel, içerik, olay, veri, ek veri sha'ları, evren sürümü), aynı İÇ referansıyla, temiz ağaçta alınmış;
   ayrışma (E) ve PBO / DSR (F) koşuları kilit commit'iyle aynı kodla ve temiz ağaçta alınmış; 125 satır eki birebir; ek veri dosyası "YOK" ya da eşik
   "okunamadı" ise kilit yok. Kıyas tabanı: F1A, IC, AYR, PBO SON koşuları ve çıktı sha'ları.
3. Sızıntı T2 ihmal edilebilir = sınıf değişmez VE en büyük d farkı <= 0,05 VE hiçbir satırda d farkı o satırın aralık yarı genişliğinin %25'ini aşmaz;
   karşılaştırmada tek tarafta olan sütun fark sayılır.
4. Ayrışma: hücre kararı "AĞIRLIK ETKİSİ + " öneki atılmış ana sınıfın çoğunluğu (önek sayısı ayrı sütun); "ayrışma var" için ay, sembol|yıl ve blok60
   aralıklarının üçü de 0'ı dışlamalı (blok60 karar kümesindedir; v1.3-E'deki "bilgi" ifadesi bu ekle düzeltildi); yapay spek çoğunluğu TANIMSIZ ise
   "VERİ YETERSİZ (yapay)"; kimlik farkı > 1e-9 ise "HESAP HATASI (kimlik)". Bilgi sütunları: örtüşen olay sayısı, çift sayılan gün payı, zincir kümesiyle
   (örtüşen diziler tek küme) G aralığı. Kesilme nedeni dönem dışı etiketli günün getirisini okumaz. İlk ayrışma koşusu (3b61627) geçersiz (sızıntılı
   kesilme etiketi, bozuk JSON), saklandı.
5. PBO / DSR bilgi sütunları: en iyi yapının aylık serisinde gecikme 1 / 2 otokorelasyonu ve etkin T (her üç aydan biri) ile DSR (seriler örtüşen 60 günlük
   getirilerden kurulu; ön kayıtlı K51 hesabı aynen, karar vermez).
6. K55 nihai karar eşlemesi (v1.3-H) netleştirme: "seçim eseri" gerekçesi yalnız BAĞIMSIZ hücre çoğunluğu MEKANİK iken; değilse karar yine İZ YOK, gerekçe
   çoğunluk sınıfıyla adlandırılır (KISMEN MEKANİK / TERS KALINTI / BELİRSİZ / TANIMSIZ). Raporlarda (iii) için sabit uyarı: seçimsiz kontrol değildir.
7. EVREN2 (fiyat görülmeden): meta'sı olmayan ya da okunamayan Ö1 adayı DIŞI (kimlik doğrulanamadı; Cemal madde 6); kimlik UYUMSUZ Ö1 ve Ö2'de DIŞI; OTC
   devamı istisnası yalnız devam satırı OTC borsasında ve bugün işlem görmüyorsa (aksi DIŞI: MPU); listeli adayda dönemsel rapor hiç yoksa DIŞI (OTC'de
   işaret); OTC tespiti "OTC devamı" işaretini de sayar; OTC son işlem kuralında dayanak yalnız T'ye kadar olan 15-12 / dönemsel rapor, çıkış belgesine
   8-K 1.03 dahil; LP adı ayrıca işaret; duyarlılık dışı işaretler: SPAC, OTC, ADR / 5. harf F-Y, kimlik YAKIN, OTC kuyruğu, CIK benzer adla, LP, meta
   yok. Geçici ağ hataları koşu içinde en çok 3 kez denenir; ön denetim geçici hata ya da kota durumunda evren kurmaz. EVREN2 raporlarında BAĞIMSIZ /
   PURGE / EMBARGO olay sayıları ve 2024 sonrası gün sayıları yer almaz (kapı dışı hesap yok). Fiyat denetimi tablosunun sha'sı evren sürümüne girer.
8. Prova: BAĞIMSIZ koşusunun kod yolu (rapor, nihai karar, JSON, ikinci koşu) İÇ verisinde küçük ölçekte prova edilir (bagimsiz_prova; karar vermez).
9. Drive kopyası (drive_kopyala) yalnız Colab'da Drive bağlıyken çalışır; bu kapta Drive bağlayıcısıyla (CLAUDE.md yöntemi) yapılır.
