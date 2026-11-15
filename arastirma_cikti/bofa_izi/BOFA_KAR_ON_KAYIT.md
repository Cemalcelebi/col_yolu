# BofA KÂRI VE HABER SONRASI YOL — ÖN KAYIT (getiri hesaplanmadan önce)

BOFA_IZI KÂR v1.0 (bofa_kar_20261113): BofA'nın kendi maliyetinden getirisi (A, betimleyici) + haber sonrası giriş yolu, 6 koşul (B, ön kayıtlı). Yazılma 2026-11-13 16:38:01 UTC. Bu dosya git'e işlenmeden ve mühürler tutmadan `python BOFA_IZI.py karkos` çalışmaz.

## Soru

A) BofA yayımlanan kendi ortalama maliyetinden kâr ediyor mu, nerede ediyor (betimleyici)? B) BofA'nın alımları haber yayımlandığı anda bilinen bilgiyle ayrılabilir mi ve Cemal haber saatinden sonra girerek bunun bir kısmını yakalayabilir mi (karar)? Kaynak: Cemal 13.11.2026 itirazı ('BofA bir hissede %40-80 zarar etmez'; listedeki 'BofA' bir aracı kurum akışıdır, liste ilk 5-10 ile sınırlıdır).

## Ne ölçülecek

- A (betimleyici): her geçerli, maliyetli BofA ALIM satırında BofA'nın yayımlanan maliyetinden 5 / 20 / 60 işlem günü getirisi; aynı gün aynı hücredeki eşlerin tipik fiyattan getirisi; eşli fark; kırılımlar; FIFO eşlemeyle gerçekleşen kâr ve kapsam; satış satırları BİLGİ.
- B (karar): BofA alım ilk 3 tetiği, 6 koşul (K1..K6) + TÜMÜ = 7 satır; ANA yol G1 + C1; FI_OLCUT dört şartı + iki alt dönem + BH q = 0,10.
- B BİLGİ: G1C2, G2C1, G2C2; düz yazı hariç; tamamlayıcılar; ikincil FI_OLCUT 60 gün; 20 gün P(+%50) / P(-%30) ve eş katları; kriz sonrası açık dönemler.

## Tanımlar ve eşikler (BK_ESIK; değişmez)

