# MUM_IZI EK 6 İŞ TANIMI — ETİKET SETİ 2: 'konum' ölçüsünün yeni sayfalarda ileri sınaması + Cemal'in kendi tutarlılığı (25 Kasım 2026)

Yazan: ana model. Durum: v1, v2, v3 üçü de Cemal'in gözüyle uyuşmadı (EK 5: D3 AUC 0,63; F1 konum 0,71, aralık 0,45-0,92; F2 0,49; F3 0,64; 24 etiket, 7 benziyor). O 24 sayfanın hepsi v2 seçimiydi (dar küme) ve yalnız 7 pozitif vardı: hiçbir ölçü hakkında hüküm verecek güç yok. Bu iş yeni ölçü KURMAZ; mevcut donmuş ölçüleri (MUM_IZI_V3'ün F1 / F2 / F3 / D3'ü, v1 S) yeni ve aralığın tamamına yayılmış sayfalarda Cemal'in işaretiyle sınamak için ETİKET SETİ hazırlar.

## Kurallar
- MUM_IZI_IS_TANIMI.md ve CLAUDE.md 'Tespit geçerliliği' aynen: yasak defter dosyaları, yalnız kendi yollarını commit, veri <= 2022-12-31, KASA açılmaz, GETİRİ / SONRASI YOK. MUM_IZI_V3.py ölçüleri DEĞİŞMEZ (sha ön kayıtta). Yeni kod: MUM_IZI_ETIKET2.py + test.
- MÜHÜR: anahtar dosyası (sayfa -> hisse, tarih, katman, ölçüler) PDF'e girmez; commit mesajlarına ve rapora katman / etiket / sayfa eşlemesi YAZILMAZ (EK 5 hatası: commit mesajı bir etiketi açık etti). Son rapor ana modele yalnız sayım düzeyinde bilgi verir (hangi sayfa hangi katman YAZMA).

## 1. Sayfa seçimi (ön kayıtta; tohum sabit)
- TEKRAR 8 sayfa: önceki 24 sayfadan (MUM_IZI4_ONAY) Cemal'in BENZİYOR dediklerinden rastgele 4 + BENZEMİYOR dediklerinden rastgele 4 (cemal_mum_izi4_onay.json bu seçim için açılabilir); aynı bölge, aynı çizim.
- YENİ 40 sayfa, evren pencerelerinden (günlük 2016-22, haftalık 2001-22; ABD / AVR P2; BIST işlem değeri o gün medyan üstü; geçerli bar; haftalıkta eksik haftasız; uzunluk 16-24 mum; hisse başına bir; önceki 24 sayfanın hisseleri hariç), donmuş F1 yüzdeliğine göre KATMANLI: K1 'en yakın' F1 <= 0,005: 16 sayfa; K2 0,005 < F1 <= 0,05: 12; K3 0,05 < F1 <= 0,20: 6; K4 tamamen rastgele pencere: 6. Her katman yarı günlük yarı haftalık; BIST katman başına en çok üçte bir. Katman içi seçim RASTGELE (ölçüye göre en iyi değil).
- 48 sayfa karışık sırada (tohum). Sayfa düzeni MUM_IZI4_ONAY ile BİREBİR AYNI (solda 'Senin kalıbın', sağda bölge: öncesi 15 mum, Bollinger 20 + SMA20, bölge sonunda kesik; hisse / tarih yok; altta ✓ benziyor / × benzemiyor kutuları). Kapak sayfası (tek sayfa, düz dil): 'Kodun üç denemesi de gözünle uyuşmadı. Bu set kodun değil senin gözünün ölçümü: 48 bölge; bir kısmı kalıbına yakın, bir kısmı uzak, bir kısmı rastgele; 8'i daha önce gördüklerin. Her sayfada benziyorsa ✓ kutusuna, benzemiyorsa × kutusuna X koy. İstersen benzeyen sayfada benzeten 2-3 mumu daire içine al.'

## 2. Ön kayıtlı sınamalar (Cemal işaretleyince koşulacak; komut hazır: `python MUM_IZI_ETIKET2.py olc`)
- T1 TUTARLILIK: 8 tekrar sayfasında önceki işaretle aynı olan sayı; >= 7 / 8 'tutarlı', 5-6 'kısmen', <= 4 'tutarsız' (tutarsızsa hiçbir formül tutturamaz; rapor böyle yazılır).
- T2 KONUM (ANA): 40 yeni sayfada donmuş F1'in AUC'si (BENZİYOR'lar daha küçük F1), bootstrap %95, permütasyon p. Hüküm: AUC >= 0,80 ve alt uç >= 0,65 'konum ölçüsü gözle UYUMLU'; AUC 0,65-0,80 KISMEN; < 0,65 UYUMSUZ. Ek: katmana göre BENZİYOR payı (K1 > K2 > K3 > K4 sırası tutuyor mu).
- T3 (bilgi): D3, F2, F3, F1'in evre parçası, v1 S için aynı AUC; günlük / haftalık ayrı.
- T4 (bilgi, EZBER RİSKLİ): 64 etiketle (24 + 40) basit öğrenen model (düzenlileştirilmiş lojistik; girdi F1 / F2 / F3 parçaları + 39 ölçü), yalnız çapraz doğrulamalı AUC raporlanır.
- SONRASI: T2 UYUMLU ise v4 = F1 eşiği + sentetik negatiflerden geçen zorunlu kapılar (yeni ön kayıt), sonra en benzer bölgelerle onay; KISMEN / UYUMSUZ ise karar Cemal'in (öğrenen model için daha çok etiket ya da hattın kapanması).

## Çıktılar
arastirma_cikti/mum_izi/: MUM_IZI6_ON_KAYIT.md (seçim kuralı, tohumlar, T1-T4, sha'lar, KONTROL LİSTESİ; PDF üretiminden önce commit), MUM_IZI6_ETIKET.pdf (49 sayfa: kapak + 48), mum_izi6_anahtar.json (mühürlü), MUM_IZI6_RAPOR.md (yalnız sayımlar: katman başına sayfa sayısı, günlük / haftalık, pazar; HATA; SAPMA; ÖNERİLEN DEFTER SATIRLARI).
