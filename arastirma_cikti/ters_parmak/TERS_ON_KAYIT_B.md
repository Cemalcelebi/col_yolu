# TERS PARMAK İZİ — ADIM B ÖN KAYDI (doğrulama; ileriye doğru)

TERS_PARMAK v1.1 (2026-11-15): büyük mum (B1) ve 20 günlük büyük hareket (BH2) öncesi bölge parmak izi — keşif (2016-22) / ön kayıt / ileriye doğru doğrulama

- TP_ESIK_SHA: `bd30046c5d65b2d1d065dfb9e12db9ad3e63973183f7fab87157739f3e1dce5c`
- TP_KOD_SHA: `aa97f67f6883f68e649691b8dc8e124402294d759bfe2984c112cea82254586c`
- TP_KURAL_SHA: `2c3d828f238364486f8a550da5112aeb0eaf87f7d1c426da359d6f33b3fb97ae`
- ZAMAN (UTC): `2026-11-15T05:38:01Z`
- Keşif koşusu: 2026-11-15T05:32:17Z; kurallar dosyası commit 9a66102c6e (2026-11-15T05:36:22+00:00)

Bu dosya doğrulamadan ÖNCE yazıldı. Panel 2023-01-01 'kes' ile kuruldu: 2023 ve sonrası büyük mum etiketleri / sonuçları HESAPLANMADI (yalnız profil günü sayımı). `dogrula` bu dosya git'e işlenmiş ve değişmemiş değilse ya da sha'lardan biri tutmazsa durur.

