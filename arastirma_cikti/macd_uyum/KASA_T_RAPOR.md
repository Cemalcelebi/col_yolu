# MACD_UYUM — KASA KÖR SINAMASI SONUCU (T: derin toplam uyumsuzluk; 2023-24)

KARAR: **TUTTU** — madde (a) birleşik ÜST10 boot alt > 0,10: True; (b) ÜST10 > ALT10: True; (c) ABD ve AVR ÜST10 > 0,10: True; (d) birleşik FARK > 0: True; birleşik n 259.

Ön kayıt: arastirma_cikti/macd_uyum/KASA_T_ON_KAYIT.md (ana bölüm 2aedf2e). Koşu UTC 2026-11-25T06:04:18Z. Kod MACD_UYUM_KASA v1.0 (2026-11-25): K47 T (derin toplam uyumsuzluk) KASA 2023-24 kör sınaması.
Veri kesiği 2024-12-31 (en geç tarih: V_ABD.pkl 2024-12-31, V_AVR.pkl 2024-12-31, V_BIST.pkl 2024-12-31).

## Ö1 ÜST10 / ALT10 (temiz eş sırası; ay kümeli boot %95)

| Grup | Hücre | n | ÜST10 [%95] | ALT10 [%95] | ÜST20 | r15 ort | eş ort |
|---|---|---|---|---|---|---|---|
| T | ABD | 211 | %14,7 [11,3; 19,3] | %11,4 [7,7; 14,6] | %28,9 | +1,75 | +1,56 |
| T | AVR | 48 | %16,7 [8,8; 23,3] | %14,6 [5,4; 28,1] | %27,1 | +1,55 | +0,22 |
| T | birlesik | 259 | %15,1 [11,6; 18,5] | %12,0 [9,0; 15,4] | %28,6 | +1,72 | +1,31 |
| T | BIST | 121 | %10,7 [7,0; 15,8] | %9,1 [5,1; 18,6] | %18,2 | +7,55 | +7,61 |
| Tz | ABD | 994 | %11,7 [9,4; 13,9] | %11,6 [8,4; 15,0] | %22,3 | +2,10 | +1,95 |
| Tz | AVR | 348 | %16,7 [13,5; 20,1] | %14,9 [10,3; 19,3] | %24,7 | +0,26 | +0,23 |
| Tz | birlesik | 1342 | %13,0 [10,8; 15,2] | %12,4 [9,8; 15,4] | %23,0 | +1,62 | +1,50 |
| Tz | BIST | 424 | %12,0 [7,9; 15,8] | %14,2 [11,0; 18,5] | %21,7 | +1,53 | +1,95 |

Piyasa yukarı (eş ort > 0) / aşağı (<= 0):

| Grup | Hücre | Piyasa | n | ÜST10 [%95] | ALT10 |
|---|---|---|---|---|---|
| T | ABD | yukari | 118 | %12,7 [6,9; 18,1] | %13,6 |
| T | ABD | asagi | 93 | %17,2 [10,5; 24,7] | %8,6 |
| T | AVR | yukari | 26 | %23,1 [11,8; 32,0] | %11,5 |
| T | AVR | asagi | 22 | %9,1 [0,0; 19,0] | %18,2 |
| T | birlesik | yukari | 144 | %14,6 [9,8; 18,6] | %13,2 |
| T | birlesik | asagi | 115 | %15,7 [9,5; 22,1] | %10,4 |
| T | BIST | yukari | 94 | %11,7 [8,6; 20,7] | %5,3 |
| T | BIST | asagi | 27 | %7,4 [0,0; 14,8] | %22,2 |
| Tz | ABD | yukari | 631 | %11,9 [9,1; 14,0] | %9,8 |
| Tz | ABD | asagi | 363 | %11,3 [7,6; 15,5] | %14,6 |
| Tz | AVR | yukari | 172 | %15,1 [10,7; 18,3] | %17,4 |
| Tz | AVR | asagi | 176 | %18,2 [13,9; 23,5] | %12,5 |
| Tz | birlesik | yukari | 803 | %12,6 [9,8; 14,7] | %11,5 |
| Tz | birlesik | asagi | 539 | %13,5 [10,3; 17,7] | %13,9 |
| Tz | BIST | yukari | 249 | %10,8 [5,7; 16,8] | %14,1 |
| Tz | BIST | asagi | 175 | %13,7 [10,4; 19,0] | %14,3 |

