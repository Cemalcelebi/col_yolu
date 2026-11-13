# BOFA İZİ ÖN KAYDI (veri toplandıktan sonra, getiri hesaplanmadan önce)

BOFA_IZI v1.0 (bofa_izi_20261113): BofA AKD alım listesi ilk sıraları -> tutma dönemi getirisi (ön kayıtlı). Yazılma 2026-11-13 15:49:10 UTC. Bu dosya git'e işlenmeden `python BOFA_IZI.py kos` çalışmaz (mühür kapısı).

## Soru

BofA aracı kurum kodunun (ForInvest AKD, haber sitelerine yansıyan) alım listesinde ilk sıralarda görünen BIST hissesi, BofA'nın tuttuğu dönem boyunca (satış listesinde görünene kadar) ve 60 gün içinde, aynı gün aynı momentum x likidite hücresindeki öteki hisselerden iyi gidiyor mu?

## Ana ölçü değişikliği (Cemal, 13.11.2026, ön kayıttan önce)

Ana ölçü sabit 60 gün değil, 'BofA tutma dönemi'dir (BI_ESIK['donem']). FI_OLCUT 60 gün ölçüsü ikincil olarak kalır (BI_ESIK['olay60']).

## Tanımlar ve eşikler (BI_ESIK, değişmez)

