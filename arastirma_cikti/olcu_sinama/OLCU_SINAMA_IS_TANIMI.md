# ÖLÇÜ SINAMASI: HANGİ ÖLÇÜ BİLİNEN ETKİYİ GÖRÜYOR? (iş tanımı, 22 Kasım 2026; yalnız AÇIK veri)

Cemal (22 Kas): "açık veride sınamak tabii ki mantıklı." Bağlam: Ç205 kart turu 1: 15-30 mum stop'suz eşli getiri (CETVEL2 v2.2) ne kartları ne kontrol kartını (12-1 momentum) gördü. Kural (IK_HATA 21 Kas): yeni ölçü önce açık veride kontrol kartını GÖRMELİ; görmeden kasa bloğu açılmaz. Bu iş iz aramaz; ÖLÇÜ seçer.

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

## 1. YASAKLAR
- VERİ: yalnız /tmp/kasa/acik (= /tmp/veri = /tmp/veri2; açık kesik 2023-12-31). Başka fiyat kaynağı, git worktree, indirme, /root altı, .kasa dosyaları YASAK. Her ölçümden önce KASA.kasa_kapisi; rapora en geç tarih yazılır. Repo içindeki eski olay / sonuç dosyaları (2024+ satır içerenler) OKUNMAZ.
- DEĞİŞTİRİLMEZ: defter dosyaları (IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, KURAL_DEFTERI_TASLAK.md, CEMAL_COL_KURALLARI.md, HAKEM_DERSLER.md, TUR_DEFTERI.md), KASA.py, CETVEL2.py, KART_TUR1.py, ORTAK_CETVEL.py, YAPI_HEDEF.py, DUSUS_SONRASI.py, POZITIF_KONTROL.py, GOZ_ETIKET.py ve arastirma_cikti/kart/, arastirma_cikti/kasa/ (KART_TUR1 bakış 2 bu dosyaların sha'sına bağlı). Yeni kod: OLCU_SINAMA.py + test_olcu_sinama.py (tek dosya, çakışma kapısı, hata yakalama, loglama). git add -A yok; e-posta / anahtar yok. Commit sonu iki satır AYNEN: 'Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>' ve 'Claude-Session: https://claude.ai/code/session_01F7vgWZPNpBhrsGQEHDtRis'; push `git push -u origin ccr-27195a1e-djv6v3`. Uzun koşu nohup; yarım sonuç yok. Rapor SubagentHandback.

## 2. PANEL (nedensel; iki bilinen geleceğe bakma DÜZELTİLMİŞ; arastirma_cikti/cetvel2/KENAR_ETKISI_DENETIM.md'yi oku)
OLCU_SINAMA kendi panelini kurar (ORTAK_CETVEL içe alınabilir ama şu iki kural yeniden yazılır): (a) hisse evrene KENDİ 80. geçerli barından sonra girer (veri sonuna kadarki bar sayısı kullanılmaz); (b) bölünme şüphesi yalnız d-1'e kadarki barlarla; son 10 barda büyük sıçrama varsa kalıcılığı henüz bilinmediği için o hisse-gün havuz DIŞI (tutucu). Geçerli bar, likidite alt %20 dışlama, giriş t+1 açılış aynı. EVREN PREFIX TESTİ (zorunlu): veri iki farklı tarihte kesilir (2022-06-30 ve 2023-12-29); sinyal günü <= 2022-05-31 olan bütün hisse-günlerde havuz üyeliği, kova ve olay kümeleri BİREBİR aynı olmalı (son giriş şeridi hariç tutulmaz; fark 0 beklenir); tutmazsa dur ve nedenini yaz.

## 3. KONTROL KARTLARI (bilinen etkiler; ay sonu olayları; ABD ve AVR; alt dönem d1 2016-19, d2 2020-23)
- MOM: 12-1 momentum üst onda (+) ve alt onda (−; 0'ı kesmesi yeter). Beklenen ufuk: 30-60.
- STREV: son 21 işlem günü getirisi ALT onda (+) ve ÜST onda (−) (kısa vadeli dönüş; Jegadeesh 1990; beklenen ufuk 15-30). Not: yaşayan evren alt ondayı yukarı yanlı gösterir; yazılır.
- HIGH52: kapanış / 252 gün en yüksek üst onda (+).
- PLASEBO: rastgele etiket (200 tohum) ve YAPAY İZ (+%1 / +%2 / +%3 / +%5 sürüklenme; n 100 / 300 / 1000; 20 tohum).

## 4. ADAY ÖLÇÜLER (hepsi giriş E0 = t+1 açılış; H ∈ {15, 30, 60}; eş = aynı giriş günü, aynı pazar, olay kümesi dışı, en az 5 eş)
EŞ KOVALARI iki sürüm, yan yana: KV1 = CETVEL2 kovası (ATRP tercili x likidite üçlüsü x F15 çeyreği); KV2 = oynaklık ince + konumsuz (ATRP ONDALIĞI x likidite üçlüsü; F15 yok). Sınırlar 2016-22'den sabit.
- O1 ortalama getiri farkı: R_H − eş ortalaması (CETVEL2 ile aynı; H 60 eklendi).
- O2 sıra: R_H'nin eş dağılımındaki yüzdeliği − 0,5 (aykırı değere dayanıklı).
- O3 hedefe dokunma: T10_H = H bar içinde High >= E0 x 1,10 (ve T5_H); olay payı − eş payı.
- O4 oynaklığa göre ölçekli asimetri: A_H = [(maks High − E0) − (E0 − min Low)] / (E0 x ATRP14(t)); olay − eş ortalaması.
- O5 önce-hedef, oynaklık ölçekli: +1,5 x ATRP hedefi −1,5 x ATRP stop'tan önce görüldü mü (H bar; aynı barda ikisi birden ise stop sayılır); olay payı − eş payı.
İstatistik (hepsi için aynı): hücre = pazar x alt dönem; ay kümeli bootstrap %95 (B 2000), ay kümeli işaret permütasyon p, L3O; TUTAR = n >= 30, fark beklenen yönde, boot alt ucu > 0 (yön − ise üst ucu < 0), L3O aynı işaret.

## 5. ÖLÇÜ SEÇİM KURALI (önceden yazılı; sonuç görülmeden)
Bir (ölçü, kova, H) üçlüsü GEÇER ancak hepsi tutarsa: (i) PLASEBO: ABD ve AVR'nin dört hücresinde ortalama fark ~0 (|fark| ölçünün hücre içi standart sapmasının %3'ünden küçük) ve yön başına tutar payı <= %7; (ii) YAPAY İZ: +%2 sürüklenme n <= 1000'de dört hücrede >= %80 yakalanır; (iii) OYNAKLIK ÖDÜLÜ YOK: MOM alt onda ve STREV üst onda (beklenen −) hiçbir hücrede beklenenin TERSİ yönde tutmaz; (iv) BİLİNEN ETKİYİ GÖRÜR: en az bir kontrol kartının + bacağı (MOM üst, STREV alt ya da HIGH52 üst) ABD'nin İKİ alt döneminde de TUTAR (AVR bilgi). Geçenler arasında sıralama: (1) Cemal'in kuralına yakın ufuk (15 < 30 < 60 tercih sırası: önce 15, sonra 30, sonra 60); (2) daha çok kontrol kartı gören; (3) yapay izde daha küçük n. Hiçbiri geçmezse: 'bu evren ve eş kurulumunda 15-60 mum ölçüsü bilinen etkiyi göremiyor' diye raporlanır; ek tanı: aynı kontrol kartları EŞSİZ (ham kesit: üst onda − alt onda aylık getiri farkı, klasik portföy yöntemi, H 21 / 63 gün) görünüyor mu (evren mi, eş kurulumu mu sorumlu).

## 6. TESLİM
Sıra: 'ÖLÇÜ SINAMASI kod' commit -> arastirma_cikti/olcu_sinama/OLCU_SINAMA_ON_KAYIT.md (kontrol tablosu K1-K14, bölüm 2-5 aynen, kova sınırları sayı olarak, sha'lar, KASA açık kesik) commit -> koşu -> OLCU_SINAMA_RAPOR.md + olcu_sinama.json + satır dosyaları commit. Rapor: (1) tek sayfa özet: GEÇEN ölçüler (varsa) ve seçim kuralına göre birinci; geçmeyenlerin hangi şarttan düştüğü; (2) tablo ölçü x kova x H x kontrol kartı x pazar x dönem (fark [boot], p, tutar); (3) plasebo ve yapay iz tabloları; (4) evren prefix testi sonucu; (5) klasik portföy tanısı; (6) YENİDEN ÜRETİM >= 3 hücre düz pandas + 30 olayın ölçüleri ham veriden düz döngü; (7) en geç tarih; HATA; KONTROL LİSTESİ. SubagentHandback: commit'ler + UTC, özet, geçen / düşen tablosu, önerilen ölçü, HATA, KONTROL LİSTESİ, testler.
