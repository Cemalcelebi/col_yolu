# HİPOTEZ ENVANTERİ (21 Kasım 2026)

Derleyen: alt ajan (derleme; ölçüm yok, web yok). Ana tablo `arastirma_cikti/kasa/hipotez_envanteri.py` ile IK_KAYIT'tan mekanik çıkarıldı; aile / karar / güvenilirlik sınıfları kayıt metni okunarak doldurulan sözlüklerdedir (betiğin başında). Uydurma yok: bulunamayan yerde "kayıtta yok" yazıldı.

Dayanak: IK_KAYIT (204 Ç), IK_ILERI (39 satır), IK_HATA (289 satır), KURAL_DEFTERI_TASLAK (A-K), HAKEM_DERSLER + GOZ_ETIKET (C1-C13, CD / VD), SINYAL_ENVANTERI + K60 olasılık tablosu, DS_ELESTIRI + DS_RAPOR, COL_OZET (kapalı konular).

## 1. BİR SAYFALIK ÖZET (Cemal için)

- **Kaç çalışma:** kayıt defterinde 204 Ç çalışması (Ç01-Ç204). Üç kaydı parçalara böldüm (Ç173 iki, Ç181 üç, Ç182 iki parça) → 208 satır. Bunlardan 26 satır araç / denetim / altyapı (hipotez değil), **182 satır gerçek hipotez**. Yanına: K60 sinyal kütüphanesinden 126 sinyal-uç çifti, düşüş sonrası (DS) web hipotezlerinden 87, Cemal'in sözlerinden 140 kural + K1-K51 + C1-C13 + dersler.
- **Sonuç özeti (Ç satırları, gerçek hipotezler):** İZ DEĞİL 117 · ÖLÇÜLEMEDİ 25 · EMARE 7 · ADAY 18 · KAPALI 6 · KARAR KAYITTA YOK 9. Hiçbiri İZ değil.
- **Asıl bulgu:** kayıtta "İZ DEĞİL" yazılı 117 satırdan yalnız **28**'i güç yeterli (A: Ç175 "hak eden gövde" + kayıtta güç yeterli yazılı); 14'i Ç175'in kendi yeniden etiketlemesiyle **ÖLÇÜLEMEDİ**; 68'inde hücre n < 1.000 ya da n kayıtta yok (B / B*; K58); kalan 7: h5 (C) ya da doğrulanmamış A?. Yani çoğu "iz yok" aslında "bakamadık".
- **Cetvel sorunu ve Ç204:** Ç190-Ç203 arasında 15 bar h5 cetveli oynaklığı ödüllendirdi (Ç203). Ç204 (21 Kas) Ç194-Ç202'yi düzeltilmiş CETVEL2 R15 (stop'suz) ile yeniden koştu: KATKI+ 0, KATKI− 0, 66 etiket değişti; eski h5 üstünlükleri (+9..+34 puan) R15'te −0,2..+0,7 puana indi (oynaklıkmış); 52 hipotez 'İZ DEĞİL (+2 puan ve üstü için)', güçsüz hücreler ÖLÇÜLEMEDİ. Ç190-Ç193 yeniden koşulmadı, h5 etiketiyle duruyor. Ç124-Ç131 '+%8 önce' cetveli de h5 akrabası.
- **Kasaya aday:** ana tabloda 46 Ç satırı kasa adayı (EVET); bunlardan öncelikle 25 kart taslağı bölüm 4'tedir (Cemal'in kendi kuralları önde).

**Aileye göre sayım (Ç satırları):**

| aile | satır |
|---|---|
| şekil / yapı | 63 |
| sektör / makro | 20 |
| momentum / gösterge / makine / sinyal kütüphanesi | 17 |
| temel / bilanço | 14 |
| Cemal'in göz kuralları / kör test | 13 |
| cetvel / altyapı / denetim | 13 |
| hacim / tavan-taban | 13 |
| evren / mekanizma / veri | 11 |
| KAP olay | 10 |
| giriş-çıkış / portföy kuralı | 8 |
| sıkışma / oynaklık | 8 |
| fon izi / büyük alıcı / BofA | 8 |
| içeriden / açığa satış | 5 |
| web hipotezleri (DS / DEVİR) | 4 |
| kripto | 1 |

**Karara göre sayım (kayıttaki etiket, normalize):**

| karar | satır |
|---|---|
| İZ | 0 |
| EMARE | 7 |
| ADAY | 18 |
| İZ DEĞİL | 117 |
| ÖLÇÜLEMEDİ | 25 |
| SINANMADI | 0 |
| KAPALI | 6 |
| KARAR KAYITTA YOK | 9 |
| ALTYAPI / DENETİM (hipotez değil) | 26 |
| (not) İZ DEĞİL satırlarının Ç175 ile ÖLÇÜLEMEDİ'ye çevrilenleri | 14 |
| (ek) DS web hipotezleri: 87 tekilleştirilmiş; ölçülen 25 → hepsi ÖLÇÜLEMEDİ; ölçülmeyen 62 → SINANMADI | 87 |
| (ek) K60 sinyal-uç çiftleri: 126 (ölçüldü; İZ ADAYI 0) | 126 |

**Güvenilirlik sayımı (bir satır birden çok harf alabilir):**

| sınıf | anlam | satır |
|---|---|---|
| A | güç yeterli, cetvel sorunsuz (karar sağlam) | 42 |
| B | n < 1.000 ya da güç yetersiz → aslında ÖLÇÜLEMEDİ (K58); "B*" kayıtta n yok | 142 |
| C | h5 (+%5 stop'tan önce) cetveli: oynaklık karışımı (Ç203) | 12 |
| D | hata defterinde ya da kayıt notunda düzeltme var | 77 |
| E | hiç ölçülmedi (SINANMADI) | Ç içinde yok; DS 62 + SINYAL_ENVANTERI + K-kuralları satırlarında (bölüm 2b-2d, 3) |

**En çok yaklaşanlar, ilk 15 (kayıttaki sayıyla; eşik dört şart ya da önceden yazılı hücre kuralı; son üçü Ç204 CETVEL2 R15 sonrası geçersiz):**

| # | kod | ne | kayıttaki sayı | neden hâlâ iz değil |
|---|---|---|---|---|
| 1 | Ç173b | −%80 dip kurulumu (ABD) | ABD 2023 n 81 +%24,8 [+8,9; +43,0] sıra 0,55 TUTTU; 2024-26 n 146 +%20,6 sıra 0,48 | 2024-26 sıra / portföy tutmadı; AVR n 3 / 8; piyango profili (P+%100 ve P−%50 ~2 kat) |
| 2 | Ç181c | Yalnız sektör rüzgârı (ABD) | ABD 2024-26 n 5.873 +%3,6 [+1,9; +5,4], +%100 katı 1,35 / 1,39 | portföy şartı tutmadı; −%50 üst ucu 1'i aşıyor; AVR ölçülemez (kapalı konu) |
| 3 | Ç128 | Geniş makine üst %5 (+%8 önce) | ABD 2024-26 +12,4, AVR +10,8 / +11,3; ABD 2023 +6,9 | ABD 2023 eşiğin (10) altında; oynaklık eşli rastgele cetvel |
| 4 | Ç125 | Dönüş noktası makinesi üst %5 | ABD +3,6 / +12,2, AVR +4,6 / +12,8, BIST +27,7 / +12,6 | 2023 hücreleri eşik altı |
| 5 | Ç127 | Sert düşüş sonrası makine üst %5 | ABD +21,8 / +16,6 puan, işlem +%2,9 / +%2,4; AVR 2023 +15,3 (n 59), 2024-26 0,0 | AVR 2024-26 sıfır; portföy piyasanın altı |
| 6 | Ç182a | Büyük mum öncesi profil P1 | ABD n 3.145 / 16.258, AVR 838 / 4.679; dört hücre alt uç > 1; BH q 0,001 | yön yok; oynaklık (ATR10 / ATR250) eşlemeli kontrol bekliyor |
| 7 | Ç118 | K24 çöl + iyi bilanço (ABD) | ABD 2023 +%7,7 (n 52, aralık artı); 2024-26 −%0,4 (n 170) | iki hücrede tutmadı; portföy tabanın altında |
| 8 | Ç112 | Blok hacimli taban günü (ABD) | ABD 2024-26 +%14,9 dört şart tutar; 2023 +%4,4 | 2023 aralık 0'ı içeriyor; AVR n 8 / 24; BIST ters |
| 9 | Ç155 | BETA_BAB ALT havuz içi (ABD) | +%100 katı 1,34 / 1,45 / 1,36; −%50 katı 0,91 / 0,73 / 0,98 | İZ değil (yalnız ABD, yalnız yaşayanlar); yükseliş etkisi olabilir |
| 10 | Ç154 | DOSYA_Y / COMP4 güvenli uç (ABD) | −%50 katı COMP4 0,43 / 0,25 / 0,47; DOSYA_Y 0,62 / 0,54 / 0,61; +%100 katı ~1 | kazanma artmıyor (koruma); yalnız yaşayanlar |
| 11 | Ç115 | ABD gece hareketi → Avrupa açılış boşluğu | boşluk +%0,23 / +%0,19 / +%0,23 (üç dönem aralık artı) | alınabilir gün içi fazla yalnız 2023 (+%0,24) |
| 12 | Ç102 | Çölde içeriden alım (ABD) | +%7,3 (aralık +0,3..+16,1, dört şart tuttu) 2023; 2024-26 +%7,2 aralık 0'ı içeriyor | örneklem dışı 2016-22 −%4,5 / −%3,5; aday güçlenmedi |
| 13 | Ç193 | Dipte S6 kırılımı Y9 (ABD, 15 bar) | KAT5 1,15 [1,05; 1,29] ve 1,21 [1,06; 1,36]; konum eşli 1,15 / 1,20 | bakılmış hücreler; n 146 / 231; h5 cetveli (C); Ç204: dipte (Ş1) fark R15'te −0,2..+0,7 puan, aralık 0'ı kesiyor → oynaklıkmış |
| 14 | Ç197 | F1-F29 puan üst %20 (15 bar) | ABD 2024-26 %50,7 vs %44,2, KAT 1,15 [1,06; 1,24]; AVR 2023 1,46 [1,18] | TUTAR hücre yok; stop payı eşten büyük; Ç204 R15: KATKI+ 0 (4 hipotez SORGULA) |
| 15 | Ç196 | Dip grubu G2 − trend içi raf G1 | ABD +18 / +27 / +13, AVR +22 / +34 / +18 puan (alt uç > 0) | G2 n 20-346 güç < %80; Ç204: h5 farkları R15'te −0,2..+0,7 puana indi (oynaklık) |

## 2. ANA TABLO (her Ç kaydı bir satır)

Satır sayısı kontrolü: IK_KAYIT uzunluğu = **204**; tablo satırı = **208** (Ç173 → 173a / 173b, Ç181 → a / b / c, Ç182 → a / b ile +4); eksik kayıt: yok; fazla: yok.

Ç204 okuma notu: CETVEL2 R15 yeniden koşusunda 'SORGULA' = karar hücrelerinin 0 / 4 (az sayıda 1 / 4) hücresi beklenen yönde tutar ve güç yeterli; Ç204 kaydı bu sınıfta güç ≥ 0,80 olanları (52 kod: Ç196 9, Ç197 3, Ç198 16, Ç199 8, Ç200 3, Ç201 2, Ç202 11) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü etki için)' diye yorumlar; 'ÖLÇÜLEMEDİ' = n < 30 ya da güç < 0,80.

Sütunlar: kod | tarih | aile | hipotez | cetvel | pazar ve dönem (kayıt metninden) | n (kayıttaki ilk üç ifade) | karar | kayıttaki ana sayı / not | GÜVENİLİRLİK | veri | t'de bilinir ve sayısal | KASA ADAYI.