```json
{
 "alt_kume": {
  "cokmus": -0.6,
  "tanim": "çökmüş <=> giriş öncesi kapanış / önceki 250 günün en yüksek kapanışı - 1 <= -0,60 (en az 120 bar); diğer"
 },
 "donem": {
  "bootstrap": "ay kümeli (giriş ayı), 2000 tekrar, tohum 27, %95 aralık ortalama eşli fark için",
  "cikis_sira": 5,
  "cikis_tur": [
   "gun_ici",
   "gun_sonu",
   "haftalik"
  ],
  "gec_kalma": "O(giriş) / BofA'nın açılış haberindeki ortalama maliyeti - 1 (maliyet yazılıysa)",
  "getiri": "dönem getirisi = O(çıkış) / O(giriş) - 1; çıkış günü açılış yoksa (durdurma) 5 gün içindeki ilk açılış, o da yoksa son kapanış",
  "giris_sira": 3,
  "giris_tur": [
   "gun_ici",
   "gun_sonu",
   "haftalik"
  ],
  "kontrol": "aynı giriş günü d ve aynı çıkış günü x: d günü aynı 60 gün momentum beşliği x 20 gün TL likidite üçlüsündeki (FI_OLCUT tanımı: momentum C[d-1]/C[d-61]-1, likidite önceki 20 günün medyan C*V) öteki hisselerin aynı kuralla dönem getirisi ortalaması; EŞLİ FARK = olay - eş ortalaması; SIRA = olayın eşler içindeki yeri (0-1)",
  "olasilik": "P(dönem getirisi >= +%50); P(dönemde -%30'a dokunma: en düşük <= -0,30)",
  "portfoy": "10 yuva, dönem boyunca tut (yuva çıkış günü boşalır), olay getirileri vs her olay yerine aynı gün aynı hücreden rastgele eş alınan 200 portföy (aynı giriş / çıkış günleri)",
  "tanim": "her hisse için alım haberleri zaman sırasıyla: ilk 3'te görüldüğü ilk haber DÖNEM AÇAR (giriş = yayından sonraki ilk açılış); çıkış haberi = giriş günü 10:00'dan SONRA yayımlanan ilk BofA satış listesi haberi (her tür) ve hisse orada ilk 5'te; çıkış = o haberin yayınından sonraki ilk açılış. Satış haberi yoksa çıkış = giriş + 250 işlem günü ya da veri sonu ('satış görülmedi' ayrı sayılır). Dönem açıkken gelen alım haberleri yeni dönem açmaz; çıkış haberinden sonra gelen alım haberi yeni dönem açar.",
  "tavan_gun": 250,
  "uc": "dönem en yüksek = max H[giriş .. çıkış-1] / O(giriş) - 1; en düşük = min L[aynı] / O(giriş) - 1",
  "varyant": "çıkış = BofA satış listesi haberleri zaman sırasıyla dizildiğinde hissenin İKİ ARDIŞIK haberde ilk 3'te görülmesi (ikinci haberin yayınından sonraki ilk açılış)"
 },
 "giris": {
  "bilgi_kapanis": "BİLGİ: gün içi listede (yayın < 18:00, işlem günü) aynı gün kapanışından giriş",
  "kural": "haberin yayınından SONRAKİ ilk işlem günü açılışı: yayın < 09:55 ve gün işlem günüyse o gün, değilse ertesi işlem günü (seans içindeki haber de ertesi açılış)",
  "takvim": "en az 50 hissenin işlem gördüğü günler (Yahoo önbelleği)"
 },
 "karar": {
  "coklu": "ana dışındaki satırlar (ilk 1, ilk 5, ardışık, varyant çıkış, TL listeleri, alt kümeler) BİLGİ / duyarlılık; çoklu deneme",
  "metin": "ANA (tutma dönemi): n >= 30 VE ortalama eşli dönem farkı > 0 VE ay kümeli bootstrap %95 alt uç > 0 VE iki alt dönemde (A, B) ortalama eşli fark aynı yönde (ikisi de > 0) -> 'BofA tutma dönemi BIST'te iz adayı'; değilse 'kanıt yok' ve hangi şart tutmadı. Sıra ve portföy raporlanır, karara girmez (Cemal'in tutma dönemi kararı). İKİNCİL (FI_OLCUT 60 gün, alım ilk 3): n >= 30, ortalama eşli fark > 0 ve alt uç > 0, sıra > 0,50, portföy > rastgele %90 VE iki alt dönem aynı yön -> 'iz adayı' (ikincil); değilse 'kanıt yok'. Tek pazar (BIST): FI_OLCUT'un ABD + Avrupa karar hücreleri bu veride yok, en fazla 'BIST iz adayı' denir. FI_OLCUT dönem hücreleri (2023, 2024-26) BİLGİ olarak ayrıca yazılır.",
  "n_min": 30
 },
 "kriz": {
  "kesik": "2026-08-31",
  "kural": "ana sonuç: çıkış günü (dönem) / 60. gün (r60) / 20. gün (20 gün ölçüleri) <= 31.08.2026. Aşanlar ana sonuca girmez, sayılır. Giriş günü >= 01.09.2026 dönemleri tek tek BİLGİ tablosunda (açık dönem: bugüne getiri, BofA hâlâ tutuyor mu)"
 },
 "kurum": {
  "bh": "Benjamini-Hochberg q = 0,10; p = ay kümeli bootstrap tek yönlü P(ortalama eşli dönem farkı <= 0) ((say + 1) / (B + 1)); m = kesik içinde en az 1 ölçülmüş dönemi olan kod sayısı (toplu hariç)",
  "birim": "her kodda bütün birimler (ana ile aynı)",
  "karar": "kod 'iz adayı' <=> ana karar şartları (n >= 30, ortalama eşli fark > 0, alt uç > 0, A ve B > 0) VE BH ile reddedilen; arşivde listesi olmayan kod 'veri yok'",
  "kaynak": "Cemal 13.11.2026 eki, ön kayıttan önce",
  "kodlar": [
   "BofA",
   "Merrill",
   "JPM",
   "MS",
   "Citi",
   "Deutsche",
   "HSBC",
   "Goldman",
   "UBS",
   "Barclays",
   "CS"
  ],
  "kriz": "kriz dönemi (giriş >= 01.09.2026) açık dönemler kod bazında tablo (BİLGİ)",
  "tanim": "her yabancı kod (haberlerde alım / satım listesi bulunan) AYNI tutma dönemi ölçüsüyle (BI_ESIK['donem']), kodun kendi listeleriyle; Merrill haberde BofA'dan ayrı geçiyorsa ayrı kod",
  "toplu": "TOPLU satır: herhangi bir yabancı kodun (BofA dahil) alım listesinde ilk 3 dönem açar, herhangi bir yabancı kodun satış listesinde ilk 5 kapatır (her liste kendi sırasıyla, birim ayrımı yok)"
 },
 "liste": {
  "ana_birim": "hepsi",
  "ana_kaynak": "ANA: haberde yayımlanan BofA listesi, birimi ne olursa olsun (lot sıralı hisse.net ForInvest tabloları ve TL sıralı YatırımX / Rota Borsa / hisse.net listeleri; Cemal'in tanımı 'haberde ilk 3'). DUYARLILIK: yalnız lot sıralı, yalnız TL sıralı, yalnız yapılandırılmış (tablo / satır; düz yazıdan çıkarılan sıra hariç)",
  "bicim": "tablo; satir ('PAHOL: 16.561.430 lot (...)'); baslik_tablo (Rota Borsa); duzyazi (aynı kurum + yön için yapılandırılmış liste yoksa metindeki geçiş sırası: geçerli kod + 90 karakter içinde 'sayı (milyon) lot / TL')",
  "blok": "bir haberde aynı kurum + yön için birden çok liste varsa ilki; sıra = listede yayımlanan sıra ('Diğer' satırı sayılmaz)",
  "kurum": "BofA",
  "tur": "haftalık <=> başlık / spot 'haftal'; gün içi <=> metinde veri saati < 18:00 ('saat 12:25 verilerine göre', '12:30 itibarıyla') ya da yayın 09:55-18:05 arası ve gün sonu ibaresi yok; gün sonu <=> başlık / spot / ilk paragrafta 'gün sonu' ya da yayın >= 18:05 ya da < 09:55; hafta sonu yayın + 'hafta' ibaresi -> haftalık",
  "veri_gunu": "gün içi / gün sonu: yayın >= 09:55 ise yayın günü (işlem günü değilse önceki işlem günü), < 09:55 ise önceki işlem günü"
 },
 "olay60": {
  "ana_sira": 3,
  "ardisik": 2,
  "duyarlilik_sira": [
   1,
   5
  ],
  "secim": "her veri günü için BİR liste: gün sonu varsa en erken yayımlanan gün sonu, yoksa en geç gün içi (ana: her birim); haftalık ayrı BİLGİ",
  "tanim": "olay = o günün seçilen alım listesinde ilk K; ardışık = iki ardışık işlem gününün seçilen listelerinde ilk 3 (olay günü ikinci gün); aynı hissede 60 işlem gününde tek olay (ilki); ölçüt FON_IZI.FI_OLCUT (r60, eşli fark, ay kümeli bootstrap, hücre içi sıra, 10 yuva portföy vs 200 rastgele); ayrıca r5, r20, P(+%50'ye dokunma 20g: max H >= 1,5 O), P(-%30'a dokunma 20g: min L <= 0,7 O) ve aynı gün aynı hücre eşlerinin aynı olasılıkları (kat = olay / eş)",
  "tekil_gun": 60,
  "ters": "satış listesi ilk 3 aynı ölçülerle (ters sınama: BofA bilgiliyse eşli fark < 0 beklenir)"
 },
 "surum_etiket": "bofa_izi_20261113",
 "yanlilik": "AKD kodu kurum kimliği değildir (savcılık 'yabancı görünümlü yerli işlem' inceliyor). Arşiv haber sitesinin seçtiği günlerdir (her gün liste yok; eksik günler sayılır). Liste ilk 5 ile sınırlı: 'ilk 5'te görülmedi' satış olmadığı anlamına gelmez. Fiyat evreni bugün işlem gören hisseler (hayatta kalma yanlılığı yukarı). İşlem maliyeti yok.",
 "yari": {
  "sinir": "2025-01-01",
  "tanim": "alt dönemler giriş tarihine göre: A < 01.01.2025 <= B. Veri aralığı (ilk liste veri günü 17.04.2023 - kriz kesiği 31.08.2026) takvim orta noktası 08.01.2025'e en yakın ay başı; veri toplandıktan, getiri hesaplanmadan seçildi"
 }
}
```

