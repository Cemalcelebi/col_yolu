# DİPTE BofA (KURULUM + TETİK) — ÖN KAYIT (getiri hesaplanmadan önce)

BOFA_IZI DİP v1.0 (bofa_dip_20261113): KURULUM (250 gün tepeden <= -%80, son 10 günde yeni dip yok, dipten <= 1,5 kat) tek başına (BIST / ABD / Avrupa, FI_OLCUT 60 gün + 120 / 250 gün + olasılık tablosu) + BofA alım ilk 5 tetiği (BIST) + kriz sonrası izleme (ön kayıtlı). Yazılma 2026-11-13 17:17:27 UTC. Bu dosya git'e işlenmeden ve mühürler tutmadan `python BOFA_IZI.py dipkos` çalışmaz.

## Soru

Cemal 13.11.2026: 'Her BofA alımında al demiyorum. Dipte %80-90 düşüş var, artık daha fazla düşmeyecek bir görüntü, çok ucuzlamış bir noktada BofA alımı ile girsek.' KURULUM = derin düşüş + dip tutuyor (yeni dip yok) + dipten henüz kaçmamış; TETİK = BofA alımı. (1) Kurulum tek başına (BofA'sız) iz mi (BIST / ABD / Avrupa)? (2) BofA alımı kurulumun üstüne bir şey ekliyor mu (BIST)? (3) Bugün kurulumdaki BIST hisseleri ve son 20 günde BofA alımı görünenler (İZLEME, öneri değil).

## Ne ölçülecek

- (1) KURULUM TEK BAŞINA: BIST (Yahoo 2015-), ABD (V_ABD), Avrupa (V_AVR); hücreler 2016-22 / 2023 / 2024-26 (giriş günü). FI_OLCUT 60 gün (r60, eşli fark, ay kümeli bootstrap, sıra, slot portföy) + 120 ve 250 gün getirisi + OLASILIK TABLOSU P(250 gün içinde +%100'e dokunma), P(-%50'ye dokunma): eşlerin ve taban oranın kaç katı.
- (2) KURULUM + BofA TETİĞİ (BIST, 17.04.2023 .. 31.08.2026): aynı ölçüler (G2 açılış girişi) + tutma dönemi (G1 giriş, C1 çıkış) + BofA'sız kurulum olaylarıyla karşılaştırma + geniş okuma (BİLGİ).
- (3) KRİZ SONRASI İZLEME (BİLGİ): bugün kurulumdaki BIST hisseleri; son 20 günde BofA ilk 5 alımında görünenler.

## Tanımlar ve eşikler (DP_ESIK; değişmez)

```json
{
 "bofa": {
  "bas": "2023-04-17",
  "bofasiz": "KARŞILAŞTIRMA: (1)'in BIST kurulum olaylarından girişi 17.04.2023 .. 31.08.2026 arasında olanlar; hisse kurulum gününden 20 işlem günü önce ile 20 işlem günü sonra arasındaki veri günlerinde hiçbir BofA alım ilk 5 tetiğinde (kurulum süzgeci yok, geçerli satır, her tür) görünmediyse BofA'SIZ, göründüyse BofA'LI (BİLGİ). FARK = (2) olaylarının ortalama eşli r60 farkı - BofA'sız olayların; iki grup bağımsız ay kümeli bootstrap (2000, tohum 27) %95 aralığı",
  "bofasiz_gun": 20,
  "donem": "TUTMA DÖNEMİ (BİLGİ): kurulumlu tetikler bk_olaylar ile (dönem açıkken gelen tetik yeni dönem açmaz); çıkış C1 = G1 girişten sonra yayımlanan ilk BofA satış listesi haberinde ilk 5 -> sonraki açılış; yoksa 250 işlem günü; ölçü bk_yol_olc G1C1 + bk_yol_ozet (eşli fark, sıra, portföy, bootstrap; çıkışı 31.08.2026'yı aşan / açık dönem girmez)",
  "genis": "DUYARLILIK (BİLGİ): 'kurulum sağlıyken' geniş okuma = karar gününde ya da önceki 19 barda kurulum sağlanmış",
  "genis_gun": 20,
  "giris": "G1 (BK_ESIK B.giris.G1): gün içi haber ve yayın veri gününde 17:30 TR'den önce -> veri günü kapanışı; değilse yayından sonraki ilk açılış. FI_OLCUT 60 gün, 120 / 250 gün ve olasılık ölçüleri standart gereği AÇILIŞ girişiyle: G2 = yayından sonraki ilk işlem günü açılışı (bi_giris_gunu; G2 >= G1, karar günü G1'den önce)",
  "karar_gunu": "tetiğin KURULUM durumu = hissenin G1 giriş gününden ÖNCEKİ son barındaki kurulum (G1 kapanış girişinde veri gününden önceki bar; açılış girişinde giriş gününden önceki bar). D1-D3 yalnız giriş anından önce kesinleşmiş kapanışlarla",
  "kesik": "2026-08-31",
  "olay": "kurulumlu tetikler hisse başına G2 sırasıyla; aynı hissede 60 işlem gününde tek olay (bi_tekil)",
  "tekil_gun": 60,
  "temizlik": "BK_ESIK['temizlik'] aynen (bk_temizle; geçerli satır = neden boş, kar_temiz.csv.gz ile aynı kural). TETİK = geçerli BofA ALIM satırı, sıra <= 5, her tür (gün içi / gün sonu / haftalık), her birim (lot / TL); veri günü + hisse başına en erken yayın (bk_tetikler; BK_ESIK yalnız giris_sira = 5 ve tur = 3 tür olarak kopyalanır)",
  "tetik_sira": 5,
  "tur": [
   "gun_ici",
   "gun_sonu",
   "haftalik"
  ]
 },
 "hucre": [
  [
   "2016-22",
   "2016-01-01",
   "2022-12-31"
  ],
  [
   "2023",
   "2023-01-01",
   "2023-12-31"
  ],
  [
   "2024-26",
   "2024-01-01",
   "2026-08-31"
  ]
 ],
 "karar": {
  "bir": "(1) KURULUM TEK BAŞINA: hücre başına FI_OLCUT dört şartı (n >= 30; ortalama eşli fark > 0 ve ay kümeli bootstrap %95 alt uç > 0; ortalama hücre içi sıra > 0,50; 10 yuva slot portföy > 200 rastgele eş portföyün %90'ı). Etiket FON_IZI.fi_olcut_karar (FI_OLCUT 'karar' = ABD + AVR, dönem 2023 ve 2024-26): dört karar hücresi (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26) tutarsa İZ (BIST iki hücresi de tutarsa 'İZ + BIST'); değilse İZ DEĞİL. 2016-22 hücreleri ve BIST BİLGİ. Olasılık tablosu, 120 / 250 gün BİLGİ",
  "iki": "(2) KURULUM + BofA: BofA arşivi yalnız BIST'te -> en fazla 'BIST-ADAY'. Havuz hücre (G2 girişi 17.04.2023 .. 31.08.2026, FI_OLCUT 60 gün): n >= 30 VE dört şart VE BIST 2023 ve BIST 2024-26 alt hücrelerinde ortalama eşli fark > 0 -> 'BIST-ADAY (BofA dipte)'; n < 30 -> 'ÖRNEKLEM YETERSİZ (n = ...)' ve olaylar tek tek listelenir; değilse 'yol yok' + tutmayan şartlar. Tutma dönemi, BofA'sız karşılaştırma, geniş okuma BİLGİ (karar değiştirmez)",
  "n_min": 30,
  "uc": "(3) İZLEME: karar yok, öneri değil"
 },
 "karar_hucre": [
  "2023",
  "2024-26"
 ],
 "kriz": {
  "izle": "veri sonu (son işlem günü) itibarıyla KURULUM sağlayan bütün BIST hisseleri (son barı son işlem günü olanlar): düşüş, 250 gün tepesi ve tarihi, dip (60 gün en düşük kapanış) ve tarihi, dipten kat, son 20 bar getirisi; son 20 işlem gününde (veri günü) BofA alım ilk 5 tetiği görünenlerde son tetiğin yayını, türü, sırası, birimi, maliyeti, payı, G1 giriş fiyatı ve bugüne getiri (G1 fiyatından ve BofA maliyetinden). İZLEME listesidir, öneri değildir",
  "izle_gun": 20,
  "kesik": "2026-08-31",
  "kriz_bas": "2026-09-01",
  "kural": "girişi / ölçü penceresi 31.08.2026'yı aşan ölçü karara girmez (FI_OLCUT 'kriz'); kriz sonrası (G2 >= 01.09.2026) BofA tetikli kurulum olayları ve bugünkü kurulum listesi BİLGİ / İZLEME"
 },
 "kurulum": {
  "ayri_gun": 60,
  "dip_gun": 60,
  "dip_yas": 10,
  "dipten_kat": 1.5,
  "dusus": -0.8,
  "kirik": {
   "ABD": [
    -0.6667,
    2.0
   ],
   "AVR": [
    -0.6667,
    2.0
   ],
   "BIST": [
    -0.25,
    0.25
   ]
  },
  "tanim": {
   "D1": "derin düşüş: C[t] / max(C[t-250 .. t-1]) - 1 <= -0,80 (C = kapanış, hissenin kendi barları; tepe penceresinde en az 200 bar, son veri kırığından sonra)",
   "D2": "dip tutuyor: min(C[t-9 .. t]) > min(C[t-59 .. t-10]) — son 60 barın en düşük kapanışı karar gününden en az 10 bar önce oluşmuş, son 10 barda ona eşit ya da daha düşük kapanış yok",
   "D3": "dipten kaçmamış: C[t] <= 1,50 x min(C[t-59 .. t-10])",
   "kirik": "VERİ KIRIĞI: r = C[t] / C[t-1] - 1 < alt ya da > üst. BIST [-0,25, +0,25] (TAVAN_SERISI kuralı: günlük marj ±%10 / 2020 öncesi ±%20, gerçek hareket olamaz); ABD ve Avrupa [-0,6667, +2,0] (marj yok; 1/3 ve 3 kat oran: düzeltilmemiş bölünme / birim (GBp-GBP) şüphesi). Kırık seriyi keser: tepe penceresi kırıktan sonra yeniden başlar, 200 bar dolmadan kurulum yok (kırıklı hisse o süre çıkarılır)",
   "kurulum": "KURULUM GÜNÜ t <=> D1 ve D2 ve D3; yalnız t günü ve öncesinin kapanışları kullanılır",
   "olay": "aynı hissede ilk kurulum günü olaydır; sonraki olay en az 60 bar sonra (o gün kurulum sağlanıyorsa). Giriş = kurulum gününden sonraki ilk bar AÇILIŞI (FI_OLCUT); kurulum günü hissenin son barıysa olay yok"
  },
  "tepe_en_az": 200,
  "tepe_gun": 250
 },
 "olcu": {
  "asagi": -0.5,
  "dokunma_gun": 250,
  "ek": "r120 / r250 eşli farkları için ay kümeli bootstrap (bi_boot: 2000, tohum 27) %95 aralığı; medyanlar",
  "es": "eş = aynı giriş günü d, FI_OLCUT hücresi aynı (P['H'], P['ok']) öteki hisseler, ölçüsü tanımlı, en az 3; eş oranı / getirisi = eşlerin ortalaması; KAT (eş) = olay oranı / olayların eş oranları ortalaması",
  "fi": "FON_IZI.FI_OLCUT 60 gün DEĞİŞTİRİLMEDEN: fi_olcut_panel (r60 = C[d+59] (5 gün ileri taşınmış) / O[d] - 1, 31.08.2026 kesiği), fi_olcut_olay (aynı giriş günü, aynı 60 gün momentum beşliği x 20 gün likidite üçlüsü öteki hisseler; eşli fark; hücre içi sıra), fi_olcut_hucre (ay kümeli bootstrap 2000 / tohum 27 %95 aralığı; 10 yuva slot portföy vs 200 rastgele eş portföyün %90'ı)",
  "kirik60": "BİLGİ: FI r60 penceresinde veri kırığı olan olay sayısı (FI_OLCUT standardı kırığı ayıklamaz; karar hücresi değişmez)",
  "taban": "TABAN = aynı pazar ve dönemde (giriş günü) FI_OLCUT 'ok' olan bütün hisse-günlerin oranı; KAT (taban) = olay oranı / taban",
  "ufuk": [
   120,
   250
  ],
  "ufuk_tanim": "r_h = C[d+h-1] / O[d] - 1 (h = 120, 250; kapanış en çok 5 gün ileri taşınmış); P(+%100) = max(H[d .. d+249]) >= 2 x O[d]; P(-%50) = min(L[d .. d+249]) <= 0,5 x O[d]. Pencere 31.08.2026'yı aşarsa, pencere sonunda fiyat yoksa ya da pencerede (d, d+h-1] veri kırığı varsa ölçülmez (olaya ve eşlere aynı kural)",
  "yukari": 1.0
 },
 "soru": "Cemal 13.11.2026: 'Her BofA alımında al demiyorum. Dipte %80-90 düşüş var, artık daha fazla düşmeyecek bir görüntü, çok ucuzlamış bir noktada BofA alımı ile girsek.' KURULUM = derin düşüş + dip tutuyor (yeni dip yok) + dipten henüz kaçmamış; TETİK = BofA alımı. (1) Kurulum tek başına (BofA'sız) iz mi (BIST / ABD / Avrupa)? (2) BofA alımı kurulumun üstüne bir şey ekliyor mu (BIST)? (3) Bugün kurulumdaki BIST hisseleri ve son 20 günde BofA alımı görünenler (İZLEME, öneri değil).",
 "surum_etiket": "bofa_dip_20261113",
 "veri": {
  "ABD": "V_ABD.pkl (islenmis-veri dalı, fi_k1_veri çıktısı) eksi evren dışı 7 fon (evren_disi_ABD.csv içeriği, IZ_DEFTERI 30.10.2026)",
  "AVR": "V_AVR.pkl (islenmis-veri; STOXX Europe 600 + FTSE 250, yerel para, likidite Kur sütunuyla EUR)",
  "BIST": "Yahoo günlük önbelleği /tmp/tavan/yahoo (TAVAN_SERISI.ts_fiyatlar, bölünme / bedelsiz düzeltmeli; değiştirilmeden), 01.01.2015'ten, en az 20 bar; izleme listesinde ekran fiyatı (Yahoo x bölünme çarpanı)",
  "bist_bas": "2015-01-01",
  "evren_disi": [
   "DBA",
   "DBB",
   "DBO",
   "UNG",
   "UNL",
   "UUP",
   "BTCW"
  ],
  "likidite": "FI_OLCUT'ta ayrı likidite alt sınırı yok (eşleme 20 gün medyan işlem değeri üçlüsüyle); bu çalışma da alt sınır koymaz"
 },
 "yanlilik": "Fiyat evreni bugün işlem gören hisseler (BIST Yahoo önbelleği, V_ABD, V_AVR): -%80 düşüp sonra batan / kotasyondan çıkan şirketler evrende yok -> P(+%100) yukarı, P(-%50) aşağı yanlı; derin düşmüşlerde batma eşlerden sık olduğu için eşli fark da yukarı yanlı olabilir (ABD'de 2016'da işlem görenlerin %44'ü sonradan çıkmış, IZ_VERI_ENVANTERI). AKD kodu kurum kimliği değildir; BofA arşivi her günü kapsamaz ('BofA'sız' olayların bir kısmında görülmemiş BofA alımı olabilir). Yahoo düzeltmesi bedelli sermaye artırımlarında eksik olabilir (kırık kuralı yalnız büyük sıçramayı yakalar). İşlem maliyeti / kayma yok; çok düşük fiyatlı hissede açılıştan alım varsayımı iyimser."
}
```

## Karar cümleleri (önceden yazılı)

(1) KURULUM TEK BAŞINA: hücre başına FI_OLCUT dört şartı (n >= 30; ortalama eşli fark > 0 ve ay kümeli bootstrap %95 alt uç > 0; ortalama hücre içi sıra > 0,50; 10 yuva slot portföy > 200 rastgele eş portföyün %90'ı). Etiket FON_IZI.fi_olcut_karar (FI_OLCUT 'karar' = ABD + AVR, dönem 2023 ve 2024-26): dört karar hücresi (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26) tutarsa İZ (BIST iki hücresi de tutarsa 'İZ + BIST'); değilse İZ DEĞİL. 2016-22 hücreleri ve BIST BİLGİ. Olasılık tablosu, 120 / 250 gün BİLGİ

(2) KURULUM + BofA: BofA arşivi yalnız BIST'te -> en fazla 'BIST-ADAY'. Havuz hücre (G2 girişi 17.04.2023 .. 31.08.2026, FI_OLCUT 60 gün): n >= 30 VE dört şart VE BIST 2023 ve BIST 2024-26 alt hücrelerinde ortalama eşli fark > 0 -> 'BIST-ADAY (BofA dipte)'; n < 30 -> 'ÖRNEKLEM YETERSİZ (n = ...)' ve olaylar tek tek listelenir; değilse 'yol yok' + tutmayan şartlar. Tutma dönemi, BofA'sız karşılaştırma, geniş okuma BİLGİ (karar değiştirmez)

(3) İZLEME: karar yok, öneri değil

## Olay sayımı (getiri içermez)

- Fiyat verisi: {"BIST": {"okunan": 630, "manifest_sha256": "5182947ec875fd59d89f61c25a24258bbdad4f376c15287fb5ffb4b50c9e2e56", "son_tarih": "2026-11-13", "bas": "2015-01-01", "hisse": 629}, "ABD": {"dosya": "/tmp/veri/V_ABD.pkl", "sha256": "82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e", "hisse": 1411, "evren_disi_cikan": [], "atlanan": 0, "ilk": "2015-06-01", "son": "2026-10-22"}, "AVR": {"dosya": "/tmp/veri/V_AVR.pkl", "sha256": "0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2", "hisse": 581, "evren_disi_cikan": [], "atlanan": 0, "ilk": "2015-01-01", "son": "2026-10-27"}}
- (1) kurulum olayları: {"BIST": {"olay": 121, "hisse": 61, "hucre": {"2016-22": 56, "2023": 4, "2024-26": 34}, "kriz_sonrasi_giris": 24, "hucre_disi_once": 3, "kurulumdaki_hisse_bugun": 10}, "ABD": {"olay": 763, "hisse": 287, "hucre": {"2016-22": 508, "2023": 81, "2024-26": 165}, "kriz_sonrasi_giris": 9, "hucre_disi_once": 0, "kurulumdaki_hisse_bugun": 3}, "AVR": {"olay": 43, "hisse": 19, "hucre": {"2016-22": 32, "2023": 3, "2024-26": 8}, "kriz_sonrasi_giris": 0, "hucre_disi_once": 0, "kurulumdaki_hisse_bugun": 0}}
- (2) BofA: {"tetik": 5519, "tetik_kurulum_bilinen": 5519, "tetik_kurulumlu": 1, "tetik_kurulumlu_hisse": 1, "tetik_genis": 8, "olay60": 1, "olay60_hucre": {"2023": 0, "2024-26": 0}, "olay60_kriz_sonrasi": 1, "olay60_genis": 5, "kurulum_olay_arsiv_donemi": {"bofasiz": 36, "bofali": 2}}

## Ön kayıttan önce görülenler (sonuç değil)

- Önceki BOFA_IZI ölçümleri (Ç171 tutma dönemi KANIT YOK; Ç172 kâr / yol YOL YOK; çökmüş (-%60) alt kümede n 20, eşli -%7,8 'yetersiz'). Bu çalışmanın hiçbir getirisi, eşli farkı, olasılığı hesaplanmadı; yukarıdaki sayılar yalnız olay / tetik / hisse sayısıdır.
- Veri: V_ABD 1.411 hisse (2015-06 .. 2026-10-22), V_AVR 581 hisse (2015-01 .. 2026-10-27), BIST Yahoo 630 hisse (son 13.11.2026); günlük kırık sayısı (|ln r| > ln 3: ABD 98, AVR 2 bar) eşik seçiminden önce görüldü; getiri görülmedi.

## Bilinen yanlılıklar

Fiyat evreni bugün işlem gören hisseler (BIST Yahoo önbelleği, V_ABD, V_AVR): -%80 düşüp sonra batan / kotasyondan çıkan şirketler evrende yok -> P(+%100) yukarı, P(-%50) aşağı yanlı; derin düşmüşlerde batma eşlerden sık olduğu için eşli fark da yukarı yanlı olabilir (ABD'de 2016'da işlem görenlerin %44'ü sonradan çıkmış, IZ_VERI_ENVANTERI). AKD kodu kurum kimliği değildir; BofA arşivi her günü kapsamaz ('BofA'sız' olayların bir kısmında görülmemiş BofA alımı olabilir). Yahoo düzeltmesi bedelli sermaye artırımlarında eksik olabilir (kırık kuralı yalnız büyük sıçramayı yakalar). İşlem maliyeti / kayma yok; çok düşük fiyatlı hissede açılıştan alım varsayımı iyimser.

ESIK_SHA256: cac944c2b07c71bdb98549ed30b66918d0ac17c64a9908c3be3e8d37b2f5afbb
KOD_SHA256: b41b1670b3e2bc2a181411b8238fcf6ca5572d1291eab193fbf4d7084ad4d02e
LISTE_SHA256: 7020587fbc90cf88875211103fd2a3173789ec57954a8d6609d99bad195a1abd
HABER_SHA256: d9d3278417e1f157b26fe961f0b287d5d3b21f3475cd0b02a237f6cfc82e35d3
BIST_SHA256: 5182947ec875fd59d89f61c25a24258bbdad4f376c15287fb5ffb4b50c9e2e56
ABD_SHA256: 82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e
AVR_SHA256: 0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2
