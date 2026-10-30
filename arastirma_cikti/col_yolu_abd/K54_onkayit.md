# K54 — ÖN KAYIT: Tarihsel hisse evreni sağlamlık denetimi (30 Ekim 2026, sonuç görülmeden)

K54 yeni bir iz araştırması değildir; K51, K52 ve K53 sonuçlarının tarihsel şirket evrenindeki eksikliklerden etkilenip etkilenmediğini sınar. K51 / K52 / K53 ön kayıtları, eşikleri ve kararları **değişmez**; K51 İZ DEĞİL kalır. Eski sonuç dosyaları silinmez ve üzerine yazılmaz (K54 kendi dosyalarını üretir; eski ve yeni değerler aynı tabloda yan yana saklanır).

## 1. Kaynaklar (hepsi ücretsiz; Tiingo fiyat kotası kullanılmaz)

- Fiyat serileri: mevcut K51 evreni (3.267 sembol: V_ABD 1.410, K34 Yahoo 1.435, K34 Tiingo 422; `K51_EVREN_PIT.csv`).
- **Tiingo desteklenen sembol listesi** (`supported_tickers.csv`, 30 Ekim 2026 çekimi): sembol, borsa, varlık türü, başlangıç ve **bitiş tarihi** (borsadan çıkanlar dahil). Bu liste fiyat verisi değildir; yalnız son işlem tarihi ve borsa bilgisi için kullanılır. Tiingo fiyat verisi eksik analist kayıtlarının yerine konmaz.
- **SEC başvuru geçmişi** (`data.sec.gov/submissions/CIK##########.json`, 30 Ekim 2026): form türleri, başvuru tarihleri, 8-K madde kodları, güncel semboller ve borsalar, eski adlar, SIC. SEC kuralı gereği iletişim e-postası yalnız bu indirmede kullanılır; koda ve repoya yazılmaz.
- **SEC sembol-şirket haritası** (`company_tickers.json`, 30 Ekim 2026): bugünkü sembol → CIK.
- Şirket kimliği: K34 için `k34_evren.csv` CIK'i; V_ABD için company_tickers.json (bugünkü sembol → CIK; eşleşmeyen sembol "kimlik doğrulanamadı").
- K52 analist günlüğü (Yahoo) kapsama tablosu; K52 / K53 olay dosyaları (`K51_ANALIST_REVIZYONLARI.csv.gz`, `K53_OLAYLAR.csv.gz`).

## 2. Şirket durumu sınıflandırması (kurallar sabit; belirsiz zorla sınıflanmaz)

T = fiyat serisinin son günü (K51 evreni). "Erken bitti" = T < 2026-08-01 (K51 `alive_sinir`). SEC sinyalleri (başvuru geçmişinden):
- B_1.03 = 8-K madde 1.03 (iflas / kayyum) başvurusu; B_2.01 = 8-K madde 2.01 (varlık edinimi / elden çıkarma tamamlanması); 25-NSE = borsadan çıkarılma bildirimi; 15-12G / 15-12B / 15-15D = kayıttan çıkma; DEFM14A / SC TO-T / SC 14D9 / S-4 / 425 = birleşme-teklif belgeleri; son 10-K / 10-Q tarihi.

