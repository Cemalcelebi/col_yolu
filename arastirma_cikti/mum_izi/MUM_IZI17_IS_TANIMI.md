# MUM_IZI EK 17 İŞ TANIMI — GÖZ ÖLÇÜMÜ ÜÇÜNCÜ BAKIŞ: hakem v4 setinin (set 6; 17 bölge) sonrası ve birleşik koşu (26 Kasım 2026)

Yazan: ana model. Cemal MUM_IZI14_ONAY_OLCEKLI'yi işaretledi (cemal_mum_izi14_onay.json, commit 0c6dfec): BENZİYOR 4 (haftalık 3, günlük 1), KISMEN 7 (haftalık 3, günlük 4), BENZEMİYOR 6 (haftalık 3, günlük 3). Onay eşiği (17'de 14 tam ✓) tutmadı: tespit GEÇERSİZ; bu ölçüm 'tespit = Cemal'in kendi etiketi' düzeniyle (MUM_IZI11 / 13 aynen) yapılır. Bu set, Cemal'in sonrasını GÖRMEDEN ve gerçek ölçeği (yüzde ekseni) GÖREREK işaretlediği ilk settir; set ayrıca dokuzuncu ölçütle ('düşüş net bitmiş, kopmuş') seçilmiştir.

## Kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, MUM_IZI_HAKEM.py, mühürlü MUM_IZI14_* dosyaları (yalnız okunur). `git add -A` / `commit -a` yasak; yalnız kendi yolların.
- Tanımlar MUM_IZI11_ON_KAYIT / MUM_IZI13_ON_KAYIT ile AYNEN (giriş = bölgeden sonraki ilk bar açılışı; ufuk 15 mum; stop = bölge dibi x 0,98; CETVEL2 konum eşi; tablolar; permütasyon). Veri <= 2022-12-31; penceresi kesiği aşan bölge 'ölçülemedi' (sayısı yazılır).
- Sayfa -> bölge eşlemesi mühürlü MUM_IZI14_onay_anahtar.json'dan ('yeni_sayfa'); etiket cemal_mum_izi14_onay.json'dan. Set 1-5 satırları değişmez (mum_izi13_olay.csv ile karşılaştırılır; fark varsa yazılır).
- Kod işi başında `python IZ_KARNE.py kontrol istanimi`; ön kayıt (MUM_IZI17_ON_KAYIT.md: kod sha, GETİRİSİZ SAYIM, KONTROL LİSTESİ) hesaptan ÖNCE commit; `IZ_KARNE.ik_kontrol_kapisi` geçmeden hesap başlamaz. Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.

## Tablolar (önceden; sonuçtan sonra değişmez)
- (i) ÜÇÜNCÜ BAKIŞ = yalnız set 6: Cemal sınıfı x zaman dilimi (n, R15 ortalama / medyan, eşli fark ortalama / medyan, artıda payı, eşinden iyi payı, +%5 / +%10 stop'tan önce payı). BENZİYOR hücreleri n 3 ve n 1: 'karşılaştırma yapılamaz / yalnız döküm' diye yazılır.
- (ii) HAKEMİN SEÇTİKLERİ (BİLGİ): set 6'nın 17 bölgesi Cemal'in işaretinden bağımsız, zaman dilimine göre: aynı ölçüler. Soru: dokuzuncu ölçütle seçilen bölgeler eşlerinden iyi gitti mi. Karşılaştırma satırı: set 5'in 24 bölgesi (hakem v3; dokuzuncu ölçütsüz) aynı ölçülerle.
- (iii) BİRLEŞİK = set 1-6 (145 bölge): MUM_IZI13 birleşik tablosunun aynısı (EVET / KISMEN / HAYIR x zaman; EVET - HAYIR eşli fark farkı, permütasyon). Soru: iki bakıştaki yön (haftalıkta BENZİYOR eşlerin gerisinde; günlükte fark yok) üçüncüyle değişti mi.
- OKUMA: bütün hücreler n < 30: etiket 'BİLGİ; ÖRNEKLEM YETERSİZ'. Eş sınırı (eşler bölgenin kendi koşusuyla eşlenmedi) raporda yazılır.

## Çıktılar
MUM_IZI_GOZ2.py'ye set 6 (çalışan kısma dokunmadan) + test; MUM_IZI17_ON_KAYIT.md, MUM_IZI17_RAPOR.md, mum_izi17_sonuc.json, mum_izi17_olay.csv (145 satır); MUM_IZI17_SONRASI.pdf (MUM_IZI13_SONRASI ile aynı düzen: kapakta özet tablo; set 6'nın 17 bölgesinin HEPSİ, sırayla BENZİYOR, KISMEN, BENZEMİYOR; her sayfada Cemal'in işareti, hisse, tarih, sonrası 30 mum, 15 mum getirisi, eş ortalaması; ayrıca bölgedeki gerçek mum boyu % ve olağana oranı (MUM_IZI14_onay_olcekli.json'daki değerler) ve sağda yüzde ekseni).