## Karar cümlesi (önceden yazılı)

ANA (tutma dönemi): n >= 30 VE ortalama eşli dönem farkı > 0 VE ay kümeli bootstrap %95 alt uç > 0 VE iki alt dönemde (A, B) ortalama eşli fark aynı yönde (ikisi de > 0) -> 'BofA tutma dönemi BIST'te iz adayı'; değilse 'kanıt yok' ve hangi şart tutmadı. Sıra ve portföy raporlanır, karara girmez (Cemal'in tutma dönemi kararı). İKİNCİL (FI_OLCUT 60 gün, alım ilk 3): n >= 30, ortalama eşli fark > 0 ve alt uç > 0, sıra > 0,50, portföy > rastgele %90 VE iki alt dönem aynı yön -> 'iz adayı' (ikincil); değilse 'kanıt yok'. Tek pazar (BIST): FI_OLCUT'un ABD + Avrupa karar hücreleri bu veride yok, en fazla 'BIST iz adayı' denir. FI_OLCUT dönem hücreleri (2023, 2024-26) BİLGİ olarak ayrıca yazılır.

ana dışındaki satırlar (ilk 1, ilk 5, ardışık, varyant çıkış, TL listeleri, alt kümeler) BİLGİ / duyarlılık; çoklu deneme

