# YAPI_HEDEF 7. TUR — PUAN: bütün bölgeleri puanlayıp seçme, sızıntısız öğrenme (Y12) — İŞ TANIMI
Yazan: ana model, 19 Kas 2026. Cemal: "kod bütün bölgelerde puanlama yaparak seçerse sonuç ne olur; koda önceden görme sızıntısı kontrolü verilip bölge parmak izi çıkarırsa ve bu parmak izini rastgele seçmeden 'şartlar uyuyor' deyip öğrense olur mu". Hedef: her seçilen bölge yukarı çıksın (ulaşılamaz; ölçülen tavan yazılır).
Yasaklar: önceki iş tanımlarıyla aynı (defterler, tur/*, üretim zinciri, GOZ_ETIKET.py; `git add -A` yok; push yok; çakışma kapıları; e-posta / anahtar yok). Kontrol tablosu ön kayıtta; ik_kontrol_kapisi; 'HATA' / 'KONTROL LİSTESİ' zorunlu. Önceki 6. tur kodu (grup / karne / mahkeme) ile çakışmamak için 6. tur commit'lerinden SONRA başlar.

## 1. VERİ ve ÖZELLİKLER (yalnız t'ye kadar)
- Satırlar: olay_Y1.csv.gz (26.663 Y1 olayı; ölçülebilir olanlar, olc). Hedef y = h5 (15 geçerli barda kapanış +%5 stop'tan önce; aynı cetvel). Eş payı es_h5 satırda.
- Özellikler X: F1-F18 (ozellik_Y1), F19 parmak (parmak_Y1_p11), F20-F23 (s7), F24-F29 (s9); pazar ve dönem ÖZELLİK DEĞİL (sızıntı / kayma); momentum x likidite kovası (eş kovası) özellik olarak ALINMAZ (eş payı zaten bunu kontrol ediyor); NaN -> medyan (eğitim kümesinden), ayrıca 'NaN bayrağı' sütunları.
- Hedefin alternatif biçimi (ikincil): y2 = h5 - es_h5 > 0 (eşini geçti mi).

## 2. SIZINTISIZ ÖĞRENME (yh_puan)
- İki yön: (A) eğitim 2016-22 -> sınama 2023 + 2024-26; (B) eğitim 2023-26 -> sınama 2016-22. Ayrıca (C) yürüyen: her takvim yılı için yalnız önceki yıllarla eğit, o yılı sına (2019'dan itibaren; ilk eğitim 2016-18).
- Modeller (ikisi de): M1 lojistik regresyon (standartlaştırılmış, L2, C = 1,0); M2 gradyan artırmalı ağaç (sklearn HistGradientBoosting; max_depth 3, learning_rate 0,05, max_iter 300, early stopping eğitim içi %20 doğrulama). Hiperparametre arama YOK (önceden sabit).
- Pazarlar: birleşik model (ABD + AVR + BIST) VE pazar başına model; ikisi de raporlanır.
- PLASEBO: aynı model, y karıştırılmış (tohum 107, 20 tekrar): üst dilim P(+5) dağılımı; gerçek modelin üst dilim payı plasebo %95'inin üstünde mi.
- SIZINTI KAPISI: sınama kümesindeki hiçbir satırın tarihi eğitim kümesinin son tarihinden <= 60 gün sonra değil (tampon 60 gün: hedef penceresi + giriş); ayrıca hisse düzeyinde tampon gerekmez (eş günlük).

## 3. ÖLÇÜ (sınama kümesinde; önceden sabit)
- Puan dilimleri: üst %10, üst %20, alt %20, tümü. Her dilimde: n, P(+5) olay, P eş (es_h5 ortalaması), KAT5 = olay / eş (ay kümeli bootstrap %95), stop payı, konum eşli KAT (F15 çeyreği); hücreler pazar x sınama dönemi.
- AUC (bilgi), kalibrasyon (10 kutu: tahmin vs gerçek).
- TUTAR (hücre): üst %20 diliminde n >= 30 VE KAT5 alt ucu > 1 VE plasebo %95 üstünde VE stop payı eşten büyük değil; etiket kuralı önceki turlar gibi (İZ / EMARE / ÖLÇÜLEMEDİ / DESTEKLENMEDİ; karar hücreleri ABD / AVR 2023 ve 2024-26 'bakılmış' notuyla; 2016-22 yönü (B) bağımsız sınama).
- 'HER SEÇİLEN YUKARI ÇIKSIN' tavanı: üst %5 diliminde P(+5) (en iyi durumda ulaşılan oran) açıkça yazılır.
- Özellik önemi (M2 permütasyon önemi, sınama kümesinde; bilgi): hangi özellikler puanı taşıyor; Cemal'in kurallarıyla (Ş1-Ş9) örtüşme.

## 4. 'ŞARTLAR UYUYOR' SEÇİCİSİ
- Üst %20 puan eşiği (eğitim kümesinden sabitlenir) -> Y12 seçicisi: sınama döneminde seçilen olaylar, aynı cetvel, huni tablosuna 'Y12 PUAN' satırı (İLERLEME tablosuna ekle). TUR 6 havuzu adayı (karar Cemal'in).
- Mahkeme (6. tur) ile bağ: seçilen üst dilim olaylarında mahkeme kural puanı ortalaması vs alt dilim (bilgi).

## 5. ÖN KAYIT / ÇIKTI / COMMIT
- ON_KAYIT_7.md (kontrol tablosu, model ve eşikler, dönem tamponu, tohumlar, getirisiz sayımlar; koşudan ÖNCE commit) -> koşu -> RAPOR_7.md (dilim tabloları (A), (B), (C); plasebo; AUC / kalibrasyon; özellik önemi; Y12 huni satırı; YENİDEN ÜRETİM iki hücre; HATA; KONTROL LİSTESİ) + puan_Y1.csv.gz (sembol, tarih, puan A / B / C, dilim) + olay_Y12.csv.gz + sonuc.json.
- Testler: test_yapi_hedef.py (sızıntı kapısı: tamponu ihlal eden bölünme DURUR; plasebo mekaniği; dilim hesabı; yapay veri ile 'öğrenilebilir sinyal' ve 'gürültü' vakaları).
- İki commit, mesaj sonu:
  Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01F7vgWZPNpBhrsGQEHDtRis
RAPOR: dilim tablosu özeti (üst %20 / %10 / %5 P(+5) vs eş, iki yön + yürüyen), plasebo, en önemli 8 özellik, Y12 n ve pay, kapılar, commit'ler, HATA, KONTROL LİSTESİ, Colab notu. Yorum yok; 'tutmadı' çıkarsa sayılarla bırak.
