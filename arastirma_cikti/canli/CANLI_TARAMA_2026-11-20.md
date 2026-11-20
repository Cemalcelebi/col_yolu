# CANLI TARAMA — 2026-11-20

**DÜRÜSTLÜK: bu liste 'izleme / ileri test' listesidir, ÖNERİ DEĞİLDİR. CLAUDE.md öneri modülünün üç kapısından (tarama + dosya + risk) burada yalnız tarama kapısı var ve seçici ÖLÇÜLEMEDİ düzeyindedir (dipte + gövdeli kırılım KATKI+ ama hücre başına +3..+9 puan). Alım-satım kararı Cemal'indir; Claude yatırım danışmanı değildir.**

Taban oran hatırlatması: 3 yılda 10x ABD mikro-cap ~%1, BIST USD ~%1,85. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı: sonuçlar yukarı yanlı okunur).

- Üretim (UTC): 2026-11-20T06:29:04Z · CANLI_TARAMA v1.0 (2026-11-20): S6 son 5 gün + havuz Ş1 VE Ş7 (kademeli) + puan7 sırası; ileri test olc (YAPI_HEDEF cetveli)
- Kurallar CT_ESIK_SHA `bb85545e07832f3c…` (ön kayıt arastirma_cikti/canli/CANLI_ON_KAYIT.md; kapı geçti)

## 1. Veri

| Pazar | hisse | son tarih | son 5 işlem günü | kaynak |
|---|---|---|---|---|
| ABD | 1411 | 2026-11-19 | 2026-11-13 .. 2026-11-19 | /tmp/veri_canli |
| AVR | 580 | 2026-11-19 | 2026-11-13 .. 2026-11-19 | /tmp/veri_canli |
| BIST | 581 | 2026-11-19 | 2026-11-13 .. 2026-11-19 | /tmp/veri_canli |

İndirme özeti (yfinance, auto_adjust):

| Pazar | istenen | başarılı | başarısız | yeni bar | ortak günde fark > %1 olan sembol | kipi ölçeklenen | şüpheli | son tarih (en çok / en sık) |
|---|---|---|---|---|---|---|---|---|
| ABD | 1411 | 1411 | 0 | 28039 | 422 | 57 | 10 | 2026-11-19 / 2026-11-19 |
| AVR | 581 | 580 | 1 | 9852 | 13 | 8 | 4 | 2026-11-19 / 2026-11-18 |
| BIST | 581 | 581 | 0 | 10460 | 426 | 93 | 19 | 2026-11-19 / 2026-11-18 |
- AVR başarısız (1; eski seri kaldı, son 5 günde sinyal veremez): MT.PA

## 2. Sinyal ve havuz

| Pazar | son 5 günde S6 AL | havuz dışı (t) | likidite alt %20 | bölünme şüphesi | 60 gün tekil düşen | şüpheli dışlanan | sinyal | özellik hatası |
|---|---|---|---|---|---|---|---|---|
| ABD | 7 | 1 | 1 | 0 | 4 | 0 | 2 | 0 |
| AVR | 9 | 1 | 1 | 0 | 1 | 0 | 7 | 0 |
| BIST | 3 | 0 | 0 | 0 | 0 | 0 | 3 | 0 |

| Havuz kademesi | toplam | ABD | AVR | BIST |
|---|---|---|---|---|
| Ş1 VE Ş7 (asıl) | 0 | 0 | 0 | 0 |
| (i) Ş1 VE F22 > 0 | 0 | 0 | 0 | 0 |
| (ii) Ş1 | 1 | 0 | 0 | 1 |

**Kullanılan kademe: (ii) Ş1**

## 3. En iyi 10 (puan7 sırası; pazar başına en çok 5)

| # | pazar | sembol | sinyal | kapanış | hat | F21 | stop0 (uzaklık) | +%5 / +%10 | puan7 | Ş9 | Ş10 | parmak | F15 | F17 | F18 | 12 kural | mahkeme | likidite 20g |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIST | VAKFN | 2026-11-17 | 0,88 | 0,81 | 0,94 | 0,79 (%-9,8) | 0,92 / 0,97 | 0,542 | - | ✓ | ✓ | 0,12 | %-30 | %+8,6 | 7/12 | ÖNCEKİ BÖLGE DAHA UYGUN | 71,2 M TL |

