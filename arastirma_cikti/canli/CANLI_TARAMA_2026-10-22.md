# CANLI TARAMA — 2026-10-22

**DÜRÜSTLÜK: bu liste 'izleme / ileri test' listesidir, ÖNERİ DEĞİLDİR. CLAUDE.md öneri modülünün üç kapısından (tarama + dosya + risk) burada yalnız tarama kapısı var ve seçici ÖLÇÜLEMEDİ düzeyindedir (dipte + gövdeli kırılım KATKI+ ama hücre başına +3..+9 puan). Alım-satım kararı Cemal'indir; Claude yatırım danışmanı değildir.**

Taban oran hatırlatması: 3 yılda 10x ABD mikro-cap ~%1, BIST USD ~%1,85. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı: sonuçlar yukarı yanlı okunur).

- Üretim (UTC): 2026-11-20T06:19:42Z · CANLI_TARAMA v1.0 (2026-11-20): S6 son 5 gün + havuz Ş1 VE Ş7 (kademeli) + puan7 sırası; ileri test olc (YAPI_HEDEF cetveli)
- Kurallar CT_ESIK_SHA `a43ec505618579ff…` (ön kayıt arastirma_cikti/canli/CANLI_ON_KAYIT.md; kapı geçti)

## 1. Veri

| Pazar | hisse | son tarih | son 5 işlem günü | kaynak |
|---|---|---|---|---|
| ABD | 1411 | 2026-10-22 | 2026-10-16 .. 2026-10-22 | /tmp/veri |
| AVR | 580 | 2026-10-27 | 2026-10-21 .. 2026-10-27 | /tmp/veri |
| BIST | 581 | 2026-10-22 | 2026-10-16 .. 2026-10-22 | /tmp/veri |

Veri güncellemesi YOK: mevcut V_*.pkl ile tarandı; 'son 5 işlem günü' her pazarın kendi son tarihinden geriye 5 bar.

## 2. Sinyal ve havuz

| Pazar | son 5 günde S6 AL | havuz dışı (t) | likidite alt %20 | bölünme şüphesi | 60 gün tekil düşen | şüpheli dışlanan | sinyal | özellik hatası |
|---|---|---|---|---|---|---|---|---|
| ABD | 82 | 17 | 16 | 1 | 22 | 0 | 43 | 0 |
| AVR | 16 | 4 | 4 | 0 | 5 | 0 | 7 | 0 |
| BIST | 3 | 0 | 0 | 0 | 0 | 0 | 3 | 0 |

| Havuz kademesi | toplam | ABD | AVR | BIST |
|---|---|---|---|---|
| Ş1 VE Ş7 (asıl) | 4 | 3 | 1 | 0 |
| (i) Ş1 VE F22 > 0 | 8 | 7 | 1 | 0 |
| (ii) Ş1 | 8 | 7 | 1 | 0 |

**Kullanılan kademe: Ş1 VE Ş7 (asıl)**

## 3. En iyi 10 (puan7 sırası; pazar başına en çok 5)

| # | pazar | sembol | sinyal | kapanış | hat | F21 | stop0 (uzaklık) | +%5 / +%10 | puan7 | Ş9 | Ş10 | parmak | F15 | F17 | F18 | 12 kural | mahkeme | likidite 20g |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ABD | RARE | 2026-10-20 | 16,02 | 14,08 | 15,73 | 13,80 (%-13,9) | 16,82 / 17,62 | 0,578 | - | - | ✓ | 0,14 | %-59 | %+13,8 | 7/12 | ÖNCEKİ BÖLGE DAHA UYGUN | 61,1 M USD |
| 2 | ABD | ALKT | 2026-10-21 | 15,10 | 13,55 | 14,70 | 13,28 (%-12,0) | 15,86 / 16,61 | 0,536 | - | - | ✓ | 0,23 | %-31 | %+11,4 | 8/12 | tutarlı | 29,4 M USD |
| 3 | ABD | FNF | 2026-10-22 | 41,88 | 38,46 | 40,98 | 37,69 (%-10,0) | 43,97 / 46,06 | 0,381 | - | - | ✓ | 0,22 | %-26 | %+8,9 | 9/12 | tutarlı | 99,4 M USD |
| 4 | AVR | NOVO-B.CO | 2026-10-22 | 264,75 | 243,15 | 263,45 | 238,29 (%-10,0) | 277,99 / 291,23 | 0,341 | - | - | - | 0,22 | %-22 | %+8,9 | 9/12 | tutarlı | 163,8 M EUR |

Okuma: stop0 = hat x 0,98; hedefler kapanışa göre (gerçek giriş ertesi açılış). puan7 = 7. tur M2 modelinin P(15 barda +%5 stop'tan önce) tahmini (eğitim 2016 - 31.08.2026 Y1 olayları; modelin taban P'si 0,377). Ş9 = U dip çanağı; Ş10 = MACD pozitif uyumsuzluk; parmak = F19 P1.1 (4 mum dip öbeği). Mahkeme bilgi satırıdır (eleme değil).

## 4. Şüpheli veri (listeden dışlandı)

- ABD BRZE: son 5 barda |günlük getiri| > %40
- ABD EYPT: son 5 barda |günlük getiri| > %40
- BIST BIGEN: son 5 barda |günlük getiri| > %40
- BIST GRTHO: son 5 barda |günlük getiri| > %40

## 5. İleri test

- Ölçüm komutu: `python CANLI_TARAMA.py olc --tarih 2026-10-22` (en geç ölçüm tarihi 2026-11-12).
- Cetvel: YAPI_HEDEF yh_olay_olc: giriş t+1 açılış, 15 geçerli bar, +%5 / +%10 kapanışla stop'tan önce (h5 / h10), stop önce (st5), takip stopu; eş = aynı giriş günü aynı OC momentum x likidite kovası (en az 3); liste (10) ve havuzun tamamı ölçülür; sonuç CANLI_SONUC.md'ye eklenir (satır silinmez).
- Sonuçlar arastirma_cikti/canli/CANLI_SONUC.md'ye eklenir.
