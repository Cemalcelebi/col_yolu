# CETVEL2: DÜZELTİLMİŞ 15 MUM CETVELİ + ÖNCEKİ TESTLERİN YENİDEN KOŞUSU (iş tanımı, 21 Kasım 2026)

Cemal (21 Kas): "bahsettiğim bütün hataları düzelt, test et, ajanlara test ettir; önceki testlerde yaptığın yanlışları doğrula; sonra doğru kodla doğrula; önceki gün testlerini gözden geçir."
Kaynak: Ç203 pozitif kontrol (POZITIF_KONTROL_RAPOR.md): h5 (+%5 stop dip x 0,98 önce) oynaklığı ödüllendiriyor (momentum alt ondası +5,3), AVR sınama eş geometrisi plaseboda +2,2 puan, n <= 100 kör, dar stop büyük kazananları kesiyor.

## 0. Kontrol listesi
```
ÖN UÇUŞ KONTROLÜ (zorunlu; hata defterinden): kod yazmaya başlamadan önce oku, ön kayıt dosyasına KONTROL LİSTESİ tablosunu (`python IZ_KARNE.py kontrol`) doldurarak koy, raporunda 'HATA' başlığıyla bulduğun her hatayı ayrı listele.
- K1 kontrol grubu: Eşler aynı giriş günü, aynı momentum x likidite hücresi, aynı giriş / çıkış geometrisi mi; taban rastgele olay sağlamasıyla (200 eş portföy) mi? Mekanik üstünlük (sinyal tanımının kendiliğinden ürettiği fark) dışlandı mı? [geçmiş: 22 kez (H005, H006, H026-H032, H055, H064, H100...)]
- K2 geleceğe bakma: Her girdi alanının bilgi tarihi <= karar günü ve bu KODDA mekanik denetleniyor mu? Satır tarihi mi (sayfa / haber tarihi değil)? Etiket, evren listesi, sektör karar günündeki haliyle mi? [geçmiş: 12 kez (H003, H016, H034, H051, H130...)]
- K3 geçerli bar: H>L ve V>0 olmayan bar sinyal ya da ölçü üretmiyor mu; hacim 0 gün fiyatı bayat sayılıyor mu; seans açıkken yarım bar atılıyor mu? [geçmiş: 2 kez aynı hata (H004, H037), H134, H141]
- K4 tekilleştirme: Aynı hissede olay 60 günde bir mi; n bağımsız olay sayısı mı; aynı işlem bir kez mi sayılıyor; ortalama yanında medyan var mı? [geçmiş: H006 (n 4-5 kat şişkin), H014]
- K5 giriş fiyatı: Giriş = sinyalden (yayın saatinden) sonraki ilk işlem fiyatı mı (ertesi açılış), sinyal günü kapanışı değil mi? [geçmiş: H005, 60 gün ufuk itirazı]
- K6 veri birimi: Fiyat tek kipte mi (ekran fiyatı ya da düzeltilmiş, karışık değil); birim (lot / TL, peni / sterlin, 100x), bölünme marjı (12.03.2020 öncesi +-%20), bedelsiz denetlendi mi; yeni pazar birim denetiminden geçti mi? [geçmiş: veri 34 satır (H007, H017, H060...)]
- K7 hayatta kalma: Evren bugünün listesi mi? Batanlar / kottan çıkanlar yoksa raporda yazılı ve sonuç 'yukarı yanlı' okunuyor mu? [geçmiş: 8 kez (H008, H057, H142...)]
- K8 örneklem ve dönem: n < 30 'örneklem yetersiz' ve olaylar tek tek listeli mi; iki alt dönem aynı yönde mi; çoklu karşılaştırma BH ile mi; küçük örneklemden 'bulgu' denmiyor mu? [geçmiş: H010, Ç169 n 11, K1 / K2 n < 30]
- K9 ön kayıt: Tanım + eşik sözlüğü + kod sha ön kayıtta; ön kayıt commit zamanı < koşu zamanı; sonuçtan sonra yalnız gösterim değişti, aksi SAPMA; eşik sonuca göre oynanmadı mı? [geçmiş: H079, H097 (ön kayıt geç commit)]
- K10 ayrıştırma: Ham kaynaktan rastgele >= 3 satır elle doğrulandı mı; haber türü (günlük / aylık / dönemsel), kurum etiketi (çok kurumlu haber), kenar kuşağı çöpü, güncelleme damgası, kurum adı hisse satırı dört ayrı denetim maddesi olarak kontrol edildi mi? [geçmiş: 5 kez tek günde (H128-H132, H136)]
- K11 yeniden üretim: Raporlanan >= 2 hücre satır dosyasından bağımsız kodla yeniden üretildi mi; metindeki sıra / tarih / sayı ham kayıtla aynı mı? [geçmiş: H136 (PEKGY 1. / 4.), H137 (blok filtresi)]
- K12 ifade: Fiyat değişimi ile gerçekleşen kâr / zarar ayrı mı; aracı kurum akışı ile kurum pozisyonu ayrı mı; 'anlamlı / ters / iz / emare' sözü yalnız bu liste geçince mi; sayı ile yorum ayrı cümlede mi? [geçmiş: yanlış yorum 16 satır (H133, H135...)]
- K13 süreç: Çakışma kapısı korundu mu; kod değiştiyse 'çalışma zamanını yeniden başlat' yazıldı mı; e-posta / anahtar sızıntı taraması yapıldı mı; kota / ücret / yeni dal Cemal onayıyla mı; yasak defter dosyalarına dokunulmadı mı? [geçmiş: süreç 21 satır (H019, H021, H143...)]
- K14 boyut (gerçek para): Öneri işinde boyut tavanı, zarardaki isme ekleme yasağı, olay bazlı çıkış ve 2x kuralı alımdan önce yazılı mı; taban oranlar (10x ~%1) yazılı mı? [geçmiş: karar-boyut 6 satır (H012, H013)]
```

