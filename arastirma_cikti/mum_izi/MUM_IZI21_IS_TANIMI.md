# MUM_IZI EK 21 İŞ TANIMI — GÖZ ÖLÇÜMÜ BEŞİNCİ BAKIŞ: katmanlı setin (set 8; 24 bölge) sonrası, kapıdan geçenler, gerçek ölçekle işaretlenenler, birleşik (26 Kasım 2026)

Yazan: ana model. Cemal MUM_IZI20_ONAY_OLCEKLI'yi işaretledi (cemal_mum_izi20_onay.json, commit fa7de71; sözü: 'Burda eğer mumlar gerçekten küçük kabul ederek işaretledim'): BENZİYOR 7, KISMEN 7 (biri iki kutu işaretli: ana sınıf KISMEN, duyarlılıkta EVET), BENZEMİYOR 9, işaretsiz 1 (karar dışı). Ön kayıtlı tespit sayımı (Ç247; getirisiz, yapıldı): H1 hakem KISMEN 12'de 4 ✓, hakem BENZEMİYOR 11'de 3 ✓ (tam ✓'de fark yok; ✓ + K: 9 / 12'ye 5 / 11); H2 oran <= 0,65: 12'de 2 ✓, üstü: 11'de 5 ✓ (önceki setteki yön tekrarlamadı).

## Kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, MUM_IZI_HAKEM.py, test_mum_izi10.py, mühürlü MUM_IZI14_* / MUM_IZI18_* / MUM_IZI20_* ve cemal_*.json (yalnız okunur). `git add -A` / `commit -a` yasak; yalnız kendi yolların.
- Tanımlar MUM_IZI11 / 13 / 17 / 19 ön kayıtlarıyla AYNEN. Veri <= 2022-12-31. Sayfa -> bölge eşlemesi mühürlü MUM_IZI20_onay_anahtar.json ('yeni_sayfa'); etiket cemal_mum_izi20_onay.json (isaret 'YOK' olan sayfa sınıf tablolarına girmez, 'kapıdan geçenler' tablosuna girer). Set 1-7 satırları değişmez (mum_izi19_olay.csv ile karşılaştırılır).
- Kod işi başında `python IZ_KARNE.py kontrol istanimi`; ön kayıt (MUM_IZI21_ON_KAYIT.md: kod sha, GETİRİSİZ SAYIM, KONTROL LİSTESİ) hesaptan ÖNCE commit; `IZ_KARNE.ik_kontrol_kapisi` geçmeden hesap başlamaz. Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI. EK 19'da bildirilen kusur (sonuç json'unda kapı kaydının tablo adıyla ezilmesi) bu işte yinelenmez.

## Tablolar (önceden; sonuçtan sonra değişmez)
- (i) BEŞİNCİ BAKIŞ = yalnız set 8: Cemal sınıfı x zaman (n, R15 ortalama / medyan, eşli fark ortalama / medyan, artıda payı, eşinden iyi payı, +%5 / +%10 stop'tan önce payı) + 24 bölgenin dökümü.
- (ii) KAPIDAN GEÇENLER = set 7 + set 8'in 36 bölgesi (mumları olağanın 0,70 katı ya da altı), Cemal'in işaretinden bağımsız, zaman dilimine göre ve birlikte: aynı ölçüler; eşli farkın ortalaması için ay kümeli olmayan basit bootstrap %95 aralığı ve işaret çevirme p (tohum 21). Soru: 'belirgin küçük mumlu bölgeler eşlerinden iyi gitti mi'. n >= 30 olan tek tablo budur.
- (iii) GERÇEK ÖLÇEKLE İŞARETLENENLER = set 6 + 7 + 8 (Cemal sonrasını görmeden, yüzde eksenli sayfada işaretledi; 52 işaretli bölge): Cemal sınıfı x zaman ve birlikte; BENZİYOR - BENZEMİYOR eşli fark farkı (permütasyon, tohum 21); BENZEMİYOR'ların eşlerine göre farkı (işaret çevirme). Duyarlılık: iki kutu işaretli sayfa EVET sayılırsa.
- (iv) BİRLEŞİK = set 1-8: MUM_IZI19 birleşik tablosunun aynısı; ne değişti.
- OKUMA: (ii) dışındaki hücreler n < 30: 'BİLGİ; ÖRNEKLEM YETERSİZ'. (ii) için: eşli fark ortalamasının %95 aralığı sıfırın üstündeyse 'eşlerinden iyi', altındaysa 'eşlerinden kötü', sıfırı içeriyorsa 'ayrışmıyor' yazılır; tek pazar ağırlıklı (ABD) ve tek aday kuralı havuzu olduğu için karar etiketi yine BİLGİ'dir. Eş sınırı raporda yazılır.

## Çıktılar
MUM_IZI_GOZ2.py'ye set 8 (çalışan kısma dokunmadan) + test; MUM_IZI21_ON_KAYIT.md, MUM_IZI21_RAPOR.md, mum_izi21_sonuc.json, mum_izi21_olay.csv; MUM_IZI21_SONRASI.pdf (MUM_IZI19_SONRASI ile aynı düzen: kapakta özet tablo; 24 bölgenin hepsi sırayla BENZİYOR, KISMEN, BENZEMİYOR, işaretsiz; her sayfada Cemal'in işareti, hisse, tarih, sonrası 30 mum, 15 mum getirisi, eş ortalaması, mum boyu % ve oran, yüzde ekseni).
