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
