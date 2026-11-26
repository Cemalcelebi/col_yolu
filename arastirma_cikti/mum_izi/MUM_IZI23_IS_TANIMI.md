# MUM_IZI EK 23 İŞ TANIMI — GÖZ ÖLÇÜMÜ ALTINCI BAKIŞ: geçmişli setin (set 9; 24 bölge) sonrası ve birleşik koşu (26 Kasım 2026)

Yazan: ana model. Cemal MUM_IZI22_ONAY_GECMISLI'yi işaretledi (cemal_mum_izi22_onay.json): BENZİYOR 10 (günlük 8, haftalık 2), KISMEN 8 (6 / 2), BENZEMİYOR 6 (günlük). Sözü: 'Evet daha güzel seçildi; burada daha fazla gerek yok; kod benim seçtiklerimin yüzde 70-90'ını seçiyorsa tamamdır'. Ön kayıtlı tespit sayımı (Ç249; getirisiz, yapıldı): tam ✓ 24'te 10 (gerisi görünmeyen sette 23'te 7); ✓ + K 24'te 18 (önce 23'te 14); sınıflarda oran medyanı ✓ 0,66 / K 0,62 / × 0,65 (kayma yok).

## Kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, MUM_IZI_HAKEM.py, test_mum_izi10.py, MUM_IZI_HAVUZ.py ve testi (başka alt ajan), mühürlü onay anahtarları / PDF'ler ve cemal_*.json (yalnız okunur). `git add -A` / `commit -a` yasak; yalnız kendi yolların.
- Tanımlar MUM_IZI11 / 13 / 17 / 19 / 21 ön kayıtlarıyla AYNEN. Veri <= 2022-12-31. Sayfa -> bölge eşlemesi mühürlü MUM_IZI22_onay_anahtar.json; etiket cemal_mum_izi22_onay.json. Set 1-8 satırları değişmez (mum_izi21_olay.csv ile karşılaştırılır).
- Kod işi başında `python IZ_KARNE.py kontrol istanimi`; ön kayıt (MUM_IZI23_ON_KAYIT.md) hesaptan ÖNCE commit; `IZ_KARNE.ik_kontrol_kapisi` geçmeden hesap başlamaz. Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.

## Tablolar (önceden; sonuçtan sonra değişmez; MUM_IZI21 ile aynı kalıp)
- (i) ALTINCI BAKIŞ = yalnız set 9: Cemal sınıfı x zaman + 24 bölgenin dökümü.
- (ii) KAPIDAN GEÇENLER = set 7 + 8 + 9 (60 bölge), Cemal'in işaretinden bağımsız, zaman dilimine göre ve birlikte: eşli fark ortalaması, basit bootstrap %95 aralığı, işaret çevirme p (tohum 23); okuma: aralık sıfırın üstünde 'eşlerinden iyi', altında 'eşlerinden kötü', içeriyorsa 'ayrışmıyor'.
- (iii) KAPI HAVUZUNDA CEMAL'İN İŞARETİ = set 7 + 8 + 9 (59 işaretli): BENZİYOR / KISMEN / BENZEMİYOR: aynı ölçüler; BENZİYOR - BENZEMİYOR ve (BENZİYOR + KISMEN) - BENZEMİYOR eşli fark farkı (permütasyon, tohum 23).
- (iv) GERÇEK ÖLÇEKLE İŞARETLENENLER = set 6 + 7 + 8 + 9; (v) BİRLEŞİK = set 1-9: MUM_IZI21 tablolarının aynısı; ne değişti.
- OKUMA: n < 30 hücreler 'BİLGİ; ÖRNEKLEM YETERSİZ'.

## Çıktılar
MUM_IZI_GOZ2.py'ye set 9 (çalışan kısma dokunmadan) + test; MUM_IZI23_ON_KAYIT.md, MUM_IZI23_RAPOR.md, mum_izi23_sonuc.json, mum_izi23_olay.csv; MUM_IZI23_SONRASI.pdf (MUM_IZI21_SONRASI ile aynı düzen; 24 bölge sırayla BENZİYOR, KISMEN, BENZEMİYOR).