| kod | tarih | aile | hipotez | cetvel | pazar / dönem | n | karar | ana sayı / not | GÜV | veri | t'de sayısal | KASA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ç01 | 2026-09 | giriş-çıkış / portföy kuralı | Giriş noktası / zamanlaması — Tavan tanımı, teyit, retest, kırılım hacmi, ilk 8 bar kırılımda girmeyi geçer mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KAPALI | Kapalı konu (CLAUDE.md). Sistem kuralı, olay izi değil. Denetim 24 Eki: mfe_analiz 'stopsuz' satırı stoplardan farklı örneklemdendi (stop maliyeti ~2 | B + D (B*: kayıtta n yok, güç bilinmiyor / D: kayıt notunda düzeltme / denetim bulgusu var) | EVET | KAYITTA YOK | HAYIR: kapalı konu (COL_OZET: giriş / çıkış / filtre) |
| Ç02 | 2026-09 | giriş-çıkış / portföy kuralı | Aday filtreleri (E_ONC, üç şart kapısı, taban kırılması düşürme) — Kırılım öncesi eleme kâr ekler mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KAPALI | KAPALI: her filtre para kaybettirdi | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: kapalı konu (COL_OZET: giriş / çıkış / filtre) |
| Ç03 | 2026-09 | giriş-çıkış / portföy kuralı | Çıkış varyantları (fiyat/zaman stopu, desen sat, şelale, SMA200) — Trail SMA20'yi yenen çıkış var mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KAPALI | KAPALI: trail SMA20 en iyi | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: kapalı konu (COL_OZET: giriş / çıkış / filtre) |
| Ç04 | 2026-09 | şekil / yapı | Segment / şekil 90+ ölçü (alt iğne, doji, dar hafta…) — Çöl şekli sonrasını ayırır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski 'TUTAN' (alt fitil<0,12, doji, dar hafta); doji col_ogren'de ayırmadı, yeniden doğrulanmadı | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç05 | 2026-09 | sektör / makro | Rejim / dış veri (CDS, EEM, VIX, DXY, temel) — Piyasa rejimi sinyal sonucunu değiştirir mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KAPALI | CDS ve borç/öz çarpan; VIX/DXY/USDTRY tutarsız (KAPALI) | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: kapalı konu (COL_OZET: giriş / çıkış / filtre) |
| Ç06 | 2026-09 | momentum / gösterge / makine / sinyal kütüphanesi | 4h / haftalık / KNN — Başka zaman dilimi ya da ML kâr ekler mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KAPALI | KAPALI: rejime bağlı, ML kâr eklemedi | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: kapalı konu (COL_OZET: giriş / çıkış / filtre) |
| Ç07 | 2026-09-18 | Cemal'in göz kuralları / kör test | Göz kalibrasyonu v3 (29 çöl + 8 olumsuz) — Kod Cemal'in çöllerini buluyor mu? | göz kalibrasyonu / araç | kayıtta yok; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | göz kalibrasyonu (13/26 → 23/26) | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç08 | 2026-09-18 | cetvel / altyapı / denetim | Kod denetimi (12 sorun) — Sonucu şişiren hata var mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | Düzeltildi: tekil işlem, ertesi açılış, drawdown | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç09 | 2026-09-25 | şekil / yapı | Dört set ölçümü (sıcak sektör, momentum, onc250, konum250, taban koruması, çöl kalitesi) — Aday özellikleri 4 sette beklentiyi artırır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KAPALI | KAPALI: oynaklık, iz yok | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: kapalı konu (COL_OZET: giriş / çıkış / filtre) |
| Ç10 | 2026-09-25 | şekil / yapı | QMLS salınım / genç halka arz 3. dip — 3. dip alımı çalışır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | n 105 | ADAY | AÇIK: bek +1,6, n 105 | B (B: kayıtta yazılı en büyük n 105 (< 1.000; kayıtta bütün hücre n'leri yok)) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç11 | 2026-10-01 | sıkışma / oynaklık | SIKISMA_TESTI — Çöl içi/dışı bilet farkı | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | Fark yok | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç12 | 2026-10-02 | şekil / yapı | BUYUK_YUKSELIS — Büyük yükselişler çölden mi gelir? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | sektör dalgası / genişlik / konum52 1,24-1,29 hafif iz | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç13 | 2026-10-02 | giriş-çıkış / portföy kuralı | TEYIT_BILETI — Teyit sonrası bilet | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | zayıf (+1,0; 2026 −2,1) | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: kapalı konu (COL_OZET: giriş / çıkış / filtre) |
| Ç14 | 2026-10-02 | şekil / yapı | COL_KIRILIM_ATLAS (öncü/rüzgâr) — Öncü + rüzgâr sırası | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | tutarsız | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç15 | 2026-10-04 | KAP olay | A1 bedelsiz bildirimi — Bedelsiz başvurusu/onayı sonrası düşüş? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski 'GEÇERLİ' (ar60 −12/−6) | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç16 | 2026-10-04 | hacim / tavan-taban | A2 tavan günü (+%9) — Tavan günü sonrası düşüş? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski 'GEÇERLİ' (ar60 −11/−15) | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç17 | 2026-10-04 | hacim / tavan-taban | A3 taban günü (−%5 altı) — Sert düşüş günü sonrası düşüş? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski 'GEÇERLİ' (ar60 −4,8/−4,7) | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç18 | 2026-10-04 | KAP olay | A4 koşmuşken iş ilişkisi haberi — 20 günde +%25 koşmuş hissede sözleşme haberi | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski 'GEÇERLİ' (ar60 −7/−8) | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç19 | 2026-10-04 | sektör / makro | A9 OLGUN rüzgâr + sözleşme/teşvik — Olgun sektör rüzgârında haber | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | eski 'GEÇERLİ ama nötrden farkı küçük'; Ç71'de tek cetvelle İZ DEĞİL | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç20 | 2026-10-04 | KAP olay | A5 söylentiye açıklama + o gün −%5 — Söylenti açıklaması günü düşüş | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | n 26/46 | ADAY | eski ADAY, n 26/46 | B (B: kayıtta yazılı en büyük n 46 (< 1.000; kayıtta bütün hücre n'leri yok)) | EVET | KAYITTA YOK | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç21 | 2026-10-04 | KAP olay | A8 sözleşme tutarı > yıllık ciro %50 — Büyük sözleşme sonrası | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | n 29/20 | ADAY | eski ADAY, n 29/20; sözleşme tutarı kap_ozet'te yok, puanlanamadı | B (B: kayıtta yazılı en büyük n 29 (< 1.000; kayıtta bütün hücre n'leri yok)) | YOK | KAYITTA YOK | HAYIR: veri yok |
| Ç22 | 2026-10-04 | içeriden / açığa satış | A7 açığa satış — Açığa satış sonrası | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | eski 'ÇÜRÜDÜ'; veri elde yok | B (B*: kayıtta n yok, güç bilinmiyor) | YOK | KAYITTA YOK | HAYIR: veri yok |
| Ç23 | 2026-10-04 | hacim / tavan-taban | A10 hacim patlaması + gün −%5 altı — Hacimli düşüş günü sonrası | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski ADAY | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç24 | 2026-10-04 | hacim / tavan-taban | A11 A10 + 20 günde zaten −%20 — Düşmüş hissede hacimli düşüş | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski ADAY-zayıf | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç25 | 2026-10-04 | hacim / tavan-taban | A12 1 yıl en geride + hacim en çok artan — Düşerken hacim = çıkış? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski ADAY-zayıf | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç26 | 2026-10-04 | KAP olay | B1 geri alım bildirimi — Geri alım sonrası yükseliş? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski 'GEÇERLİ' (ar60 +4,9/+2,4) | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç27 | 2026-10-04 | KAP olay | B1'' geri alım + koşmamış — Koşmamış hissede geri alım | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski 'GEÇERLİ?' | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç28 | 2026-10-04 | sektör / makro | B9 yeni rüzgâr + sözleşme — Yeni rüzgârda haber | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | eski 'ÇÜRÜDÜ' (tek hisse tekrarı) | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç29 | 2026-10-04 | sektör / makro | B5 teyit günü / B6 likidite / B8 genişlik yılları — Teyit, likidite, piyasa genişliği | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski 'GEÇERLİ' (sistem filtresi); tanım defterde tam yazılı değil | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç30 | 2026-10-04 | sektör / makro | B10 kriz teyidi + küçük PD / B11 dayanıklı — Kriz sonrası küçük şirket | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski ADAY / REJİME BAĞLI; veri bu turda yok | B (B*: kayıtta n yok, güç bilinmiyor) | YOK | KAYITTA YOK | HAYIR: veri yok |
| Ç31 | 2026-10-04 | hacim / tavan-taban | B12-B13 çöl kırılım günü hacim yönü — Çölün son 4 haftası hacmi kırılım yönünü verir mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ADAY | eski ADAY yön (B13 sonradan bilgi); olay dosyası yok | B (B*: kayıtta n yok, güç bilinmiyor) | YOK | KAYITTA YOK | HAYIR: veri yok |
| Ç32 | 2026-10-04 | KAP olay | Ölü eşek (KAP kötü haber, bilanço, geride) — Ölü şirketten kaçınma | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ | test edilemez (hayatta kalma; çıkmış hisse verisi yok) | B (B*: kayıtta n yok, güç bilinmiyor) | YOK | KAYITTA YOK | HAYIR: veri yok |
| Ç33 | 2026-10-04 | şekil / yapı | Çölde erken giriş / güvenilir isim V / para izi — Çöl içinde erken alım | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | eski 'ÇÜRÜDÜ / iz değil' | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç34 | 2026-10-04 | hacim / tavan-taban | Hacimli yukarı kırılım (+%5 kapanış) — Hacimli kırılım devam eder mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | İz değil | A (A: Ç175 "İZ DEĞİL'i hak eden gövde") | EVET | KAYITTA YOK | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç35 | 2026-10-08 | şekil / yapı | col_v2 / yeniden_tara, tahtaci_oyunu — Yeni liste / tahtacı klimaksı | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | tahtacı GEÇMEDİ | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç36 | 2026-10-09 | şekil / yapı | col_ogren / col_tanim2 — Çöl metrikleri simetrik etikette ayırır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | İz yok | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç37 | 2026-10-17 | şekil / yapı | D7 küçük mum (H−L) + D9 uzun çöl + rüzgâr — Küçük mum tanımı ve uzun çöl yönü | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | 14 Kas Ç181: D9 uzun çöl İZ DEĞİL; D9 + rüzgâr ÖLÇÜLEMEDİ | B + D (B*: kayıtta n yok, güç bilinmiyor / D: "Test sürüyor" diye kalan D9 uzun çöl + rüzgâr hiç kapanmadı, yeni cetvelle puanlanmadı, üreti…) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç38 | 2026-10-19 | şekil / yapı | A13 dipte doji kutusu → sert düşüş riski — Doji kutusundan sonra sert düşüş azalır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD, BIST; dönem kayıtta yok | kayıtta yok | ADAY | eski BIST 'GEÇERLİ' risk; denetimde etkinin çoğu dipte olmaktan (B_dip 0,94 / 0,97 / 0,90) | B + D (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi / D: Doji kutusu ilk koşuda ileriye bakan 'kirilim' sütunuyla (kutu ufuk içinde kırıldı mı) seçilmi… (+1 satır)) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç39 | 2026-10-19 | şekil / yapı | Doji kutusu → sert yukarı hareket — Doji kutusu yukarı hareketi haber verir mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | 0,90-1,02 | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç40 | 2026-10-19 | Cemal'in göz kuralları / kör test | GOZ_ESLE bölge kuralı + çöl karnesi — Bölge kuralı Cemal'in gözüyle eşleşiyor mu? | göz kalibrasyonu / araç | kayıtta yok; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | Ölçüm (altyapı) | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç41 | 2026-10-20 | şekil / yapı | D12 dip çölü (COL_DIP_TEST) — Dip çölünden atılım tabanı geçer mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | 6 dönemin 3'ü | A + D (A: Ç175 "İZ DEĞİL'i hak eden gövde" / D: Hedefli işlem 120. barda kesilip verinin son barına atlıyordu; kazananlar "açık" diye atılıyor…) | EVET | KAYITTA YOK | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç42 | 2026-10-20 | cetvel / altyapı / denetim | COL_GECMIS (geçmiş gün taraması) — Kod geçmişte hangi çölleri bulurdu? | göz kalibrasyonu / araç | kayıtta yok; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | Araç | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç43 | 2026-10-21 | şekil / yapı | COL_BUGUN / COL_SEKIL / etiketler — Bugünkü kutular + şekil ölçüleri | göz kalibrasyonu / araç | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | denetim: hiçbir şekil ölçüsü çölü ayırmıyor (AUC 0,37-0,60) | B + D (B*: kayıtta n yok, güç bilinmiyor / D: "Ayıran ölçüler" kıyaslanamaz negatiflerden: 21 'bugün' kutusu kodun kendi ret nedenine göre s…) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç44 | 2026-10-21 | şekil / yapı | B14 yuvarlanma öbeği (COL_OBEK) — Öbekten sonra alım gelir mi, kazanç artar mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | eski 'ADAY yön'; denetimde yön izi de yok (mekanikti) | A + D (A: Ç175 "İZ DEĞİL'i hak eden gövde" / D: "Alım oranı tabandan +15-20p" mekanikti (taban kutusu tavana ~2 kat uzak); işlemlerin yarısı k…) | EVET | KAYITTA YOK | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç45 | 2026-10-21 | giriş-çıkış / portföy kuralı | B15 çıkış kuralı (COL_YOL) → T10 üretimde — +%8 maliyet stopu + trail kazancı artırır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD, BIST; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | portföy kuralı; T10 getiri dayanağı ters döndü | B + D (B*: kayıtta n yok, güç bilinmiyor / D: T10 dayanağı "+157 vs +144": kopya işlemler, hisse başına tek slot yok, trail ufuklu; düzeltil…) | EVET | KAYITTA YOK | HAYIR: kapalı konu (COL_OZET: giriş / çıkış / filtre) |
| Ç46 | 2026-10-21 | giriş-çıkış / portföy kuralı | COL_KAZANC ek şart + K7 küçük alım mumu + K8 NVI/CMF — Üretim yoluna şart eklemek kazanç artırır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | BIST; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | üretim yolu içi ölçüm, BIST'e özgü | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: kapalı konu (COL_OZET: giriş / çıkış / filtre) |
| Ç47 | 2026-10-21 | şekil / yapı | D13 tespit motoru (COL_TESPIT, col_dip2) — Cemal'in 3 kuralıyla tespit | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | 'alım +12..26p' mekanikti | A + D (A: Ç175 "İZ DEĞİL'i hak eden gövde" / D: ABD olayları dosyada '.US' ekliydi, adaptör okumuyordu; ABD hiç puanlanmamıştı [veri / hesap] (+1 satır)) | EVET | KAYITTA YOK | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç48 | 2026-10-21 | Cemal'in göz kuralları / kör test | COL_GOZ (746 kutu gözle) + Cemal kararı — Kodun kutuları gözle çöl mü? | göz kalibrasyonu / araç | kayıtta yok; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | 746 kutu gözle (%6 çöl) | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç49 | 2026-10-22 | şekil / yapı | MUM_SUKUN v1.1 hisseye özel mum küçülmesi — Düşüş sonrası sakin 3-4 mum | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | 0,96-1,04 | A (A: Ç175 "İZ DEĞİL'i hak eden gövde") | EVET | KAYITTA YOK | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç50 | 2026-10-22 | şekil / yapı | MUM_SUKUN v1.2 düz zemine yapışan sıra — Sert düşüş sonrası zemin sırası | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | İZ DEĞİL | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç51 | 2026-10-22 | şekil / yapı | MUM_SUKUN v1.3 kısa ufuk + ayrılma sertliği — Zeminden 3-10 günlük hareket | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | kısa ufuk; 60 gün cetveli uygun değil | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç52 | 2026-10-22 | sektör / makro | Faiz kararı günleri (TCMB) sektör/borç tepkisi — Faiz kararında hangi grup ayrışır? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KARAR KAYITTA YOK | ölçüm, karar yazılmadı | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: sonuç kayıtta yok (önce sonuç dosyası bulunmalı) |
| Ç53 | 2026-10-22 | sektör / makro | Derin dip sonrası oynaklık tercilleri — Piyasa dipteyken oynak hisse önce mi gider? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KARAR KAYITTA YOK | ölçüm, karar yazılmadı | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: sonuç kayıtta yok (önce sonuç dosyası bulunmalı) |
| Ç54 | 2026-10-22 | hacim / tavan-taban | Tavan-taban olayı (≥4 tavan sonra ≥3 taban) — Tavan serisi sonrası taban serisi sonrası ne olur? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KARAR KAYITTA YOK | ölçüm 117 olay, karar yazılmadı | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: sonuç kayıtta yok (önce sonuç dosyası bulunmalı) |
| Ç55 | 2026-10-22 | fon izi / büyük alıcı / BofA | FON_IZI v1.0 fon hisselerinin yükseliş izi (iz B) — Tek yönlü fiyat izi evrende ayırır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | İZ DEĞİL | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç56 | 2026-10-23 | şekil / yapı | FON_IZI v1.1 sessiz yuvarlanma (Z0) + hacim — Küçük mum + ufak yukarı + kuru hacim | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | İZ DEĞİL | A (A: Ç175 "İZ DEĞİL'i hak eden gövde") | EVET | KAYITTA YOK | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç57 | 2026-10-23 | şekil / yapı | Z0 + hacim kuru (≤0,6) — Sessiz bölgede kuru hacim | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD, BIST; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | ABD 2,45 / BIST 0,97 | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç58 | 2026-10-23 | momentum / gösterge / makine / sinyal kütüphanesi | SESSIZ_ML (LightGBM alış/satış + öğretmen) — Makine öğrenmesi iz bulur mu? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD, BIST; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | LightGBM; BIST yok, ABD oynaklık | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç59 | 2026-10-23 | momentum / gösterge / makine / sinyal kütüphanesi | FON_IZI v1.2 62 gösterge / uyumsuzluk / Fibonacci — Göstergeler iz verir mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | yukarı hiçbiri 1,3 değil; 62 sinyalin olay dosyası saklanmadı | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç60 | 2026-10-23 | hacim / tavan-taban | A14 blok hacimli taban günü — Blok hacimli sert düşüş günü ek risk mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | eski 'ÇÜRÜDÜ' (eşli 0,91-1,73) | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel |
| Ç61 | 2026-10-23 | KAP olay | A15a borsa sorusu: olağan dışı fiyat (KAP 42) — Borsa bayrağı sonrası düşüş | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | eski 'ÇÜRÜDÜ' (eşli 1,14-1,17) | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç62 | 2026-10-23 | KAP olay | A15b VBTS / BISTECH tedbiri (KAP 14) — Tedbir sonrası düşüş | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | BIST; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | eski 'ÇÜRÜDÜ' (eşli 1,02-1,14) | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç63 | 2026-10-23 | cetvel / altyapı / denetim | Bağımsız denetim + v1.4 düzeltmeleri (Mart 2020 marjı) — Kod/veri hatası var mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | Veri hatası düzeltildi; kararlar değişmedi | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç64 | 2026-10-24 | fon izi / büyük alıcı / BofA | K9-K11 KAP fon portföy defteri — Fonlar hangi gün kaç lot aldı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | betimleyici: fonlar koşu fazında giriyor | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç65 | 2026-10-24 | fon izi / büyük alıcı / BofA | K10 fon girişi (rapor yayını sonrası) — 'Fon girdi' bilgisi sonrasını ayırır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | 0,80-1,07 | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç66 | 2026-10-24 | fon izi / büyük alıcı / BofA | K10 fon payı sermayenin %5'ini aştı — Yoğunlaşma sonrası | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | oynaklık | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KAYITTA YOK | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç67 | 2026-10-24 | şekil / yapı | K13 TEHOL tipi taban (Ders 3) — Cemal'in TEHOL bölgesinin ölçüsüyle arama | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | İZ DEĞİL | B + D (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi / D: "Kod TEHOL bölgesinin aynısını daha önce gördü" sözü fazlaydı: D13'ün eski kutuları bu bölgeye…) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç68 | 2026-10-24 | şekil / yapı | K14-K15 TEHOL tipi 6 devam denemesi (Ders 4) — Rüzgâr, 2/3 kat, kırılım, genişlik, oynaklık eşli | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | BIST; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | BIST'te aşağı risk düşük | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç69 | 2026-10-24 | şekil / yapı | TEHOL tipi taban → BIST'te aşağı risk düşük — Sakin dar tabandan sonra önce −%20 daha seyrek mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD, BIST; dönem kayıtta yok | kayıtta yok | ADAY | gözlem: BIST 0,45-0,68, ABD yok | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç70 | 2026-10-24 | hacim / tavan-taban | A11 oynaklık ölçekli (−3σ gün + hacim 3x + 20 günde −%20) — BIST'te güçlü A11 ABD'de aynı anlamla tutar mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | 'yeni deneme'; sonuç satırı yok (Ç175: ÖLÇÜLEMEDİ) | B + D (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi / D: Eski cetvelde "GEÇERLİ" A1-A4, A9, A13, B1: fark hissenin zaten düşmüş / yükselmiş / sakin olm…) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç71 | 2026-10-24 | sektör / makro | A9 OLGUN rüzgâr + sözleşme/teşvik (tek cetvel) — Puanlanmamış tek GEÇERLİ madde | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | Ç19 notundan (tek cetvel) | B + D (B*: kayıtta n yok, güç bilinmiyor / D: Eski cetvelde "GEÇERLİ" A1-A4, A9, A13, B1: fark hissenin zaten düşmüş / yükselmiş / sakin olm…) | EVET | KAYITTA YOK | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç72 | 2026-10-24 | şekil / yapı | D13 tespiti aşağı riski düşürür mü (koruma) — COL_TESPIT 'bozulma %2-9 vs %31-44' eşli tabanla tutar mı? | eski tek cetvel + eşli kutu (önce +%20 oranı ≥ 1,3 kat) | ABD; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | Denetim 24 Eki: ABD olayları artık puanlanıyor (adaptör düzeltildi). | A + D (A: Ç175 "İZ DEĞİL'i hak eden gövde" / D: Eski cetvelde "GEÇERLİ" A1-A4, A9, A13, B1: fark hissenin zaten düşmüş / yükselmiş / sakin olm…) | EVET | KAYITTA YOK | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç73 | 2026-10-24 | şekil / yapı | TEHOL tipi taban + DÜZGÜN DİP (K13b) — Cemal: 'Ekim 2024 dibi düzgün, 2021'inki değil' — dibi haftalarca test edilen taban sonrası yükseliş? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | Ç76 sonucu İZ DEĞİL | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç74 | 2026-10-24 | şekil / yapı | TEHOL tipi taban + düzgün dip → aşağı risk düşük mü — Düzgün dipli taban sonrası önce −%20 daha seyrek mi? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KARAR KAYITTA YOK | sonuç kayıtta yok | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: sonuç kayıtta yok (önce sonuç dosyası bulunmalı) |
| Ç75 | 2026-10-24 | şekil / yapı | Düzgün dip tek başına (çöküş sonrası taban, şekil şartı gevşek) — Düzgün dip, TEHOL'ün öteki ölçüleri olmadan da fark yaratır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD; dönem kayıtta yok | n 400 | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | Ç179 düzeltmesi: ABD ÖLÇÜLEMEDİ / TUTMADI | B + D (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi / D: kayıt notunda düzeltme / denetim bulgusu var) | EVET | HAYIR | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç76 | 2026-10-24 | şekil / yapı | Ç73 olayları, Cemal'in ölçüsü: 250 günde dip kırılmadan 2 kat (eşli kutu) — Düzgün dipli TEHOL tipi tabandan sonra büyük yükseliş daha sık mı? | eski tek cetvel + eşli kutu (önce +%20 oranı ≥ 1,3 kat) | ABD, BIST; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | Eşli kutu kıyası. SONUÇ İZ DEĞİL. Denetim sonrası (K13 pencere + eşli kutu geçmiş bilgi + fi_duzelt): 2 kat katı BIST 0,79 / 0,00 (n2) / 1,30 (n41), A | B + D (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi / D: Eşli kutu geleceğe göre seçiliyordu; "çok test edilen dip daha sık kırılıyor" gözlemi (1,00-1,…) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç77 | 2026-10-24 | şekil / yapı | Ç75 olayları, 250 günde dip kırılmadan 2 kat (eşli kutu) — Düzgün dip tek başına büyük yükselişi daha sık getirir mi? | eski tek cetvel + eşli kutu (önce +%20 oranı ≥ 1,3 kat) | ABD, BIST; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | Eşli kutu kıyası. SONUÇ İZ DEĞİL. Denetim sonrası 2 kat katı BIST 0,71 / 0,96 / 1,06, ABD 0,73 / 1,08 / 0,91; önce −%20 katı 0,75-1,31 (eskiden 1,00-1 | B + D (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi / D: Eşli kutu geleceğe göre seçiliyordu; "çok test edilen dip daha sık kırılıyor" gözlemi (1,00-1,…) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç78 | 2026-10-24 | şekil / yapı | İKİ YUVARLAMA: dipten sonra önce aşağı (∩), hemen ardından yukarı (∪) yuvarlama (K17 Y1) — Cemal (TEHOL 2021): '1'de aşağı yuvarlama, 2. bölge istenen; ikisi p… | eski tek cetvel + eşli kutu (önce +%20 oranı ≥ 1,3 kat) | ABD, BIST; dönem kayıtta yok | n 400 | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | Ç179 düzeltmesi: dip kümeleri PİYANGO | B + D (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi / D: kayıt notunda düzeltme / denetim bulgusu var) | EVET | HAYIR | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç79 | 2026-10-24 | şekil / yapı | İki yuvarlama + 2. bölgenin dibi düzgün (K17 Y2) — ∪ bölgesinin dibi haftalarca test edilmişse fark var mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | BIST; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | ayırıcı değil (BIST 735'in 688'i düzgün dipli) | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç80 | 2026-10-24 | şekil / yapı | İki yuvarlama + kutu tavanı kırılımı (K17 Y3) — İki yuvarlamalı kutunun tavanı kırılınca girmek fark yaratır mı? | eski tek cetvel + eşli kutu (önce +%20 oranı ≥ 1,3 kat) | ABD, BIST; 2023, 2024-26 | kayıtta yok | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | Eşli kutuya göre BIST 2023 1,46 (önce −%20 0,46), 2024-26 0,94, ABD 0,73-0,97 → İZ DEĞİL. | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: t'de bilinir sayısal tanım yok / eski cetvel (B) |
| Ç81 | 2026-10-24 | şekil / yapı | İki yuvarlama, sıkı yay (iki bölgede R2 >= 0,70; K17 Y4) — Gözle temiz yay olanlar ayrışır mı? (Ç78-Ç80 iz değil sonrası tur 2, eşik önceden) | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KARAR KAYITTA YOK | sonuç kayıtta yok (tur 2) | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: sonuç kayıtta yok (önce sonuç dosyası bulunmalı) |
| Ç82 | 2026-10-24 | şekil / yapı | İki yuvarlama + sektör rüzgârı (K17 Y5) — Rüzgârlı sektörde iki yuvarlama ayrışır mı? (tur 2) | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | BIST; 2023 | n 29 | KARAR KAYITTA YOK | önce −%20 BIST 0,51-0,71 ama tek cetvelde ters kat; karar yazılmadı | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: sonuç kayıtta yok (önce sonuç dosyası bulunmalı) |
| Ç83 | 2026-10-24 | şekil / yapı | İki yuvarlama, hafif silkeleme (-%5..-%15; K17 Y6) — Cemal'in 'iki kutu' girişi gibi sığ ikinci çukur ayrışır mı? (tur 2) | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KARAR KAYITTA YOK | sonuç kayıtta yok (tur 2) | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | KAYITTA YOK | HAYIR: sonuç kayıtta yok (önce sonuç dosyası bulunmalı) |
| Ç84 | 2026-10-24 | cetvel / altyapı / denetim | GERİYE DÖNÜK KOD DENETİMİ (6 bağımsız denetçi; ölçüm + üretim kodu) — Cemal: 'eski modeller sık hata yaptı; yanlışları bul, doğrula, düzelt, yeniden koştur' | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | 6 bağımsız denetçi, ~30 ölçüm hatası | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç85 | 2026-10-25 | Cemal'in göz kuralları / kör test | CEMAL'İN VAKA PROFİLİ: düşüş sonrası dar kutu, mum ve hacim düşüştekinden küçük, tavan kırılımı (K18 C1) — Cemal: 'TEHOL, BINBN, KTLEV, ESCAR, BORLS, VERUS, MA… | eski tek cetvel + eşli kutu (önce +%20 oranı ≥ 1,3 kat) | ABD, BIST; 2024-26 | kayıtta yok | İZ DEĞİL | profil ayırmıyor (7/9 koşan, 2/3 koşmayan profilde) | A + D (A: Ç175 "İZ DEĞİL'i hak eden gövde" / D: Hatırlanan vakalar koşanlardı (hafıza yanlılığı); koşmayan VSNMD / PAPIL'de de aynı profil (+1 satır)) | EVET | HAYIR | HAYIR: Cemal gözü; kasa fiyat bloğu değil, kör etiket gerekir |
| Ç86 | 2026-10-25 | Cemal'in göz kuralları / kör test | Cemal'in vaka profili, kutu >= 40 bar ('aylarca'; K18 C2) — Aylarca süren kutu ayrışır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | Yeni deneme | A (A: Ç175 "İZ DEĞİL'i hak eden gövde") | EVET | HAYIR | HAYIR: Cemal gözü; kasa fiyat bloğu değil, kör etiket gerekir |
| Ç87 | 2026-10-25 | Cemal'in göz kuralları / kör test | Cemal'in vaka profili, önce düşüş <= -%50 ('sert çöküş'; K18 C3) — Sert çöküş sonrası kutu ayrışır mı? | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KARAR KAYITTA YOK | sonuç kayıtta yok (Ç175: ÖLÇÜLEMEDİ) | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | HAYIR | HAYIR: sonuç kayıtta yok (önce sonuç dosyası bulunmalı) |
| Ç88 | 2026-10-25 | Cemal'in göz kuralları / kör test | Cemal'in vaka profili, dar kutu (bant <= %20; K18 C4) — TEHOL/BINBN/ESCAR/MANAS gibi dar çöl ayrışır mı? (Ç85-Ç87 iz değil sonrası tur 2, eşik önceden) | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | Yeni deneme | A (A: Ç175 "İZ DEĞİL'i hak eden gövde") | EVET | HAYIR | HAYIR: Cemal gözü; kasa fiyat bloğu değil, kör etiket gerekir |
| Ç89 | 2026-10-25 | Cemal'in göz kuralları / kör test | Cemal'in vaka profili + kutuda dev hacim barı (>= 10 kat; K18 C5) — Cemal'in EUHOL 24 Ara 2024 izi: çölün içindeki dev hacim barı ayrışır mı? (tur 2) | eski tek cetvel + eşli kutu (önce +%20 oranı ≥ 1,3 kat) | ABD, BIST; 2023, 2024-26 | n 25 | ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi) | BIST 2023 0,86 (n 25); oynak hisse | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | HAYIR | HAYIR: Cemal gözü; kasa fiyat bloğu değil, kör etiket gerekir |
| Ç90 | 2026-10-25 | Cemal'in göz kuralları / kör test | Cemal'in vaka profili + sektör rüzgârı (K18 C6) — Rüzgârlı sektörde profil ayrışır mı? (tur 2) | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | KARAR KAYITTA YOK | sonuç kayıtta yok (Ç175: ÖLÇÜLEMEDİ) | B (B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi) | EVET | HAYIR | HAYIR: sonuç kayıtta yok (önce sonuç dosyası bulunmalı) |
| Ç91 | 2026-10-25 | giriş-çıkış / portföy kuralı | SİSTEM vs RASTGELE: kırılımda gir + kutu dibi stop + trail, aynı çıkışla rastgele girişe göre (K19) — Cemal: 'kırılım + kutu dibi + trail rastgele hisseden / r… | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | 12 hücrenin hiçbiri eşli hisseden üstün değil | A + D (A: Ç175 "İZ DEĞİL'i hak eden gövde" / D: "Kazandıran kırılım + kutu dibi stop + trail" cümlesi hiç rastgeleye göre ölçülmemişti; fark ~…) | EVET | KISMEN | HAYIR: kapalı konu (COL_OZET: giriş / çıkış / filtre) |
| Ç92 | 2026-10-25 | şekil / yapı | SAĞ AYAK: çöl atılımından sonraki yükseliş (120 gün en yüksek, 250 gün 2 kat) vs aynı gün eşli hisse; nadir ç… — Cemal: 'çöl bitişi, sağ ayak rastgele hisseden… | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | hiçbir sinyal dört hücrede geçmedi | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KISMEN | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç93 | 2026-10-25 | şekil / yapı | SAĞ AYAK MUM MUM: çöl atılımından sonra her gün yüzde yol ve aynı gün BÜTÜN hisseler içindeki sıra; en sıkı ç… — Cemal: 'çölden çıkan hisse ile rastgele günde… | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | BIST; 2024-26 | n 30; 29 | İZ DEĞİL | sıra 0,45-0,53 | A (A: Ç175 "İZ DEĞİL'i hak eden gövde") | EVET | KISMEN | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç94 | 2026-10-25 | şekil / yapı | CEMAL'İN PENCERESİ + TAVANDA BEKLEYEN ALIŞ EMRİ: çölün son gününden 15 gün (atılım mumu dahil) ve atılım mumu… — Cemal: 'MANAS 18 Temmuz - 8 Ağustos 2025, çölü… | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | BIST; 2024-26 | kayıtta yok | İZ DEĞİL | fark atılım mumunda (sonradan bilinen) | B + D (B*: kayıtta n yok, güç bilinmiyor / D: Cemal'in penceresinde çöl önde (0,57-0,66) ama fark yalnız atılım mumunda = sonradan bilinen;…) | EVET | KISMEN | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç95 | 2026-10-25 | Cemal'in göz kuralları / kör test | BÖLGE PARMAK İZİ + BİREBİR BENZER BÖLGELER: MANAS 13 Haz-11 Tem ve 20 Eki-5 Kas 2025'in 16 ölçüsü, en yakın 1… — Cemal: 'işaretli bölgenin her özelliğini kayde… | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | göz izi değil (v4: ✓ %54, ✗ %57, havuz %60) | B + D (B*: kayıtta n yok, güç bilinmiyor / D: Kör set v2 küçük grafik (sayfada 6 kutu, Bollinger, 40 mum): Cemal mum yapısını göremedi; ilk…) | EVET | HAYIR | HAYIR: Cemal gözü; kasa fiyat bloğu değil, kör etiket gerekir |
| Ç96 | 2026-10-25 | şekil / yapı | İKİ EVRE KURALI: düşüş sonrası SMA20 altı (1. evre) → SMA20 üstünde 5 gün dizilme, en fazla 2 delen, BB sıkış… — Cemal: '1. evre kırmızı SMA altında, 2. evre k… | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD, BIST; 2016-22, 2023, 2024-26 | n 516; 967; 200 | İZ DEĞİL | tarif eşliden iyi değil (ABD); BIST n küçük hücreler Ç175'e göre ölçülemedi | A + D (A: Ç175 "İZ DEĞİL'i hak eden gövde" / D: kayıt notunda düzeltme / denetim bulgusu var) | EVET | KISMEN | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç97 | 2026-10-25 | fon izi / büyük alıcı / BofA | ÇÖL = BÜYÜK ALICININ İZİ Mİ: çölden sonra fon payı geliyor mu, fon girişinden önce çöl var mı; çölde fon var/… — Cemal: 'bir hisseyi fazla alıcı olunca o bölge… | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | BIST; 2023 | kayıtta yok | İZ DEĞİL | fon payı çölle ilişkili değil | B (B*: kayıtta n yok, güç bilinmiyor) | EVET | KISMEN | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç98 | 2026-10-26 | şekil / yapı | DÖRT ÇÖLÜN ORTAK PARMAK İZİ: MANAS x2, BINBN, KZBGY 04.02-11.03.2025; dördünde ortak ölçüler profil olarak BI… — Cemal: 'KZBGY 4 Şubat - 13 Mart bölgesinin par… | eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60) | ABD, BIST; 2023, 2024-26 | n 109; 309; 5 | İZ DEĞİL | profil 1,02 | B (B: kayıtta yazılı en büyük n 309 (< 1.000; kayıtta bütün hücre n'leri yok)) | EVET | KISMEN | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç99 | 2026-10-26 | içeriden / açığa satış | İÇERİDEN ALIM (KAP Pay Alım Satım Bildirimi) ve ÇÖLDE İÇERİDEN ALIM, YENİ ÖLÇÜTLE (K27) — Cemal: '1 + 3 ile başla, ölçütü değiştir' (yol önerisi: şekil yerine… | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; 2023, 2024-26, 2022-26 | n 201; 418; 12 / 30 | İZ DEĞİL | KAP net alım BIST −%4,5 / −%2,6 | B (B: kayıtta yazılı en büyük n 418 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç100 | 2026-10-27 | temel / bilanço | BİLANÇO SÜRPRİZİ (PEAD): bilanço tepkisi en üst / alt %20, çöl + iyi sürpriz, ABD analist sürprizi (K28) — Cemal: 'başla' (yol 2: bilanço sürprizi) | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; 2016-22, 2023, 2024-26 | n 19 | İZ DEĞİL | hiçbiri dört hücrede tutmadı | B (B: kayıtta yazılı en büyük n 19 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç101 | 2026-10-27 | temel / bilanço | RİSK SÜZGECİ: K24 çöl sinyallerinde kötü bilanço / A11 / A14 işaretli adaylar kaçınılmalı mı; temiz adaylar (… — Cemal: 'devam et' (öneri b + a: BIST'e özgü ri… | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; 2023, 2024-26 | n 15; 1 | İZ DEĞİL | Aday = K24 iki evre sinyalleri (BIST 2023 504 / 2024-26 902; ABD 643 / 1.818). İşaretli (riskli) pay BIST %18, ABD %35. Eşli fark 60 gün, BIST 2023 / | B (B: kayıtta yazılı en büyük n 15 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç102 | 2026-10-27 | içeriden / açığa satış | ABD İÇERİDEN ALIM (SEC Form 4 açık piyasa alımı) ve ÇÖLDE İÇERİDEN ALIM (K30) — Cemal: 'ABD verisi izin vereyim, devam edelim; BIST hep manipülasyon' | FI_OLCUT 60 gün eşli (dört şart) | ABD; 2016-22, 2023, 2024-26, 2022-26 | kayıtta yok | İZ DEĞİL | çölde alım ABD 2023 dört şart tuttu, 2024-26 tutmadı, örneklem dışı güçlenmedi | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç103 | 2026-10-27 | içeriden / açığa satış | ANALİST İZLERİ: içeriden satış, seyrelme, nakit tükenmesi, açığa satış (13F yerine FINRA) ve çöl adaylarına u… — Cemal: 'en başarılı analistlerin izlediği 4 ve… | FI_OLCUT 60 gün eşli (dört şart) | ABD; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | Veri: SEC Form 4 (10b5-1 planlı satışlar hariç), SEC finansal tablo veri setleri 2021-2026 (pay sayısı bilanço kaleminden; dei kalemi veri setinde yok | B + D (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: SEC finansal tablo veri setinde pay sayısı 'dei' kalemi yok; ilk kod yanlış kalem okuyordu (so…) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç104 | 2026-10-27 | giriş-çıkış / portföy kuralı | SADE PORTFÖY ÖLÇÜMÜ: çöl adayları 10 yuvalı portföyde, çıkış kuralıyla; piyasa ve rastgele girişle karşılaştı… — Cemal: 'a ile devam et, sade portföy ölçümü' | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; 2023, 2024-26 | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | düzen ölçümü (iz testi değil) | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç105 | 2026-10-27 | momentum / gösterge / makine / sinyal kütüphanesi | SIÇRAYAN HİSSE PROFİLİ: 60 günde ortancanın +%40 üstüne çıkanları önceden ayıran özellik (12 fiyat/hacim özel… — Cemal: 'piyango gibi sıçrayan hisseler neden a… | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; 2016-22, 2023, 2024-26 | kayıtta yok | İZ DEĞİL | sıçrayan hisse profili: asimetrik özellik yok | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç106 | 2026-10-27 | temel / bilanço | NAKİT TÜKENMESİ GRUBUNDA İYİ ÇIKANLARIN İZİ (ABD, K31 M3 içinde; 12 özellik + şirket verisi, AUC profili; K33… — Cemal: 'nakit tükenmesi araştırmasında bazılar… | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | ABD-ADAY GEÇERSİZ (hayatta kalma yanlılığı) | B + D (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: ABD-ADAY ilan edilecekti ama evren yalnız bugün işlem görenler; nakit tükenenlerin %26-52'si b…) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç107 | 2026-10-27 | temel / bilanço | BATANLAR DAHİL NAKİT TÜKENMESİ TESTİ: SEC'te o gün bildirim veren bütün şirketler, eski kod kapak sayfasından… — Cemal: 'batanlar da test edilsin; parmak izine… | FI_OLCUT 60 gün eşli (dört şart) | ABD; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | batanlar dahil; 2024-26 sıra 0,48 | B + D (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: Kırpılmamış ortalamada ters bölünme veri hatası +%4.800) | İNDİR | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç108 | 2026-10-28 | sektör / makro | RÜZGÂR BATANLARI AYIRIR MI: nakdi biten ABD şirketlerinde sektör rüzgârı (üretim D9b, SEC SIC sektörü) varken… — Cemal: 'nakdi yetmeyen şirketlerin arkasında r… | FI_OLCUT 60 gün eşli (dört şart) | ABD; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | AYIRMIYOR (iki kohort) | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç109 | 2026-10-28 | sektör / makro | PATLAYANLARIN ARKASINDA RÜZGÂR: 60 günde eşlerinin +%40 üstüne çıkan nakdi biten ABD hisselerinde girişte ve… — Cemal: 'patlayanların arkasında rüzgâr var mıyd… | FI_OLCUT 60 gün eşli (dört şart) | ABD; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | AYIRMIYOR | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç110 | 2026-10-28 | sektör / makro | RÜZGÂRIN SEBEBİ: sektörü kaldıran sebep (altın, petrol, bakır, çelik, buğday, USDTRY, ABD 10y faiz, TR CDS) f… — Cemal: 'rüzgâr fiyattan görülünce geç kalınır;… | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | sebep önce gelmiyor | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç111 | 2026-10-28 | sektör / makro | BÜYÜKLER ÖNCE, KÜÇÜKLER SONRA: sektörün büyükleri (işlem değeri üst üçte bir) 20 günde piyasayı +%10 geçmiş,… — Cemal: '2 ile başla; para akışı tek başına yetm… | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | 2.700 sektör sinyali (BIST 1.023, ABD 1.677), 11.609 küçük üye olayı. Eşli fark (BIST 2023 / 2024-26 / ABD 2023 / 2024-26): hepsi +%6,0 / +%1,8 / -%6, | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç112 | 2026-10-28 | hacim / tavan-taban | EN YAKIN ADAYLAR 3 PAZARDA (yeni karar pazarları ABD + AVRUPA, BIST bilgi): tavan günü kaçınması, geride kala… — Cemal: 'Amerika ve Avrupa tutan iz kabul edils… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; 2023, 2024-26 | n 8 / 24; 9 / 31 | İZ DEĞİL | blok taban ABD 2024-26 dört şart tutar, 2023 tutmaz | B + D (B: kayıtta yazılı en büyük n 31 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: Avrupa verisinde Londra peni / sterlin 100x geçişleri (5 hisse) ve DIA.MC; ilk koşudaki −… | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç113 | 2026-10-28 | şekil / yapı | ŞEKİLLER 3 PAZARDA: çöl (K24), ikili dip, ters omuz baş omuz, RSI / MACD boğa uyumsuzluğu, RSI ayı uyumsuzluğ… — Cemal: 'çöl, ikili dip, ters OBO, RSI MACD uyu… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; 2023, 2024-26 | n 71; 18; 7 | İZ DEĞİL | Eşli fark ABD 2023 / 2024-26, AVR 2023 / 2024-26, BIST 2023 / 2024-26: çöl K24 +%3,1 (aralık artı) / -%0,5, +%0,4 / +%0,5, -%1,4 / -%0,7; ikili dip (b | B (B: kayıtta yazılı en büyük n 71 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç114 | 2026-10-28 | sektör / makro | ABD ÖNCÜ, AVRUPA TAKİP: ABD kaba sektör sepeti piyasayı geçince Avrupa'daki (ve BIST'teki) aynı sektör üyeler… — Cemal: 'Amerika verileri öncü, Avrupa ve Asya… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | kayıtta yok | İZ DEĞİL | ABD -> AVR, ana çeşit (20 gün, %10, Avrupa henüz gelmedi; 203 sinyal): eşli fark 2016-22 -%0,3, 2023 0, 2024-26 +%1,0; Avrupa küçükleri +%1 / -%1 / -% | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç115 | 2026-10-28 | sektör / makro | SAAT FARKI: ABD güçlü günü / sektör günü / geç seansı -> Avrupa ertesi gün boşluk, ilk saat, gün içi, 5 gün (… — Cemal: 'Avrupa ile Amerika arasında gün değil… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR; 2016-22, 2023, 2024-26 | kayıtta yok | İZ DEĞİL | boşluk +%0,23 üç dönemde aralık artı; gün içi yalnız 2023 | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç116 | 2026-10-28 | momentum / gösterge / makine / sinyal kütüphanesi | KLASİK GÖSTERGELER 3 PAZARDA: Bollinger alt bant dönüşü / üst bant, RSI 30 / 70, MACD kesişimi, altın / ölüm… — Cemal: 'eski adamların icat ettiği formasyonlar… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | sekizi de; ABD Fibonacci ortalama artı, sıra 0,52 / 0,50 | A (A: on binlerce olay) | EVET | EVET | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç117 | 2026-10-28 | sektör / makro | RÜZGÂR SÜREKLİLİĞİ: sektör rüzgârı başladığı gün üyeleri almak (eşli fark + ham fark) ve çöl + rüzgâr (K41-B) — Cemal: 'd seçeneğini yap (rüzgâr göründükten so… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; dönem kayıtta yok | n 3 / 35. | İZ DEĞİL | Rüzgâr başlangıcında üyeler, HAM fark (pazar medyanına göre r60): ABD +%1,2 / +%5,7, BIST +%11,8 / +%8,3, AVR -%3,8 / +%0,9; EŞLİ fark (aynı momentum | B (B: kayıtta yazılı en büyük n 35 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç118 | 2026-10-28 | temel / bilanço | ABD ÇÖL ADAYI OLAY SÜZGECİ: K24 çöl sinyalleri + son 60 günde iyi bilanço (K28) / son 90 günde içeriden alım… — Cemal: 'e seçeneğini yap' | FI_OLCUT 60 gün eşli (dört şart) | ABD; 2023, 2024-26 | n 52 / 170; 19 / 71 | İZ DEĞİL | 6.912 çöl sinyali; iyi bilanço 253, içeriden alım 710, temiz temel 1.821. Eşli fark ABD 2023 / 2024-26: hepsi +%3,1 / -%0,5; iyi bilanço +%7,7 / -%0,4 | B (B: kayıtta yazılı en büyük n 170 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç119 | 2026-10-28 | sektör / makro | K40 SEKTÖR 5 GÜN KALINTISI DIŞ ÖRNEK + MALİYET: hücreler 2016-19 / 2020-22 / 2023 / 2024-26, BIST hedef bilgi… — Cemal: 'kalıntıyı dış örnekle ayrıca ölç' | FI_OLCUT 60 gün eşli (dört şart) | AVR, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | AVR kalıntı dört hücrenin ikisi; sağlam değil, bilgi | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç120 | 2026-10-28 | cetvel / altyapı / denetim | ÖLÇÜM HATTI KONTROLÜ: geleceğe bakan sinyal (pozitif), yarı pozitif ve rastgele sinyal (negatif, 20 tohum) üç… — Cemal: 'ya sen hata yapıyorsun, görmüyorsun' | FI_OLCUT 60 gün eşli (dört şart) | AVR; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | ölçüm hattı kontrolü | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç121 | 2026-10-28 | cetvel / altyapı / denetim | BİLİNEN ETKİLER KIYASI: momentum 12-1, 1 ay tersine dönüş, küçüklük; ham cetvel (pazar medyanına göre) ve eşl… — Cemal: 'hiçbir yerde iz yok, o zaman kesin sen… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | bilinen etkiler kıyası | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç122 | 2026-10-28 | momentum / gösterge / makine / sinyal kütüphanesi | ALINABİLİR İZ KARNESİ: 23 sinyal (trend 7, dip 9, öteki 7; çöl yalnız biri) x 3 pazar x 3 dönem; ham fark (eş… — Cemal: 'çölü boş ver; bir iz var mı, alım satı… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | kayıtta yok | İZ DEĞİL | alınabilir iz yok; küçüklük ADAY (hayatta kalma) | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç123 | 2026-10-28 | şekil / yapı | INTEM BÖLGESİNİN PARMAK İZİ: 28 Eyl - 9 Eki 2026 sıkışması (düşüş sonrası 195-200), 8 ölçü, iki pencere (20 /… — Cemal: 'bu bölgenin parmak izini çıkart; bu bö… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 8; 13 | İZ DEĞİL | INTEM izi; piyasayı geçmiyor | B (B: kayıtta yazılı en büyük n 13 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç124 | 2026-10-28 | şekil / yapı | KISA UFUK, KUTU ÇIKIŞI: INTEM'e birebir eşleşen bölgelerden sonra ilk +-%5 / 8 / 12 hangisi önce (20 gün), ku… — Cemal: '60 gün bakarsan orası küçük bir durak;… | diğer: +%8 önce kısa ufuk (20 gün, oynaklık eşli) / makine (h5 akrabası) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 240; 26; 51 | EMARE | sıkışma ailesindeki tek EMARE; ileri testte ÖLÇÜLEMEDİ (Ç180) | C + B + D (C: '+%8 önce' hedef-önce cetveli (Ç124: ilk koşuda oynaklık karışımı; Ç203 h5 kusuruyla akraba) / D: İlk koşu düz rastgele tabanla +20 puan gösterdi ama −%8'e ulaşma da +8 puan yüksekti (oynak bö…) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç125 | 2026-10-28 | momentum / gösterge / makine / sinyal kütüphanesi | DÖNÜŞ NOKTASINI MAKİNEYE ÖĞRETME: 1,09 milyon hisse-günü (ABD + AVR + BIST, her 5. gün, 2016-26), 36 özellik,… — Cemal: 'tipik dönüş noktasını bul; sen ara, ma… | diğer: +%8 önce kısa ufuk (20 gün, oynaklık eşli) / makine (h5 akrabası) | ABD, AVR, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | ABD 2023 +3,6 eşiğin altında | C (C: '+%8 önce' hedef-önce cetveli (Ç124: ilk koşuda oynaklık karışımı; Ç203 h5 kusuruyla akraba)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç126 | 2026-10-28 | şekil / yapı | ECOGR HAFTALIK YUKARI YUVARLANMA + BBIO DÜŞÜŞ -> İKİ DİP -> YUVARLANMA: parmak izi eşleşmeleri (haftalık ve g… — Cemal: 'birinci slayt haftalık yukarı yuvarlan… | diğer: +%8 önce kısa ufuk (20 gün, oynaklık eşli) / makine (h5 akrabası) | ABD, AVR, BIST; 2023, 2024-26 | n 12; 9; 27 | İZ DEĞİL | A) ECOGR haftalık (13 hafta, 9 kendi-içi ölçü; eşleşme ABD 154, AVR 122, BIST 59; band 0,20): eşli fark ABD -%1 / +%7 (n 12) / -%7, AVR 0 / 0 / -%1, B | C (C: '+%8 önce' hedef-önce cetveli (Ç124: ilk koşuda oynaklık karışımı; Ç203 h5 kusuruyla akraba)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç127 | 2026-10-28 | momentum / gösterge / makine / sinyal kütüphanesi | SERT DÜŞÜŞ SONRASI MAKİNE: K46 makinesi yalnız son 40 gün tepesinden >= %20 düşmüş hisse-günlerinde (135 bin… — Cemal: 'burada makine çalıştır; belki ben yanlı… | diğer: +%8 önce kısa ufuk (20 gün, oynaklık eşli) / makine (h5 akrabası) | ABD, AVR, BIST; 2023, 2024-26 | n 59 | İZ DEĞİL | AUC 0,50-0,60 (K46'nın 0,6-0,7'sinden zayıf; alt küme zaten 'düşmüş' olduğundan ayrım azalıyor); karışık etiket 0,508. ÜST %5 vs oynaklık eşli rastgel | C (C: '+%8 önce' hedef-önce cetveli (Ç124: ilk koşuda oynaklık karışımı; Ç203 h5 kusuruyla akraba)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç128 | 2026-10-28 | momentum / gösterge / makine / sinyal kütüphanesi | GENİŞ PARMAK İZİ MAKİNESİ: TradingView örneğindeki üç aile (mum fiziği, trend / konum, kesişim) çok pencereli… — Cemal: 'makineye çok metrik yüklesem belki bir… | diğer: +%8 önce kısa ufuk (20 gün, oynaklık eşli) / makine (h5 akrabası) | ABD, AVR, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | ABD 2023 +6,9 (eşik 10) altında; AVR +10,8 / +11,3 | C + D (C: '+%8 önce' hedef-önce cetveli (Ç124: ilk koşuda oynaklık karışımı; Ç203 h5 kusuruyla akraba) / D: Örnek Pine kodundaki `gap = ta.pvt` hatalıydı (PVT hacim göstergesi)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç129 | 2026-10-28 | momentum / gösterge / makine / sinyal kütüphanesi | GENİŞ MAKİNE SERT DÜŞÜŞ SONRASI: K48'in 204 ölçüsü, yalnız dd40 <= -%20 satırları (135 bin) (K48-B) — Cemal: 'sert düşüşten sonra olan bir şey' (K46-B'nin geni… | diğer: +%8 önce kısa ufuk (20 gün, oynaklık eşli) / makine (h5 akrabası) | ABD, AVR, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | AVR +1,7 / +0,6 | C (C: '+%8 önce' hedef-önce cetveli (Ç124: ilk koşuda oynaklık karışımı; Ç203 h5 kusuruyla akraba)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç130 | 2026-10-28 | momentum / gösterge / makine / sinyal kütüphanesi | KABUK DIŞI DERLEME: her ölçü iki yönde (normal / ters, olayda açığa satış), pazar pazar, bütün birleşimi; ban… — Cemal: 'kural bizi sınırlıyor olabilir, kabuğu… | diğer: +%8 önce kısa ufuk (20 gün, oynaklık eşli) / makine (h5 akrabası) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 9; 31 | İZ DEĞİL | pazar izi üç pazarda 0 | C (C: '+%8 önce' hedef-önce cetveli (Ç124: ilk koşuda oynaklık karışımı; Ç203 h5 kusuruyla akraba)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç131 | 2026-10-28 | momentum / gösterge / makine / sinyal kütüphanesi | MAKİNE SİNYALİYLE GERÇEKÇİ PORTFÖY: K48 / K48-B üst %5 sinyalleri, 10 yuva, günde en çok 2 yeni giriş, +%8 he… — K49 'iz yok çıkarsa durma' sıradaki deneme; Ce… | diğer: +%8 önce kısa ufuk (20 gün, oynaklık eşli) / makine (h5 akrabası) | ABD, AVR, BIST; 2023, 2024-26 | kayıtta yok | İZ DEĞİL | üç pazarda portföy piyasanın altı | C (C: '+%8 önce' hedef-önce cetveli (Ç124: ilk koşuda oynaklık karışımı; Ç203 h5 kusuruyla akraba)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç132 | 2026-10-29 | şekil / yapı | ABD ÇÖL YOLU, AKADEMİK YÖNTEMLERLE: sert düşüş -> küçük mumlu sıkışma (P1 oluşurken) -> kırılım (P2); batanla… — Cemal'in iki araştırma görevi (29 Eki): 'forma… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | ABD, AVR, BIST; 2023, 2024-26 | n 906 / 1.316 | İZ DEĞİL | P1 +2,5 / +2,4 puan (eşik 5) | A + D (A: Ç175 "İZ DEĞİL'i hak eden gövde" / D: Küçük artı etkinin tamamı bugün işlem görenlerden (+5,3 / +6,4); batanlarda eksi; 'rüzgâr yok'…) | EVET | EVET | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç133 | 2026-10-29 | şekil / yapı | KIRILIM DEVAMLILIĞI GİRİŞİ: P2 kırılımından sonra 10 gün kapanışlar kutu tavanı üstünde kalırsa 11. gün al (K… — K51 'iz yok çıkarsa durma' sıradaki deneme | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 210; 138 | İZ DEĞİL | İZ DEĞİL. ABD 2016-22 -7,5 puan (n 210), Avrupa 2016-26 +4,6 [-1,6] (n 138); esin dönemi ABD 2023 +2,2, 2024-26 -0,8; BIST 0. Ders: 'süren kırılım' gr | B + D (B: kayıtta yazılı en büyük n 210 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: "Süren kırılım" grubunun iyi görünmesi tamamen sonradan bilinen bilgiydi (10 gün kutu üs… | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç134 | 2026-10-29 | cetvel / altyapı / denetim | K51 SONRASI BAĞIMSIZ DENETİM (v1.2): veri bütünlüğü (sayı uzlaşması, point-in-time evren, çıkış sınıflaması,… — Cemal'in 'K51 sonrası bağımsız araştırma planı'… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | kayıtta yok; 2016-22, 2023, 2024-26 | n 2.300 / 1.104 / 2.536; 35; 28 | İZ DEĞİL | beş hipotezin beşi desteklenmiyor | A + D (A: Ç175 "İZ DEĞİL'i hak eden gövde" / D: Tiingo 'batan' 422 sembolün yalnız 51'i batma benzeri; 171 satın alma; 153 kod yeniden kullanı…) | EVET | EVET | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç135 | 2026-10-29 | temel / bilanço | K52 GRAFİK İZİ + ANALİST REVİZYONLARI (v1.3): Yahoo analist not günlüğü ile K51 izlerine (P1, P2) olay öncesi… — Cemal'in 'K51 — grafik izi + analist revizyonl… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | ABD; 2016-22 | n 178 / 122 / 197; 30 | İZ DEĞİL | analist revizyonu ek bilgi katmıyor | B + D (B: kayıtta yazılı en büyük n 197 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: G1 (teyit alan iz) ile G2a dengesiz: G1'in son 60 gün getirisi +8 vs +0,6; teyit zaten y… | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç136 | 2026-10-29 | temel / bilanço | K53 BİLGİ DİRENCİ (v1.4): ilk olumlu analist revizyonundan sonraki 5 günde fiyat zayıf + satış baskısı azalıy… — Cemal'in K53 mesajı (29 Eki; ADE / KGS tanımla… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | kayıtta yok; 2016-22, 2024-26 | n 184 | İZ DEĞİL | T1 / T5 / T6 hiçbiri desteklenmiyor | B + D (B: kayıtta yazılı en büyük n 184 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: ADE / KGS tanımları Cemal'in mesajı kesik geldiği için Claude tarafından sabitlendi; Cem… | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç137 | 2026-10-30 | evren / mekanizma / veri | K54 TARİHSEL HİSSE EVRENİ SAĞLAMLIK DENETİMİ (v1.5): 3.267 sembol SEC başvuru geçmişi (8-K 1.03 / 2.01, 25-NS… — Cemal'in K54 görevi (30 Eki) | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | ABD; 2023, 2024-26 | n 0 | ALTYAPI / DENETİM (hipotez değil) | evren sağlamlık denetimi | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç138 | 2026-10-30 | evren / mekanizma / veri | K55 DALLANMALI İZ ARAMA — FAZ 0 (tam evren) + FAZ 1 (63 OHLCV hücresi, yalnız KEŞİF 2016-21) + vekil kıyası:… — Cemal'in K55 planı (30 Eki) ve 'Tam evren Faz 0… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | kayıtta yok; 2024-26 | kayıtta yok | İZ DEĞİL | K55 keşif taraması (iz yok) | B + D (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: 25 KEŞİF'in 19-20'si ters yönlü: olay başlangıcı seçim etkisi (t0 = +%30'u ilk yakalayan gün);…) | EVET | EVET | HAYIR: kripto kapandı / mekanizma işi |
| Ç139 | 2026-10-30 | evren / mekanizma / veri | K56 K51-K55 ETKİ VE MEKANİZMA ARAŞTIRMASI — FAZ 0: bütün K51-K55 bulgularının envanteri, mekanizma hipotezler… — Cemal'in 'K51-K55 Etki ve Mekanizma Araştırmas… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | kayıtta yok; 2023 | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | mekanizma envanteri | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç140 | 2026-10-31 | evren / mekanizma / veri | K56-F1A FAZ 1 YEREL (KEŞİF 2016-21, keşif verisi yeniden kullanımı): K55'in KEŞİF'i sağlayan 125 (hücre, vary… — Cemal'in Faz 1 kararları (31 Eki): ilk üç anal… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | gerçek etki 0 / 125 | B + D (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: 25 KEŞİF'in 19-20'si ters yönlü: olay başlangıcı seçim etkisi (t0 = +%30'u ilk yakalayan gün);… (+1 satır)) | EVET | EVET | HAYIR: kripto kapandı / mekanizma işi |
| Ç141 | 2026-10-31 | evren / mekanizma / veri | K56-IC İÇ DOĞRULAMA 2022-23: yalnız önceden belirlenmiş 125 satır / 64 varyant; B1 K55 A (ilk geçiş), B2 seçi… — Cemal'in Faz 1 kararları (31 Eki): İÇ açılabil… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | ABD; 2024-26 | kayıtta yok | İZ DEĞİL | gerçek etki 0 / 125 | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR: kripto kapandı / mekanizma işi |
| Ç142 | 2026-10-31 | evren / mekanizma / veri | K56-EVREN2 BATAN ŞİRKETLERLE EVREN v2 (aday ve hazırlık): Ö1 K34 eşleme kuralı (212), Ö2 Tiingo listesinden K… — Cemal'in Faz 1 kararları (31 Eki): Tiingo Kası… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | evren v2 hazırlığı | - | İNDİR | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç143 | 2026-10-31 | evren / mekanizma / veri | K56-AYR (iii) RASTGELE GÜN / BÜTÜN GÜNLER AYRIŞMASI (KEŞİF + İÇ, yapay veri denetimiyle): 125 satırda olay ağ… — Cemal'in BAĞIMSIZ kararı (31 Eki) madde 4 | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | KEŞİF: 107 / 125 satır mekanik (AĞIRLIK ETKİSİ + MEKANİK 99, MEKANİK 8), BELİRSİZ (yapay) 8, AYRIŞMA YOK 5, AĞIRLIK ETKİSİ (gerçek veriye özgü) 3, AÇI | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç144 | 2026-10-31 | evren / mekanizma / veri | K56-PBO PBO / DEFLATED SHARPE (K55 ön kaydı §7; KEŞİF + İÇ, donem60): 64 KEŞİF yapısı, K55 B seçiminin eşleşm… — K55 ön kaydı §7 + Cemal'in BAĞIMSIZ kararı (31… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | PBO / DSR | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç145 | 2026-10-31 | evren / mekanizma / veri | K56-SIZ İÇ → BAĞIMSIZ DOLAYLI ERİŞİM SINAMASI: T0 K55 panel / olay tablosunun baştan yeniden üretimi; T1 aynı… — Cemal'in BAĞIMSIZ kararı (31 Eki) madde 2: 'İç… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | kayıtta yok; 2023 | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | KARAR: İÇ hesaplarında 2023-12-31 sonrası bilgiye dolaylı erişim YOK. T0 panel 4.909.423 satır ve 22.502 olay birebir. T1b S (125) / H (25) / B3 (64) | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç146 | 2026-11-01 | evren / mekanizma / veri | K56-BAG BAĞIMSIZ DOĞRULAMA 2024-26 (TEK AÇILIŞ, K55_125_B) + K55 NİHAİ KARAR: yalnız ön kayıtlı 125 satır / 6… — Cemal'in BAĞIMSIZ kararı (31 Eki), madde 1-5 v… | diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma) | kayıtta yok; 2024-26 | kayıtta yok | İZ DEĞİL | K55 NİHAİ: İZ YOK | B (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez) | EVET | EVET | HAYIR: kripto kapandı / mekanizma işi |
| Ç147 | 2026-11-08 | kripto | KRİPTO YENİ TOKEN +%100 GÜNÜ: önceden tespit ve sonrası (RITUAL/USDT vakası); 759 yeni token (2024-01 .. 2026… — Cemal (8 Kas 2026): 'Bu gibi yükseliş nasıl te… | diğer: kripto olay ölçüsü (eşli taban yok) | ABD, BIST, kripto; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | İZ DEĞİL. Liste günü kapanışından medyan: 7 g -%14, 30 g -%30, 90 g -%53, 180 g -%68. +%100 günü (406 olay) ertesi açılıştan medyan: +1 g -%16, +7 g - | B + D (B*: kayıtta n yok, güç bilinmiyor / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: OKX / Gate'te delist edilenler yok (hayatta kalma yanlılığı); Binance ana API 451 ve Bybit 403…) | İNDİR | EVET | HAYIR: kripto kapandı / mekanizma işi |
| Ç148 | 2026-11-09 | temel / bilanço | YEOTK PROFİLİ ('SIKI DOSYA') ÖN KAYITLI GEÇMİŞ TESTİ: bilanço günü güçlü tepki (F7, kayan üst %20 + ham >= +%… — Cemal (9 Kas 2026, tek ve son talimat): YEOTK… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; 2023, 2024-26 | n 1; 20; 2 | İZ DEĞİL | YEOTK profili V1-V3 | B + D (B: kayıtta yazılı en büyük n 96 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: K57 tam profil n 2-5; V_ABD'de ABD 2024-26 +%10,3 (n 31) geniş evrende +%4,8'e indi (örne… | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç149 | 2026-11-09 | temel / bilanço | K57-B: YEOTK profili V1 (güçlü tepki + büyüme + ivme + sağlam bilanço, fiyat şartı yok) çevresinde önceden ya… — K57 eşiğe en yakın V1 geniş evrende / kısa ufu… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; 2023, 2024-26 | n 64; 16; 58 | İZ DEĞİL | İZ DEĞİL. B1 geniş ABD evreni [İZ DEĞİL]: ABD 2021-22: n 64, +%3,9 (-%1,7 .. +%8,5), sıra 0,56, portföy %83,0, tutmaz; ABD 2023: n 16, +%11,4 (-%5,0 . | B + D (B: kayıtta yazılı en büyük n 99 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: K57 tam profil n 2-5; V_ABD'de ABD 2024-26 +%10,3 (n 31) geniş evrende +%4,8'e indi (örne… | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç150 | 2026-11-09 | temel / bilanço | K57-C: YEOTK profili V1 geniş ABD evreninde önceden yazılı son 3 deneme: C1 V1 + F4 (seyrelme yok), C2 likidi… — K57-B önceden yazılı C1-C3 iki ABD karar hücre… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; 2023, 2024-26 | n 26; 10; 41 | İZ DEĞİL | İZ DEĞİL. C1 V1 + F4 (seyrelme yok) [İZ DEĞİL]: ABD 2021-22: n 26, +%4,4 (-%8,5 .. +%9,7), sıra 0,59, portföy %92,5, tutmaz; ABD 2023: n 10, +%5,9 (-% | B + D (B: kayıtta yazılı en büyük n 64 (< 1.000; kayıtta bütün hücre n'leri yok) / K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez / D: K57 tam profil n 2-5; V_ABD'de ABD 2024-26 +%10,3 (n 31) geniş evrende +%4,8'e indi (örne… | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç151 | 2026-11-10 | cetvel / altyapı / denetim | K58 CETVEL SAĞLAMASI: FI_OLCUT gücü (plasebo olay + bilinen δ), French faktörleri pozitif kontrol, portföy ce… — İz bulamamamızın nedeni piyasa mı, ölçüm aleti… | FI_OLCUT güç + portföy cetveli kalibrasyonu | ABD, BIST; dönem kayıtta yok | n 30/100/300/1000/3000 | ALTYAPI / DENETİM (hipotez değil) | K58 cetvel sağlaması | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç152 | 2026-11-11 | momentum / gösterge / makine / sinyal kütüphanesi | K59 BASİT SİNYALLER: dokuz sürekli sinyal + önceden yazılı COMP4 bileşiği + DOSYA ailesi (YEOTK / DGXX mantığ… — Basit, nedeni bilinen sürekli sinyaller ve sır… | portföy cetveli v2 + olasılık tablosu (12 ay +%100 / −%50 katı; K59 / K60) | ABD, BIST; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | K59 TUTMAZ | A (A: cetvel v2 GÜVENİLİR) | EVET | EVET | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç153 | 2026-11-11 | momentum / gösterge / makine / sinyal kütüphanesi | K59-B: K59 §6daki önceden yazılı üç deneme: (a) yalnız küçük-orta hisseler, (b) 3 ay tutma + örtüşen üç kohor… — K59da tutmayan bileşik küçük-orta hisselerde y… | portföy cetveli v2 + olasılık tablosu (12 ay +%100 / −%50 katı; K59 / K60) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | TUTMAZ; (b) cetvel GÜVENİLMEZ | A + D (A: cetvel (a) GÜVENİLİR, (b) GÜVENİLMEZ / D: 3 ay tutma + örtüşen kohort cetveli (b) plaseboda GÜVENİLMEZ çıktı -> HÜKÜM YOK) | EVET | EVET | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç154 | 2026-11-11 | momentum / gösterge / makine / sinyal kütüphanesi | K60: sinyal kütüphanesi (77 sinyal + 12 bileşik, 13 aile) x iki cetvel (R1 portföy cetveli v2; R2 OLASILIK TA… — Hangi ölçülebilir özellik bir hissenin 12 ayda… | portföy cetveli v2 + olasılık tablosu (12 ay +%100 / −%50 katı; K59 / K60) | ABD; 2024-26 | kayıtta yok | İZ DEĞİL | K60: iz adayı yok; asimetrik fırsat yok; güvenli uç COMP4 / DOSYA_Y (bilgi) | A + D (A: cetvel v2 GÜVENİLİR (yalnız yaşayanlar) / D: R2 olasılık tablosunda 106 seçilen hipotez OYNAKLIK etkisi (iki kuyruk birlikte şişer, ln katl…) | EVET | EVET | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç155 | 2026-11-11 | momentum / gösterge / makine / sinyal kütüphanesi | K60-B: piyango havuzu (her ay 60 günlük oynaklığı en yüksek %20) İÇİNDE koşullu ayrım; 77 sinyal + 12 bileşik… — Oynak hisseler arasında hangi özellik ikiye ka… | portföy cetveli v2 + olasılık tablosu (12 ay +%100 / −%50 katı; K59 / K60) | ABD; dönem kayıtta yok | kayıtta yok | EMARE | BİLGİ düzeyi: 2 koşullu fırsat (BETA_BAB ALT, NDF_BS ALT) + 8 koruma; yalnız ABD, yalnız yaşayanlar | A + D (A: cetvel v2 (yalnız yaşayanlar) / D: NDF_BS 'fırsat' etiketi yön değil KAPSAM etkisi (kalemi bildiren hisse %35-39); TAX_CHG KEŞİF'…) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç156 | 2026-11-12 | temel / bilanço | K64 + K65: çöl sinyaline (K24, değişmeden) EK BİLGİ: 52 hafta zirvesi ailesi (Z52 zirveye uzaklık, D52 dipten… — Cemal: 'aynı fiyat şekillerini ölçmek yerine ç… | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; 2023, 2022-26, 2017-21 | n 300 | İZ DEĞİL | 22 değişken-yönün hepsi | A (A: Ç175 "İZ DEĞİL'i hak eden gövde") | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç157 | 2026-11-12 | evren / mekanizma / veri | K63: veri erişim araştırması: analist revizyonu, emir akışı, hisse ödünç verme (BIST ve ABD) — Cemal: analist revizyonları, emir akışı (OFI) ve ödünç ücreti iç… | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; dönem kayıtta yok | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | veri erişim araştırması | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç158 | 2026-11-12 | temel / bilanço | K62: BIST PEAD birebir tekrar (Ahlatcıoğlu & Okay 2021, Borsa Istanbul Review 21(1); doi 10.1016/j.bir.2020.0… — Cemal: 'BIST PEAD makalesini birebir yeniden ü… | FI_OLCUT 60 gün eşli (dört şart) | BIST; 2023, 2024-26, 2022-26, 2017-21 | kayıtta yok | İZ DEĞİL | makale yeniden üretildi; alınabilir bacak tutmadı | A (A: 5.430 olay, makale yeniden üretildi) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç159 | 2026-11-12 | içeriden / açığa satış | K66: ABD açığa satış talebi (FINRA iki haftalık açık pozisyon, 2017-12+) çöl sinyaline ek bilgi: SI_PAY (açık… — Cemal: 'hisse ödünç verme ve açığa satış taleb… | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; 2023, 2022-26 | kayıtta yok | İZ DEĞİL | 8 değişken-yön | A (A: cetvel v2 (çöl içi n kayıtta yok)) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç160 | 2026-11-12 | temel / bilanço | K62-B: bilanço sürprizi (çöl günü bilinen son açıklamanın SUETF ve EAR'ı, en çok 90 gün önce) çöl sinyaline e… — Cemal: 'çöl sonrası getiriyi açıklayan dış bil… | FI_OLCUT 60 gün eşli (dört şart) | ABD, BIST; 2023, 2022-26, 2017-21 | kayıtta yok | İZ DEĞİL | 4 değişken-yön | A (A: cetvel v2 (çöl içi n kayıtta yok)) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç161 | 2026-11-12 | temel / bilanço | K67: bilanço sonrası analist revizyonları (Yahoo not günlüğü: hedef fiyat ve tavsiye değişimleri, 2011-12+, 2… — Cemal: 'bilanço sonrası analist EPS ve hedef f… | FI_OLCUT 60 gün eşli (dört şart) | ABD, AVR, BIST; 2022-26, 2017-21 | kayıtta yok | İZ DEĞİL | 16 değişken-yön | A (A: 35.698 olay) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç162 | 2026-11-12 | sıkışma / oynaklık | VDYT (Volatilite Denge ve Yön Tahmini; ayrı motor, Çöl Yolu değişmedi): 5 sıkışma tanımı (ATR oranı, RV yüzde… — Cemal: 'uzun sıkışma ne zaman ve hangi yöne bi… | diğer: VDYT (Brier skill, büyük hareket olasılığı) | ABD, BIST; 2024-26 | kayıtta yok | İZ DEĞİL (ABD; BIST ÖLÇÜLEMEDİ) | Ç175: ABD İZ DEĞİL, BIST ÖLÇÜLEMEDİ | B + D (B*: kayıtta n yok, güç bilinmiyor / D: Motor 1 'basitten iyi' ama sıkışmaya özgü değil: rastgele bölgelerde aynı skill; kaynak bilanç… (+2 satır)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç163 | 2026-11-12 | sıkışma / oynaklık | VDYT2 (v2_20261112; Cemal'in tek ve değişmez hedefi): küçük mum sessiz bölgesi G5 = küçük mum + dar bant + (y… — Cemal: 'sessiz bölgeyi büyük hareketten önce b… | diğer: VDYT (Brier skill, büyük hareket olasılığı) | ABD, BIST; 2024-26 | kayıtta yok | İZ DEĞİL (ABD; BIST ÖLÇÜLEMEDİ) | Ç175: 'bölgeyi bulmak başarılı' tanımsal; ABD İZ DEĞİL, BIST ÖLÇÜLEMEDİ | B + D (B*: kayıtta n yok, güç bilinmiyor / D: "Bölgeyi bulmak BAŞARILI" ilanı tanımsaldı: büyük mum bölgenin kendi küçük mumlarına göre ölçü… (+3 satır)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç164 | 2026-11-12 | sıkışma / oynaklık | VDYT2-B test A: VDYT2 başarı (1) için MUTLAK HAREKET sağlaması (bölgeden bağımsız etiket): MA1 (ANA) = 20 gün… — Cemal: 'ikisini de yap; önce ön kayıt ve ölçüt… | diğer: VDYT (Brier skill, büyük hareket olasılığı) | ABD, BIST; dönem kayıtta yok | kayıtta yok | İZ DEĞİL (ABD; BIST ÖLÇÜLEMEDİ) | mutlak harekette başarısız; BIST olay 6 / 12 ÖLÇÜLEMEDİ | B + D (B*: kayıtta n yok, güç bilinmiyor / D: "Bölgeyi bulmak BAŞARILI" ilanı tanımsaldı: büyük mum bölgenin kendi küçük mumlarına göre ölçü… (+3 satır)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç165 | 2026-11-12 | cetvel / altyapı / denetim | VDYT2-B test B (batanlar dahil, Tiingo): doğrulama pilotu 12 bilinen başarısız sembol; ardından 450 sembollük… — Cemal: 'Tiingo'nun batanları eksiksiz verdiğin… | diğer: VDYT (Brier skill, büyük hareket olasılığı) | kayıtta yok; 2023 | kayıtta yok | ALTYAPI / DENETİM (hipotez değil) | Tiingo batan doğrulama pilotu (7 / 12 KISMEN) | - | İNDİR | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç166 | 2026-11-13 | Cemal'in göz kuralları / kör test | VDYT2 G5 sessiz bölge dedektörü insan gözü kör testi (40 grafik: 16 G5, 16 kontrol, 8 batan) + Tiingo batan O… — Cemal: 'algoritma insan gözünün gördüğü sıkışm… | göz-etiket (kör test) | kayıtta yok; dönem kayıtta yok | kayıtta yok | ÖLÇÜLEMEDİ | İŞARET YOK = VERİ YETERSİZ (işaretli grafik < 8) | B + D (B*: kayıtta n yok, güç bilinmiyor / D: Tiingo batan OHLC: SUNE yanlış seri (iki şirket birleştirilmiş), CHK karışık, OTC döneminde >1… (+2 satır)) | EVET | HAYIR | HAYIR: Cemal gözü; kasa fiyat bloğu değil, kör etiket gerekir |
| Ç167 | 2026-11-13 | Cemal'in göz kuralları / kör test | GOZ_G5: G5 sessiz bölge dedektörü ve 10 basit şekil ölçüsü x Cemal'in mevcut göz etiketleri (kalibre 29 COL +… — Kör test (Ç166) işaretsiz kalınca: G5 Cemal'in… | göz-etiket (kör test) | kayıtta yok; dönem kayıtta yok | kayıtta yok | İZ DEĞİL | G5 Cemal'in çöllerinin 1/29'unu yakalıyor | B + D (B*: kayıtta n yok, güç bilinmiyor / D: G5 Cemal'in çöllerinin 1/29'unu yakalıyor, olumsuzlarda daha sık (2/8); en iyi basit ölçü AUC…) | EVET | HAYIR | HAYIR: Cemal gözü; kasa fiyat bloğu değil, kör etiket gerekir |
| Ç168 | 2026-11-13 | hacim / tavan-taban | TAVAN SERİSİ: çökmüş BIST hissesinde (250 gün tepeden >= %80 aşağı) k. ardışık tavandan sonra katılmak (k = 1… — Cemal: fon krizinde 1 TL'ye inmiş hisseler art… | FI_OLCUT 60 gün eşli (dört şart) / geniş kesit | BIST; dönem kayıtta yok | n 120; 42 | İZ DEĞİL | İZ DEĞİL. k=1 (n 120, 38 hisse): ertesi gün tavan %35, 60g medyan -%10, +%100 %9, -%50 %7 (kontrol %0); medyan fark -%3,9 [-14,5; +9,4] = KUMAR. k >= | B + D (B: kayıtta yazılı en büyük n 120 (< 1.000; kayıtta bütün hücre n'leri yok) / D: k=1 'KUMAR' (medyan fark −%3,9 [−14,5; +9,4]); k >= 2 örneklem yetersiz (n 42) [ölçüt (örnekle…) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç169 | 2026-11-13 | hacim / tavan-taban | TAVAN SERİSİ HACİM (Cemal'in itirazı): H1 çökmüş + hacim >= 10x 20g medyan + tavan; H2 dipte tavansız hacim;… — Cemal: 'hepsi kumar değil; TEHOL'de devasa haci… | FI_OLCUT 60 gün eşli (dört şart) / geniş kesit | kayıtta yok; dönem kayıtta yok | n 11; 201; 54 | İZ DEĞİL | ana n 11 | B + D (B: kayıtta yazılı en büyük n 201 (< 1.000; kayıtta bütün hücre n'leri yok) / D: H1 ana hücre n 11 (9 hisse, 8'i 2016-19), kontrollü 5 olay: 'KANIT YOK' dendi; ilk raporda ora…) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç170 | 2026-11-13 | KAP olay | GENİŞ KESİT: çökmüş 64 BIST hissesi, 31.10'da bilinen 19 özellik vs 31.10 -> 13.11 dönüşü (Y1 kat, Y2 tavan s… — Cemal: 'emare vardır; geniş açıdan bak, bütün… | FI_OLCUT 60 gün eşli (dört şart) / geniş kesit | BIST; dönem kayıtta yok | kayıtta yok | EMARE | tek olay (çöküş), q 0,003 | B + D (B*: kayıtta n yok, güç bilinmiyor / D: Geri alım emaresi tek olaydan (31.10 -> 13.11, 64 hisse) [ölçüt (tek olay)]) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç171 | 2026-11-13 | fon izi / büyük alıcı / BofA | BofA İZİ: AKD alım listesi ilk 3 -> tutma dönemi (çıkış satış ilk 5 haberi; yoksa 250 gün), eşli fark + 200 r… — Cemal: 'BofA almış, emare; alımından satımına… | FI_OLCUT 60 gün eşli (dört şart) + 250 gün olasılık | kayıtta yok; 2023 | n 1.751; 79; 76 | İZ DEĞİL | BofA AKD alım listesi; güç yeterli | A + D (A: n 1.789 güç yeterli / D: BofA için ilk tasarım 60 gün sabit ufuktu; Cemal 'alımından satımına kadar takip et, 60 gün de… (+6 satır)) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç172 | 2026-11-13 | fon izi / büyük alıcı / BofA | BofA KENDİ MALİYETİNDEN KÂRI + HABER SONRASI YOL: A betimleyici (maliyetli alım satırı -> 5/20/60g, eşli; FIF… — Cemal: 'BofA bir hissede %40-80 zarar etmez; b… | FI_OLCUT 60 gün eşli (dört şart) + 250 gün olasılık | BIST; dönem kayıtta yok | n 87; 1.567; 732 | İZ DEĞİL | YOL YOK (BIST-ADAY ancak) | A? + D (A?: en büyük kayıtlı n ≥ 1.000, hücre bazı doğrulanmadı / D: BofA ayrıştırma 2: aylık / dönemsel özet haberleri (45) günlük liste sayıldı; 01.09 hisse.net… (+3 satır)) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç173a | 2026-11-13 | fon izi / büyük alıcı / BofA | DİPTE BofA: KURULUM = 250g tepeden <= -%80 + son 10 günde yeni dip yok + dipten <= 1,5 kat (60 gün ayrı olay)… — Cemal: 'her BofA alımında değil; dipte %80-90… | FI_OLCUT 60 gün eşli (dört şart) + 250 gün olasılık | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 81; 146; 3 / 8 | ÖLÇÜLEMEDİ | BofA dipte yolu ölçülemez (kriz öncesi olay 0) | B + D (B: kayıtta yazılı en büyük n 508 (< 1.000; kayıtta bütün hücre n'leri yok) / D: kayıt notunda düzeltme / denetim bulgusu var) | EVET | EVET | HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir |
| Ç173b | 2026-11-13 | şekil / yapı | DİPTE BofA: KURULUM = 250g tepeden <= -%80 + son 10 günde yeni dip yok + dipten <= 1,5 kat (60 gün ayrı olay)… — Cemal: 'her BofA alımında değil; dipte %80-90… | FI_OLCUT 60 gün eşli (dört şart) + 250 gün olasılık | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 81; 146; 3 / 8 | İZ DEĞİL | −%80 dip kurulumu: ABD 2023 TUTTU +%24,8, 2024-26 sıra tutmadı; piyango | B + D (B: kayıtta yazılı en büyük n 508 (< 1.000; kayıtta bütün hücre n'leri yok) / D: kayıt notunda düzeltme / denetim bulgusu var) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç174 | 2026-11-14 | sıkışma / oynaklık | SIKISMA_YENIDEN (bağımsız yeniden ölçüm, VDYT raporları okunmadan): S1 sıkışma (10 gün ort. TR/C <= 250 günün… — Cemal: 'şu kesin ki sıkışmadan sonra büyük mum… | diğer: S1 KAT (20 gün büyük gün, oynaklık eşli) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 1.266; 108; 2.392 | İZ DEĞİL | güç yeterli, eğilim TERS | A + D (A: n 1.266-9.540 güç yeterli / D: Bölünme şüphesi süzgecinin ilk hali sıçramanın geri dönüş bacağını da şüpheli sayıyordu (+8 satır)) | EVET | EVET | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç175 | 2026-11-14 | cetvel / altyapı / denetim | VDYT AİLESİ DENETİMİ (Ç162-Ç164) + ESKİ ÇÖL KAYITLARININ YENİDEN ETİKETLENMESİ: 14 maddelik kontrol listesiyl… — Cemal: 'eski çöller iz değil diye kaldı; bu ka… | diğer: VDYT (Brier skill, büyük hareket olasılığı) | ABD, BIST; 2023, 2024-26 | n 730; 307 | ALTYAPI / DENETİM (hipotez değil) | VDYT denetimi + eski çöl yeniden etiketleme | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç176 | 2026-11-14 | sıkışma / oynaklık | SIKISMA DUYARLILIĞI (Cemal'in 'gözüm neden büyük görsün' itirazı): büyük mum eşiği k {1,5; 2; 2,5; 3; 4} x re… — Cemal: 'gözüm küçük mumlardan sonra gelen muml… | diğer: S1 KAT (20 gün büyük gün, oynaklık eşli) | ABD, AVR, BIST; 2023, 2024-26 | n 5.868; 5.515; 71 | ALTYAPI / DENETİM (hipotez değil) | S1 duyarlılığı (bilgi) | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç177 | 2026-11-14 | cetvel / altyapı / denetim | ORTAK CETVEL v1.0 (Aşama 1 / 4): dört aşamalı yeniden ölçüm (K24 iki evre, D9 uzun çöl + rüzgâr, düzgün dip v… — Cemal: 'her aşamada aynı ölçüm kriterleri; son… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, BIST; 2016-22, 2023 | n 1.000 | ALTYAPI / DENETİM (hipotez değil) | ORTAK CETVEL v1.0 | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç178 | 2026-11-14 | şekil / yapı | K24 İKİ EVRE ÇÖL YENİDEN (Aşama 2 / 4, ORTAK CETVEL v1.0): FON_IZI fi_k24_tara değişmeden; BIST (bilgi), ABD… — Cemal: 'temel çöl yapısının tespit başarısını ö… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 2.869; 941; 100 | ÖLÇÜLEMEDİ | K24 iki evre çöl | B (B: karar ÖLÇÜLEMEDİ) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç179 | 2026-11-14 | şekil / yapı | DÜZGÜN DİP vs ÇÖL AYRIMI (Aşama 4 / 4, ORTAK CETVEL v1.0): dip16 (Ç75 FI_K16_GEVSEK) / dip17 (Ç78 k17) ile K2… — Cemal: 'çöl formasyonuyla gerçek dip oluşumunu… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, AVR; 2023, 2024-26 | n 400; 200; 1.059 / 1.248 / 2.518 | ÖLÇÜLEMEDİ | dip + çöl ayrımı | B (B: karar ÖLÇÜLEMEDİ) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç180 | 2026-11-14 | şekil / yapı | INTEM İLERİ TEST (Aşama 5, ORTAK CETVEL v1.0): Ç124 kuralı (FI_K44 parmak izi + K45 kısa ufuk kutu çıkışı, de… — Cemal: 'önceki aşamalardan çıkan kuralları değ… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, AVR; 2016-22, 2023, 2024-26 | n 26; 30; 42 | ÖLÇÜLEMEDİ | INTEM ileri test; EMARE desteklenmedi, iddia kapanmadı | B + D (B: kayıtta yazılı en büyük n 105 (< 1.000; kayıtta bütün hücre n'leri yok) / D: İş tanımında 'Avrupa V_AVR Ç124'te hiç yok' yazıldı; yanlış: Ç124 AVR'yi kullanmış (k44_eslesm…) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç181a | 2026-11-14 | şekil / yapı | D9 UZUN ÇÖL + SEKTÖR RÜZGÂRI YENİDEN (Aşama 3 / 4, ORTAK CETVEL v1.0; Ç37'nin kapanmamış testi): (a) D9 tek b… — Cemal: 'uzun süren sıkışmanın ve rüzgâr etkisi… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, AVR, BIST; 2023, 2024-26 | n 2.399; 4.556; 1.102 | İZ DEĞİL | D9 uzun çöl; güç yeterli | A + D (A: n 1.102-4.556 güç yeterli / D: Ajan (c) yalnız rüzgâr satırına 'İZ DEĞİL (AVR verisi yok)' etiketi yazdı; kurala göre AVR ola… (+5 satır)) | EVET | EVET | HAYIR: zaten A (güç yeterli İZ DEĞİL) |
| Ç181b | 2026-11-14 | sektör / makro | D9 UZUN ÇÖL + SEKTÖR RÜZGÂRI YENİDEN (Aşama 3 / 4, ORTAK CETVEL v1.0; Ç37'nin kapanmamış testi): (a) D9 tek b… — Cemal: 'uzun süren sıkışmanın ve rüzgâr etkisi… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, AVR, BIST; 2023, 2024-26 | n 2.399; 4.556; 1.102 | ÖLÇÜLEMEDİ | D9 + rüzgâr (T8) | B + D (B: karar ÖLÇÜLEMEDİ / D: Ajan (c) yalnız rüzgâr satırına 'İZ DEĞİL (AVR verisi yok)' etiketi yazdı; kurala göre AVR ola… (+5 satır)) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç181c | 2026-11-14 | sektör / makro | D9 UZUN ÇÖL + SEKTÖR RÜZGÂRI YENİDEN (Aşama 3 / 4, ORTAK CETVEL v1.0; Ç37'nin kapanmamış testi): (a) D9 tek b… — Cemal: 'uzun süren sıkışmanın ve rüzgâr etkisi… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, AVR, BIST; 2023, 2024-26 | n 2.399; 4.556; 1.102 | EMARE | yalnız sektör rüzgârı ABD; portföy şartı tutmadı, AVR ölçülemez | A? + D (A?: en büyük kayıtlı n ≥ 1.000, hücre bazı doğrulanmadı / D: Ajan (c) yalnız rüzgâr satırına 'İZ DEĞİL (AVR verisi yok)' etiketi yazdı; kurala göre AVR ola… (+5 satır)) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç182a | 2026-11-15 | şekil / yapı | TERSTEN PARMAK İZİ (Cemal: 'büyük mumdan geriye git, önceki mumların dizilimi / boyu / fitili / eğimi; bölge… — Cemal: 'sıkışma tanımın rastgele bölge seçiyor;… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 3.145; 16.258; 1.473 | EMARE | P1 büyük mumdan önceki profil | A? + D (A?: en büyük kayıtlı n ≥ 1.000, hücre bazı doğrulanmadı / D: Cemal: 'bin-üç bin olay dediğin sıkışmalar gerçek sıkışma değil, rastgele seçilmiş bölgeler; s… (+3 satır)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç182b | 2026-11-15 | şekil / yapı | TERSTEN PARMAK İZİ (Cemal: 'büyük mumdan geriye git, önceki mumların dizilimi / boyu / fitili / eğimi; bölge… — Cemal: 'sıkışma tanımın rastgele bölge seçiyor;… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 3.145; 16.258; 1.473 | EMARE | H1 çok günlü büyük hareket öncesi profil | A? + D (A?: en büyük kayıtlı n ≥ 1.000, hücre bazı doğrulanmadı / D: Cemal: 'bin-üç bin olay dediğin sıkışmalar gerçek sıkışma değil, rastgele seçilmiş bölgeler; s… (+3 satır)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç183 | 2026-11-15 | sıkışma / oynaklık | CEMAL TANIMLI SIKIŞMA S4 (FENER itirazı üzerine): 15 gün küçük mum (250 gün %20 yüzdeliği) + dar Bollinger (B… — Cemal (FENER grafiği): 'kod 3-16 Aralık'ı seçm… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, AVR, BIST; 2023 | n 467 | ÖLÇÜLEMEDİ | S4 Cemal tanımlı sıkışma | B + D (B: kayıtta yazılı en büyük n 467 (< 1.000; kayıtta bütün hücre n'leri yok) / D: S1 yalnız 'küçük mum + 10 gün bant' soruyor; FENER'de 3-16 Ara 2025'i seçti (mum 0,46 x ATR am… (+1 satır)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç184 | 2026-11-15 | sıkışma / oynaklık | S5 ÖBEK SIKIŞMASI (Cemal'in üç grafiğinden): 15 bar, en büyük 1 mum (zıplama) hariç MEDYAN mum <= 0,75 x ATR2… — Cemal: 'öbek gibi yan yana sıkışmış mumlar, zı… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, AVR, BIST; 2023, 2024-26 | n 292 / 389; 1.000; 578 | EMARE | S5 DİP öbek sıkışması (ABD büyük gün 1,14-1,17 kat) | A? + D (A?: en büyük kayıtlı n ≥ 1.000, hücre bazı doğrulanmadı / D: Cemal'in fotoğraflarından bölge tarihleri okunamıyor; ana model ENJSA bölgesini tahminle (10 T… (+6 satır)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç185 | 2026-11-15 | sektör / makro | SEKTÖR RÜZGÂRI AVRUPA'DA (Ç181c devamı; Cemal 'sektör derle'): STOXX 600 + FTSE 250 evreni için sektor_AVR.cs… — Cemal: 'UZUN ÇÖL ETİKETİNİ KALDIR sektör derle… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | ABD, AVR; 2023, 2024-26 | n 125; 447; 110 / 201 | ÖLÇÜLEMEDİ | rüzgâr Avrupa'da | B (B: kayıtta yazılı en büyük n 447 (< 1.000; kayıtta bütün hücre n'leri yok)) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç186 | 2026-11-16 | sektör / makro | ÇÖKÜŞ SONRASI OYNAK HİSSE (Cemal'in tezi: fon krizinde her şey %40+ düştü, artık çok düşmez, oynak hisse seçi… — Cemal: 'bu dönemde risk büyük değil, gerçekten… | ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık) | kayıtta yok; 2023 | n 69; 217; 73 / 219 / 72 | ÖLÇÜLEMEDİ | çöküş sonrası oynak hisse; tamamlanmış çöküş 1 < 2 | B + D (B: kayıtta yazılı en büyük n 219 (< 1.000; kayıtta bütün hücre n'leri yok) / D: kayıt notunda düzeltme / denetim bulgusu var) | EVET | EVET | HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir |
| Ç187 | 2026-11-16 | şekil / yapı | FİTİL ÖBEĞİ (Cemal: PAPIL'de alt fitilsiz / üst fitilli mum öbeği 'has yukarı çıkma mumları', DGXX'te tersi d… — Cemal: 'parmak izini çıkar... DGXX'te o mumlar… | ORTAK_CETVEL v1.0 (60 gün r60) | ABD, AVR, BIST; 2023, 2024-26 | n 1.000; 2.180; 1.734 | ÖLÇÜLEMEDİ | fitil öbeği; 2024-26 hücreleri TUTMADI, 2023 güç %52 | B + D (B: karar ÖLÇÜLEMEDİ / D: Yapı (taban / fitil öbeği / sıkışma) kuralları 60 günlük eşli farkla ölçüldü; Cemal: bu yapıla…) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç188 | 2026-11-16 | şekil / yapı | FİTİL ÖBEĞİ — HATA NEREDE (üç halka): HALKA 1 tanım bağlamı (S+ yalnız S6 taban içi, DİP sınıfı; varyantlar g… — Cemal: 'kesin bir tanı; kod ya şeklimi almadı,… | ORTAK_CETVEL v1.0 (60 gün r60) | ABD; 2024-26 | n 60; 11; 80 | ALTYAPI / DENETİM (hipotez değil) | fitil öbeği hata nerede (tanım bağlamı) | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç189 | 2026-11-17 | şekil / yapı | S+ v2 'TAM GİRİLİR' (Cemal'in kör set kurallarından): şekil S+ (ASİM >= 0,20, alt fitilsiz payı >= 0,50) + sa… — Cemal: 'kod bu kurallar eşiğinde tam girilir d… | ORTAK_CETVEL v1.0 (60 gün r60) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 47; 187; 34 | ÖLÇÜLEMEDİ | S+ v2 | B + D (B: karar ÖLÇÜLEMEDİ / D: Kör set sorusu 'bu son mumda tam girilir mi' diye mum gününe göre soruldu; Cemal grafiği forma… (+2 satır)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç190 | 2026-11-17 | şekil / yapı | YAPI_HEDEF: yapı kurallarının Cemal'in yeni test standardıyla ilk ölçümü (giriş = kırılım mumundan sonraki il… — Cemal (17 Kas akşam): '60 gün testi kapandı; k… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite) | ABD, AVR, BIST; 2023, 2024-26 | n 2.040 / 4.083 / 815 / 1.711; 34; 257 | ÖLÇÜLEMEDİ | Y1-Y5, 15 bar | C + B + D (C: h5 cetveli (Ç203 oynaklık kusuru); B: karar hücreleri n < 1.000 / güç < %80 / D: Eşler momentum x likidite ile eşlendi, oynaklıkla eşlenmedi; kırılım sonrası oynak olaylar (Y3… (+6 satır)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç191 | 2026-11-17 | şekil / yapı | YAPI_HEDEF 2. tur: Cemal'in PDF değerlendirmesinden (E1-E7) kurulan Y6 (S6 AL + hat >= 3 dokunuş eğimsiz + ge… — Cemal'in el yazısı notları (17 Kas akşam, sonu… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite) | ABD, AVR; 2016-22, 2023, 2024-26 | n 0; 0 | ÖLÇÜLEMEDİ | Y6 / Y8; yön aleyhte | C + B + D (C: h5 cetveli (Ç203 oynaklık kusuru); B: karar hücreleri n < 1.000 / güç < %80 / D: Y7'de 'stop uzaklığı <= %10' şartı Y3'ün 'kapanış > pencere tavanı' kırılımıyla birlikte hiç o… (+2 satır)) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç192 | 2026-11-17 | Cemal'in göz kuralları / kör test | GOZ_ETIKET: kodun bulduğu S6 taban kırılımlarını (Y1) Cemal'in gözüyle (C1-C13: taban net, dip savunulmuş, kü… — Cemal (17 Kas akşam): 'benim nasıl karar verdi… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite) | ABD, AVR; 2016-22, 2023, 2024-26 | n 6; 57; 243 | ÖLÇÜLEMEDİ | göz skoru; yön ters | C + B + D (C: h5 cetveli (Ç203 oynaklık kusuru); B: karar hücreleri n < 1.000 / güç < %80 / D: RR.L 2022-12-14 barında High 239,65, O / C ~90 (komşular <= 94,66): tek alanlık veri hatası. T… (+5 satır)) | EVET | HAYIR | HAYIR: Cemal gözü; kasa fiyat bloğu değil, kör etiket gerekir |
| Ç193 | 2026-11-18 | şekil / yapı | YAPI_HEDEF 3. tur: Cemal'in çöl tanımıyla bağlam süzgeci: Y9 DÜŞÜŞ SONRASI DİPTE (S6 AL + 120 gün konumu <= 0… — Cemal (18 Kas): 'çoğunda şemsiye var, bunlar y… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite) | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 146 / 231 / 20 / 55 | ÖLÇÜLEMEDİ | Y9 dipte S6 (bakılmış ABD KAT5 1,15 / 1,21) | C + B (C: h5 cetveli (Ç203 oynaklık kusuru); B: karar hücreleri n < 1.000 / güç < %80) | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç194 | 2026-11-18 | şekil / yapı | YAPI_HEDEF 4. tur: S7 CEMAL BÖLGE SEÇİCİ: S6 AL olayına Cemal'in 8 kuralı mekanik süzgeç olarak: Ş1 dipte (F1… — Cemal (18 Kas): 'onca fikir ve bu şekilde olsu… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite); Ç204'te CETVEL2 R15 (stop'suz) ile yeniden koşuldu | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 25; 6; 31 | ÖLÇÜLEMEDİ (h5) → Ç204 CETVEL2 R15 yeniden koşu: ÖLÇÜLEMEDİ 2, SORGULA 1 | S7 / Y10 | A / B (CETVEL2 R15) + D (h5 etiketi Ç204'te yeniden koşuldu (R15 etiketleri: ÖLÇÜLEMEDİ 2, SORGULA 1); Ç204 kaydı: güç ≥ 0,80 dört hücrede olup hiçbir hücresi tutmayan hipotezler (52 kod) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü e… | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç195 | 2026-11-19 | şekil / yapı | YAPI_HEDEF 5. tur: Ş9 U DİP + PARABOLİK DEVAM (Cemal K47, S7 PDF No 38): son 40 geçerli barın Low serisine ik… — Cemal (19 Kas): 'bölge U dip çizmeli ve parabo… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite); Ç204'te CETVEL2 R15 (stop'suz) ile yeniden koşuldu | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 3 / 15; 20; 0 | ÖLÇÜLEMEDİ (h5) → Ç204 CETVEL2 R15 yeniden koşu: ÖLÇÜLEMEDİ 3 | Ş9 U dip / Y11 | A / B (CETVEL2 R15) + D (h5 etiketi Ç204'te yeniden koşuldu (R15 etiketleri: ÖLÇÜLEMEDİ 3); Ç204 kaydı: güç ≥ 0,80 dört hücrede olup hiçbir hücresi tutmayan hipotezler (52 kod) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü etki için)',… | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç196 | 2026-11-19 | şekil / yapı | YAPI_HEDEF 6. tur: (A) GRUPLAR G0 bütün Y1 / G1 trend içi raf (F14 >= 0, F15 >= 0,50) / G2 düşüş sonrası dip… — Cemal (19 Kas): 'gruplar: trend / düşüş ve dip… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite); Ç204'te CETVEL2 R15 (stop'suz) ile yeniden koşuldu | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 54 | ÖLÇÜLEMEDİ (h5) → Ç204 CETVEL2 R15 yeniden koşu: ÖLÇÜLEMEDİ 13, SORGULA 9 | G2 dip vs G1 trend içi raf | A / B (CETVEL2 R15) + D (h5 etiketi Ç204'te yeniden koşuldu (R15 etiketleri: ÖLÇÜLEMEDİ 13, SORGULA 9); Ç204 kaydı: güç ≥ 0,80 dört hücrede olup hiçbir hücresi tutmayan hipotezler (52 kod) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü… | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç197 | 2026-11-19 | momentum / gösterge / makine / sinyal kütüphanesi | YAPI_HEDEF 7. tur PUAN: bütün Y1 bölgeleri (26.663) F1-F29 ile puanlanır; hedef h5 (15 barda +%5 stop'tan önc… — Cemal (19 Kas): 'kod bütün bölgelerde puanlama… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite); Ç204'te CETVEL2 R15 (stop'suz) ile yeniden koşuldu | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 1737 | ÖLÇÜLEMEDİ (h5) → Ç204 CETVEL2 R15 yeniden koşu: SORGULA 4 | F1-F29 puan üst %20 | A / B (CETVEL2 R15) + D (h5 etiketi Ç204'te yeniden koşuldu (R15 etiketleri: SORGULA 4); Ç204 kaydı: güç ≥ 0,80 dört hücrede olup hiçbir hücresi tutmayan hipotezler (52 kod) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü etki için)', gü… | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç198 | 2026-11-19 | web hipotezleri (DS / DEVİR) | DEVİR 1 (Workflow col-devir, 7 ajan): araştırma (web sonnet: W1 Corwin-Schultz spread, W2 gece / gün-içi geti… — Cemal (19 Kas): 'altı yapay zekâya görev dağıt… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite); Ç204'te CETVEL2 R15 (stop'suz) ile yeniden koşuldu | AVR; dönem kayıtta yok | n 41; 33; 30 | ÖLÇÜLEMEDİ (h5) → Ç204 CETVEL2 R15 yeniden koşu: SORGULA 18, ÖLÇÜLEMEDİ 18 | devir 1 (F30-F42) | A / B (CETVEL2 R15) + D (h5 etiketi Ç204'te yeniden koşuldu (R15 etiketleri: SORGULA 18, ÖLÇÜLEMEDİ 18); Ç204 kaydı: güç ≥ 0,80 dört hücrede olup hiçbir hücresi tutmayan hipotezler (52 kod) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü… | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç199 | 2026-11-19 | web hipotezleri (DS / DEVİR) | DEVİR 2 (Workflow col-devir, 7 ajan): karne v2 (60 bar ambargo, ABD / AVR ayrı n >= 30, ay kümeli bootstrap,… — Cemal (19 Kas): sürekli devir; web / sosyal med… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite); Ç204'te CETVEL2 R15 (stop'suz) ile yeniden koşuldu | ABD, AVR; dönem kayıtta yok | n 30; 29 | ÖLÇÜLEMEDİ (h5) → Ç204 CETVEL2 R15 yeniden koşu: SORGULA 8, ÖLÇÜLEMEDİ 12 | devir 2 | A / B (CETVEL2 R15) + D (h5 etiketi Ç204'te yeniden koşuldu (R15 etiketleri: SORGULA 8, ÖLÇÜLEMEDİ 12); Ç204 kaydı: güç ≥ 0,80 dört hücrede olup hiçbir hücresi tutmayan hipotezler (52 kod) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü… | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç200 | 2026-11-19 | web hipotezleri (DS / DEVİR) | DEVİR 3 (dar yeniden sınama; karne v3: v2 + ATRP ve F13 tabakası, her ATRP tercilinde MARJ > 0, KATKI− için b… — Devir 2 eleştiri lenslerinin önceden yazdığı y… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite); Ç204'te CETVEL2 R15 (stop'suz) ile yeniden koşuldu | ABD, AVR; 2024-26 | kayıtta yok | ÖLÇÜLEMEDİ (h5) → Ç204 CETVEL2 R15 yeniden koşu: SORGULA 4, ÖLÇÜLEMEDİ 4 | devir 3 | A / B (CETVEL2 R15) + D (h5 etiketi Ç204'te yeniden koşuldu (R15 etiketleri: SORGULA 4, ÖLÇÜLEMEDİ 4); Ç204 kaydı: güç ≥ 0,80 dört hücrede olup hiçbir hücresi tutmayan hipotezler (52 kod) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü e… | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç201 | 2026-11-20 | şekil / yapı | YAPI_HEDEF 8. tur: Ş10 MACD POZİTİF UYUMSUZLUK (Cemal K47 / K48): [t-60, t-1] iki salınım dibi (5 bar yerel m… — Cemal (20 Kas, ekran görüntüsü BIST Haz-Ağu 20… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite); Ç204'te CETVEL2 R15 (stop'suz) ile yeniden koşuldu | ABD, AVR, BIST; 2016-22, 2023, 2024-26 | n 226 / 378 / 77 / 157; 712; 360 | ÖLÇÜLEMEDİ (h5) → Ç204 CETVEL2 R15 yeniden koşu: SORGULA 2, ÖLÇÜLEMEDİ 1 | Ş10 MACD pozitif uyumsuzluk | A / B (CETVEL2 R15) + D (h5 etiketi Ç204'te yeniden koşuldu (R15 etiketleri: SORGULA 2, ÖLÇÜLEMEDİ 1); Ç204 kaydı: güç ≥ 0,80 dört hücrede olup hiçbir hücresi tutmayan hipotezler (52 kod) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü e… | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç202 | 2026-11-20 | web hipotezleri (DS / DEVİR) | DÜŞÜŞ SONRASI PARMAK İZİ (DS): web araştırması 4 kol (akademik / pratisyen / güncel açık kaynak + sosyal / te… — Cemal (20 Kas): 'bizde olmayan hipotezleri web… | 15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite); Ç204'te CETVEL2 R15 (stop'suz) ile yeniden koşuldu | ABD, AVR, BIST; 2016-22, 2023 | n 6; 224; 1.724 | ÖLÇÜLEMEDİ (h5) → Ç204 CETVEL2 R15 yeniden koşu: SORGULA 15, ÖLÇÜLEMEDİ 10 | DS 25 / 25 ÖLÇÜLEMEDİ | A / B (CETVEL2 R15) + D (h5 etiketi Ç204'te yeniden koşuldu (R15 etiketleri: SORGULA 15, ÖLÇÜLEMEDİ 10); Ç204 kaydı: güç ≥ 0,80 dört hücrede olup hiçbir hücresi tutmayan hipotezler (52 kod) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü… | EVET | EVET | EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı |
| Ç203 | 2026-11-20 | cetvel / altyapı / denetim | POZİTİF KONTROL: 15 bar cetveli (giriş t+1 açılış, stop dip x 0,98, +%5 / +%10, eş = aynı gün aynı ATRP x lik… — Cemal (20 Kas): 'sadece veri madenciliği yapıy… | pozitif kontrol (h5 + r15 + r60 yan yana) | ABD, AVR; dönem kayıtta yok | n 1000; 1000; 300 | ALTYAPI / DENETİM (hipotez değil) | pozitif kontrol | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |
| Ç204 | 2026-11-21 | cetvel / altyapı / denetim | CETVEL2 (düzeltilmiş 15 mum cetveli) + pozitif kontrol v2 + Ç194-Ç202 yeniden koşusu. Tanım: R15 = 15. geçerl… — Cemal (21 Kas): 'bahsettiğim hataları düzelt,… | CETVEL2 R15 (15. geçerli bar kapanışı / t+1 açılış − 1, stop yok; eş = ATRP × likidite × F15 çeyreği) | ABD, AVR, BIST; dönem kayıtta yok | n 30; 40 | ALTYAPI / DENETİM (hipotez değil) | CETVEL2 (R15) pozitif kontrol v2 + Ç194-Ç202 yeniden koşusu (124 hipotez) | - | EVET | - | HAYIR: hipotez değil (altyapı / denetim) |

### 2b. K60 sinyal kütüphanesi (Ç154 içinde; 126 sinyal-uç çifti; ölçüm: 12 ay +%100 / −%50 olasılık katı, üç dönem KEŞİF / DOĞRULAMA / KASA)

Hepsi ABD, yalnız yaşayanlar (K7), cetvel R1 / R2 (K60). Karar: İZ ADAYI 0; "K60-OLASILIK İZİ" etiketleri oynaklık etkisi (karar bilgisi değil). Sütun: kat = (+%100 katı / −%50 katı) KEŞİF → DOĞRULAMA → KASA. GÜV: A (cetvel v2 güvenilir) + D (oynaklık karışımı: Ç154).

| sinyal (uç) | +%100 katı KE / DO / KA | −%50 katı KE / DO / KA |
|---|---|---|
| ACCRUALS (ALT) | 1,27 / 1,52 / 1,32 | 1,34 / 1,47 / 1,35 |
| ACCRUALS (ÜST) | 2,24 / 1,60 / 1,47 | 2,57 / 2,00 / 2,24 |
| ACT_13D (ÜST) | 1,26 / 0,60 / 0,81 | 2,24 / 2,09 / 2,01 |
| AILE_DIS (ALT) | 2,32 / 2,76 / 2,61 | 3,20 / 3,92 / 3,35 |
| AILE_DIS (ÜST) | 0,33 / 0,30 / - | 0,27 / 0,10 / - |
| AILE_EAR (ALT) | 1,46 / 1,45 / 1,44 | 1,80 / 1,75 / 1,57 |
| AILE_EAR (ÜST) | 1,05 / 1,57 / 1,19 | 0,81 / 0,88 / 1,16 |
| AILE_INV (ALT) | 1,47 / 1,67 / 1,71 | 2,52 / 2,04 / 1,73 |
| AILE_INV (ÜST) | 0,83 / 0,69 / 0,46 | 0,37 / 0,41 / 0,66 |
| AILE_LIQ (ALT) | 0,41 / 0,55 / - | 0,45 / 0,25 / - |
| AILE_LIQ (ÜST) | 1,80 / 2,04 / 1,53 | 1,93 / 2,17 / 2,24 |
| AILE_MOM (ALT) | 1,62 / 1,57 / 1,72 | 1,85 / 2,36 / 1,61 |
| AILE_MOM (ÜST) | 1,19 / 1,47 / - | 1,17 / 0,53 / - |
| AILE_PRF (ALT) | 1,53 / 1,95 / 1,98 | 2,43 / 2,68 / 2,11 |
| AILE_PRF (ÜST) | 0,76 / 0,77 / - | 0,58 / 0,33 / - |
| AILE_RSK (ALT) | 2,10 / 2,02 / 1,99 | 2,23 / 2,23 / 2,26 |
| AILE_RSK (ÜST) | 0,21 / 0,16 / - | 0,18 / 0,18 / - |
| AILE_SEA (ALT) | 1,73 / 1,86 / 1,58 | 1,97 / 2,32 / 2,27 |
| AILE_SEA (ÜST) | 1,61 / 1,41 / 1,66 | 1,93 / 1,70 / 1,49 |
| AILE_SEC (ALT) | 1,02 / 1,00 / - | 1,23 / 1,05 / - |
| AILE_SEC (ÜST) | 1,16 / 1,14 / - | 0,94 / 0,47 / - |
| AILE_VAL (ALT) | 2,14 / 1,81 / 1,92 | 2,82 / 2,54 / 2,48 |
| AILE_VAL (ÜST) | 1,32 / 0,62 / - | 0,63 / 0,51 / - |
| AM (ALT) | 1,65 / 1,27 / 1,14 | 2,03 / 1,27 / 1,55 |
| AMIHUD (ÜST) | - / 2,33 / 1,60 | - / 2,67 / 3,23 |
| ASSET_G (ALT) | 1,65 / 1,58 / 1,68 | 2,58 / 2,25 / 1,68 |
| ASSET_G (ÜST) | 1,79 / 1,98 / 1,59 | 1,43 / 2,15 / 2,32 |
| BETA_BAB (ALT) | 2,41 / 2,39 / 2,71 | 1,89 / 1,80 / 2,24 |
| BE_G (ALT) | 1,46 / 1,25 / 1,42 | 2,31 / 1,78 / 1,41 |
| BE_G (ÜST) | 1,82 / 1,95 / 1,55 | 1,49 / 1,93 / 2,22 |
| BM (ALT) | 1,36 / 0,93 / - | 1,60 / 1,00 / - |
| BM (ÜST) | 1,59 / 1,33 / 1,01 | 1,20 / 1,01 / 1,03 |
| BUYBACK_YLD (ALT) | 1,28 / 1,44 / 1,22 | 1,48 / 1,54 / 1,33 |
| CAPEX_G (ALT) | 1,75 / 1,68 / 1,38 | 2,21 / 2,43 / 1,74 |
| CAPEX_G (ÜST) | 1,52 / 1,70 / 1,82 | 1,59 / 1,27 / 2,53 |
| CBOP_A (ALT) | 2,15 / 2,55 / 2,40 | 3,37 / 3,76 / 3,42 |
| CFP (ALT) | 2,19 / 2,67 / 2,28 | 2,85 / 3,16 / 3,12 |
| CFP (ÜST) | 2,11 / 0,95 / - | 1,24 / 0,77 / - |
| CHS_FAIL (ALT) | 2,70 / 2,45 / 2,31 | 2,77 / 3,41 / 2,88 |
| COMP4 (ALT) | 1,89 / 2,09 / 2,17 | 2,49 / 2,71 / 2,39 |
| COMP4 (ÜST) | 0,70 / 1,02 / 0,74 | 0,43 / 0,25 / 0,47 |
| DOLVOL (ÜST) | 1,58 / 1,68 / 1,25 | 1,78 / 1,84 / 2,18 |
| DOSYA_Y (ALT) | 1,89 / 1,54 / 1,50 | 1,98 / 2,10 / 2,21 |
| DOSYA_Y (ÜST) | 0,95 / 1,08 / 0,98 | 0,62 / 0,54 / 0,61 |
| D_ASSET_TURN (ALT) | 1,48 / 1,15 / 1,02 | 1,35 / 1,33 / 1,09 |
| D_ASSET_TURN (ÜST) | 1,55 / 1,61 / 1,59 | 1,33 / 0,86 / 1,70 |
| EARN_STREAK (ALT) | 1,45 / 1,44 / 1,31 | 1,73 / 2,11 / 1,24 |
| EAR_ANN (ALT) | 1,67 / 1,57 / 1,54 | 1,87 / 1,79 / 1,59 |
| EAR_ANN (ÜST) | 1,70 / 1,93 / 1,61 | 1,44 / 1,87 / 1,61 |
| EAR_FILE (ALT) | 1,73 / 1,70 / 1,62 | 1,94 / 1,81 / 1,60 |
| EAR_FILE (ÜST) | 1,71 / 1,81 / 1,67 | 1,53 / 1,83 / 1,59 |
| EAR_VOL (ALT) | 1,09 / 1,32 / 1,25 | 1,74 / 1,35 / 1,72 |
| EAR_VOL (ÜST) | 1,20 / 1,25 / 1,03 | 1,15 / 1,10 / 1,22 |
| EP (ALT) | 2,69 / 2,82 / 2,32 | 2,84 / 3,32 / 2,95 |
| EV_EBITDA (ALT) | 1,46 / 1,07 / - | 1,10 / 1,12 / - |
| EV_EBITDA (ÜST) | 1,52 / 1,18 / - | 1,21 / 0,69 / - |
| E_424B5 (ALT) | 1,02 / 0,91 / 1,03 | 1,39 / 1,26 / 1,69 |
| E_DIV_OMIT (ALT) | 1,70 / - / - | 0,78 / - / - |
| E_IPO_3Y (ALT) | 1,93 / 1,77 / 1,64 | 2,79 / 2,66 / 2,01 |
| E_RSPLIT (ALT) | 1,57 / 1,81 / 1,35 | 4,30 / 3,95 / 5,53 |
| E_S3 (ALT) | 1,17 / 1,05 / 1,17 | 1,56 / 1,45 / 1,50 |
| F_SCORE (ALT) | 2,04 / 2,67 / 2,08 | 2,60 / 2,90 / 2,87 |
| GAP_OVN (ALT) | 1,35 / 1,38 / 1,39 | 1,80 / 1,85 / 1,49 |
| GAP_OVN (ÜST) | 1,82 / 1,69 / 1,88 | 2,13 / 1,92 / 2,05 |
| GP_A (ALT) | 1,46 / 1,42 / 1,88 | 2,16 / 2,83 / 1,80 |
| GP_A (ÜST) | 1,49 / 1,27 / 0,69 | 1,21 / 0,86 / 1,50 |
| HIGH52 (ALT) | 2,43 / 2,45 / 2,24 | 3,47 / 3,38 / 2,79 |
| IND_LEAD_BIG (ALT) | 1,21 / 1,33 / 1,54 | 1,46 / 1,36 / 1,02 |
| IND_LEAD_BIG (ÜST) | 1,46 / 1,21 / - | 1,10 / 1,05 / - |
| IND_MOM_6 (ALT) | 1,18 / 1,14 / 1,04 | 1,43 / 1,26 / 0,74 |
| IND_MOM_6 (ÜST) | 1,42 / 1,32 / - | 1,34 / 0,59 / - |
| ISKEW (ALT) | 1,17 / 1,25 / 1,18 | 1,37 / 1,26 / 1,40 |
| IVOL_FF3 (ALT) | 2,49 / 2,49 / 2,10 | 3,40 / 3,26 / 3,25 |
| LEV_MKT (ALT) | 1,56 / 1,51 / 1,47 | 2,36 / 1,88 / 1,81 |
| LTREV_60_13 (ÜST) | 2,14 / 1,91 / 1,54 | 2,34 / 1,47 / 2,30 |
| MAX5 (ALT) | 2,62 / 2,35 / 2,27 | 3,23 / 3,38 / 3,14 |
| MOM_12_1 (ALT) | 2,16 / 2,11 / 1,90 | 2,40 / 3,07 / 2,27 |
| MOM_12_1 (ÜST) | 1,79 / 2,03 / 1,90 | 2,05 / 1,01 / 2,02 |
| MOM_6_1 (ALT) | 2,01 / 2,02 / 1,94 | 2,54 / 2,95 / 2,13 |
| MOM_6_1 (ÜST) | 1,88 / 1,98 / 1,78 | 1,94 / 1,44 / 2,19 |
| MOM_FIP (ALT) | 1,16 / 0,97 / 1,00 | 1,43 / 1,27 / 1,00 |
| MOM_INT_12_7 (ALT) | 2,06 / 2,03 / 1,83 | 2,10 / 2,83 / 2,51 |
| MOM_INT_12_7 (ÜST) | 1,69 / 1,93 / 1,96 | 2,05 / 1,21 / 1,72 |
| NDF_BS (ALT) | 1,15 / 1,39 / 1,25 | 1,03 / 1,01 / 1,02 |
| NDF_BS (ÜST) | 1,27 / 1,23 / 1,15 | 0,91 / 0,72 / 0,99 |
| NEF (ALT) | 1,52 / 1,82 / 1,94 | 2,63 / 2,40 / 2,02 |
| NEF (ÜST) | 0,67 / 0,70 / 0,46 | 0,35 / 0,47 / 0,57 |
| NET_PAYOUT_YLD (ALT) | 1,43 / 1,74 / 1,81 | 2,36 / 2,29 / 1,96 |
| NOA (ALT) | 0,94 / 1,15 / 1,06 | 1,62 / 1,34 / 1,06 |
| NOA (ÜST) | 1,49 / 1,63 / 1,48 | 1,81 / 1,90 / 1,77 |
| NSI_1Y (ALT) | 1,62 / 1,81 / 1,92 | 2,64 / 2,19 / 2,35 |
| NSI_5Y (ALT) | 1,46 / 1,39 / 1,59 | 2,19 / 2,06 / 1,88 |
| NT_LATE (ALT) | 1,16 / 1,50 / 1,20 | 2,74 / 2,49 / 2,62 |
| ODDS_MODEL (ÜST) | 2,53 / 2,64 / 2,18 | 2,85 / 3,20 / 3,20 |
| OPLEV (ÜST) | 1,42 / 1,56 / 1,01 | 1,06 / 0,99 / 1,57 |
| OP_BE (ALT) | 2,45 / 2,45 / 2,25 | 3,28 / 3,43 / 3,32 |
| O_SCORE (ALT) | 2,43 / 2,48 / 2,05 | 3,52 / 3,39 / 3,41 |
| PRICE_LVL (ÜST) | 2,47 / 2,18 / 2,23 | 3,11 / 3,30 / 2,75 |
| RD_ME (ALT) | 0,75 / 0,74 / 1,07 | 1,64 / 1,20 / 1,09 |
| RD_ME (ÜST) | 2,59 / 3,38 / 2,32 | 3,43 / 3,56 / 3,61 |
| REV_SURP (ALT) | 1,19 / 0,86 / 0,86 | 1,00 / 1,20 / 1,17 |
| REV_SURP (ÜST) | 0,79 / 0,90 / - | 0,85 / 0,76 / - |
| ROA_Q (ALT) | 2,44 / 2,36 / 2,41 | 3,42 / 3,63 / 3,29 |
| ROE_TTM (ALT) | 2,48 / 2,47 / 2,16 | 3,06 / 3,22 / 3,10 |
| RUNWAY (ALT) | 2,19 / 2,61 / 2,32 | 2,95 / 3,24 / 3,11 |
| SALES_ACCEL (ALT) | 1,56 / 1,21 / 1,25 | 1,48 / 1,60 / 1,67 |
| SALES_ACCEL (ÜST) | 1,47 / 1,62 / 1,28 | 1,62 / 1,67 / 1,39 |
| SEAS_1 (ALT) | 1,76 / 1,85 / 1,65 | 1,86 / 2,28 / 2,19 |
| SEAS_1 (ÜST) | 1,63 / 1,47 / 1,81 | 1,99 / 1,55 / 1,54 |
| SEAS_2_5 (ALT) | 1,46 / 1,43 / 1,40 | 1,79 / 1,29 / 1,56 |
| SEAS_2_5 (ÜST) | 1,44 / 1,32 / 1,53 | 1,38 / 1,45 / 1,34 |
| SIZE_ME (ÜST) | 2,25 / 2,11 / 1,61 | 2,94 / 2,67 / 2,82 |
| SKEW_TOT (ALT) | 1,26 / 1,22 / 1,09 | 1,44 / 1,48 / 1,59 |
| SP (ALT) | 1,66 / 1,36 / 1,60 | 2,33 / 2,24 / 1,78 |
| SP (ÜST) | 2,17 / 1,71 / 1,18 | 1,04 / 0,91 / 1,29 |
| SPREAD_CS (ÜST) | 2,61 / 2,57 / 2,35 | 3,60 / 3,76 / 3,56 |
| STREV_1M (ALT) | 1,76 / 1,75 / 1,78 | 1,82 / 1,81 / 1,98 |
| STREV_1M (ÜST) | 1,77 / 1,86 / 1,67 | 2,39 / 2,34 / 2,24 |
| SUE_SRW (ALT) | 1,34 / 1,18 / 1,26 | 1,69 / 1,71 / 1,27 |
| TAX_CHG (ALT) | 1,31 / 0,93 / 1,02 | 1,01 / 1,13 / 1,00 |
| TREND_MA (ALT) | 1,90 / 1,84 / 1,42 | 2,18 / 2,48 / 2,27 |
| TREND_MA (ÜST) | 1,77 / 1,78 / 1,87 | 1,91 / 1,73 / 1,92 |
| TURN_12M (ALT) | 2,36 / 2,16 / 2,01 | 2,74 / 2,59 / 2,64 |
| VOL_60D (ALT) | 2,73 / 2,56 / 2,46 | 3,62 / 3,81 / 3,44 |
| VOL_SHOCK (ALT) | 1,33 / 1,26 / 1,30 | 1,90 / 1,92 / 1,90 |
| VOL_SHOCK (ÜST) | 1,26 / 1,33 / 1,23 | 1,30 / 1,28 / 1,37 |

### 2c. Düşüş sonrası (DS) web hipotezleri (Ç202; 87 DS = 123 web hipotezi tekilleştirildi; ölçülen 25 / 25 ÖLÇÜLEMEDİ)

| DS | hipotez | kaynak kodları (WEB A-D) | süzgeç sınıfı | ölçüldü mü / ABD sınama FARK / güç / etiket | karar | GÜV | KASA |
|---|---|---|---|---|---|---|---|
| DS01 | Fiyat yolu konveksliği (kazan / hızlanan düşüş) | A14 | I | EVET: 1422 / +0,5 / %45-%47 / boot [-3,0, +3,4] / güç 1,00 / 0,99 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS02 | Kaybeden × devir (düşük devir döner, yüksek sürer) | A2, A12 | I | EVET: 790 / +0,2 / %48-%47 / boot [-3,4, +3,5] / güç 0,98 / 0,91 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80: AVR sinama) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS03 | Sektör (AVR: piyasa) artığı son ay düşüşü döner | A4 | I | EVET: 1316 / -0,4 / %50-%50 / boot [-2,7, +2,1] / güç 0,98 / 0,99 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS04 | Büyük tek gün düşüşü / dead-cat fazı | A18, A19, B21, B22 | I | EVET: 964 / -0,9 / %44-%43 / boot [-4,4, +2,4] / güç 1,00 / 0,95 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80: AVR sinama) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS05 | Kapitülasyon / satış doruğu (geniş aralık + hacim) | B12, C15, C16, A11, A13 | I | EVET: 3905 / +0,4 / %43-%44 / boot [-1,2, +2,0] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS06 | Dip süpürme + geri alma (Turtle Soup, spring, likidite süpürme, Oops) | B24, C1, C2, B26, B14 | I | EVET: 224 / +6,9 / %42-%49 / boot [+1,0, +12,9] / güç 0,59 / 0,38 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80: ABD sinama, AVR egitim, AVR sinama) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS07 | Smash day dönüşü | B25 | I | EVET: 313 / +0,9 / %43-%43 / boot [-3,4, +5,6] / güç 0,63 / 0,50 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80: ABD sinama, AVR egitim, AVR sinama) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS08 | Weinstein evresi / ortalama eğimi | B10, B9 | I | EVET: 3224 / +0,5 / %42-%43 / boot [-2,4, +3,9] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS09 | RSI(2) aşırı satım | B1, B4 | I | EVET: 2122 / +0,9 / %48-%50 / boot [-1,3, +3,1] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS10 | DV2 aşırı satım | B2 | I | EVET: 2245 / -1,6 / %50-%50 / boot [-3,9, +0,4] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS11 | Kapanış 7 gün dibinde (Double 7) / H2 düşen bıçak | B3 | I | EVET: 4342 / +0,4 / %49-%51 / boot [-1,8, +2,5] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR; plasebo kapısı düşen: ABD egitim, AVR egitim, AVR sinama) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS12 | Elder Impulse kırmızıdan çıkış | B8 | I | EVET: 725 / -0,7 / %41-%42 / boot [-3,7, +2,4] / güç 0,96 / 0,83 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80: AVR sinama) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS13 | TD Sequential setup 9 / countdown 13 | B5, B6 | I | EVET: 213 / +2,2 / %46-%52 / boot [-3,9, +9,3] / güç 0,50 / 0,36 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80: ABD egitim, ABD sinama, AVR egitim, AVR sinama) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS14 | Düşüş direnci kırılımı (CHoCH / TDST / trend çizgisi) | C5, B7, B19 | I | EVET: 38 / +17,6 / %21-%38 / boot [+3,4, +33,5] / güç 0,16 / 0,10 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80: ABD egitim, ABD sinama, AVR egitim, AVR sinama) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS15 | Busted aşağı kırılım | B23 | I | EVET: 0 / - / --- / boot [-, -] / güç 0,03 / 0,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80: ABD egitim, ABD sinama, AVR egitim, AVR sinama) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS16 | Wyckoff ikinci test | B13 | I | EVET: 1229 / -0,8 / %42-%44 / boot [-3,5, +1,7] / güç 0,98 / 0,99 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (1 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS17 | Aşağı gün direnci (asimetrik göreli güç) | B17 | I | EVET: 2289 / -4,0 / %44-%44 / boot [-6,9, -1,1] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS18 | Göreli güç eğimi / göreli dip uyumsuzluğu | C17, C18 | I | EVET: 1732 / -1,6 / %42-%40 / boot [-4,5, +1,2] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS19 | Bollinger %b W dip | B27 | I | EVET: 706 / -2,9 / %46-%43 / boot [-6,4, +0,6] / güç 0,96 / 0,87 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80: AVR sinama) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS20 | Alt bantta yürüme (−) | B28 | I | EVET: 2194 / +2,4 / %44-%48 / boot [+0,3, +4,8] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS21 | Düşüşte gece payı (−) | B34 | I | EVET: 1668 / +0,2 / %40-%41 / boot [-3,4, +3,4] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS22 | Aşağı boşluk / dengesizlik doldurma | C11, C4 | I | EVET: 98 / +5,9 / %35-%38 / boot [-2,5, +13,8] / güç 0,22 / 0,19 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80: ABD egitim, ABD sinama, AVR egitim, AVR sinama) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS23 | Yukarıda mıknatıs (dolmamış boşluk / eşit tepeler +%5..+%10) | C12, C13 | I | EVET: 1811 / -0,1 / %44-%45 / boot [-1,9, +1,5] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS24 | Yukarı FVG (3 bar itki) | C3 | I | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS25 | AVWAP (dipten çapalı test / tepeden çapalı geri alma) | C8, C9 | I | EVET: 1724 / +2,2 / %39-%40 / boot [+0,6, +3,9] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (0 / 4 karar hücresi beklenen yönde TUTAR) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS26 | POC süpürme + geri alma | C10 | I | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS27 | 50 gün ortalamadan ATR katı gerilme | C14 | I | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS28 | Düşüş derinliği | C23 (+ A1 derinlik kolu) | I | EVET: 1577 / +1,0 / %44-%43 / boot [-1,4, +3,8] / güç 1,00 / 1,00 | ÖLÇÜLEMEDİ (h5) → Ç204 R15: SORGULA (1 / 4 karar hücresi beklenen yönde TUTAR; plasebo kapısı düşen: ABD egitim) | A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz | EVET: sayısal, ds_esik.json sabit |
| DS29 | P&F hedef / alt direk dönüşü | B20, B32 | I (öncelik dışı, H15) | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS30 | 52 hafta dibi yakınlığı | A10 | ELENDİ (g) | HAYIR | SINANMADI | E | HAYIR: ELENDİ (g) |
| DS31 | Dipten 18 barda yarı geri alma hızı | C7 | ELENDİ (g, boş küme) | HAYIR | SINANMADI | E | HAYIR: ELENDİ (g, boş küme) |
| DS32 | Boyut × düşüş (büyük mü küçük mü) | C22 (+ A1 küçük kolu) | ELENDİ (kova ile sıfırlanır) | HAYIR | SINANMADI | E | HAYIR: ELENDİ (kova ile sıfırlanır) |
| DS33 | Order block geri dönüşü | C6 | ELENDİ (tanım yok) | HAYIR | SINANMADI | E | HAYIR: ELENDİ (tanım yok) |
| DS34 | Beklenen kazanç ≥ 3 x zarar | B18 | ELENDİ (g) | HAYIR | SINANMADI | E | HAYIR: ELENDİ (g) |
| DS35 | Yükseliş / düşüş günü hacim oranı | B16 | KAPALI | HAYIR | SINANMADI | E | HAYIR: KAPALI |
| DS36 | Piyasa geçmişte düşmüş (ayı) | A5 | KOŞUL | HAYIR | SINANMADI | E | HAYIR: KOŞUL |
| DS37 | Zweig genişlik hamlesi | B29 | KOŞUL | HAYIR | SINANMADI | E | HAYIR: KOŞUL |
| DS38 | Takip günü (FTD) | B30 | KOŞUL | HAYIR | SINANMADI | E | HAYIR: KOŞUL |
| DS39 | VIX yüksek | A6 | KAPALI | HAYIR | SINANMADI | E | HAYIR: KAPALI |
| DS40 | Evre 2 hacim patlaması / SOS + LPS | B11, B15 | KAPALI | HAYIR | SINANMADI | E | HAYIR: KAPALI |
| DS41 | Connors çıkışları / TD stop | B35, B36 | KAPALI | HAYIR | SINANMADI | E | HAYIR: KAPALI |
| DS42 | RSI7 zayıflıkta al vs onay | C21 | KAPALI | HAYIR | SINANMADI | E | HAYIR: KAPALI |
| DS43 | Darvas kutusu | B31 | bağlam dışı | HAYIR | SINANMADI | E | HAYIR: bağlam dışı |
| DS44 | Habersiz büyük düşüş döner, haberli sürer | A3, C19 | II | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS45 | Konveks yol × not düşürme | A15 | II | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS46 | Düşüş sonrası içeriden alım | A20, A21, D3 | II | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS47 | Zorunlu CEO değişimi + ilk bilanço kötü → V | D5 | II | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS48 | Form 144 satış niyeti | D13 | II | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS49 | Yeni pasif %5 ortak (13G) | D14 | II | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS50 | 8-K 2.03 yeni borç / kredi | D20 | II | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS51 | 8-K 2.04 borç hızlandırma (−) | D21 | II | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS52 | 8-K 1.02 sözleşme feshi (−) | D22 | II | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS53 | Ters bölünme / ortak hakları değişimi (3.03) | D7, D23 | II (KISMEN) | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS54 | 13G → 13D geçişi | D15 | ELENDİ (c) | HAYIR | SINANMADI | E | HAYIR: ELENDİ (c) |
| DS55 | Düşen bıçak × ucuz (EV/Satış) | A1 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS56 | Sıkıntı × kaybeden | A8, A25 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS57 | F-skoru × kaybeden | A17, B33, C24 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS58 | Açık piyasa geri alım programı duyurusu (+ BIST KAP) | A9, D1, D28 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS59 | Hızlandırılmış geri alım (ASR) (−) | D2 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS60 | Opsiyon dibi (plan dışı CEO tahsisi) | D4 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS61 | Going concern kalkması | D6 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS62 | 'Stratejik seçenekler' duyurusu (−) | D8 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS63 | Borç takas teklifi (duyuru − / tamamlanma +) | D9 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS64 | Açık pozisyon eğilimi ve kârla / zararla kapanış | D16, D17 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS65 | Önceden duyurulmuş yatırımcı günü | D18 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS66 | Hükûmet / savunma sözleşmesi | D19 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS67 | Temettü kesip yeniden başlatma | D24 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS68 | Dava uzlaşması | D26 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS69 | Nasdaq uyumu yeniden kazanma | D27 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS70 | S&P 500'den çıkarma | A22, D11 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS71 | Russell 1000 → 2000 göçü | D12 | III | HAYIR | SINANMADI | E | EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok) |
| DS72 | İflastan çıkan yeni hisse | D10 | ELENDİ (DS olayına girmez) | HAYIR | SINANMADI | E | HAYIR: ELENDİ (DS olayına girmez) |
| DS73 | Fon çıkışı zorunlu satış | A7, D25 | ELENDİ (d) | HAYIR | SINANMADI | E | HAYIR: ELENDİ (d) |
| DS74 | Not düşürme dalgası sonrası dönüş | A16 | ELENDİ (d) | HAYIR | SINANMADI | E | HAYIR: ELENDİ (d) |
| DS75 | 13F kurumsal artış | D37 | ELENDİ (a, d) | HAYIR | SINANMADI | E | HAYIR: ELENDİ (a, d) |
| DS76 | PDUFA öncesi koşu | D29 | MEVCUT (H3 / K51) | HAYIR | SINANMADI | E | HAYIR: MEVCUT (H3 / K51) |
| DS77 | Aktivist 13D | D30 | MEVCUT (ACT_13D) | HAYIR | SINANMADI | E | HAYIR: MEVCUT (ACT_13D) |
| DS78 | Analist yükseltme dalgası | D31 | MEVCUT (REC_UP) | HAYIR | SINANMADI | E | HAYIR: MEVCUT (REC_UP) |
| DS79 | ATM / raftan satış | D33 | MEVCUT (E_424B5) | HAYIR | SINANMADI | E | HAYIR: MEVCUT (E_424B5) |
| DS80 | Kayıtsız satış 3.02 | D34 | MEVCUT (E_302) | HAYIR | SINANMADI | E | HAYIR: MEVCUT (E_302) |
| DS81 | Endekse ekleme | D35 | MEVCUT (E_IDX_ADD) | HAYIR | SINANMADI | E | HAYIR: MEVCUT (E_IDX_ADD) |
| DS82 | Spin-off | D36 | MEVCUT (E_SPINOFF) | HAYIR | SINANMADI | E | HAYIR: MEVCUT (E_SPINOFF) |
| DS83 | Öngörü yükseltme | D32 | VERİ YOK (GUIDANCE_UP) | HAYIR | SINANMADI | E | HAYIR: VERİ YOK (GUIDANCE_UP) |
| DS84 | Google arama ilgisi | A23 | VERİ YOK | HAYIR | SINANMADI | E | HAYIR: VERİ YOK |
| DS85 | Opsiyon IV çarpıklığı | A24 | VERİ YOK | HAYIR | SINANMADI | E | HAYIR: VERİ YOK |
| DS86 | Reddit anılma + hacim | C20 | VERİ YOK | HAYIR | SINANMADI | E | HAYIR: VERİ YOK |
| DS87 | Birleşme söylentisi | D38 | VERİ YOK | HAYIR | SINANMADI | E | HAYIR: VERİ YOK |

### 2d. SINYAL_ENVANTERI satırları (120 satır; yukarıdaki 84 sinyal K60'ta ölçüldü) K60 tablosunda adı geçmeyenler (ad eşleşmesiyle; K60 farklı kod kullanmış olabilir) → 51 satır, SINANMADI (E)

(Not: envanterde 120 satır ayrıştırıldı; 4 satır "YOK" = ücretsiz veriyle hesaplanamaz. Bu satırlar ölçülmedi; kayıtta hangi nedenle K60'a girmediği ayrıca yazılı değil: "kayıtta yok".)

| kod | aile | tanım (kısa) | yön | bizde var mı | KASA ADAYI |
|---|---|---|---|---|---|
| MOM_RES_12_1 | MOM | 36 aylık FF3 regresyon artıklarının t−12..t−2 toplamı / artık std | + | EVET | EVET: fiyat / SEC özütü elde, tanım sayısal |
| NDF | INV | (borç ihracı − borç geri ödeme) / ortalama varlık | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| INV_A | INV | (maddi duran varlık + stok) değişimi / önceki yıl varlık | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| INVTRY_G | INV | stok yıllık büyümesi / varlık | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| HIRE_G | INV | çalışan sayısı yıllık büyümesi | − | YOK | HAYIR: veri YOK |
| SUE_ANALYST | EAR | (gerçekleşen − beklenti) / beklenti büyüklüğü | + | EVET (2022-12+) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| REC_UP | EAR | son 20 işlem gününde not yükseltme sayısı | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| REC_DOWN | EAR | son 20 işlem gününde not düşürme sayısı | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| PT_REV | EAR | hedef fiyat revizyonu (yeni / eski − 1), son 20 gün ortalaması | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| N_ANALYST_CHG | EAR | 12 ayda not veren kurum sayısının değişimi | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| EPS_REV | EAR | konsensüs EPS tahmin revizyonu | + | YOK | HAYIR: veri YOK |
| GUIDANCE_UP | EAR | yönetim beklenti yükseltmesi | + | YOK | HAYIR: veri YOK |
| INS_BUY_90 | OWN | son 90 günde yönetici / yönetim kurulu açık piyasa alımı (Form 4 kod P): alıcı sayısı ve net değer / piyasa d… | + | EVET (k30_alim) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| INS_CLUSTER | OWN | 30 günde ≥ 3 farklı alıcı | + | EVET (k30_alim) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| INS_OPP_BUY | OWN | "rutin olmayan" alım: kişi son 3 yılda aynı ayda işlem yapmamış | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| INS_SELL_90 | OWN | son 90 günde açık piyasa satışı (kod S, 10b5-1 hariç) ≥ 100 bin $ | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| INS_OPP_SELL | OWN | rutin olmayan satış | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| IO_BREADTH_CHG | OWN | hisseyi tutan 13F kurumu sayısının çeyreklik değişimi / toplam kurum | + | İNDİR (zor) | HAYIR (şimdilik): İNDİR gerekir |
| IO_CHG | OWN | kurumsal sahiplik payının çeyreklik değişimi | + | İNDİR (zor) | HAYIR (şimdilik): İNDİR gerekir |
| SI_RATIO | OWN | açığa satış pozisyonu / pay sayısı | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| DTC | OWN | açığa satış pozisyonu / ortalama günlük hacim | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| SI_LOW | OWN | likit hisselerde en düşük açığa satış onluğu | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| SHORT_VOL | OWN | borsa dışı açığa satış hacmi / toplam hacim, 5 gün ortalaması | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| EA_MONTH | SEA | bu ay bilanço açıklaması bekleniyor (geçen yıl aynı ay açıklamış) | + | EVET | EVET: fiyat / SEC özütü elde, tanım sayısal |
| TAXLOSS_JAN | SEA | 12 ayın en çok düşen onluğu, yalnız ocak ayı | + | EVET | EVET: fiyat / SEC özütü elde, tanım sayısal |
| DIV_MONTH | SEA | bu ay temettü bekleniyor (3 / 6 / 12 ay önce ödemiş) | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| Z_SCORE | DIS | Altman (1968) Z; düşük Z | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| GC_FLAG | DIS | son 10-K / 10-Q'da "substantial doubt ... going concern" | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| E_101 | EVT | son 20 işlem gününde 8-K madde 1.01 (önemli sözleşme) | ? | EVET (sec_ozet) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| E_201 | EVT | son 60 günde 8-K 2.01 (devralma tamamlandı; alıcı taraf) | − | EVET (sec_ozet) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| E_205_206 | EVT | son 60 günde 8-K 2.05 / 2.06 (yeniden yapılanma / değer düşüklüğü) | ? | EVET (sec_ozet) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| E_301 | EVT | son 120 günde 8-K 3.01 (kottan çıkarma uyarısı) | − | EVET (sec_ozet) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| E_302 | EVT | son 60 günde 8-K 3.02 (kayıtsız hisse satışı) | − | EVET (sec_ozet) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| E_401 | EVT | son 120 günde 8-K 4.01 (denetçi değişimi) | − | EVET (sec_ozet) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| E_402 | EVT | son 120 günde 8-K 4.02 (eski tablolara güvenilmez) | − | EVET (sec_ozet) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| E_502 | EVT | son 60 günde 8-K 5.02 (yönetici ayrılışı / ataması) | ? | EVET (sec_ozet) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| E_LOCKUP | EVT | halka arz + 180 gün çevresi (−10..+10 gün) | − | EVET (sec_ozet) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| E_MA_TARGET | EVT | hedef şirket: DEFM14A / SC 14D9 / SC TO-T sonrası, kapanışa kadar | + (küçük) | EVET (sec_ozet) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| E_TENDER_SELF | EVT | son 90 günde SC TO-I (şirketin kendi hisselerine çağrısı) | + | EVET (sec_ozet) | EVET: fiyat / SEC özütü elde, tanım sayısal |
| E_SPLIT | EVT | son 12 ayda ileri bölünme (≥ 2:1) | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| E_IDX_ADD | EVT | son 20 günde S&P 500'e ekleme duyurusu | + (sönmüş) | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| E_SPINOFF | EVT | ayrılma (10-12B) sonrası ilk 24 ay, ayrılan şirket | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| E_DIV_INIT | EVT | son 12 ayda ilk temettü | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| COMM_LINK | SEC | sektörün emtia duyarlılığı (36 ay regresyon) × emtianın geçen ay getirisi | ? | EVET | EVET: fiyat / SEC özütü elde, tanım sayısal |
| IO_MOM_CUST | SEC | müşteri sektörlerinin geçen ay getirisi (BEA girdi-çıktı ağırlıklı) | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| IO_MOM_SUPP | SEC | tedarikçi sektörlerinin geçen ay getirisi | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| GEO_MOM | SEC | aynı kentte (eyalette) merkezli, başka sektördeki şirketlerin geçen ay getirisi | + | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| CUST_MOM | SEC | şirketin adı açıklanan büyük müşterilerinin geçen ay getirisi | + | YOK | HAYIR: veri YOK |
| LAZY_SIM | TXT | bu yılın 10-K'sı ile geçen yılınki arasındaki benzerlik (kosinüs / Jaccard); düşük benzerlik = çok değişiklik | + (benzerlik yüksekse) | İNDİR (ağır) | HAYIR (şimdilik): İNDİR gerekir |
| TONE_NEG | TXT | 10-K'da Loughran-McDonald olumsuz sözcük payı | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |
| TONE_CHG | TXT | olumsuz + belirsizlik + dava sözcük payının yıllık değişimi | − | İNDİR | HAYIR (şimdilik): İNDİR gerekir |

## 3. CEMAL'İN KURALLARI TABLOSU

Kaynak: KURAL_DEFTERI_TASLAK.md (A-J: 140 kural, K1-K51: 51 kural; taslak, ana model işler), GOZ_ETIKET_IS_TANIMI (C1-C13), HAKEM_DERSLER (CD / VD). Güvenilirlik harfi bu tabloda: A = güç yeterli ve cetvel sorunsuz TUTTU / TUTMADI; B = ölçülemedi / n küçük (K58); C = 15 bar h5 ya da vekil cetveli; E = hiç ölçülmedi. "Kodda" sütunu kural defterinden alındı.

### 3a. K1-K51 (kural defteri bölüm K: kör set 2 dersleri, YAPI_HEDEF değerlendirmesi, hakem / TUR dersleri, Ekim eşleri)

| kural | düz dil | sayısal tanım (F / Ş kodu) | şimdiye kadarki ölçüm (Ç, cetvel, sonuç) | GÜV | kasa adayı |
|---|---|---|---|---|---|
| K1 | Formasyon hedefi küçük (+%5..+%10); 60 gün ölçüsü bunu ölçmez; hedef sonrası yeni yapı belirler | cetvel kuralı (h5 / r15) | Hayır: SINANMADI | E | HAYIR: ölçüt (cetvel kuralı) |
| K2 | Düz taban = yukarı formasyon (hedef önceki tepe), düz tavan = aşağı formasyon (hedef önceki dip) | YOK (S6 ayna sürümü) | Hayır: SINANMADI | E | EVET → KK06 |
| K3 | Kubbe kuralı: şemsiye aşağı, kazan (çanak) yukarı | Ş9 (a > 0) yakın | Hayır: SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K4 | Çanağın yukarı dönüşü görülmeden giriş yok | FITIL_V2 s4 (ters) | Hayır (kör set 2 dolaylı): SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K5 | Taban kapanışla kırıldıysa o mumların hükmü yok; karantina | FITIL_V2 s2 kısmen | Hayır: SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K6 | Tutmayan dip (alçalan dipler zinciri) = güven yok | FITIL_V2 s2 kısmen | Hayır: SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K7 | Küçücük yapı güven vermez; yapı boyu düşüş bacağıyla orantılı | S6 nMin sabit | Hayır: SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K8 | Kağıt hafızası: önceki formasyonlar hedefe gittiyse güven artar, patladıysa biter | YOK | Hayır: SINANMADI | E | EVET → KK07 |
| K9 | SAT mumu: düz tavandan kopan ilk büyük kırmızı mum | YOK | Hayır: SINANMADI | E | EVET → KK06 |
| K10 | Çekiştirme (uçurum kenarında zayıf yukarı çeken el) = BELİRSİZ, bekle; REEDR örneği | YOK | Hayır: SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K11 | Oluşum yoksa yön önceki yoldur; kod 'yapı yok' diyebilmeli | YOK | Hayır: SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K12 | Geçmişte dev tek mum (fitil > +%100) varsa kağıt şüpheli (kripto gibi) | YOK | Hayır: SINANMADI | E | EVET → KK05 |
| K13 | Üç kez tepen taban: üçüncü sekmede girilebilir ama Cemal'in yapısı değil | YOK | Hayır: SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K14 | Geri test hedefi büyütür (asıl giriş retest; iki kutu 2. giriş) | COL_v1 yorum | Hayır: SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K15 | UFUK 15 MUM: kodun gördüğü yapılar en fazla 15 mumun geleceğini gösterir; 60 gün ölçüsünde rolleri yok. Eski 20-60 mumlu büyük çöller fon iziydi; gerçek hissed… | ORTAK_CETVEL ufuk 15 | Hayır: SINANMADI | E | HAYIR: ölçüt (ufuk 15; cetvele girer) |
| K16 | Büyük çöl (TEHOL / BINBN / KETLV, 20-60 mum, çok katlı hedef) gerçekti ama yalnız fon gibi satmayan alıcı grupları girince oluşur (manipülasyon); o dönem kapan… | FON_IZI K12 | Dolaylı (K12 FON_IZI fon lekesi; Ç147 kripto): SINANMADI | E | HAYIR: tez; büyük çöl aranmaz (kapalı) |
| K17 | SON DERS: fon çöllerinden öğrenilen kurallar gerçek ve bugün geçerli (alt fitili az mumlar + dip savunması = yukarı, tersi aşağı) ama etkisi kısa; hedef %5-10… | FITIL_V2 s1 | Hayır (15 bar / %5-10 ölçüsüyle hiç ölçülmedi): SINANMADI | E | HAYIR: tez / ders; K30 ve KK01-KK04 içinde |
| K18 | YENİ TEST STANDARDI: giriş = dip tavanı / taban kırılım mumu; hedef +%5 / +%10 = 'ulaştı'; takip stopu yukarı revize, yeni ters oluşuma kadar; ilk hedefte stop… | cetvel | Hayır: SINANMADI | E | HAYIR: ölçüt (test standardı) |
| K19 | Büyük desen önce: küçük kutu 120-250 barlık büyük yapının içindeyse karar büyük yapıya göre; alçalan büyük kanalda küçük taban girilmez; stop büyük dip | Y6 / F-büyük desen | Hayır: SINANMADI | E | EVET → KK16 |
| K20 | Hat net olmalı: >= 3 dokunuş, eğimi aşağı değil; 1-2 mumluk hat hat değil | Y6 F1 (hat dokunuş) | Hayır: SINANMADI | E | EVET → KK16 |
| K21 | Giriş mumu gerçek kırılım: kapanış tavanı ancak dokunuyorsa giriş yok (pay + gövde) | Y6 gerçek kırılım | Hayır: SINANMADI | E | EVET → KK16 |
| K22 | Kazan şemsiye değil: simetrik çanak + dipte küçük mum + dip savunması; a > 0 uyumu yetmez | Ş9 / Y3 | Hayır: SINANMADI | E | EVET sonra (Ş9; kart yok, Ç195 n 1-20) |
| K23 | Stop uzaklığı: giriş-hat > %10 ise işlem yok ya da ana stop %5; stop büyük desenin dibi | Y6 stop ≤ %10 | Hayır: SINANMADI | E | EVET → KK16 |
| K24 | Hedef önceki tepe; tepede ters formasyon oluşunca çık | YOK | Hayır: SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K25 | Kağıt hafızası Cemal tanımı: aynı hissede benzer yapı patladıysa girilmez (S6 AL sayımı değil) | Y4 / Y8 | Y4 benzeri ölçüldü (farklı tanım): SINANMADI | E | EVET → KK07 |
| K26 | Dip savunması şart: küçük mumlu sıkışma tek başına yetmez | Y6 | Hayır: SINANMADI | E | EVET → KK16 |
| K27 | Zayıf hat = +%5 hedef; yeniden hat oluşursa yeniden girilir | YOK | Hayır: SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K28 | Patlamış yapı / 10 barlık küçük bölge = yapılacak şey yok (Y5 nMin 15) | Y5 nMin | Hayır: SINANMADI | E | EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok) |
| K29 | Tavan = ilk dip yapısının tavanı; rastgele tavan hattı çizilmez | S6 pencere | Hayır: SINANMADI | E | EVET → KK06 içinde (tavan tanımı) |
| K30 | Fitil teorisi: üst fitiller uzamışsa yukarıdaki satıcı emiliyor (aşağı beklenmez); altta alıcı yoksa uzun alt fitil oluşur; fitilsiz kısım yukarıdaysa yön tersi | FITIL_OBEK ASİM | Hayır: SINANMADI | E | EVET → KK01 |
| K31 | Giriş teyidi: kırılım mumu gün sonu kapanışla + ertesi gün kalıcılık (iki gün tavan üstünde kapanış); tek mumla girilmez | COL_v1 AL tek kapanış | Hayır (kapalı konu 'giriş onayı' ile çakışır): SINANMADI | E | HAYIR: kapalı konu (giriş onayı); Cemal kararı |
| K32 | Parmak izi: büyük yeşil alış mumundan hemen önceki 4 mum dibe yakın, alt fitili kısa öbek | FITIL_OBEK k 10 | Kısmen (Ç187 S+ öbeği, k 10 bar): ÖLÇÜLEMEDİ | B | EVET → KK01 ile birleşir |
| K33 | Kazan çizimi = OLUR, şemsiye çizimi = OLMAZ; Cemal kör yarıda 19 sayfanın 8'ine OLUR dedi (vekil 300'de 6): vekil göz Cemal'in gözü değil (kappa -0,13) | GOZ_ETIKET etiket.json | Evet (hakem, n 19): TUTMADI (uyum) | C | HAYIR: vekil göz / kör set |
| K34 | CD1-CD7 Cemal'in hakem dersleri: fitil teorisi bağlamsız yön vermez; tepede raf OLMAZ / BELİRSİZ; kazan yetmez dönüş görülmeli; en güzel taban stop olabilir (ş… | YOK | Evet (n 40, bilgi): SINANMADI | E | HAYIR: hakem dersi, 100 sayfalık set bekler |
| K35 | VD1-VD4 vekil / ana model dersleri: kural toplamı göz değil; stop %10 ve kırılım payı süzgeçleri hedefe gidenleri eliyor; 'kararsız' grup en iyi grup; önce hak… | GOZ_ETIKET C11 / C5 (vekil kuralı) | Evet (n 40, bilgi): TUTMADI (vekil) | C + D | HAYIR: vekil dersi (bırakıldı) |
| K36 | CD8 / CD9 (TUR 1): 'kodun bölgesi yanlış' ile 'fiyat gitmez' ayrı hükümler; şemsiye çizimi tek başına OLMAZ değil | YOK | Evet (n 30, bilgi): SINANMADI | E | HAYIR: tek tur dersi |
| K37 | VD6-VD8 (TUR 1): dipte kazan OLUR için dönüş + gövdeli kırılım; tepe rafı iki tür (dağıtım / yükselen trend rafı); kırılım mumu tavanı ortalamalı (Cemal s2) | TUR 2 model kuralı; YAPI_HEDEF Y1c adayı | Evet (n 30, bilgi): SINANMADI | E | HAYIR: tek tur dersi |
| K38 | CD13 / CD14 (TUR 2): büyük kırılım mumu tek başına eleme nedeni değil; alçalan büyük resimde kazan ✓ üçüncü kez yanılttı; kararsızlık fırsat kaybı | YOK | Evet (n 30, bilgi): SINANMADI | E | HAYIR: tek tur dersi |
| K39 | VD9 (TUR 2): gevşetilen kurallarla model OLUR'u 21'e çıktı, isabet %48 = taban; OLUR için üç şart birlikte (dönüş + gövdeli ortalayan kırılım + yükselen / yata… | TUR 3 model kuralı | Evet (n 30, bilgi): SINANMADI | E | HAYIR: tek tur dersi |
| K40 | U DİP + PARABOLİK DEVAM (19 Kas, S7 PDF No 38): seçilen sıkışma bölgesi U dip çizmeli, sağ kenarı parabolik kalkmalı; alçalan dipler zincirindeki durak (daha d… | Ş9 (Y11) | Evet (mekanik Ş9, Y11): SINANMADI | E | EVET sonra (Ş9) |
| K41 | CD15 (TUR 4): kod iki adaydan kötüsünü seçmişse (önceki dip savunması / kazan daha net) hedef gelmez; mahkeme 'ÖNCEKİ BÖLGE DAHA UYGUN' = OLMAZ | mahkeme | Evet (mahkeme): SINANMADI | E | HAYIR: tek tur dersi (mahkeme) |
| K42 | CD16 (TUR 4; Cemal düzeltmesi 19 Kas): 'zaman / haber ister' = DOSYA GEREKLİ sınıfı (geçmiş, hikâye, sektör bakılmadan karar yok); kör sette ölçülemez, puana g… | - | Hayır (dosya bilgisi kör sette yok): SINANMAZ (kör) | - | HAYIR: dosya bilgisi kör sette yok |
| K43 | CD17 (TUR 4): önceki toparlanma sert / hızlıysa bu da hızlı olur | - | Evet (C8 kağıt hafızası): SINANMADI | E | HAYIR: tek tur dersi |
| K44 | CD20 (TUR 4): hat x 0,98 stopu U dip havuzunda dar; OLUR'ların 4 / 9 yanlışı stop (s5 sonra +%86) | - | Evet: SINANMADI | E | HAYIR: tek tur dersi |
| K45 | CD21 (TUR 4): 'önceki kazan bitmedi / ikinci kazan daha derin / satıcı bitmedi' OLMAZ gerekçeleri 4 / 4 yanılttı; derin ikinci dip tek başına eleme değil | - | Evet: SINANMADI (ters emare) | E | HAYIR: tek tur dersi |
| K46 | VD10 (TUR 4, model): 'büyük resim yükselen' şartı düşüş sonrası dip havuzuyla çelişir; dipte havuzda uygulanmaz; OLUR = dönüş + gövdeli ortalayan kırılım; elem… | TUR 5 model kuralı | Evet: SINANMADI | E | HAYIR: tek tur dersi |
| K47 | MACD POZİTİF UYUMSUZLUK (Cemal, 20 Kas; ekran görüntüsü: Haziran-Ağustos 2026 iki dip): fiyat aynı / daha derin dip yaparken MACD (12, 26, 9) daha yukarıda dip… | Ş10 / F65-F68 | Evet (F65-F68, YAPI_HEDEF 8. tur): SINANMADI | E | HAYIR (Ç204): Ş10 R15'te etki yok; kart düştü |
| K48 | ÇİFT KAZAN (Cemal, 20 Kas, ALKT): dipler kazan + tepeler şemsiye = mantar / mercek (ortası bombeli) = sıkıntı; doğru taban hem dipler hem tepeler kazan | Ş11 / F69 a_high | Evet (F69 a_high; Ş11): SINANMADI | E | EVET sonra: Ş11 eşiği yok |
| K49 | H1 bilanço penceresi = kuyruk büyüteci (yön değil): giriş-15. bar arasında bilanço olan olaylarda hem en iyi hem en kötü sonuç (Ekim eşleri: kazanan 20 / 20, k… | BIL15 | Evet (BIL15; duyuru <= t): SINANMADI | E | EVET → KK25 |
| K50 | H2 düşen bıçak: 120 günün tam dibine son 5 günde düşerek gelen hisse (F15 <= 0,05 ve r5 <= −%3) kaybeder; 'dip savunulmadan giriş yok' (C2 / TUR 4 s7 destek; C… | F15 ≤ 0,05 ve r5 ≤ −%3 | Evet: SINANMADI | E | EVET → KK04 |
| K51 | H3 önceden bilinen katalizör (FDA / birleşme tarihi t+5..t+40, t'de kamuya açık) öncesi koşu; çöl tanımındaki 'katalizör olmadan çöl aranmaz' ile uyumlu | katalizör takvimi (veri gerekir) | Kısmen (katalizör takvimi verisi gerekir): SINANMADI | E | HAYIR: katalizör takvimi verisi yok |

### 3b. C1-C13 (Cemal'in göz kuralları; vekil göz bunlarla etiketledi, GOZ_ETIKET)

| kural | düz dil | sayısal tanım | ölçüm | GÜV |
|---|---|---|---|---|
| C1 | Taban net: hat ≥ 3 dokunuş, aynı seviye, eğim aşağı değil; 1-2 mumluk hat = OLMAZ | F1 (hat dokunuş), Y6 / Ş2 | Ç191 (Y6 / Y8, 15 bar h5): ölçülemedi, yön aleyhte (KAT5 0,59-0,90) | B + C |
| C2 | Dip savunulmuş: alçalan dipler zinciri yok | S6 dip şartı, F15, Y9, Y11 | Ç193 (Y9): ölçülemedi; bakılmış ABD KAT5 1,15 / 1,21 | B + C |
| C3 | Mumlar küçük (fitil dahil, öncesine göre) | MUM_OLCU aralik; S5 / S4 eşikleri | Ç174 (S1) İZ DEĞİL güç yeterli; Ç183 ölçülemedi; Ç184 EMARE | A (S1) / B |
| C4 | Mum şekli: alt fitil kısa, açılış dibe yakın, üst fitil biraz uzun | FITIL_OBEK ASİM ≥ 0,20, fitilsiz payı ≥ 0,50, k = 10 | Ç187: ölçülemedi (2024-26 TUTMADI); Ç189 | B |
| C5 | Kırılım mumu belirgin (kapanış tavanı net aşmış, gövdeli) | Y6 gerçek kırılım: kapanış > tavan × 1,01 ve gövde ≥ bölge medyanı | Ç191: ölçülemedi | B + C |
| C6 | Büyük desen: 120-250 bar alçalan kanal ise küçük taban OLMAZ | Y6 büyük desen şartı | Ç191: ölçülemedi; vekil etiket VD2 / VD3 | B + C |
| C7 | Yapı boyu düşüşe göre yeterli | S6 nMin, FITIL_V2 10 bar sabit | ölçülmedi (K7) | E |
| C8 | Kağıt hafızası: önceki yapı patladıysa OLMAZ | Y4 / Y8 (farklı tanım) | Ç190: Y4 Y1'i iyileştirmiyor (AVR aleyhte) | B + C |
| C9 | Kubbe: kazan OLUR, şemsiye OLMAZ; dönüş görülmeden BELİRSİZ | Ş9 U dip (a > 0, çanak, R²) | Ç195: Y11 n 1-20 ölçülemedi; Y11c KAT5 ~1 | B + C |
| C10 | Yol almış: tabandan uzaklaşmışsa kovalama yok | FITIL_V2 yol şartı | Ç189 içinde (ölçülemedi) | B |
| C11 | Stop uzaklığı: kapanış hattan %10'dan uzaksa işlem yok | stop0 = hat × 0,98; Y1 stop ≤ %10 | vekil etiket: hedefe gidenleri eliyor (VD2); ölçüt dar stop sorunu CD20 | D (vekil dersi) |
| C12 | Çekiştirme / oluşum yok = BELİRSİZ | - | sinyal değil etiket | E |
| C13 | Dev tek mum / şüphe: geçmişte dev mum = riskli | K12 / J4 (kodda YOK) | ölçülmedi | E |

### 3c. CD / VD dersleri (HAKEM_DERSLER; hepsi SINANMADI ya da tek tur n küçük)

| ders | düz dil | sayısal karşılık | ölçüm | GÜV |
|---|---|---|---|---|
| CD1 | Fitil teorisi bağlamsız yön vermez | HAKEM: iki sayfada iki yönde yanıldı | SINANMADI | E |
| CD2 | Tepede raf OLMAZ / BELİRSİZ | Y9c (tepede) ters | Ç193 (Y9c) ölçülemedi | B + C |
| CD3 | Kazan çizmek yetmez; sağ kenar dönmeli | Ş9 / C9 | Ç195 ölçülemedi | B + C |
| CD5 | En güzel taban stop olabilir (şekil güzelliği garanti değil) | Ş9 R² uyumu | CD23: R² 0,9+ gitti 3, stop 4 / 7 | SINANMADI |
| CD6 / CD7 | Eleme ve teyit refleksleri karışık: tavana değiyor elemesi yanılttı, iki gün teyit korudu | AL_PAY, 2 gün teyit (kapalı konu 'giriş onayı') | SINANMADI | E / KAPALI |
| CD8 / CD9 | Kodun bölgesi yanlış ile fiyat gitmez ayrı hükümler | - | SINANMADI (süreç) | E |
| CD15 | Kod iki aday bölgeden kötüsünü seçmişse OLMAZ (mahkeme: ÖNCEKİ BÖLGE DAHA UYGUN) | mahkeme kuralı (TUR 4) | SINANMADI; TUR 4: 5 / 5 gelmedi | E |
| CD16 | 'Zaman / haber ister' = DOSYA GEREKLİ (kör sette ölçülemez) | dosya bilgisi (K57) | puana girmez | E |
| CD17 | Önceki toparlanma sert / hızlıysa bu da hızlı olur (C8) | önceki yükseliş hızı | TUR 4: 2 / 4 | SINANMADI |
| CD20 | Hat × 0,98 stopu U dip havuzunda dar | stop eşiği | TUR 4: 4 / 9 yanlış stop; Ç203: ARRY, JBLU, CAPR (ikinci bağımsız olay) | C |
| CD21 | 'Önceki kazan bitmedi / ikinci kazan daha derin' OLMAZ gerekçeleri 4 / 4 yanılttı | - | TUR 4 ters emare | SINANMADI |
| CD22 | Sert düşüş sonrası hemen toparlanma beklenmez tezi 3 / 3 ters | dd ≤ −%50 | TUR 6 | SINANMADI |
| CD23 | Çanak uyumu iyi (R² 0,9+) tek başına ayırmadı | Ş9 R² | TUR 6: İYİ 13 sayfanın 6'sı gitti (%46 = taban) | SINANMADI |
| VD1 | Kuralların toplamı Cemal'in gözü değil (OLUR 6 sayfanın hiçbiri gitmedi) | GOZ_ETIKET C1-C13 toplamı | Ç192: vekil OLUR 6 / 300 | C + D |
| VD2 | Stop %10 ve kırılım payı süzgeçleri hedefe gidenleri eliyor | C11, C5 | Ç192; Ç191 | C + D |
| VD3 | Vekilin BELİRSİZ grubu en iyi grup | - | TUR 1-2 | SINANMADI |
| VD4 | Önce hakem sonra eğitim | süreç | Ç192 hata satırı | süreç |
| VD6-VD8 | Dipte kazan OLUR için dönüş + gövdeli kırılım; tepe rafı iki tür | TUR 2 model kuralı | SINANMADI | E |
| VD9 / VD10 | OLUR için iki şart (dönüş + gövdeli ortalayan kırılım); büyük resim yükselen şartı dipte uygulanmaz | TUR 3-5 model kuralı | TUR 2: model OLUR isabeti %48 = taban | SINANMADI |
| VD11 | TUR 6 modeli 'hep OLMAZ' ile aynı (%52,5) | - | TUR 6 | SINANMADI |

### 3d. A-J grupları (kural defteri; 140 kural, ayrıntı ve durumlar orada; burada yalnız sonuç sayımı)

Sonuç sayımı: SINANMADI 52 · TUTMADI 40 · ÖLÇÜLEMEDİ 17 · TUTTU 17 · TUTMADI* 11 · EMARE 3.

| no | kural (kısa) | sonuç | kodda | durum |
|---|---|---|---|---|
| A1 | Çöl, düşüş sonrası dipte aylarca süren sıkışmadır; dip savunulur, mumlar küçüktür | ÖLÇÜLEMEDİ | COL_v1.col_dip2 (SEGMENT_MOD='dip2'); F… | İLERİ TEST Mart 2027 |
| A2 | Tepede oluşan sıkışma dağıtımdır, çöl değildir | SINANMADI | FITIL_V2.fv_kural s5 (120 gün tepesinin… | AÇIK (FITIL_V2 aşama 2) |
| A3 | Küçük mum = gövde değil, fitil dahil boy (H−L) | SINANMADI | COL_v1.MUM_OLCU='aralik' | KAPALI (tanım) |
| A4 | Tam desen üç evre: sıkışma → kırılım + yükselen SMA üstünde raf → bölgeye sert test, sonra hareket | ÖLÇÜLEMEDİ | FON_IZI.fi_k24_tara (2 evre); 3. evre Y… | İLERİ TEST Mart 2027 |
| A5 | 1. evre SMA20 altı, 2. evre SMA20 üstünde muntazam dizilme, delen yok | ÖLÇÜLEMEDİ | FON_IZI.fi_k24_tara; K24_YENIDEN | İLERİ TEST Mart 2027 |
| A6 | Bölge = tabanın TAMAMI (düşüş bitip dip savunulduğu yerden tavanı kıran al mumuna); 15 barlık parça değil (K1) | SINANMADI | S6_TABAN.s6_durum / s6_bolgeler | AÇIK |
| A7 | Bölge en az 8 mum (5 alt sınır), çoğu ~60'a kadar; tek mumluk bölge yok; bitişik parçalar tek bölge | SINANMADI | S6_TABAN.S6_PRM nMin 8, nMax 70 | KAPALI (tasarım) |
| A8 | Sınır mumlardan gelir; bant kısa bölgede %5-8, uzun tabanda %20'ye kadar (K2) | SINANMADI | S6_TABAN.S6_PRM bantMax 0,12 | AÇIK |
| A9 | Sakin bölge: ilk-son kapanış farkı küçük (aday ≤ %5); eğimli pencere çöl değil (K3) | TUTTU | S6_TABAN.S6_PRM netMax 0,03 | KAPALI (tasarım) |
| A10 | Düşüş sonrası; kayan düşüş kanalı çöl değil; dip korunur (K4) | SINANMADI | S6_TABAN dipTol 0,05, dipDusus -0,10 | AÇIK |
| A11 | Bollinger daralması bütün bölgelerde şart; öbek gibi yan yana küçük mumlar; zıplama mumu görmezden gelinir | EMARE | SIKISMA_OBEK.so_s5 (bb 0,20, k_m 0,75);… | İLERİ TEST Mart 2027 |
| A12 | Yükselişteki bölge dinlenme olmalı, taban korunmalı; dip bölgesi de sayılır | TUTMADI | SIKISMA_OBEK.so_s5 sınıf YOL | KAPALI |
| A13 | Küçük mum hissenin normalinden küçük; 0,75 x ATR250 bazen fazla sıkı (K5) | SINANMADI | S6_TABAN kM 0,90; SIKISMA_OBEK k_m 0,75 | AÇIK |
| A14 | Çöl aylarca sürebilir; giriş mumu aylar sonra gelebilir; ikinci çöl riskli (K7) | TUTMADI | COL_v1.uzun_col_olc (ölçüm referansı; T… | İLERİ TEST Mart 2027 |
| A15 | Çöl nadirdir; nadir çölün sağ ayağı rastgele hisseden iyi olmalı | TUTMADI | YOK | KAPALI |
| A16 | Kutu yeni dipten başlar; önceki raf / düşüş kutuya girmez | TUTMADI | COL_v1.col_dip2 (d = son 120 bar dibi) | AÇIK (üretimde, dayanağı düştü; Cemal kararı) |
| A17 | Dip savunması + parabolik yukarı yuvarlanma + küçük mum öbekleri birlikte; tespit işlemden ayrı | TUTMADI | COL_v1.col_dip2 (_d13_obekler, parabol… | AÇIK (üretimde) |
| A18 | Aşağı kırılıp toparlanıp giden çöller kaçmamalı (tespit daraltılmaz, bu çıkış işi) | SINANMADI | YOK | AÇIK |
| A19 | Dibi düzgün (haftalarca test edilen) taban; TEHOL 2024 düzgün, 2021 değil | ÖLÇÜLEMEDİ | FON_IZI FI_K13B_ESIK / fi_k16; DIP_COL_… | İLERİ TEST Mart 2027 |
| A20 | İki yuvarlama: önce aşağı yay (∩), hemen ardından kâse (∪) | ÖLÇÜLEMEDİ | FON_IZI k17 | AÇIK (yeniden koşu sırası, IK_ACIK) |
| A21 | Sıkışma = yatay + dar Bollinger; küçük mumlu ama kayan pencere sıkışma değil (FENER 14 Eki - 7 Kas doğru, 3-16 Ara yanl… | ÖLÇÜLEMEDİ | SIKISMA_CEMAL (SC_ESIK) | İLERİ TEST Mart 2027 |
| B1 | Giriş = tavanı kapanışla kıran al mumu; tavan kırılmadan alım yok (K6) | TUTMADI | COL_v1.AL_PAY 1,002 (bugun_liste); S6_T… | KAPALI (giriş zamanlaması kapalı konu) |
| B2 | Büyük çölün tavanı sivri tepe mumudur; o yatayı kapanışla kıran mum al mumudur; küçük tabanın kendi tepesi ayrı (K6b) | SINANMADI | S6_TABAN AL (tavan mumu ayrı şart değil) | AÇIK (S6 al mumu, başarısız kırılımla sınana… |
| B3 | İki kutu: ilk giriş 2. kutu oluştuktan sonraki hafif silkelemede; bölge testi yukarı dönerse ekleme | ÖLÇÜLEMEDİ | FON_IZI k17 Y6 (ölçüm); üretimde YOK | AÇIK |
| B4 | Kutu içindeki tepe aşılmıyorsa risk çok; alış mumu yoksa çöl mumları yeterli değil | TUTMADI | YOK | KAPALI |
| B5 | Öbekte hacim kurusun, alım mumu 2-3-4 kat hacimle gelsin | TUTMADI | YOK | KAPALI |
| B6 | Küçük alım mumu ve NVI / CMF kurumsal birikim ayrışması | TUTMADI | YOK | KAPALI |
| B7 | Dönüm mumu vs yön mumu: düşüşün son mumları 'son nokta' diyorsa dönüm (akümülasyon); yalnız yön gösteren mum sinyal değ… | SINANMADI | FITIL_V2.fv_kural s3 (60 bar tepesinden… | AÇIK (FITIL_V2 aşama 2) |
| B8 | Savunma hattı: şekil aynı olsa bile savunulan seviye kırılmışsa aşağı, kırılmamışsa yukarı (K10) | TUTMADI | FITIL_V2.fv_kural s2 (HAT = min Low, ha… | AÇIK (FITIL_V2 aşama 2) |
| B9 | Yol almış = kovalama yok (K11) | SINANMADI | FITIL_V2.fv_kural s4 (C ≤ HAT x 1,10) | AÇIK (FITIL_V2 aşama 2) |
| B10 | Akümülasyonda alıcının kurumsal olup olmadığı önemli; kim alıyor (K15) | SINANMADI | YOK | AÇIK (veri yok) |
| B11 | Sağ ayak: çölden çıkan hisse rastgele hisseden çok daha fazla yol almalı (MANAS 18 Tem - 8 Ağu 2025) | TUTMADI | YOK | KAPALI |
| B12 | 60 gün değil, bölgenin altı / üstü çıkışı; +%8 iz (INTEM) | ÖLÇÜLEMEDİ | FON_IZI k45; INTEM_ILERI.py | İLERİ TEST Mart 2027+ |
| B13 | Yükselişte alınca zarar az, dipte dönüş varsayımıyla alınca kötüleşti | TUTTU | YOK | KAPALI |
| B14 | Dipler aynı çizgide, dip kırılmazsa sert çıkar (S+DÜZ) | ÖLÇÜLEMEDİ | FITIL_KOR (SPD, SPDb satırları) | AÇIK (ileri test adayı) |
| B15 | Dipte %80-90 düşmüş, dip tutuyor, ucuz noktada BofA alımıyla gir | ÖLÇÜLEMEDİ | BOFA_IZI dipkos | İLERİ TEST Mart 2027 |
| C1 | Taban kırılınca çık (T6; YKSLN Temmuz stop, K8) | TUTMADI | takip.TABAN_TOL 0,02 (T6) | AÇIK (H23: üretim testle çelişiyor, karar be… |
| C2 | +%8 görülünce stop maliyete (T10) | TUTMADI | takip.MALIYET_ESIK 8,0 (T10) | AÇIK (Cemal kararı) |
| C3 | %20 hedefe değince SMA20 trail, en çok 120 bar; stop yok | TUTMADI | COL_v1.HEDEF 20; takip trail SMA20, ufu… | KAPALI (çıkış kapalı konu) |
| C4 | Son büyük mumda büyük kısmı sat ('içindeysem %70 satılır', K11) | SINANMADI | YOK | AÇIK |
| C5 | Tepe mumları aşağı gösteriyorsa çık / alma (K13) | SINANMADI | YOK (çıkış); FITIL_V2 s5 (giriş) | AÇIK |
| C6 | DGXX bilanço günü +%25 ve üstü 1/3 sat; kötü bilanço (nakit < kalan yatırım, teslim kayması) beklemeden sat | SINANMADI | YOK (ONERI_DEFTERI metni) | AÇIK |
| C7 | QMLS: bilanço iyi ve sıçrama o gün sat; NT 10-Q / ağırlaşan going-concern ertesi sabah sat; en geç 8 Oca 2027; ekleme y… | SINANMADI | YOK (ONERI_DEFTERI metni) | AÇIK (8 Oca 2027) |
| C8 | Sektör yeşil gününde sat: sektör %1 yükselirse QMLS %10 zıplar | TUTMADI | YOK | KAPALI |
| D1 | Sektör rüzgârı veya katalizör olmadan çöl aranmaz | ÖLÇÜLEMEDİ | COL_v1 RUZ_ESIK 0,10, RUZ_MUTLAK 0 (sek… | İLERİ TEST Mart 2027 |
| D2 | Sektör rüzgârının kendisi (sepet - piyasa ≥ eşik, sepet > 0) | EMARE | COL_v1.sektor_ruzgar / ruzgar_listesi | İLERİ TEST Mart 2027 |
| D3 | Rüzgâr fiyattan görülünce geç kalınır; önce sebebe bak | TUTMADI* | YOK | KAPALI |
| D4 | Patlayanların arkasında ve patlama zamanında rüzgâr var mı; rüzgâr batmayı azaltır mı | TUTMADI* | YOK | KAPALI |
| D5 | Büyükler önce, küçükler sonra; para akışı yetmez, temel ve haber zamanlaması | TUTMADI* | YOK | KAPALI |
| D6 | Amerika öncü; Avrupa ve Asya takip eder; gecikme saat farkıyla alınabilir | TUTMADI* | YOK | KAPALI |
| D7 | BIST öngörülemez (siyaset, tedbir, fon); Amerika ve Avrupa'da tutan iz kabul edilir, BIST bilgi | SINANMADI | FON_IZI FI_OLCUT 'karar'; ORTAK_CETVEL… | KAPALI (standart) |
| D8 | Bilanço iyi gelecek; önce korkutup aldırmıyorlar, iyi gelirse göstermelik yukarı, sonra yavaş dağıtım | SINANMADI | YOK | AÇIK |
| D9 | SMA üstüne atılım (AMZN) iz mi; endeks SMA200 filtresi | TUTMADI | YOK | KAPALI |
| D10 | Kilit öncesi yükseltip perakendeye satıyorlar: düşük float, yeni listeleme, sığ tahta = çıkış likiditesi | SINANMADI | YOK | KAPALI (kripto kapandı) |
| E1 | Fitil öbeği S+: alt fitil yok / küçük, üst fitil biraz uzun = has yukarı çıkma mumları, öbek olunca | ÖLÇÜLEMEDİ | FITIL_OBEK (FO_ESIK k 10, ASİM 0,20, AL… | İLERİ TEST Mart 2027 |
| E2 | Tersi (üst fitil yok, aşağı sert dişler) aşağı götürür (DGXX 2,50 → 2'nin altı) | TUTMADI | FITIL_OBEK S- | İLERİ TEST Mart 2027 |
| E3 | 'PAPIL'e has değil' (fitil öbeği genel çöl izi) | TUTMADI | YOK | KAPALI |
| E4 | Doji / fitil / dar hafta / alt fitil < 0,12 kaliteli çöldür (boyut çarpanı) | SINANMADI | COL_v1.carpanlar_hesapla (CARPAN doji /… | AÇIK (COL_OZET 9.8 'yeniden doğrulama') |
| E5 | D12 imzası: mumlar küçülür, Bollinger daralır, doji ve hacim kuruması | TUTMADI | COL_v1.col_dip (D12; üretimde değil) | KAPALI |
| E6 | Düşüş sonrası son 3-4 mumun dizilimi ve küçülmesi (hissenin kendi oynaklığına oranla) | TUTMADI | MUM_SUKUN.py | KAPALI |
| E7 | Akışkan madde düz zemine çarpar; 4-5 mum zemine yapışık sıra | ÖLÇÜLEMEDİ | MUM_SUKUN.py (zemin) | AÇIK |
| E8 | 60 gün uzun; kısa sıkışma %3-5 verir; uzun sıkışma + para girişi sert ayrılma | TUTMADI | MUM_SUKUN.py | KAPALI |
| E9 | Sıkışmadan sonra büyük mumlar kesin gelir; başlama zamanı tahmin edilebilir | TUTMADI | SIKISMA_YENIDEN.py | İLERİ TEST Mart 2027 |
| E10 | Gözüm küçük mumlardan sonra gelen mumları büyük görür, ayrılık var | TUTMADI | YOK | KAPALI |
| E11 | Su yolu: çölde engelde birikip birikmiş potansiyelle hızlı akış (büyük mumdan geriye git) | TUTMADI | TERS_PARMAK.py | İLERİ TEST Mart 2027 (P1) |
| E12 | İşaretli bölgenin parmak izi (eğim, küçük mum, kırmızı-yeşil, fitil, yakınlık, hacim, RSI, MACD); birebir benzerler yuk… | TUTMADI | FON_IZI k23 / k26 / k44 / k47 | KAPALI (şekil / parmak izi 'yanlış yol', 11… |
| E13 | Koşan vakaların ortak profili: sert düşüş → mumu ve hacmi küçük dar kutu → kapanışla tavan kırılımı | TUTMADI | FON_IZI k18 | KAPALI |
| E14 | Eski formasyonlar (Bollinger, RSI, MACD, Fibonacci, ikili dip, ters OBO, uyumsuzluk) başarılı mı | TUTMADI* | FON_IZI gosterge / k38b / k41 | KAPALI |
| F1 | Sıkı dosya (YEOTK profili): gerçek iş + isimli sözleşme, son çeyrek satış / kâr ivmesi, nakit seyrelme yok, fon lekesi… | TUTMADI* | K57.py; oneri tarama_kosu (DOSYA kapısı) | KAPALI (hat kapandı) |
| F2 | Fiyat tepeden düşmüş olsun (dipten al) | TUTMADI | K57 F6 | KAPALI |
| F3 | Bilanço günü güçlü tepki / bilanço sürprizi | TUTMADI* | FON_IZI k28; K62.py | KAPALI |
| F4 | Görünen alıcı = içeriden alan (KAP pay alım, SEC Form 4); çölde içeriden alım | TUTMADI* | FON_IZI k27 / k30 | KAPALI |
| F5 | En başarılı analistlerin dört verisi: seyrelme, içeriden satış, nakit tükenmesi, kurumsal sahiplik | TUTMADI* | FON_IZI k31 | KAPALI |
| F6 | Nakit tükenmesinde iyi çıkanların izi; batanlar dahil sına | TUTMADI | FON_IZI k33b / k34 | KAPALI |
| F7 | Fonların para girişi iz bırakır (balina girişinde küçük mum ve ufak ufak yukarı yuvarlanma); fon girişi | TUTMADI | FON_IZI k9-k11, fon_iz_b, z0 | KAPALI |
| F8 | Fon yoğunlaşması yapı riskidir (TERA / Pusula); tasfiye fonu payı yüksek hisse elenir | SINANMADI | COL_v1.FON_ESIK 5,0 + FON_TASFIYE (D8);… | KAPALI (üretimde) |
| F9 | DOSYA kapısı: birincil kaynak (KAP / SEC) gerçek gelir, sözleşme, nakit, borç, seyrelme, going-concern, tedbir / fon le… | ÖLÇÜLEMEDİ | oneri tarama_kosu (DOSYA bayrakları); Y… | AÇIK (aylık karne) |
| F10 | BofA almış = emare; en erken bul, alımından satımına kadar takip et; diğer yabancı kodlar da | TUTMADI | BOFA_IZI kos | İLERİ TEST Haziran 2027 |
| F11 | BofA bir hissede %40-80 zarar etmez | TUTMADI | BOFA_IZI karkos | İLERİ TEST Haziran 2027 |
| F12 | Emare vardır; geniş açıdan bak (çöküş sonrası dönüşü önceden gösteren) | EMARE | GENIS_KESIT.py | İLERİ TEST (2018 / 2020 BIST, ABD; ön kayıtl… |
| G1 | Tek isim, kaybetmeyi kabul ettiği tutarı aşmaz; HEDEF: tamamı kaybedilebilir | SINANMADI | YOK (ONERI_DEFTERI metni) | AÇIK |
| G2 | Zarardaki isme olaysız ekleme yok | TUTTU | YOK | KAPALI (kural) |
| G3 | Maliyetin 2 katında anaparayı çek (2x kuralı) | SINANMADI | YOK | AÇIK |
| G4 | Aynı sektörde ikinci isim yoğunlaşma uyarısıyla | SINANMADI | YOK | AÇIK |
| G5 | Tavanda kovalama yok | SINANMADI | YOK | AÇIK |
| G6 | Risk değil boyut öldürür; koruma = pozisyon boyutu, stop değil (PAPIL, QMLS, TERA) | TUTTU | COL_v1 boyut %6 x çarpanlar, üst %12 (ü… | KAPALI |
| G7 | BIST'te fiyat stopu çalışmaz (taban serisi) | TUTTU | YOK (C1 T6 ile çelişir) | KAPALI |
| G8 | Boyut çarpanları: CDS, borç / öz, doji, alt fitil, dar hafta, üç şart | SINANMADI | COL_v1.carpanlar_hesapla, cds_rejim | AÇIK |
| G9 | İlk hissede 2x yaparsam sonraki hisselerde riski azaltırım | SINANMADI | YOK | AÇIK |
| H1 | Ön kayıt: tanım + eşik + kod sha ölçümden önce git'te (K9) | SINANMADI | IZ_KARNE.ik_kontrol_kapisi; ORTAK_CETVE… | KAPALI (kural) |
| H2 | Her aşamada aynı ölçüm kriteri; sonucu beğenmediğimiz için eşikle oynanmaz | SINANMADI | ORTAK_CETVEL.oc_kapi (CETVEL_SHA) | KAPALI (kural) |
| H3 | Yeni ölçüt: eşli fark, ay kümeli %95, sıra > 0,50, 200 rastgele portföy | SINANMADI | FON_IZI FI_OLCUT; ORTAK_CETVEL OC_ESIK | KAPALI (standart) |
| H4 | 'Kazandıran kırılım + stop + trail' rastgele hisseden / noktadan çok daha fazla kazandırmalı; bu test yok, aptallık var | TUTTU | ORTAK_CETVEL plasebo 200 | KAPALI |
| H5 | Eski modeller sık hata yaptı; bul, doğrula, düzelt, yeniden koştur | TUTTU | YOK (üretim 11 hatası 'yaz' bekliyor) | AÇIK (üretim düzeltmeleri) |
| H6 | Batanlar neden test edilmiyor; o dönem parmak izine uyan bütün hisseler katılsın | TUTTU | K34 / Tiingo (yalnız ABD nakit testi);… | AÇIK (ABD batan fiyatı kotalı) |
| H7 | Kör set: hisse adı yok, sonraki mumlar yok; gerçek mum grafiği, ortak ölçek, geriye zum, alış mumu çizilsin | TUTTU | KOR_TEST, FITIL_KOR, FITIL_V2 kör set | KAPALI (kural) |
| H8 | Yanlış kabul ettiğimiz kural sonra doğru çıkabilir; ileri test, üç art arda aynı yön = kesin | TUTTU | IZ_KARNE.IK_ILERI | KAPALI (kural) |
| H9 | İZ DEĞİL yalnız güç yeterliyken (n ≥ 1.000 ya da güç %80); aksi ÖLÇÜLEMEDİ | SINANMADI | ORTAK_CETVEL.oc_hucre_durum | KAPALI (standart) |
| H10 | Bütün yanlış hesapların kaydı alınsın (hata defteri) | SINANMADI | IZ_KARNE.IK_HATA | KAPALI (kural) |
| H11 | İz ararken hatalar önceden okunsun, kod yazmaya öyle başlansın; bütün modeller için | SINANMADI | IZ_KARNE.IK_KONTROL + ik_kontrol_kapisi | AÇIK (6 modül) |
| H12 | Hedefli bağımsız denetim: iddia taşıyan, üretime ya da gerçek paraya dokunan işte yazan ve sınayan ayrı | SINANMADI | YOK | KAPALI (kural) |
| H13 | Yapmayı alt modeller yapsın; ana model iş tanımı + denetim | SINANMADI | YOK | KAPALI (kural) |
| H14 | MD defterini yalnız ana model değiştirsin | SINANMADI | test_iz_karne (defter kapsamı) | KAPALI (kural) |
| H15 | Gerçek ve değerli bilgi basit ve erişilebilirdir; karmaşık ölçü basiti geçmiyorsa seçilmez | TUTTU | YOK | KAPALI |
| H16 | Sonuç olasılık tablosuyla: +%100 ve -%50 olasılığı kaç kat; 'bu var, şu yok' dili | SINANMADI | ORTAK_CETVEL (olasılık), K60.py | KAPALI (kural) |
| H17 | Çöl ardından gelen yükselişle değerlendirilir; sabit ufuktaki kapanış başarı ölçüsü değildir; 60 gün değil alımdan satı… | TUTMADI | YOK (ana ölçü ORTAK_CETVEL r60) | AÇIK (bkz. bölüm 5) |
| H18 | İz yok çıkarsa durma: denenen, yaklaşan, sıradaki 3 deneme önceden sabit eşikle | SINANMADI | YOK | KAPALI (kural) |
| H19 | Hiçbir yerde iz yok, o zaman kesin sen hata yapıyorsun | TUTTU | ORTAK_CETVEL güç tablosu | KAPALI |
| H20 | Sıkışma tanımın rastgele bölge seçiyor; son iki çıktı tamamıyla rastgele | TUTTU | SIKISMA_CEMAL / SIKISMA_OBEK / S6 (yeni… | KAPALI |
| H21 | Kutu neredeyse rastgele: bölgenin önceki ve sonraki küçük mumları dahil değil | TUTTU | S6_TABAN (sınır mumdan); COL_S5_OBEK.pi… | KAPALI |
| H22 | Ücretli veri / abonelik yalnız açık onayla; Aralık Tiingo kotası kanıtlanmamış fikre harcanmaz | SINANMADI | YOK | KAPALI (kural) |
| H23 | Fotoğraftan bölge tarihi tahmin edilmez; Cemal'den tarih alınır | TUTTU | S6_TABAN S6_IZGARA_V11 puan_disi (KNFRT) | KAPALI |
| I1 | Hedef: zarar etmemek, %100'ün üstü, ilk hedef 10x; küçük yüzdeyle girmek yetmez, büyük kazanmalıyım | TUTMADI | K60.py; öneri modülü (YOK: 10x ölçüsü) | AÇIK |
| I2 | YEOTK daha da çıkar, DGXX kazanır; gerisi gürültü | ÖLÇÜLEMEDİ | oneri_karne/karne.py | İLERİ TEST (60 gün eşli kıyas, Ocak 2027) |
| I3 | Fon yüzünden her şey %40+ düştü, artık çok düşmez; oynak hisse seçilince yükselme ihtimali yüksek | ÖLÇÜLEMEDİ | COKUS_OYNAK.py | İLERİ TEST Mart / Kasım 2027 |
| I4 | Fon krizinde 1 TL'ye inmiş hisse tavan serisi; devasa hacim barı; 1 liradan daha nereye düşer | TUTMADI | TAVAN_SERISI.py | İLERİ TEST Mart 2027 |
| I5 | Fon krizi: 31.08.2026 sonrası olağanüstü, çöl ve sinyaller teste girmez; düşüşler gerçek, bölünme değil | TUTTU | ORTAK_CETVEL OC_ESIK 'kriz' 2026-08-31;… | KAPALI (standart) |
| I6 | Bir hisseyi fazla alıcı olunca o bölgede çöl yapısı oluşur (BINBN fon almış, %1000) | TUTMADI | FON_IZI k25 | KAPALI (AKD yok) |
| I7 | Piyango gibi sıçrayan hisselerde belirgin özellik vardır | TUTMADI* | FON_IZI k33 | KAPALI |
| I8 | Kripto +%100 günü önceden tespit edilir (RITUAL) | TUTMADI | arastirma_cikti/kripto_yukselis | KAPALI (Cemal 9 Kas: kripto kapandı) |
| I9 | Tipik dönüş noktası makineye öğretilebilir | TUTMADI* | FON_IZI k46 | KAPALI |
| J1 | Çöl swing tepesinden türetilmez; tek mumun H / L'i ile bant kurulmaz | SINANMADI | S6_TABAN bant (bölgedeki bütün mumlarda… | KAPALI (tanım) |
| J2 | Sabit % eşik yanlış; eşikler hisse başına (ATR / kendi oynaklığı) | SINANMADI | S6_TABAN kM x ATR250 (kısmen); bantMax… | AÇIK |
| J3 | Tek özelliğe bakılmaz: bölge, dip, Bollinger, küçük mum, doji, birikim izi, hacim kuruması BİRLİKTE | TUTMADI | COL_v1.col_dip (D12 imza, üretimde deği… | KAPALI |
| J4 | Peş peşe büyük mumla bölgeden çıkılıyorsa çöl değil; BIST 'dev mum' (~%10) çöl içinde ASLA sayılmaz | SINANMADI | YOK (dolaylı: S6 kM, bantMax) | AÇIK |
| J5 | İniş mumları (bölgeye giren büyük mumlar) çöle dahil edilmez | SINANMADI | COL_v1.col_dip2 (d = son 120 bar dibi);… | KAPALI (tanım) |
| J6 | Bölgeden azıcık çıkıp dönmek olur; uzağa çıkıp dönmek çöl değil | SINANMADI | YOK (dolaylı: S6 dipTol 0,05, kirTol 0,… | AÇIK |
| J7 | EN KRİTİK ÖZELLİK doji: dipteki kutuda 3-5 doji bile birikim / sıkışma işaretidir | ÖLÇÜLEMEDİ | COL_v1 CARPAN doji (boyut) ve col_dip I… | AÇIK |
| J8 | Çöl bir yıla kadar uzar, genişler, içinde sert silkelemeler olur | TUTMADI | COL_v1.uzun_col_olc; S6 nMax 70 | İLERİ TEST Mart 2027 |
| J9 | Bitişte çok küçük mumlar (3 ya da 7-8 adet) görülebilir (esnek, zorunlu değil) | TUTMADI | MUM_SUKUN.py; üretimde YOK | KAPALI |
| J10 | Eğim / 'kanama' gürültüdür | SINANMADI | S6_TABAN netMax 0,03 (tersi yönde) | AÇIK (Cemal kararı) |
| J11 | AL kuralı: dünkü aday + kapanış > tavan x 1,002; kapanışla kırılım high'dan güvenilir | TUTMADI | COL_v1.AL_PAY 1,002 (bugun_liste, kapan… | KAPALI (giriş zamanlaması kapalı konu) |
| J12 | Segmentin en düşük dibi kırılırsa segment oradan yeniden hesaplanır | SINANMADI | COL_v1.col_dip2 (d = son 120 bar dibi);… | KAPALI (tanım) |
| J13 | İki kutu: kutu 1 = çöl (SMA200 civarı iyi), kutu 2 = raf | SINANMADI | YOK | AÇIK |
| J14 | Daha önce 732 kırılımda çöl şekli tek başına yazı-tura çıktı (%36 yukarı, %32 aşağı); şekil tek başına yetmez | TUTTU | YOK (bulgu, şart değil) | KAPALI |
| J15 | ABD hissesinde önce sermaye yapısı kontrolü | SINANMADI | oneri tarama / DOSYA kapısı; K60B bayra… | KAPALI (öneri modülünde) |
| J16 | Tek dosya, KURAL_MOTORU, tam hata yönetimi + log; doğru kısmı koru; isim çakışması mekanik yakalansın; test önbellekten… | SINANMADI | Modüllerde _cakisma_kontrol (çakışma ka… | KAPALI (kural) |
| J17 | Bir ölçü bir testte artı, ötekinde eksi ise iz değil; küçük örneklem bulgu değil; tek izle karar yok | SINANMADI | ORTAK_CETVEL.oc_hucre (iki yarı, n ≥ 30) | KAPALI (kural) |
| J18 | Tarayıcı yalnız aday bulur; desen / göstergeye göre alım-satım yasak | SINANMADI | COL_v1.bugun_liste (aday listesi) | KAPALI (kural) |
| J19 | Cevaplar Türkçe; 'yatırım tavsiyesi değildir' cümlesi yazılmaz | SINANMADI | YOK | AÇIK (Cemal kararı) |

## 4. KASA KART TASLAKLARI (25; öncelik sırası)

Seçim ölçütü (önceden): (i) Cemal'in kendi kuralı, (ii) eşiğe en çok yaklaşmış ve B / C sınıfı, (iii) sayısal tanımı ve eşiği kayıtta hazır, (iv) veri elde, (v) aile çeşitliliği. Yeni eşik yazılmadı; eşik kayıtta yoksa "kayıtta eşik yok, ana model sabitleyecek". Hepsinde ortak ölçü notu: ölçü: karar için stop'suz r15 eşli fark + r60 (Ç203 öneri 1); h5 yalnız bilgi (Ç203); plasebo sapması sıfırlanmadan AVR karar vermez (Ç203 öneri 2). Ortak başarı şartı (kayıttaki FI_OLCUT / ORTAK_CETVEL): FI_OLCUT dört şart (n ≥ 30; eşli fark > 0 ve ay kümeli alt uç > 0; sıra > 0,50; portföy > rastgele p90) + n ≥ 1.000 / güç ≥ %80 (K58 / Ç175).

### KK01 (Ç187 / K30)
- **CÜMLE:** Son 10 barda üst fitili uzun, alt fitili kısa mum öbeği (S+) görülürse sonraki 15 barda eşlerinden daha çok yükselir; tersi (S−) düşer.
- **GÖRÜLEN ŞEY:** ASİM = ort(üst fitil) − ort(alt fitil), son 10 geçerli bar; ASİM ≥ 0,20 ve alt fitilsiz payı ≥ 0,50 (Ç187 kaydı, FITIL_OBEK k = 10); t'de bilinir
- **EŞİK:** FITIL_OBEK sabit: k = 10, ASİM 0,20, fitilsiz payı 0,50 (kayıt). Ölçü eşiği: FI_OLCUT dört şart (n ≥ 30; eşli fark > 0 ve ay kümeli alt uç > 0; sıra > 0,50; portföy > rastgele p90) + n ≥ 1.000 / güç ≥ %80 (K58 / Ç175)
- **YÖN:** S+ yukarı, S− aşağı
- **ÖNCEKİ SONUÇ:** 60 gün, ORTAK_CETVEL: 2024-26 hücreleri n 1.557-2.367 TUTMADI (fark ±%0,3, sıra 0,49-0,51); 2023 n 592-928 güç %52 → ÖLÇÜLEMEDİ
- **NEDEN YENİDEN:** B + C (60 gün kapandı; 15 bar hiç koşulmadı, IK_ILERI UFUK15)

### KK02 (Ç193 / Y9)
- **CÜMLE:** Sert düşüş sonrası dipte (120 gün konumu düşük) S6 taban kırılımı, 15 barda eşlerinden ve konum eşlerinden daha sık hedefe (+%5 / +%10) gider.
- **GÖRÜLEN ŞEY:** S6 AL + F15 ≤ 0,25 (120 gün konumu) + bölge öncesi 60 gün düşüş ≥ %20 (F17 ≤ −0,20); kaynak Ç193 / YAPI_HEDEF Y9
- **EŞİK:** YAPI_HEDEF Y9 eşikleri sabit (F15 ≤ 0,25, F17 ≤ −0,20; ön kayıt d32c2b1)
- **YÖN:** yukarı
- **ÖNCEKİ SONUÇ:** 15 bar h5: Y9 n 146 / 231 / 20 / 55 güç ≤ %57; bakılmış ABD KAT5 1,15 [1,05; 1,29] ve 1,21 [1,06; 1,36]; konum eşli 1,15 / 1,20; AVR n küçük
- **NEDEN YENİDEN:** B; Ç204 sonrası h5 üstünlüğü kalktı: kart yalnız stop'suz R15 / r60 ölçüsüyle (Cemal'in çöl tanımı olduğu için tutuldu)

### KK03 (Ç189 / K1-K29)
- **CÜMLE:** Fitil öbeği + savunma hattı + dönüm + yol almamış + dipte (S+ v2 'tam girilir') 15 barda eşlerinden iyi.
- **GÖRÜLEN ŞEY:** S+ (ASİM ≥ 0,20, alt fitilsiz payı ≥ 0,50) + savunma hattı (10 bar dibi, önceki 30 barın dibini kırmamış) + yol almamış (t hariç) + dipte; kaynak FITIL_V2 N30
- **EŞİK:** FITIL_V2 N30 eşikleri sabit (ön kayıt cc02f7fa)
- **YÖN:** yukarı
- **ÖNCEKİ SONUÇ:** 60 gün: n 34-187, güç %10-29, eşli fark −3,8..+1,1; −%50 katı > 1
- **NEDEN YENİDEN:** B + C

### KK04 (K50 / H2 (Cemal, Ekim eşleri))
- **CÜMLE:** 120 günün tam dibine son 5 günde düşerek gelen hisse (dip savunulmadan) 15 barda eşlerinden kötü kaybeder; 'dip savunulmadan giriş yok'.
- **GÖRÜLEN ŞEY:** F15 ≤ 0,05 (120 gün konumu) ve r5 ≤ −%3 (kural defteri K50); t'de bilinir
- **EŞİK:** tanım eşikleri kayıtlı (F15 ≤ 0,05, r5 ≤ −%3); karar eşiği kayıtta yok, ana model sabitleyecek (9. tur ön kayıt, BH 3)
- **YÖN:** aşağı (kaçınma)
- **ÖNCEKİ SONUÇ:** hiç ölçülmedi; Ekim eşleri (sonradan bakma, n 77): h5 %64 / st5 %32 vs %71 / %18 (K50 kaydı)
- **NEDEN YENİDEN:** E

### KK05 (K12 (Cemal, kör set 2 No 1))
- **CÜMLE:** Geçmişinde dev tek mum (fitil > +%100) olan hissenin kağıdı şüphelidir (kripto gibi): yapıları 15 barda eşlerinden kötü sonuç verir.
- **GÖRÜLEN ŞEY:** geçmişte tek mum fitili > +%100 (kural metni); fiyat-hacim, t'de bilinir; ters bölünme / OTC sıçraması ayıklanmalı (Ç175: k60 verisinde 4.678 hissenin 1.235'inde > 3x sıçrama ya da H-L > 2 x kapanış)
- **EŞİK:** kayıtta eşik yok, ana model sabitleyecek (yalnız "> +%100" kural metninde)
- **YÖN:** aşağı (kaçınma)
- **ÖNCEKİ SONUÇ:** hiç ölçülmedi (SINANMADI; devir notu J4 / C13 ile akraba; K6 birim denetimi şart)
- **NEDEN YENİDEN:** E

### KK06 (K2 / K9 (E))
- **CÜMLE:** Düz tavan (ilk dip yapısının tavanı) 15 barda aşağı kırılırsa (SAT mumu = tavandan kopan ilk büyük kırmızı mum) ilk düşüş hedefi gelir; S6 ayna sürümü.
- **GÖRÜLEN ŞEY:** S6 taban kırılımının aynası: düz tavan çizgisi (K29: ilk yapının tavanı) + aşağı kırılım mumu; hedef: önceki dip
- **EŞİK:** kayıtta eşik yok, ana model sabitleyecek (ön kayıt gerekir)
- **YÖN:** aşağı (kısa kol / kaçınma)
- **ÖNCEKİ SONUÇ:** hiç ölçülmedi (SM_TEPE fitil aynasıydı, düz tavan değil; K2 SINANMADI)
- **NEDEN YENİDEN:** E

### KK07 (K8 / C8 (E))
- **CÜMLE:** Aynı hissede önceki benzer yapılar hedefe gittiyse (kağıt hafızası) yeni yapı da gider; patladıysa girilmez.
- **GÖRÜLEN ŞEY:** hisse bazlı formasyon karnesi: önceki S6 / yapı olaylarının +%5 hedefine ulaşma payı (t'ye kadar)
- **EŞİK:** kayıtta eşik yok, ana model sabitleyecek
- **YÖN:** yukarı (önceki başarı) / aşağı (önceki patlama)
- **ÖNCEKİ SONUÇ:** hiç ölçülmedi (Y4 / Y8 farklı tanım: AVR 2024-26 0,87 aleyhte; Cemal'in en ağır şartı)
- **NEDEN YENİDEN:** E

### KK08 (Ç196 / K19)
- **CÜMLE:** Düşüş sonrası dip grubu (G2), trend içi raf (G1) ve rastgele (G3) gruplarından 15 barda daha çok hedefe ulaşır.
- **GÖRÜLEN ŞEY:** G2 = Ş1 (F15 ≤ 0,25 ve F17 ≤ −0,20); G1 = F14 ≥ 0 ve F15 ≥ 0,50; G3 = G2 ile aynı n rastgele
- **EŞİK:** YAPI_HEDEF YH_ESIK6 sabit (ön kayıt 3833f78)
- **YÖN:** G2 > G1; G2 > G3
- **ÖNCEKİ SONUÇ:** 15 bar h5: G2 − G1 ABD +18 / +27 / +13, AVR +22 / +34 / +18 puan (alt uçlar > 0); G2 n 20-346 güç < %80; G1 ters | Ç204 (CETVEL2 R15 yeniden koşu, 21 Kas): eski h5 farkları (+9..+34 puan) R15'te −0,2..+0,7 puana indi, aralıklar 0'ı kesiyor: dipteki 'daha sık +%5' üstünlüğü yön değil oynaklıkmış
- **NEDEN YENİDEN:** B; Ç204 sonrası h5 farkı oynaklık: kart R15 / r60 ile

### KK09 (Ç173b)
- **CÜMLE:** Tepeden ≥ %80 düşmüş, son 10 günde yeni dip yapmamış, dipten ≤ 1,5 kat uzaktaki hisse (D1-D3 kurulumu) eşlerinden iyi.
- **GÖRÜLEN ŞEY:** 250 gün tepeden ≤ −%80 + son 10 günde yeni dip yok + dipten ≤ 1,5 kat; 60 gün ayrı olay
- **EŞİK:** BOFA_DIP kurulum D1-D3 sabit; FI_OLCUT dört şart + 250 gün olasılık
- **YÖN:** yukarı (piyango riski: P+%100 ve P−%50 ikisi de ~2 kat)
- **ÖNCEKİ SONUÇ:** FI_OLCUT: ABD 2023 n 81 +%24,8 [+8,9; +43,0] sıra 0,55 TUTTU; 2024-26 n 146 +%20,6 sıra 0,48 portföy tutmadı; AVR n 3 / 8
- **NEDEN YENİDEN:** B (AVR n yetersiz) + yön çelişkisi

### KK10 (Ç184)
- **CÜMLE:** Cemal'in öbek sıkışması (dip sınıfı) sonrası 20 günde büyük gün (≥ 3 × ATR250) eşlerinin 1,14-1,17 katı sıklıkla gelir.
- **GÖRÜLEN ŞEY:** 15 bar, en büyük 1 mum hariç medyan mum ≤ 0,75 × ATR250, 1 uç gün hariç kapanış bandı ≤ %8 (BIST) / %6, eğim −%2..; SIKISMA_OBEK mühür de384bbd
- **EŞİK:** SIKISMA_OBEK mühür de384bbd sabit: p 15, k_m 0,75, bant 8 / 6, bb 0,20
- **YÖN:** büyük gün olasılığı yukarı; getiri / yön yok
- **ÖNCEKİ SONUÇ:** ABD n 579 / 649 (< 1.000) KAT 1,14-1,17 EMARE; AVR n 292 / 389 ölçülemedi
- **NEDEN YENİDEN:** B

### KK11 (Ç178 / K24 / A1)
- **CÜMLE:** İki evre çöl (düşüş sonrası SMA20 altı → SMA20 üstü 5 gün dizilme, ≤ 2 delen, BB sıkışması; üretimdeki tek çöl sinyali) eşlerinden ayrışır.
- **GÖRÜLEN ŞEY:** FI_K24 fi_k24_tara değişmeden; ORTAK_CETVEL v1.0
- **EŞİK:** ORTAK_CETVEL v1.0 (4763c458) + FI_K24 sabit; SAPMA-1: t'ye kadar 200 bar
- **YÖN:** yukarı
- **ÖNCEKİ SONUÇ:** ABD 2024-26 n 2.869 −%1,1 [−2,7; +0,9] TUTMADI (güç yeterli); ABD 2023 n 941 +%1,3 güç %52; AVR n 100 / 286 güç %29; iki yönde büyük hareket (piyango)
- **NEDEN YENİDEN:** B (2023 / AVR güç)

### KK12 (Ç179)
- **CÜMLE:** Düzgün dip + çöl birlikteliği (C), yalnız dipten (A) ya da yalnız çölden (B) ayrılır.
- **GÖRÜLEN ŞEY:** dip16 / dip17 / K24 parametreleri sabit (DIP_COL_AYRIM); A yalnız dip, B yalnız çöl, C 60 günde ikisi
- **EŞİK:** ORTAK_CETVEL v1.0; ön kayıtlı: ayrım kuralı
- **YÖN:** C > A ve C > B
- **ÖNCEKİ SONUÇ:** ABD C n250 381 / 723 (< 1.000); AVR C n250 11 / 33; ABD'de C ≈ A, +%100 katı 1,41 / 1,42 ve 1,40 / 1,33, aralık 0'ı kapsıyor
- **NEDEN YENİDEN:** B

### KK13 (Ç182 P1)
- **CÜMLE:** Son mum büyük (≥ 1,22 × ATR250) + 250 gün tepesine yakın + 40 günde küçük mum dizisi yok olan hissede 20 günde büyük mum olasılığı eşlerinden yüksek.
- **GÖRÜLEN ŞEY:** P1: son mum ≥ 1,22 × ATR250, 250 gün tepesine yakın, 40 günde küçük mum dizisi yok; eşler σ250 ondalığında
- **EŞİK:** P1 eşikleri sabit (ters_kurallar.json sha); BH q
- **YÖN:** büyük mum olasılığı yukarı (yön yok)
- **ÖNCEKİ SONUÇ:** ABD n 3.145 / 16.258, AVR 838 / 4.679; dört hücre alt uç > 1; BH q 0,001 EMARE; IK_ILERI: anlık oynaklık (ATR10 / ATR250) eşlemeli kontrolle yeniden
- **NEDEN YENİDEN:** B/D (oynaklık karışımı şüphesi; IK_ILERI maddesi)

### KK14 (Ç183 / S4)
- **CÜMLE:** Cemal tanımlı sıkışma (15 gün küçük mum + dar BB + yatay) büyük hareketin habercisidir.
- **GÖRÜLEN ŞEY:** 15 gün küçük mum (250 gün %20 yüzdeliği) + dar Bollinger (BB 20, 2σ genişliği 250 gün %20 yüzdeliği) + yatay (|net| ≤ %3...)
- **EŞİK:** SC_ESIK mühür 2533e1f0 sabit
- **YÖN:** büyük hareket yukarı
- **ÖNCEKİ SONUÇ:** ABD n 843 / 787, AVR 513 / 479 (< 1.000); B1 KAT ~1, BH2 < 1 nokta; ÖLÇÜLEMEDİ
- **NEDEN YENİDEN:** B

### KK15 (Ç194 / K32-K42)
- **CÜMLE:** S6 taban kırılımına Cemal'in 8 mekanik kuralı (Ş1-Ş8) süzgeç olarak eklenince 15 barda eşlerinden iyi.
- **GÖRÜLEN ŞEY:** Ş1 dipte (F15 ≤ 0,25, F17 ≤ −0,20), Ş2 hat net (F1 ≥ 3), Ş3 dip savunusu … Ş8; kaynak YAPI_HEDEF Y10 / Y10b / Y10c
- **EŞİK:** YAPI_HEDEF Y10 / Y10b / Y10c eşikleri sabit (ön kayıt b4b701c)
- **YÖN:** yukarı
- **ÖNCEKİ SONUÇ:** Huni: 8 kural S6 bölgelerinin ~%0,6'sını geçiriyor; Y10 n 6-25 (güç %0); Y10c n 118-467; KAT5 ~1; Ç204: Y10 / Y10b ÖLÇÜLEMEDİ, Y10c SORGULA (1 / 4 hücre tutar)
- **NEDEN YENİDEN:** B (kasada n çok küçük kalır; yalnız Y10c; Ç204 R15 sonrası)

### KK16 (Ç191 / K19-K23)
- **CÜMLE:** Cemal'in süzgeçleriyle (net hat, gerçek kırılım, stop ≤ %10, büyük desen, hafıza) seçilen S6 kırılımı (Y6 / Y8) 15 barda eşlerinden iyi.
- **GÖRÜLEN ŞEY:** Y6 = S6 AL + hat ≥ 3 dokunuş eğimsiz + gerçek kırılım (kapanış > tavan × 1,01, gövde ≥ bölge medyanı) + stop ≤ %10 …; Y8 + hafıza
- **EŞİK:** YAPI_HEDEF YH_ESIK Y6 / Y8 sabit (ön kayıt 8b246d1)
- **YÖN:** yukarı
- **ÖNCEKİ SONUÇ:** n 80-310, güç ≤ %57; YÖN ALEYHTE: KAT5 0,59-0,90, üç hücrede üst uç < 1 (Ç203: stop süzgeci hedefe gidenleri eliyor)
- **NEDEN YENİDEN:** B + C + D (VD2)

### KK17 (Ç186)
- **CÜMLE:** Çöküş sonrası en oynak / en çok düşmüş hisse 250 günde +%100'ü eşlerinden daha sık görür, −%50'yi daha sık görmez (Cemal'in tezi).
- **GÖRÜLEN ŞEY:** çöküş = evren medyan 120 gün getirisi ≤ −0,30; OYNAK = σ250 üst beşlik; giriş = çöküşten +5 gün (COKUS_OYNAK)
- **EŞİK:** COKUS_OYNAK eşikleri sabit (IK_ILERI: medyan r120 ≤ −0,30; σ250 üst beşlik; giriş +5 gün); olasılık katı: ORTAK_CETVEL
- **YÖN:** yukarı (+%100 katı > 1, −%50 katı ≤ 1)
- **ÖNCEKİ SONUÇ:** ÖLÇÜLEMEDİ: tamamlanmış çöküş 1 < 2 (2023-05-22; 2026-10-13); 2023 OYNAK n 69, P+%100 %73,9, P−%50 %2,9, kat 0,95 (alt uç −15). Not: 2026-10-13 çöküşü fon krizi (31.08.2026) sonrasıdır: CLAUDE.md gereği testlere girmez, yalnız bilgi; kasa kullanımı Cemal kararı
- **NEDEN YENİDEN:** B (tek olay)

### KK18 (Ç124)
- **CÜMLE:** INTEM tipi kısa ufuk kutu çıkışı: birebir eşleşen bölgelerden sonra +%8 hedefi −%8 stop'tan önce görme payı, oynaklık eşli rastgeleden yüksek (sıkışma ailesindeki tek EMARE).
- **GÖRÜLEN ŞEY:** FI_K44 parmak izi (8 ölçü, band ±0,125) + K45 kısa ufuk kutu çıkışı; ileri test Ç180 değişmeden
- **EŞİK:** Ç124 eşikleri sabit: ABD + AVR 2016-26 n ≥ 30, +%8 önce payı rastgeleden ≥ +10 puan ve aralık artı
- **YÖN:** yukarı
- **ÖNCEKİ SONUÇ:** ÖLÇÜLEMEDİ: ABD 2023 n 26 −%3,2; 2024-26 n 42 −%7,5 (güç %10); AVR görülmemiş (Ç180)
- **NEDEN YENİDEN:** B + C (hedef-önce cetveli)

### KK19 (Ç128 / Ç125)
- **CÜMLE:** Geniş parmak izi makinesi (166 ölçü; Ç125 36 ölçülü dönüş noktası makinesi) üst %5 sinyali oynaklık eşli rastgeleden +%8 hedefi daha sık görür (AVR).
- **GÖRÜLEN ŞEY:** sabit model katsayıları (K46 / K48 kuralı), ABD + AVR 2023 ve 2024-26 üst %5
- **EŞİK:** üst %5 fark ≥ +10 puan, aralık artı, işlem > 0 (kayıt)
- **YÖN:** yukarı
- **ÖNCEKİ SONUÇ:** Ç128: ABD 2023 +6,9 (aralık +5,2) eşiğin altı; 2024-26 +12,4; AVR +10,8 / +11,3 (geçti); BIST +23,5 / +9,3; AUC 0,59-0,71. Ç125: ABD +3,6 / +12,2, AVR +4,6 / +12,8 (2023 eşik altı)
- **NEDEN YENİDEN:** C (+%8 önce cetveli) — oynaklık karışımı şüphesi

### KK20 (Ç112)
- **CÜMLE:** ABD'de blok hacimli sert düşüş (taban) günü sonrası hisse eşlerinden iyi (BIST'te ters).
- **GÖRÜLEN ŞEY:** A14 blok hacimli taban günü (hacim ≥ blok eşiği, taban günü)
- **EŞİK:** FI_OLCUT dört şart (Ç112 kaydı)
- **YÖN:** yukarı (ABD)
- **ÖNCEKİ SONUÇ:** ABD 2024-26 +%14,9 dört şart tutar; 2023 +%4,4 aralık 0'ı içerir; AVR n 8 / 24; BIST −%23 / −%30 (n 9 / 31); Ç60 BIST eski ÇÜRÜDÜ
- **NEDEN YENİDEN:** B + yön çelişkisi

### KK21 (Ç115)
- **CÜMLE:** ABD güçlü günü (eşit ağırlıklı ≥ +%1,5) sonrası Avrupa ertesi gün açılış boşluğuna alınabilir fazla girer.
- **GÖRÜLEN ŞEY:** ABD eşit ağırlık ≥ +%1,5 gün; Avrupa ertesi gün fazla = taban üstü; gün içi (açılıştan) fazla
- **EŞİK:** alınabilir gecikme = açılıştan sonraki fazla ≥ +%0,2 ve aralık artı; günlük 2023 + 2024-26 ve saatlik en az 2 endeks
- **YÖN:** yukarı
- **ÖNCEKİ SONUÇ:** boşluk +%0,23 / +%0,19 / +%0,23 üç dönemde aralık artı; gün içi +%0,10 / +%0,24 / +%0,03 (yalnız 2023 aralık artı); 5 gün sıfır
- **NEDEN YENİDEN:** B (saatlik veri son 730 gün); sektör / makro (Cemal kararı)

### KK22 (Ç155)
- **CÜMLE:** Oynak hisse havuzunda düşük beta olmayan (yüksek beta) hisse ikiye katlanmayı artırır, yarıya inmeyi artırmaz (BETA_BAB ALT, koşullu fırsat).
- **GÖRÜLEN ŞEY:** BETA_BAB (K60 tanımı) havuz içi ALT %20; havuz = ayda 60 günlük oynaklığı en yüksek %20
- **EŞİK:** K60B kuralı: kazanma katı > 1 ve batma katı ≤ 1 üç dönemde (ön kayıt K60B_ON_KAYIT sha256 b74f3e2d2656)
- **YÖN:** yukarı (+%100 olasılığı)
- **ÖNCEKİ SONUÇ:** +%100 katı 1,34 / 1,45 / 1,36; −%50 katı 0,91 / 0,73 / 0,98; aylık portföy havuzu +%5 / +%16 / +%16 geçti; yalnız ABD, yalnız yaşayanlar, 2024-25 yükseliş etkisi olabilir
- **NEDEN YENİDEN:** B + hayatta kalma (K7)

### KK23 (Ç154 DOSYA_Y)
- **CÜMLE:** Cemal'in 'sıkı dosya' ölçüsü (DOSYA_Y ÜST) yarıya inme olasılığını azaltır, ikiye katlanmayı azaltmaz (güvenli uç).
- **GÖRÜLEN ŞEY:** DOSYA_Y (K59 YEOTK / DGXX mantığı, SEC finansal özütleri, t'de bilinen) ÜST %10
- **EŞİK:** K60 ön kayıt: üç dönemde −%50 katı < 1 ve +%100 katı ≥ 1 (kayıt)
- **YÖN:** koruma (−%50 azalır)
- **ÖNCEKİ SONUÇ:** −%50 katı 0,62 / 0,54 / 0,61; +%100 katı 0,95 / 1,08 / 0,98; medyan evrenin üstünde; havuz içinde 0,65 / 0,81 / 0,73 (Ç155); yalnız ABD, yalnız yaşayanlar
- **NEDEN YENİDEN:** B (KASA ikinci kullanım; hayatta kalma)

### KK24 (Ç154 COMP4)
- **CÜMLE:** COMP4 bileşiği (K59 önceden yazılı sıra ortalaması) ÜST %10 yarıya inmeyi azaltır; portföyde piyasayı geçmez.
- **GÖRÜLEN ŞEY:** COMP4 = K59 §3 sıra ortalaması bileşiği (4 aile); ÜST %10
- **EŞİK:** K60 ön kayıt eşikleri; U1 / U2 TUTMAZ (K59)
- **YÖN:** koruma
- **ÖNCEKİ SONUÇ:** −%50 katı 0,43 / 0,25 / 0,47; +%100 katı 0,70 / 1,02 / 0,74; K59 U2 yıllık fazla +%5,5 NW t 2,30 TUTMAZ; K59-B (a) U2 +%7,0 t 2,39 TUTAR (yineleme)
- **NEDEN YENİDEN:** B

### KK25 (K49 / H1 (Cemal, Ekim eşleri))
- **CÜMLE:** Giriş ile 15. bar arasında bilanço duyurusu olan olaylarda hem en iyi hem en kötü sonuçlar toplanır (bilanço penceresi = kuyruk büyüteci, yön değil).
- **GÖRÜLEN ŞEY:** BIL15: giriş-15. bar arasında bilanço duyurusu var mı (duyuru ≤ t); ABD Nasdaq takvimi (Ç100) elde, BIST KAP
- **EŞİK:** kayıtta eşik yok, ana model sabitleyecek (9. tur ön kayıt, BH 3)
- **YÖN:** yön yok (kuyruk genişliği: hem +%5 hem stop payı artar)
- **ÖNCEKİ SONUÇ:** hiç ölçülmedi (Ekim eşleri sonradan bakma: kazanan 20 / 20, kaybeden %70); olay verisi (bilanço takvimi) fiyat bloğunda yok, ayrı kasa bloğu gerekir
- **NEDEN YENİDEN:** E

### Ç204 sonrası kart yapılmayanlar (ilk taslakta vardı; CETVEL2 R15 yeniden koşusunda etki yok)

- Ç201 Ş10 MACD pozitif uyumsuzluk (Cemal K47): Ç204: Ç201 3 hipotezin 2'si SORGULA (0 / 4 hücre tutar, güç yeterli → İZ DEĞİL +2 puan ve üstü için); kasaya alınmadı
- Ç202 DS06 dip süpürme (Turtle Soup): Ç204: ABD sınama FARK +6,9 → +0,21 (R15); etki yok
- Ç202 DS13 / DS28 / DS23: Ç204 R15: DS13 ÖLÇÜLEMEDİ, DS28 ve DS23 SORGULA (0 / 4 hücre tutar); AVR plasebo sapması Ç204'te giderildi
- Ç197 F1-F29 puan üst %20: Ç204: dört hipotezin dördü SORGULA; eski KAT 1,15 R15'te kalmadı; karmaşık ölçü basit ölçüyü geçmiyor (CLAUDE.md: basit seçilir)

## 5. KAPALI KONULAR ve gerekçesi (COL_OZET / CLAUDE.md; kart olmaz)

| konu | kayıt | gerekçe |
|---|---|---|
| Giriş noktası / zamanlaması / teyit / retest / kırılım hacmi | Ç01 (KAPALI: hiçbiri geçmedi) | sistem kuralı, olay izi değil; Ç01 denetimi yön aynı |
| Aday filtreleri (E_ONC, üç şart kapısı, taban kırılması düşürme) | Ç02 | her filtre para kaybettirdi |
| Çıkış varyantları / stop / erken kesme | Ç03, Ç45, Ç46, Ç91 | trail SMA20 en iyi; T10 getiri dayanağı ters döndü (Ç45); stop darlığı CD20 ayrı ölçüt (Ç203) olarak yeniden açılmaz, cetvel revizyonu işidir |
| Rejim / dış veri: VIX / DXY / USDTRY / CDS / temel | Ç05, Ç110 (DXY yok) | tutarsız |
| 4h / haftalık / KNN / ML kâr eklemesi | Ç06, Ç95 (Cemal isteğiyle KNN), Ç58 | rejime bağlı, ML kâr eklemedi |
| 90+ şekil ölçüsü | Ç04, Ç09, Ç43, Ç128 (166 ölçü) | şekil ölçüsü çölü ayırmıyor (Ç43 AUC 0,37-0,60); Ç09 oynaklık |
| Sektör ısısı | Ç28, Ç108-Ç111, Ç114, Ç117, Ç181c (Cemal istedi) | kapalı konu; Ç181c EMARE ve IK_ILERI maddeleri Cemal kararıyla yürür (kasa kartı değil) |
| Büyük çöl (20-60 mum, çok katlı hedef) | K16 (17 Kas) | fon / manipülasyon sınıfı; aranmaz; yalnız fon izi (K12) ile birlikte görülürse not |
| Kripto | Ç147 | İZ DEĞİL; Cemal 9 Kas: kripto kapandı |
| 60 gün sabit ufuk yapı ölçümü | K15 / UFUK 15 MUM | yapı kuralları 15 barla ölçülür; 60 gün yalnız bilgi (kapalı değil, ölçüt değişti) |

Not: Ç175 kapalı konuların çoğunun (n < 1.000 hücre) aslında ÖLÇÜLEMEDİ olduğunu, "İZ DEĞİL"i hak eden gövdenin Ç34, Ç41, Ç44, Ç47, Ç49, Ç56, Ç72, Ç85, Ç86, Ç88, Ç91, Ç93, Ç96 (ABD), Ç104, Ç132, Ç134, Ç156 olduğunu yazar. Kapalı konuların yeniden açılması Cemal kararıdır (CLAUDE.md), bu envanter açmaz.

## 6. HATA (derlerken bulunan çelişkiler)

1. Kayıtlarda iki ayrı 'K' numaralaması var: kural defteri bölüm K (K1-K51, Cemal'in kör set / hakem dersleri) ile CEMAL_COL_KURALLARI.md (K1-K8, K6b, K10-K49, 15 Kas taslağı; numaralar aynı değil, ör. 'K30 UFUK 15 MUM' orada, kural defterinde K30 fitil teorisi). Ayrıca FON_IZI / K51 / K58 gibi deneme kodları kural numarası değil. Bu envanterde K1-K51 = kural defteri bölüm K; deneme kodları Ç numarasıyla anıldı.
2. Etiket ile sayı uyumsuzluğu: Ç37 kaydında 'D9 yön ADAY (%56-61); test sürüyor' duruyor; Ç181 ve Ç175 aynı hipotezi 'İZ DEĞİL' (güç yeterli) yazıyor. Ç37 satırı bu envanterde İZ DEĞİL olarak sayıldı; IK_ILERI'de Ç37 ve Ç181a iki ayrı satır (ileri test çift sayılabilir).
3. Ç175 'İZ DEĞİL'i hak eden gövde' listesine Ç72, Ç86, Ç88, Ç156'yı koyuyor ama Ç72 / Ç86 / Ç88'in kendi satırında ana sayı yok (Ç72 'yeni deneme', Ç86 / Ç88 notu boş). Bu satırlar karar alanı kayıtta olmadan Ç175'ten alındı: kayıtta yok kısmı doğrulanamadı.
4. Kayıtta sonuç / karar olmayan (not alanı boş ya da 'karar yazılmadı') çalışmalar: Ç52, Ç53, Ç54, Ç74, Ç81, Ç82, Ç83, Ç87, Ç90. Bunlar ölçüldü mü, hangi sonuç çıktı, kayıtta yok; kasa adayı yapılmadı.
5. Kayıtta n (örneklem) hiç yazılı olmayan 118 gerçek hipotez satırı var: Ç01, Ç02, Ç03, Ç04, Ç05, Ç06, Ç09, Ç11, Ç12, Ç13, Ç14, Ç15, Ç16, Ç17, Ç18, Ç19, Ç22, Ç23, Ç24, Ç25, Ç26, Ç27, Ç28, Ç29, Ç30, Ç31, Ç32, Ç33, Ç34, Ç35, Ç36, Ç37, Ç38, Ç39, Ç41, Ç43, Ç44, Ç45, Ç46, Ç47, Ç49, Ç50, Ç51, Ç52, Ç53, Ç54, Ç55, Ç56, Ç57, Ç58, Ç59, Ç60, Ç61, Ç62, Ç65, Ç66, Ç67, Ç68, Ç69, Ç70 .... Bunlar B* (güç bilinmiyor) sayıldı; K8 gereği n olmadan karar sağlam değil.
6. Aynı kayıt iki farklı cetvelle iki farklı karar taşıyor: Ç37 / Ç181 (D9: 'ADAY' → 'İZ DEĞİL'); Ç75 / Ç78 / Ç179 (düzgün dip, iki yuvarlama: eski 'İZ DEĞİL' → ORTAK_CETVEL 'ÖLÇÜLEMEDİ / PİYANGO'); Ç96 / Ç178 (K24: eski 'İZ DEĞİL' → 'ÖLÇÜLEMEDİ'). Tabloda eski etiket korundu, yeni hüküm 'ana sayı' sütununda.
7. Ç203 pozitif kontrol (momentum ALT onda h5 +5,3) h5'in oynaklığı ödüllendirdiğini gösterdi; Ç204 CETVEL2 R15 ile Ç194-Ç202'yi yeniden koştu (66 etiket değişti, KATKI+ 0). Ama Ç190-Ç193 yeniden koşulmadı ve Ç124-Ç131 '+%8 önce' cetveli de h5 akrabası: bu satırlarda etiketler h5'e dayanıyor. İlk kart taslağım Ç193 / Ç196 / Ç197 / Ç201 / Ç202 sayılarını 'en yakın' diye öne almıştı; Ç204 geldikten sonra bunlar düşürüldü ya da Ç204 notuyla işaretlendi (kayıttaki Ç193 'en yakın aday' ifadesi Ç204 öncesidir; Ç193 R15 ile yeniden koşulmadı, ancak Ç204 (3) 'Ş1 dipte' sonucu aynı çekirdeği kapsıyor).
8. K58 yalnız Ç100-Ç151 için yazıldı (IK_ILERI ilk satır); Ç01-Ç98'in eski tek cetveli (önce +%20 ≥ 1,3 kat) için güç ölçülmedi. Bu satırlar B* sayıldı (kayıt: Ç175 yalnız 'en az 20 kayıt' diyor, listesi yukarıdaki Ç38-Ç90 aralığı).
9. CLAUDE.md 'Test ve bulgu standardı' karar hücrelerini iki kez tanımlıyor: 26 Ekim (BIST 2023, BIST 2024-26, ABD 2023, ABD 2024-26) ve 28 Ekim 'KARAR HÜCRELERİ DEĞİŞTİ' (ABD + AVR dört hücre, BIST bilgi). 26-28 Ekim arası kayıtlar (Ç99-Ç111) eski dört hücre dilini kullanıyor; eski 'iz yok' satırları aynı ölçütle karşılaştırılamaz (kayıtta yazılı hücre kümesi satırdan satıra değişiyor).
10. SINYAL_ENVANTERI '120 satır' diyor ve tablo A-bölümünde 120 satır ayrıştırıldı (uyuşuyor); ama K60 olasılık tablosundaki ayrı sinyal sayısı 84, K60 kaydı (Ç154) '77 sinyal + 12 bileşik' diyor: 120 - 77 = 43 satırın K60'a girmeme nedeni kayıtta tek tek yazılı değil (veri YOK 4; geri kalanı kayıtta yok).

## KONTROL LİSTESİ (python IZ_KARNE.py kontrol; bu iş derleme olduğu için yalnız ilgili satırlar dolduruldu)

| madde | durum | kanıt |
|---|---|---|
| K1 kontrol grubu | UYGULANMAZ | yeni ölçüm yok |
| K2 geleceğe bakma | EVET | yeni ölçüm yok; kart taslaklarında "t'de bilinir" tanım alanı ayrı yazıldı; Ç75 / Ç78 geleceğe bakma düzeltmeleri satırında işaretli |
| K3 geçerli bar | UYGULANMAZ | ölçüm yok |
| K4 tekilleştirme | UYGULANMAZ | ölçüm yok |
| K5 giriş fiyatı | UYGULANMAZ | ölçüm yok |
| K6 veri birimi | UYGULANMAZ | veri okunmadı |
| K7 hayatta kalma | EVET | K60 / Ç155 / Ç154 satırlarında "yalnız yaşayanlar" yazıldı |
| K8 örneklem ve dönem | EVET | n < 1.000 → B sınıfı (K58 / Ç175); n kayıtta yoksa "kayıtta yok / B*"; n < 30 hücreler kart taslağında yazılı |
| K9 ön kayıt | UYGULANMAZ | ön kayıt değil derleme; kartlar ön kayıt değildir (kasa öncesi ana model sabitler) |
| K10 ayrıştırma | EVET | ana tablo IK_KAYIT'tan mekanik; IK_KAYIT 204, tablo 208 satır (Ç173 / Ç181 / Ç182 bölünmesi); DS 87 / 87, K60 126 çift, kural defteri A-J 140 + K 51, Ç204 R15 etiketi cetvel2 YENIDEN_KOSU.md bölüm 4'ten (yalnız okundu) sayıldı; rastgele 3 satır kayıt metniyle elle karşılaştırıldı (Ç203, Ç181, Ç154) |
| K11 yeniden üretim | UYGULANMAZ | ölçüm yok |
| K12 ifade | EVET | sayı ile yorum ayrı sütunda; "iz" sözü yalnız kayıttaki etiketten; hiçbir satır İZ yazılmadı |
| K13 süreç | EVET | yasak defter dosyalarına, .py modüllerine, cetvel2 / KASA dosyalarına dokunulmadı; yeni dosya yalnız hipotez_envanteri.py ve HIPOTEZ_ENVANTERI.md; e-posta / anahtar yok |
| K14 boyut | UYGULANMAZ | öneri işi değil |

