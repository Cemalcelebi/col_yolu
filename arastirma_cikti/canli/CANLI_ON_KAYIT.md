# CANLI_TARAMA — ön kayıt (kurallar; sonuç görülmeden)

DÜRÜSTLÜK: bu liste 'izleme / ileri test' listesidir, ÖNERİ DEĞİLDİR. CLAUDE.md öneri modülünün üç kapısından (tarama + dosya + risk) burada yalnız tarama kapısı var ve seçici ÖLÇÜLEMEDİ düzeyindedir (dipte + gövdeli kırılım KATKI+ ama hücre başına +3..+9 puan). Alım-satım kararı Cemal'indir; Claude yatırım danışmanı değildir.

- Zaman (UTC): 2026-11-20T06:12:49Z
- Sürüm: CANLI_TARAMA v1.0 (2026-11-20): S6 son 5 gün + havuz Ş1 VE Ş7 (kademeli) + puan7 sırası; ileri test olc (YAPI_HEDEF cetveli)
- CT_ESIK_SHA: `a43ec505618579ffe47e99defc1b404844738b9654fac6c61f8147df53958f32`
- YH_ESIK7_SHA (puan7 ayarları): `14f11dee1c6c96e976f60357771c7bb2b312ce91ad99cde691dad7dd2410ff26`
- İş tanımı: arastirma_cikti/yapi_hedef/CANLI_TARAMA_IS_TANIMI.md (commit 39a8d2f)

## Kurallar (CT_ESIK)