Okuma: stop0 = hat x 0,98; hedefler kapanışa göre (gerçek giriş ertesi açılış). puan7 = 7. tur M2 modelinin P(15 barda +%5 stop'tan önce) tahmini (eğitim 2016 - 31.08.2026 Y1 olayları; modelin taban P'si 0,377). Ş9 = U dip çanağı; Ş10 = MACD pozitif uyumsuzluk; parmak = F19 P1.1 (4 mum dip öbeği). Mahkeme bilgi satırıdır (eleme değil).

## 4. Şüpheli veri (listeden dışlandı)

- ABD AEHL: yeni barda günlük getiri %178
- ABD ARI: ortak günlerde yeni/eski oranı 0.364 (bölünme / birim)
- ABD GDYN: yeni barda günlük getiri %41
- ABD SGRY: yeni barda günlük getiri %48
- ABD SLS: yeni barda günlük getiri %156
- ABD SOC: yeni barda günlük getiri %54
- ABD STLN: yeni barda günlük getiri %46
- ABD VCYT: yeni barda günlük getiri %54
- ABD XRX: yeni barda günlük getiri %40
- ABD ZURA: yeni barda günlük getiri %70
- AVR BCG.L: ortak günlerde yeni/eski oranı 0.010 (bölünme / birim)
- AVR CLDN.L: ortak günlerde yeni/eski oranı 100.000 (bölünme / birim)
- AVR MEGP.L: ortak günlerde oran tek tip değil (0.010 .. 1.000; ayarlama / birim karışık)
- AVR ROSE.L: ortak günlerde oran tek tip değil (0.010 .. 1.000; ayarlama / birim karışık)
- BIST BRMEN: ortak günlerde oran tek tip değil (1.000 .. 1.888; ayarlama / birim karışık)
- BIST CVKMD: ortak günlerde yeni/eski oranı 2.623 (bölünme / birim)
- BIST DITAS: ortak günlerde oran tek tip değil (0.983 .. 1.790; ayarlama / birim karışık)
- BIST DUNYH: ortak günlerde yeni/eski oranı 6.923 (bölünme / birim)
- BIST FENER: ortak günlerde oran tek tip değil (0.964 .. 2.754; ayarlama / birim karışık)
- BIST KENT: ortak günlerde oran tek tip değil (1.000 .. 1.499; ayarlama / birim karışık)
- BIST KONTR: ortak günlerde oran tek tip değil (0.986 .. 1.944; ayarlama / birim karışık)
- BIST KRTEK: ortak günlerde yeni/eski oranı 3.529 (bölünme / birim)
- BIST MANAS: ortak günlerde oran tek tip değil (1.000 .. 1.868; ayarlama / birim karışık)
- BIST MARTI: ortak günlerde oran tek tip değil (0.926 .. 1.579; ayarlama / birim karışık)
- BIST MERCN: ortak günlerde yeni/eski oranı 0.330 (bölünme / birim)
- BIST MERKO: ortak günlerde yeni/eski oranı 7.388 (bölünme / birim)
- BIST MRGYO: ortak günlerde oran tek tip değil (0.940 .. 1.474; ayarlama / birim karışık)
- BIST ORCAY: ortak günlerde oran tek tip değil (0.995 .. 2.529; ayarlama / birim karışık)
- BIST SEKFK: ortak günlerde yeni/eski oranı 1.809 (bölünme / birim)
- BIST SELVA: ortak günlerde oran tek tip değil (0.979 .. 1.722; ayarlama / birim karışık)
- BIST TUCLK: ortak günlerde oran tek tip değil (0.990 .. 1.724; ayarlama / birim karışık)
- BIST USAK: ortak günlerde oran tek tip değil (1.000 .. 1.596; ayarlama / birim karışık)
- BIST YKSLN: ortak günlerde oran tek tip değil (0.973 .. 1.693; ayarlama / birim karışık)

## 5. İleri test

- Ölçüm komutu: `python CANLI_TARAMA.py olc --tarih 2026-11-20` (en geç ölçüm tarihi 2026-12-08).
- Cetvel: YAPI_HEDEF yh_olay_olc: giriş t+1 açılış, 15 geçerli bar, +%5 / +%10 kapanışla stop'tan önce (h5 / h10), stop önce (st5), takip stopu; eş = aynı giriş günü aynı OC momentum x likidite kovası (en az 3); liste (10) ve havuzun tamamı ölçülür; sonuç CANLI_SONUC.md'ye eklenir (satır silinmez).
- Sonuçlar arastirma_cikti/canli/CANLI_SONUC.md'ye eklenir.