```json
{
 "A": {
  "cokmus": -0.6,
  "donem": [
   [
    "2023-24",
    "2023-01-01",
    "2024-12-31"
   ],
   [
    "2025-26",
    "2025-01-01",
    "2026-08-31"
   ]
  ],
  "fifo": "aynı hissede geçerli, maliyetli, LOT birimli gün içi / gün sonu satırları (A tekilleştirmesi, alım ve satım) yayın sırasıyla; alımlar kuyruğa (lot, maliyet), satışlar en eski alımdan eşlenir. Eşleşme getirisi = satış maliyeti / alış maliyeti - 1; gerçekleşen TL = lot x (satış - alış); tutma günü = işlem günü farkı; KAPSAM = eşlenen lot / alınan lot; eşleşmeyen satış lotu ayrı sayılır; kalan alımlar son kapanışla BİLGİ. Aynı yayın anında alım önce. Kriz: satış veri günü <= 31.08.2026 / sonrası ayrı",
  "fiyat_kova": [
   2.0,
   10.0,
   50.0
  ],
  "getiri": "her geçerli, maliyetli ALIM satırı (tekilleştirilmiş): r_k = Kapanış(veri günü + k işlem günü) / BofA maliyeti - 1, k = 5, 20, 60 (işlem günü takvimi bi_takvim; kapanış en çok 5 gün ileri taşınmış)",
  "kirilim": "fiyat kovası (maliyet < 2 TL, 2-10, 10-50, > 50); çökmüş (veri gününden önceki kapanış / önceki 250 günün en yüksek kapanışı - 1 <= -0,60, en az 120 bar) / değil; birim lot / TL; BofA payı >= %20 / < %20 / yazılı değil; dönem 2023-24 / 2025-26 (pencere sonu <= 31.08.2026); kriz sonrası (veri günü >= 01.09.2026) BİLGİ",
  "kontrol": "aynı veri günü, aynı FI_OLCUT momentum beşliği x likidite üçlüsü hücresindeki (bi_panel H; hisse kendisi hariç, en az 3) öteki hisselerin veri günü tipik fiyatı (H + L + C) / 3'ten Kapanış(veri günü + k)'ya getirisi; eş ortalaması; EŞLİ FARK = r_k - eş ortalaması. Eşlerin P(>= +%30) ve P(<= -%30) oranları da (kat = olay / eş)",
  "kriz": "ana A tablosu: pencere sonu (veri günü + k) <= 31.08.2026; veri günü <= 31.08 < pencere sonu 'kesik aşan' (sayılır, girmez); veri günü >= 01.09.2026 'kriz sonrası' BİLGİ (penceresi veride bitenler)",
  "olcu": "kâr oranı P(r_k > 0), medyan, ortalama, P(r_k >= +%30), P(r_k <= -%30), ortalama / medyan eşli fark, eş ortalaması",
  "pay_esik": 20.0,
  "satis_bilgi": "BİLGİ: geçerli maliyetli SATIM satırlarında işaretli getiri -(Kapanış(veri günü + k) / maliyet - 1) (BofA'nın sattıktan sonra kaçındığı düşüş pozitif)",
  "uc": 0.3,
  "ufuk": [
   5,
   20,
   60
  ]
 },
 "B": {
  "K1_pay": 20.0,
  "K2_kovalama": 0.05,
  "K3_en_az": 2,
  "K3_gun": 5,
  "K4_gun": 20,
  "K4_sira": 5,
  "K5_cokmus": -0.6,
  "K6_birim": "lot",
  "ana": "G1C1",
  "c2_gun": 20,
  "cikis": {
   "C1": "BOFA_IZI tutma dönemi kuralı: G1 giriş anından SONRA yayımlanan ilk BofA satış listesi haberinde (gün içi / gün sonu / haftalık; BOFA_IZI.bi_liste_hazirla satırları, blok 1) hisse ilk 5'te -> o yayından sonraki ilk açılış (durdurmada 5 gün içindeki ilk açılış, o da yoksa kapanış); satış haberi yoksa G1 giriş günü + 250 işlem günü açılışı; veri sonunda hâlâ açıksa 'açık'",
   "C2": "sabit 20 işlem günü: açılış girişinde giriş günü + 19, kapanış girişinde giriş günü + 20 işlem günü KAPANIŞI"
  },
  "cikis_sira": 5,
  "cikis_tur": [
   "gun_ici",
   "gun_sonu",
   "haftalik"
  ],
  "g1_saat": "17:30",
  "giris": {
   "G1": "tetik gün içi haberi ve yayın veri gününde 17:30 TR'den önce -> veri günü KAPANIŞI (giriş anı 18:10); değilse yayından sonraki ilk işlem günü AÇILIŞI (bi_giris_gunu; giriş anı 10:00)",
   "G2": "her zaman yayından sonraki ilk işlem günü açılışı (bi_giris_gunu)"
  },
  "giris_sira": 3,
  "kosul": {
   "K1": "BofA günlük hacim payı >= %20 (tetik satırında pay yazılı)",
   "K2": "kovalamama: G1 giriş fiyatı / tetik satırındaki BofA maliyeti - 1 <= +%5 (maliyet yazılı)",
   "K3": "birikim: veri günü dahil son 5 işlem gününde (veri günü - 4 .. veri günü) en az 2 FARKLI veri gününde geçerli gün içi / gün sonu alım listesinde ilk 3; önceki günler yalnız tetik yayınından ÖNCE yayımlanmış haberlerden",
   "K4": "dönüş: tetik yayınından ÖNCE ve veri gününden 20 işlem günü önceki gün 00:00'dan SONRA yayımlanmış bir BofA satış listesi haberinde (C1'deki satış satırları, her tür) hisse ilk 5'te",
   "K5": "çökmüş: G1 giriş gününden önceki kapanış / önceki 250 günün en yüksek kapanışı - 1 <= -0,60 (bi_panel dd)",
   "K6": "lot sıralı liste (tetik satırı birim lot)"
  },
  "olay": "her koşul (ve TÜMÜ) için ayrı olay kümesi: koşulu sağlayan tetikler hisse başına yayın sırasıyla; tetik bir dönem açar, dönem açıkken (tetik yayını <= çıkış haberi yayını / 250. gün / veri sonu) gelen tetikler yeni dönem açmaz. Olay kümesi ANA yolla (G1 + C1) kurulur; G1C2, G2C1, G2C2 aynı olayların başka giriş / çıkış uygulamasıdır (BİLGİ). Tamamlayıcı = koşul bilinen ve sağlanmayan tetikler (BİLGİ); koşulu bilinmeyen (pay / maliyet yazılı değil, çökmüşlük ölçülemiyor) tetik ikisine de girmez",
  "olcu": "BOFA_IZI dönem ölçüsü (bi_donem_ozet ile aynı tanım): getiri = çıkış fiyatı / giriş fiyatı - 1; eş = giriş günü aynı FI_OLCUT momentum beşliği x likidite üçlüsü hücresindeki öteki hisseler, AYNI giriş (açılış ya da kapanış) ve AYNI çıkış (açılış ya da kapanış) günü ve türüyle; EŞLİ FARK = olay - eş ortalaması; SIRA = olayın eşler içindeki yeri; 10 yuva slot portföy (yuva çıkış günü boşalır) vs her olay yerine aynı hücreden rastgele eş alınan 200 portföy; ay kümeli bootstrap (giriş ayı, 2000, tohum 27); ayrıca en yüksek / en düşük, P(getiri >= +%50) ve eşlerin aynı oranı (kat)",
  "tavan_gun": 250,
  "tetik": "geçerli (temizlik) BofA ALIM listesi satırı, sıra <= 3, tür gün içi ya da gün sonu (haftalık B'de tetik değil); veri günü + hisse başına en erken yayımlanan (BI tekil kuralı B)",
  "tur": [
   "gun_ici",
   "gun_sonu"
  ]
 },
 "ikincil": {
  "tanim": "aynı koşullu tetikler, BOFA_IZI olay60 tanımıyla: giriş = yayından sonraki ilk açılış, aynı hissede 60 işlem gününde tek olay, FON_IZI.FI_OLCUT r60 eşli fark / sıra / portföy (bi_olay_olc, bi_olay_ozet, bi_olay_karar); 20 gün P(+%50'ye dokunma) ve P(-%30'a dokunma), eşlerin kaç katı (60 gün penceresi / 20 gün penceresi 31.08.2026 içinde)",
  "tekil_gun": 60
 },
 "kapsam": {
  "blok": 1,
  "kurum": "BofA",
  "tanim": "bofa_liste.csv'de kurum BofA, haberdeki ilk blok (blok 1), tür gün içi / gün sonu / haftalık (aylık dışarıda)",
  "tur": [
   "gun_ici",
   "gun_sonu",
   "haftalik"
  ],
  "yon": [
   "alim",
   "satim"
  ]
 },
 "karar": {
  "alt_donem": [
   "2023-04 .. 2024-12 (A)",
   "2025-01 .. 2026-08 (B)"
  ],
  "bh_m": 7,
  "bh_q": 0.1,
  "bilgi": "G1C2, G2C1, G2C2, düz yazı hariç, tamamlayıcılar, ikincil 60 gün ve olasılıklar BİLGİ / duyarlılıktır; karar değiştirmez",
  "metin": "Her satır (K1..K6, TÜMÜ), ANA yol G1 + C1, çıkışı <= 31.08.2026 olan kapanmış dönemlerle: n >= 30 VE ortalama eşli fark > 0 VE ay kümeli bootstrap %95 alt uç > 0 VE ortalama sıra > 0,50 VE 10 yuva portföy > 200 rastgele eş portföyün %90'ı VE iki alt dönemde (giriş < 01.01.2025 / >= 01.01.2025) ortalama eşli fark > 0 VE Benjamini-Hochberg q = 0,10 ile reddedilen (7 satır, p = bootstrap tek yönlü P(ortalama <= 0)) -> 'YOL ADAYI (BIST)'; değilse 'yol yok' ve tutmayan şartlar. AKD verisi yalnız BIST'te var: ABD / Avrupa karar hücresi YOK; karar en fazla 'BIST-ADAY' düzeyindedir (CLAUDE.md 28 Eki karar hücreleri: İZ değildir).",
  "n_min": 30,
  "port_n": 200,
  "port_yuzde": 0.9,
  "yari": "2025-01-01"
 },
 "kriz": {
  "kesik": "2026-08-31",
  "kriz_bas": "2026-09-01",
  "kural": "çıkışı 31.08.2026'dan sonra olan ya da veri sonunda açık dönem karara girmez (sayılır); G1 giriş günü >= 01.09.2026 olan TÜMÜ dönemleri ayrı BİLGİ tablosunda (açık olanlar bugüne getiri)"
 },
 "soru": "A) BofA yayımlanan kendi ortalama maliyetinden kâr ediyor mu, nerede ediyor (betimleyici)? B) BofA'nın alımları haber yayımlandığı anda bilinen bilgiyle ayrılabilir mi ve Cemal haber saatinden sonra girerek bunun bir kısmını yakalayabilir mi (karar)? Kaynak: Cemal 13.11.2026 itirazı ('BofA bir hissede %40-80 zarar etmez'; listedeki 'BofA' bir aracı kurum akışıdır, liste ilk 5-10 ile sınırlıdır).",
 "surum_etiket": "bofa_kar_20261113",
 "tekil": {
  "A": "A'da aynı veri günü + hisse + yön için birden çok GEÇERLİ MALİYETLİ satır varsa: gün sonu varsa en erken yayımlanan gün sonu, yoksa en geç yayımlanan gün içi (gün içi / gün sonu). Haftalık satırlar ayrı tutulur (veri günü + hisse + yön başına en erken yayın).",
  "B": "B'de tetik HABER ANIDIR: aynı veri günü + hisse için hissenin alım ilk 3'te göründüğü geçerli gün içi / gün sonu haberlerinden EN ERKEN yayımlanan tetiktir (Cemal'in o hisseyi ilk öğrendiği an; A'daki gün sonu önceliği B'de G1'in 'gün içi haber 17:30'dan önce' kuralını boşa çıkaracağından B'de uygulanmaz). Koşul değerleri (pay, maliyet, sıra, birim) o tetik satırından alınır."
 },
 "temizlik": {
  "haftalik_bant_gun": 5,
  "lot_min": 1000,
  "lot_tl_min": 100000.0,
  "maliyet_bant": [
   0.97,
   1.03
  ],
  "neden_sira": [
   "veri_gunu_yok",
   "fiyat_paneli_yok",
   "veri_gunu_bar_yok",
   "net_yok",
   "esik_alti",
   "maliyet_bant_disi"
  ],
  "tanim": "satır GEÇERLİ <=> (1) veri günü belirlenebilir (BOFA_IZI.bi_veri_gunu; haftalık listede de aynı işlev: yayın günü ya da önceki işlem günü); (2) hisse fiyat panelinde (Yahoo önbelleği, bi_panel) var; (3) veri günü barı var (H, L, C sonlu); (4) net sayısı yazılı; (5) birim lot ise |net| >= 1.000 lot VE |net| x fiyat >= 100.000 TL (fiyat = maliyet, maliyet yoksa veri günü kapanışı); birim TL ise |net| >= 1.000.000 TL; (6) maliyet yazılıysa veri günü [Low x 0,97, High x 1,03] aralığında (haftalık listede veri günü ve önceki 4 işlem gününün en düşük Low / en yüksek High'ı). Düşen satır İLK tutmayan nedenle sayılır (neden_sira). Net işareti kullanılmaz (satış tablolarının çoğu tutarı işaretsiz yazıyor; |net| kullanılır). 'duzyazi' biçimli satırlar ayrı sayılır; B ana sonucu ayrıca düz yazı hariç raporlanır (A'da düz yazı satırında maliyet yazılı değildir).",
  "tl_min": 1000000.0
 },
 "yanlilik": "AKD kodu kurum kimliği değildir (müşteri akışı; BofA'nın kendi pozisyonu değil). Liste ilk 5-10 ile sınırlı: BofA'nın listede görünmeyen alım / satımları yok; FIFO yalnız yayımlanmış lot listeleriyle, kapsamı düşüktür. Maliyet yalnız bazı hisse.net / YatırımX listelerinde yazılı (çoğu 2025-26). Gün içi maliyet o saate kadarki ortalamadır. Fiyatlar Yahoo bölünme düzeltmeli: bölünme öncesi maliyet bant dışı kalır ve düşer. Fiyat evreni bugün işlem gören hisseler (hayatta kalma yanlılığı). İşlem maliyeti / kayma yok."
}
```

