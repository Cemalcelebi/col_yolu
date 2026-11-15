# İŞ TANIMI — T8 'uzun çöl' (D9) etiketinin üretim ekranından kaldırılması (Cemal, 15 Kas 2026: "UZUN ÇÖL ETİKETİNİ KALDIR")

Yazan: ana model. Yapan: alt ajan (yazıcı). Denetleyen: ayrı alt ajan (bağımsız sınayıcı) + ana model. Üretim kodu değişikliğidir.
Dayanak: Ç181a (14 Kas) D9 uzun çöl İZ DEĞİL (ABD n 2.399 / 4.556, AVR 1.102 / 2.102; 4 hücre tutmadı; sakin hisse seçer). Ç181b D9 + rüzgâr ÖLÇÜLEMEDİ. Ç181c YALNIZ SEKTÖR RÜZGÂRI EMARE (ABD 2024-26 dört şartın üçü) -> RÜZGÂR EKRANDA KALIR, yalnız 'uzun çöl' etiketi ve ona bağlı hisse listesi kalkar.

## 0. ÖN UÇUŞ KONTROLÜ (zorunlu)
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
- Dokunma: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, D9_YENIDEN.py, ORTAK_CETVEL.py, test_d9_yeniden.py.
- git commit / push / stash / checkout yok (yalnız okuma). E-posta / anahtar yazılmaz.
- Değişecek dosyalar YALNIZ: COL_v1.py, takip.py, test_takip.py ve rapor arastirma_cikti/d9_yeniden/T8_KALDIR_RAPOR.md.
- COL_v1.py içinde uzun_col_olc, UZUN_W / UZUN_BANT / UZUN_MUM / UZUN_KONUM, sektor_ruzgar, RUZ_* sabitleri, SEKTOR_DOSYALAR DEĞİŞMEZ (test_d9_yeniden bunları COL_v1'in kendisiyle birebir karşılaştırır: 'D9_PARAM == COL_v1 sabitleri', 'd9_uzun_ref == COL_v1.uzun_col_olc'). Fonksiyon ölçüm referansı olarak kalır; yalnız ekrandan ve listelerden ÇAĞRISI kalkar.
- Çalışan kısma dokunma: yalnız aşağıdaki yerler. Çakışma kapıları korunur. Yeniden yazma / biçimleme yok.

## 2. DEĞİŞECEK YERLER
1. takip.py gun(): BEKLE tablosu başlığı "(hisse  tavana%  girilecek%  doji  fitil  uzun  ruz%)" -> 'uzun' sütunu kalkar; satırlarda ucl basılmaz; _uz_rz artık uzun_col_olc çağırmaz (yalnız ruz, var döner; adı _rz yapılabilir). ruz% ve ' RUZGAR' bayrağı AYNEN kalır.
2. takip.py gün sonu: RUZGAR_LISTE bloğu kalır ama artık COL_v1'in yeni ruzgar_listesi'ni (sektör özeti) çağırır.
3. COL_v1.py ruzgar_listesi: D9 süzgeci (uzun_col_olc) ve "uzun colde (dipte, ...) N hisse" tablosu KALKAR; sektör rüzgârı özeti (başlık, sektör sepeti, piyasa farkı, üyeler, AZ DUSEN) KALIR; başlık "=== D9 RUZGAR LISTESI" -> "=== SEKTOR RUZGARI" ; docstring güncellenir; dönüş: rüzgârlı sektör tablosu (alt, sepet, ruz, uye) — çağıranlar dönüşü kullanmıyor, kontrol et (grep). Fon süzgeci artık hisse listesi olmadığı için uygulanmaz; FON_ELE başka yerde değişmez.
4. COL_v1.py bugun_liste (satır ~851-854): 'uzun' sütunu için uzun_col_olc çağrısı kalkar. ŞEMA: 'uzun' anahtarını okuyan her yeri grep et (takip.py, gh_gunluk.py, takip_adaylar.csv başlıkları, rapor yazımı); bir CSV / pkl şeması bu sütunu taşıyorsa sütun boş dize olarak KALIR (okuyucular kırılmasın), yalnız hesap ve ekran kalkar; şema taşımıyorsa sütun tamamen kalkar. Hangisini yaptığını raporda yaz.
5. Başlık yorumları: COL_v1.py dosya başına "D14) 2026-11-15: D9 uzun çöl etiketi ve ruzgar_listesi'ndeki uzun çöl hisse listesi üretim ekranından kaldırıldı (Ç181a İZ DEĞİL; Cemal 'uzun çöl etiketini kaldır'); uzun_col_olc ölçüm referansı olarak kalır; sektör rüzgârı (Ç181c EMARE) kalır" notu; takip.py başına T12 notu aynı içerikte; her iki dosyanın [ok] print satırına kısa ek ("D14/T12: uzun çöl etiketi kaldırıldı").
6. Bu dosyalar Colab'da exec ile yüklenir: raporda "çalışma zamanını yeniden başlat" hatırlatması; Drive kopyalarını (COL_v1.py, takip.py; col_tarayici kökü) ANA MODEL günceller, sen dokunma.

## 3. TESTLER
(DÜZELTME 15 Kas, ana model: bu bölümün ilk sürümü kabuk heredoc'unda ters tırnaklar çalıştığı için test çıktılarıyla bozulmuştu; alt ajan amacı doğru anlayıp uyguladı. Aşağıdaki metin asıl istenendir; hata defterine girdi.)
- test_takip.py mevcut testler geçmeli (SONUC: HEPSI OK). Yeni test(ler): (a) gun() çıktısında BEKLE başlığında 'uzun' YOK, 'ruz%' VAR; (b) ruzgar_listesi çıktısında 'uzun colde' geçmez, 'SEKTOR RUZGARI' geçer; (c) uzun_col_olc ve UZUN_* sabitleri hâlâ COL_v1'de ve değişmedi.
- test_d9_yeniden.py geçmeli (SONUC HEPSI OK); COL_v1 / takip kullanan öteki test dosyaları (grep ile bulunur) koşturulur; veri gerektirenler 'VERİ YOK, KOŞMADI' diye yazılır.
- Sözdizimi: COL_v1.py ve takip.py ast.parse ile temiz (BASLAT.py / gh_gunluk.py bu dosyaları exec eder).

## 4. RAPOR (arastirma_cikti/d9_yeniden/T8_KALDIR_RAPOR.md; zorunlu başlıklar)
1. ÖZET  2. DEĞİŞEN SATIRLAR (eski -> yeni)  3. ŞEMA KARARI ('uzun' sütunu)  4. KONTROL LİSTESİ (K1-K14; yanıt + kanıt)  5. TEST (çıktı son satırları)  6. HATA (bulduğun her hata; yoksa 'bulunmadı')  7. ÖNERİLEN DEFTER METNİ (IK_GOREV satırı; ana model işler)  8. DOKUNULAN DOSYALAR (git status --short, git diff --stat)
