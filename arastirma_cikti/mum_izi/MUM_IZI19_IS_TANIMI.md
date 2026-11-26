# MUM_IZI EK 19 İŞ TANIMI — GÖZ ÖLÇÜMÜ DÖRDÜNCÜ BAKIŞ: mum boyu kapılı setin (set 7; 12 bölge) sonrası ve birleşik koşu (26 Kasım 2026)

Yazan: ana model. Cemal MUM_IZI18_ONAY_OLCEKLI'yi işaretledi (cemal_mum_izi18_onay.json, commit 5068fa8): BENZİYOR 6 (günlük 5, haftalık 1; ikisine yıldız koydu), KISMEN 2 (günlük), BENZEMİYOR 4 (günlük). Onay eşiği (12'de 10 tam ✓) tutmadı: tespit GEÇERSİZ; bu ölçüm 'tespit = Cemal'in kendi etiketi' düzeniyle (MUM_IZI11 / 13 / 17 aynen) yapılır.

## Kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, MUM_IZI_HAKEM.py, test_mum_izi10.py (başka alt ajan çalışıyor), mühürlü MUM_IZI14_* / MUM_IZI18_* ve cemal_*.json (yalnız okunur). `git add -A` / `commit -a` yasak; yalnız kendi yolların.
- Tanımlar MUM_IZI11 / 13 / 17 ön kayıtlarıyla AYNEN. Veri <= 2022-12-31; penceresi kesiği aşan bölge 'ölçülemedi'. Sayfa -> bölge eşlemesi mühürlü MUM_IZI18_onay_anahtar.json ('yeni_sayfa'); etiket cemal_mum_izi18_onay.json. Set 1-6 satırları değişmez (mum_izi17_olay.csv ile karşılaştırılır).
- Kod işi başında `python IZ_KARNE.py kontrol istanimi`; ön kayıt (MUM_IZI19_ON_KAYIT.md: kod sha, GETİRİSİZ SAYIM, KONTROL LİSTESİ) hesaptan ÖNCE commit; `IZ_KARNE.ik_kontrol_kapisi` geçmeden hesap başlamaz. Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI. EK 17'de bildirilen kusur (yön etiketi satırında n >= 2 koruması eksik) bu işte düzeltilir (eski çıktılar değişmeden; test).

## Tablolar (önceden; sonuçtan sonra değişmez)
- (i) DÖRDÜNCÜ BAKIŞ = yalnız set 7: Cemal sınıfı x zaman (n, R15 ortalama / medyan, eşli fark ortalama / medyan, artıda payı, eşinden iyi payı, +%5 / +%10 stop'tan önce payı) + 12 bölgenin dökümü (yıldızlı iki bölge işaretli).
- (ii) KAPIDAN GEÇENLER (BİLGİ): set 7'nin 12 bölgesi Cemal'in işaretinden bağımsız: aynı ölçüler ('mumları belirgin küçük bölgeler eşlerinden iyi gitti mi').
- (iii) GERÇEK ÖLÇEKLE İŞARETLENENLER = set 6 + set 7 (29 bölge; Cemal sonrasını görmeden, yüzde eksenli sayfada işaretledi): Cemal sınıfı x zaman ve zaman dilimleri birlikte; BENZİYOR - BENZEMİYOR eşli fark farkı (permütasyon, tohum 19). Bu, bugüne kadarki en temiz örnek; n 29.
- (iv) BİRLEŞİK = set 1-7 (157 bölge): MUM_IZI17 birleşik tablosunun aynısı; ne değişti.
- OKUMA: bütün hücreler n < 30: etiket 'BİLGİ; ÖRNEKLEM YETERSİZ'. Eş sınırı raporda yazılır.

## Çıktılar
MUM_IZI_GOZ2.py'ye set 7 (çalışan kısma dokunmadan) + test; MUM_IZI19_ON_KAYIT.md, MUM_IZI19_RAPOR.md, mum_izi19_sonuc.json, mum_izi19_olay.csv (157 satır); MUM_IZI19_SONRASI.pdf (MUM_IZI17_SONRASI ile aynı düzen: kapakta özet tablo; 12 bölgenin hepsi sırayla BENZİYOR (yıldızlılar önce), KISMEN, BENZEMİYOR; her sayfada Cemal'in işareti, hisse, tarih, sonrası 30 mum, 15 mum getirisi, eş ortalaması, mum boyu % ve oran, yüzde ekseni).
