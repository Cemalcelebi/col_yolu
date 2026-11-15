# İŞ TANIMI — FON_IZI tarayıcılarında seri uzunluğu şartının geleceğe bakması (H satırı 2026-11-14) düzeltmesi

Yazan: ana model, 2026-11-15. Yapan: alt ajan. Denetleyen: ana model.
Hata kaynağı: IK_HATA 2026-11-14 satırı — "FON_IZI tarayıcıları (fi_k24_tara n<200; fi_k13 / fi_k17 n<400; fi_k23_parmak n<L+200): hisse atlama şartı serinin TOPLAM uzunluğuna bakıyor; toplam uzunluk gelecekteki barları içerdiği için geleceğe bakma. K24'te 1.430 sinyal etkilendi." Ders: "Seri uzunluğu şartı daima karar günü konumuyla (i >= N) yazılır."

## 0. ÖN UÇUŞ KONTROLÜ (zorunlu, kod yazmadan önce oku)
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

## 1. YASAKLAR
- Şu dosyalara DOKUNMA: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md. Defter kaydını yalnız ana model yazar; sen önerdiğin metni raporuna yazarsın.
- git commit / push / branch / stash ile dalı değiştirme (yalnız okuma: git log, git diff, git show; eski kodu denemek için `git show HEAD:FON_IZI.py > /tmp/.../FON_IZI_eski.py` kullan, stash kullanma).
- Değiştirilecek dosyalar yalnız: FON_IZI.py, test_fon_izi.py ve raporun arastirma_cikti/fon_izi/GELECEK_DUZELTME_RAPOR.md. Başka dosya açma, yeni modül yazma.
- Çalışan kısma dokunma: yalnız aşağıdaki şartları değiştir; yeniden yazma, yeniden biçimleme, isim değiştirme yok. FON_IZI.py başındaki çakışma kapısını koru.
- Eşik / parametre değerleri (400, 400, 400, 400, 400, 400, L+200, 200) DEĞİŞMEZ; yalnız 'toplam uzunluk' şartı 'karar günü konumu' şartına çevrilir.
- E-posta, anahtar, token hiçbir dosyaya yazılmaz.

## 2. SORUN VE KURAL
Şu an: `n = len(d); if n < N: continue/return boş`. n serinin TOPLAM uzunluğu; serinin sonu gelecekte olduğu için, hissenin taranıp taranmaması gelecekteki bar sayısına bağlı (geleceğe bakma). Örnek: 600 barlık seride t=380'de sinyal çıkar; aynı seri t=390'da kesilirse (o gün tarama yapılsaydı) hisse 'n<400' diye atlanırdı -> sinyal yok.
Kural (sibling modüllerle aynı): bar indeksi t'deki sinyal / ölçü yalnız `t >= N - 1` ise üretilir (t dahil en az N bar geçmiş), serinin toplam uzunluğuna bakılmaz. Referans uygulamalar: K24_YENIDEN.py satır 205 (`X.t_i >= 200 - 1`), DIP_COL_AYRIM.py satır 182-189 (`i >= G[tur] - 1`), INTEM_ILERI.py SAPMA-1.
Sonuç: yeni kod eski kodun sinyallerinin ALT KÜMESİNİ verir (uzun serilerde t < N-1 bölgesindeki sinyaller düşer; kısa serilerden yeni sinyal çıkmaz). Bu davranış değişikliği raporda SAPMA olarak açıkça yazılır.
ÖNEKE DEĞİŞMEZLİK (asıl doğruluk şartı): herhangi bir T için, serinin [0, T] önekine uygulanan tarama ile tam seriye uygulanan taramanın T ve öncesi satırları birebir aynı olmalıdır (sonuç sütunları — yon60, yon20, r60 gibi ileriye bakan sonuç alanları — hariç; onlar gelecek veriyle hesaplanır ve NaN olabilir).