## Ö2 R15 temiz eş FARK (C2.c2_hucre + MU.mu_hukum, plasebo hariç; güç eğrisi 'acik')

| Grup | Hücre | n | FARK [%95] | medyan | SIRA [alt] | L3O | güç | hüküm | +%5 olay / eş | stop olay / eş |
|---|---|---|---|---|---|---|---|---|---|---|
| T | ABD | 211 | +0,20 [-1,63; +1,74] | +0,50 | 0,531 [0,499] | -0,72 | 0,61 | ÖLÇÜLEMEDİ | %55,7 / %47,2 | %35,7 / %35,6 |
| T | AVR | 48 | +1,33 [-2,03; +4,22] | -0,94 | 0,485 [0,387] | -2,12 | 0,24 | ÖLÇÜLEMEDİ | %41,7 / %38,9 | %37,5 / %28,7 |
| T | birlesik | 259 | +0,41 [-1,29; +1,78] | +0,23 | 0,522 [0,489] | -0,81 | - | ÖLÇÜLEMEDİ | %53,1 / %45,7 | %36,0 / %34,3 |
| T | BIST | 121 | -0,06 [-2,37; +0,93] | -1,03 | 0,508 [0,427] | -1,78 | 0,51 | ÖLÇÜLEMEDİ | %60,8 / %63,5 | %31,7 / %27,5 |
| Tz | ABD | 994 | +0,15 [-1,14; +1,21] | +0,09 | 0,512 [0,474] | -0,82 | 1,00 | TUTMADI | %47,8 / %47,1 | %34,6 / %33,3 |
| Tz | AVR | 348 | +0,02 [-0,84; +0,98] | +0,01 | 0,502 [0,467] | -0,61 | 0,96 | TUTMADI | %42,4 / %36,3 | %30,8 / %29,3 |
| Tz | birlesik | 1342 | +0,12 [-0,82; +1,03] | +0,08 | 0,509 [0,479] | -0,52 | - | ÖLÇÜLEMEDİ | %46,4 / %44,3 | %33,6 / %32,2 |
| Tz | BIST | 424 | -0,42 [-1,91; +0,75] | -1,41 | 0,498 [0,459] | -1,86 | 0,99 | TUTMADI | %50,1 / %48,7 | %39,5 / %40,9 |

## Yıl ayrımı (bilgi)

| Grup | Hücre | Yıl | n | ÜST10 | ALT10 | FARK [%95] |
|---|---|---|---|---|---|---|
| T | ABD | 2023 | 113 | %14,2 | %10,6 | +1,01 [-1,48; +2,71] |
| T | ABD | 2024 | 98 | %15,3 | %12,2 | -0,74 [-2,90; +1,88] |
| T | AVR | 2023 | 20 | %20,0 | %20,0 | +1,73 [-4,57; +7,16] |
| T | AVR | 2024 | 28 | %14,3 | %10,7 | +1,05 [-2,47; +3,40] |
| T | birlesik | 2023 | 133 | %15,0 | %12,0 | +1,12 [-1,45; +2,65] |
| T | birlesik | 2024 | 126 | %15,1 | %11,9 | -0,34 [-2,59; +1,99] |
| T | BIST | 2023 | 58 | %6,9 | %5,2 | -0,05 [-7,60; +0,76] |
| T | BIST | 2024 | 63 | %14,3 | %12,7 | -0,07 [-1,95; +1,63] |
| Tz | ABD | 2023 | 566 | %11,8 | %9,5 | +0,62 [-1,36; +1,93] |
| Tz | ABD | 2024 | 428 | %11,4 | %14,3 | -0,45 [-1,88; +0,92] |
| Tz | AVR | 2023 | 201 | %16,4 | %17,4 | -0,42 [-1,57; +0,94] |
| Tz | AVR | 2024 | 147 | %17,0 | %11,6 | +0,64 [-0,60; +1,95] |
| Tz | birlesik | 2023 | 767 | %13,0 | %11,6 | +0,34 [-1,14; +1,43] |
| Tz | birlesik | 2024 | 575 | %12,9 | %13,6 | -0,18 [-1,40; +1,04] |
| Tz | BIST | 2023 | 141 | %8,5 | %17,0 | -1,56 [-3,11; -0,05] |
| Tz | BIST | 2024 | 283 | %13,8 | %12,7 | +0,14 [-1,88; +1,41] |

