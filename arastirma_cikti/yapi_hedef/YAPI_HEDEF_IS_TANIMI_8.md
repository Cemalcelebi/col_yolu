# YAPI_HEDEF 8. TUR — Ş10 MACD POZİTİF UYUMSUZLUK (Y13 / Y13b / Y13c) — İŞ TANIMI
Yazan: ana model, 20 Kas 2026. Cemal: "iki tarih arasındaki fiyat ve MACD uyumsuzluğuna bak; fiyatın döneceğini öngörüyor; bunu da kullan" (K47 / K48, SINANMADI). Cemal'in önerisi tek hipotez, veri madenciliği değil; yine de aynı veri üzerinde yeni bir karşılaştırma olduğu notu rapora yazılır.
Yasaklar: 4.-7. tur iş tanımlarıyla aynı (defterler, tur/*, üretim zinciri, GOZ_ETIKET.py; `git add -A` yok; push yok; çakışma kapıları; e-posta / anahtar yok). Kontrol tablosu ön kayıtta (K1-K14 + kanıt), ik_kontrol_kapisi koşudan önce; 'HATA' / 'KONTROL LİSTESİ' zorunlu. Yalnız t'ye kadar bilgi.

## 1. Ş10 TANIMI (sabit; sonuç görülünce değişmez)
- MACD(12, 26, 9) kapanış üzerinden: MACD çizgisi = EMA12 − EMA26; sinyal = EMA9(MACD); histogram = MACD − sinyal. EMA'lar [t-250, t] geçerli barlarla (ge_hazir: H > L, V > 0, kriz kesiği), ilk 35 bar ısınma.
- Salınım dipleri: [t-60, t-1] içinde Low'un 5 bar sağ / 5 bar sol yerel minimumu (eşitlikte ilk bar). L2 = t'ye en yakın dip (t-1'e kadar; sağ 5 bar da t'den önce olmalı: yani L2 <= t-6), L1 = L2'den en az 8 bar önceki bir önceki dip (yoksa Ş10 NaN = tutmaz).
- F65 FİYAT ŞARTI: Low(L2) <= Low(L1) x 1,01 (ikinci dip birinciye eşit ya da daha aşağı).
- F66 MACD ŞARTI: MACD(L2) > MACD(L1) VE MACD(L2) < 0 (sıfırın altında, dipte); F66 değeri = (MACD(L2) − MACD(L1)) / Close(L2) (normalize).
- F67 = L2 − L1 (bar); F68 = t barında MACD > sinyal (dönüş teyidi; 0 / 1).
- Ş10 TUTAR ⇔ F65 VE F66 > 0. Ş10t (bilgi) = Ş10 VE F68 = 1.
- Histogram sürümü (bilgi): F66h = hist(L2) − hist(L1) > 0.

## 2. DENEMELER (yön +, giriş t+1 açılış, hat / stop0 Y1 ile aynı)
- Y13 = Y1 olayı ∧ Ş10 (kol A); Y13b = Y9 (dipte) ∧ Ş10 (kol B); Y13c = Y13 ∧ F68 (bilgi). Karşılaştırma: Y1 ∧ NOT Ş10 (uyumsuzluk yok) aynı hücrelerde (bilgi).
- Huni getirisiz ön kayıtta (Y1 -> L1/L2 var -> F65 -> F66 -> Ş10 -> + F68), pazar x dönem.

## 3. ÖLÇÜM: aynı 15 bar cetveli (h5 / es_h5 / st5, KAT5 ay kümeli %95, konum eşli KAT, plasebo); KARNE v3 (60 bar ambargo iki yönde, ABD / AVR ayrı n >= 30, ay kümeli bootstrap alt ucu > 0, leave-3-out, stop payı eşten büyük değil, K1 tabakası F10 / F15 / F7 / F55 ATRP / F13 tercilleri, ters yön bilgi); sınama dönemleri 2023 ve 2024-26 AYRI hücre; karar hücreleri ABD / AVR 2023 ve 2024-26 (bakılmış değil: bu özellik ilk kez ölçülüyor; ama aynı olaylar üzerinde 7 tur ölçüm yapıldığı notu), dış sınama 2016-22, BIST bilgi; etiket kuralı yh_etiket (İZ / EMARE / ÖLÇÜLEMEDİ / DESTEKLENMEDİ + TERS); BH aile 'bh_tur8' (Y13 / Y13b x 4 hücre, n >= 30). Regresyon: Y1-Y12 eşik sha'ları aynen; Y13* satırları olay_Y1 ile 9 sütunda eşit. Ön kayıt kapısı GE_FN_SHA ve V_*.pkl sha'larını da mühürler (Devir 3 dersi).
## 4. CEMAL UYUMU (bilgi; h5 okunmaz): Ş10'un Cemal'in etiketlediği sayfalarda (hakem KÖR 19, TUR 1, 2, 4, 6) tutma payı x OLUR / OLMAZ; TUR 6'da Cemal'in 'sert düşüş' dediği 5, 9, 30 ve 'iyi' dediği sayfalarda Ş10 var mı (bilgi).
## 5. ÇIKTILAR: YAPI_HEDEF.py (yh_macd, yh_s10_ozellik -> ozellik_Y1_s10.csv.gz + denetim json (prefix: veri t'de kesilince aynı), Y13*), test_yapi_hedef.py (yapay vakalar: uyumsuzluk var / yok / MACD sıfırın üstünde / L1 yok; prefix; EMA ısınma), ON_KAYIT_8.md (koşudan ÖNCE commit), RAPOR_8.md (4.-7. tur biçimi + 'MACD uyumsuzluğu olan vs olmayan' tablo + Cemal uyumu + YENİDEN ÜRETİM iki hücre), olay_Y13*.csv.gz, sonuc.json. İki commit, mesaj sonu:
  Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01F7vgWZPNpBhrsGQEHDtRis
RAPOR: huni, SONUÇ tablosu (karar hücreleri n / KAT5 / konum eşli / plasebo / stop), dış sınama, BIST, Ş10 var vs yok farkı, Cemal uyumu, kapılar, commit'ler, HATA, KONTROL LİSTESİ, Colab notu. Yorum yok.