## Karar cümlesi (önceden yazılı)

Her satır (K1..K6, TÜMÜ), ANA yol G1 + C1, çıkışı <= 31.08.2026 olan kapanmış dönemlerle: n >= 30 VE ortalama eşli fark > 0 VE ay kümeli bootstrap %95 alt uç > 0 VE ortalama sıra > 0,50 VE 10 yuva portföy > 200 rastgele eş portföyün %90'ı VE iki alt dönemde (giriş < 01.01.2025 / >= 01.01.2025) ortalama eşli fark > 0 VE Benjamini-Hochberg q = 0,10 ile reddedilen (7 satır, p = bootstrap tek yönlü P(ortalama <= 0)) -> 'YOL ADAYI (BIST)'; değilse 'yol yok' ve tutmayan şartlar. AKD verisi yalnız BIST'te var: ABD / Avrupa karar hücresi YOK; karar en fazla 'BIST-ADAY' düzeyindedir (CLAUDE.md 28 Eki karar hücreleri: İZ değildir).

G1C2, G2C1, G2C2, düz yazı hariç, tamamlayıcılar, ikincil 60 gün ve olasılıklar BİLGİ / duyarlılıktır; karar değiştirmez

## Veri ve temizlik sayımı (getiri içermez)

- Arşiv (BOFA_IZI topla, değişmedi): {"liste_haber": 2781, "liste_satir": 26888, "ilk": "2023-04-16 21:29:37", "son": "2026-11-13 12:58:31"}
- Fiyat: {"okunan": 630, "manifest_sha256": "5182947ec875fd59d89f61c25a24258bbdad4f376c15287fb5ffb4b50c9e2e56", "son_tarih": "2026-11-13"}
- Temizlik: {"kapsam_satir": 25927, "gecerli": 24350, "dusen": {"fiyat_paneli_yok": 574, "net_yok": 335, "esik_alti": 322, "veri_gunu_bar_yok": 292, "maliyet_bant_disi": 54}, "dusen_yon": {"alim/esik_alti": 207, "alim/fiyat_paneli_yok": 314, "alim/maliyet_bant_disi": 32, "alim/net_yok": 237, "alim/veri_gunu_bar_yok": 162, "satim/esik_alti": 115, "satim/fiyat_paneli_yok": 260, "satim/maliyet_bant_disi": 22, "satim/net_yok": 98, "satim/veri_gunu_bar_yok": 130}, "gecerli_yon_tur": {"alim/gun_ici": 1588, "alim/gun_sonu": 8803, "alim/haftalik": 2041, "satim/gun_ici": 1224, "satim/gun_sonu": 8618, "satim/haftalik": 2076}, "gecerli_bicim": {"baslik_tablo": 11315, "tablo": 11171, "satir": 1433, "duzyazi": 431}, "duzyazi_kapsam": 1009, "duzyazi_gecerli": 431, "gecerli_maliyetli": {"alim/TL": 143, "alim/lot": 177, "satim/TL": 114, "satim/lot": 182}, "gecerli_payli": 790, "kapsam_disi_BofA": {"satir": 961, "maliyetli": 607, "blok_2_ve_sonrasi": 957, "tur_disi": {"aylik": 4}}}
- A sayımı: {"alim_gun_satir": 252, "alim_haftalik_satir": 50, "satim_gun_satir": 227, "alim_ceyrek": {"2025Q2": 33, "2025Q3": 22, "2026Q1": 2, "2026Q2": 15, "2026Q3": 7, "2026Q4": 173}, "pencere": {"5": {"ana": 72, "kesik_asan": 0, "kriz_sonrasi": 156, "pencere_yok": 24}, "20": {"ana": 72, "kesik_asan": 0, "kriz_sonrasi": 87, "pencere_yok": 93}, "60": {"ana": 72, "kesik_asan": 0, "kriz_sonrasi": 0, "pencere_yok": 180}}, "fifo_lot": {"alim": 126, "satim": 132}}
- B sayımı: {"tetik": 3020, "g1_tip": {"acilis": 2460, "kapanis": 560}, "tetik_bicim": {"tablo": 1523, "baslik_tablo": 1170, "satir": 205, "duzyazi": 122}, "bayrak": {"K1": {"evet": 17, "hayir": 121, "bilinmiyor": 2882}, "K2": {"evet": 101, "hayir": 3, "bilinmiyor": 2916}, "K3": {"evet": 1431, "hayir": 1589, "bilinmiyor": 0}, "K4": {"evet": 2667, "hayir": 353, "bilinmiyor": 0}, "K5": {"evet": 59, "hayir": 2878, "bilinmiyor": 83}, "K6": {"evet": 119, "hayir": 2901, "bilinmiyor": 0}}, "olay": {"K1": {"toplam": 17, "kesik_ici_kapanmis": 11, "kriz_sonrasi_giris": 5}, "K2": {"toplam": 80, "kesik_ici_kapanmis": 22, "kriz_sonrasi_giris": 57}, "K3": {"toplam": 862, "kesik_ici_kapanmis": 741, "kriz_sonrasi_giris": 113}, "K4": {"toplam": 1630, "kesik_ici_kapanmis": 1439, "kriz_sonrasi_giris": 171}, "K5": {"toplam": 45, "kesik_ici_kapanmis": 20, "kriz_sonrasi_giris": 24}, "K6": {"toplam": 93, "kesik_ici_kapanmis": 37, "kriz_sonrasi_giris": 50}, "TUM": {"toplam": 1854, "kesik_ici_kapanmis": 1616, "kriz_sonrasi_giris": 187}}}

