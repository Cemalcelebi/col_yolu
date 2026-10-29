# K52 — ÖN KAYIT: Grafik izi + analist revizyonları (29 Ekim 2026, sonuç görülmeden)

K51 kararı (**İZ DEĞİL**) ve K51 grafik kuralları (P1 / P2 tanımları, eşikler, üçlü bariyer +%20 / −%10 / 60 gün, maliyet, delist kuralı, taban) **değişmez**. AL sinyali, strateji ya da eşik optimizasyonu yok. 2023-26 bağımsız test değildir (K51'de görüldü); üç dönemde tutma şartı sağlamlık kontrolüdür; olumlu sonuç KEŞİFSEL etiketlenir.

## 1. Veri kaynağı denetimi (koşudan önce yapıldı; yalnız kapsam, sonuç değil)

- **Kaynak:** Yahoo Finance analist not değişiklikleri günlüğü (yfinance `upgrades_downgrades`). Ücretsiz. Çekim 29 Ekim 2026.
- **Var olan alanlar:** zaman damgası (tarih + saat; saat dilimi belgelenmemiş), kurum (Firm), eski ve yeni tavsiye (FromGrade, ToGrade), eylem (up / down / main / init / reit), hedef fiyat eylemi (Raises / Lowers / Maintains / Announces), eski ve yeni hedef fiyat.
- **Olmayan alanlar:** EPS / kâr tahmini revizyonu (B), rapor gerekçesi ve riskler (H), analist kişi kimliği (yalnız kurum), rapor kimliği, tarihsel sürüm bilgisi. Bunlar olmadan ilgili hipotezler ÖLÇÜLEMEZ diye yazılır; yerine başka alan konmaz.
- **Tarihsel sürüm:** Yahoo günlüğü olay kaydı biçimindedir (her değişiklik ayrı satır); geriye dönük yeniden yazılıp yazılmadığı doğrulanamaz. Bu belirsizlik raporda kalır; "geçmiş test" ifadesi bu çekinceyle kullanılır.
- **Hayatta kalma:** yalnız bugün Yahoo'da bulunan semboller veri taşır; borsadan çıkmış şirketlerin çoğunda veri YOK → bunlar "veri yok" alt grubudur (G2b / G4b), olumsuz görüşle karıştırılmaz.
- **Zaman damgası güvenilirliği:** saat 00:00:00 olan kayıt payı, yıl yıl kapsama (kayıt / hisse), kaynak grubuna göre (V_ABD, K34 Yahoo, K34 Tiingo) kapsama oranı ve eksik alan oranı raporlanır (K51_ANALIST_VERI_KAPSAMI.csv).
- **Sızıntı kuralı (sabit):** olay günü d için yalnız zaman damgası tarihi ≤ d−1 olan kayıtlar "biliniyor" sayılır (saat dilimi belirsiz olduğundan aynı gün kayıtları kullanılmaz). Giriş d+1 açılışı (K51 ile aynı). Hedef fiyatlar kayıt anındaki değerlerdir; sonraki güncellemeler kullanılmaz. Aynı kurum, aynı tarih tek kayıt sayılır (kopya ayıklama).

## 2. Değişkenler (ayrı tutulur; birleşik puan yok)

Pencere W = olay gününden önceki 20 işlem günü (tarih ≤ d−1).
- A tavsiye değişimi: n_yukari (Action = up), n_asagi (down), n_baslangic_al (init ve ToGrade alım kümesinde: Buy, Strong Buy, Outperform, Overweight, Positive, Accumulate, Market Outperform, Sector Outperform, Top Pick, Conviction Buy).
- B EPS revizyonu: YOK (ölçülemez).
- C hedef fiyat revizyonu: n_hedef_yukari (Raises), n_hedef_asagi (Lowers), ortalama yüzde değişim (current / prior − 1, prior > 0).
- D genişlik: W'de aynı yönde revizyon yapan FARKLI kurum sayısı ve W'deki toplam kurum sayısına oranı.
- E bağımsızlık: kurum adı normalize edilir (büyük harf, "& Co", "Securities" gibi ekler atılır); aynı kurumun aynı günkü kayıtları tek sayılır. Kişi kimliği olmadığından daha ince bağımsızlık ölçülemez; yazılır.
- F tazelik: en son olumlu revizyon ile d arasındaki işlem günü.
- G kurum geçmiş doğruluğu: kurumun d−61'den önceki "up" kayıtlarının üçlü bariyer isabeti (yalnız sonucu d'den önce bilinen kayıtlar); en az 10 kayıt, yoksa boş.
- H gerekçe: YOK (ölçülemez).
- Kapsama: d'den önceki 365 günde hisseye ait kayıt sayısı (popülerlik vekili).

**Olumlu revizyon** = up VEYA Raises VEYA baslangic_al. **Olumsuz** = down VEYA Lowers. **TEYİT** = W'de olumlu ≥ 1 ve olumlu > olumsuz.

## 3. Dört grup

- G1: P1 (K51 grafik izi, oluşurken) ∧ TEYİT.
- G2a: P1 ∧ sembolün d'den önce en az bir analist kaydı var ∧ TEYİT yok.
- G2b: P1 ∧ sembolün d'den önce hiç kaydı yok (veri yok / doğrulanamıyor).
- G3: P1 değil (likit panel günü, ÇEK dışı) ∧ TEYİT. G4a / G4b aynı biçimde.
- Aynı analiz P2 (kırılım) için ayrı koşulur. Olumsuz teyit (olumsuz > olumlu) bilgi olarak ayrı yazılır.
- Dengesizlik denetimi: gruplar arasında sektör, rejim, likidite üçte biri, oynaklık ondalığı, dd250, r60, kapsama dağılımları tablolanır; birincil ölçüt zaten K51 tabanıyla (aynı gün aynı oynaklık ondalığı ortalaması) ayarlıdır; ek olarak v1.2 eşleştirmesi (aynı gün, vd, lt, dd250, trend, sektör + kapsama üçte biri) ile G1 − eşleşmiş G2a farkı da verilir (H5).