## 3. DEĞİŞECEK YERLER (FON_IZI.py, HEAD 9b30436 satır numaraları)
| # | Satır | Fonksiyon | Şu an | Olacak |
|---|---|---|---|---|
| 1 | 426 | fi_k4_olaylar | `if len(d) < 400: continue` | hisse atlanmaz; olay / ölçü yalnız bar konumu t >= 399 iken (fi_pencere çıktısındaki ok maskesi ya da olay döngüsü içinde konum şartı) |
| 2 | 466 | fi_k4b_hacim_olaylar | `if len(d) < 400: continue` | aynı: t >= 399 |
| 3 | 825 | fi_k6_evren | `if len(d) < 400: continue` | aynı: t >= 399 |
| 4 | 2528 | fi_k13_tara | `if n < 400: continue` + döngü `range(max(b1, 320), n)` | hisse atlanmaz; döngü alt sınırı `max(b1, 320, 399)` (yani t >= 399) |
| 5 | 2845 | fi_k14_esli | `if n < 400: continue` | aynı: eş aday günleri t >= 399 (fi_k13_tara ile aynı konum şartı, eş ile olay aynı kurala tabi olmalı: K1 kontrol grubu) |
| 6 | 3329 | fi_k17_tara | `if n < 400: continue` + döngü `range(max(b1, 320), n)` | döngü alt sınırı `max(b1, 320, 399)` |
| 7 | 4627 | fi_k23_parmak | `if n < L + 200: return boş` | boş dönüş yalnız `n < L` (pencere kurulamaz) iken; çıktı satırları `e >= L + 200 - 1` konumuna süzülür (on_m / on_v shift(L) ile 60 bar geriye bakar; süzgeç bunu zaten kapsar, kontrol et) |
| 8 | 4777 | fi_k24_tara | `if n < 200: return boş` | boş dönüş yalnız gerekli pencereler kurulamıyorsa (ör. n < 21); sinyal döngüsünde `t >= 199` şartı (K24_YENIDEN satır 205 ile birebir aynı anlam) |
Satır 1110 (`if n < 200:` _fi_metne PDF metin uzunluğu) BU HATAYLA İLGİSİZ, dokunma.
Her yerde: kısa seride artık 'continue' olmadığı için sonraki satırların (sliding_window_view, rolling, argmax dilimleri) boş / küçük dizide hata vermediğini doğrula; gerekirse en küçük teknik alt sınırı (pencere kurulabilsin diye) koru ve raporda yaz. Mevcut `try/except` blokları korunur.

## 4. TESTLER (test_fon_izi.py'ye ekle, mevcut stile uy: hata listesi, sayaç 62 -> yeni toplam)
- T1 ÖNEK DEĞİŞMEZLİĞİ: fi_k13_tara, fi_k17_tara, fi_k24_tara, fi_k23_parmak, fi_k4_olaylar, fi_k4b_hacim_olaylar, fi_k14_esli, fi_k6_evren (uygulanabilen hepsi; uygulanamayan varsa gerekçesiyle raporda) için sentetik uzun seri (>= 600 bar) üret; desen t ~ 380 (eski kodda sinyal verir, N=400 şartı altında) ve t ~ 450'de olsun; tam seri sonucu ile T = 390, 420, 470'te kesilmiş önek sonuçlarını (T ve öncesi satırlar, sonuç sütunları hariç) karşılaştır; birebir aynı olmalı.
- T2 ESKİ KOD KIRMIZI: aynı testi `git show HEAD:FON_IZI.py` ile çıkarılan eski dosyaya karşı çalıştır (ayrı geçici dizinde, -I olmadan, modül adını çakıştırmadan; çakışma kapısına dikkat: aynı yorumlayıcıda iki FON_IZI yükleme, ayrı süreç kullan) ve en az fi_k13_tara / fi_k24_tara / fi_k23_parmak için eski kodun T1'i GEÇMEDİĞİNİ raporda göster (çıktıyı yapıştır). Yeni kodun geçtiğini göster.
- T3 MEVCUT TESTLER: `python test_fon_izi.py` 62 eski test + yenileri tamamı OK. Ayrıca FON_IZI'yi içe alan her test dosyasını bul (`grep -l "FON_IZI" test_*.py`) ve çalıştır; veri gerektirip çalışmayanları raporda 'VERİ YOK, KOŞMADI' diye yaz.
- Test 30 (d30, 300 bar, t=226) yeni şartla da geçmeli (226 >= 199 ve 226 >= 15+200-1); geçmiyorsa testi değil kodu sorgula ve raporda yaz.