## 1. YASAKLAR (iki adım için)
Defter dosyalarına (IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, KURAL_DEFTERI_TASLAK.md, CEMAL_COL_KURALLARI.md, HAKEM_DERSLER.md, TUR_DEFTERI.md) ve üretim zincirine dokunma. YAPI_HEDEF.py, DUSUS_SONRASI.py, ORTAK_CETVEL.py, POZITIF_KONTROL.py, GOZ_ETIKET.py DEĞİŞTİRİLMEZ (eski sonuçlar yeniden üretilebilir kalmalı); içe alınır. Yeni kod tek dosya CETVEL2.py (+ test_cetvel2.py), çakışma kapısı, tam hata yakalama, loglama. git add -A yok; e-posta / anahtar yok; dış servis yok. Commit mesajı sonu iki satır AYNEN: 'Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>' ve 'Claude-Session: https://claude.ai/code/session_01F7vgWZPNpBhrsGQEHDtRis'; her commit'ten sonra `git push -u origin ccr-27195a1e-djv6v3`. Uzun koşular nohup ile; yarım sonuç yazılmaz. Rapor dili: iddia yok; etiketler aşağıdaki kurala göre.

## 2. CETVEL2 TANIMI (ana model ön kaydı; sabit; sonuç görülmeden)
Girdi: olay listesi (pazar, sembol, sinyal günü t, isteğe bağlı özellik bayrakları). Fiyat: /tmp/veri/V_ABD.pkl, V_AVR.pkl, V_BIST.pkl (ORTAK_CETVEL.oc_veri; aynı geçerli bar ve likidite kuralları).
- Giriş E0 = t'den sonraki ilk geçerli bar AÇILIŞI (K5). Olay t'de bilinir; prefix testi (K2).
- KARAR ÖLÇÜSÜ R15 = 15. geçerli barın kapanışı / E0 − 1 (stop yok). 15 bar yoksa ölçülmez (kriz kesiği 31.08.2026, K8).
- EŞ (konum eşli, bütün evren): aynı giriş günü, aynı pazar, aynı KOVA = ATRP(14) tercili x 20 gün işlem değeri üçlüsü x F15 (120 gün konumu, t dahil) çeyreği; eş kümesinden olay kümesindeki hisseler (aynı deneme) çıkarılır; en az 5 eş yoksa olay 'eşsiz' (ölçülmez; sayısı yazılır). Terciller / üçlüler / çeyrekler EĞİTİM döneminde (2016-22) pazar başına sabitlenir, sayı olarak ön kayıtta.
- FARK = R15(olay) − ortalama R15(eş). SIRA = olayın R15'inin eş dağılımındaki yüzdeliği (0-1). Hücre (pazar x dönem): n, ortalama FARK, medyan FARK, ortalama SIRA, ay kümeli bootstrap %95 (B 2000), ay kümeli işaret permütasyon p (tek yönlü, beklenen yöne göre; iki yönlü işaretli hipotezlerde iki yönlü), L3O (en iyi 3 ay çıkınca ortalama FARK).
- HÜCRE TUTAR: n >= 30 VE güç >= 0,80 (R15 ile güç eğrisi: bölüm 3 A'dan hücre sigma'sı) VE ortalama FARK > 0 VE boot alt ucu > 0 VE ortalama SIRA > 0,50 VE L3O > 0 (beklenen yön − ise işaretler ters).
- PLASEBO KAPISI (hücre başına, ön kayıtta): rastgele etiketli olay kümesi (aynı n, aynı dönem dağılımı, 20 tohum): ortalama FARK mutlak değeri < 0,5 puan VE 'tutar' payı <= %7. Kapıyı geçmeyen hücre KARAR VERMEZ (BİLGİ); nedeni araştırılır ve yazılır (AVR sınama şüpheli: eş sayısı, kova boşluğu, aynı gün az hisse).
- ETİKET (karne v3 mantığı): KATKI+ = ABD ve AVR'de, eğitim ve sınamada dört hücre TUTAR (plasebo kapısını geçen hücrelerle); KATKI− = dört hücrede ters yönde tutar; SORGULA = bazı hücreler tutar; ÖLÇÜLEMEDİ = n / güç yetersiz; ÇELİŞKİLİ = eğitim ile sınama ters işaret (boot aralıkları ayrık). BIST bilgi. Çoklu test: aynı ön kayıttaki hipotez sayısı m ile BH q 0,10 (sınama hücresi p'leri üzerinden; m sabit).
- BİLGİ SÜTUNLARI (karar dışı, eski sonuçlarla kıyas için): h5 / st5 (eski cetvel: stop dip x 0,98), ATR stop kolu (stop = E0 − 2 x ATR14(t); hedef +%5 stop'tan önce, 15 bar), r60 eşli fark (ORTAK_CETVEL tanımı), R15 medyanı.

## 3. ADIM G (alt ajan 1): CETVEL2.py + POZİTİF KONTROL v2 + ÖN KAYIT
1. CETVEL2.py: c2_veri (oc_veri), c2_panel (E0, R15, ATRP, likidite, F15, kova; prefix testi), c2_es (konum eşli R15 ortalaması, eş sayısı), c2_hucre, c2_plasebo, c2_guc (yapay iz eğrisi), c2_etiket, c2_bh, c2_olc(olay_listesi, hipotez_bayraklari) -> satır dosyası + hücre tablosu + etiketler, c2_rapor. test_cetvel2.py: çakışma kapısı, sentetik veri (R15 düz döngüyle eşit, eş kurulumu, plasebo ~0, yapay iz yakalanıyor, prefix).
2. POZİTİF KONTROL v2 (aynı POZITIF_KONTROL iş tanımı mantığı, R15 ile): (A) yapay iz: DS ANA olayları, delta +%1 / +%2 / +%3 / +%5, n 30 / 100 / 300 / 1000 / yarı, 20 tohum, plasebo delta 0; yakalama payı tablosu ve hücre başına güç eğrisi (kayıt: cetvel2_guc.json); (B) momentum 12-1 üst onda (beklenen +) ve ALT onda (beklenen −) ve PEAD üst / alt: R15 FARK, p; ÖLÇÜT (önceden yazılı): cetvel2 DOĞRU ŞEYE DUYARLI sayılır ancak momentum üst onda + ve alt onda − (ya da 0'ı kesen) çıkarsa; alt onda yine + çıkarsa cetvel2 de kusurlu, nedeni yazılır; (C) plasebo kapısı bütün hücreler (ABD / AVR / BIST x eğitim / sınama). Sonuç: arastirma_cikti/cetvel2/CETVEL2_POZITIF_KONTROL.md.
3. ÖN KAYIT: arastirma_cikti/cetvel2/CETVEL2_ON_KAYIT.md: kontrol tablosu K1-K14, cetvel tanımı (bölüm 2 aynen + eğitim döneminde sabitlenen kova sınırları sayı olarak), plasebo kapısı eşikleri, güç eğrisi, sha'lar (CETVEL2.py, DS / YH / OC eşik sha'ları), git mühür. Sıra: kod + test commit ('CETVEL2 kod') -> ön kayıt commit ('CETVEL2 ön kayıt') -> pozitif kontrol koşusu -> commit ('CETVEL2 pozitif kontrol'). Pozitif kontrol kusur bulursa cetvel düzeltilir, ÖN KAYIT YENİ SÜRÜM olarak yazılır (eski silinmez, 'v2.1' notu), yeniden koşulur; en çok 2 tur.
Rapor (SubagentHandback): commit hash'leri + UTC; A tablosu (hangi n / delta'da yakalama >= %80; plasebo), B tablosu (momentum üst / alt, PEAD; R15 FARK, p; h5 ile yan yana), C plasebo kapısı hücre tablosu (geçen / geçmeyen, AVR nedeni); SONUÇ (cetvel2 doğru şeye duyarlı mı: EVET / HAYIR / KISMEN); YENİDEN ÜRETİM (>= 2 hücre düz kod); HATA; KONTROL LİSTESİ; testler.