## Cetvel mühür satırları (ORTAK_CETVEL; aynen)

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`

## Önceki işlerden farkı

K23 (Ç95, bölge parmak izi) ve K44 (Ç123, INTEM parmak izi) TEK bir bölgenin (Cemal'in işaretlediği MANAS / BINBN / INTEM) ölçülerine en yakın bölgeleri arayıp sonraki getiriyi ölçtü: çıkış noktası seçilmiş bir örnekti. K46 / K48 (Ç125, Ç128) makineye '20 günde +%8 önce' dönüş etiketini öğretti: çıkış noktası GETİRİ etiketiydi, bölge değil. Ç58 SESSIZ_ML alış / satış sinyali öğretti. VDYT / VDYT2 (Ç162-Ç163) önce sıkışma bölgesini tanımlayıp sonra genişlemeyi ölçtü ve VDYT2-B (Ç164) büyük mumun bölgenin KENDİ küçük mumlarına göre tanımlanmasının üstünlüğü tanımsal yaptığını gösterdi. Bu iş TERSİNDEN başlar: çıkış noktası sinyal ya da bölge değil, MUTLAK ölçekli BÜYÜK MUMDUR (hissenin 250 günlük ATR / σ'sına göre; bölgeden bağımsız); profil büyük mumdan geriye bakarak keşif verisinde (2016-22) çıkarılır, burada dondurulur ve yalnız görülmemiş 2023 / 2024-26 verisinde ileriye doğru ölçülür (keşif / doğrulama kesin ayrı).

## Dondurulan aday kurallar (ters_kurallar.json; keşif kontrol yüzdeliklerinden eşikler)

| Kod | etiket | kural | keşif ABD LR (duyarlılık_cc) | keşif AVR LR (duyarlılık_cc) |
|---|---|---|---|---|
| P1 | B1 | son_mum >= 1.219 (kontrol %70) VE konum_250 >= 0.8062 (kontrol %70) VE kucuk_dizi_40 <= 1 (kontrol %30) | 2,03 (%16,2) | 1,71 (%11,4) |
| P2 | B1 | son_mum >= 1.219 (kontrol %70) VE dusus_120 >= -0.271 (kontrol %70) | 1,86 (%15,5) | 1,61 (%11,0) |
| P3 | B1 | son_mum >= 1.219 (kontrol %70) VE egim_40 >= 0.09793 (kontrol %70) | 1,87 (%17,7) | 1,56 (%12,8) |
| H1 | BH2 | bant_5 >= 1.404 (kontrol %70) VE dusus_120 <= -1.346 (kontrol %20) VE konum_250 <= 0.07779 (kontrol %10) | 2,37 (%10,0) | 2,49 (%10,1) |
| H2 | BH2 | konum_250 <= 0.1682 (kontrol %20) VE dar_bant_gun <= 3 (kontrol %20) VE bant_20 >= 2.119 (kontrol %80) | 2,33 (%10,1) | 2,33 (%10,6) |
| H3 | BH2 | bant_10 >= 2.865 (kontrol %90) VE dusus_120 <= -1.346 (kontrol %20) VE dar_bant_gun <= 2 (kontrol %10) | 2,42 (%10,2) | 2,09 (%11,0) |

```json
[
 {
  "ad": "son_mum>=q70 & konum_250>=q70 & kucuk_dizi_40<=q30",
  "kosul": [
   {
    "olcu": "son_mum",
    "yon": ">=",
    "yuzdelik": 0.7,
    "esik": 1.2194194793701172
   },
   {
    "olcu": "konum_250",
    "yon": ">=",
    "yuzdelik": 0.7,
    "esik": 0.8062045812606811
   },
   {
    "olcu": "kucuk_dizi_40",
    "yon": "<=",
    "yuzdelik": 0.3,
    "esik": 1.0
   }
  ],
  "olcu_set": [
   "son_mum",
   "konum_250",
   "kucuk_dizi_40"
  ],
  "cc": {
   "ABD": {
    "duyarlilik_cc": 0.1619456602527046,
    "yanlis_cc": 0.07959369064332315,
    "LR": 2.0346544926333263
   },
   "AVR": {
    "duyarlilik_cc": 0.11429079274795592,
    "yanlis_cc": 0.06693921080696764,
    "LR": 1.7073818374933618
   }
  },
  "skor": 1.7073818374933618,
  "kod": "P1",
  "etiket": "B1"
 },
 {
  "ad": "son_mum>=q70 & dusus_120>=q70",
  "kosul": [
   {
    "olcu": "son_mum",
    "yon": ">=",
    "yuzdelik": 0.7,
    "esik": 1.2194194793701172
   },
   {
    "olcu": "dusus_120",
    "yon": ">=",
    "yuzdelik": 0.7,
    "esik": -0.2710338175296784
   }
  ],
  "olcu_set": [
   "son_mum",
   "dusus_120"
  ],
  "cc": {
   "ABD": {
    "duyarlilik_cc": 0.15492608803369395,
    "yanlis_cc": 0.08332645139978528,
    "LR": 1.8592666005946483
   },
   "AVR": {
    "duyarlilik_cc": 0.110024884464984,
    "yanlis_cc": 0.06836118023462495,
    "LR": 1.609464378575143
   }
  },
  "skor": 1.609464378575143,
  "kod": "P2",
  "etiket": "B1"
 },
 {
  "ad": "son_mum>=q70 & egim_40>=q70",
  "kosul": [
   {
    "olcu": "son_mum",
    "yon": ">=",
    "yuzdelik": 0.7,
    "esik": 1.2194194793701172
   },
   {
    "olcu": "egim_40",
    "yon": ">=",
    "yuzdelik": 0.7,
    "esik": 0.09793169647455215
   }
  ],
  "olcu_set": [
   "son_mum",
   "egim_40"
  ],
  "cc": {
   "ABD": {
    "duyarlilik_cc": 0.17714096952679825,
    "yanlis_cc": 0.09455776695020233,
    "LR": 1.873362445414847
   },
   "AVR": {
    "duyarlilik_cc": 0.12762175613224316,
    "yanlis_cc": 0.08165659438322076,
    "LR": 1.5629081410535481
   }
  },
  "skor": 1.5629081410535481,
  "kod": "P3",
  "etiket": "B1"
 },
 {
  "ad": "bant_5>=q70 & dusus_120<=q20 & konum_250<=q10",
  "kosul": [
   {
    "olcu": "bant_5",
    "yon": ">=",
    "yuzdelik": 0.7,
    "esik": 1.4036540389060974
   },
   {
    "olcu": "dusus_120",
    "yon": "<=",
    "yuzdelik": 0.2,
    "esik": -1.345697283744812
   },
   {
    "olcu": "konum_250",
    "yon": "<=",
    "yuzdelik": 0.1,
    "esik": 0.07779407128691673
   }
  ],
  "olcu_set": [
   "bant_5",
   "dusus_120",
   "konum_250"
  ],
  "cc": {
   "ABD": {
    "duyarlilik_cc": 0.10007600709399544,
    "yanlis_cc": 0.042207112970711294,
    "LR": 2.3710697095875997
   },
   "AVR": {
    "duyarlilik_cc": 0.10124688279301745,
    "yanlis_cc": 0.04068241469816273,
    "LR": 2.488713699621913
   }
  },
  "skor": 2.3710697095875997,
  "kod": "H1",
  "etiket": "BH2"
 },
 {
  "ad": "konum_250<=q20 & dar_bant_gun<=q20 & bant_20>=q80",
  "kosul": [
   {
    "olcu": "konum_250",
    "yon": "<=",
    "yuzdelik": 0.2,
    "esik": 0.16815438866615295
   },
   {
    "olcu": "dar_bant_gun",
    "yon": "<=",
    "yuzdelik": 0.2,
    "esik": 3.0
   },
   {
    "olcu": "bant_20",
    "yon": ">=",
    "yuzdelik": 0.8,
    "esik": 2.118976593017578
   }
  ],
  "olcu_set": [
   "konum_250",
   "dar_bant_gun",
   "bant_20"
  ],
  "cc": {
   "ABD": {
    "duyarlilik_cc": 0.10083607803394984,
    "yanlis_cc": 0.04335774058577406,
    "LR": 2.3256764921702304
   },
   "AVR": {
    "duyarlilik_cc": 0.10623441396508729,
    "yanlis_cc": 0.04552796285079749,
    "LR": 2.3333882588429153
   }
  },
  "skor": 2.3256764921702304,
  "kod": "H2",
  "etiket": "BH2"
 },
 {
  "ad": "bant_10>=q90 & dusus_120<=q20 & dar_bant_gun<=q10",
  "kosul": [
   {
    "olcu": "bant_10",
    "yon": ">=",
    "yuzdelik": 0.9,
    "esik": 2.8652442693710327
   },
   {
    "olcu": "dusus_120",
    "yon": "<=",
    "yuzdelik": 0.2,
    "esik": -1.345697283744812
   },
   {
    "olcu": "dar_bant_gun",
    "yon": "<=",
    "yuzdelik": 0.1,
    "esik": 2.0
   }
  ],
  "olcu_set": [
   "bant_10",
   "dusus_120",
   "dar_bant_gun"
  ],
  "cc": {
   "ABD": {
    "duyarlilik_cc": 0.10159614897390423,
    "yanlis_cc": 0.04194560669456067,
    "LR": 2.4220927286546745
   },
   "AVR": {
    "duyarlilik_cc": 0.10972568578553615,
    "yanlis_cc": 0.05249343832020997,
    "LR": 2.0902743142144637
   }
  },
  "skor": 2.0902743142144637,
  "kod": "H3",
  "etiket": "BH2"
 }
]
```

## Ölçüm ve karar (önceden yazılı; eşik sonuca göre oynanmaz)

- B1 büyük mum: hissenin kendi geçerli barlarında gün t: gerçek aralık TR_t = max(H_t, C_t-1) - min(L_t, C_t-1) >= 3 x ATR250(t-1) VE |C_t / C_t-1 - 1| >= 2 x σ250(t-1); ATR250(t-1) = t-250..t-1 TR ortalaması, σ250(t-1) = t-250..t-1 günlük ln getiri std (ddof 1); t-1 ile t arası en çok 7 takvim günü (askı / boşluk sonrası sıçrama sayılmaz); yön = getiri işareti (yukarı / aşağı ayrı etiket). Büyük mum günü HİÇBİR ölçüye girmez (önceki pencere t-1'de biter).
- BH2 büyük hareket: BH2 (iki etiketin ikincisi; koordinatör eki 15 Kas, keşiften ÖNCE): gün s kapanışından sonraki 20 işlem gününde (s+1..s+20) kapanıştan kapanışa en büyük |ln(C_s+k / C_s)| >= max(%15, 3 x σ250(s) x √20); yön = o en büyük hareketin işareti. Gerekçe: BIST ±%10 fiyat sınırı tek günlük büyük mumu (B1) imkânsız kılar; 'günlerce süren tavan / taban serisi' BH2 ile yakalanır. Keşif satırı s'dir (önceki pencere s'de biter, s dahil; hareket s+1'de başlar); aynı hissede 20 barda bir (ilk etiketli s). İlk 5 gün = aynı eşikle s+1..s+5.
- Etiket ve karar: her etiketin kuralları (B1 -> P1-P3, BH2 -> H1-H3) KENDİ etiketinde karar; BH o etiketin 3 kuralı içinde. Çapraz ölçüm (P kuralları BH2'de, H kuralları B1'de) bilgi. ABD / AVR'de iki etiket; BIST bilgi hücresinde BH2 ana, B1 ek.
- KAT ve duyarlılık her kural için İKİ etikette ayrı sütun (B1: olay = s+1..s+20'de büyük mum; BH2: olay = s+1..s+20'de büyük hareket); karar kuralı (aşağıda) etiket başına aynen, BH o etiketin kendi 3 kuralı içinde.
- Uygunluk: profil / pencere son günü s (büyük mum için s = t-1): ATR250 ve σ250 tanımlı (>= 251 bar); likidite = s'de biten 20 barın C x V (x Kur, AVR EUR) medyanı, aynı pazar aynı gün kesitinin alt %20'si dışarı; bölünme şüphesi (OC.oc_bolunme_supheli) [s-60, s] barlarında varsa dışarı (yalnız geçmiş pencere); ABD k34 hissesi evren_bas'tan önce dışarı.
- Doğrulama: profil günü s: kural s'de doğru VE uygun; aynı hissede 20 barda bir (ilk). OLAY = s+1..s+20 barında en az bir büyük mum (yalnız fiyat tanımı; geçerli bar), ilk 5 = s+1..s+5. EŞ = aynı gün, aynı pazar, gün içi σ250 ondalığı x likidite üçlüsü, uygun, profil DIŞI, sonucu ölçülebilir hisseler (en az 3); eş oranı = eşlerin olay oranı. KAT = Σ olay / Σ eş oranı (OC.oc_kat: ay kümeli bootstrap 2000, tohum 27, %95). DUYARLILIK = hücrenin uygun, 20 günde bir tekilleştirilmiş büyük mumlarından (s = t-1 uygun) önceki 20 barda (t-20..t-1) en az bir profil günü (tekilsiz) olanların payı. Hücre GEÇER = n >= 30 VE KAT alt uç > 1 VE duyarlılık >= %5. p_hücre = bootstrap KAT <= 1 payı ((k+1)/(B+1)); p_kural = dört karar hücresinin en büyüğü; 3 kural BH (alfa 0,05). ETİKET: dört karar hücresi GEÇER ve BH q <= 0,05 -> PARMAK İZİ VAR; en az bir hücre GEÇER (dördü değil ya da BH tutmaz) -> EMARE; hiçbiri geçmez ve dört hücrede n >= 1.000 -> İZ DEĞİL (parmak izi yok, güç yeterli); aksi -> ÖLÇÜLEMEDİ. BIST bilgi.
- Karar hücreleri: ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26 (dönem = profil günü s tarihi; 2024-26 = 2024-01-01 .. 2026-08-31, sonuç penceresi 31.08.2026'yı aşan gün ölçülmez). BIST 2023 / 2024-26 bilgi (V_BIST 2023-06'dan; 250 bar şartıyla ilk uygun gün ~2024-06).
- İkinci ölçü: ilk 5 gün KAT (bilgi). Üçüncü: yön (büyük mumla biten profil günlerinde ilk büyük mumun yukarı payı vs aynı günlerin profilsiz büyük mumlu eşleri; bilgi). Dördüncü: ORTAK_CETVEL oc_olc ile profil günlerinin (cetvelin 60 gün tekilleştirmesiyle) 60 gün eşli getirisi + olasılık tablosu (giriş = s sonrası ilk açılış; yön bilinmediği için yalnız bilgi; cetvel etiketleri yazılır, karar değil).
- Kör grafik seti: doğrulama setinden (s >= 2023-01-01; ABD + AVR) P1 profil günlerinden rastgele 20 + her birinin günü ve katmanından (σ250 ondalığı x likidite üçlüsü) rastgele bir profilsiz uygun hisse (20 kontrol); 120 bar önce + s + 20 bar sonra; KOR_TEST v1.1 çizimi (ortak log ölçek, %10 cetveli, hisse adı / tarih yok); s'nin sağına kesikli dikey çizgi; sıra karıştırılır; anahtar ayrı json. Amaç: Cemal 'bunlar gerçek sıkışma mı' diye kendi gözüyle yargılar; ölçüm değil.
- Hayatta kalma: evren bugün işlem gören hisseler (ABD + k34 nakdi biten); batanlar yok: büyük aşağı mum olasılığı aşağı yanlı olabilir.
- İleri test (IK_ILERI önerisi): aynı komut, aynı kurallar (bu sha), aynı eşikle Eylül 2026 - Şubat 2027 verisi geldiğinde (kriz sonrası dönem ayrı hücre; en erken Mart 2027) yeniden ölçülür.

## Veri sha256

- V_ABD.pkl: `82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e`
- V_AVR.pkl: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2`
- V_BIST.pkl: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`

## PROFİL GÜNÜ SAYIMI (sonuç hesaplanmadan; uygun, 20 günde bir tekil / tekilsiz)

| Kural | Pazar | Dönem | profil günü (tekil) | profil günü (tekilsiz) | uygun satır |
|---|---|---|---|---|---|
| P1 | ABD | 2023 | 3145 | 15096 | 443725 |
| P1 | ABD | 2024-26 | 16762 | 113510 | 1354761 |
| P1 | AVR | 2023 | 838 | 2953 | 114920 |
| P1 | AVR | 2024-26 | 4806 | 26516 | 309737 |
| P1 | BIST | 2023 | 1131 | 10842 | 89791 |
| P1 | BIST | 2024-26 | 3083 | 25845 | 280738 |
| P2 | ABD | 2023 | 5800 | 23519 | 443725 |
| P2 | ABD | 2024-26 | 22898 | 133993 | 1354761 |
| P2 | AVR | 2023 | 1645 | 4791 | 114920 |
| P2 | AVR | 2024-26 | 5637 | 25384 | 309737 |
| P2 | BIST | 2023 | 1474 | 11825 | 89791 |
| P2 | BIST | 2024-26 | 4344 | 30213 | 280738 |
| P3 | ABD | 2023 | 5554 | 24234 | 443725 |
| P3 | ABD | 2024-26 | 22394 | 150705 | 1354761 |
| P3 | AVR | 2023 | 1415 | 4616 | 114920 |
| P3 | AVR | 2024-26 | 5641 | 29631 | 309737 |
| P3 | BIST | 2023 | 1889 | 20193 | 89791 |
| P3 | BIST | 2024-26 | 4968 | 44055 | 280738 |
| H1 | ABD | 2023 | 1473 | 5869 | 443725 |
| H1 | ABD | 2024-26 | 4940 | 19085 | 1354761 |
| H1 | AVR | 2023 | 253 | 817 | 114920 |
| H1 | AVR | 2024-26 | 946 | 3229 | 309737 |
| H1 | BIST | 2023 | 108 | 336 | 89791 |
| H1 | BIST | 2024-26 | 448 | 1328 | 280738 |
| H2 | ABD | 2023 | 497 | 1410 | 443725 |
| H2 | ABD | 2024-26 | 2089 | 5928 | 1354761 |
| H2 | AVR | 2023 | 86 | 221 | 114920 |
| H2 | AVR | 2024-26 | 500 | 1402 | 309737 |
| H2 | BIST | 2023 | 58 | 118 | 89791 |
| H2 | BIST | 2024-26 | 151 | 334 | 280738 |
| H3 | ABD | 2023 | 225 | 437 | 443725 |
| H3 | ABD | 2024-26 | 1195 | 2492 | 1354761 |
| H3 | AVR | 2023 | 39 | 76 | 114920 |
| H3 | AVR | 2024-26 | 338 | 645 | 309737 |
| H3 | BIST | 2023 | 168 | 334 | 89791 |
| H3 | BIST | 2024-26 | 132 | 335 | 280738 |

Kural: hücrede n < 30 ise ÖLÇÜLEMEDİ; İZ DEĞİL yalnız dört karar hücresinde n >= 1.000 iken.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | keşif kontrolü: aynı pazar, aynı takvim ayı, aynı σ250 ondalığı x likidite üçlüsü, uygun, ertesi gün büyük mum olmayan rastgele satırlar (büyük mum başına 5; tp_kesif_orneklem); doğrulama eşi: aynı gün, aynı pazar, σ250 ondalığı x likidite üçlüsü, profilsiz (tp_kural_olc). Mekanik üstünlük: büyük mum hissenin kendi ATR250 / σ250'sine göre; σ250 eşlendiği için 'oynak hisse' etkisi dışlanır, son 20 gün oynaklığı eşlenmez (ölçü olarak raporda: oynaklık kümelenmesi). 60 gün getirisi yalnız OC.oc_olc |
| K2 | geleceğe bakma | EVET | ölçüler yalnız s'ye kadar barlarla (geriye pencere; büyük mum günü hariç); büyük mum etiketi ATR / σ'yı t-1'den alır; keşif ve ön kayıtta 2023-01-01'den sonraki büyük mum etiketleri panelde NaN (tp_panel kes); dogrula 30 rastgele profil gününde seri s'de kesilince ölçüler ve kural aynı (tp_gelecek_denetimi; test 'geleceğe bakma'). Sınır: bölünme şüphesi tespiti 10 bar sonrasını kullanır (cetvel ile aynı veri temizliği) |
| K3 | geçerli bar | EVET | OC.oc_veri temiz bar (H>L, V>0, fiyat > 0); geçersiz bar atılır, büyük mum ve ölçüler yalnız geçerli barlarla; t-1 / t arası > 7 takvim günü ise büyük mum sayılmaz (askı sonrası sıçrama) |
| K4 | tekilleştirme | EVET | büyük mum aynı hissede 20 barda bir (ilk; uygunluk süzgecinden sonra); profil günü 20 barda bir; n = bağımsız gün; 60 gün ölçüsünde OC.oc_olc kendi 60 gün tekilleştirmesi; KAT oran-oran (ortalama) + sayılar |
| K5 | giriş fiyatı | EVET | KAT ölçüsü olay olasılığıdır (fiyat girişi yok); 60 gün eşli getiri OC.oc_olc: giriş = s'den sonraki ilk geçerli bar açılışı |
| K6 | veri birimi | EVET | tek kip fi_k1_veri düzeltilmiş fiyat (V_*.pkl); bütün ölçüler ATR250 / σ250 ile ölçeksiz; AVR likidite x Kur (EUR); bölünme şüphesi geçmiş pencerede dışarı; büyük mum günündeki bölünme şüphesi sayısı keşif raporunda (dışlanmaz, iş tanımı) |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler (+ ABD k34 nakdi biten, yine bugün işlem gören); batanlar yok; raporda 'hayatta kalma' notu: büyük aşağı mumlar ve 60 gün getirisi yukarı yanlı okunmalı |
| K8 | örneklem ve dönem | EVET | keşif 2016-22 / doğrulama 2023 ve 2024-26 ayrı; n < 30 hücre ÖLÇÜLEMEDİ; tek ölçüde BH q 0,10, kurallarda BH (3 kural); İZ DEĞİL yalnız dört hücrede n >= 1.000; profil günü sayımı ön kayıtta sonuç hesaplanmadan |
| K9 | ön kayıt | EVET | arama yordamı ve bütün eşikler (TP_ESIK) keşiften önce commit'li kodda; kurallar ters_kurallar.json sha256 + TP_ESIK sha + kod sha + cetvel üç sha ön kayıt B'de; dogrula OC.oc_kapi + tp_onkayit_dogrula (git işlenmiş / değişmemiş) geçmezse durur; eşik doğrulama sonucuna göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | metin / KAP ayrıştırma yok; yalnız OHLCV; 3 büyük mum ham veriden elle doğrulanır (rapor DENETİM) |
| K11 | yeniden üretim | EVET | satır verisi /tmp/ters_parmak (keşif örneklemi, profil günleri, olaylar); 3 ölçünün d / AUC'u ve 2 hücre KAT'ı bağımsız kodla yeniden üretilir (rapor DENETİM) |
| K12 | ifade | EVET | 'parmak izi var / emare / iz değil / ölçülemedi' yalnız ön kayıtlı kuralla; KAT olasılık oranıdır, kâr değil; yön bilinmediği için 60 gün getirisi yalnız bilgi; sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_tp; yasak dosyalar (IZ_KARNE, defterler, ORTAK_CETVEL, FON_IZI, COL_v1, takip, K58, VDYT*, SIKISMA_YENIDEN, D9_YENIDEN, K24_YENIDEN, DIP_COL_AYRIM, INTEM_ILERI) yalnız okunur / içe alınır, git diff denetimi; e-posta / anahtar taraması testte; ücretli veri yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; araştırma ölçümü |

## Test

`python test_ters_parmak.py` (sentetik: büyük mum tanımı, önceki pencere ölçüleri yalnız s öncesi, geleceğe bakma kesme testi, kontrol eşleme, kural uygulaması, KAT bootstrap = OC.oc_kat, kapı, e-posta / anahtar taraması).