- **veri**: yfinance auto_adjust=True, son 400 takvim günü, 100'lük paket, threads; başarısızlar ikinci turda 20'lik pakette bir kez daha. Birleştirme: eski seri korunur, yeni barlar eklenir; ortak günlerde Close farkı > %1 olan gün sayısı uyarıdır ve ortak günlerde yeni veri esastır; ortak günlerin medyan oranı (yeni / eski) 1'den > %1 farklıysa (temettü / ayarlama kipi) eski kısmın O/H/L/C'si bu oranla ölçeklenir (tek fiyat kipi, K6); oran 1'den > %40 farklıysa (bölünme / birim: peni-sterlin) sembol ŞÜPHELİ. Yeni barlarda |günlük getiri| > %40 -> ŞÜPHELİ (listeden dışlanır). AVR yeni barlarda Kur = son bilinen Kur (ileri taşınır; yalnız likidite ölçüsü). Seans kapanmadan (pazar kapanış UTC saati + pay) gelen bugünkü bar atılır.
- **sinyal**: S6 AL (YAPI_HEDEF.yh_s6_hisse X1 = Y1) günü t; havuz t günündeki bilgiyle (OC 'gecmis' kipinin t+1 girişli hali): t'de geçerli bar, momentum C(t)/C(t-60) sonlu (kapanış en çok 5 gün ileri taşınır), likidite = C*V*Kur'un t dahil son 20 birleşik takvim günü medyanı (en az 10), aynı gün geçerli barı olan pazar hisseleri arasında alt %20 değil, [t-60, t] içinde bölünme şüphesi (OC.oc_bolunme_supheli) yok; aynı hissede havuzdan geçen AL günleri birleşik takvimde >= 60 gün arayla tekil (ilk tutulur). Liste: pazarın birleşik takviminin son 5 günündeki tekil AL günleri.
- **havuz**: Ş1 = F15 <= 0,25 VE F17 <= -0,20; Ş7 = F22 > 0 VE F22a < 0 (O_t < F21) VE F23 >= 0,50 (YAPI_HEDEF.yh_s7_sartlar, YH_ESIK Y10 eşikleri). Kademe 0: Ş1 VE Ş7. Bütün pazarlarda havuz boşsa kademe (i): Ş1 VE F22 > 0; o da boşsa (ii): Ş1. Kademe atlanmaz; raporda yazılır.
- **sira**: puan7 azalan; eşitlikte Ş9 (U dip) var önce; sonra F18 küçük (yol almamış). Pazar karışık, pazar başına en çok 5.
- **olcu**: stop0 = hat x 0,98; hedef fiyatları kapanışa göre (giriş = sonraki açılış varsayımı; gerçek ölçüm giriş açılışıyla); ileri test yh_olay_olc (YAPI_HEDEF 15 bar cetveli; eş aynı gün aynı OC kovası, en az 3); ölçüm tarihi = sinyal + 15 işlem günü (giriş t+1, 15. geçerli bar t+15)
- **model**: eğitim = YH.yh_veri7() satırlarından ölçülen (h5 ve es_h5 var) VE giriş <= 2026-08-31 olanlar; özellikler _YH_OZ7 (F1-F29, F22a dahil) + NaN bayrakları (YH_ESIK7['nan_bayrak']); NaN -> eğitim medyanı; puan7 = P(h5 = 1)
- **kriz**: canlı taramada 31.08.2026 kesiği bellekte geçici olarak kaldırılır (SY_ESIK / OC_ESIK / YH_ESIK 'kriz' -> 2100-01-01); dosyalar değişmez; fonksiyon çıkışında eski değer geri yazılır

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | liste ölçüm değildir; ileri test (olc) eşi YAPI_HEDEF yh_olay_olc ile aynı giriş günü, aynı OC momentum x likidite kovası, aynı d / hedef / takip / 15 bar; tek tek okunur, n < 30 iken 'örneklem yetersiz' |
| K2 | geleceğe bakma | EVET | S6 nedensel (yh_s6_hisse); özellikler yalnız [.., t] (önceki turların prefix denetimleri: F1-F29, F65-F68, mahkeme prefix kapısı); havuz t günündeki bilgiyle; model eğitimi giriş <= 31.08.2026 satırlarıyla, canlı sinyaller Ekim 2026 ve sonrası; test_canli_tarama prefix testi |
| K3 | geçerli bar | EVET | OC.oc_veri_hazirla / YH._yh_hazir geçerli bar (H > L, V > 0, O/H/L/C > 0); seans kapanmadan gelen bugünkü bar atılır |
| K4 | tekilleştirme | EVET | aynı hissede 60 birleşik takvim günü tekil (havuzdan geçen AL günleri); olc oc_olay_hazirla tekilleştirmesiyle |
| K5 | giriş fiyatı | EVET | liste hedefleri kapanışa göre (bilgi); ileri test girişi t+1 AÇILIŞI (yh_olay_olc E0 = Op[d]) |
| K6 | veri birimi | EVET | tek fiyat kipi: yfinance auto_adjust=True; ortak günlerde oran tek tipse eski kısım yeni kipe ölçeklenir; oran > %40 (bölünme / peni-sterlin) ve yeni barda /getiri/ > %40 ŞÜPHELİ, listeden dışlanır; AVR likidite EUR (Kur) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_*.pkl); batan yok; rapor ve ileri test sonucu yukarı yanlı okunur (her çıktıda yazılı) |
| K8 | örneklem ve dönem | EVET | liste 10 isim: bulgu değil; ileri test sonuçları birikimli, n < 30 'örneklem yetersiz', olaylar tek tek listelenir |
| K9 | ön kayıt | EVET | kurallar iş tanımında (commit 39a8d2f) ve CT_ESIK sha256'sı bu ön kayıtta, ilk taramadan önce commit; tara komutu ESIK sha'sını ve kontrol kapısını (IZ_KARNE.ik_kontrol_kapisi) denetler, tutmazsa DURUR |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV (yfinance) ve mühürlü özellik / olay dosyaları |
| K11 | yeniden üretim | EVET | json'da her adayın bütün sayıları; test_canli_tarama olc hesabını YAPI_HEDEF cetveliyle (yh_sim elle) yeniden üretir; puan7 matrisi YH._yh_matris7 ile eşit |
| K12 | ifade | EVET | çıktıların başında dürüstlük cümlesi (izleme, öneri değil); 'iz / emare' sözü yok; sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_ct; yasak defter dosyalarına, YAPI_HEDEF / GOZ_ETIKET / üretim zincirine dokunulmaz (yalnız import); e-posta / anahtar taraması (_ct_yaz); veri repoya girmez; push yok; kod değişti -> Colab'da çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | EVET | öneri değil; boyut / giriş / çıkış kuralı yazılmaz; gerçek para kararı için öneri modülü üç kapısı (dosya + risk) ayrıca gerekir; taban oran (3 yılda 10x ~%1) her çıktıda dürüstlük cümlesiyle |