## Ön kayıttan önce görülenler (sonuç değil)

- Önceki BOFA_IZI ölçümü (Ç171: tutma dönemi eşli fark +%0,6 [-0,6, +2,0]; lot listeleri 60 gün -%10,3) ve iş tanımındaki PEKGY örneği (27.10.2026 gün sonu alım maliyet 0,856; 11.11.2026 gün içi satış maliyet 1,219; kriz sonrası, karara girmez). Bu bölümün hiçbir getirisi, eşli farkı, kâr oranı hesaplanmadı; yukarıdaki sayımlar yalnız satır / tetik / olay sayısıdır.
- Maliyet ve pay sütunlarının dağılımı (kaç satırda yazılı, hangi çeyrekte) ve net işaretinin satış tablolarında çoğunlukla işaretsiz yazıldığı (bu yüzden |net|) görüldü.

## Bilinen yanlılıklar

AKD kodu kurum kimliği değildir (müşteri akışı; BofA'nın kendi pozisyonu değil). Liste ilk 5-10 ile sınırlı: BofA'nın listede görünmeyen alım / satımları yok; FIFO yalnız yayımlanmış lot listeleriyle, kapsamı düşüktür. Maliyet yalnız bazı hisse.net / YatırımX listelerinde yazılı (çoğu 2025-26). Gün içi maliyet o saate kadarki ortalamadır. Fiyatlar Yahoo bölünme düzeltmeli: bölünme öncesi maliyet bant dışı kalır ve düşer. Fiyat evreni bugün işlem gören hisseler (hayatta kalma yanlılığı). İşlem maliyeti / kayma yok.

ESIK_SHA256: f50d11088ccbb73cb8bae7ed06abe8088d619a3786c946c0e01da2828ff26bb6
KOD_SHA256: 7ab2a2a5f189a05b5c29b0cc6129b78b53c8e4ee7e9f5562d5da3a186f52b802
LISTE_SHA256: 7020587fbc90cf88875211103fd2a3173789ec57954a8d6609d99bad195a1abd
HABER_SHA256: d9d3278417e1f157b26fe961f0b287d5d3b21f3475cd0b02a237f6cfc82e35d3