## 4. ADIM H (alt ajan 2, G bittikten sonra): ÖNCEKİ TESTLERİN CETVEL2 İLE YENİDEN KOŞUSU
Aynı olay kümeleri, aynı eşikler (sha'lar değişmez), yalnız cetvel değişir. Her satır için ESKİ (h5 cetveli, rapordaki etiket ve FARK) ve YENİ (CETVEL2: R15 FARK, SIRA, boot, plasebo kapısı, etiket) yan yana; 'DEĞİŞTİ Mİ' sütunu.
Kapsam (18-20 Kasım testleri; olay dosyaları repoda):
- Ç194 S7 (Cemal'in 8 kuralı, YAPI_HEDEF 3. tur ozellik_Y1_s7): Y1 ∧ S7 vs Y1.
- Ç195 Ş9 U dip (ozellik_Y1_s9; Y1 ∧ Ş9, Y9 dipte ∧ Ş9).
- Ç196 filtre karnesi (FILTRE_KARNE.md; Ş1-Ş8 tek süzgeç olarak Y1 ve Y9 üstünde; grup: dip grubu vs trend içi raf).
- Ç197 PUAN (puan_Y1.csv.gz; üst %20 dilim vs gerisi).
- Ç198-Ç200 DEVİR 1-3 adayları (ozellik_Y1_d1 / d2 + devir3 F30+; 32 aday; kol A Y1 ve kol B Y9).
- Ç201 Ş10 MACD uyumsuzluğu (olay_Y13, Y13b, Y13c).
- Ç202 DS 25 hipotez (ds_olay.csv.gz F_DS* bayrakları; DS olay kümesi; eş = konum eşli bütün evren, ayrıca DS içi eş bilgi).
- Ayrıca HAKEM TURLARI model kuralı havuzları (T1.6 U dip, T1.7, T1.8; tur/4-7 anahtar dosyaları): havuzun R15 eşli farkı bilgi.
Her satır: deneme | pazar | hücre | n | ESKİ h5 FARK / etiket | YENİ R15 FARK [boot] / SIRA / plasebo geçti mi / etiket | değişti mi. BH: her Ç'nin kendi m'si (ön kayıttaki hipotez sayısı). Çıktı: arastirma_cikti/cetvel2/YENIDEN_KOSU.md + yeniden_kosu.json + satır dosyaları; özet: kaç satır etiket değiştirdi, hangi yönde; CETVEL2 ile KATKI+ / KATKI− çıkan var mı (varsa bağımsız lens için satır verisi). YENİDEN ÜRETİM >= 3 hücre; HATA; KONTROL LİSTESİ. Commit 'CETVEL2 yeniden koşu'. Rapor SubagentHandback ile.
