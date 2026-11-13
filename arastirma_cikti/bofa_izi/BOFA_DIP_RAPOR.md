# Dipte BofA: kurulum + tetik — sonuç (13 Kasım 2026)

## Düzeltme sonrası (ana model denetimi 13.11.2026)

Bu rapor, BofA liste verisi yeniden ayrıştırıldıktan sonra AYNI ön kayıt, aynı eşikler ve aynı tanımlarla yeniden koşuldu. Sapma gerekçesi: AYRIŞTIRMA DÜZELTMESİ (ana model denetimi 13.11): çok kurumlu haberlerde kurum etiketi, kurum adı hisse satırları, aylık özet haberleri; eşikler değişmedi. Düzeltilenler: çok kurumlu haberlerde her tablonun kurumu tablodan önceki başlık / cümleden okunur (belirsiz -> BİLİNMİYOR, ölçüme girmez); hisse sütunundaki kurum adı satırları ('HSBC: -433 mn') düşer; aylık / dönemsel özet haberleri tur='aylik' / 'donemsel' (kapsam dışı); sayfada biriken günlük güncellemeler ('GÜNCELLEME 30 EYLÜL') kendi tarihini taşır (Eylül listesi Haziran tarihli sayılmaz); numaralı tek satırlık tablolar tek liste; haber sitelerinin ilgili haber kuşağı gövde dışı (kenar kuşağından 'SSAAT 56 TL' gibi satırlar BofA listesi sayılmaz). Liste mührü 7020587fbc90 -> 28014e1a3be8.

**KARAR: DEĞİŞMEDİ** — eski: kurulum İZ DEĞİL / BofA tetikli ÖRNEKLEM YETERSİZ (n = 0); yeni: kurulum İZ DEĞİL / BofA tetikli ÖRNEKLEM YETERSİZ (n = 0). Eski rapor ve JSON: /home/user/col_yolu/arastirma_cikti/bofa_izi/eski_v1.

| satır | ESKİ | YENİ |
|---|---|---|
| BofA tetikli kurulum (FI 60 gün) | n 2, eşli fark -30,9% [-45,1%, -16,7%], sıra 0.18, portföy -0.04 / %90 0.09 | n 2, eşli fark -30,9% [-45,1%, -16,7%], sıra 0.18, portföy -0.04 / %90 0.09 |
| BofA'sız kurulum | n 30, eşli fark +4,5% [-7,5%, +15,7%], sıra 0.53, portföy 0.39 / %90 0.48 | n 30, eşli fark +4,5% [-7,5%, +15,7%], sıra 0.53, portföy 0.39 / %90 0.48 |
| ABD 2023 kurulum | n 81, eşli fark +24,8% [+8,9%, +43,0%], sıra 0.55, portföy 2.85 / %90 0.91 | n 81, eşli fark +24,8% [+8,9%, +43,0%], sıra 0.55, portföy 2.85 / %90 0.91 |
| ABD 2024-26 kurulum | n 146, eşli fark +20,6% [+0,4%, +46,2%], sıra 0.48, portföy 2.25 / %90 4.17 | n 146, eşli fark +20,6% [+0,4%, +46,2%], sıra 0.48, portföy 2.25 / %90 4.17 |
| BIST 2024-26 kurulum | n 28, eşli fark +3,7% [-9,1%, +17,5%], sıra 0.52, portföy 0.11 / %90 0.28 | n 28, eşli fark +3,7% [-9,1%, +17,5%], sıra 0.52, portföy 0.11 / %90 0.28 |
| BofA tetik sayısı | 5519 | 5679 |
| tetikli kurulum olayı (60 gün) | 1 | 1 |
| tetikli kurulum kriz sonrası | 1 | 1 |
| dönem (n / toplam) | {'kesik_disi_ya_da_acik': 1, 'kriz_sonrasi_giris': 1, 'n': 0, 'toplam': 1} | {'kesik_disi_ya_da_acik': 1, 'kriz_sonrasi_giris': 1, 'n': 0, 'toplam': 1} |
| izleme listesi n | 10 | 10 |
| izlemede BofA 20 günde | 1 | 1 |
| kriz sonrası BofA tetiği (tek tek) | HDFGS 2026-10-21 sıra 1 | HDFGS 2026-10-21 sıra 1 |
| izleme listesi | SKBNK, KLRHO, PRZMA, BORLS, OTTO, A1CAP, IZFAS, BURVA, USAK, IHLAS | SKBNK, KLRHO, PRZMA, BORLS, OTTO, A1CAP, IZFAS, BURVA, USAK, IHLAS |

