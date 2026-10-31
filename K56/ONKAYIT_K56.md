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
