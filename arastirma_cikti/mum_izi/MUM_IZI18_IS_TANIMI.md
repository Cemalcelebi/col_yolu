# MUM_IZI EK 18 İŞ TANIMI — MUM BOYU KAPISI: 'mumlar genel mumlara oranla belirgin küçük olmalı'; kapıdan geçen yeni adaylar, ölçekli sayfayla hakem v5, yeni onay seti (26 Kasım 2026)

Yazan: ana model. Cemal (26 Kas, ölçekli onay setini işaretledikten sonra; yazdığı gibi): "Mumlar küçük değil yani genel mumlara oranla belirgin küçük olmalı". Durum: ölçekli sette (17 bölge) Cemal 4 BENZİYOR, 7 KISMEN, 6 BENZEMİYOR dedi (eşik 14 tam ✓: tutmadı). O 17 bölgede mum boyunun hissenin önceki 120 mumuna oranı 0,71 - 1,98 (medyan 0,97): 'belirgin küçük' olan hiç yoktu. Ç243: önceki bütün etiketler ve hakem ölçeksiz sayfalarla çalıştı.

Bu iş yalnız TESPİT içindir (getiri / sonrası hesaplanmaz, gösterilmez).

## 0. Kesin kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, MUM_IZI_GOZ2.py / test_mum_izi13.py (başka alt ajan çalışıyor), mühürlü eski anahtarlar / PDF'ler (yalnız okunur). `git add -A` / `commit -a` yasak; yalnız kendi yolların. Commit mesajına / rapora etiket-sayfa ya da hisse-sayfa eşlemesi yazılmaz.
- Veri <= 2022-12-31. Ölçüler yalnız bölge ve öncesi barlarından (bölge sonundan sonraki bar kullanılmaz: assert + test).
- Kapı eşiği sonuçtan / Cemal'in işaretlerinden sonra değişmez; değişirse yeni iş tanımı.
- Kod işi başında `python IZ_KARNE.py kontrol istanimi`; raporda KONTROL LİSTESİ (ölçüm olmadığı için uygulanmayanlar gerekçeli) ve HATA başlıkları.

## 1. KAPI (ZORUNLU; önceden sabit)
ORAN = bölge barlarında (H - L) / C medyanı / bölgeden önceki 120 barın (H - L) / C medyanı (en az 40 bar; yoksa aday DEĞİL). Tanım Ç243 BOY_OZ ile aynı.
- KAPI: ORAN <= 0,70 ('belirgin küçük' = hissenin olağan mumundan en az %30 küçük; eşik ana modelin seçimi, Cemal'in sözünün sayıya çevrilmiş hali; Cemal'in gözündeki eşik bu setteki işaretlerinden okunacak).
- Katmanlar (yalnız raporlama ve set dengesi için): ÇOK KÜÇÜK ORAN <= 0,50; KÜÇÜK 0,50 < ORAN <= 0,70.

## 2. İŞ A (kod; opus) — MUM_IZI_HAKEM.py, çalışan kısma dokunmadan
A1. Havuz sayımı (getirisiz): bütün v5M havuz olaylarında (MUM_IZI8 taraması; evren içi, tekil) ORAN dağılımı, zaman dilimine göre: n, ORAN <= 0,85 / 0,70 / 0,50 payları; önceki partilerde (1-3) ve hiç gösterilmemişlerde ayrı.
A2. `aday --parti 4`: havuzdan KAPI'yı geçen, önceki bütün set ve partilerde bulunmayan adaylar; hedef 600 (300 günlük + 300 haftalık; bir dilimde yetmezse eksik raporlanır, ötekiyle doldurulmaz; toplam 600'den azsa hepsi alınır); seçim tohumlu rastgele; klasör arastirma_cikti/mum_izi/hakem_aday4/ (mum_izi18_aday_*.pdf, 50'şer sayfa + mühürlü anahtar; anahtarda ORAN ve katman). ADAY SAYFALARI ÖLÇEKLİ basılır (yüzde ekseni, uç fitil kesimi, mum boyu satırı; `onay --olcek` sayfasıyla aynı çizim; işaret kutusu yok).
A3. `ogren --olcek`: tek öğrenme dosyası arastirma_cikti/mum_izi/MUM_IZI18_OGREN.pdf, hepsi ÖLÇEKLİ çizimle ve üstte etiket şeridiyle: önce MUM_IZI14 ölçekli setinin 17 bölgesi (etiket cemal_mum_izi14_onay.json; şerit: 'CEMAL (ölçekli sayfada): BENZİYOR / KISMEN / BENZEMİYOR'), sonra MUM_IZI10 + MUM_IZI12 setlerinin 48 bölgesi (etiketler cemal_mum_izi10_onay / 12_onay.json; şerit: 'CEMAL (eski, ölçeksiz sayfada): ...'); bölgeler ilgili mühürlü anahtarlardan yeniden çizilir. Sıra: her grupta BENZİYOR, KISMEN, BENZEMİYOR. Sınıf sayıları json'larla eşit (test); 6 sayfa PNG'ye çevrilip gözle doğrulanır.
A4. `onay --olcek` iki aşamalı seçim parti 4 için de çalışır (aday klasörü parametre); set sayfalarında ORAN görünür (zaten mum boyu satırında). Set 24 sayfa: önce iki hakemin de EVET dedikleri, sonra 2. hakem KISMEN (EK 14 kuralı aynen).
A5. Testler (eski partilerin anahtar sha'ları ve eski komut çıktıları değişmez; kapı sınırı 0,70 dahil / 0,7001 hariç; 40 bar kuralı; geleceğe bakma; hariç tutma) -> `aday --parti 4`, `ogren --olcek` koşulur -> kod + test + çıktılar + MUM_IZI18_KOD_RAPOR.md commit + push.

## 3. İŞ B / C (hakem v5; sonnet) ve derleme (ana model)
Hakem metni = v4 (ölçütler 1-9 + kopma) + 10. madde (Cemal: 'mumlar genel mumlara oranla belirgin küçük olmalı'; adayların hepsi ORAN <= 0,70 kapısından geçmiştir; hakem yine de gözle bakar: bölge mumları öncesindeki mumlara göre belirgin küçük mü) + MUM_IZI18_OGREN.pdf. 1. aşama: aday sayısına göre 150'şer sayfalık hakemler, her birine ayrı geçici klasör; çıktı anahtarı sayfa numarası (yalnız rakam, ör. "37"). 2. aşama: 1. aşama EVET + aynı sayıda rastgele (tohum 18) öteki, karışık, bilmeden. Derleme: hakem json'ları commit (mühür) -> `onay --olcek` -> ana model 6 sayfaya bakar -> MUM_IZI18_ONAY_OLCEKLI.pdf Cemal'e. Onay eşiği: sayfaların >= %80'i tam ✓. Set 12 sayfadan azsa: 2. aşama KISMEN'lerden sonra 1. aşama KISMEN (puanı >= 6) olanlarla 12'ye tamamlanır ve bu, kapakta söylenir.
