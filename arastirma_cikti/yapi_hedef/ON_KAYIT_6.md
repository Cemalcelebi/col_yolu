# YAPI_HEDEF — ÖN KAYIT 6 (6. tur: GRUPLAR G1 / G2 / G2u / G3 + FİLTRE KARNESİ + MAHKEME)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo; 6. tur eklendi (YAPI_HEDEF_IS_TANIMI_6.md)

- YH_ESIK6_SHA: `6f05f68cd07560e407c7d1b06431990704b79441c51f4e09bbddfafba4086410` (6. tur eşikleri: gruplar, fark, karne, mahkeme)
- YH_ESIK_SHA: `bde83033af9c3a4d1f293278679ff33d7739dfc783a1b75fb391f49399d644a9` (= ON_KAYIT_5.md YH_ESIK_SHA: Y1-Y11c, cetvel, karar ve etiket kuralı AYNEN)
- YH_KOD_SHA: `f3dbc97aafdfeba01cced3ab5355325c9b271664b1f78f12d315820ef44c76c4` (YAPI_HEDEF.py)
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb` (ORTAK_CETVEL.py)
- S6_KOD_SHA: `ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d` (S6_TABAN.py)
- GE_FN_SHA: `9b6c86fdd23a34b653a611d34cc97a145f41d92c061d2e4665dec85e45f669e6` (GOZ_ETIKET ge_s6 + ge_bolge + ge_ozellik_bar + GE_ESIK 'ozellik' kaynak metni; dosyanın geri kalanı başka ajanca değişebilir, 6. tur yalnız bunlara dayanır)
- GUC_SHA: `b7b63dbdbbf6305744e226d4095cc2154c14fbbe8b2ca84545cab8b27436a913` (guc_tablosu.json, 1. tur)
- OZELLIK_SHA: `bae156939290b421fb2320f85a2639db71726ca6f7449081e2bc292f5043fd76` (goz_etiket/ozellik_Y1.csv.gz; F1-F18)
- S7_OZELLIK_SHA: `9463e08e6bb7eb95820eccc9be9dcb3a1d549312dc62cdcc657b2a2b02e6137d` (ozellik_Y1_s7.csv.gz; F20-F23)
- S9_OZELLIK_SHA: `c9a6a4e62673fcc56cc82550c915feed3be4b7235ada8a940d4de09ff0f28756` (ozellik_Y1_s9.csv.gz; F24-F29)
- Y1_OLAY_SHA: `e13eb12699a6d749bccc16ee4cde5ac467ea2bf8687b23a6a821fef74bf8871b` (olay_Y1.csv.gz; regresyon)
- Y9_OLAY_SHA: `56aa6101aba25cddd66dedddcba3d536a05b8e0850b727f015ef3cec295d5809` (olay_Y9.csv.gz; tutarlılık kapısı)
- Y9C_OLAY_SHA: `8ff73448ff90ed80d3b97447b8139056188e471fa7ec9b786da5963ad25a020a` (olay_Y9c.csv.gz; tutarlılık kapısı)
- G3_SHA: `0ebb505ee9da6e124ff570e32dd68ae87ef3c57eb5ef282cd6132834fd9dadab` (grup6_G3.csv; rastgele grup örneklemi, getirisiz)
- S7PDF_KOD_SHA: `3d906755724772d0aa9ace4f2c5a95bcb6f8ef768b615b5d87b8166cd1ef6308` (s7_bolge_pdf.py; mahkeme 50 olay sırası)
- ON_KAYIT_5: git 146e2785b7, ?
- IS_TANIMI_6: git 5f9ea6dc9e, ?
- ZAMAN (UTC): `2026-11-19 07:42:11 UTC`

Bu dosya 6. tur A ölçümünden ÖNCE yazıldı. Gruplar için alt ajan hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri / konum eşli oran hesaplamadı ve okumadı: aşağıdaki sayılar yalnız olay_Y1.csv.gz'nin kimlik + dönem sütunları ve mühürlü özellik dosyalarından (getirisiz). `python YAPI_HEDEF.py grup6` bu dosyanın kontrol listesini, sha'larını, git kaydını ve Y1-Y11c mührünü denetler; biri tutmazsa durur. Eşikler sonuç görüldükten sonra değişmez. B (filtre karnesi) getiri okur ama eşik seçmez (raporlama); C (mahkeme) getirisizdir.

## İŞ TANIMI 6 §A / §B / §C (AYNEN)

### A
- G1 TREND İÇİ RAF: F14 >= 0 (250 bar dip noktaları yükseliyor) VE F15 >= 0,50 (120 günün üst yarısı).
- G2 DÜŞÜŞ SONRASI DİP: Ş1 (F15 <= 0,25 VE F17 <= -0,20). G2u alt grubu: G2 VE Ş9 (U dip).
- G3 RASTGELE: her hücrede (pazar x dönem) Y1 olaylarından tohum 106 ile G2 ile aynı n (G2 n'si hücrede 0 ise G3 de 0); ayrıca G0 = bütün Y1 (taban).
- Ölçü: aynı 15 bar cetveli (h5 / h10 / st5, eş payı, KAT5 ay kümeli %95, konum eşli KAT, plasebo); hücreler ABD / AVR / BIST x 2016-22 / 2023 / 2024-26 (hepsi tabloya; karar etiketi ABD / AVR 2023 ve 2024-26 'bakılmış' notuyla, önceki turlar gibi). OLASILIK TABLOSU Cemal biçimi: grup | hücre | n | +%5 payı | eş payı | KAT | stop payı. Gruplar arası fark: G2 − G1 ve G2 − G3 (P olay), bootstrap %95.
- Y9 / Y9c ile tutarlılık kapısı: G2 = Y9 olay kümesi (aynı satırlar), değilse DUR.

### B
- Filtre sırası (ders sırası): Ş1 dipte, Ş2 hat net, Ş3 dip savunulmuş, Ş4 küçük mum, Ş5 alt fitil, Ş6 kazan dönüş, Ş9 U dip, Ş7 yakın tavan gövdeli kırılım, Ş8 yol almamış, F14 büyük resim. Her adımda huniye eklenir (önce Ş1, sonra Ş1+Ş2, ...; Ş6 ve Ş9 ayrı kollar: S7 kolu Ş6'lı, U kolu Ş9'lu).
- Her adım için her pazarda: n, P(+5) olay, P eş, FARK = olay − eş, ve MARJİNAL = FARK(bu adım) − FARK(önceki adım). İKİ DÖNEM: EĞİTİM 2016-22, SINAMA 2023-26 (ve tersi: eğitim 2023-26, sınama 2016-22). Etiket (sabit): KATKI+ = marjinal > 0 iki dönemde de VE adım n >= 30 iki dönemde de; KATKI− = marjinal < 0 iki dönemde de (n >= 30); SORGULA = dönemler çelişiyor ya da n < 30 (bu filtre 'son uygulanan ve kötü çıkan' adayıdır). Ayrıca TEK-ÇIKARMA: tam S7 (ve tam U kolu) kümesinden her filtre tek tek çıkarılınca FARK nasıl değişiyor (hangi filtre zarar veriyor).
- Çıktı: FILTRE_KARNE.md (tablo: filtre | kol | eğitim n / fark / marjinal | sınama n / fark / marjinal | etiket) + filtre_karne.json; en alta otomatik cümle: 'SORGULANACAK FİLTRELER: …' (etiket SORGULA ve KATKI− olanlar, en son eklenenden geriye). Bu dosya her yeni ders / filtre eklendiğinde AYNI komutla yenilenir (`python YAPI_HEDEF.py filtrekarne`).

### C
- Girdi: (pazar, sembol, t) Y1 olayı. Yalnız [t-250, t] barları.
- (1) KURAL TABLOSU: seçilen bölge için her kural ✓ / ✗ + ölçülen değer + eşik: Ş1 dipte, Ş2 hat net, Ş3 dip savunulmuş, Ş4 küçük mum, Ş5 alt fitil, Ş6 kazan dönüş, Ş9 U dip (F24-F29), Ş7 yakın tavan + gövdeli ortalayan kırılım, Ş8 yol almamış, F14 büyük resim, C8 kağıt hafızası (F16 son 250 barda KIRILDI bölge sayısı; 0 = ✓), C13 dev mum (son 250 barda |günlük kapanış getirisi| > 4 x ATR250 olan gün var mı; yoksa ✓). PUAN = ✓ sayısı / kural sayısı.
- (2) ÖNCEKİ ADAYLAR: aynı hissede [t-250, t-1] içinde (a) S6'nın gördüğü bütün bölgeler (S6.s6_taban çıktısında kutu bitişleri: AL, KIRILDI, zaman aşımı; her birinin kendi 't_k' = kutunun son günü / al günü) ve (b) Ş9 çanak uyumunun kaydırılmış pencerelerde (t-120 .. t-5, adım 5) tuttuğu günler. Her aday için aynı kural tablosu, aynı puan (bilgi yalnız adayın kendi gününe kadar).
- (3) KARAR: seçilen bölgenin puanı >= en iyi önceki adayın puanı ise 'SEÇİM TUTARLI'; değilse 'ÖNCEKİ BÖLGE DAHA UYGUN: bar -k, puan a/b vs c/d, seçilenin tutmadığı kurallar: …, önceki adayın tutmadığı: …'. Ayrıca 'seçilen bölge her kurala uyuyor mu': tam puan değilse eksik kurallar listesi.
- (4) Çıktı: düz metin tek sayfa (Türkçe) + json; komut `python YAPI_HEDEF.py mahkeme --pazar ABD --sembol X --tarih YYYY-MM-DD` ve toplu `--liste dosya.csv`. Toplu koşular: (i) S7 PDF'indeki 50 olay (s7_bolge_pdf.s7b_olaylar(104)) -> arastirma_cikti/yapi_hedef/S7_MAHKEME.md (sayfa No ile; sembol / tarih yok); (ii) TUR 4'ün 40 sayfası (tur/4/tur_4_anahtar.json hazır olunca; hazır değilse atla ve rapora yaz) -> tur/4/TUR_4_MAHKEME.md (sayfa no ile, sembol / tarih yok, SONUÇ YOK: kör; h5 okunmaz). Özet: kaç olayda 'ÖNCEKİ BÖLGE DAHA UYGUN', en sık eksik kurallar.
- (5) KAPILAR: önceki adayların kural değerleri yalnız kendi günlerine kadarki veriyle (prefix testi: veri t_k'da kesilince aynı değer); seçilen bölge Ş-şartları ozellik dosyalarıyla birebir (regresyon); mahkeme çıktısında sembol / tarih sızıntısı 0 (toplu md'ler).

## TANIMLAR ve EŞİKLER (YH_ESIK6; uygulama kararları dahil)

- G0 BÜTÜN Y1 (taban): bütün Y1 OLAYLARI (olay_Y1.csv.gz satırları = özellik dosyası satırları).
- G1 TREND İÇİ RAF: Y1 olayı VE F14 >= 0 VE F15 >= 0,50 (NaN tutmaz).
- G2 DÜŞÜŞ SONRASI DİP: Y1 olayı VE Ş1 (F15 <= 0,25 VE F17 <= -0,20) = Y9 kümesi.
- G2u DİP + U: G2 VE Ş9 (YH_ESIK Y11 eşikleri, altı alt şart; NaN tutmaz).
- G3 RASTGELE: her (pazar, dönem) hücresinde Y1 OLAY satırlarından (olay_Y1.csv.gz; dönem = giriş günü dönemi) yerine koymadan G2'nin aynı hücredeki OLAY satırı sayısı kadar; satırlar (sembol, tarih) sırasında; rng = default_rng([106, pazar no, dönem no]); G2 0 ise 0; G2 olaylarını da içerebilir; örneklem ön kayıtta grup6_G3.csv (sha) ile mühürlü (getirisiz: yalnız kimlik + dönem).
- ÖLÇÜ: 1. tur 15 bar cetveli AYNEN: olay ölçümü = Y1 ölçümü (yh_olc_pazar deneme 'Y1'; eş / taban / plasebo tohumu Y1'inki; satırlar olay_Y1.csv.gz ile regresyon, plasebo dahil) -> grup satırları Y1 satırlarının alt kümesi; hücre: yh_hucre (h5 / h10 / st5 olay, eş, KAT5 ay kümeli %95, plasebo) + yh_hucre_konum (konum eşli KAT, yh_konum_es_olc); hücre kuralı ve durum (yh_durum, güç tablosu 1. tur) ve etiket 3. tur kuralı (yh_etiket + yh_etiket3: ABD / AVR 2023 ve 2024-26 BAKILMIŞ -> en fazla EMARE; dış sınama ABD / AVR 2016-22; TERS iki yönlü); hücreler ABD / AVR / BIST x 2016-22 / 2023 / 2024-26.
- GRUP FARKI: FARK = P(+%5) olay (G2) - P(+%5) olay (Gx), ölçülen olaylar (h5 ve eş h5 var: yh_hucre n'i); %95 aralık: iki grupta AYRI ay kümeli bootstrap (giriş ayı, yerine koyarak, 2000, rng [66, pazar no, dönem no, çift no]); BİLGİ (karar kuralı yok).
- TUTARLILIK KAPISI: G2 (pazar, sembol, tarih) kümesi = olay_Y9.csv.gz kümesi VE h5 / h10 / st5 / es_h5 / es_st5 / n_es / tb_h5 / getiri / k_es_h5 / k_es_st5 / k_n_es eşit (göreli 1e-4, NaN = NaN); G0 ∩ F15 >= 0,75 kümesi = olay_Y9c.csv.gz kümesi (aynı sütunlar); değilse DUR.
- GELECEĞE BAKMA: her grup x pazar: yh_gelecek5 (5 rastgele olay; veri t'de kesilir; Y1 sinyali + F1-F29 kesik veriden = dosya; değilse DUR).
- KARNE: Huni Y1 (adım 0) -> + filtre (kol sırasıyla; Ş1-Ş5 iki kolda ortak). Her adım x pazar x dönem: n = ölçülen olay (h5 ve eş h5 var), P olay = ort h5, P eş = ort es_h5, FARK = P olay - P eş, MARJİNAL = FARK(adım) - FARK(önceki adım). EĞİTİM 2016-22, SINAMA 2023-26 (2023 + 2024-26); tersi (eğitim 2023-26, sınama 2016-22) aynı iki sayıyı kullandığı için etiket simetriktir.
- KARNE ETİKETİ: KATKI+ = marjinal > 0 iki dönemde VE adım n >= 30 iki dönemde; KATKI− = marjinal < 0 iki dönemde VE n >= 30 iki dönemde; değilse SORGULA (dönemler çelişiyor ya da n < 30).
- TEK-ÇIKARMA: TAM kol kümesi (kolun bütün filtreleri) ve her filtre tek tek çıkarılınca: DELTA = FARK(tam - f) - FARK(tam), iki dönem; DELTA > 0 iki dönemde (n >= 30 iki dönemde) -> ZARAR VERİYOR; DELTA < 0 iki dönemde -> YARARLI; değilse BELİRSİZ.
- SORGULANACAK FİLTRELER: karar pazarı satırlarında (ABD+AVR) etiketi SORGULA ya da KATKI− olan (filtre, kol) çiftleri, kolda en son eklenenden geriye; ayrıca tek-çıkarmada ZARAR VERİYOR olanlar.
- KARNE KOLLARI: S7 = S1 -> S2 -> S3 -> S4 -> S5 -> S6 -> S7 -> S8 -> F14; U = S1 -> S2 -> S3 -> S4 -> S5 -> S9 -> S7 -> S8 -> F14; pazarlar ABD, AVR, BIST, ABD+AVR (karar pazarı ABD+AVR).
- MAHKEME GİRDİ: (pazar, sembol, t) Y1 olayı; veri t'de KESİLİR (t sonrası okunmaz); adaylar [t-250, t-1] içinde; her kural değeri yalnız kendi gününe kadarki veriyle (adayın günü t_k'dan öncesi okunur: F3 ATR250, F14 250 bar, F17 60 gün; sonrası okunmaz).
- MAHKEME KURALLARI (12): Ş1 F15 <= 0,25 VE F17 <= -0,20; Ş2 F1 >= 3; Ş3 F2 >= -0,01; Ş4 F3 <= 0,90; Ş5 F4 <= 0,25; Ş6 F20 >= 0; Ş9 altı alt şart (Y11); Ş7 F22 > 0 VE F22a < 0 VE F23 >= 0,50; Ş8 F18 <= 0,20; F14 >= 0; C8 F16 = 0 (son 250 barda KIRILDI bölge sayısı); C13 max |C_k / C_k-1 - 1| (son 250 bar, k = t-249..t) <= 4 x ATR250 (ort TR / C_önceki, aynı 250 bar; 250 bar yoksa NaN = tutmaz). NaN = ✗.
- PUAN = ✓ sayısı / 12 kural.
- ÖNCEKİ ADAYLAR (a): S6 (s6_taban, kesik veri) bölgeleri, seçilenin bölgesi hariç, son barı [t-250, t-1] içinde ve bitişi t'ye kadar bilinen: AL (t_k = al günü; bölge = GE bölgesi), KIRILDI (t_k = kırılma günü; bölge [kutu_sol, t_k-1], hat = kutu_alt(t_k), tavan = TAVAN(t_k-1)), ZAMAN AŞIMI / sönme (t_k = kutunun son günü; bölge [kutu_sol, t_k-1], hat = kutu_alt(t_k), tavan = kutu_ust(t_k)).
- ÖNCEKİ ADAYLAR (b): Ş9 çanak: t_k = t-5, t-10, ..., t-120; Ş9 t_k'da TUTARSA aday; bölge = Ş9 penceresi [t_k-40, t_k-1], hat = min Low, tavan = max High[t_k-15, t_k-1].
- ÖZELLİK HESABI: F1-F18 = GOZ_ETIKET.ge_ozellik_bar (aday için bölge sahte 'AL' olarak verilir; F16 gerçek durum dizisinden), F20-F23 = yh_s7_bar, F24-F29 = yh_s9_bar (t_k'da).
- KARAR: seçilenin puanı >= en iyi önceki adayın puanı -> SEÇİM TUTARLI; değilse ÖNCEKİ BÖLGE DAHA UYGUN (en iyi aday: en yüksek puan, eşitlikte en yakın); önceki aday yoksa SEÇİM TUTARLI (önceki aday yok). Ayrıca seçilen bölge tam puan değilse eksik kurallar.
- MAHKEME KAPILARI: prefix: her adayın kural değerleri veri t_k'da kesilince aynı (göreli 1e-9); seçilen bölgenin F1-F29 + F16 değerleri özellik dosyalarıyla aynı (göreli 1e-5); toplu md'lerde sembol / tarih sızıntısı 0.

UYGULAMA YORUMLARI (iş tanımında açık değildi; ölçümden önce yazıldı): (1) 'yalnız [t-250, t] barları' = adaylar [t-250, t-1] içinde; her kural değeri kendi gününe kadarki veriyle (öncesi okunabilir: F3 ATR250 / F14 250 bar / F17 60 gün; sonrası okunmaz); (2) Ş9 adaylarının bölgesi Ş9 penceresidir (bölge kuralları Ş2-Ş5 / F17 / F18 için bir bölge gerekir); (3) karne karar satırı ABD+AVR birleşik (karar pazarları), ABD / AVR / BIST ayrı satırlar bilgi; (4) G3 olay satırı sayısıyla eşlenir (ölçülebilirlik sonra bilinir); (5) grup plasebosu Y1'in plasebosudur (deneme tohumu 'Y1'); (6) KATKI etiketi 'tersi' yönünde aynıdır (iki dönem sayısı simetrik).

## GRUP OLAY SAYILARI (getirisiz; olay satırı = Y1 olayı, ölçülebilirlik bilinmez)

| Grup | ABD 2016-22 | ABD 2023 | ABD 2024-26 | AVR 2016-22 | AVR 2023 | AVR 2024-26 | BIST 2016-22 | BIST 2023 | BIST 2024-26 | toplam |
|---|---|---|---|---|---|---|---|---|---|---|
| G0 BÜTÜN Y1 (taban) | 8686 | 2042 | 4153 | 4496 | 815 | 1743 | 2588 | 381 | 1759 | 26663 |
| G1 TREND İÇİ RAF | 5346 | 911 | 2383 | 2683 | 380 | 1060 | 1363 | 173 | 691 | 14990 |
| G2 DÜŞÜŞ SONRASI DİP | 346 | 146 | 232 | 89 | 20 | 55 | 238 | 81 | 297 | 1504 |
| G2u DİP + U | 31 | 3 | 20 | 11 | 2 | 3 | 16 | 2 | 29 | 117 |
| G3 RASTGELE | 346 | 146 | 232 | 89 | 20 | 55 | 238 | 81 | 297 | 1504 |

## KARNE HUNİSİ (getirisiz; olay satırı; eğitim 2016-22 / sınama 2023-26)

Kol S7:

| Adım | ABD egitim | ABD sinama | AVR egitim | AVR sinama | BIST egitim | BIST sinama | ABD+AVR egitim | ABD+AVR sinama |
|---|---|---|---|---|---|---|---|---|
| Y1 | 8686 | 6195 | 4496 | 2558 | 2588 | 2140 | 13182 | 8753 |
| S1 | 346 | 378 | 89 | 75 | 238 | 378 | 435 | 453 |
| S2 | 206 | 233 | 51 | 51 | 145 | 220 | 257 | 284 |
| S3 | 176 | 217 | 44 | 44 | 135 | 194 | 220 | 261 |
| S4 | 152 | 199 | 41 | 41 | 135 | 193 | 193 | 240 |
| S5 | 71 | 100 | 22 | 25 | 85 | 159 | 93 | 125 |
| S6 | 56 | 78 | 18 | 20 | 72 | 124 | 74 | 98 |
| S7 | 32 | 38 | 9 | 12 | 40 | 76 | 41 | 50 |
| S8 | 31 | 38 | 9 | 12 | 40 | 76 | 40 | 50 |
| F14 | 8 | 12 | 1 | 3 | 14 | 40 | 9 | 15 |

Kol U:

| Adım | ABD egitim | ABD sinama | AVR egitim | AVR sinama | BIST egitim | BIST sinama | ABD+AVR egitim | ABD+AVR sinama |
|---|---|---|---|---|---|---|---|---|
| Y1 | 8686 | 6195 | 4496 | 2558 | 2588 | 2140 | 13182 | 8753 |
| S1 | 346 | 378 | 89 | 75 | 238 | 378 | 435 | 453 |
| S2 | 206 | 233 | 51 | 51 | 145 | 220 | 257 | 284 |
| S3 | 176 | 217 | 44 | 44 | 135 | 194 | 220 | 261 |
| S4 | 152 | 199 | 41 | 41 | 135 | 193 | 193 | 240 |
| S5 | 71 | 100 | 22 | 25 | 85 | 159 | 93 | 125 |
| S9 | 10 | 7 | 4 | 2 | 6 | 10 | 14 | 9 |
| S7 | 4 | 3 | 2 | 2 | 4 | 9 | 6 | 5 |
| S8 | 4 | 3 | 2 | 2 | 4 | 9 | 6 | 5 |
| F14 | 1 | 2 | 1 | 1 | 2 | 4 | 2 | 3 |

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | gruplar Y1 olay satırlarının alt kümesi; eş / taban / plasebo 1. tur kodu (yh_olc_pazar 'Y1' -> yh_olay_olc, yh_sim; aynı gün, aynı OC kovası, AYNI d, aynı hedef / takip / 15 bar); konum eşli KAT (yh_konum_es_olc: eşin F15'i olayın çeyreğinde: G1 / G2 konum farkı momentum kovasıyla karışmasın); G3 rastgele grup aynı hücre, aynı n (G2 ile); karne FARK = olay - eş (aynı gün aynı kova) |
| K2 | geleceğe bakma | EVET | grup tanımları F14 / F15 / F17 / Ş9 mühürlü özellik dosyalarından (yalnız [.., t]); koşuda her grup x pazar 5 olay veri t'de kesilerek yeniden (yh_gelecek5, DURUR); mahkeme veriyi t'de keser, her aday yalnız t_k'ya kadar (prefix kapısı: t_k'da kesik veri = aynı değer); G3 örneklemi yalnız kimlik + dönem ile, ön kayıtta mühürlü |
| K3 | geçerli bar | EVET | aynı geçerli bar süzgeci (_yh_hazir = SY.sy_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği); mahkeme pencereleri geçerli bar sayımıyla; C13 ATR250 geçerli barlarla |
| K4 | tekilleştirme | EVET | Y1 olayları OC 60 gün tekil; yh_olc_pazar'da hiçbir olay düşmemeli (DURUR); n = bağımsız olay; grup hücrelerinde getiri ortalama + medyan (yh_hucre); mahkeme adayları bölge başına bir kez (S6 bölge kimliği) |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (OC); Y1 regresyonu: ölçülen her satır olay_Y1.csv.gz satırına eşit (plasebo dahil), DURUR |
| K6 | veri birimi | EVET | aynı V_*.pkl tek kip; bütün ölçüler oran / sayı (birimden bağımsız); AVR yerel para; mahkeme çıktısında fiyat seviyesi yok |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; G2 (dipte) gruplarında batan hisse eksikliği daha büyük olabilir -> G2 - G1 farkı yukarı yanlı okunur; rapora yazılır |
| K8 | örneklem ve dönem | EVET | grup x hücre n (ölçülen) tabloda; n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; ABD / AVR 2023 ve 2024-26 BAKILMIŞ (Y1 ve Y9 hücreleri önceki turlarda görüldü; G1 / G2u / G3 Y1 alt kümesi) -> etiket en fazla EMARE; karne n < 30 SORGULA; grup farkı bootstrap %95 (bilgi); küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | ON_KAYIT_6.md: YH_ESIK6_SHA, YH_ESIK_SHA (= ON_KAYIT_5.md: Y1-Y11c aynen), kod / OC / S6 / GE fonksiyon / özellik / Y1-Y9-Y9c olay / güç / G3 / s7_bolge_pdf sha + git; yh_kapi6 hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt ayrı commit (A koşusundan önce), ölçüm ikinci commit; B / C yeni eşik seçmez (B raporlama, C getirisiz); eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV ve mühürlü özellik dosyaları; TUR 4 anahtarı yalnız okunur (sayfa -> kimlik), sha md'ye yazılır |
| K11 | yeniden üretim | EVET | olay_G6.csv.gz satır dosyası (grup bayraklı); RAPOR_6.md 'YENİDEN ÜRETİM' iki hücre (biri konum eşli) bağımsız komutla; tutarlılık kapısı G2 = olay_Y9, G0 ∩ F15 >= 0,75 = olay_Y9c; karne olay_Y1 + özellik dosyalarından yeniden üretilebilir |
| K12 | ifade | EVET | etiket yalnız 3. tur kuralıyla (en fazla EMARE; TERS iki yönlü); grup farkı ve karne 'bilgi'; 'iz değil' yazılmaz; mahkeme kararı kural uyumu (getiri değil); sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_ / YH_ / _YH_ önekli); yasak defter dosyalarına, GOZ_ETIKET.py'ye, tur/1-5 içeriklerine dokunulmadı (git diff; TUR 4 anahtarı yalnız okundu); e-posta / anahtar taraması (_yh_yaz); push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm ve kural denetimi |

