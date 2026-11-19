# CEMAL'İN KURAL DEFTERİ — TASLAK (17 Kasım 2026)

Kaynak: arastirma_cikti/kural_defteri/DEVIR_NOTU_2026-11-17.md (J grubu), IZ_DEFTERI.md (0. İNDEKS, A-E), IZ_KARNE.py (IK_KAYIT Ç1-Ç188, IK_GOREV 159 satır, IK_HATA 221 satır, IK_ILERI 22 satır, IK_KONTROL 14 madde, IK_ACIK 43 madde), COL_OZET.md, ONERI_DEFTERI.md, CLAUDE.md, arastirma_cikti/sikisma_obek/CEMAL_COL_KURALLARI.md, arastirma_cikti/fitil_v2/FITIL_V2_IS_TANIMI.md (+ TASARIM.md), arastirma_cikti/fitil_obek/HALKA_RAPOR.md, arastirma_cikti/iz_karne/karne.csv. Ham sohbet repoda yok; kurallar defterdeki aktarımdan alındı. Taslaktır; defter dosyalarına işlenmedi (yalnız ana model işler).

Sonuç etiketleri: TUTTU (ölçüm kuralın yönünü verdi ya da itiraz doğrulandı) · TUTMADI (güç yeterli ya da önceden yazılı ölçütle ayrışmadı / ters) · TUTMADI* (eski 'İZ DEĞİL'; K58'e göre n < 1.000 hücrelerde aslında ÖLÇÜLEMEDİ sayılır, IK_ILERI 'Ç100-Ç151' satırı) · ÖLÇÜLEMEDİ (n ya da güç yetersiz) · EMARE (tek pazar / tek olay) · SINANMADI (ölçüm yok ya da yalnız tasarım / süreç kuralı). Kodda: YOK = hiçbir modülde şart olarak yok.

## 1. ÖZET

- Kural sayısı: 140 (A çöl / bölge 21, B giriş 15, C çıkış 8, D bağlam 10, E mum okuma 14, F dosya / temel 12, G boyut / risk 9, H süreç ve itirazlar 23, I tezler 9, J devir notu 19). EK (17 Kas akşam): K kör set 2 dersleri 18 + YAPI_HEDEF değerlendirmesi 11 (K19-K29; sonuç görülerek yazıldı, sınanacak) + hakem PDF'i 6 (K30-K35) + TUR 1 2 (K36-K37) + TUR 2 2 (K38-K39) + S7 PDF 1 (K40) + TUR 4 6 (K41-K46) (toplam 186; K15 ufuk 15 mum Cemal'in ölçüt kararı). Bunların 113'ü piyasa / işlem kuralı ya da tezi (A-G, I, J1-J15), 27'si süreç kuralı ya da Cemal'in yönteme itirazı (H, J16-J19).
- Sınanan: 88 / 140 (sınanmayan 52; 16'sı sınanmayacak süreç kuralı).
- Sonuç, bütün tablo: TUTTU 17 · TUTMADI 51 (40 + 11 TUTMADI*) · ÖLÇÜLEMEDİ 17 · EMARE 3 · SINANMADI 52.
- Yalnız piyasa / işlem kuralları ve tezler (113): TUTTU 7 · TUTMADI 50 (39 + 11*) · ÖLÇÜLEMEDİ 17 · EMARE 3 · SINANMADI 36.
- Piyasada TUTAN 7 kuralın hiçbiri getiri izi değil: A9 net değişim sınırı (etiket uyumu), B13 'yükselişte almak zarar ettirmez' (piyasayı geçmiyor), G2 olaysız ekleme yok, G6 boyut öldürür, G7 BIST'te fiyat stopu çalışmaz (eski cetvel), I5 fon krizi kesiği, J14 'şekil tek başına yazı-tura'.
- Devir notu (J, 19 madde): 4 TUTMADI (birleşik imza, uzun çöl, bitişteki küçük mumlar, AL kuralı), 1 ÖLÇÜLEMEDİ (doji 'en kritik özellik': doji kutusu n < 1.000, col_ogren'de ayırmadı), 1 TUTTU (732 kırılım yazı-tura; sayı repoda yok, yön repo ölçümleriyle aynı), 13 SINANMADI. Kodda olmayan 5: dev mum şartı (J4), 'azıcık çıkıp dönmek' (J6), kutu 1 SMA200 (J13), J14 (bulgu), J19 (iletişim). İki madde mevcut kurallarla çelişiyor: 'eğim gürültü' (J10, A9 / S6 netMax ile ters), 'yatırım tavsiyesi değildir yazılmaz' (J19, CLAUDE.md dürüstlük kuralıyla ters).
- EMARE 3: A11 S5 DİP öbek sıkışması (ABD büyük gün 1,14-1,17 kat, yön yok), D2 sektör rüzgârı (ABD +%2,8 / +%3,6, portföy şartı düştü), F12 çöküş sonrası KAP geri alım (tek olay, q 0,003).
- H grubunda Cemal'in yönteme itirazlarından 10'u TUTTU (H4-H8, H15, H19-H21, H23): rastgele kıyas yoktu, eski kodlarda ~30 hata vardı, batanlar dışarıdaydı, kör set grafikleri okunmuyordu, 'iz değil'lerin çoğu ölçülemedi, sıkışma tanımı rastgeleydi, fotoğraftan tarih yanlıştı.
- Kodda olmayan kural: 41 / 140. Bunların 13'ü ölçülüp tutmadığı için üretim şartı olarak önerilmez (A15, B4, B5, B6, B11, C8, D3, D4, D5, D6, D9, E3, E10); kalan 28 için bölüm 4b'de tek satırlık şart ya da ölçüm önerisi var (çoğu boyut / çıkış kuralı: C4-C7, G1-G5, G9; devir notundan J4 dev mum, J6, J7 doji sütunu, J13).
- İleri testi takvimde olan: Mart 2027 (A1, A4, A5, A11, A14, A19, A21, B12, B15, D1, D2, E1, E2, E9, E11, I4), Haziran 2027 (F10, F11), Kasım 2027 (I3), Ocak 2027 (I2 60 gün karne).

En çok tekrar eden 5 ders (IK_HATA 221 satır; tür sayımı: ölçüt 49, veri 40, süreç 35, hesap 31, yanlış yorum 20, iletişim 20, geleceğe bakma 14, karar-boyut 6, ayrıştırma 6):
1. Kontrol grubu yanlış ya da yok, fark mekanik (IK_KONTROL K1: 22 kez): eski 'GEÇERLİ' A1-A4, A9, A13, A14, B1, B14 öbek, D13, T10 bu yüzden düştü.
2. Veri hatası (veri türü 40 satır): kilitli / hacimsiz bar sinyal sayıldı (MUM_SUKUN v1.0'da sinyallerin %24'ü), Mart 2020 marjı, peni / sterlin 100x, bölünme / bedelsiz, bayat CDS.
3. Geleceğe bakma ya da sonradan bilinen bilgi (14 satır; K2): çölün son günü girişi (B13), ileriye bakan kırılım sütunu (A13), atılım mumu dahil sağ ayak, tarayıcıların toplam seri uzunluğu (H178), sayfa tarihi / satır tarihi karışması (BofA).
4. Güç yetersizken 'İZ DEĞİL' ya da küçük örneklemden 'bulgu' (K8; H118, H165): en az 20 eski kayıt ÖLÇÜLEMEDİ'ye döndü, K58'e göre n ≤ 300'de güç ≤ %11.
5. Yalnız yaşayan evren (hayatta kalma, K7: 8 kez): K33-B ABD-ADAY, K51 'en yakın aday', K48-K50 deneyleri batanlar eklenince düştü / geçersiz oldu.
Ayrıca sık: Cemal'in gözündeki bölge ile kod tanımının ayrışması (H186, H193, H194, H197, H207, H208, H221) ve düşen iddiaların hepsinin iyimserden gerçeğe düşmesi (14 Kas sayımı: tersi yok).

## 2. KURAL TABLOSU

### A. Çöl tanımı ve bölge

| No | Kural (Cemal'in sözü, kısa) | Kaynak (tarih, Ç / görev) | Sınandı mı (Ç no, cetvel) | Sonuç | Neden (bir cümle) | Kodda (modül.şart) | Durum |
|---|---|---|---|---|---|---|---|
| A1 | Çöl, düşüş sonrası dipte aylarca süren sıkışmadır; dip savunulur, mumlar küçüktür | CLAUDE.md 'çöl tanımı'; D12 tarifi 20 Eki (COL_OZET 9.5) | Ç41 D12 (eski cetvel 3/6 dönem), Ç47 D13, Ç96 K24, Ç132 K51, Ç178 ORTAK CETVEL v1.0 | ÖLÇÜLEMEDİ | K24 ABD 2024-26 n 2.869 eşli -%1,1 TUTMADI, ABD 2023 n 941 güç %52, AVR güç %29; iki yönde büyük hareket (piyango) | COL_v1.col_dip2 (SEGMENT_MOD='dip2'); FON_IZI.fi_k24_tara | İLERİ TEST Mart 2027 |
| A2 | Tepede oluşan sıkışma dağıtımdır, çöl değildir | CLAUDE.md; kör set notu K13 (17 Kas, sayfa 14, 27, 8) | Doğrudan yok; COL_OZET §8 konum250 (eski cetvel) | SINANMADI | Konum ölçüsü yalnız eski cetvelde (dipte beklenti ve ağır kayıp birlikte yüksek); FITIL_V2 (5) koşusu bekliyor | FITIL_V2.fv_kural s5 (120 gün tepesinin %15 altı); COL_v1.DIP_KONUM 0,35 (yalnız col_dip, üretimde değil) | AÇIK (FITIL_V2 aşama 2) |
| A3 | Küçük mum = gövde değil, fitil dahil boy (H−L) | CLAUDE.md; COL_v1 D7 17 Eki | COL_OZET 9.1 (piyasaya göre, eşsiz); Ç37 | SINANMADI | Yalnız eski cetvelde ölçüldü (2020-22 n 125, 2023-26 n 97); eşli / ortak cetvelde ayrı sınanmadı | COL_v1.MUM_OLCU='aralik' | KAPALI (tanım) |
| A4 | Tam desen üç evre: sıkışma → kırılım + yükselen SMA üstünde raf → bölgeye sert test, sonra hareket | CLAUDE.md 'çöl tanımı' | Yalnız iki evre kısmı Ç96 / Ç178 (K24); test evresi sınanmadı | ÖLÇÜLEMEDİ | İki evre kuralı eşlerden ayrışmadı (A1 ile aynı ölçüm); üçüncü evre (sert test) için ölçüm yok | FON_IZI.fi_k24_tara (2 evre); 3. evre YOK | İLERİ TEST Mart 2027 |
| A5 | 1. evre SMA20 altı, 2. evre SMA20 üstünde muntazam dizilme, delen yok | 25 Eki (MANAS), Ç96 | Ç96 (eski eşli 0,74-1,04), Ç178 | ÖLÇÜLEMEDİ | Tarif eşliden iyi değil (BIST 2023 %46 vs %62); ortak cetvelde ABD 2023 güç %52 | FON_IZI.fi_k24_tara; K24_YENIDEN | İLERİ TEST Mart 2027 |
| A6 | Bölge = tabanın TAMAMI (düşüş bitip dip savunulduğu yerden tavanı kıran al mumuna); 15 barlık parça değil (K1) | 15 Kas, CEMAL_COL_KURALLARI K1 (DESA, KNFRT, TUCLK, ENJSA) | S6 tasarım sınaması (etiket uyumu 13 / 14; getiri yok) | SINANMADI | Yalnız etiket uyumu ölçüldü; S6 bölgesinin sonrası eşli cetvelde ölçülmedi | S6_TABAN.s6_durum / s6_bolgeler | AÇIK |
| A7 | Bölge en az 8 mum (5 alt sınır), çoğu ~60'a kadar; tek mumluk bölge yok; bitişik parçalar tek bölge | 15 Kas (ENJSA, S6 TASLAK) | Tasarım kuralı | SINANMADI | Tasarım kuralı; sonuç ölçülmedi | S6_TABAN.S6_PRM nMin 8, nMax 70 | KAPALI (tasarım) |
| A8 | Sınır mumlardan gelir; bant kısa bölgede %5-8, uzun tabanda %20'ye kadar (K2) | 15 Kas (DESA %20) | Tasarım ızgarası (bantMax 0,12 / 0,20) | SINANMADI | Izgarada 0,12 seçildi; DESA'nın %20 bandı bu eşiğin dışında | S6_TABAN.S6_PRM bantMax 0,12 | AÇIK |
| A9 | Sakin bölge: ilk-son kapanış farkı küçük (aday ≤ %5); eğimli pencere çöl değil (K3) | 15 Kas (ENJSA 2021 etiketleri) | Etiket sayımı (yanlış dediği 2 bölge mutlak net değişim %8-10, doğru %0,3; S5 pencerelerinin %13'ü > %5) | TUTTU | Cemal'in etiketleri net değişim sınırıyla ayrıştı (etiket uyumu; getiri ölçüsü değil) | S6_TABAN.S6_PRM netMax 0,03 | KAPALI (tasarım) |
| A10 | Düşüş sonrası; kayan düşüş kanalı çöl değil; dip korunur (K4) | 15 Kas (TUCLK Ağu 2026, PAPIL) | S6 v1.0 / v1.1 tasarım | SINANMADI | Kod bu yanlışı eleyemiyor (TUCLK Ağu 2026 v1.1'de de seçiliyor); sonuç ölçümü yok | S6_TABAN dipTol 0,05, dipDusus -0,10 | AÇIK |
| A11 | Bollinger daralması bütün bölgelerde şart; öbek gibi yan yana küçük mumlar; zıplama mumu görmezden gelinir | 15 Kas (FENER, CCOLA, ENJSA), Ç184 | Ç184 S5 (ORTAK CETVEL), Ç183 S4 | EMARE | S5 DİP sınıfı ABD iki dönemde 20 günde büyük gün olasılığı 1,14-1,17 kat (n 579 / 649); yön ve getiri yok; Avrupa'da yok | SIKISMA_OBEK.so_s5 (bb 0,20, k_m 0,75); S6_TABAN bbSart 0,30 | İLERİ TEST Mart 2027 |
| A12 | Yükselişteki bölge dinlenme olmalı, taban korunmalı; dip bölgesi de sayılır | 15 Kas, Ç184 | Ç184 S5 YOL sınıfı | TUTMADI | YOL (yükseliş içi) sınıfı hiçbir karar hücresinde tutmadı (EMARE yalnız DİP'te) | SIKISMA_OBEK.so_s5 sınıf YOL | KAPALI |
| A13 | Küçük mum hissenin normalinden küçük; 0,75 x ATR250 bazen fazla sıkı (K5) | 15 Kas (ENJSA May-Haz 2025: medyan 0,82 x ATR) | Tasarım (S6 kM 0,75 / 0,90 / 1,00) | SINANMADI | S6'da 0,90 seçildi; S5 0,75'te kaldı (ön kayıt); sonuç ölçülmedi | S6_TABAN kM 0,90; SIKISMA_OBEK k_m 0,75 | AÇIK |
| A14 | Çöl aylarca sürebilir; giriş mumu aylar sonra gelebilir; ikinci çöl riskli (K7) | 15 Kas (YKSLN); D9 uzun çöl 18 Eki | Ç181a D9 (ORTAK CETVEL) | TUTMADI | 6-12 ay dar bant eşlerden iyi değil, dört karar hücresi TUTMADI (n 1.102-4.556); +%100 katı 0,40: sakin hisse seçiyor | COL_v1.uzun_col_olc (ölçüm referansı; T8 ekrandan kaldırıldı, D14 / T12) | İLERİ TEST Mart 2027 |
| A15 | Çöl nadirdir; nadir çölün sağ ayağı rastgele hisseden iyi olmalı | 25 Eki | Ç92 (nadir = dar kutu + düşüş ≤ -%50), S6 v1.1 sıklık | TUTMADI | BIST'te nadir çölün 250 gün 2 kat oranı %20,7 vs eş %20,5; S6 hisse-yıl başına 4,2 bölge (Cemal'in 'nadir'inden sık) | YOK | KAPALI |
| A16 | Kutu yeni dipten başlar; önceki raf / düşüş kutuya girmez | 21 Eki (OYLUM / EUYO), D13 kural 1 | Ç47 D13 (tek cetvel + mesafe eşli) | TUTMADI | Alım farkı ham +12..26 puan mekanikti, mesafe eşli +0,5..+3,8; tek cetvel 0,97 / 0,98 | COL_v1.col_dip2 (d = son 120 bar dibi) | AÇIK (üretimde, dayanağı düştü; Cemal kararı) |
| A17 | Dip savunması + parabolik yukarı yuvarlanma + küçük mum öbekleri birlikte; tespit işlemden ayrı | 21 Eki (D13 kural 2-3) | Ç44 B14 öbek, Ç47 | TUTMADI | Öbek 'alım +15-20p' mekanik; eşli tabanda +3 / +2 / -3 / +4 puan | COL_v1.col_dip2 (_d13_obekler, parabol a > 0) | AÇIK (üretimde) |
| A18 | Aşağı kırılıp toparlanıp giden çöller kaçmamalı (tespit daraltılmaz, bu çıkış işi) | 21 Eki (COL_OZET 9.8) | Yok | SINANMADI | Ayrı ölçüm yapılmadı | YOK | AÇIK |
| A19 | Dibi düzgün (haftalarca test edilen) taban; TEHOL 2024 düzgün, 2021 değil | 24 Eki, Ç73-Ç77 | Ç73-Ç77 tek cetvel; Ç179 ORTAK CETVEL | ÖLÇÜLEMEDİ | Ölçü gözü yakalıyor (2021 elendi) ama eşlerden ayrışmıyor; dip ile çöl ayrımı ABD C n250 381 / 723 < 1.000 | FON_IZI FI_K13B_ESIK / fi_k16; DIP_COL_AYRIM.py | İLERİ TEST Mart 2027 |
| A20 | İki yuvarlama: önce aşağı yay (∩), hemen ardından kâse (∪) | 24 Eki (TEHOL 2021), Ç78-Ç83 | Ç78-Ç83 tek cetvel + eşli kutu | ÖLÇÜLEMEDİ | Eşli kutuya göre 0,86-1,08; n < 1.000 ve güç kanıtı yok (H165 listesi) | FON_IZI k17 | AÇIK (yeniden koşu sırası, IK_ACIK) |
| A21 | Sıkışma = yatay + dar Bollinger; küçük mumlu ama kayan pencere sıkışma değil (FENER 14 Eki - 7 Kas doğru, 3-16 Ara yanlış) | 15 Kas, Ç183 | Ç183 S4 (ORTAK CETVEL) | ÖLÇÜLEMEDİ | S4 hücreleri n 467-843 < 1.000; FENER bölgesi (iv) uzunluk koşulundan kaçtı (tasarım hatası H194) | SIKISMA_CEMAL (SC_ESIK) | İLERİ TEST Mart 2027 |

### B. Giriş (al mumu, kırılım, onay)

| No | Kural (Cemal'in sözü, kısa) | Kaynak (tarih, Ç / görev) | Sınandı mı (Ç no, cetvel) | Sonuç | Neden (bir cümle) | Kodda (modül.şart) | Durum |
|---|---|---|---|---|---|---|---|
| B1 | Giriş = tavanı kapanışla kıran al mumu; tavan kırılmadan alım yok (K6) | COL_OZET §1 (Eylül); 15 Kas K6 (KNFRT, TUCLK, PAPIL) | Ç91 K19 (aynı gün eşli / rastgele), COL_OZET §3 giriş testleri | TUTMADI | Kırılım girişi 12 hücrenin hiçbirinde aynı gün eşli hisseden üstün değil (fark -1,8..+1,7 puan) | COL_v1.AL_PAY 1,002 (bugun_liste); S6_TABAN AL / KIRILDI (kirTol 0,02) | KAPALI (giriş zamanlaması kapalı konu) |
| B2 | Büyük çölün tavanı sivri tepe mumudur; o yatayı kapanışla kıran mum al mumudur; küçük tabanın kendi tepesi ayrı (K6b) | 15 Kas (PAPIL düzeltmesi) | Yok (tek örnek veride okundu) | SINANMADI | PAPIL'de bu kuralla alım 2 Mar 2026 tepesine denk geliyor; küçük taban kırılımı +%8 sonra söndü (tek örnek) | S6_TABAN AL (tavan mumu ayrı şart değil) | AÇIK (S6 al mumu, başarısız kırılımla sınanacak) |
| B3 | İki kutu: ilk giriş 2. kutu oluştuktan sonraki hafif silkelemede; bölge testi yukarı dönerse ekleme | CLAUDE.md; 21 Eki (ARZUM) | Ç83 (K17 Y6 hafif silkeleme -%5..-%15) | ÖLÇÜLEMEDİ | Tek cetvelde iz değil ama n < 1.000 (H165 listesi); ekleme kuralı hiç sınanmadı | FON_IZI k17 Y6 (ölçüm); üretimde YOK | AÇIK |
| B4 | Kutu içindeki tepe aşılmıyorsa risk çok; alış mumu yoksa çöl mumları yeterli değil | 26 Eki (kör set v4) | Ç95 kör set v4 (48 aday) | TUTMADI | ✓ önce +%15 %54, ✗ %57, havuz %60 (n 48, ön deneme) | YOK | KAPALI |
| B5 | Öbekte hacim kurusun, alım mumu 2-3-4 kat hacimle gelsin | 21 Eki (COL_KAZANC) | COL_KAZANC 25 ölçü x 6 dönem | TUTMADI | TERS: alım mumu hacmi ≥ 4x BIST 4 / 4 dönem kötü (-0,4..-7,3 puan); öbek hacmi kuruması 3 dönemde kötü | YOK | KAPALI |
| B6 | Küçük alım mumu ve NVI / CMF kurumsal birikim ayrışması | 21 Eki (K7, K8 planı) | COL_KAZANC v1.1 / v1.2 | TUTMADI | Küçük alım mumu BIST'te 4 / 4 ama ABD'de yok (düşük hacim vekili); birikim akışı ABD'de kâr eklemiyor | YOK | KAPALI |
| B7 | Dönüm mumu vs yön mumu: düşüşün son mumları 'son nokta' diyorsa dönüm (akümülasyon); yalnız yön gösteren mum sinyal değil (K12) | 17 Kas kör set (sayfa 22, 3, 9 / 4, 2, 1) | FITIL_V2 tasarım (getirisiz; E-GİRİŞ 5 / 7) | SINANMADI | Getiri ve eşli ölçüm aşama 2'de; tasarım yalnız etiket uyumu | FITIL_V2.fv_kural s3 (60 bar tepesinden düşüş ≥ 0,20) | AÇIK (FITIL_V2 aşama 2) |
| B8 | Savunma hattı: şekil aynı olsa bile savunulan seviye kırılmışsa aşağı, kırılmamışsa yukarı (K10) | 17 Kas kör set (sayfa 41, 37, 38, 28) | Ç162 / Ç175 VDYT savunma hattı; FITIL_V2 tasarım | TUTMADI | VDYT'de korunan hat yukarı kırılmayı +10..+22 puan artırdı ama yön bölge içi konumdan mekanik (Ç175: İZ DEĞİL); FITIL_V2 (2) koşusu bekliyor | FITIL_V2.fv_kural s2 (HAT = min Low, hatTol 0,02) | AÇIK (FITIL_V2 aşama 2) |
| B9 | Yol almış = kovalama yok (K11) | 17 Kas kör set (sayfa 24, 25, 21, 20) | Doğrudan yok; dolaylı Ç168, Ç147 | SINANMADI | Dolaylı veri aynı yönde: çökmüş hissede tavana katılmak eşlerden kötü (duyarlılık -%12..-%29), kriptoda +%100 sonrası 30 gün medyan -%49 | FITIL_V2.fv_kural s4 (C ≤ HAT x 1,10) | AÇIK (FITIL_V2 aşama 2) |
| B10 | Akümülasyonda alıcının kurumsal olup olmadığı önemli; kim alıyor (K15) | 17 Kas (sayfa 9); 26 Eki AKD sorusu | Yok (AKD ücretsiz yok); Ç97 raporlu fon payı | SINANMADI | Aracı kurum dağılımı verisi yok; raporlu fon payı çölle ilişkili değil (A dolaylı) | YOK | AÇIK (veri yok) |
| B11 | Sağ ayak: çölden çıkan hisse rastgele hisseden çok daha fazla yol almalı (MANAS 18 Tem - 8 Ağu 2025) | 25 Eki, Ç92-Ç94 | Ç92, Ç93, Ç94 (aynı gün sıra) | TUTMADI | Atılımdan sonra sıra 0,45-0,53; fark yalnız atılım mumunda (kapanışta bilinir), bekleyen emirle sahte kırılımlar farkı siliyor | YOK | KAPALI |
| B12 | 60 gün değil, bölgenin altı / üstü çıkışı; +%8 iz (INTEM) | 28 Eki, Ç124 | Ç124 (oynaklık eşli rastgele), Ç180 ileri test | ÖLÇÜLEMEDİ | İlk koşu ABD +11,2 puan; görülmemiş hisselerde ORTAK CETVEL L20 n 26 / 42, kendi ölçüsü +2,7 puan [-6,8; +12,2] | FON_IZI k45; INTEM_ILERI.py | İLERİ TEST Mart 2027+ |
| B13 | Yükselişte alınca zarar az, dipte dönüş varsayımıyla alınca kötüleşti | 28 Eki, Ç122 | Ç122 alınabilir iz karnesi (23 sinyal, 3 pazar) | TUTTU | Trend grubu zarar ettirmiyor (-%2..+%1), dip grubu ABD 2023 dışında sıfır / eksi; ama ikisi de piyasayı geçmiyor | YOK | KAPALI |
| B14 | Dipler aynı çizgide, dip kırılmazsa sert çıkar (S+DÜZ) | 16 Kas, Ç188 | Ç188 HALKA 1 ek (SPD, SPDb) | ÖLÇÜLEMEDİ | Dip bağlamında n 11-77; bağlamsız SPDb yalnız ABD 2024-26 tutuyor (n 80, +%6,7) ama kırılımda ters (-15,6 puan) | FITIL_KOR (SPD, SPDb satırları) | AÇIK (ileri test adayı) |
| B15 | Dipte %80-90 düşmüş, dip tutuyor, ucuz noktada BofA alımıyla gir | 13 Kas, Ç173 | Ç173 (FI_OLCUT + 250 gün olasılık) | ÖLÇÜLEMEDİ | Kriz öncesi olay 0 (BofA dipte hiç almamış); kurulum tek başına piyango (P+%100 ve P-%50 ikisi ~2 kat) | BOFA_IZI dipkos | İLERİ TEST Mart 2027 |

### C. Çıkış ve stop

| No | Kural (Cemal'in sözü, kısa) | Kaynak (tarih, Ç / görev) | Sınandı mı (Ç no, cetvel) | Sonuç | Neden (bir cümle) | Kodda (modül.şart) | Durum |
|---|---|---|---|---|---|---|---|
| C1 | Taban kırılınca çık (T6; YKSLN Temmuz stop, K8) | takip T6 17 Eki ('Cemal'in kuralı'); 15 Kas K8 | COL_OZET §3 (taban kırılınca çık kötü); Ç91 K19 kutu dibi stop | TUTMADI | Getiride 120 gün tutmaktan düşük; yalnız yatay piyasada derin kaybı azaltıyor (BIST 2024-26 -%30 altı %11 → %4) | takip.TABAN_TOL 0,02 (T6) | AÇIK (H23: üretim testle çelişiyor, karar bekliyor) |
| C2 | +%8 görülünce stop maliyete (T10) | 21 Eki (Cemal 'yaz') | Ç45 COL_YOL denetim sonrası | TUTMADI | Getiri dayanağı ters döndü (BIST +144 vs +155, ABD 0 vs +6); tutarlı tek etki ağır kayıp %9,1 → %5,4 | takip.MALIYET_ESIK 8,0 (T10) | AÇIK (Cemal kararı) |
| C3 | %20 hedefe değince SMA20 trail, en çok 120 bar; stop yok | COL_OZET §1 (18 Eyl; söyleyen yazılı değil) | COL_OZET §3 (eski cetvel), Ç91 | TUTMADI | Aynı girişlerde 120 gün tutmaktan ortalamada hep düşük (Ç91) | COL_v1.HEDEF 20; takip trail SMA20, ufuk 120 | KAPALI (çıkış kapalı konu) |
| C4 | Son büyük mumda büyük kısmı sat ('içindeysem %70 satılır', K11) | 17 Kas kör set (sayfa 20, 24) | Yok | SINANMADI | Ölçüm yok | YOK | AÇIK |
| C5 | Tepe mumları aşağı gösteriyorsa çık / alma (K13) | 17 Kas kör set (sayfa 1, 14, 27, 8) | Yok (çıkış olarak) | SINANMADI | Ölçüm yok; FITIL_V2 (5) yalnız giriş tarafında | YOK (çıkış); FITIL_V2 s5 (giriş) | AÇIK |
| C6 | DGXX bilanço günü +%25 ve üstü 1/3 sat; kötü bilanço (nakit < kalan yatırım, teslim kayması) beklemeden sat | 6-7 Kas (ONERI_DEFTERI) | Yok | SINANMADI | Pozisyon kuralı; olay sonucu defterde yok | YOK (ONERI_DEFTERI metni) | AÇIK |
| C7 | QMLS: bilanço iyi ve sıçrama o gün sat; NT 10-Q / ağırlaşan going-concern ertesi sabah sat; en geç 8 Oca 2027; ekleme yok | 6 Kas (ONERI_DEFTERI) | 12 Kas kontrolü | SINANMADI | 10-Q'da sıçrama yok (-%7,3), NT 10-Q yok: kural tetiklenmedi | YOK (ONERI_DEFTERI metni) | AÇIK (8 Oca 2027) |
| C8 | Sektör yeşil gününde sat: sektör %1 yükselirse QMLS %10 zıplar | 6 Kas | Beta ölçümü (görev 6 Kas, H106) | TUTMADI | QMLS beta 0,59, sektörle 1:1 civarı | YOK | KAPALI |

### D. Bağlam (dip / orta / tepe, düşüş sonrası, sektör rüzgârı, pazar)

| No | Kural (Cemal'in sözü, kısa) | Kaynak (tarih, Ç / görev) | Sınandı mı (Ç no, cetvel) | Sonuç | Neden (bir cümle) | Kodda (modül.şart) | Durum |
|---|---|---|---|---|---|---|---|
| D1 | Sektör rüzgârı veya katalizör olmadan çöl aranmaz | CLAUDE.md; D9 18 Eki | Ç181b (D9 + rüzgâr), Ç117 (çöl + rüzgâr), Ç90, Ç82 | ÖLÇÜLEMEDİ | D9 + rüzgâr ABD 2023 güç %52, 2024-26 n 1.556 TUTMADI; çöl + rüzgâr ABD -%1,3 / -%0,4 | COL_v1 RUZ_ESIK 0,10, RUZ_MUTLAK 0 (sektor_ruzgar); takip ruz% sütunu | İLERİ TEST Mart 2027 |
| D2 | Sektör rüzgârının kendisi (sepet - piyasa ≥ eşik, sepet > 0) | 18 Eki (D9b); 15 Kas 'sektör derle' | Ç181c (ORTAK CETVEL), Ç185 Avrupa | EMARE | ABD eşli +%2,8 / +%3,6, +%100 katı 1,35-1,39; portföy şartı düştü; Avrupa güç %29 / %52 ÖLÇÜLEMEDİ; bilinen etki (sektör momentumu) | COL_v1.sektor_ruzgar / ruzgar_listesi | İLERİ TEST Mart 2027 |
| D3 | Rüzgâr fiyattan görülünce geç kalınır; önce sebebe bak | 28 Eki, Ç110 | Ç110 (FI_OLCUT) | TUTMADI* | Sebep rüzgârdan önce gelmiyor (öncülük 1,0-1,2); sebep sinyalinde üyeler eşlerden iyi değil | YOK | KAPALI |
| D4 | Patlayanların arkasında ve patlama zamanında rüzgâr var mı; rüzgâr batmayı azaltır mı | 28 Eki, Ç108-Ç109 | Ç108, Ç109 | TUTMADI* | Rüzgâr patlamaya eşlik ediyor ama girişte görünmüyor (0,54-1,20); batmayı ayırmıyor (2021-22 farkı SPAC'ler) | YOK | KAPALI |
| D5 | Büyükler önce, küçükler sonra; para akışı yetmez, temel ve haber zamanlaması | 28 Eki, Ç111 | Ç111 | TUTMADI* | Küçükleri almak eşleri geçmiyor (BIST 2023 +%6 aralık 0'ı içeriyor, ABD 2023 -%6); maliyetle eksi | YOK | KAPALI |
| D6 | Amerika öncü; Avrupa ve Asya takip eder; gecikme saat farkıyla alınabilir | 28 Eki, Ç114-Ç115, Ç119 | Ç114, Ç115, Ç119 | TUTMADI* | Avrupa aynı gün / ertesi açılışta fiyatlıyor; gecikme dakika (açılış boşluğu); sektör 5 gün kalıntısı dört hücrenin ikisinde | YOK | KAPALI |
| D7 | BIST öngörülemez (siyaset, tedbir, fon); Amerika ve Avrupa'da tutan iz kabul edilir, BIST bilgi | 27-28 Eki | Karar kuralı; Ç112 | SINANMADI | Standart kararı; Ç112'de BIST kaçınma izleri ABD'de ters çıktı (BIST'e özgü) | FON_IZI FI_OLCUT 'karar'; ORTAK_CETVEL karar hücreleri | KAPALI (standart) |
| D8 | Bilanço iyi gelecek; önce korkutup aldırmıyorlar, iyi gelirse göstermelik yukarı, sonra yavaş dağıtım | 6 Kas | Ayrı ölçüm yok; dolaylı Ç100 | SINANMADI | Görev satırı 'ABD son dönem ölçümüyle tutarlı' diyor (Ç100 ABD 2024-26 iyi sürpriz -%1,4); kendi tanımıyla ölçülmedi | YOK | AÇIK |
| D9 | SMA üstüne atılım (AMZN) iz mi; endeks SMA200 filtresi | 10 Kas, Ç151 C4 | Ç151 portföy cetveli | TUTMADI | Hisse düzeyinde ABD eksi; endekste düşüşü yarıya indiriyor ama getiri %68'de kalıyor (risk aracı, iz değil) | YOK | KAPALI |
| D10 | Kilit öncesi yükseltip perakendeye satıyorlar: düşük float, yeni listeleme, sığ tahta = çıkış likiditesi | 9 Kas (kripto) | Yok | SINANMADI | Pratik kural; ölçülmedi (kripto kapandı) | YOK | KAPALI (kripto kapandı) |

### E. Mum okuma (fitil, küçük mum, öbek, parmak izi)

| No | Kural (Cemal'in sözü, kısa) | Kaynak (tarih, Ç / görev) | Sınandı mı (Ç no, cetvel) | Sonuç | Neden (bir cümle) | Kodda (modül.şart) | Durum |
|---|---|---|---|---|---|---|---|
| E1 | Fitil öbeği S+: alt fitil yok / küçük, üst fitil biraz uzun = has yukarı çıkma mumları, öbek olunca | 16 Kas (PAPIL; TEHOL, BINBN örnekleri), Ç187-Ç188 | Ç187 (ORTAK CETVEL), Ç188 üç halka, kör set 50 sayfa | ÖLÇÜLEMEDİ | 2024-26 n 1.557-2.367 eşli ±%0,3 TUTMADI, 2023 güç %52; kör sette kod S+ ile S- sayfalarını Cemal'in gözünde ayıramıyor (fark 0, KISMİ) | FITIL_OBEK (FO_ESIK k 10, ASİM 0,20, ALTYOK 0,50); COL_FITIL_OBEK.pine; FITIL_V2 s1 | İLERİ TEST Mart 2027 |
| E2 | Tersi (üst fitil yok, aşağı sert dişler) aşağı götürür (DGXX 2,50 → 2'nin altı) | 16 Kas, Ç187 | Ç187 S- satırı | TUTMADI | S- ABD n 2.367 -%0,3, AVR n 1.557 -%0,2; DGXX'te S- yanmadı (üst fitilsiz bar payı %30) | FITIL_OBEK S- | İLERİ TEST Mart 2027 |
| E3 | 'PAPIL'e has değil' (fitil öbeği genel çöl izi) | 16 Kas | Mum parmak izi tablosu (12 bölge) | TUTMADI | Alt fitilsiz pay Cemal'in öteki DOĞRU bölgelerinde %0-30 (PAPIL %47); en benzer bölge YANLIŞ etiketli TUCLK Ağu 2026 | YOK | KAPALI |
| E4 | Doji / fitil / dar hafta / alt fitil < 0,12 kaliteli çöldür (boyut çarpanı) | COL_OZET §1, §3 (Eylül; söyleyen yazılı değil) | Eylül eski cetvel; col_ogren 9 Eki | SINANMADI | Eşli / ortak cetvelde sınanmadı; col_ogren'de doji ayırmadı; dar hafta tanımı doğrulanmadı (H7, H30) | COL_v1.carpanlar_hesapla (CARPAN doji / fitil / dar) | AÇIK (COL_OZET 9.8 'yeniden doğrulama') |
| E5 | D12 imzası: mumlar küçülür, Bollinger daralır, doji ve hacim kuruması | 20 Eki (COL_OZET 9.5) | Ç41 D12 (eski cetvel), COL_SEKIL | TUTMADI | 6 dönemin 3'ünde tabandan iyi; hacim kuruma imzası ters (çölde hacim_kat60 0,91 vs 0,72) | COL_v1.col_dip (D12; üretimde değil) | KAPALI |
| E6 | Düşüş sonrası son 3-4 mumun dizilimi ve küçülmesi (hissenin kendi oynaklığına oranla) | 22 Eki (ANGX), Ç49 | Ç49 MUM_SUKUN v1.1 | TUTMADI | Tek cetvel 0,96-1,04, dört dilimde fark yok | MUM_SUKUN.py | KAPALI |
| E7 | Akışkan madde düz zemine çarpar; 4-5 mum zemine yapışık sıra | 22 Eki, Ç50 | Ç50 MUM_SUKUN v1.2 | ÖLÇÜLEMEDİ | Tek cetvelde iz değil ama n < 1.000 ve güç kanıtı yok (H165 listesi) | MUM_SUKUN.py (zemin) | AÇIK |
| E8 | 60 gün uzun; kısa sıkışma %3-5 verir; uzun sıkışma + para girişi sert ayrılma | 22 Eki, Ç51 | Ç51 MUM_SUKUN v1.3 | TUTMADI | 10 bar içinde önce +%3 katı 1,01-1,26; hiçbir varyant dört dilimde 1,3 değil | MUM_SUKUN.py | KAPALI |
| E9 | Sıkışmadan sonra büyük mumlar kesin gelir; başlama zamanı tahmin edilebilir | 14 Kas, Ç174 | Ç174 (güç yeterli, n 1.266-9.540) | TUTMADI | Mutlak ölçüde KAT 0,75-0,98 (eğilim ters); 'büyük mum' algısı göreli ölçüden (tanımsal 1,6-1,9) | SIKISMA_YENIDEN.py | İLERİ TEST Mart 2027 |
| E10 | Gözüm küçük mumlardan sonra gelen mumları büyük görür, ayrılık var | 14 Kas, Ç176 | Ç176 duyarlılık | TUTMADI | Göz göreli olarak doğru (sıkışma mumunun 2,7 katı) ama aynı derecede sakinleşmiş eşlerde de aynı (KAT ~1,00); öngörü yok | YOK | KAPALI |
| E11 | Su yolu: çölde engelde birikip birikmiş potansiyelle hızlı akış (büyük mumdan geriye git) | 15 Kas, Ç182 | Ç182 keşif + doğrulama | TUTMADI | Bulgu tersi: büyük mumdan önceki bölge küçük mumlu değil, zaten büyümüş mumlu ve tepeye yakın (P1 KAT 1,3-1,7, EMARE, yalnız oynaklık) | TERS_PARMAK.py | İLERİ TEST Mart 2027 (P1) |
| E12 | İşaretli bölgenin parmak izi (eğim, küçük mum, kırmızı-yeşil, fitil, yakınlık, hacim, RSI, MACD); birebir benzerler yukarı gider (MANAS, BINBN, KZBGY, INTEM, ECOGR, BBIO) | 25-28 Eki, Ç95, Ç98, Ç123, Ç126 | Ç95, Ç98, Ç123, Ç126 | TUTMADI | En yakın benzerler havuzun 0,72-1,50 katı, dönemler arası tutarsız; KZBGY profili 1,01-1,02 | FON_IZI k23 / k26 / k44 / k47 | KAPALI (şekil / parmak izi 'yanlış yol', 11 Kas) |
| E13 | Koşan vakaların ortak profili: sert düşüş → mumu ve hacmi küçük dar kutu → kapanışla tavan kırılımı | 25 Eki, Ç85-Ç90 | Ç85 (eşli kutu), Ç86-Ç90 | TUTMADI | Profil koşmayan VSNMD ve PAPIL'de de var; eşli 0,87-1,06 (Ç87, Ç89, Ç90 sonradan ÖLÇÜLEMEDİ listesinde) | FON_IZI k18 | KAPALI |
| E14 | Eski formasyonlar (Bollinger, RSI, MACD, Fibonacci, ikili dip, ters OBO, uyumsuzluk) başarılı mı | 23 Eki, 28 Eki; Ç59, Ç113, Ç116 | Ç59, Ç113, Ç116 | TUTMADI* | Üç pazarda eşlerden ayrışmıyor; tek kalıntı ABD Fibonacci ortalaması (tipik olay değil) | FON_IZI gosterge / k38b / k41 | KAPALI |

### F. Dosya / temel (sıkı dosya, KAP, fon lekesi, BofA)

| No | Kural (Cemal'in sözü, kısa) | Kaynak (tarih, Ç / görev) | Sınandı mı (Ç no, cetvel) | Sonuç | Neden (bir cümle) | Kodda (modül.şart) | Durum |
|---|---|---|---|---|---|---|---|
| F1 | Sıkı dosya (YEOTK profili): gerçek iş + isimli sözleşme, son çeyrek satış / kâr ivmesi, nakit seyrelme yok, fon lekesi yok, tepeden düşmüş, bilanço günü güçlü tepki | 9 Kas son talimat, Ç148-Ç150 | Ç148 K57, Ç149 K57-B, Ç150 K57-C (FI_OLCUT) | TUTMADI* | 48 ABD karar hücresinin hiçbiri tutmadı; tam profil n 2-5, en yakın V1 n 31 geniş evrende +%10,3 → +%4,8 | K57.py; oneri tarama_kosu (DOSYA kapısı) | KAPALI (hat kapandı) |
| F2 | Fiyat tepeden düşmüş olsun (dipten al) | 9 Kas (F6), 11 Kas | Ç148 F6, Ç152-Ç153 K59 | TUTMADI | F6 eklenince profil bozuluyor; düşmüş yarı zirveye yakın yarının gerisinde; BIST zirveye yakınlık +%16,6 (bilgi) | K57 F6 | KAPALI |
| F3 | Bilanço günü güçlü tepki / bilanço sürprizi | 27 Eki (yol 2), 12 Kas; Ç100, Ç158, Ç160 | Ç100 (FI_OLCUT), Ç158 BIST PEAD, Ç160 | TUTMADI* | İyi sürpriz ABD 2024-26 -%1,4; BIST PEAD makalesi yeniden üretildi ama proje cetvelinde alınabilir uzun bacak tutmadı | FON_IZI k28; K62.py | KAPALI |
| F4 | Görünen alıcı = içeriden alan (KAP pay alım, SEC Form 4); çölde içeriden alım | 26-27 Eki, Ç99, Ç102 | Ç99 BIST, Ç102 ABD | TUTMADI* | BIST net alım eşlerin %2,6-4,5 gerisinde; ABD alım +%0,1 / +%0,2; çölde alım ABD 2023 +%7,3 tuttu, 2016-22 ters | FON_IZI k27 / k30 | KAPALI |
| F5 | En başarılı analistlerin dört verisi: seyrelme, içeriden satış, nakit tükenmesi, kurumsal sahiplik | 27 Eki, Ç103 | Ç103 | TUTMADI* | ABD 2023-26 eşlerden ayrışmıyor; seyrelen / nakdi biten şirketler ortalamada birkaç sıçrayanla iyi | FON_IZI k31 | KAPALI |
| F6 | Nakit tükenmesinde iyi çıkanların izi; batanlar dahil sına | 27 Eki, Ç106-Ç107 | Ç106, Ç107 (Tiingo batanlar dahil) | TUTMADI | Küçük nakdi biten şirket yalnız yaşayanlarla +%9-11, batanlarla +%6-8; 2024-26 sıra 0,48 | FON_IZI k33b / k34 | KAPALI |
| F7 | Fonların para girişi iz bırakır (balina girişinde küçük mum ve ufak ufak yukarı yuvarlanma); fon girişi | 22-24 Eki, Ç55-Ç57, Ç64-Ç66 | Ç55, Ç56, Ç57, Ç65, Ç66 (tek cetvel) | TUTMADI | Fon girişi 0,80-1,07; fonlar fiyatı zaten yükselmiş hisseye giriyor; Ç57 sonradan ÖLÇÜLEMEDİ listesinde | FON_IZI k9-k11, fon_iz_b, z0 | KAPALI |
| F8 | Fon yoğunlaşması yapı riskidir (TERA / Pusula); tasfiye fonu payı yüksek hisse elenir | Eylül (COL_OZET §3, H6); D8 17 Eki | Sinyal olarak sınanmadı; Ç66 (%5 aşımı) | SINANMADI | Süzgeç olarak getiri ölçülmedi; bayrak yokken TERA -%88,6, DSTKF -%90,1 kapandı (canlı kayıp) | COL_v1.FON_ESIK 5,0 + FON_TASFIYE (D8); takip T7; oneri tarama fon lekesi | KAPALI (üretimde) |
| F9 | DOSYA kapısı: birincil kaynak (KAP / SEC) gerçek gelir, sözleşme, nakit, borç, seyrelme, going-concern, tedbir / fon lekesi | 11 Kas (CLAUDE.md öneri modülü) | Karne 11 Kas (3-5 gün, 76 ad) | ÖLÇÜLEMEDİ | Sıralama elenenleri geçmedi (ABD -1,0, BIST -3,6 puan; z -0,1 / -0,5); 16-25 ay gerekir | oneri tarama_kosu (DOSYA bayrakları); YOK (kapı ölçümü) | AÇIK (aylık karne) |
| F10 | BofA almış = emare; en erken bul, alımından satımına kadar takip et; diğer yabancı kodlar da | 13 Kas, Ç171 | Ç171 (tutma dönemi eşli, n 1.751) | TUTMADI | Eşli fark +%0,6 [-0,6; +2,0], portföy rastgele %90'ı geçmedi; güç yeterli | BOFA_IZI kos | İLERİ TEST Haziran 2027 |
| F11 | BofA bir hissede %40-80 zarar etmez | 13 Kas, Ç172 | Ç172 (BofA maliyetinden) | TUTMADI | Kriz öncesi piyasa gibi (+%3,2 / 20 gün), kriz sonrası 20 gün medyan -%9,9, kârlı %22; ama -%40..-%65 rakamları gerçekleşen zarar değildi (H156) | BOFA_IZI karkos | İLERİ TEST Haziran 2027 |
| F12 | Emare vardır; geniş açıdan bak (çöküş sonrası dönüşü önceden gösteren) | 13 Kas, Ç170 | Ç170 GENİŞ KESİT (Spearman, BH) | EMARE | Yalnız KAP geri alım bildirimi: tek olay, 64 hisse, q 0,003 (x1,52 vs x1,26) | GENIS_KESIT.py | İLERİ TEST (2018 / 2020 BIST, ABD; ön kayıtla) |

### G. Boyut ve risk

| No | Kural (Cemal'in sözü, kısa) | Kaynak (tarih, Ç / görev) | Sınandı mı (Ç no, cetvel) | Sonuç | Neden (bir cümle) | Kodda (modül.şart) | Durum |
|---|---|---|---|---|---|---|---|
| G1 | Tek isim, kaybetmeyi kabul ettiği tutarı aşmaz; HEDEF: tamamı kaybedilebilir | CLAUDE.md 11 Kas; ONERI 16 Kas | Yok | SINANMADI | Yazılı kural; ölçüm konusu değil | YOK (ONERI_DEFTERI metni) | AÇIK |
| G2 | Zarardaki isme olaysız ekleme yok | CLAUDE.md 11 Kas; QMLS dersi (H125) | Gerçek pozisyon kaydı | TUTTU | QMLS'te üç ayda 7 alım ≈ -650 $, hesap zararının ≈ %90'ı | YOK | KAPALI (kural) |
| G3 | Maliyetin 2 katında anaparayı çek (2x kuralı) | 6-7 Kas (DGXX) | Yok | SINANMADI | Tetiklenmedi (DGXX 10 Kas 2,16 $, 2x = 4,02 $) | YOK | AÇIK |
| G4 | Aynı sektörde ikinci isim yoğunlaşma uyarısıyla | CLAUDE.md 11 Kas; 6 Kas (QMLS → DGXX) | Yok | SINANMADI | Uyarı verildi; DGXX hesabın ≈ %55'i oldu (H107) | YOK | AÇIK |
| G5 | Tavanda kovalama yok | 16 Kas (HEDEF boyut kuralı) | Doğrudan yok; dolaylı Ç168 | SINANMADI | Çökmüş hissede tavana katılmak eşlerden kötü (B9 ile aynı dolaylı veri) | YOK | AÇIK |
| G6 | Risk değil boyut öldürür; koruma = pozisyon boyutu, stop değil (PAPIL, QMLS, TERA) | COL_OZET ders 3, 7 (Eylül); 6 Kas | Gerçek kayıp kaydı (H3) | TUTTU | Gerçek kayıplar sinyalden değil boyut ve yapı riskinden geldi | COL_v1 boyut %6 x çarpanlar, üst %12 (üretim); öneri boyut YOK | KAPALI |
| G7 | BIST'te fiyat stopu çalışmaz (taban serisi) | COL_OZET §3, ders 3 (Eylül) | Eylül STOP_TEST (eski cetvel) | TUTTU | Fiyat stopu %5-30 ve felaket sınırı hepsi kötü (eski cetvel; eşli değil) | YOK (C1 T6 ile çelişir) | KAPALI |
| G8 | Boyut çarpanları: CDS, borç / öz, doji, alt fitil, dar hafta, üç şart | COL_OZET §1 (18 Eyl) | Eylül eski cetvel | SINANMADI | Eşli / ortak cetvelde sınanmadı; CDS verisi bayattı (H41), negatif özkaynak hatası (H8) | COL_v1.carpanlar_hesapla, cds_rejim | AÇIK |
| G9 | İlk hissede 2x yaparsam sonraki hisselerde riski azaltırım | 6 Kas | Yok | SINANMADI | Karar Cemal'in; ölçüm yok | YOK | AÇIK |

### H. Süreç kuralları ve Cemal'in itirazları

| No | Kural (Cemal'in sözü, kısa) | Kaynak (tarih, Ç / görev) | Sınandı mı (Ç no, cetvel) | Sonuç | Neden (bir cümle) | Kodda (modül.şart) | Durum |
|---|---|---|---|---|---|---|---|
| H1 | Ön kayıt: tanım + eşik + kod sha ölçümden önce git'te (K9) | 29 Eki plan; 14 Kas kontrol listesi | Süreç kuralı | SINANMADI | Uygulanıyor; sapmalar: K57-C (H115), FITIL_OBEK (H220), Ç186, Ç188 gitsiz koşu | IZ_KARNE.ik_kontrol_kapisi; ORTAK_CETVEL.oc_kapi | KAPALI (kural) |
| H2 | Her aşamada aynı ölçüm kriteri; sonucu beğenmediğimiz için eşikle oynanmaz | 14 Kas (dört aşama), CLAUDE.md | Süreç kuralı | SINANMADI | Cetvel sha kilitli; sapma: S6 yazıcı eşik seçimini sonuçtan sonra değiştirdi (H210) | ORTAK_CETVEL.oc_kapi (CETVEL_SHA) | KAPALI (kural) |
| H3 | Yeni ölçüt: eşli fark, ay kümeli %95, sıra > 0,50, 200 rastgele portföy | 26 Eki ('ölçütü değiştir') | Ç151 K58, Ç177 güç | SINANMADI | Cetvel kuruldu; K58: δ +%2'de n ≤ 300 güç ≤ %11; portföy şartı gücü tavanlıyor (H177) | FON_IZI FI_OLCUT; ORTAK_CETVEL OC_ESIK | KAPALI (standart) |
| H4 | 'Kazandıran kırılım + stop + trail' rastgele hisseden / noktadan çok daha fazla kazandırmalı; bu test yok, aptallık var | 25 Eki, Ç91 | Ç91 K19 | TUTTU | İtiraz doğrulandı: cümle hiç ölçülmemişti, ölçülünce fark ~0 (BIST 2023 +%38 = rastgele +%40) | ORTAK_CETVEL plasebo 200 | KAPALI |
| H5 | Eski modeller sık hata yaptı; bul, doğrula, düzelt, yeniden koştur | 24 Eki, Ç84 | Ç84 (6 bağımsız denetçi) | TUTTU | ~30 ölçüm hatası, üretimde 11 hata; T10, öbek, D13, düzgün dip iddiaları düştü | YOK (üretim 11 hatası 'yaz' bekliyor) | AÇIK (üretim düzeltmeleri) |
| H6 | Batanlar neden test edilmiyor; o dönem parmak izine uyan bütün hisseler katılsın | 27 Eki, Ç107 | Ç107 | TUTTU | Batanlar eklenince etki üçte bir eridi, ABD-ADAY düştü | K34 / Tiingo (yalnız ABD nakit testi); ORTAK_CETVEL evreni yaşayanlar (K7 notu) | AÇIK (ABD batan fiyatı kotalı) |
| H7 | Kör set: hisse adı yok, sonraki mumlar yok; gerçek mum grafiği, ortak ölçek, geriye zum, alış mumu çizilsin | 25-26 Eki, 13 Kas | Ç95 kör set v2 / v4, Ç166 | TUTTU | Grafik itirazları doğrulandı: v2'de mum yapısı görünmüyordu (H64), v1.0'da otomatik ölçek (H140) | KOR_TEST, FITIL_KOR, FITIL_V2 kör set | KAPALI (kural) |
| H8 | Yanlış kabul ettiğimiz kural sonra doğru çıkabilir; ileri test, üç art arda aynı yön = kesin | 14 Kas | Ç175 denetimi | TUTTU | En az 20 eski 'İZ DEĞİL' kaydı aslında ÖLÇÜLEMEDİ (H165) | IZ_KARNE.IK_ILERI | KAPALI (kural) |
| H9 | İZ DEĞİL yalnız güç yeterliyken (n ≥ 1.000 ya da güç %80); aksi ÖLÇÜLEMEDİ | 14 Kas | Ç177 güç simülasyonu | SINANMADI | Kural; Ç177: güç %80 yolu gerçek veride açılmıyor, fiilen n ≥ 1.000 | ORTAK_CETVEL.oc_hucre_durum | KAPALI (standart) |
| H10 | Bütün yanlış hesapların kaydı alınsın (hata defteri) | 14 Kas | Süreç kuralı | SINANMADI | 221 satır; düşen iddiaların hepsi iyimserden gerçeğe (14 Kas sayımı) | IZ_KARNE.IK_HATA | KAPALI (kural) |
| H11 | İz ararken hatalar önceden okunsun, kod yazmaya öyle başlansın; bütün modeller için | 14 Kas | Süreç kuralı | SINANMADI | Mekanik kapı kuruldu; FON_IZI, BOFA_IZI, GENIS_KESIT, TAVAN_SERISI, KOR_TEST, GOZ_G5'te henüz yok | IZ_KARNE.IK_KONTROL + ik_kontrol_kapisi | AÇIK (6 modül) |
| H12 | Hedefli bağımsız denetim: iddia taşıyan, üretime ya da gerçek paraya dokunan işte yazan ve sınayan ayrı | 14 Kas | Süreç kuralı | SINANMADI | Uygulanıyor (S6 v1.1 bağımsız sınayıcı, T8 kaldırma) | YOK | KAPALI (kural) |
| H13 | Yapmayı alt modeller yapsın; ana model iş tanımı + denetim | 10 Kas | Süreç kuralı | SINANMADI | Uygulanıyor; alt ajan hataları IK_HATA'da (alt ajan kaynaklı 30+ satır) | YOK | KAPALI (kural) |
| H14 | MD defterini yalnız ana model değiştirsin | 11 Kas | Süreç kuralı | SINANMADI | Uygulanıyor | test_iz_karne (defter kapsamı) | KAPALI (kural) |
| H15 | Gerçek ve değerli bilgi basit ve erişilebilirdir; karmaşık ölçü basiti geçmiyorsa seçilmez | 9 Kas | Ç125, Ç128-Ç131, Ç132, Ç152 | TUTTU | Makine / çok metrik / CNN / LSTM bağımsız testte ek katkı vermedi (K48 AUC değişmedi, K51 katkı yok) | YOK | KAPALI |
| H16 | Sonuç olasılık tablosuyla: +%100 ve -%50 olasılığı kaç kat; 'bu var, şu yok' dili | 11 Kas | Ç154, Ç178+ | SINANMADI | Kural; ORTAK CETVEL olasılık satırı ekli | ORTAK_CETVEL (olasılık), K60.py | KAPALI (kural) |
| H17 | Çöl ardından gelen yükselişle değerlendirilir; sabit ufuktaki kapanış başarı ölçüsü değildir; 60 gün değil alımdan satıma | CLAUDE.md; 28 Eki (INTEM); 13 Kas (BofA) | Ç76-Ç77 (250 gün dip kırılmadan 2 kat), Ç92 (120 gün en yüksek), Ç171 (tutma dönemi), Ç188 HALKA 3 (r20, önce tavan mı dip mi) | TUTMADI | Ölçü değişince sonuç değişmedi: 2 kat katı 0,33-1,30, sağ ayak eşit, r20 +%0,0, önce tavan oranı -6,6 puan | YOK (ana ölçü ORTAK_CETVEL r60) | AÇIK (bkz. bölüm 5) |
| H18 | İz yok çıkarsa durma: denenen, yaklaşan, sıradaki 3 deneme önceden sabit eşikle | 24 Eki | Süreç kuralı | SINANMADI | Uygulandı (K14-K15, K57-B / C, K59-B) | YOK | KAPALI (kural) |
| H19 | Hiçbir yerde iz yok, o zaman kesin sen hata yapıyorsun | 28 Eki, Ç120-Ç121; Ç151 | Ç120-Ç121 hat kontrolü; Ç151 K58 | TUTTU | O gün 'hat sağlam' dendi (bilinen etkileri görüyor); 10 Kas K58: cetvel küçük etkiyi göremiyor, 'iz yok'un büyük kısmı aracın kabalığından | ORTAK_CETVEL güç tablosu | KAPALI |
| H20 | Sıkışma tanımın rastgele bölge seçiyor; son iki çıktı tamamıyla rastgele | 15 Kas (H186) | Ç166-Ç167 (G5 1 / 29), FENER S1 | TUTTU | G5 Cemal'in çöllerinin 1 / 29'unu yakalıyor; S1 FENER'de net -%6 kayan, BB 0,70 bölgeyi seçti (H193) | SIKISMA_CEMAL / SIKISMA_OBEK / S6 (yeni tanımlar) | KAPALI |
| H21 | Kutu neredeyse rastgele: bölgenin önceki ve sonraki küçük mumları dahil değil | 15 Kas (ENJSA S5 v1.1, H207) | Gösterge incelemesi | TUTTU | Kutu sabit 15 bar sayıyordu; sınır artık mumlardan | S6_TABAN (sınır mumdan); COL_S5_OBEK.pine v1.2 | KAPALI |
| H22 | Ücretli veri / abonelik yalnız açık onayla; Aralık Tiingo kotası kanıtlanmamış fikre harcanmaz | 12 Kas | Süreç kuralı | SINANMADI | Uygulanıyor (Ç166 İŞARET YOK → kota harcanmadı) | YOK | KAPALI (kural) |
| H23 | Fotoğraftan bölge tarihi tahmin edilmez; Cemal'den tarih alınır | 15 Kas (ENJSA H197, KNFRT H208) | Etiket denetimi | TUTTU | KNFRT tahmini aralıkta fiyat ~%80 yükseliyor (etiket yanlış); ENJSA tahmini Cemal'in bölgesi değildi | S6_TABAN S6_IZGARA_V11 puan_disi (KNFRT) | KAPALI |

### I. Tezler

| No | Kural (Cemal'in sözü, kısa) | Kaynak (tarih, Ç / görev) | Sınandı mı (Ç no, cetvel) | Sonuç | Neden (bir cümle) | Kodda (modül.şart) | Durum |
|---|---|---|---|---|---|---|---|
| I1 | Hedef: zarar etmemek, %100'ün üstü, ilk hedef 10x; küçük yüzdeyle girmek yetmez, büyük kazanmalıyım | 6 Kas, 11 Kas | Ç154 K60 olasılık tablosu | TUTMADI | +%100 olasılığını artırıp -%50'yi artırmayan özellik yok (asimetrik fırsat 0); taban 12 ayda +%100 %4-7, 3 yılda 10x ~%1 | K60.py; öneri modülü (YOK: 10x ölçüsü) | AÇIK |
| I2 | YEOTK daha da çıkar, DGXX kazanır; gerisi gürültü | 9 Kas son talimat | Karne 6 → 16 Kas | ÖLÇÜLEMEDİ | YEOTK +%10,7 (XU100 +%3,5), DGXX +%9,4 (IWM +%1,4); iki hisse, on gün | oneri_karne/karne.py | İLERİ TEST (60 gün eşli kıyas, Ocak 2027) |
| I3 | Fon yüzünden her şey %40+ düştü, artık çok düşmez; oynak hisse seçilince yükselme ihtimali yüksek | 16 Kas, Ç186 | Ç186 (sabit çöküş tanımı) | ÖLÇÜLEMEDİ | Tamamlanmış çöküş 1 (2023): oynak P+100 %73,9 vs taban %77,9 (kat 0,95); 2018 ve 2020 eşiği geçmedi | COKUS_OYNAK.py | İLERİ TEST Mart / Kasım 2027 |
| I4 | Fon krizinde 1 TL'ye inmiş hisse tavan serisi; devasa hacim barı; 1 liradan daha nereye düşer | 13 Kas, Ç168-Ç169 | Ç168, Ç169 | TUTMADI | Tavana katılmak eşlerden kötü (k=1 medyan -%3,9 KUMAR; duyarlılık -%12..-%29); hacimli tavan piyango (+%61 2,5 kat ama 60 gün -%14,8) | TAVAN_SERISI.py | İLERİ TEST Mart 2027 |
| I5 | Fon krizi: 31.08.2026 sonrası olağanüstü, çöl ve sinyaller teste girmez; düşüşler gerçek, bölünme değil | 27 Eki; COL_OZET 9.3 | K28 kriz denetimi | TUTTU | Sonuçlar krizden etkilenmemiş çıktı; taban serileri veri kayıtlarıyla birebir | ORTAK_CETVEL OC_ESIK 'kriz' 2026-08-31; FON_IZI FI_OLCUT 'kriz' | KAPALI (standart) |
| I6 | Bir hisseyi fazla alıcı olunca o bölgede çöl yapısı oluşur (BINBN fon almış, %1000) | 25 Eki, Ç97 | Ç97 (raporlu fon payı) | TUTMADI | Çölden sonra fon gelme 1,10-1,15; fon girişinden önce çöl 1,07; çölde fon varken sonrası kötü | FON_IZI k25 | KAPALI (AKD yok) |
| I7 | Piyango gibi sıçrayan hisselerde belirgin özellik vardır | 27 Eki, Ç105 | Ç105 (keşif / test) | TUTMADI* | Sıçrayanın izi 'oynak, ucuz, sığ' ama aynı iz çöküşü de getiriyor (asimetri yok) | FON_IZI k33 | KAPALI |
| I8 | Kripto +%100 günü önceden tespit edilir (RITUAL) | 8 Kas, Ç147 | Ç147 | TUTMADI | +%100 günü ancak 1 gün önce < %1 olasılıkla seçilebiliyor; sonrası 30 gün medyan -%49 | arastirma_cikti/kripto_yukselis | KAPALI (Cemal 9 Kas: kripto kapandı) |
| I9 | Tipik dönüş noktası makineye öğretilebilir | 28 Eki, Ç125, Ç127 | Ç125 K46, Ç127 | TUTMADI* | Makine öğreniyor (AUC 0,6-0,7) ama üst %5 sinyal 2023'te eşik altı; portföyde avantaj kayboluyor | FON_IZI k46 | KAPALI |

### J. Devir notu (Cemal'in başka bir Claude oturumundan getirdiği 'KOD DEVİR NOTU'; kaynak: DEVIR_NOTU_2026-11-17.md, eski oturum, tarihi yazılı değil)

| No | Kural (Cemal'in sözü, kısa) | Kaynak (tarih, Ç / görev) | Sınandı mı (Ç no, cetvel) | Sonuç | Neden (bir cümle) | Kodda (modül.şart) | Durum |
|---|---|---|---|---|---|---|---|
| J1 | Çöl swing tepesinden türetilmez; tek mumun H / L'i ile bant kurulmaz | Devir notu 17 Kas; eski oturum (§3) | Yok (tanım) | SINANMADI | Repodaki tanımlar zaten çok mumlu bant kullanıyor (S6 sınırı mumlardan, A6 / A8) | S6_TABAN bant (bölgedeki bütün mumlardan) | KAPALI (tanım) |
| J2 | Sabit % eşik yanlış; eşikler hisse başına (ATR / kendi oynaklığı) | Devir notu 17 Kas (§3) | Yok | SINANMADI | Küçük mum ATR250'ye göre ölçülüyor; ama bant (0,12), net değişim (0,03), AL payı (1,002) ve tavan %9,5 sabit yüzde | S6_TABAN kM x ATR250 (kısmen); bantMax / netMax / COL_v1.AL_PAY sabit % | AÇIK |
| J3 | Tek özelliğe bakılmaz: bölge, dip, Bollinger, küçük mum, doji, birikim izi, hacim kuruması BİRLİKTE | Devir notu 17 Kas (§3) | Ç41 D12 (4 imzadan ≥ 3), Ç58 SESSIZ_ML, Ç128 K48 (204 ölçü) | TUTMADI | Birleşik imza (D12) 6 dönemin 3'ünde tabandan iyi; çok ölçülü makine bağımsız testte ek katkı vermedi | COL_v1.col_dip (D12 imza, üretimde değil); S6 birleşik şart | KAPALI |
| J4 | Peş peşe büyük mumla bölgeden çıkılıyorsa çöl değil; BIST 'dev mum' (~%10) çöl içinde ASLA sayılmaz | Devir notu 17 Kas (§4) | Yok | SINANMADI | Açık şart yok; S6 küçük mum ve bant şartı dev mumu yalnız dolaylı dışlıyor (ana model notu) | YOK (dolaylı: S6 kM, bantMax) | AÇIK |
| J5 | İniş mumları (bölgeye giren büyük mumlar) çöle dahil edilmez | Devir notu 17 Kas (§4); repoda aynı itiraz 21 Eki (OYLUM / EUYO, H39) | Getiride ayrı ölçüm yok; A16 (D13 kutu yeni dipten) Ç47 | SINANMADI | Kod buna göre düzeltildi (D13 kutusu dipten başlar; S6 geriye uzatmada bant dışı iniş mumları alınmaz), ayrı ölçülmedi | COL_v1.col_dip2 (d = son 120 bar dibi); S6_TABAN refOnce / bant | KAPALI (tanım) |
| J6 | Bölgeden azıcık çıkıp dönmek olur; uzağa çıkıp dönmek çöl değil | Devir notu 17 Kas (§4) | Yok | SINANMADI | 'Azıcık' ve 'uzak' sayısı tanımlı değil; S6'da bant toleransı girdi olarak var ama ayrı kural yok | YOK (dolaylı: S6 dipTol 0,05, kirTol 0,02) | AÇIK |
| J7 | EN KRİTİK ÖZELLİK doji: dipteki kutuda 3-5 doji bile birikim / sıkışma işaretidir | Devir notu 17 Kas (§4); Eylül doji çarpanı; A13 DOJI_KUTU 19 Eki | Ç38 (koruma), Ç39 (yukarı, 0,90-1,02), col_ogren 9 Eki (doji çekirdeği), COL_OZET §3 (eski cetvel monoton) | ÖLÇÜLEMEDİ | Tek cetvelde doji kutusu yukarı hareketi artırmadı ama n < 1.000 (H165 listesi); col_ogren'de 5-8 doji ayırmadı; eşli / ortak cetvelde yeniden ölçülmedi | COL_v1 CARPAN doji (boyut) ve col_dip IMZA_DOJI (D12); üretim col_dip2 ve S6'da YOK | AÇIK |
| J8 | Çöl bir yıla kadar uzar, genişler, içinde sert silkelemeler olur | Devir notu 17 Kas (§4) | Ç181a D9 (6-12 ay, ORTAK CETVEL) | TUTMADI | Uzun dar bant eşlerden iyi değil (dört hücre TUTMADI, +%100 katı 0,40); S6 nMax 70 bir yılı kapsamıyor | COL_v1.uzun_col_olc; S6 nMax 70 | İLERİ TEST Mart 2027 |
| J9 | Bitişte çok küçük mumlar (3 ya da 7-8 adet) görülebilir (esnek, zorunlu değil) | Devir notu 17 Kas (§4) | Ç49 MUM_SUKUN v1.1 (son 3-4 mum küçülmesi) | TUTMADI | Son 3-4 mumun küçülmesi tek cetvelde 0,96-1,04 | MUM_SUKUN.py; üretimde YOK | KAPALI |
| J10 | Eğim / 'kanama' gürültüdür | Devir notu 17 Kas (§4) | A9 etiketleri (15 Kas) | SINANMADI | Sonraki etiketlerde Cemal eğimli pencereyi YANLIŞ dedi (net %8-10); kod net değişim sınırı koyuyor: bu madde A9 ile çelişiyor (bölüm 5) | S6_TABAN netMax 0,03 (tersi yönde) | AÇIK (Cemal kararı) |
| J11 | AL kuralı: dünkü aday + kapanış > tavan x 1,002; kapanışla kırılım high'dan güvenilir | Devir notu 17 Kas (§2, §4) | Ç91 K19 (kırılım girişi aynı gün eşli) | TUTMADI | Kırılım girişi rastgele hisseden iyi değil; high ile kapanış kırılımı ayrıca kıyaslanmadı | COL_v1.AL_PAY 1,002 (bugun_liste, kapanış) | KAPALI (giriş zamanlaması kapalı konu) |
| J12 | Segmentin en düşük dibi kırılırsa segment oradan yeniden hesaplanır | Devir notu 17 Kas (§4) | Yok (getiri) | SINANMADI | Tanım kodda var (yeni dip yeni kutu); sonucu ayrıca ölçülmedi | COL_v1.col_dip2 (d = son 120 bar dibi); S6_TABAN KIRILDI → yeni kutu | KAPALI (tanım) |
| J13 | İki kutu: kutu 1 = çöl (SMA200 civarı iyi), kutu 2 = raf | Devir notu 17 Kas (§4); CLAUDE.md iki kutu | Yok (SMA200 kısmı) | SINANMADI | Üç faz / iki kutu A4 / B3'te; 'SMA200 civarı' şartı hiç ölçülmedi | YOK | AÇIK |
| J14 | Daha önce 732 kırılımda çöl şekli tek başına yazı-tura çıktı (%36 yukarı, %32 aşağı); şekil tek başına yetmez | Devir notu 17 Kas (§4); kaynak yok (bu sayı repoda yok) | Aynı yönlü repo ölçümleri: COL_OZET §3 zıpla-düş ~%27, Ç91-Ç94, Ç96 / Ç178 | TUTTU | Repodaki bütün şekil / kırılım ölçümleri de eşlerden ayrışmıyor | YOK (bulgu, şart değil) | KAPALI |
| J15 | ABD hissesinde önce sermaye yapısı kontrolü | Devir notu 17 Kas (§5) | Ç155 K60-B kırmızı bayraklar (bilgi düzeyi) | SINANMADI | Kontrol DOSYA kapısında uygulanıyor (seyrelme, raf kaydı, ters bölünme bayrakları); kuralın kendisi bir sonuç ölçüsü değil | oneri tarama / DOSYA kapısı; K60B bayrakları | KAPALI (öneri modülünde) |
| J16 | Tek dosya, KURAL_MOTORU, tam hata yönetimi + log; doğru kısmı koru; isim çakışması mekanik yakalansın; test önbellekten okusun | Devir notu 17 Kas (§5); CLAUDE.md kod standardı | Süreç kuralı | SINANMADI | CLAUDE.md'de aynı kurallar | Modüllerde _cakisma_kontrol (çakışma kapısı); test_*.py | KAPALI (kural) |
| J17 | Bir ölçü bir testte artı, ötekinde eksi ise iz değil; küçük örneklem bulgu değil; tek izle karar yok | Devir notu 17 Kas (§5); CLAUDE.md test standardı | Süreç kuralı | SINANMADI | CLAUDE.md'de aynı; ORTAK CETVEL iki yarı şartı | ORTAK_CETVEL.oc_hucre (iki yarı, n ≥ 30) | KAPALI (kural) |
| J18 | Tarayıcı yalnız aday bulur; desen / göstergeye göre alım-satım yasak | Devir notu 17 Kas (§5); CLAUDE.md | Süreç kuralı | SINANMADI | CLAUDE.md'de aynı | COL_v1.bugun_liste (aday listesi) | KAPALI (kural) |
| J19 | Cevaplar Türkçe; 'yatırım tavsiyesi değildir' cümlesi yazılmaz | Devir notu 17 Kas (§5) | İletişim kuralı | SINANMADI | CLAUDE.md dürüstlük kuralı 'Claude yatırım danışmanı değildir' cümlesini ister: bu madde onunla çelişiyor (bölüm 5) | YOK | AÇIK (Cemal kararı) |

### K. Kör set 2 dersleri (Cemal'in el yazısı, 17 Kas akşam; kaynak arastirma_cikti/fitil_v2/KOR2_DERS_CEMAL.md ve kor2_cevap_cemal.json)

Cemal 40 sayfalık kör set 2'yi 'son mumda tam girilir mi' diye değil, formasyon + hedef + kağıt hafızası okuyarak işaretledi (26 yanıt: E 2, H 13, B 11; 14 yanıtsız). Aşağıdaki 14 kural o notlardan çıkarıldı; hiçbiri ölçülmedi.

| No | Kural (Cemal'in sözü, kısa) | Kaynak (sayfa) | Sınandı mı | Sonuç | Neden (bir cümle) | Kodda (modül.şart) | Durum |
|---|---|---|---|---|---|---|---|
| K1 | Formasyon hedefi küçük (+%5..+%10); 60 gün ölçüsü bunu ölçmez; hedef sonrası yeni yapı belirler | 17 Kas kör set 2 No 4 | Hayır | SINANMADI | ORTAK CETVEL r60 / 250 gün dokunma ölçer; 20 barda +%5 / +%10 'önce' ölçüsü yok | YOK (FITIL_V2 'önce KIRILIM/STOP' en yakın) | AÇIK: bilgi satırı olarak eklenir |
| K2 | Düz taban = yukarı formasyon (hedef önceki tepe), düz tavan = aşağı formasyon (hedef önceki dip) | No 4, 6, 8, 9, 14, 20, 23 | Hayır | SINANMADI | Tavan aynası hiç tanımlanmadı (SM_TEPE fitil aynasıydı, düz tavan değil) | S6 yalnız taban; tavan YOK | AÇIK: S6 ayna sürümü, ayrı ön kayıt |
| K3 | Kubbe kuralı: şemsiye aşağı, kazan (çanak) yukarı | No 5, 9, 21 | Hayır | SINANMADI | Eğri biçimi ölçülmedi; S6 düz bant arar | YOK | AÇIK |
| K4 | Çanağın yukarı dönüşü görülmeden giriş yok | No 5, 9, 10, 16-18, 24, 28 | Hayır (kör set 2 dolaylı) | SINANMADI | FITIL_V2 (4) dönüş istemez; kodun TAM günlerine Cemal'in H demesinin ana nedeni | FITIL_V2 s4 ters yönde | AÇIK: FITIL_V2 (3b) şartı |
| K5 | Taban kapanışla kırıldıysa o mumların hükmü yok; karantina | No 3, 12 | Hayır | SINANMADI | FITIL_V2 s2 yalnız 30 bar bakar | FITIL_V2 s2 kısmen | AÇIK |
| K6 | Tutmayan dip (alçalan dipler zinciri) = güven yok | No 16, 18, 24 | Hayır | SINANMADI | 60-120 bar dip zinciri ölçülmedi | FITIL_V2 s2 kısmen (30 bar) | AÇIK |
| K7 | Küçücük yapı güven vermez; yapı boyu düşüş bacağıyla orantılı | No 7, 13, 17, 28 | Hayır | SINANMADI | S6 nMin 8 / FITIL_V2 10 bar sabit; düşüşe oran yok | S6 nMin (sabit) | AÇIK |
| K8 | Kağıt hafızası: önceki formasyonlar hedefe gittiyse güven artar, patladıysa biter | No 8, 11, 25 | Hayır | SINANMADI | Hisse bazlı formasyon karnesi hiçbir modülde yok; Cemal'in en ağır şartı | YOK | AÇIK: yeni ölçü |
| K9 | SAT mumu: düz tavandan kopan ilk büyük kırmızı mum | No 8, 10, 14, 20 | Hayır | SINANMADI | Çıkışlar fiyat stopu; tavan kopuşu tanımı yok | takip.py T6/T10 (farklı) | AÇIK: C grubu |
| K10 | Çekiştirme (uçurum kenarında zayıf yukarı çeken el) = BELİRSİZ, bekle; REEDR örneği | No 22, 27 | Hayır | SINANMADI | Sinyal değil etiket; tanım REEDR'de doğrulanacak | YOK | AÇIK |
| K11 | Oluşum yoksa yön önceki yoldur; kod 'yapı yok' diyebilmeli | No 2, 19, 26, 29 | Hayır | SINANMADI | FITIL_V2 No 19 ve 29'a TAM dedi; sessiz kalma şartı yok | YOK | AÇIK |
| K12 | Geçmişte dev tek mum (fitil > +%100) varsa kağıt şüpheli (kripto gibi) | No 1 | Hayır | SINANMADI | Devir notu J4 ile akraba; boyut kuralı | YOK | AÇIK (G grubu) |
| K13 | Üç kez tepen taban: üçüncü sekmede girilebilir ama Cemal'in yapısı değil | No 10 | Hayır | SINANMADI | Düşük öncelik | YOK | AÇIK, düşük öncelik |
| K14 | Geri test hedefi büyütür (asıl giriş retest; iki kutu 2. giriş) | No 15 (tek E TAM sayfası) | Hayır | SINANMADI | A4 / B3 ile aynı; ölçülmedi | COL_v1 yorumu, şart yok | AÇIK: A4 ile birleşir |
| K15 | UFUK 15 MUM: kodun gördüğü yapılar en fazla 15 mumun geleceğini gösterir; 60 gün ölçüsünde rolleri yok. Eski 20-60 mumlu büyük çöller fon iziydi; gerçek hissede küçük yapılar, hedef <= 15 mum | 17 Kas akşam ('bunu kaydet'), CLAUDE.md UFUK 15 MUM | Hayır | SINANMADI | Yapı kuralları 15 barla hiç ölçülmedi; Ç187 / Ç189 60 günlüktü | ORTAK_CETVEL ufuk 60 sabit (15 parametresi yok) | AÇIK: cetvele ufuk 15 eklenir, Ç187 / Ç189 / S5 / S6 yeniden ölçülür |
| K16 | Büyük çöl (TEHOL / BINBN / KETLV, 20-60 mum, çok katlı hedef) gerçekti ama yalnız fon gibi satmayan alıcı grupları girince oluşur (manipülasyon); o dönem kapandı, tekrarı neredeyse imkânsız (müdahale). Büyük çöl aranmaz; küçük yapı + 15 mum hedefi aranır | 17 Kas akşam | Dolaylı (K12 FON_IZI fon lekesi; Ç147 kripto) | SINANMADI | Tez; fon alıcılı yapı sınıfı ayrı etiketle not edilir, giriş kuralı olmaz | FON_IZI K12 (fon izi), COL_v1 fon süzgeci | KAPALI DÖNEM (tez kaydı) |
| K17 | SON DERS: fon çöllerinden öğrenilen kurallar gerçek ve bugün geçerli (alt fitili az mumlar + dip savunması = yukarı, tersi aşağı) ama etkisi kısa; hedef %5-10 tutulur; eski çöle benzer yapı oluşursa manipülasyon; kurum girişinde benzer yapı en fazla 3-5 günlük | 17 Kas akşam ('kaydet, artık bu kural geçerli') | Hayır (15 bar / %5-10 ölçüsüyle hiç ölçülmedi) | SINANMADI | Ç187 / Ç189 60 günle ölçüldü; şekil + savunma + kısa hedef birlikte sınanmadı | FITIL_V2 s1 + s2 (şekil + hat) var; hedef / ufuk yok | AÇIK: 15 bar + %5 / %10 ölçüsüyle ilk koşu |
| K18 | YENİ TEST STANDARDI: giriş = dip tavanı / taban kırılım mumu; hedef +%5 / +%10 = 'ulaştı'; takip stopu yukarı revize, yeni ters oluşuma kadar; ilk hedefte stop hedefe yakın; 60 gün testi kapandı. Takip stopu geçici, daha iyisi testle eklenir | 17 Kas akşam ('testler bu şekilde devam etsin') | Hayır | SINANMADI | Cetvel henüz yazılmadı | YOK (ORTAK_CETVEL 60 gün) | AÇIK: cetvel + ilk koşu |
| K19 | Büyük desen önce: küçük kutu 120-250 barlık büyük yapının içindeyse karar büyük yapıya göre; alçalan büyük kanalda küçük taban girilmez; stop büyük dip | PDF notları s6, 10, 14, 16, 29, 31 | Hayır | SINANMADI | S6 nMax 70; büyük yapı tanımı yok | YOK | AÇIK: Y6 şartı |
| K20 | Hat net olmalı: >= 3 dokunuş, eğimi aşağı değil; 1-2 mumluk hat hat değil | s7, 16, 17, 27, 28 | Hayır | SINANMADI | S6 dibi = min Low (tek mum); FITIL HAT 10 bar dibi | S6 / FITIL_V2 (tek mum) | AÇIK: Y6 |
| K21 | Giriş mumu gerçek kırılım: kapanış tavanı ancak dokunuyorsa giriş yok (pay + gövde) | s9 (MKC) | Hayır | SINANMADI | YAPI_HEDEF Y1 pay 0; üretim AL_PAY 1,002 | COL_v1 AL_PAY (üretim) | AÇIK: Y6 |
| K22 | Kazan şemsiye değil: simetrik çanak + dipte küçük mum + dip savunması; a > 0 uyumu yetmez | s21, 23, 24 (yok), s19 (doğru) | Hayır | SINANMADI | Y3 tanımı V dibi / dağınık pencereyi de seçti | YAPI_HEDEF Y3 (gevşek) | AÇIK: Y7 |
| K23 | Stop uzaklığı: giriş-hat > %10 ise işlem yok ya da ana stop %5; stop büyük desenin dibi | s22 (%25 'çok büyük stop'), s37, s16, s29 | Hayır | SINANMADI | Y3 stop uzaklığı medyanı %19,8 | YOK (stop0 = hat x 0,98) | AÇIK: Y6 / Y7 (a), bilgi (b) |
| K24 | Hedef önceki tepe; tepede ters formasyon oluşunca çık | s12, s22 | Hayır | SINANMADI | D2 / D9 ile aynı | YOK | AÇIK (D2) |
| K25 | Kağıt hafızası Cemal tanımı: aynı hissede benzer yapı patladıysa girilmez (S6 AL sayımı değil) | s15 (TURGG) | Y4 benzeri ölçüldü (farklı tanım) | SINANMADI | Y4 tanımı Cemal'inki değil (H kaydı) | YAPI_HEDEF Y4 (farklı) | AÇIK: Y8 |
| K26 | Dip savunması şart: küçük mumlu sıkışma tek başına yetmez | s30 (MNKD) | Hayır | SINANMADI | D4 / K19 ile aynı | YOK | AÇIK: Y6 |
| K27 | Zayıf hat = +%5 hedef; yeniden hat oluşursa yeniden girilir | s17 (SDTTR) | Hayır | SINANMADI | Hedef hat gücüne bağlı; ölçü yok | YOK | AÇIK |
| K28 | Patlamış yapı / 10 barlık küçük bölge = yapılacak şey yok (Y5 nMin 15) | s37, s38 | Hayır | SINANMADI | Y5 bölge boyu medyanı 13 bar | YAPI_HEDEF Y5 nMin 8 | AÇIK |
| K29 | Tavan = ilk dip yapısının tavanı; rastgele tavan hattı çizilmez | s31 (RYGYO) | Hayır | SINANMADI | S6 en büyük pencereyi seçer | S6 pencere seçimi | AÇIK |
| K30 | Fitil teorisi: üst fitiller uzamışsa yukarıdaki satıcı emiliyor (aşağı beklenmez); altta alıcı yoksa uzun alt fitil oluşur; fitilsiz kısım yukarıdaysa yön tersi | 18 Kas hakem PDF s1, s5 | Hayır | SINANMADI | E1 / E2 (Ç187) fitil asimetrisinin ters yorumu; yön bağlama göre | FITIL_OBEK ASİM (yönsüz) | AÇIK |
| K31 | Giriş teyidi: kırılım mumu gün sonu kapanışla + ertesi gün kalıcılık (iki gün tavan üstünde kapanış); tek mumla girilmez | s23, s24 | Hayır (kapalı konu 'giriş onayı' ile çakışır) | SINANMADI | Cemal'in kendi kuralı; COL_OZET kapalı konu listesiyle çelişki (kaydedildi) | COL_v1 AL tek kapanış | AÇIK: Cemal kararı |
| K32 | Parmak izi: büyük yeşil alış mumundan hemen önceki 4 mum dibe yakın, alt fitili kısa öbek | s25 | Kısmen (Ç187 S+ öbeği, k 10 bar) | ÖLÇÜLEMEDİ | Ç187 k = 10 bar öbeğiydi; '4 mum + kırılım mumu' tanımı ölçülmedi | FITIL_OBEK (k 10) | AÇIK |
| K33 | Kazan çizimi = OLUR, şemsiye çizimi = OLMAZ; Cemal kör yarıda 19 sayfanın 8'ine OLUR dedi (vekil 300'de 6): vekil göz Cemal'in gözü değil (kappa -0,13) | hakem PDF kör yarı | Evet (hakem, n 19) | TUTMADI (uyum) | Vekil etiketleri ve göz skoru (Ç192) Cemal'in gözünü temsil etmiyor | GOZ_ETIKET etiket.json | KAPALI: Ç192 yorumu düzeltildi |
| K34 | CD1-CD7 Cemal'in hakem dersleri: fitil teorisi bağlamsız yön vermez; tepede raf OLMAZ / BELİRSİZ; kazan yetmez dönüş görülmeli; en güzel taban stop olabilir (şekil güzelliği); iki gün teyit korudu | 18 Kas hakem seti (s1, 5, 6, 14, 24, 25, 28, 35) | Evet (n 40, bilgi) | SINANMADI | Sayfa başına tek olay; p 0,06-0,15 | YOK | AÇIK: 100 sayfalık set |
| K35 | VD1-VD4 vekil / ana model dersleri: kural toplamı göz değil; stop %10 ve kırılım payı süzgeçleri hedefe gidenleri eliyor; 'kararsız' grup en iyi grup; önce hakem sonra eğitim | 18 Kas hakem seti (s2, 4, 9, 15, 23, 25, 26, 28, 30, 33, 35) | Evet (n 40, bilgi) | TUTMADI (vekil) | Vekil OLUR 0 / 6 hedef | GOZ_ETIKET C11 / C5 (vekil kuralı) | KAPALI: vekil yaklaşımı bırakıldı |
| K36 | CD8 / CD9 (TUR 1): 'kodun bölgesi yanlış' ile 'fiyat gitmez' ayrı hükümler; şemsiye çizimi tek başına OLMAZ değil | TUR 1 s9, 11, 17, 26, 30 | Evet (n 30, bilgi) | SINANMADI | Tek tur | YOK | AÇIK |
| K37 | VD6-VD8 (TUR 1): dipte kazan OLUR için dönüş + gövdeli kırılım; tepe rafı iki tür (dağıtım / yükselen trend rafı); kırılım mumu tavanı ortalamalı (Cemal s2) | TUR 1 s2, 3, 5, 6, 8, 20-23 | Evet (n 30, bilgi) | SINANMADI | Tek tur; VD7 Y9c ile çelişiyor (n küçük) | TUR 2 model kuralı; YAPI_HEDEF Y1c adayı | AÇIK |
| K38 | CD13 / CD14 (TUR 2): büyük kırılım mumu tek başına eleme nedeni değil; alçalan büyük resimde kazan ✓ üçüncü kez yanılttı; kararsızlık fırsat kaybı | TUR 2 s2, 10, 15, 30, 12-21 | Evet (n 30, bilgi) | SINANMADI | Tek tur | YOK | AÇIK |
| K39 | VD9 (TUR 2): gevşetilen kurallarla model OLUR'u 21'e çıktı, isabet %48 = taban; OLUR için üç şart birlikte (dönüş + gövdeli ortalayan kırılım + yükselen / yatay büyük resim) | TUR 2 model 11 / 21 yanlış | Evet (n 30, bilgi) | SINANMADI | TUR 3'te sınanır | TUR 3 model kuralı | AÇIK |
| K40 | U DİP + PARABOLİK DEVAM (19 Kas, S7 PDF No 38): seçilen sıkışma bölgesi U dip çizmeli, sağ kenarı parabolik kalkmalı; alçalan dipler zincirindeki durak (daha derin dip gelebilir) bölge değil | S7_BOLGE_2016-22.pdf No 38 (AVR; gelmedi) | Evet (mekanik Ş9, Y11) | SINANMADI | YAPI_HEDEF 5. tur | Ş9 (Y11) | AÇIK |
| K41 | CD15 (TUR 4): kod iki adaydan kötüsünü seçmişse (önceki dip savunması / kazan daha net) hedef gelmez; mahkeme 'ÖNCEKİ BÖLGE DAHA UYGUN' = OLMAZ | TUR 4 s13, 18, 29, 30, 32: 5 / 5 gelmedi | Evet (mahkeme) | SINANMADI | TUR 5 model kuralı | mahkeme | AÇIK |
| K42 | CD16 (TUR 4): 'sert düşüş sonrası zaman / haber lazım' tereddüdü fırsat kaçırır (BELİRSİZ 6 / 10 gitti) | TUR 4 s19, 28, 31, 33, 35, 40 | Evet | SINANMADI | bilgi | - | AÇIK |
| K43 | CD17 (TUR 4): önceki toparlanma sert / hızlıysa bu da hızlı olur | TUR 4 s5, 6, 20, 21: 2 / 4 (2 stop) | Evet (C8 kağıt hafızası) | SINANMADI | - | - | AÇIK |
| K44 | CD20 (TUR 4): hat x 0,98 stopu U dip havuzunda dar; OLUR'ların 4 / 9 yanlışı stop (s5 sonra +%86) | TUR 4 s5, 6, 8, 27 | Evet | SINANMADI | ileri test (stop eşiği önceden) | - | AÇIK |
| K45 | CD21 (TUR 4): 'önceki kazan bitmedi / ikinci kazan daha derin / satıcı bitmedi' OLMAZ gerekçeleri 4 / 4 yanılttı; derin ikinci dip tek başına eleme değil | TUR 4 s10, 17, 37, 39 | Evet | SINANMADI (ters emare) | TUR 5 model kuralı | - | AÇIK |
| K46 | VD10 (TUR 4, model): 'büyük resim yükselen' şartı düşüş sonrası dip havuzuyla çelişir; dipte havuzda uygulanmaz; OLUR = dönüş + gövdeli ortalayan kırılım; eleme yalnız K41 ve dev mum | TUR 4 model OLMAZ 18 / 38 gitti, OLUR 2 / 2 | Evet | SINANMADI | TUR 5 | TUR 5 model kuralı | AÇIK |

## 3. SONRADAN YANLIŞ ÇIKAN DOĞRULAR

### 3a. Eski 'GEÇERLİ / İZ / ADAY / BAŞARILI' denip sonra düşenler

| Eski iddia | Eski etiket (tarih) | Sonraki sonuç | Neden düştü | Kaynak |
|---|---|---|---|---|
| A1 bedelsiz bildirimi sonrası düşüş | GEÇERLİ ar60 -12 / -6 (4 Eki) | Tek cetvel İZ DEĞİL (BIST 2 / 3 dönem, ABD yok) | Eşli taban yoktu; fark hissenin zaten yükselmiş olmasından | Ç15, H49, karne.csv |
| A2 tavan günü sonrası düşüş | GEÇERLİ (4 Eki) | İZ DEĞİL (1 / 4 hücre); ABD'de tavan sonrası İYİ (Ç112) | Eşli taban; BIST'e özgü (tedbir, tavan kuyruğu) | Ç16, Ç112, H49 |
| A3 taban günü, A4 koşmuşken sözleşme, A9 olgun rüzgâr + sözleşme | GEÇERLİ (4 Eki) | İZ DEĞİL | Eşli tabanda tutmadı | Ç17, Ç18, Ç19 / Ç71, H49 |
| B1 geri alım bildirimi | GEÇERLİ ar60 +4,9 / +2,4 (4 Eki) | İZ DEĞİL; 13 Kas çöküş sonrası tek olayda EMARE | Eşli taban (sıradan dönemde); çöküş sonrası ayrı bağlam | Ç26, Ç170 |
| A13 dipte doji kutusu = sert düşüş riski düşük | BIST GEÇERLİ risk (19 Eki) | Eşlide tutmadı; sonra ÖLÇÜLEMEDİ listesinde | İleriye bakan 'kirilim' sütunu ile seçilmişti; kontrol (dojisiz dip) yoktu; etki dipte olmaktan | Ç38, H26, H48, H165 |
| A14 blok hacimli taban günü | Ham kat 1,9-2,9 (23 Eki) | ÇÜRÜDÜ (eşli 0,91-1,73); ABD 2024-26 +%14,9 tuttu, 2023 tutmadı | Eşli taban yoktu (zaten sıçramış hisse) | Ç60, Ç112, H46 |
| B13 çöl kırılımı + rüzgâr | ADAY piy60 +16,6 / +26,9 (4 Eki) | Gerçek zamanda tutmadı | Giriş 'çölün son günü' = sonradan bilinen bilgi | B13, H19 |
| B14 yuvarlanma öbeği alım oranı +15-20 puan | ADAY yön (21 Eki) | Düştü | Mekanik (taban kutusu tavana 2 kat uzak); işlemlerin yarısı kopya | Ç44, H33 |
| D13 'alım +12..26p, bozulma %2-9' | Tespit bulgusu 6 / 6 (21 Eki), üretime alındı | Mesafe eşli +0,5..+3,8; tek cetvel 0,97 / 0,98 | Mekanik (dibe / tavana uzaklık farkı) | Ç47, H36 |
| T10 stop maliyete '+157 vs +144' | Üretime yazıldı (21 Eki) | Ters: +144 vs +155, ABD 0 vs +6 | Kopya işlemler, hisse başına tek slot yok, trail ufuklu | Ç45, H34 |
| COL_OZET §1 'doğrulanmış sonuçlar' (kırılımda gir + trail, %73-90 kazanan) | Doğrulanmış (18 Eyl) | Aynı gün rastgele hisse kadar | Mutlak getiri = piyasanın sayısı; rastgele kıyas yoktu | Ç91, H60 |
| Eski %74 / +14,8 | Sistem sonucu (Eylül) | %64 / +8,9 | Ufuk 250, tekilsiz, maliyetsiz | H12 |
| '12 elle işaretli çöl: kod 9 doğru, 0 kaçırma' | Segment sağlam (Eylül) | 29 çöllük sette 13 / 26 | Küçük örneklem | COL_OZET §7, H15 |
| D9 uzun çöl yön %56-61 | ADAY, 'test sürüyor' (18 Eki), üretim ekranında (T8) | İZ DEĞİL (Ç181a), T8 kaldırıldı | Eşsiz kıyastı; eşlerle sakin hisse seçtiği görüldü (+%100 katı 0,40) | Ç37, Ç181, H166 |
| Düzgün dip '-%20'yi daha sık getirir' | Gözlem 1,00-1,93 (24 Eki) | 0,75-1,31, gözlem geri alındı | Eşli kutu geleceğe göre seçiliyordu | Ç77, H55 |
| K33-B nakit tükenmesi küçük şirket | ABD-ADAY (27 Eki) | GEÇERSİZ, sonra İZ DEĞİL | Evren yalnız yaşayanlar; batanlarla etki üçte bir eridi | Ç106-Ç107, H70 |
| K51 'en yakın aday' (küçük artı etki) | Aday yorumu (29 Eki) | Düştü | Etkinin tamamı bugün işlem görenlerden | Ç132, H82 |
| 'BIST momentum +%7-10' | Mesaj ve DERS 32 (28 Eki) | Geçersiz; momentum ABD zayıf, BIST yok | Taban pazar medyanıydı (sağa çarpık r60) | Ç121, H78 |
| K45 'KISA İZ' (INTEM +%8) | KISA İZ ama zayıf (28 Eki) | EMARE → ileri testte ÖLÇÜLEMEDİ, yön zayıfladı | Düz rastgele taban oynak bölgeyi kayırıyordu; görülmemiş veride +2,7 puan | Ç124, Ç180, H79 |
| VDYT Motor 1 / 2 'basitten iyi'; VDYT2 'bölgeyi bulmak BAŞARILI' | BAŞARILI (12 Kas) | İZ DEĞİL / tanımsal | Hedef penceresi karar gününü içeriyordu; yön konumdan mekanik; büyük mum bölgenin kendi mumlarına göre | Ç162-Ç164, H134, H136, H161 |
| Kuruş hisse lot listelerinde 'işaret ters' (BofA) | Anlamlı ters (13 Kas) | Kalktı (aralık 0'ı kapsıyor) | Kirli ayrıştırma (5 ayrıştırma hatası) | Ç171, H154 |
| 'BofA normal dönemde piyasa gibi +%3' | İfade (13 Kas) | Değişti | Sayfa tarihi ile satır tarihi karıştı (Eylül listesi Haziran sayıldı) | H151 |
| Çölde içeriden alım ABD 2023 +%7,3 (dört şart tuttu) | Tek hücre (27 Eki) | 2016-22'de ters; İZ DEĞİL | Tek dönem | Ç102, Ç118 |
| Çöl + güçlü bilanço sürprizi 2023-26 dört hücrede artı | (27 Eki) | 2016-22 BIST'te ters | Tek dönem | Ç100 |
| COMP4 U2 +%5,5 / yıl (t 2,30) | Aday (11 Kas) | TUTMAZ | Son %30 ayda -%0,06 / ay; bilinen faktörlerle açıklanıyor | Ç152-Ç153 |
| Fon 'ilk kez girdi' → 3 ay +11,9 | İzleme listesi (Eylül) | Fon girişi İZ DEĞİL (0,92-1,03) | Tek dönem n 90; fonlar yükselmiş hisseye giriyor | COL_OZET §3, Ç65 |

### 3b. Eski 'İZ DEĞİL' denip sonra ÖLÇÜLEMEDİ'ye dönenler

| Eski karar | Yeni etiket | Neden | Kaynak |
|---|---|---|---|
| Ç38, Ç39, Ç50, Ç57, Ç67-Ç70, Ç73-Ç83, Ç87, Ç89, Ç90 (tek cetvel İZ DEĞİL) | ÖLÇÜLEMEDİ | n < 1.000 ve güç kanıtı yok (14 Kas kuralı) | H165, IK_ACIK 'ESKİ ETİKET DÜZELTMESİ' |
| Ç100-Ç151 dönemindeki FI_OLCUT 'İZ DEĞİL'lerin çoğu (bu taslakta TUTMADI*) | ÖLÇÜLEMEDİ | K58: δ +%2'de n ≤ 300 güç en çok %11; dört hücre birden ~%0,2 | Ç151, H118, IK_ILERI |
| Ç96 K24 iki evre çöl | ÖLÇÜLEMEDİ | ABD 2023 güç %52, AVR güç %29 (yalnız ABD 2024-26 güç yeterli ve TUTMADI) | Ç178, IK_ILERI |
| Ç37 D9 + rüzgâr ('test sürüyor') | ÖLÇÜLEMEDİ | ABD 2023 n 870 güç %52; AVR sektör yok | Ç181b |
| Ç75 düzgün dip, Ç78 iki yuvarlama | ÖLÇÜLEMEDİ (ayrım) | FON_IZI tarayıcı geleceğe bakıyordu (n < 400 toplam uzunluk); ortak cetvelde C n250 < 1.000 | Ç179, H178 |
| Ç164 BIST 'BAŞARISIZ' (VDYT2-B) | ÖLÇÜLEMEDİ | Bölge tarafında 6 / 12 olay, aralık 0'ı içeriyor | H160 |
| Ç181c yalnız rüzgâr 'İZ DEĞİL (AVR verisi yok)' | EMARE (ABD) | Kurala göre AVR verisi yoksa en fazla ABD-ADAY; portföy şartı düştüğü için EMARE | H182 |
| Ç166 kör test 'İŞARET YOK' | ÖLÇÜLEMEDİ | Cemal tek tek işaretlemedi; yanıt yok | IK_ILERI |
| Ç173 dipte BofA 'yol yok' | ÖLÇÜLEMEDİ | Kriz öncesi olay 0; 'yol yok' sözü ölçülemedi için kullanılmaz | IK_ILERI, CLAUDE.md |
| Ç174 / Ç176 sıkışma İZ DEĞİL | Yalnız S1 tanımı için geçerli | S1 Cemal'in sıkışmasını seçmiyor (FENER); Cemal tanımlı S4 / S5 ayrı ölçüldü | H186, H193 |

### 3c. Cemal'in reddedilen ya da ölçülemeyen sözlerinden sonradan doğru çıkanlar

| Söz | İlk cevap | Sonra | Kaynak |
|---|---|---|---|
| 'Hiçbir yerde iz yok, kesin sen hata yapıyorsun' (28 Eki) | Hat bilinen etkileri görüyor (Ç121) | K58: cetvel küçük etkiyi göremiyor (güç ≤ %21) | Ç121, Ç151, H118 |
| 'Sıkışma tanımın rastgele bölge seçiyor' (15 Kas) | Ç174 / Ç176 güç yeterli İZ DEĞİL | S1 Cemal'in bölgelerini seçmiyor; karar yalnız S1 için | H186, H193 |
| 'PAPIL'e has değil' (16 Kas) | Parmak izi PAPIL'e özgü, kural adayı değil | Kod S+ TEHOL, BINBN, PAPIL'in üçünde yanıyor (algılama çalışıyor); sonuç yine ayrışmıyor | CEMAL_COL_KURALLARI, Ç188 |
| 'BofA %40-80 zarar etmez' (13 Kas) | -%40..-%65 'BofA zararı' diye yazılmıştı | Bunlar 20 gün sonraki fiyat, gerçekleşen zarar değil; ifade düzeltildi | H156 |
| 'VBTYZ ağır hantal, 10x ihtimali sıfır' (16 Kas) | VBTYZ tek DOSYA geçen | Kullanılan ölçüler patlama olasılığını ölçmüyordu | H212 |
| 'Her işte yanlışlık var' (13 Kas) | — | Kuruş hisse 'ters işaret' kalktı; BofA ayrıştırma 5 hata | H149-H154 |
| 'Bir yıldır yanlış hesapların kaydı yok' (14 Kas) | — | 158 (bugün 221) hata satırı; ~20 iddia geri alındı | IK_HATA |
| 'Batanlar test edilmiyor' (27 Eki) | — | Batanlarla etki üçte bir eridi | Ç107 |
| 'Kazandıran kırılım + trail rastgeleye göre ölçülmemiş' (25 Eki) | — | Ölçülünce fark ~0 | Ç91, H60 |

## 4. KODA ENTEGRASYON ÖNERİSİ

### 4a. Kodda olan kurallar

| Kural no | Modül.şart | Not |
|---|---|---|
| A1, A16, A17 | COL_v1.col_dip2 (SEGMENT_MOD='dip2') | Üretimde; dayanak düştü (Ç47) |
| A3 | COL_v1.MUM_OLCU='aralik' | Tanım |
| A4, A5 | FON_IZI.fi_k24_tara; K24_YENIDEN | Ölçüm modülü; 3. evre yok |
| A6-A10, A13, B1, B2 | S6_TABAN.S6_PRM (nMin 8, nMax 70, bantMax 0,12, netMax 0,03, kM 0,90, dipTol 0,05, bbSart 0,30), AL / KIRILDI | Göz aracı + Pine; sonuç ölçümü yok |
| A11, A12 | SIKISMA_OBEK.so_s5 (sınıf DİP / YOL) | S5 ön kayıtlı |
| A14 | COL_v1.uzun_col_olc | Ekrandan kaldırıldı (T12) |
| A19, A20 | FON_IZI k13b / k16 / k17; DIP_COL_AYRIM | Ölçüm |
| A21 | SIKISMA_CEMAL (SC_ESIK) | Ölçüm |
| B1 | COL_v1.AL_PAY 1,002 | Üretim AL |
| B7, B8, B9, A2 | FITIL_V2.fv_kural s3 / s2 / s4 / s5 | Aşama 2 bekliyor |
| B12 | FON_IZI k45; INTEM_ILERI | İleri test |
| B14 | FITIL_KOR (SPD, SPDb) | Bilgi satırı |
| B15, F10, F11 | BOFA_IZI | İleri test |
| C1 | takip.TABAN_TOL 0,02 (T6) | Üretim; testle çelişiyor |
| C2 | takip.MALIYET_ESIK 8,0 (T10) | Üretim; dayanak ters döndü |
| C3 | COL_v1.HEDEF 20 + takip trail SMA20 / 120 bar | Üretim |
| D1, D2 | COL_v1.RUZ_ESIK 0,10 / RUZ_MUTLAK 0 (sektor_ruzgar); takip ruz% | Üretim (bilgi sütunu) |
| D7, H3, H9, I5 | ORTAK_CETVEL (OC_ESIK karar hücreleri, 'kriz' 2026-08-31, oc_hucre_durum); FON_IZI FI_OLCUT | Standart |
| E1, E2 | FITIL_OBEK (FO_ESIK); COL_FITIL_OBEK.pine | İleri test |
| E4, G8 | COL_v1.carpanlar_hesapla (CARPAN), cds_rejim | Üretim boyutu; yeniden doğrulanmadı |
| F1, F2 | K57.py; oneri tarama_kosu | Kapandı |
| F8 | COL_v1.FON_ESIK 5,0 + FON_TASFIYE (D8); takip T7 | Üretim süzgeci |
| F12 | GENIS_KESIT.py | İleri test |
| H1, H2, H11 | IZ_KARNE.ik_kontrol_kapisi; ORTAK_CETVEL.oc_kapi | 6 modülde kapı yok |
| H8, H10, H14 | IZ_KARNE.IK_ILERI / IK_HATA; test_iz_karne | Defter |
| I3, I4 | COKUS_OYNAK.py; TAVAN_SERISI.py | İleri test |
| J5, J12 | COL_v1.col_dip2 (yeni dip yeni kutu); S6_TABAN KIRILDI / refOnce | Tanım |
| J7 | COL_v1 CARPAN doji; col_dip IMZA_DOJI | Yalnız boyut çarpanı ve D12; S6 / dip2'de yok |
| J11 | COL_v1.AL_PAY 1,002 (kapanışla) | Üretim AL |
| J16-J18 | Çakışma kapısı; ORTAK_CETVEL iki yarı şartı; bugun_liste | Süreç |

### 4b. Kodda olmayan kurallar ve önerilen şart (tek satır)

| Kural no | Kural (kısa) | Önerilen şart (tek satır) |
|---|---|---|
| A4 (3. evre) | Bölgeye sert test, sonra hareket | `test3 = kırılımdan sonra 60 gün içinde Low <= tavan x (1 + 0,02) ve kapanış > tavan` (al mumundan sonra ilk geri test günü; ayrı ön kayıt) |
| A15 | Çöl nadir | `nadir = hisse-yıl başına S6 bölge <= 1` sayımı ön kayıtta raporlanır; sinyal şartı değil, tanım denetimi |
| A18 | Aşağı kırılıp toparlanan çöl kaçmasın | `toparlanma = KIRILDI sonrası 20 gün içinde kapanış > taban` ise bölge 'yeniden açık' sayılır (S6 durum makinesi) |
| B3 | İki kutu girişi + bölge testi yukarı dönerse ekleme | `ekle = pozisyon kârdayken ve Low <= ilk kutu tavanı x 1,02 ve ertesi kapanış > önceki gün High`; zarardaki isme ekleme yasağı (G2) ile birlikte |
| B4 | Kutu içi tepe aşılmadan alım yok | `al = kapanış > max(High, bölge)` (S6 AL ile aynı; kutu içi sivri tepe = K6b tavan) |
| B10 | Kim alıyor (kurumsal) | Veri yok; `kurumsal = AKD ilk 5 alıcıda yabancı / kurum payı >= %20` ancak ücretli AKD onayıyla |
| B11 | Sağ ayak rastgeleden iyi | Şart değil; ölçüt: `sağ ayak = al mumundan sonraki 120 gün en yüksek / eşli aynı gün` (ORTAK CETVEL bilgi satırı) |
| B13 | Yükselişte al, dipte dönüş varsayımıyla alma | `trend = kapanış > SMA200 ve SMA50 eğimi > 0` bayrağı; aday listesine yalnız bilgi sütunu |
| C4 | Son büyük mumda büyük kısmı sat | `sat_kismi = poz kârdayken gün aralığı >= 2 x ATR250 ve kapanış aralığın üst %25'inde -> %50-70 sat` |
| C5 | Tepe mumları aşağı gösteriyorsa çık | `tepe_cik = kapanış >= 120 gün en yüksek x 0,95 ve S- (FITIL_OBEK) yanıyor -> çık` |
| C6, C7 | Bilanço günü çıkış kuralları | `olay_cik = bilanço günü getiri >= +%25 -> 1/3 sat; NT 10-Q / going-concern ağırlaşması -> ertesi açılış sat` (takip'e olay sütunu) |
| D3-D6, B5, B6, C8, D9, E3, E10 | Sebep, patlama rüzgârı, büyükler önce, ABD öncü; hacim beklentisi; küçük alım mumu / birikim; sektör %1 → %10; SMA atılımı; 'PAPIL'e has değil'; D12 imzası | Ölçülüp tutmadı; şart önerilmez |
| G7 | BIST'te fiyat stopu çalışmaz | Şart önerilmez; üretimdeki T6 / T10 ile çelişki (bölüm 5 madde 2) Cemal kararıyla kapanır |
| D8 | İyi bilanço sonrası göstermelik yükseliş ve yavaş dağıtım | `dagitim = bilanço günü +%10 ve sonraki 20 günde kapanış < bilanço günü kapanışı` (ölçüm satırı, şart değil) |
| D10 | Düşük float / yeni listeleme = çıkış likiditesi | `uzak = halka arzdan < 250 gün ve fiili dolaşım < %15` bayrağı (boyut düşürür) |
| G1 | Kaybedilebilir tutar tavanı | `boyut <= Cemal'in yazdığı kayıp tutarı` (öneri modülünde zorunlu alan; boşsa öneri basılmaz) |
| G2 | Zarardaki isme olaysız ekleme yok | `ekleme yalnız (kâr > 0) ya da (olay sütunu dolu)`; takip'te ekleme satırı bu şartsız reddedilir |
| G3 | 2x'te anaparayı çek | `kapanış >= 2 x maliyet -> adet x 0,5 sat` (takip / öneri çıkış sütunu) |
| G4 | Aynı sektörde ikinci isim | `sektör payı > %50 ise uyarı` (öneri modülü portföy denetimi) |
| G5 | Tavanda kovalama yok | `alım yasak: gün getirisi >= tavan sınırı x 0,95 ya da önceki 2 gün tavan` |
| G9 | 2x sonrası risk azaltma | `2x gerçekleştiyse sonraki isim boyutu <= ilk ismin kalan kârı` |
| H5 | Üretim 11 hatası düzeltilsin | Kod düzeltmesi (takip çıkış günü, bölünme ölçeği, AL ekranı ...; IK_ACIK ÜRETİM) |
| H12, H13, H18, H22 | Süreç kuralları | Kod şartı değil; iş tanımı şablonu |
| H15 | Basit ölçü öncelikli | Ön kayıtta `basit_kıyas = aynı hücrede tek değişkenli sürüm` satırı zorunlu |
| H17 | Sabit ufuk başarı ölçüsü değil | ORTAK_CETVEL'e `r_cikis = al mumundan S6 KIRILDI / tavan + %20 / 250 gün, hangisi önce` ikinci ana ölçü (ön kayıtla) |
| J4 | BIST dev mum (~%10) çöl içinde sayılmaz | `dev = günlük getiri >= +%9,5 ya da <= -%9,5 (BIST) veya H-L >= 3 x ATR250 -> S6 bölgesi o barda kapanır, dev mum kutuya alınmaz` |
| J6 | Azıcık çıkıp dönmek olur, uzağa çıkmak olmaz | `tasma = bant dışı kapanış <= 2 bar ve tavan / dip x (1 ± 0,02..0,03) içinde -> bölge sürer; aksi bölge biter` (eşik ön kayıtta, Cemal etiketiyle) |
| J7 | Doji en kritik özellik | S6'ya `doji_say = bölgedeki geçerli barlarda \|C-O\| / (H-L) < 0,15 sayısı` bilgi sütunu; sonra ORTAK CETVEL'de ön kayıtla 'doji ≥ 3' satırı |
| J13 | Kutu 1 SMA200 civarı | `sma200_yakin = bölge medyan kapanışı SMA200 x (0,9..1,1) içinde` bilgi sütunu |
| J14 | Şekil tek başına yetmez | Şart değil (bulgu) |
| J19 | 'Yatırım tavsiyesi değildir' yazılmaz | Kod şartı değil; CLAUDE.md dürüstlük kuralıyla çelişki Cemal kararıyla kapanır |
| I1 | 10x hedefi | `p10x = 3 yıl içinde 10x olasılığı / taban (~%1)` olasılık tablosu satırı |

## 5. HATA (kaynaklar arası çelişkiler)

1. Sabit ufuk çelişkisi: CLAUDE.md 'çöl ardından gelen yükselişle değerlendirilir, sabit ufuktaki kapanış başarı ölçüsü değildir' derken FI_OLCUT ve ORTAK_CETVEL ana ölçüsü r60 (60. gün kapanışı); Cemal 28 Eki ('60 günlük hedef olamaz') ve 13 Kas ('60 gün değil') aynı itirazı yaptı. Kural metni ile kod ölçüsü uyuşmuyor (H17).
2. Çıkış çelişkisi: COL_OZET §1 'STOP YOK' ve §3 'taban kırılınca çık kötü', ders 3 'BIST'te stop çalışmaz'; üretimde T6 (taban kırılınca çık) ve T10 (stop maliyete) çalışıyor. H23 'açık (tut ya da kaldır)' 17 Eki'den beri kapanmadı.
3. İZ tanımı: IZ_DEFTERI.md 0. İNDEKS başlığı hâlâ 'İZ = BIST 2023, BIST 2024-26, ABD 2023, ABD 2024-26 dört hücrede kat ≥ 1,3' diyor; CLAUDE.md'ye göre 26 Eki'den beri FI_OLCUT, 28 Eki'den beri karar hücreleri ABD + AVRUPA.
4. Etiket çelişkisi: karne.csv ve indeks Ç38, Ç39, Ç50, Ç57, Ç67, Ç69, Ç70, Ç73-Ç75, Ç78-Ç83, Ç87, Ç89, Ç90 için 'İZ DEĞİL' yazıyor; IK_ACIK (Ç175, 14 Kas) aynı kayıtları ÖLÇÜLEMEDİ sayıyor ('eski metinler tarih kaydı'). İki etiket yan yana basılı.
5. Hata numarası iki sistemde: IZ_DEFTERI hata tablosu H1-H221 (sıra no), IK_HATA 'kayit' alanı eski H001-H144 numaralarını taşıyor (ör. tablo H1 = eski H009). IK_KONTROL 'geçmişte kaç kez' sütunu eski numaraları kullanıyor (K3 'H004, H037' = tablodaki H10, H44); görev günlüğü 15 Kas ve IK_ACIK yeni numarayı kullanıyor ('H178'). Aynı 'H' kodu iki sistemde farklı satırı gösterir (ör. tablo H26 = eski H025, tablo H33 = eski H029).
6. Küçük mum eşiği modüller arasında farklı: COL_v1 D7 'H−L ≤ 0,65 x ATR30', SIKISMA_OBEK S5 k_m 0,75 x ATR250, S6 kM 0,90; Cemal'in ENJSA bölgesi 0,82 x ATR. Aynı 'küçük mum' sözü üç sayıyla kodda.
7. Bölge uzunluğu: görev 15 Kas 'en çok ~60 mum', CEMAL_COL_KURALLARI 'çoğu 40-70', S6_PRM nMax 70.
8. Bant: CEMAL_COL_KURALLARI K2 'uzun tabanda %20'ye kadar (DESA %20)'; S6 seçilen bantMax 0,12 DESA'nın bandını dışarıda bırakır.
9. KNFRT etiketi: CEMAL_COL_KURALLARI K1 ve etiket tablosu KNFRT 'Haz/Tem-Ağu tabanı'nı kanıt olarak gösteriyor; H208 bu aralığın ana modelin fotoğraftan tahmini olduğunu ve veride fiyatın ~%80 yükseldiğini (etiket yanlış) yazıyor; S6 v1.1 KNFRT'yi puan dışı bıraktı.
10. Kör set kararı: commit 64dc638 'ALGILAMA KIRIK'; commit 885c40b ve görev günlüğü 'önceden yazılı kurala göre KISMİ'. Son geçerli etiket KISMİ.
11. QMLS zarar rakamı dört farklı: görev 7 Kas -656 $ / -658 $, ONERI açık pozisyon '≈ -640 $', ONERI kapanan '≈ -650 $'.
12. QMLS durumu: görev 7 Kas Cemal 'QMLS'ten çıktım'; ONERI_DEFTERI ve görev 9 / 12 Kas kalan 83 adedi açık pozisyon sayıyor.
13. Defter başlığı: IZ_DEFTERI.md 1. satır 'güncelleme: 30 Ekim 2026, 18:05'; içerik 17 Kas'a kadar.
14. Kapalı konu çelişkisi: CLAUDE.md 'kapanmış konuları yeniden açma (sektör ısısı, KNN ...)'; Ç95 (KNN, 'Cemal'in isteğiyle'), Ç108-Ç111, Ç117 (sektör ısısı, 'Cemal istedi') yeniden açıldı. Kayıtta gerekçe var; kural metninde istisna yok.
15. Sektör rüzgârı kuralı ile sonuç: CLAUDE.md 'rüzgâr ya da katalizör olmadan çöl aranmaz' üretim kuralı gibi duruyor; Ç117 'rüzgâr = üyelerin momentumu, üstüne katkı yok', Ç181c yalnız ABD EMARE. Kural ölçülmüş bir şart değil.
16. FITIL_V2 tasarım sapması: iş tanımı (4) 'C_t < max(High, W)' (t dahil); ON_KAYIT SAPMA-1 ve FV_SART s4 't HARİÇ önceki 9 bar'. Kayıtlı sapma; iş tanımı metni güncellenmemiş.
17. Devir notu (J10) 'eğim / kanama gürültü' diyor; Cemal'in 15 Kas etiketleri ve CEMAL_COL_KURALLARI K3 'eğimli pencere çöl değil (net ≤ %5)' diyor; S6 netMax 0,03 ikincisini uyguluyor. Eski oturumun tarihi yazılı olmadığı için hangisinin sonra geldiği belirsiz.
18. Devir notu (J19) "'yatırım tavsiyesi değildir' cümlesi yok" diyor; CLAUDE.md 11 Kas dürüstlük kuralı 'Claude yatırım danışmanı değildir' ifadesini her öneride ister.
19. Devir notu (J14) '732 kırılımda %36 yukarı / %32 aşağı' sayısını veriyor; bu sayı IZ_DEFTERI, COL_OZET ve IZ_KARNE'de yok (kaynak yok). En yakın repo sayısı COL_OZET §3 'zıpla-düş oranı ~%27'.
20. Devir notu (J8) 'çöl bir yıla kadar uzar'; S6_PRM nMax 70 bar (~3,5 ay) ve 15 Kas görev satırı 'çoğu ~60 mum'.
21. Devir notu (J7) 'en kritik özellik doji'; repoda doji kutusu (Ç38-Ç39) ve col_ogren doji çekirdeği ayırmadı, üretim col_dip2 ve S6 doji kullanmıyor (yalnız boyut çarpanı). Kural ile kod ağırlığı ters.
22. Devir notu (J2) 'sabit % eşik yanlış'; üretim AL_PAY 1,002, S6 bantMax 0,12 / netMax 0,03 ve BIST tavan %9,5 sabit yüzdedir.