## 5. GERÇEK VERİ ETKİ SAYIMI (denemeye değer; olmazsa 'SAYILMADI' yaz)
- Veri: `git worktree add /tmp/iv origin/islenmis-veri` (yalnız okuma, dal değişmez) ve `python FON_IZI.py vpac /tmp/iv/veri /tmp/veri` -> V_BIST.pkl, V_ABD.pkl (yapı: FON_IZI içinde `fi_k1_veri` çıktısı; nasıl yüklendiğini koddan bul).
- Eski (HEAD kopyası) ve yeni kodla fi_k13_tara (FI_K13_ESIK), fi_k17_tara, fi_k24_tara (her hisse), fi_k23_parmak(L=15) satır sayılarını BIST ve ABD için say; tablo: fonksiyon x pazar x (eski n, yeni n, düşen n, düşen %). Fiyat kesiği 31.08.2026 (kriz kuralı) — kesiği uygula ve raporda yaz.
- Beklenti (önceden yazılı): yeni <= eski her hücrede; K24 ABD+BIST düşen ~1.430 civarı (H satırındaki sayıyla kıyasla, farkı yorumla). Beklentiye uymayan sayı varsa HATA başlığına yaz.
- Getiri ölçümü, cetvel, karar YOK: eski çalışmaların kararları değişmez (yeniden koşular K24_YENIDEN / DIP_COL_AYRIM / INTEM_ILERI'de zaten yapıldı).

## 6. SÜRÜM VE NOT
- FI_SURUM dizesini "FON_IZI v1.40 (2026-11-15, geleceğe bakma düzeltmesi: tarayıcı seri uzunluğu şartı karar günü konumuna alındı (fi_k4 / k4b / k6 / k13 / k14 / k17 / k23_parmak / k24); ..." biçiminde güncelle, eski metni sonuna ekle (sil değil).
- Değişen her satırın yanına kısa yorum: `# 15 Kas: toplam uzunluk değil karar günü konumu (geleceğe bakma, H satırı 14 Kas)`.

## 7. RAPOR (arastirma_cikti/fon_izi/GELECEK_DUZELTME_RAPOR.md; zorunlu başlıklar)
1. ÖZET (3-5 satır, bulgu dili: ne değişti, kaç test, kaç sinyal düştü)
2. DEĞİŞEN SATIRLAR (satır no, eski -> yeni, 8 yer + varsa teknik alt sınır)
3. SAPMA (davranış değişikliği: t < N-1 sinyalleri düşer; eski karar kayıtlarına etkisi yok, gerekçe)
4. KONTROL LİSTESİ (K1-K14 tablo: Kod | Madde | Yanıt EVET / UYGULANMAZ | Kanıt (>= 8 karakter)); K2 için kanıt T1 + T2 çıktısı
5. TEST (T1 tasarımı, T2 eski kırmızı / yeni yeşil çıktıları, T3 sonuçları, toplam sayaç)
6. GERÇEK VERİ SAYIMI (tablo) ya da SAYILMADI + neden
7. HATA (bu işte bulduğun her hata: kodda, testte, iş tanımında, veride; yoksa 'bulunmadı' yaz)
8. ÖNERİLEN DEFTER METNİ (ana model işler): IK_HATA 2026-11-14 satırına düzeltme notu; IK_GOREV satırı önerisi; Colab hatırlatması ('kod değişti, çalışma zamanını yeniden başlat')
9. DOKUNULAN DOSYALAR (git status --short çıktısı)
