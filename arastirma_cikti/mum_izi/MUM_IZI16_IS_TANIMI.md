# MUM_IZI EK 16 İŞ TANIMI — ÖLÇEK: sayfadaki 'küçük mum' gerçekte küçük mü; gerçek mum boyu sonrasını ayırıyor mu; onay sayfasına gerçek ölçek (26 Kasım 2026)

Yazan: ana model. Cemal (26 Kas, MUM_IZI13_SONRASI'yı işaretleyip gerçek grafiklere baktıktan sonra; yazdığı gibi): "Yani gitmesini gereken ancak gitmeyenin mumları gerçek grafikte bakınca gerçek anlamda küçük gostermuyor grafikteki ölçek mi ne bilmiyorum". El notları (işaretli dosya repoda: MUM_IZI13_SONRASI_cemal_isaretli.pdf; ana modelin okuması, bazıları belirsiz): 'yeni olay var, bu değil' (haber düşüşü), 'ağır bir hisse', 'Bollinger dar değil', 'sorun ne, bu niye gitmemiş', 'bunun gerçeği', bir sayfada yol çizimi (çıkış - geri çekilme - yükseliş), bir sayfada 'önce düştü'.

Olgu (ana model): onay / etiket sayfalarında fiyat ekseni yok; dikey ölçek pencereye (öncesindeki sert düşüş, uç fitiller ve Bollinger bantları dahil) otomatik sığdırılıyor. Bu yüzden sayfada 'küçük' görünen mum, çerçeveye göre küçüktür; yüzde olarak ya da hissenin kendi geçmişine göre küçük olmayabilir. Cemal'in gözü sayfada gerçek boyu göremiyor.

SINIR (önceden): Cemal sonrasını gördü ve gerçek grafiğe yalnız GİTMEYENLERDE baktı (gidenlere aynı gözle bakılmadı). Aşağıdaki sonrası tablosu bu yüzden GERİYE DÖNÜK BİLGİDİR; ölçüler sonrasından bağımsız, yalnız bölge barlarından hesaplanır (geleceğe bakma yok). Temiz sınama: MUM_IZI14 seti (Cemal sonrasını görmeden, ÖLÇEKLİ sayfada işaretler).

## 0. Kesin kurallar

- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/. `git add -A` / `commit -a` yasak; yalnız kendi yolların; iki alt ajan aynı dalda çalışıyor (İŞ A: MUM_IZI_GOZ2.py; İŞ B: MUM_IZI_HAKEM.py): birbirinizin dosyasına dokunmayın; index.lock görürsen bekle; push reddedilirse fetch + merge.
- Veri <= 2022-12-31; /root/.kasa, /tmp/veri*, /tmp/mum_izi yalnız okunur. Commit mesajına / rapora etiket-sayfa eşlemesi yazılmaz (MUM_IZI14 seti için; eski setlerin sonrası zaten açık).
- İŞ A: kod işi başında `python IZ_KARNE.py kontrol istanimi`; ön kayıt (MUM_IZI16_ON_KAYIT.md: kod sha, ölçü tanımları, GETİRİSİZ SAYIM, KONTROL LİSTESİ) sonrası tablosundan ÖNCE commit; `IZ_KARNE.ik_kontrol_kapisi` geçmeden sonrası hesabı başlamaz. Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.
- Çalışan kısma dokunma: mevcut komutların çıktıları ve eski PDF / anahtar sha'ları değişmemeli (test).

## 1. İŞ A (ölçü + sonrası; opus) — MUM_IZI_GOZ2.py `olcek` komutu + test

Örneklem: mum_izi13_olay.csv'nin 128 bölgesi (bölge barları mumun kendi zaman diliminde; haftalık barlar MUM_IZI_GOZ ile aynı yoldan).

Ölçüler (yalnız bölge ve öncesi barları; sabit):
- BOY_MUTLAK = bölge barlarında (H - L) / C medyanı, %.
- BOY_OZ (ANA ÖLÇÜ) = BOY_MUTLAK / bölgeden önceki 120 barın (H - L) / C medyanı (en az 40 bar; yoksa boş). < 1: hisse kendi olağanından sakin.
- SON_BOY_OZ = aynı oran, yalnız bölgenin son üçte biri için.
- BOY_BANT = (H - L) / (üst bant - alt bant) medyanı (Bollinger 20, 2 sigma).
- BOY_SAYFA = (H - L) medyanı / onay sayfasının dikey açıklığı (sayfayı çizen fonksiyonun o bölge için kullandığı y sınırları yeniden hesaplanır): gözün gördüğü boy.
- SISME = sayfanın dikey açıklığı / bölgenin (en yüksek H - en düşük L) açıklığı.

A1 (OLGU; getirisiz): 128 bölgede BOY_SAYFA ile BOY_MUTLAK ve BOY_OZ arasındaki Spearman; 'sayfada küçük (BOY_SAYFA alt üçte bir) ama kendi geçmişine göre büyük (BOY_OZ üst üçte bir)' bölge sayısı; Cemal'in sınıflarına göre (EVET / KISMEN / HAYIR x günlük / haftalık) ölçülerin medyanı (Cemal'in gözü gerçek boyu seçebilmiş mi: EVET - HAYIR farkı, Mann-Whitney); Cemal'in not yazdığı on bölgenin (MUM_IZI13_SONRASI fiziksel sayfa 4, 5, 7-14) ölçü satırları.

