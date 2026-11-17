# İŞ TANIMI: YAPI_HEDEF sonuç PDF'i (Cemal'le birlikte değerlendirme; 17 Kas 2026)

## YASAKLAR
- IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, KURAL_DEFTERI_TASLAK.md, CEMAL_COL_KURALLARI.md dosyalarına DOKUNMA. YAPI_HEDEF.py'yi DEĞİŞTİRME (yalnız oku / çağır). `git add -A` yok, push yok. E-posta / anahtar yok.
- Sayıları sonuc.json ve olay_Y*.csv.gz'den al; yeniden hesaplama yapma, yeni ölçü üretme. Raporda 'iz / bulgu / kesin' dili yok; etiketler sonuc.json'daki gibi (ÖLÇÜLEMEDİ / DESTEKLENMEDİ / TUTAR).

## AMAÇ
Cemal (mobilden okur, grafik okur, alım kararını kendisi verir) bugünkü beş denemenin sonucunu görüp 'ne doğru ne yanlış' diye kodu değerlendirecek. PDF düz dille, Türkçe, kısa; her sayfa kendi başına anlaşılır. Kaynak: arastirma_cikti/yapi_hedef/RAPOR.md, sonuc.json, olay_Y1..Y5.csv.gz, ON_KAYIT.md; tanımlar CLAUDE.md 'YENİ TEST STANDARDI' ve arastirma_cikti/fitil_v2/KOR2_DERS_CEMAL.md. Veri: /tmp/veri (V_BIST / V_ABD / V_AVR; ORTAK_CETVEL.oc_veri ile).

## İÇERİK (sırayla)
1. KAPAK + TEK SAYFA ÖZET: yeni test standardı 4 satırla (giriş kırılım mumu, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş = aynı gün aynı kova); beş denemenin ne olduğu birer cümle; sonuç tablosu (deneme x karar hücresi: n, KAT5 [%95], etiket); bir cümle okuma: hiçbir karar hücresi tutmadı, Y3 hedefi de stopu da eşlerden sık görüyor (oynaklık), Y5 yalnız BIST bilgi hücresinde.
2. OLASILIK TABLOSU (Cemal'in biçimi): her deneme x hücre: P(+5) olay / eş / taban, P(+10), P(stop önce), KAT [%95]. Küçük puntoda tek-iki sayfa.
3. HER DENEME İÇİN BİR BÖLÜM (Y1..Y5): (a) tanım şeması: şematik çizim (mumsuz basit çizgi: yapı, kırılım mumu, hat / stop, +%5 / +%10 çizgileri); (b) o denemenin hücre satırları; (c) ÖRNEK GRAFİKLER: satır dosyasından rastgele (tohum 7) 3 'hedefe ulaşan' (h10 = 1 öncelikli, yoksa h5 = 1) + 3 'stop olan' (st5 = 1) olay, BIST ve ABD karışık; her grafik: sinyal öncesi 60 mum + giriş + sonraki 20 mum (SONRASI GÖSTERİLİR, kör set değil); hisse adı, pazar, tarih başlıkta; giriş günü dikey çizgi, hat / stop0 kesikli kırmızı, +%5 ve +%10 yeşil kesikli, gerçekleşen çıkış noktası işaretli; hacim altta; fiyat ekseni gerçek fiyat. Her grafiğin altında bir satır: 'kodun gördüğü: ...; sonuç: +%5 gün 3, +%10 gün 9 / stop gün 4'. Cemal'in değerlendirmesi için grafiğin altında boş satır 'Cemal: ____'.
4. BİRLİKTE DEĞERLENDİRME SAYFASI: kodun olası yanlışları (iş tanımındaki yazılı şüpheler: eşler oynaklıkla eşlenmedi; Y1 bölgeleri çok sık (hisse-yıl başına kaç bölge, sonuc.json / satır dosyasından say); Y3 kazan tanımı sayısal uyum; Y4 hafıza tanımı; Y5 tavan tanımı) ve Cemal'e 5 somut soru (örn. 'bu Y1 örneklerinde kodun çizdiği taban senin tabanın mı?', 'Y3'ün kazanı senin kazanın mı?', 'takip stopu kuralı böyle mi?', 'hedef +%5 kapanışla mı High ile mi sayılsın?', 'Y5 SAT mumu doğru mu?').
5. SON SAYFA: veri sınırları (hayatta kalma, komisyon yok, 31.08.2026 kesiği), ön kayıt / ölçüm commit'leri, güç notu (n 300-999 hücreleri ÖLÇÜLEMEDİ kalıyor), sıradaki 3 deneme (alt ajan raporundaki üç öneri: oynaklık kovası, Y5 n büyütme, Y1 + D4 dönüş).

## BİÇİM
- matplotlib + PdfPages (Türkçe karakterler DejaVu Sans ile), A4 yatay grafik sayfaları; tablolar matplotlib table ya da monospace metin; toplam 25-40 sayfa.
- Çıktı: arastirma_cikti/yapi_hedef/YAPI_HEDEF_SONUC_2026-11-17.pdf ve üreten betik yapi_hedef_pdf.py (arastirma_cikti/yapi_hedef/ altında; tek dosya, tohum sabit, hata yakalama). PDF < 8 MB.
- Commit (adlı dosyalar: pdf + betik), push yok. Raporunda: hangi örneklerin seçildiği (sembol, tarih, sonuç), sayfa sayısı, HATA başlığı (yoksa 'yok'), KONTROL LİSTESİ gerekmez (ölçüm yok) ama K12 ifade kuralına uyduğunu yaz.
