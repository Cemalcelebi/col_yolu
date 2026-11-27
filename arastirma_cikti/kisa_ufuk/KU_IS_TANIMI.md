# KISA_UFUK İŞ TANIMI — bugüne kadar bulunan bütün olay kümeleri 3 ve 5 mumluk ufukta: desenin etkisi 15 mumdan çok daha kısa mı (27 Kasım 2026)

Yazan: ana model (kendi girişimi; Cemal'in 'hâlâ görmediğin bir şeyler vardır' eleştirisi üzerine kör nokta taraması). Bugüne kadarki bütün ölçümler 15 mumluk ufukla yapıldı (Cemal'in 17 Kas kuralı: karar ölçüsü 15 bar). Aynı gün Cemal şunu da demişti: büyük kurumlar girince benzer yapılar oluşur ama 'en fazla 3-5 günlük oluşumlardır'. Mum deseni bir alış-satış izi taşıyorsa etkisi ilk birkaç mumda görülüp 15 mumda silinmiş olabilir. Bu iş YENİ olay aramaz; mevcut, mühürlü olay kümelerinin sonrasını 3 ve 5 mumda ölçer.

## 0. Kesin kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, mevcut modüller ve testleri (yalnız import / okuma). `git add -A` / `commit -a` yasak.
- KASA AÇILMAZ: veri <= 2022-12-31 (assert). Olay kümeleri AYNEN alınır (yeniden taranmaz, süzülmez, eşik değişmez); yalnız sonuç ufku değişir. Giriş her kümede kendi tanımındaki giriş (sonraki açılış ya da desenin giriş fiyatı).
- Yeni tek dosya KISA_UFUK.py (KURAL_MOTORU düzeni, hata yakalama, loglama, çakışma kapısı) + test_kisa_ufuk.py; çıktılar arastirma_cikti/kisa_ufuk/.
- Sıra: kod + test -> GETİRİSİZ SAYIM (küme x hücre olay sayıları; kaynak dosya sha'ları) -> ön kayıt KU_ON_KAYIT.md (kod sha, sayımlar, `python IZ_KARNE.py kontrol` tablosu) commit + push (kısa ufuk getirileri hesaplanmadan ÖNCE) -> `IZ_KARNE.ik_kontrol_kapisi` -> ölçüm -> rapor.
- Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.

## 1. Olay kümeleri (mevcut dosyalardan; günlük; ABD 2016-19, ABD 2020-22, AVR iki dönem)
- K1 WEB DESENLERİ: /root/.kasa/ham/web_desen/olay_*.pkl; 17 kol (yönleriyle).
- K2 DOJİ ÖBEĞİ (gövde <= %10): /root/.kasa/ham/doji_obek/olay_ANA_*.pkl; k = 2, 3, 4+ (yönsüz).
- K3 UÇLAR: /root/.kasa/ham/mum_izi27/olay27.pkl; her pencere evreni (E2), günlük; 12 ölçü + 4 bileşiğin UÇ10 bayrakları (yönsüz; beklenen yön Cemal'in kalıbına göre YUKARI).
- K4 KODUN SEÇTİĞİ BÖLGELER: arastirma_cikti/mum_izi/mum_izi24_olay.csv.gz; KAPILI ve KAPISIZ (günlük).
- K5 ESKİ ÇÖL PUANI: /root/.kasa/ham/col_skor6/pencere_*.pkl; PUAN_ESIT üst %10 (L = 20 ve 40; kesimler cs_kesim.json'dan) ve sol bacak düşüşü üst %2 (L = 40).
Bir küme dosyası okunamıyorsa o küme 'DOSYA YOK' diye raporlanır; yeniden üretilmez.

## 2. Ölçüler (H = 3 ve H = 5 bar; sabit)
- R_H = (giriş barı dahil H'inci geçerli barın kapanışı) / giriş - 1; yönlü kümelerde yönle çarpılır.
- TOPLAM FARK_H = R_H - T1_H; T1_H = aynı hissenin aynı dönemdeki bütün günlerinin (sonraki açılıştan) R_H ortalaması (yönlü kümelerde yönle çarpılmış haliyle).
- SEÇİM_H = R_H - o günün pazar ortalaması R_H (yönlü kümelerde yönle).
- ÖNCE HANGİSİ (H = 5): giriş sonrası 5 bar içinde +1 ATR mi -1 ATR mi önce görüldü (yönlü kümelerde desen yönü 'artı'); pay farkı ve aynı hissenin rastgele günlerindeki pay farkı (asimetri).
- İLK MUM: giriş barının kendi getirisi (açılıştan kapanışa), yönle; rastgele güne göre fark.
- Çıkarım: ay kümeli bootstrap %95 (10.000; tohum 2714); n, farklı ay. Aile = bütün küme kolları x 2 ufuk; BH q 0,10.
- MALİYET ÇİZGİSİ (bilgi; önceden): gidiş-dönüş %0,20; bunun altındaki ortalama fark 'işlenemez' diye işaretlenir.
- HÜKÜM (kol x ufuk; önceden): 'TUTAR' <=> ABD'nin iki döneminde de TOPLAM FARK_H > 0 ve ay kümeli alt ucu > 0 VE AVR'nin iki döneminde işaret artı (n >= 100 olanlarda) VE BH'yi geçer; ayrıca 'İŞLENEBİLİR' <=> iki dönemin ortalaması > %0,20. 'TERS' <=> iki dönemde üst ucu < 0 (yönsüz kümelerde 'EKSİ' diye okunur). 'TEK DÖNEM', 'TUTMADI', 'ÖLÇÜLEMEDİ' (n < 300 ya da farklı ay < 12).
- 15 barlık eski sonuç her satırın yanına karşılaştırma için yazılır (kaynak raporlardan).
- Evren bugün yaşayanlar.

## 3. Çıktılar
KISA_UFUK.py, test_kisa_ufuk.py; arastirma_cikti/kisa_ufuk/: KU_ON_KAYIT.md, KU_RAPOR.md (tablo: küme / kol | yön | H = 3: TOPLAM FARK iki dönem [aralık] | H = 5: aynı | önce hangisi asimetrisi | ilk mum | 15 bar eski sonuç | hüküm), ku_sonuc.json, ku_ozet.csv.