## Huni, prefix, yeniden üretim

```
{"ABD": {"U1_c2_olay": 1231, "T": 215, "r15_sonlu": 1212, "temiz_esli": 1205, "T_temiz_esli": 211, "r15_yok_donem_sonu": 19}, "AVR": {"U1_c2_olay": 431, "T": 50, "r15_sonlu": 421, "temiz_esli": 396, "T_temiz_esli": 48, "r15_yok_donem_sonu": 10}, "BIST": {"U1_c2_olay": 592, "T": 132, "r15_sonlu": 590, "temiz_esli": 545, "T_temiz_esli": 121, "r15_yok_donem_sonu": 2}}
{"ABD": {"n": 30, "tuttu": 30, "T_say": 7}, "AVR": {"n": 30, "tuttu": 30, "T_say": 4}, "BIST": {"n": 30, "tuttu": 30, "T_say": 10}}
{"birlesik_ust10": 0.15057915057915058, "birlesik_alt10": 0.11969111969111969, "birlesik_n": 259, "abd_fark": 0.001974265889662795, "abd_n": 211, "tuttu": true}
```

Satır dosyası: arastirma_cikti/macd_uyum/kasa_t_satir.csv.gz (sha 09f5bc941ced1acd…; en geç tarih 2024-12-31).

Sınırlar: evren bugün işlem gören hisseler (batanlar yok; sonuç yukarı yanlı). Komisyon / kayma yok. Tek başına alım-satım kuralı değildir.

## Kasa düzeni: YEREL MÜHÜR (resmi KASA açılışı yapılamadı)
- KASA_GIZLI (gizli anahtar) bu oturumda yok; `KASA.py ac` çalıştırılamadı. Ayrıca 2023Q1-Q4 (4a7fbad…) ve 2024Q1-Q4 (32d362…) blokları KART_TUR1 / KART_TUR2 için açılmış olduğundan KASA.py ac, ön kaydı ilk açılıştan sonra (25 Kas) işlenmiş bu hipotez için anahtar olsa da DURURDU. KASA_DEFTERI.md'ye satır YAZILMADI.
- İş tanımındaki izinli alternatif uygulandı: islenmis-veri fce5d94 (KASA 1 / Ç217 kaynağı) geçici açıldı, `python KASA.py muhurle --kesik 2024-12-31` ile mühürlendi: yerel mühür 22efc7f75c6c64f1 (manifest repo dışında, /tmp/kasa_t_yerel); 2025Q1 .. 2026Q4 (8 çeyrek x 3 pazar) açık anahtarla şifreli kaldı ve açılamaz; tam kaynak ve worktree mühürden hemen sonra silindi. Açık kısmın 2022-12-31'e kadarki satırları /tmp/kasa/acik ile hisse hisse aynı (ABD 1361 / 1361, AVR 575 / 575, BIST 475 / 475). Ölçüm yalnız açık kısımdan (en geç 2024-12-31; kasa_kapisi).

## Sonuç sonrası not (sonradan bakma; KARAR DEĞİŞMEZ)
- ÜST10'un şans tabanı %10 değil: temiz eş sayısı N sonlu olduğundan sıra (k / N) ayrık; eşlerle değiştirilebilirlik varsayımında P(sıra >= 0,90) = olay başına (N - tavan(0,9 N) + 1) / (N + 1). Bu olayların eş sayılarıyla şans tabanı: T birleşik %12,0 (ABD %11,6, AVR %13,6); ALT10 tabanı da %12,0. Açık veride T birleşik tabanı %11,6 idi.
- Bu tabana göre: birleşik ÜST10 %15,1, boot alt ucu %11,6 < şans tabanı %12,0. Kuralın (a) maddesi ön kayıtta 0,10 eşiğiyle yazıldığı için kural TUTTU veriyor; şans tabanına göre okunduğunda ÜST10 fazlası boot aralığı içinde sıfırdan ayrılmıyor. Kontrol Tz: ÜST10 %13,0 (tabanı %12,0).
- Ö2'de T ABD FARK +0,20 [-1,63; +1,74], L3O -0,72, güç 0,61 (ÖLÇÜLEMEDİ); AVR medyan -0,94; 2024 birleşik FARK -0,34. Ö2 tarafında T'nin eşlerden ayrıştığını gösteren bir hücre yok.