Soru: Cemal 13.11.2026: 'Her BofA alımında al demiyorum. Dipte %80-90 düşüş var, artık daha fazla düşmeyecek bir görüntü, çok ucuzlamış bir noktada BofA alımı ile girsek.' KURULUM = derin düşüş + dip tutuyor (yeni dip yok) + dipten henüz kaçmamış; TETİK = BofA alımı. (1) Kurulum tek başına (BofA'sız) iz mi (BIST / ABD / Avrupa)? (2) BofA alımı kurulumun üstüne bir şey ekliyor mu (BIST)? (3) Bugün kurulumdaki BIST hisseleri ve son 20 günde BofA alımı görünenler (İZLEME, öneri değil).

## Özet (düz dil)

- **Dipte -%80+ ve dip tutuyor KURULUMU tek başına: İZ DEĞİL.** ABD 2023: n 81, eşli fark +24,8% [+8,9%, +43,0%] TUTTU; ABD 2024-26: n 146, eşli fark +20,6% [+0,4%, +46,2%]; AVR 2023: n 3, eşli fark -38,0% [-87,2%, +14,5%]; AVR 2024-26: n 8, eşli fark -8,0% [-22,7%, +11,0%]; BIST 2023: n 4, eşli fark -7,6% [-44,6%, +6,6%]; BIST 2024-26: n 28, eşli fark +3,7% [-9,1%, +17,5%].
- 12 ay (250 gün) olasılıkları: ABD 2016-22 (n 482): +%100 %47 (eşin 1,57 katı, tabanın 4,11), -%50 %46 (eşin 1,68, tabanın 2,90 katı); ABD 2023 (n 79): +%100 %62 (eşin 2,01 katı, tabanın 4,33), -%50 %46 (eşin 2,00, tabanın 4,16 katı); ABD 2024-26 (n 106): +%100 %75 (eşin 1,88 katı, tabanın 4,02), -%50 %36 (eşin 1,71, tabanın 2,53 katı); AVR 2016-22 (n 32): +%100 %44 (eşin 2,88 katı, tabanın 15,06), -%50 %38 (eşin 3,12, tabanın 5,46 katı); AVR 2023 (n 1): +%100 %100 (eşin — katı, tabanın 52,64), -%50 %0 (eşin 0,00, tabanın 0,00 katı); AVR 2024-26 (n 5): +%100 %40 (eşin 6,52 katı, tabanın 10,04), -%50 %40 (eşin 4,44, tabanın 10,35 katı); BIST 2016-22 (n 53): +%100 %36 (eşin 0,94 katı, tabanın 0,85), -%50 %9 (eşin 1,96, tabanın 1,57 katı); BIST 2023 (n 4): +%100 %75 (eşin 1,62 katı, tabanın 1,41), -%50 %0 (eşin 0,00, tabanın 0,00 katı); BIST 2024-26 (n 10): +%100 %50 (eşin 2,42 katı, tabanın 2,00), -%50 %20 (eşin 3,81, tabanın 3,51 katı).
- **BofA alımı eklenince (BIST, 2023-04 .. 2026-08): ÖRNEKLEM YETERSİZ (n = 0).** Tetikli olay 0, FI ölçülen 0: eşli r60 farkı — [—, —], ortalama r60 —. Aynı dönemde BofA'sız kurulum olayları n 30, eşli fark +4,5%; BofA'lı - BofA'sız = — [—, —].
- Tutma dönemi (G1 giriş, BofA satış ilk 5'te çık; BİLGİ): n 0, ortalama getiri —, eşli fark — [—, —], medyan — gün.
- Bugün (veri sonu 2026-11-13) kurulumdaki BIST hissesi 10; bunlardan son 20 günde BofA alım ilk 5'te görünen 1; kriz sonrası (01.09.2026'dan) BofA tetikli kurulum olayı 1. Bu bir İZLEME listesidir, öneri değildir; kriz dönemi karara girmez.
- Sonuç: kurulum tek başına **İZ DEĞİL**; BofA tetiğiyle **YOL YOK** (ÖRNEKLEM YETERSİZ (n = 0)).

## (1) KURULUM TEK BAŞINA — karar tablosu (FI_OLCUT 60 gün)

**KARAR: İZ DEĞİL** (İZ = ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26 dört hücre; BIST ve 2016-22 bilgi)

| pazar | hücre | olay | n (r60) | hisse | ort r60 | medyan r60 | eş r60 | eşli fark | %95 aralık | sıra | portföy | rastgele p90 | 4 şart | r60'ta kırık |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BIST | 2016-22 | 56 | 56 | 24 | +5,5% | -2,4% | +11,5% | -6,0% | [-16,7%, +3,9%] | 0,43 | +17,2% | +108,0% | tutmadı: ortalama eşli fark <= 0; bootstrap %95 alt uç <= 0; sıra <= 0,50; portföy rastgele %90'ı geçmedi | 0 |
| BIST | 2023 | 4 | 4 | 4 | +32,1% | +38,4% | +39,7% | -7,6% | [-44,6%, +6,6%] | 0,40 | +12,9% | +23,3% | tutmadı: n = 4 < 30 (örneklem yetersiz) | 0 |
| BIST | 2024-26 | 34 | 28 | 17 | +6,4% | -1,6% | +2,7% | +3,7% | [-9,1%, +17,5%] | 0,52 | +10,6% | +28,3% | tutmadı: n = 28 < 30 (örneklem yetersiz) | 0 |
| ABD | 2016-22 | 508 | 508 | 226 | +13,5% | +1,1% | +16,2% | -2,7% | [-13,3%, +6,1%] | 0,48 | +6,2% | +689,7% | tutmadı: ortalama eşli fark <= 0; bootstrap %95 alt uç <= 0; sıra <= 0,50; portföy rastgele %90'ı geçmedi | 7 |
| ABD | 2023 | 81 | 81 | 57 | +36,1% | +11,9% | +11,4% | +24,8% | [+8,9%, +43,0%] | 0,55 | +284,8% | +91,0% | TUTTU | 1 |
| ABD | 2024-26 | 165 | 146 | 76 | +37,1% | +3,3% | +16,5% | +20,6% | [+0,4%, +46,2%] | 0,48 | +225,3% | +416,9% | tutmadı: sıra <= 0,50; portföy rastgele %90'ı geçmedi | 1 |
| AVR | 2016-22 | 32 | 32 | 16 | +19,3% | +10,2% | +10,4% | +8,8% | [-6,8%, +25,4%] | 0,56 | +97,4% | +63,1% | tutmadı: bootstrap %95 alt uç <= 0 | 0 |
| AVR | 2023 | 3 | 3 | 2 | -36,0% | -42,7% | +2,0% | -38,0% | [-87,2%, +14,5%] | 0,31 | -10,8% | +4,4% | tutmadı: n = 3 < 30 (örneklem yetersiz) | 1 |
| AVR | 2024-26 | 8 | 8 | 4 | -6,5% | -12,4% | +1,4% | -8,0% | [-22,7%, +11,0%] | 0,30 | -5,2% | +7,1% | tutmadı: n = 8 < 30 (örneklem yetersiz) | 0 |

## OLASILIK TABLOSU — 250 işlem günü (~12 ay) içinde +%100'e / -%50'ye dokunma (BİLGİ)

| pazar | hücre | n | P(+%100) | eş | kat (eş) | taban | kat (taban) | P(-%50) | eş | kat (eş) | taban | kat (taban) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BIST | 2016-22 | 53 | %35,8 | %38,1 | 0,94 | %41,9 | 0,85 | %9,4 | %4,8 | 1,96 | %6,0 | 1,57 |
| BIST | 2023 | 4 | %75,0 | %46,3 | 1,62 | %53,3 | 1,41 | %0,0 | %2,2 | 0,00 | %4,3 | 0,00 |
| BIST | 2024-26 | 10 | %50,0 | %20,7 | 2,42 | %25,0 | 2,00 | %20,0 | %5,2 | 3,81 | %5,7 | 3,51 |
| ABD | 2016-22 | 482 | %46,7 | %29,6 | 1,57 | %11,4 | 4,11 | %46,1 | %27,4 | 1,68 | %15,9 | 2,90 |
| ABD | 2023 | 79 | %62,0 | %30,9 | 2,01 | %14,3 | 4,33 | %45,6 | %22,8 | 2,00 | %11,0 | 4,16 |
| ABD | 2024-26 | 106 | %74,5 | %39,6 | 1,88 | %18,5 | 4,02 | %35,8 | %21,0 | 1,71 | %14,2 | 2,53 |
| AVR | 2016-22 | 32 | %43,8 | %15,2 | 2,88 | %2,9 | 15,06 | %37,5 | %12,0 | 3,12 | %6,9 | 5,46 |
| AVR | 2023 | 1 | %100,0 | %0,0 | — | %1,9 | 52,64 | %0,0 | %2,8 | 0,00 | %4,1 | 0,00 |
| AVR | 2024-26 | 5 | %40,0 | %6,1 | 6,52 | %4,0 | 10,04 | %40,0 | %9,0 | 4,44 | %3,9 | 10,35 |

## 120 ve 250 gün getirisi (ikinci sırada; BİLGİ)

| pazar | hücre | n120 | ort r120 | medyan | eş | eşli fark [%95] | n250 | ort r250 | medyan | eş | eşli fark [%95] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BIST | 2016-22 | 55 | +8,3% | +0,0% | +20,9% | -12,6% [-23,6%, -1,0%] | 53 | +44,5% | +22,2% | +72,4% | -27,9% [-58,6%, +10,3%] |
| BIST | 2023 | 4 | +28,1% | +29,4% | +39,0% | -10,9% [-62,8%, +9,1%] | 4 | +21,3% | +23,4% | +44,7% | -23,4% [-69,1%, +14,0%] |
| BIST | 2024-26 | 20 | +5,9% | -6,9% | +9,1% | -3,2% [-18,8%, +11,7%] | 10 | +174,7% | +14,3% | +27,4% | +147,2% [-27,0%, +328,5%] |
| ABD | 2016-22 | 495 | +25,3% | -4,1% | +15,4% | +9,9% [-4,8%, +29,0%] | 482 | +102,5% | +3,7% | +46,7% | +55,8% [+11,9%, +111,6%] |
| ABD | 2023 | 79 | +52,1% | +17,7% | +18,7% | +33,4% [+7,3%, +58,4%] | 79 | +110,9% | +41,4% | +44,4% | +66,5% [+14,0%, +110,3%] |
| ABD | 2024-26 | 129 | +68,2% | +21,2% | +37,4% | +30,8% [+6,9%, +59,2%] | 106 | +174,6% | +82,2% | +102,3% | +72,3% [+20,3%, +128,2%] |
| AVR | 2016-22 | 32 | +19,3% | +14,0% | +15,5% | +3,8% [-14,3%, +21,5%] | 32 | +34,2% | +27,5% | +30,8% | +3,5% [-23,5%, +38,7%] |
| AVR | 2023 | 1 | +30,0% | +30,0% | -2,5% | +32,5% [—, —] | 1 | +115,4% | +115,4% | +4,5% | +110,9% [—, —] |
| AVR | 2024-26 | 7 | +21,4% | -18,2% | +4,1% | +17,3% [-37,4%, +107,6%] | 5 | +104,6% | +42,5% | +10,4% | +94,3% [-36,1%, +296,5%] |

## (2) KURULUM + BofA ALIM İLK 5 TETİĞİ (BIST, 17.04.2023 .. 31.08.2026)

**KARAR: ÖRNEKLEM YETERSİZ (n = 0)** — tutmayan: n = 0 < 30

Sayım: {"kurulum_olay_arsiv_donemi": {"bofali": 3, "bofasiz": 35}, "olay60": 1, "olay60_genis": 7, "olay60_hucre": {"2023": 0, "2024-26": 0}, "olay60_kriz_sonrasi": 1, "tetik": 5679, "tetik_genis": 12, "tetik_kurulum_bilinen": 5679, "tetik_kurulumlu": 1, "tetik_kurulumlu_hisse": 1}

| satır | olay | n (r60) | ort r60 | eşli fark | %95 aralık | sıra | portföy / p90 | n250 | P(+%100) (kat eş) | P(-%50) (kat eş) | r250 eşli fark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BofA tetikli kurulum (havuz) | 0 | 0 | — | — | [—, —] | — | — / — | 0 | — (—) | — (—) | — |
|   alt hücre BIST 2023 | 0 | 0 | — | — | [—, —] | — | — / — | 0 | — (—) | — (—) | — |
|   alt hücre BIST 2024-26 | 0 | 0 | — | — | [—, —] | — | — / — | 0 | — (—) | — (—) | — |
| BofA'SIZ kurulum olayları (aynı dönem) | 35 | 30 | +11,7% | +4,5% | [-7,5%, +15,7%] | 0,53 | +38,5% / +48,5% | 14 | %57 (2,04) | %14 (3,26) | +98,5% |
| BofA'LI kurulum olayları (±20 gün, BİLGİ) | 3 | 2 | -21,0% | -30,9% | [-45,1%, -16,7%] | 0,18 | -4,2% / +9,3% | 0 | — (—) | — (—) | — |
| Geniş okuma (son 20 barda kurulum; BİLGİ) | 3 | 2 | -20,1% | -38,1% | [-38,1%, -38,1%] | 0,30 | -4,0% / +17,0% | 0 | — (—) | — (—) | — |

BofA tetikli - BofA'sız ortalama eşli r60 farkı: — [—, —] (n — / —; bağımsız ay kümeli bootstrap).

Tutma dönemi (BİLGİ; G1 giriş, BofA satış ilk 5 -> sonraki açılış, yoksa 250 gün): kapanmış dönem n 0 (toplam 1, açık / kesik dışı 1); ortalama getiri —, medyan —, eş —, eşli fark — [—, —], sıra —, medyan — gün, çıkış nedeni {}.

### BofA tetikli kurulum olayları (tek tek; 1 olay, G2 girişi)

| hisse | tetik yayını | tür | sıra | birim | pay | maliyet | karar günü | düşüş | dipten | giriş | r60 | eşli fark | r250 | +%100 | -%50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HDFGS | 2026-10-21 19:37 | gun_sonu | 1 | lot | 8,72 | 1,11 | 2026-10-21 | -82% | 1,29 | 2026-10-22 | — | — | — | — | — |

### Tutma dönemleri (tek tek; 1)

| hisse | yayın | giriş | tip | çıkış | neden | gün | getiri | eş | eşli fark | en yüksek | en düşük |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HDFGS | 2026-10-21 19:37 | 2026-10-22 | acilis | 2026-11-09 | satis | 11 | +17,6% | +6,6% | +11,0% | +15,7% | -18,5% |

## (3) KRİZ SONRASI — İZLEME LİSTESİ (BİLGİ; öneri değil, karara girmez)

Veri sonu 2026-11-13. Kurulumdaki BIST hissesi 10; son 20 işlem gününde BofA alım ilk 5 tetiği görünen 1. Fiyatlar ekran fiyatı (TL).

| hisse | düşüş (250g tepe) | tepe (tarih) | dip (tarih) | son | dipten kat | son 20 gün | BofA 20g | BofA son tetik | tür / sıra | maliyet | pay | G1 fiyat | G1'den bugüne | maliyetten bugüne |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SKBNK | -80% | 19,63 (2026-07-17) | 2,88 (2026-10-30) | 3,83 | 1,33 | -24,9% | EVET (2 gün) | 2026-11-05 12:46 | gun_ici / 2 | — | — | 3,65 | +4,9% | — |
| KLRHO | -97% | 658,50 (2026-02-04) | 8,68 (2026-10-30) | 11,73 | 1,35 | +10,0% | — | — | — | — | — | — | — | — |
| PRZMA | -91% | 91,00 (2026-08-31) | 6,38 (2026-10-30) | 8,60 | 1,35 | -22,0% | — | — | — | — | — | — | — | — |
| BORLS | -85% | 12,95 (2025-11-14) | 1,50 (2026-09-30) | 1,89 | 1,26 | -12,1% | — | — | — | — | — | — | — | — |
| OTTO | -83% | 528,00 (2026-01-06) | 70,80 (2026-10-23) | 89,25 | 1,26 | -28,0% | — | — | — | — | — | — | — | — |
| A1CAP | -82% | 18,05 (2026-02-17) | 2,50 (2026-10-30) | 3,17 | 1,27 | -20,6% | — | — | — | — | — | — | — | — |
| IZFAS | -82% | 72,40 (2026-04-20) | 10,53 (2026-10-06) | 12,72 | 1,21 | -37,9% | — | — | — | — | — | — | — | — |
| BURVA | -82% | 1295,00 (2026-04-30) | 187,00 (2026-10-28) | 238,80 | 1,28 | -40,7% | — | — | — | — | — | — | — | — |
| USAK | -81% | 2,05 (2026-01-29) | 0,36 (2026-10-30) | 0,39 | 1,08 | -4,9% | — | — | — | — | — | — | — | — |
| IHLAS | -80% | 3,80 (2025-11-21) | 0,67 (2026-10-30) | 0,76 | 1,13 | -9,5% | — | — | — | — | — | — | — | — |

### Kriz sonrası BofA tetikli kurulum tetikleri (G2 >= 01.09.2026; 1)

| hisse | yayın | tür / sıra | birim | pay | maliyet | karar günü | düşüş | dipten | G1 | G1 fiyat | bugüne |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HDFGS | 2026-10-21 19:37 | gun_sonu / 1 | lot | 8,72 | 1,11 | 2026-10-21 | -82% | 1,29 | 2026-10-22 (acilis) | 1,08 | +18,5% |

## Sınırlar

Fiyat evreni bugün işlem gören hisseler (BIST Yahoo önbelleği, V_ABD, V_AVR): -%80 düşüp sonra batan / kotasyondan çıkan şirketler evrende yok -> P(+%100) yukarı, P(-%50) aşağı yanlı; derin düşmüşlerde batma eşlerden sık olduğu için eşli fark da yukarı yanlı olabilir (ABD'de 2016'da işlem görenlerin %44'ü sonradan çıkmış, IZ_VERI_ENVANTERI). AKD kodu kurum kimliği değildir; BofA arşivi her günü kapsamaz ('BofA'sız' olayların bir kısmında görülmemiş BofA alımı olabilir). Yahoo düzeltmesi bedelli sermaye artırımlarında eksik olabilir (kırık kuralı yalnız büyük sıçramayı yakalar). İşlem maliyeti / kayma yok; çok düşük fiyatlı hissede açılıştan alım varsayımı iyimser.

## Ön kayıt ve kapı

- Ön kayıt: BOFA_DIP_ON_KAYIT.md; git {"commit": "22750ff19fd5853412e9944598009d6422792e15", "commit_zamani": "2026-11-13T17:17:37+00:00"}; eşik mührü cac944c2b07c; kod aynı: False; SAPMA: AYRIŞTIRMA DÜZELTMESİ (ana model denetimi 13.11): çok kurumlu haberlerde kurum etiketi, kurum adı hisse satırları, aylık özet haberleri; eşikler değişmedi
- Koşu 2026-11-13 18:20:44 UTC – 2026-11-13 18:21:30 UTC; BOFA_IZI DİP v1.0 (bofa_dip_20261113): KURULUM (250 gün tepeden <= -%80, son 10 günde yeni dip yok, dipten <= 1,5 kat) tek başına (BIST / ABD / Avrupa, FI_OLCUT 60 gün + 120 / 250 gün + olasılık tablosu) + BofA alım ilk 5 tetiği (BIST) + kriz sonrası izleme (ön kayıtlı)
- Satır verisi: /tmp/bofa/dip_*.csv.gz (repoya girmez)
