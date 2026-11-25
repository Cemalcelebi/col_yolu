# ES_ON_KAYIT — K47 eş kirliliği (Cemal'in itirazı, 25 Kas 2026)

Yazıldı: 2026-11-25T05:11:14Z (MACD_UYUM_ES v1.0 (2026-11-25): K47 eş kirliliği (ham U1 durumu taşıyan eşler) payı ve temiz eşle yeniden ölçüm; açık veri). Getirisiz: bu dosyada yeni getiri / fark / hüküm YOK (D2 yalnız Ç217'nin yayımlanmış satır değerlerini yeniden üretir; D4 yalnız eşitlik sayısı).

## SHA

- kod: cf11efdb57c4c78bcf0b45dd41d9b14d321939d13fe429aa19138105ab6685a8
- esik: cead08e439b0bf74411630c73ed6dd96630112fe146bbedd91d0cbc3f75df7b9
- MACD_UYUM.py: a8b37d06e9d8efee749f5b30dd26932d081fcc6d02f468cf94acb71b68fffbd0
- CETVEL2.py: 2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6
- uyum_olay: 7b6720b895b0fa899f3e7a005025e2e85383e0ea03228d9e466dfb2e3fe9a29d
- uyum_satir: c8964b7bc42d19b42c27675f49fa7f5c893c18e90ad5dfd5ef636fdeb9c41df2
- V_ABD: e96a5728320e59ef51b340aa092e227a9f42ee457a41ae4ce460df7afece238b
- V_AVR: 0c47dd662dcf90f49b3bcfac7f46d32519e655f1914737dec8738165564907c0
- V_BIST: d6e9466e3c4577d5f0b194f0c4df0d4a4e9227e0b72079561f3704eb8f66c529
- kod commit (MACD_UYUM_ES.py): ffd448bc486a63464725be085f42d96000bc5685 2026-11-25T08:10:06+03:00
- eşik sözlüğü (ES_ESIK) sha: cead08e439b0bf74411630c73ed6dd96630112fe146bbedd91d0cbc3f75df7b9
- KASA: açık kesik 2022-12-31, mühür f674b4ee291c2f35, açılan []

## TANIMLAR (iş tanımı aynen)

- HAM U1 DURUMU: MU.mu_hisse kosul['U1'] maskesi (S10 ∧ F68 ∧ DİPTE; aday gün tanımıyla) doğru olan bütün barlar; dip başına ilk gün ve 15 bar aralığı UYGULANMADAN. HAM S10F68: aynı, DİPTE şartsız (kosul['U1b']).
- K20 (ANA): eşin b-20 .. b-1 barlarından en az birinde ham U1. K1 (bilgi): b-1'de ham U1. KG (bilgi): b-20 .. b-1'de en az bir ham S10F68.
- BARIZ = U1 ∧ F65 <= -0,05 (uyum_satir.csv.gz). Hücreler: ABD / AVR x d1619 / d2022 KARAR; BIST BİLGİ.

## UYGULAMA YORUMLARI (ölçümden önce)

- b = eşin hazır (geçerli bar) serisinde tarihi d'den küçük bar sayısı. Eş havuzda olduğu için d'de geçerli barı vardır; b onun sırasıdır.
- Olay kümesi Ç217 c2_olc22 ile aynı: uyum_olay U1 -> c2_olay (tekil 15); eş kümesi c2_es (olayların kendisi dışarıda). D2 bunu birebir denetler.
- Kirli eş sayısı = Ç217 eş kümesinde (olay çiftleri dışarıda) bayraklı üye sayısı; pay = kirli / n_es; A tablosu yalnız Ç217'de ölçülen olaylar (n_es >= 5, R15 sonlu).
- Olay hissesinin kendisi de giriş günü d'de K1 / K20 kirlidir (sinyal günü t = b-1 ham U1); Ç217'de zaten eş dışıydı.
- Temiz eş: Ç217 dışlaması + olay günlerindeki bütün K20 (bilgi: KG) kirli havuz çiftleri; en az 5 temiz eş; az kalan olay düşer (sayısı yazılır).
- Hüküm tohumları: U1 = Ç217 (100000 + pazar sırası x 100 + dönem sırası), BARIZ = Ç219 (300 + 10 x pazar sırası + dönem sırası); eski ve temiz aynı tohumla.
- C (bilgi): bütün havuz (bütün günler). İkinci satır (bilgi, önceden yazılı): Ç217 U1 olay çiftleri havuzdan çıkarılarak.
- D3: pazar başına 30 çift Ç217 eş üyeliklerinden; yarısı K20 kirli (yeterliyse), yarısı temiz (kirli bayrağı da sınansın diye).
- D: uyarı eşiği |F15 kirli - temiz| > 0,05 ya da |ATRP kirli / temiz - 1| > %10.

## DOĞRULAMALAR (D1-D4; hepsi tuttu, tutmasaydı DURURDU)

- ABD: D1 olay dosyası 4716 = ham üretim 4716 (ortak 4716) TUTTU; D2 3266 olay (ölçülen 3210) es_r15 / n_es / fark / sıra göreli 1e-9 TUTTU; D3 30 / 30 çift (kirli 15) TUTTU; D4 40 / 40 karşılaştırma (20 olay x eski / temiz) TUTTU
- AVR: D1 olay dosyası 1798 = ham üretim 1798 (ortak 1798) TUTTU; D2 1499 olay (ölçülen 1394) es_r15 / n_es / fark / sıra göreli 1e-9 TUTTU; D3 30 / 30 çift (kirli 15) TUTTU; D4 40 / 40 karşılaştırma (20 olay x eski / temiz) TUTTU
- BIST: D1 olay dosyası 1486 = ham üretim 1486 (ortak 1486) TUTTU; D2 1073 olay (ölçülen 982) es_r15 / n_es / fark / sıra göreli 1e-9 TUTTU; D3 30 / 30 çift (kirli 15) TUTTU; D4 40 / 40 karşılaştırma (20 olay x eski / temiz) TUTTU

## A. KİRLİLİK PAYI (getirisiz)

| grup | pazar | hücre | bayrak | n olay | pay ort | pay medyan | pay %90 | >= 1 kirli eşli olay | pay >= %25 olay | taban (havuz) |
|---|---|---|---|---|---|---|---|---|---|---|
| U1 | ABD | d1619 | K20 | 1279 | %15,6 | %14,3 | %30,0 | %90,2 | %21,1 | %4,9 |
| U1 | ABD | d1619 | K1 | 1279 | %6,8 | %5,0 | %16,1 | %72,2 | %3,2 | %1,9 |
| U1 | ABD | d1619 | KG | 1279 | %28,2 | %27,3 | %46,5 | %98,4 | %58,1 | %13,8 |
| U1 | ABD | d2022 | K20 | 1893 | %22,1 | %21,2 | %41,5 | %96,2 | %39,5 | %7,8 |
| U1 | ABD | d2022 | K1 | 1893 | %9,7 | %7,1 | %23,7 | %87,4 | %8,5 | %3,1 |
| U1 | ABD | d2022 | KG | 1893 | %32,4 | %30,8 | %54,5 | %99,7 | %66,3 | %15,9 |
| U1 | AVR | d1619 | K20 | 631 | %17,1 | %14,3 | %34,2 | %85,1 | %27,6 | %4,9 |
| U1 | AVR | d1619 | K1 | 631 | %8,2 | %5,3 | %22,7 | %67,4 | %8,1 | %1,9 |
| U1 | AVR | d1619 | KG | 631 | %31,8 | %30,4 | %52,2 | %98,3 | %64,2 | %16,0 |
| U1 | AVR | d2022 | K20 | 636 | %16,2 | %14,3 | %30,1 | %90,4 | %17,5 | %6,0 |
| U1 | AVR | d2022 | K1 | 636 | %7,4 | %6,0 | %17,1 | %75,3 | %2,7 | %2,4 |
| U1 | AVR | d2022 | KG | 636 | %26,5 | %26,0 | %42,9 | %97,2 | %56,6 | %14,8 |
| U1 | BIST | d1619 | K20 | 659 | %23,5 | %20,0 | %51,7 | %87,4 | %40,4 | %7,9 |
| U1 | BIST | d1619 | K1 | 659 | %11,5 | %7,1 | %30,4 | %64,5 | %16,8 | %3,2 |
| U1 | BIST | d1619 | KG | 659 | %34,3 | %32,0 | %61,4 | %96,2 | %64,9 | %16,7 |
| U1 | BIST | d2022 | K20 | 320 | %18,5 | %17,5 | %35,3 | %86,9 | %30,9 | %4,5 |
| U1 | BIST | d2022 | K1 | 320 | %8,5 | %6,5 | %18,3 | %66,2 | %5,3 | %1,8 |
| U1 | BIST | d2022 | KG | 320 | %33,9 | %33,3 | %57,1 | %96,6 | %66,6 | %11,0 |
| BARIZ | ABD | d1619 | K20 | 505 | %16,6 | %14,6 | %30,4 | %91,7 | %24,0 | %4,9 |
| BARIZ | ABD | d1619 | K1 | 505 | %7,1 | %5,4 | %16,7 | %76,8 | %2,8 | %1,9 |
| BARIZ | ABD | d1619 | KG | 505 | %27,1 | %26,7 | %44,1 | %98,2 | %55,4 | %13,8 |
| BARIZ | ABD | d2022 | K20 | 848 | %22,9 | %22,5 | %40,1 | %98,0 | %41,2 | %7,8 |
| BARIZ | ABD | d2022 | K1 | 848 | %10,1 | %7,4 | %23,7 | %91,0 | %7,9 | %3,1 |
| BARIZ | ABD | d2022 | KG | 848 | %32,8 | %31,7 | %54,5 | %99,9 | %69,2 | %15,9 |
| BARIZ | AVR | d1619 | K20 | 189 | %18,2 | %15,8 | %37,7 | %90,5 | %33,3 | %4,9 |
| BARIZ | AVR | d1619 | K1 | 189 | %9,4 | %6,5 | %23,5 | %76,7 | %8,5 | %1,9 |
| BARIZ | AVR | d1619 | KG | 189 | %30,1 | %28,6 | %50,0 | %100,0 | %58,7 | %16,0 |
| BARIZ | AVR | d2022 | K20 | 260 | %16,2 | %14,4 | %29,4 | %92,3 | %16,9 | %6,0 |
| BARIZ | AVR | d2022 | K1 | 260 | %8,0 | %6,9 | %17,1 | %80,8 | %3,1 | %2,4 |
| BARIZ | AVR | d2022 | KG | 260 | %26,1 | %26,0 | %41,9 | %98,1 | %57,3 | %14,8 |
| BARIZ | BIST | d1619 | K20 | 271 | %23,0 | %19,0 | %50,0 | %86,0 | %39,5 | %7,9 |
| BARIZ | BIST | d1619 | K1 | 271 | %11,4 | %7,1 | %29,2 | %66,1 | %15,1 | %3,2 |
| BARIZ | BIST | d1619 | KG | 271 | %33,3 | %30,8 | %62,5 | %94,8 | %63,1 | %16,7 |
| BARIZ | BIST | d2022 | K20 | 114 | %15,5 | %13,5 | %32,8 | %84,2 | %21,9 | %4,5 |
| BARIZ | BIST | d2022 | K1 | 114 | %7,0 | %4,9 | %16,7 | %62,3 | %2,6 | %1,8 |
| BARIZ | BIST | d2022 | KG | 114 | %30,0 | %28,6 | %50,0 | %96,5 | %57,9 | %11,0 |

Taban = bütün eş havuzunda (bütün günler, pazar x dönem) bayraklı (d, hisse) payı.

## BEKLENTİ (sonuçtan önce)

Kirli eşler olayla aynı etkiyi taşıyorsa, kirli pay p iken ölçülen fark ≈ (1 - p) x gerçek fark olur; kirlilik farkı küçültür, p %100'e yaklaşmadıkça sıfırlamaz. Yukarıdaki A tablosu p'yi verir; Ç217 farkları ±0,4 puan civarında olduğundan p küçükse temiz eşle farkın anlamlı büyümesi beklenmez.

## KARAR KURALI (sonuçtan sonra değişmez)

- EŞ KİRLİLİĞİ SONUCU DEĞİŞTİRDİ <=> temiz eşle (K20) U1'in 4 karar hücresinin (ABD / AVR x d1619 / d2022) HEPSİNDE hüküm TUTAR (plasebo hariç şartlar: n >= 30, güç >= 0,80, FARK > 0, FARK boot alt > 0, SIRA > 0,50, SIRA boot alt > 0,50, L3O > 0). BARIZ için ayrı satır, aynı kural. Aksi halde DEĞİŞTİRMEDİ. Her hücrede FARK_temiz - FARK_eski yazılır.
- Açık veriye K47 için 4. bakış: TUTAR çıksa bile keşiftir; kesin hüküm yalnız KASA körüyle (Cemal kararı). Bir hücre TUTAR çıkarsa iddiadan önce plasebo kapısı gerekir; raporda 'plasebo koşulmadı' yazılır.
- Evren yalnız bugün işlem görenler: sonuç yukarı yanlı (K7).

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt; HAYIR ya da boş = kos çalışmaz)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = Ç217 c2_es aynen (aynı giriş günü d, aynı ATRP x likidite x F15 kovası, aynı R15 açılıştan 15. bar kapanışı); taban = Ç217 eş ortalaması; temiz eşte yalnız K20 kirli çiftler ek dışlanır (c2_es exc_d / exc_j); mekanik fark denetimi: D bölümü (kirli / temiz eş F15 ve ATRP); 200 eş portföy plasebosu bu işte KOŞULMADI (hüküm plasebo hariç, raporda yazılı) |
| K2 | geleceğe bakma | EVET | bayraklar yalnız b-20 .. b-1 barlarından (b = d'den önceki geçerli bar sayısı, searchsorted tarih < d); ham durum mu_hisse yapı taşlarıyla (dipler [t-60, t-1], MACD [t-250, t]); D3: pazar başına 30 (d, eş) çifti veri d'den önce kesilip yeniden -> aynı; kova / evren Ç217 paneli; KASA açık kesik 2022-12-31 |
| K3 | geçerli bar | EVET | ham durum YH._yh_hazir geçerli barlarında (H > L, V > 0); b geçerli bar sayısı; eş havuzu CETVEL2 (P ok, H >= 0, R15 sonlu) |
| K4 | tekilleştirme | EVET | olaylar Ç217'nin aynısı (dip başına ilk gün + aynı hissede 15 bar + c2_olay tekil 15; 60 gün kuralı Ç217 tanımında yok, tanım değişmez); n = ölçülen olay; her olay bir kez; kirlilik payında ortalama + medyan + %90 birlikte |
| K5 | giriş fiyatı | EVET | giriş = sinyalden sonraki ilk işlem günü açılışı (c2_olay / OC, Ç217 aynen); R15 = 15. geçerli bar kapanışı / E0 - 1 |
| K6 | veri birimi | EVET | V_*.pkl açık kısım tek kip (sha ön kayıtta); R15 / ATRP / F15 oran; bölünme şüphesi havuz dışı (OC, Ç217 aynen) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler: batanlar yok -> sonuç yukarı yanlı okunur; raporda yazılı |
| K8 | örneklem ve dönem | EVET | n < 30 ya da güç < 0,80 ÖLÇÜLEMEDİ (mu_hukum); iki alt dönem d1619 / d2022 ayrı hücre; tek önceden yazılı karar kuralı (BH gerekmez, çoklu bilgi satırları hüküm taşımaz); küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | ES_ON_KAYIT.md: ES_ESIK sha + MACD_UYUM_ES.py sha + bağımlı kod ve veri sha'ları + D1-D4 + A tablosu + karar kuralı; kos kapısı: ön kayıt git'te işlenmiş ve değişmemiş, sha'lar aynı, ik_kontrol_kapisi, KASA kapısı, es_sonuc.json yok |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber ayrıştırması yok; yalnız OHLCV ve Ç217 satır / olay dosyaları (D1 / D2 ile birebir denetlendi) |
| K11 | yeniden üretim | EVET | raporda >= 2 hücre (U1 ABD d1619 ve AVR d2022 temiz FARK / n) es_satir.csv.gz'den bağımsız düz pandas ile yeniden üretilir (göreli 1e-9); tutmazsa DURUR |
| K12 | ifade | EVET | hüküm yalnız önceden yazılı kuralla (DEĞİŞTİRDİ / DEĞİŞTİRMEDİ; hücre TUTAR / TUTMADI / ÖLÇÜLEMEDİ); C ve D bilgi; 'iz / emare' sözü yok; sayı ile yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_es; es_ / ES_ önekleri; test); yasak dosyalar ve mevcut macd_uyum çıktıları değişmez (git diff); KASA bloğu açılmaz; e-posta / anahtar taraması YH._yh_yaz; push yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | bu işte alım-satım önerisi yok; ölçüm |