## Ölçülecekler

- ANA: tutma dönemleri (giriş ilk 3, çıkış satış ilk 5): n, süre dağılımı, dönem getirisi, en yüksek / en düşük, P(getiri >= +%50), P(-%30'a dokunma), geç kalma bedeli, eşli fark + ay kümeli %95 aralık, sıra, 10 yuva portföy vs 200 rastgele, alt dönem A / B.
- Varyant çıkış (satış ilk 3, iki ardışık haber); alt kümeler çökmüş / diğer; TL sıralı listeler (duyarlılık).
- İKİNCİL (FI_OLCUT 60 gün): alım ilk 3 (ana), ilk 1, ilk 5, ardışık 2+ gün ilk 3, çökmüş / diğer, satış ilk 3 (ters), haftalık alım ilk 3 (bilgi); her satırda r5, r20, P(+%50, 20g), P(-%30, 20g) ve eş katları. BİLGİ: gün içi listede aynı gün kapanıştan giriş.
- Kriz dönemi (giriş >= 01.09.2026): dönemler tek tek (açık dönem bugüne, BofA hâlâ tutuyor mu).
- En erken bilgi: liste haberlerinin yayın saati dağılımı (gün içi / gün sonu / haftalık, site), gün içi veri saati ve gecikme.

## Veri ve tanım sayımı (sonuç içermez)

- Arşiv: {"bicim": {"hissenet/duzyazi": 133, "hissenet/satir": 163, "hissenet/tablo": 84, "rotaborsa/baslik_tablo": 1153, "rotaborsa/duzyazi": 140, "rotaborsa/tablo": 1181, "yatirimx/duzyazi": 113, "yatirimx/satir": 156, "yatirimx/tablo": 73}, "birim": {"hissenet/TL": 180, "hissenet/lot": 200, "rotaborsa/TL": 2459, "rotaborsa/lot": 15, "yatirimx/TL": 311, "yatirimx/lot": 31}, "diger_kurum": {"CS": 1, "Citi": 12, "Deutsche": 104, "Goldman": 1, "HSBC": 1031, "JPM": 1, "Merrill": 3, "UBS": 1}, "haber": 4652, "ilk": "2023-04-16 21:29:37", "kurum_liste_haber": {"BofA": 2781, "CS": 1, "Citi": 12, "Deutsche": 104, "Goldman": 1, "HSBC": 1031, "JPM": 1, "Merrill": 3, "UBS": 1}, "liste_haber": 2781, "liste_satir": 26888, "site": {"hissenet": {"aday": 561, "indirilen": 561, "inmeyen": 0}, "rotaborsa": {"aday": 3391, "indirilen": 3391, "inmeyen": 0}, "yatirimx": {"aday": 700, "indirilen": 700, "inmeyen": 0}}, "site_liste": {"hissenet": 250, "rotaborsa": 2301, "yatirimx": 230}, "son": "2026-11-13 12:58:31", "tur": {"aylik": 1, "gun_ici": 424, "gun_sonu": 1899, "haftalik": 457}, "zaman": "2026-11-13 15:47:26 UTC"}
- Fiyat: {"okunan": 630, "manifest_sha256": "5182947ec875fd59d89f61c25a24258bbdad4f376c15287fb5ffb4b50c9e2e56", "son_tarih": "2026-11-13"}
- Sayım: {"liste_haber": 2774, "veri_gunu_ilk": "2023-04-17", "veri_gunu_son": "2026-11-13", "islem_gunu": 896, "alim_listesi_olan_gun": 879, "satim_listesi_olan_gun": 870, "alim_listesi_eksik_gun": 17, "tur_haber": {"gun_sonu": 1899, "haftalik": 457, "gun_ici": 418}, "ay_alim_gun": {"2023-04": 8, "2023-05": 20, "2023-06": 19, "2023-07": 21, "2023-08": 22, "2023-09": 21, "2023-10": 21, "2023-11": 22, "2023-12": 19, "2024-01": 22, "2024-02": 21, "2024-03": 19, "2024-04": 17, "2024-05": 20, "2024-06": 17, "2024-07": 21, "2024-08": 20, "2024-09": 20, "2024-10": 22, "2024-11": 21, "2024-12": 20, "2025-01": 21, "2025-02": 20, "2025-03": 20, "2025-04": 20, "2025-05": 20, "2025-06": 19, "2025-07": 22, "2025-08": 21, "2025-09": 22, "2025-10": 22, "2025-11": 20, "2025-12": 22, "2026-01": 21, "2026-02": 20, "2026-03": 21, "2026-04": 21, "2026-05": 16, "2026-06": 22, "2026-07": 22, "2026-08": 21, "2026-09": 22, "2026-10": 21, "2026-11": 10}, "donem": {"toplam": 2099, "neden": {"satis": 2013, "acik_veri_sonu": 57, "satis_gorulmedi_250": 29}, "cikis_kesik_ici": 1837}, "olay60_alim_ilk3": 504}

## Ön kayıttan önce görülenler (sonuç değil)

- Arşiv kapsamı, liste türleri, ayrıştırma örnekleri; 27.10 / 28.10 / 2.11 PEKGY, 20-26.10 ODINE / GUNDG haberleri (iş tanımında; kriz dönemi, ana sonuca girmez). Getiri, eşli fark, dokunma oranı hesaplanmadı.
- Alt dönem sınırı (BI_ESIK['yari']) veri aralığından seçildi (sonuçtan değil).

## Bilinen yanlılıklar

AKD kodu kurum kimliği değildir (savcılık 'yabancı görünümlü yerli işlem' inceliyor). Arşiv haber sitesinin seçtiği günlerdir (her gün liste yok; eksik günler sayılır). Liste ilk 5 ile sınırlı: 'ilk 5'te görülmedi' satış olmadığı anlamına gelmez. Fiyat evreni bugün işlem gören hisseler (hayatta kalma yanlılığı yukarı). İşlem maliyeti yok.

ESIK_SHA256: 6b544f940e2309b7163b7af8910af698d2ac6d1b0a6d880d873c091ae4f28dba
KOD_SHA256: fdcac64b83d1bab1f5c81c44e4246463ad88cf2a230b901e4edd6789d9388187
LISTE_SHA256: 7020587fbc90cf88875211103fd2a3173789ec57954a8d6609d99bad195a1abd
HABER_SHA256: d9d3278417e1f157b26fe961f0b287d5d3b21f3475cd0b02a237f6cfc82e35d3