## 4. Birincil ölçüt ve karar koşulları (sabit)

- **Birincil ölçüt:** taban-ayarlı isabet farkı Δ = ortalama(y − e_y | G1) − ortalama(y − e_y | G2a); y = +%20 önce (K51 etiketi), e_y = K51 tabanı. İkincil: ham isabet farkı, net (maliyet sonrası) getiri farkı.
- **Koşullar (her dönemde, ayrı ayrı):** n_G1 ≥ 30 ve n_G2a ≥ 30; Δ ≥ +0,05; ay kümeli bootstrap %95 alt uç > 0; net fark > 0. Hisse × çeyrek kümeli aralık da yazılır.
- **Dönemler:** 2016-22, 2023, 2024-26. Üçünde de tutarsa "DESTEKLENİYOR (KEŞİFSEL)"; birinde n < 30 ise "YETERSİZ ÖRNEKLEM"; aksi "DESTEKLENMİYOR". Δ ≤ −0,05 ve üst uç < 0 ise "TERS YÖN" (bilgi).
- **Çoklu test:** ölçülebilen hipotezler (birincil, H2, H3, H5, H6 hücreleri) bir aile; 2023-26 birleşik tek yönlü bootstrap p'leri Holm ile düzeltilir; ayrıca Holm p < 0,05 aranır.
- **En iyi 20 hisse çıkarma**, yıl yıl (2023 / 2024 / 2025 / 2026 kısmi), rejim (AYI / BOĞA, SPY 200 gün), veri var / yok alt örneklemleri raporlanır.

## 5. Hipotezler

| Kod | Hipotez | Destekleyici gözlem | Karşı kanıt / alternatif | Reddetme koşulu | Ölçüt |
|---|---|---|---|---|---|
| H0 (birincil) | Yeni olumlu revizyon P1'e ek bilgi katar | Δ(G1 − G2a) ≥ +5, CI > 0, net > 0 üç dönemde | fark hayatta kalanlara / kapsamaya bağlı (H5) | koşullardan biri sağlanmazsa | Δ, dönem başına |
| H1 | Yukarı EPS revizyonu ek bilgi katar | — | — | — | **ÖLÇÜLEMEZ** (EPS alanı yok); karar verilmez |
| H2 | Tavsiye değişimi, hedef fiyat yükseltmesinden daha çok bilgi taşır | Δ(yalnız up teyidi) − Δ(yalnız Raises teyidi) ≥ +5, CI > 0 | hedef yükseltmesi zaten fiyat hareketini izler | fark < +5 ya da CI 0'ı içerir | iki alt teyit türü, 2016-22 ve 2023-26 |
| H3 | Bağımsız kurumların aynı yönde yeni revizyonu, tek kurumdan daha çok bilgi taşır | Δ(≥ 2 farklı kurum) − Δ(1 kurum) ≥ +5, CI > 0 | kopya / sürü davranışı | fark < +5 ya da CI 0'ı içerir | aynı |
| H4 | Revizyonlar çoğunlukla fiyat hareketinden SONRA gelir, ek katkı yok | W'deki olumlu revizyonların, W içindeki en düşük kapanıştan ≥ %10 yükseliş SONRASI gelen payı ≥ %50 VE H0 desteklenmiyor | revizyonlar önce geliyor ve H0 destekleniyor | pay < %50 ve H0 destekleniyor | zamanlama payı + Δ(önce gelen) vs Δ(sonra gelen) |
| H5 | Görünen katkı büyüklük, sektör, momentum, kapsama / popülerlikten gelir | eşleşmiş (kapsama dahil) G1 − G2a farkı < +5 iken ham Δ ≥ +5 | eşleşince de ≥ +5 | eşleşmiş Δ ≥ +5 ve CI > 0 | v1.2 eşleştirme + kapsama üçte biri |
| H6 | Katkı yalnız belirli rejim / iz türünde | rejim (AYI, BOĞA) × iz (P1, P2) hücrelerinde H0 koşulları; n < 30 "yetersiz"; birleştirme yok | tutarsız yön | hiçbir hücre tutmaz | hücre başına Δ |

Bilgi (karar değil): kurum geçmiş doğruluğu (G) üst / alt yarı teyitleri; olumsuz teyit (ters yön).

## 6. Çıktılar

K51_ANALIST_VERI_KAPSAMI.csv, K51_ANALIST_REVIZYONLARI.csv (olay × pencere özellikleri; ham günlük repoda değil), K51_GRAFIK_ANALIST_4GRUP.csv, K51_ANALIST_EK_KATKI_TESTI.csv, K51_ANALIST_TARIHSEL_VERI_DENETIMI.md, K51_GRAFIK_ANALIST_ARASTIRMA.md. Kod: COL_YOLU_ABD.py v1.3 (`cy_v13_calistir`), test_col_yolu_abd.py ekleri.

## 7. Karar kuralı

Bu araştırma K51 kararını değiştirmez. Tarihsel analist verisi güvenilir değilse geçmiş test yapılmış gibi davranılmaz. H0 olumlu çıksa bile bulgu keşifseldir; bağımsız doğrulama (sinyal ≥ 01.09.2026, en erken Mart 2027) tasarlanır; AL sinyaline dönüştürülmez.