A2 (SONRASI; ön kayıttan sonra): Cemal'in EVET bölgelerinde (36; günlük 16, haftalık 20) her ölçü için: eşli fark (fark sütunu) ile Spearman; zaman dilimi içinde medyandan ikiye bölüp KÜÇÜK - BÜYÜK eşli fark farkı (permütasyon 10.000, tohum 16), R15 ortalama / medyan, artıda payı, eşinden iyi payı. Aynısı EVET + KISMEN (52) ve 128 bölgenin tamamı için.
OKUMA KURALI: 'YÖN CEMAL'İN DEDİĞİ GİBİ' <=> ANA ÖLÇÜDE (BOY_OZ) EVET bölgelerinde KÜÇÜK yarının eşli farkı > BÜYÜK yarının eşli farkı, günlükte VE haftalıkta. Öteki ölçüler bilgi (aile: 5 ölçü x 2 zaman dilimi; çoklu karşılaştırma notu). Hangi sonuç çıkarsa çıksın etiket 'BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK'; grup / eşik değişmez.

Çıktılar: MUM_IZI16_ON_KAYIT.md, MUM_IZI16_RAPOR.md, mum_izi16_sonuc.json, mum_izi16_olay.csv. PDF yok.

## 2. İŞ B (sayfa; opus) — MUM_IZI_HAKEM.py `onay --olcek` seçeneği + test

Amaç: Cemal'in gözü gerçek mum boyunu görsün. Seçenek verilmezse sayfa eskisiyle birebir aynı (sha testi).
- B1. Büyük grafiğin sağında YÜZDE EKSENİ: 0 = bölgenin son kapanışı; yuvarlak adımlar (ör. %5 / %10 / %20; adım açıklığa göre seçilir, en az 4 en çok 8 çizgi), ince yatay kılavuz çizgileri. Fiyat, tarih, hisse adı YOK.
- B2. Sağlam dikey sınır: sınırlar pencere barlarının gövde + fitil %2 - %98 dilimine ve bölge içindeki bütün barlara göre kurulur; bunu aşan uç fitiller / bantlar çerçevede kesilir ve kesilen yere küçük bir işaret konur (tek dev fitil ölçeği ezmesin).
- B3. Grafiğin altına bir satır: 'Bölgede ortalama mum boyu: %x · bu hissenin önceki 120 mumunda: %y · oran z' (İŞ A'daki BOY_MUTLAK / BOY_OZ tanımıyla aynı; kendi içinde hesaplanır, İŞ A'yı beklemez; iki işin sayıları sonradan karşılaştırılır).
- B4. Sayfaya ÜÇÜNCÜ KUTU: '✓ benziyor', 'K kısmen', '× benzemiyor' (yalnız --olcek sayfasında).
- B5. MUM_IZI14 seti aynı 17 bölge, AYNI sayfa sırası ve numaralarıyla yeniden basılır: arastirma_cikti/mum_izi/MUM_IZI14_ONAY_OLCEKLI.pdf; mühürlü MUM_IZI14_onay_anahtar.json DEĞİŞMEZ; yeni pdf sha'sı ayrı küçük dosyaya (MUM_IZI14_onay_olcekli.json) yazılır. Kapak: eski kapak metni + 'Bu sürümde sağda yüzde ekseni var: mumların gerçek boyu görünür. Önceki (ölçeksiz) dosya yerine bunu işaretle.' Sağlama: 3 sayfa PNG'ye çevrilip gözle bakılır (eksen okunaklı mı, kırpma işareti doğru mu, bölge aynı mı); 17 sayfanın bölge kimliği eski anahtarla aynı (test).
Çıktı: kod + test + PDF + MUM_IZI16_SAYFA_RAPOR.md (KONTROL LİSTESİ: ölçüm yok, uygulanmayanlar gerekçeli; HATA).