Sıralı kurallar (ilk uyan sınıf atanır):
1. **Halen işlem gören:** seri erken bitmemiş VE (Tiingo listesinde bitiş ≥ 2026-08-01 VEYA SEC güncel sembolleri bizim sembolü içeriyor).
2. **İflas / tasfiye:** seri erken bitmiş VE [T−365 gün, T+365 gün] içinde B_1.03 var.
3. **Birleşme / satın alma:** seri erken bitmiş VE B_1.03 yok VE ([T−120, T+120] içinde B_2.01 VEYA 25-NSE) VE [T−400, T+60] içinde birleşme-teklif belgesi (DEFM14A / SC TO-T / SC 14D9 / S-4 / 425) var.
4. **Sembol değiştiren / başka şirkete dönüşen:** seri erken bitmiş VE şirket T'den ≥ 180 gün sonra 10-K / 10-Q vermeye devam ediyor (şirket yaşıyor, serimiz bitmiş: sembol değişimi / kod yeniden kullanımı) VEYA bugünkü sembol company_tickers'ta başka bir CIK'e bağlı. Eski-yeni sembol ilişkisi: SEC güncel semboller ve eski adlar kaydedilir.
5. **Veri sağlayıcısında kaybolan, durumu belirsiz:** seri erken bitmiş, yukarıdakilerin hiçbiri yok (örn. yalnız 15-12G ile kayıttan çıkma: özelleşme mi, iflas mı belli değil; başvurular T'den sonra sessizce kesilmiş; pembe tahtaya inmiş).
6. **İşlem geçmişi doğrulanamayan:** CIK bulunamadı VEYA SEC başvuru geçmişi indirilemedi VEYA Tiingo listesinde ve SEC'te sembol hiç yok.
Her şirket için: son işlem tarihi (T), Tiingo bitiş tarihi, delist bildirim tarihi (25-NSE varsa), CIK, SEC güncel semboller, eski adlar, sınıf kanıtı (hangi kural, hangi tarihler). Belirsiz kayıtlar ne iflas ne aktif sayılır.

## 3. "Düzeltilmiş evren" (sonuç görülmeden sabit)

K51 etiket kuralı (giriş ertesi açılış, +%20 / −%10 / 60 gün, delist: son kapanış, son 60 gün getirisi negatifse ek −%30) **eski sonuçta aynen kalır**. Düzeltilmiş evrende yalnız çıkış işlemi şirket sınıfına göre değişir:
- Sınıf 1: değişmez.
- Sınıf 2 (iflas / tasfiye): seri sonunda tam kayıp (ek −%100; panelde `y_d100`).
- Sınıf 3 (birleşme / satın alma): ek kayıp yok (son kapanış = alınan bedel; `y_d0`).
- Sınıf 4 (sembol değişimi / kod yeniden kullanımı): seri, şirketin son 10-K / 10-Q tarihi + 120 gün ile kesilir (`y_kes`); kesimden sonraki günler evrenden çıkar.
- Sınıf 5 (belirsiz): K51 kuralı kalır (ek −%30); ayrıca −%0 / −%100 bandı duyarlılık tablosunda yazılır.
- Sınıf 6 (doğrulanamayan): düzeltilmiş evrenden **tamamen çıkarılır** (tabandan da).
- Taban e_y düzeltilmiş evrende (sınıf 6 çıkarılmış, düzeltilmiş etiketlerle) yeniden hesaplanır.

## 4. Karşılaştırılacak testler ve ölçüler (aynı tanım ve eşikler)

Her test için üç sütun: eski evren, düzeltilmiş evren, fark (düzeltilmiş − eski). Ölçüler: n olay, +%20'ye ulaşma oranı, −%10'a ulaşma oranı, zaman aşımı oranı, net getiri, taban-ayarlı isabet (y − e_y), ay kümeli %95 aralık, dönem başına (2016-22, 2023, 2024-26), en iyi 20 hisse çıkarılmış sonuç.
1. **K51 P1 / P2 / ES / HT temel hücreleri** (v1.2 tanımları; `cy_v12_hisse` bayrakları).
2. **Üçlü bariyer ve delist duyarlılığı:** sınıf başına olay sayısı ve P1 / P2 hücrelerinin −%0 / −%30 / −%100 bandı; sınıf 5 ve 6 payı.
3. **Küçük mum (H-B), hacim kuruması (H-C), hacimli taban (H-D)**: K51 v1.2 tanımlarıyla olay − eşleşmiş kontrol farkı; eşleştirme havuzu düzeltilmiş evren. **BB sıkışması ve EMA deneyleri (K48 / FON_IZI)** yalnız bugün işlem gören V_ABD evreninde koşmuştu ve o kod K34 evrenini almaz; bunlar yeniden koşulmaz, "GEÇERSİZ (evren yeniden kurulamıyor: yalnız hayatta kalanlar)" diye sınıflanır ve nedeni yazılır.
4. **Sessiz ML (K51 meta-etiketleme):** P1 olaylarında LightGBM (K51 ile aynı özellik kümesi: panel özellikleri vol60, log_dv20, dd250, r60, ar20, imza, hacim_ok, trend + rejim), yıl yıl ileriye yürüyen eğitim (eğitim: önceki yıllar, test: yıl; 2019-2026), ölçü: test yılı AUC ve model üst üçte biri − alt üçte biri isabet farkı; eski ve düzeltilmiş evrende aynı tohum ve ayarlarla. CNN / LSTM yeniden koşulmaz (K51'de zaten katkısızdı; süre), "yeniden koşulmadı" yazılır.
5. **K52 / K53 özel denetimi:** Yahoo analist kapsaması sınıf başına; analist verisi olmayan batık şirketler "analist verisi yok" (sıfır revizyon değil). K52 H0 (P1 / P2, G1 − G2a) ve K53 T1 / T5 / T6 hücreleri kaydedilmiş olay dosyalarından düzeltilmiş etiketlerle yeniden hesaplanır; sınıf 6 olayları çıkar. Sonuçların yalnız Yahoo kapsamındaki (çoğu hayatta kalan) şirketler için geçerli olduğu açıkça yazılır.

## 5. Değerlendirme sınıfları (sabit)

Her test için:
- **SAĞLAM:** birincil ölçü (taban-ayarlı isabet farkı) düzeltilmiş evrende eskiye göre en çok 2 puan değişiyor VE karar (TUTAR / TUTMAZ / DESTEKLENMİYOR) her dönemde aynı VE %95 aralıklar örtüşüyor.
- **ETKİLENMİŞ:** fark 2 puandan büyük VEYA herhangi bir dönemde karar değişiyor VEYA aralık işareti değişiyor.
- **GEÇERSİZ:** testin tarihsel evreni güvenilir biçimde kurulamıyor: evrendeki sınıf 5 + 6 payı olayların %30'undan fazla, VEYA test yalnız hayatta kalan evrende koşmuş ve kodu K34 evrenini alamıyor (BB sıkışması, EMA, K48 / K49 / K50 deneyleri).
K51 kararı hiçbir sınıfta değişmez; K54 yalnız güvenilirliği etiketler.

## 6. Çıktılar

K54_EVREN_ESLESTIRME.csv (sembol, kaynak, CIK, SEC güncel semboller, eski adlar, Tiingo borsa / başlangıç / bitiş, analist kaydı var mı), K54_SIRKET_DURUMU.csv (sınıf, kural, T, Tiingo bitiş, 25-NSE tarihi, son 10-K/10-Q, 8-K 1.03 / 2.01 tarihleri, kesim tarihi), K54_ESKI_YENI_TEST_KARSILASTIRMA.csv, K54_DELIST_DUYARLILIK.csv, K54_RAPOR.md. Kod: COL_YOLU_ABD.py v1.5 (`cy_v15_calistir`), test_col_yolu_abd.py ekleri (sınıflandırma kuralları sentetik başvuru geçmişiyle). Ham SEC başvuru geçmişleri repoya konmaz (özet CSV konur).

## 7. Açıklama (kod yazılırken, sonuç görülmeden; 30 Ekim 2026)

Sınıf 4 iki alt duruma ayrılır: **4a sembol değişimi** (serimiz T'de bitmiş, şirket SEC'e 10-K / 10-Q vermeye devam ediyor; hisse başka sembolle işlem görmüş) → çıkışta ek kayıp yok (`y_d0`), çünkü seri sonu borsadan çıkış değil veri kesintisidir. **4b kod yeniden kullanımı** (bugünkü sembol company_tickers'ta başka CIK'e bağlı ve serimiz şirketin son 10-K / 10-Q tarihinden sonra da sürüyor) → seri son 10-K / 10-Q + 120 gün ile kesilir (`y_kes`), kesimden sonraki günler çıkar. Her ikisi de "sembol değiştiren / başka şirkete dönüşen" sınıfında raporlanır.
Sessiz ML özellikleri (sabit): vol60, log_dv20, dd250, r60, ar20, imza, hacim_ok, trend, rejim (BOĞA = 1). LightGBM ayarları K51 `meta.lgbm`; tohum 515; yıllar 2019-2026; embargo 10 gün (çıkış tarihi eğitim yılı başından önce).

## 8. EK — Kodlama öncesi zorunlu metodoloji düzeltmeleri (Cemal, 30 Ekim 2026; düzeltilmiş koşunun sonucu görülmeden yazıldı)

İlk K54 koşusu (commit ac63f0d; çıktıları git geçmişinde) görülmüştü. Bu ek, düzeltilmiş koşu başlamadan önce commit'lenir; yukarıdaki 1-7 bölümleri, eşikler (n ≥ 30, Δ ≥ 0,05, SAĞLAM ≤ 2 puan, GEÇERSİZ > %30) ve karar kuralları **değişmez**. K51 İZ DEĞİL kalır.

1. **Sınıf 1 doğrulaması.** SEC güncel sembolü tek başına aktif işlem kanıtı sayılmaz. Her sınıf 1 kaydına `dogrulama` yazılır: "Tiingo + SEC" (Tiingo bitiş ≥ 2026-08-01 ve SEC güncel semboller bizimkini içeriyor), "yalnız Tiingo" (SEC sembol listesi boş; çelişki yok), **belirsiz**: "yalnız SEC, Tiingo bitiş çelişiyor" (Tiingo bitiş < sınır), "yalnız SEC, Tiingo'da yok", "Tiingo tamam, SEC sembolü farklı". Belirsiz kayıtlar sınıf 1'de kalır (seri 2026-08-01 sonrasına sürdüğü için çıkış işlemi yok) ama sayısı raporlanır ve K51 P1 / P2 hücreleri bu kayıtlar çıkarılarak ayrıca hesaplanır (duyarlılık satırı).
2. **Sınıf 2 kronolojisi.** 8-K madde 1.03 başvurusunun T'ye göre zamanı sembol başına yazılır: `b103_T_fark_gun` (başvuru − T, gün), `b103_zaman` ("T'den N gün önce / sonra / aynı gün"), pencere içindeki bütün 1.03 tarihleri. Sınıf atanması değişmez; rapor sınıf 2'de T öncesi / sonrası dağılımını verir.
3. **Sınıf 4a çıkış değeri.** Başka sembolle devam eden şirkette eski sembolün son kapanışı otomatik nakit bedel sayılmaz (`y_d0` kaldırıldı). Doğrulama (`cy_v15_4a_dogrula`): SEC güncel sembollerinden biri evrende VE yeni seri T'nin ±30 takvim günü içinde başlıyor VE oran = eski son kapanış / yeni ilk kapanış 1'den en çok %2 sapıyor (1:1 sembol değişimi) → "doğrulandı", fiyat serisi bağlanır (eski seri + T sonrası yeni seri; etiket bağlı seriden, çıkış işlemi yeni sembolün sınıfına göre). Aksi halde "doğrulanamadı (belirsiz)": ana sonuçta K51 kuralı (son kapanış, son 60 gün negatifse −%30) uygulanır ve −%0 / −%30 / −%100 bandı ayrı duyarlılık satırında raporlanır. Kurumsal işlem oranı 1:1 dışındaysa dış kaynak olmadığı için doğrulanmış sayılmaz.
4. **Sınıf 6 duyarlılığı.** Ana sonuç sınıf 6 çıkarılmış evrendir (değişmedi). Ek olarak sınıf 6 dahil edilip çıkışta −%30 (K51 kuralı) ve −%100 varsayılan iki sonuç K51 temel hücreleri için ayrıca üretilir (`kume` eki "(sınıf 6 −%30 dahil)" / "(sınıf 6 −%100 dahil)"). Raporda sınıf 6'nın olası başarısız şirketleri dışarıda bırakmasından ve evrende hiç bulunmayan batık şirketlerden doğan hayatta kalma yanlılığı ayrı başlıkta tartışılır.

**Ortak örneklem (her testte üç karşılaştırma).** A = eski evrenin kendi örneklemi (K51 etiketi ve tabanı). B = düzeltilmiş evrenin kendi örneklemi (düzeltilmiş etiket ve taban). C = iki evrende ortak kalan sembol × tarih satırları; C üzerinde iki hesap: C-eski (K51 etiketi, taban ortak satırlarda yeniden) ve C-yeni (düzeltilmiş etiket, taban ortak satırlarda yeniden). Ayrıştırma: **evren etkisi** = C-eski − A, **etiket etkisi** = C-yeni − C-eski, **toplam** = B − A (taban-ayarlı isabet farkı, puan). Uygulandığı testler: K51 P1 / P2 / ES / HT / ÇEK, H-B / H-C / H-D (eşleştirme havuzu her örneklemde ayrı), K52 H0 ve K53 T1 / T5 / T6 (kayıtlı olay dosyaları; C-eski = düzeltilmiş evrende kalan olaylar, eski etiket), sessiz ML. SAĞLAM / ETKİLENMİŞ / GEÇERSİZ değerlendirmesi yine A ile B arasında yapılır (bölüm 5).

**ML.** Eski (A), düzeltilmiş (B), ortak-eski ve ortak-yeni örneklemlerinde aynı özellikler (bölüm 7), aynı etiket tanımı, eğitim / test yılları 2019-2026 (eğitim: çıkış tarihi test yılı başından 10 gün önce biten olaylar), eksik değer yöntemi (LightGBM yerel), `meta.lgbm` ayarları ve tohum 515 sabit. Ölçü: yıl AUC, toplam AUC, model üst üçte biri − alt üçte biri taban-ayarlı isabet farkı.

Ek çıktılar: K54_SIRKET_DURUMU.csv'ye `dogrulama`, `b103_T_fark_gun`, `b103_zaman`, `b103_tarihler`, `yeni_sembol`, `baglama` sütunları; K54_ESKI_YENI_TEST_KARSILASTIRMA.csv'ye `ortak_eski_*`, `ortak_yeni_*`, `evren_etkisi`, `etiket_etkisi` sütunları ve duyarlılık satırları; K54_DELIST_DUYARLILIK.csv'ye sınıf 4a bandı. Testler: test_col_yolu_abd.py 28 güncellenir, 30 (sınıf 1 doğrulama, sınıf 2 kronoloji, 4a doğrulama) ve 31 (ortak örneklem ayrıştırma aritmetiği) eklenir.
