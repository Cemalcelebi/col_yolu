# YAPI_HEDEF — DEVİR 2 RAPORU (karne v2: Y2 web entegrasyon adayları F43-F64 + DEVİR 1 YENİDEN W1 / W2 / W2D)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo. Koşu: 2026-11-19 13:00:22 UTC. Ön kayıt: DEVIR_2_ON_KAYIT.md (2026-11-19 12:51:05 UTC, git 157d22d055). Komut: `python YAPI_HEDEF.py devir2kos`.

**SONUÇ (karar: ABD ve AVR ayrı ayrı; 20 ana satır = 10 aday x 2 kol): KATKI+ 0, KATKI− 1, SORGULA 19.** KATKI+ olanlar: yok.

Ölçü: 1. tur 15 bar cetveli AYNEN, satırlar olay_Y1.csv.gz (yeniden simülasyon yok): n = h5 ve es_h5 olan olay; FARK = ort h5 - ort es_h5 (aynı gün aynı OC kovası eşleri); MARJ = FARK(aday VE kol) - FARK(kol), aynı pazar x hücre (aynı ambargo); stop: ort st5 / ort es_st5. Etiket: KARNE v2 (yalnız 'ana' adaylar): KATKI+ = ABD ve AVR AYRI AYRI, eğitim (2016-22) ve sınama (2023-26, ambargolu) dört hücrenin her birinde n >= 30 VE FARK > 0 VE MARJ > 0 VE MARJ ay kümeli bootstrap %95 alt ucu > 0 VE leave-3-out MARJ > 0 VE st5 olay <= es_st5 eş; ayrıca K1 tabaka şartı; KATKI− = dört hücrede n >= 30 VE MARJ < 0; değilse SORGULA. Ters yön (YÖN 2) hücresi ve 'bilgi' / 'ters' adaylar yalnız BİLGİ (bağımsız sayılmaz). BIST ve ABD+AVR bilgi (tabaka hariç). Değerler yüzde puan; P = 15 barda +%5 hedefin stop'tan önce görülme payı. PP ve RV 'giriş zamanlaması / onay / hacim' kapalı konusuna dokunur (COL_OZET): sonuç yapı ölçüsü olarak raporlanır; KATKI+ çıksa bile üretime / kurala girmeden ana model ve Cemal onayı gerekir.

## 1. Karar tablosu (ana adaylar; her hücre ABD | AVR)

| Aday | Kol | eğitim n / FARK (MARJ; boot alt; L3O) ABD | AVR | sınama n / FARK (MARJ; boot alt; L3O) ABD | AVR | stop olay / eş (eğitim; sınama) ABD | AVR | tabaka | etiket |
|---|---|---|---|---|---|---|---|---|---|
| PP | A | 4191 / -0,4 (+0,9; -0,1; +0,5) | 2172 / +2,0 (+1,5; +0,2; +0,9) | 2770 / -0,5 (-0,3; -1,9; -0,9) | 1020 / -0,3 (+0,8; -1,2; -0,1) | %26,5 / %25,3; %29,4 / %28,4 | %19,0 / %19,7; %20,6 / %19,9 | İŞARET DEĞİŞTİ | SORGULA |
| AY | A | 1811 / -1,1 (+0,2; -1,8; -0,7) | 823 / -1,6 (-2,1; -4,6; -3,3) | 1265 / +0,5 (+0,7; -2,0; -0,8) | 379 / -1,5 (-0,4; -4,4; -2,4) | %29,4 / %25,7; %30,4 / %28,8 | %19,9 / %18,5; %23,0 / %19,5 | İŞARET DEĞİŞTİ | SORGULA |
| AYK | A | 2172 / +1,2 (+2,5; +0,7; +1,8) | 1122 / +3,1 (+2,6; +0,4; +1,5) | 1601 / +1,8 (+1,9; -0,0; +0,5) | 543 / -0,4 (+0,7; -2,7; -0,9) | %30,8 / %26,8; %32,6 / %28,8 | %22,8 / %20,5; %23,9 / %20,1 | İŞARET DEĞİŞTİ | SORGULA |
| DT | A | 1752 / -3,5 (-2,3; -4,5; -3,2) | 1045 / +0,6 (+0,1; -2,0; -0,8) | 1012 / -2,4 (-2,2; -5,0; -3,8) | 568 / -0,6 (+0,6; -3,4; -1,9) | %21,4 / %22,7; %21,7 / %26,1 | %16,6 / %18,2; %17,1 / %19,6 | İŞARET DEĞİŞTİ | SORGULA |
| RV | A | 586 / +3,9 (+5,1; +0,5; +3,4) | 584 / +3,0 (+2,5; -1,0; +1,1) | 292 / -0,6 (-0,5; -6,4; -4,0) | 248 / +7,3 (+8,5; +2,5; +5,3) | %23,9 / %24,0; %30,8 / %30,3 | %20,5 / %19,3; %23,0 / %21,0 | İŞARET DEĞİŞTİ | SORGULA |
| NR7 | A | 1164 / +1,5 (+2,7; -0,1; +1,6) | 612 / +0,8 (+0,3; -2,6; -0,9) | 698 / +4,1 (+4,2; +0,8; +2,4) | 287 / -5,9 (-4,8; -8,7; -7,3) | %24,9 / %26,5; %27,2 / %29,1 | %18,8 / %19,4; %24,0 / %19,4 | İŞARET DEĞİŞTİ | SORGULA |
| VCP | A | 24 / +7,2 (+8,5; -10,4; -1,2) | 12 / +1,3 (+0,8; -25,0; -18,9) | 18 / +7,3 (+7,5; -10,2; -6,1) | 3 / -38,2 (-37,0; -55,5; -46,8) | %33,3 / %28,6; %38,9 / %32,8 | %25,0 / %28,2; %33,3 / %18,7 | tuttu | SORGULA |
| W1 | A | 1977 / -1,1 (+0,1; -1,8; -0,7) | 1060 / +1,7 (+1,2; -1,0; +0,2) | 1175 / +1,4 (+1,6; -0,5; +0,5) | 433 / -0,1 (+1,0; -2,5; -0,5) | %23,9 / %25,1; %24,3 / %26,5 | %19,2 / %19,5; %20,1 / %19,6 | İŞARET DEĞİŞTİ | SORGULA |
| W2 | A | 1750 / -2,9 (-1,6; -3,6; -2,5) | 973 / -0,9 (-1,4; -3,7; -2,8) | 1108 / -2,2 (-2,1; -4,3; -3,0) | 516 / -1,1 (-0,0; -3,9; -2,5) | %21,4 / %22,4; %23,8 / %26,4 | %18,0 / %19,4; %20,7 / %19,6 | İŞARET DEĞİŞTİ | KATKI− |
| W2D | A | 1752 / -0,3 (+1,0; -1,8; -0,0) | 973 / +0,5 (-0,0; -2,4; -1,0) | 1098 / +2,4 (+2,6; -0,3; +1,3) | 500 / +0,6 (+1,8; -2,7; -1,6) | %25,8 / %25,2; %26,0 / %27,3 | %18,4 / %18,7; %22,6 / %20,5 | İŞARET DEĞİŞTİ | SORGULA |
| PP | B | 150 / +6,1 (+3,2; -2,3; +0,9) | 42 / +11,3 (+4,1; -6,8; -3,3) | 153 / +9,0 (+0,8; -4,2; -2,5) | 38 / +13,1 (+4,8; -5,7; -0,8) | %33,3 / %28,8; %30,7 / %32,4 | %26,2 / %20,3; %31,6 / %26,0 | İŞARET DEĞİŞTİ | SORGULA |
| AY | B | 74 / -6,2 (-9,1; -19,1; -14,6) | 10 / -4,9 (-12,1; -45,0; -44,8) | 111 / +10,1 (+1,8; -3,7; -1,4) | 16 / +15,7 (+7,5; -11,4; -7,6) | %47,3 / %29,5; %31,5 / %32,2 | %50,0 / %23,3; %37,5 / %24,1 | İŞARET DEĞİŞTİ | SORGULA |
| AYK | B | 157 / -3,1 (-5,9; -12,1; -7,9) | 41 / +15,1 (+7,9; -3,8; +2,3) | 188 / +9,4 (+1,1; -4,8; -2,2) | 34 / +7,9 (-0,4; -14,5; -6,7) | %43,9 / %29,2; %34,6 / %34,5 | %24,4 / %22,4; %29,4 / %23,1 | İŞARET DEĞİŞTİ | SORGULA |
| DT | B | 24 / -1,4 (-4,3; -24,2; -15,5) | 6 / +37,7 (+30,5; -15,0; -15,6) | 21 / -10,0 (-18,3; -35,8; -31,8) | 5 / -15,1 (-23,4; -47,5; -43,8) | %54,2 / %32,9; %23,8 / %32,5 | %33,3 / %30,0; %40,0 / %33,8 | tuttu | SORGULA |
| RV | B | 18 / +17,0 (+14,2; -8,6; +1,8) | 12 / +15,6 (+8,4; -16,4; -6,2) | 11 / +35,7 (+27,5; +12,7; +15,6) | 5 / +10,5 (+2,2; -48,2; -44,4) | %33,3 / %24,2; %9,1 / %20,8 | %25,0 / %20,2; %40,0 / %28,0 | tuttu | SORGULA |
| NR7 | B | 48 / +7,4 (+4,6; -9,7; -3,9) | 13 / -5,1 (-12,3; -36,4; -31,9) | 60 / +13,3 (+5,1; -5,2; +0,7) | 6 / +6,5 (-1,8; -35,0; -30,2) | %29,2 / %29,6; %31,7 / %33,9 | %46,2 / %14,4; %33,3 / %31,5 | tuttu | SORGULA |
| VCP | B | 0 / - (-; -; -) | 0 / - (-; -; -) | 1 / -7,2 (-15,5; -20,9; -18,4) | 0 / - (-; -; -) | - / -; %100,0 / %72,5 | - / -; - / - | tuttu | SORGULA |
| W1 | B | 53 / +9,7 (+6,9; -4,3; +2,1) | 15 / +4,3 (-2,9; -22,9; -18,0) | 52 / +12,6 (+4,3; -5,4; -1,9) | 5 / -15,9 (-24,2; -53,8; -47,2) | %26,4 / %30,9; %30,8 / %32,0 | %20,0 / %22,2; %60,0 / %27,7 | İŞARET DEĞİŞTİ | SORGULA |
| W2 | B | 37 / +5,3 (+2,5; -10,3; -4,7) | 4 / +35,8 (+28,6; +9,6; +11,1) | 20 / +16,4 (+8,1; -10,2; -1,6) | 9 / +13,1 (+4,8; -31,1; -27,9) | %27,0 / %30,3; %25,0 / %30,8 | %0,0 / %10,2; %11,1 / %22,8 | tuttu | SORGULA |
| W2D | B | 51 / +4,7 (+1,9; -13,7; -5,4) | 15 / +5,2 (-2,0; -29,6; -25,0) | 66 / +3,3 (-4,9; -12,0; -7,9) | 22 / +12,3 (+4,0; -16,6; -8,0) | %39,2 / %27,6; %39,4 / %35,1 | %26,7 / %23,9; %27,3 / %22,7 | İŞARET DEĞİŞTİ | SORGULA |

## 2. İstenen tablo biçimi (aday | kol | eğitim n / fark | sınama n / fark | stop olay / eş | etiket); pazar ABD+AVR havuzu bilgi, etiket ABD / AVR kuralından

| Aday | Kol | Tür | eğitim n / FARK (MARJ) | sınama n / FARK (MARJ) | ters yön n / FARK (MARJ; BİLGİ) | stop olay / eş (eğitim; sınama) | etiket |
|---|---|---|---|---|---|---|---|
| PP | A | ana | 6363 / +0,4 (+1,1) | 3790 / -0,5 (-0,0) | 6124 / +0,4 (+1,0) | %23,9 / %23,4; %27,0 / %26,1 | SORGULA |
| PPq | A | bilgi | 3291 / +1,7 (+2,4) | 1939 / +0,7 (+1,2) | 3226 / +1,6 (+2,2) | %24,0 / %23,0; %27,6 / %26,2 | BİLGİ (SORGULA) |
| PPb | A | bilgi | 2361 / +2,5 (+3,1) | 1422 / +0,2 (+0,7) | 2263 / +2,5 (+3,1) | %24,0 / %23,6; %29,3 / %26,1 | BİLGİ (SORGULA) |
| PPt | A | ters | 6808 / -1,7 (-1,0) | 4093 / -0,4 (+0,0) | 6545 / -1,5 (-0,9) | %23,0 / %23,5; %24,1 / %25,5 | BİLGİ (SORGULA) |
| AY | A | ana | 2634 / -1,2 (-0,6) | 1644 / +0,0 (+0,5) | 2505 / -1,1 (-0,5) | %26,5 / %23,5; %28,6 / %26,7 | SORGULA |
| AYK | A | ana | 3294 / +1,9 (+2,5) | 2144 / +1,2 (+1,7) | 2859 / +2,3 (+2,9) | %28,1 / %24,6; %30,4 / %26,6 | SORGULA |
| AY5 | A | bilgi | 1335 / -0,4 (+0,2) | 801 / -0,4 (+0,0) | 1266 / -0,0 (+0,6) | %26,6 / %23,2; %29,5 / %27,1 | BİLGİ (SORGULA) |
| AY2 | A | bilgi | 524 / +1,5 (+2,1) | 319 / +4,4 (+4,8) | 495 / +2,3 (+2,9) | %27,1 / %23,0; %29,2 / %28,8 | BİLGİ (SORGULA) |
| AYKK | A | bilgi | 684 / +1,5 (+2,2) | 540 / +5,3 (+5,7) | 586 / +2,1 (+2,7) | %30,3 / %24,7; %32,0 / %28,1 | BİLGİ (SORGULA) |
| AYC | A | bilgi | 3294 / -2,1 (-1,4) | 1811 / -0,9 (-0,5) | 3384 / -1,7 (-1,1) | %23,8 / %23,9; %24,6 / %26,1 | BİLGİ (SORGULA) |
| AYT | A | bilgi | 3293 / +0,1 (+0,8) | 1967 / -0,2 (+0,2) | 3129 / +0,0 (+0,6) | %21,7 / %23,3; %23,6 / %25,0 | BİLGİ (SORGULA) |
| AYt | A | ters | 107 / -1,1 (-0,5) | 113 / -3,6 (-3,1) | 106 / -1,9 (-1,3) | %16,8 / %23,0; %20,4 / %28,4 | BİLGİ (SORGULA) |
| DT | A | ana | 2797 / -2,0 (-1,3) | 1580 / -1,7 (-1,3) | 2731 / -2,0 (-1,4) | %19,6 / %21,0; %20,1 / %23,8 | SORGULA |
| DT05 | A | bilgi | 2086 / -2,4 (-1,8) | 1163 / -0,8 (-0,4) | 2038 / -2,4 (-1,8) | %18,5 / %20,8; %19,9 / %23,2 | BİLGİ (SORGULA) |
| DT2 | A | bilgi | 4272 / -2,7 (-2,0) | 2385 / -2,0 (-1,6) | 4181 / -2,6 (-2,0) | %19,0 / %20,8; %19,5 / %23,8 | BİLGİ (KATKI−) |
| DTt | A | ters | 10378 / -0,3 (+0,4) | 6307 / -0,1 (+0,3) | 9942 / -0,2 (+0,4) | %24,5 / %24,1; %26,9 / %26,3 | BİLGİ (SORGULA) |
| RV | A | ana | 1170 / +3,4 (+4,1) | 540 / +3,0 (+3,5) | 1148 / +3,6 (+4,2) | %22,2 / %21,7; %27,2 / %26,0 | SORGULA |
| RVq | A | bilgi | 3292 / +1,3 (+1,9) | 1932 / +0,3 (+0,7) | 3249 / +1,4 (+2,0) | %24,2 / %23,2; %27,1 / %26,2 | BİLGİ (SORGULA) |
| RVt | A | ters | 3909 / -1,9 (-1,3) | 2289 / -1,6 (-1,1) | 3738 / -1,7 (-1,1) | %21,6 / %23,2; %23,0 / %25,3 | BİLGİ (KATKI−) |
| NR7 | A | ana | 1776 / +1,3 (+1,9) | 985 / +1,2 (+1,6) | 1699 / +1,5 (+2,1) | %22,8 / %24,1; %26,3 / %26,3 | SORGULA |
| NR7a | A | bilgi | 317 / +4,7 (+5,4) | 216 / +4,7 (+5,1) | 303 / +4,6 (+5,2) | %30,0 / %24,2; %34,3 / %28,7 | BİLGİ (SORGULA) |
| NR7y | A | bilgi | 1459 / +0,5 (+1,2) | 769 / +0,2 (+0,6) | 1396 / +0,8 (+1,4) | %21,2 / %24,0; %24,1 / %25,6 | BİLGİ (SORGULA) |
| IDNR4 | A | bilgi | 758 / +2,0 (+2,6) | 479 / +2,0 (+2,4) | 734 / +2,0 (+2,6) | %25,1 / %23,5; %24,2 / %25,9 | BİLGİ (SORGULA) |
| NR7t | A | ters | 11399 / -0,9 (-0,3) | 6902 / -0,7 (-0,2) | 10974 / -0,9 (-0,3) | %23,5 / %23,4; %25,4 / %25,7 | BİLGİ (SORGULA) |
| VCP | A | ana | 36 / +5,3 (+5,9) | 21 / +0,8 (+1,2) | 35 / +4,1 (+4,7) | %30,6 / %28,5; %38,1 / %30,8 | SORGULA |
| VCP5 | A | bilgi | 44 / +7,6 (+8,2) | 23 / -2,9 (-2,5) | 43 / +6,7 (+7,3) | %27,3 / %27,0; %39,1 / %30,0 | BİLGİ (SORGULA) |
| VCPt | A | ters | 13139 / -0,7 (-0,0) | 7866 / -0,4 (-0,0) | 12638 / -0,6 (-0,0) | %23,4 / %23,5; %25,5 / %25,8 | BİLGİ (SORGULA) |
| W1 | A | ana | 3037 / -0,1 (+0,5) | 1608 / +1,0 (+1,5) | 3200 / -0,3 (+0,3) | %22,3 / %23,2; %23,2 / %24,6 | SORGULA |
| W1t | A | ters | 3035 / -0,1 (+0,6) | 1994 / -0,6 (-0,2) | 2687 / -0,0 (+0,6) | %23,2 / %23,0; %24,2 / %26,3 | BİLGİ (SORGULA) |
| W2 | A | ana | 2723 / -2,2 (-1,5) | 1624 / -1,9 (-1,4) | 2507 / -1,7 (-1,1) | %20,2 / %21,3; %22,8 / %24,2 | KATKI− |
| W2t | A | ters | 2725 / +1,9 (+2,5) | 1704 / +2,2 (+2,6) | 2560 / +1,5 (+2,1) | %23,0 / %23,0; %26,6 / %25,6 | BİLGİ (SORGULA) |
| W2D | A | ana | 2725 / +0,0 (+0,7) | 1598 / +1,9 (+2,3) | 2708 / -0,2 (+0,4) | %23,2 / %22,9; %24,9 / %25,2 | SORGULA |
| W2Dt | A | ters | 2723 / -2,3 (-1,7) | 1710 / -0,7 (-0,3) | 2384 / -2,3 (-1,7) | %19,9 / %21,1; %23,0 / %24,8 | BİLGİ (SORGULA) |
| taban | A | - | 13175 / -0,6 | 7887 / -0,4 | 12673 / -0,6 | %23,4 / %23,5; %25,5 / %25,8 | - |
| PP | B | ana | 192 / +7,2 (+3,5) | 191 / +9,8 (+1,6) | 179 / +6,9 (+2,7) | %31,8 / %27,0; %30,9 / %31,1 | SORGULA |
| PPq | B | bilgi | 87 / +12,9 (+9,2) | 90 / +5,9 (-2,4) | 84 / +12,5 (+8,3) | %33,3 / %29,1; %35,6 / %30,0 | BİLGİ (SORGULA) |
| PPb | B | bilgi | 69 / +13,1 (+9,3) | 71 / +11,8 (+3,5) | 64 / +13,6 (+9,5) | %34,8 / %28,5; %32,4 / %30,2 | BİLGİ (SORGULA) |
| PPt | B | ters | 243 / +1,0 (-2,8) | 235 / +7,0 (-1,3) | 220 / +1,9 (-2,2) | %35,0 / %28,5; %33,2 / %32,0 | BİLGİ (KATKI−) |
| AY | B | ana | 84 / -6,1 (-9,8) | 127 / +10,8 (+2,6) | 77 / -3,7 (-7,8) | %47,6 / %28,7; %32,3 / %31,2 | SORGULA |
| AYK | B | ana | 198 / +0,7 (-3,1) | 222 / +9,1 (+0,9) | 165 / +0,6 (-3,5) | %39,9 / %27,8; %33,8 / %32,8 | SORGULA |
| AY5 | B | bilgi | 36 / -15,9 (-19,7) | 63 / +11,3 (+3,0) | 33 / -14,5 (-18,6) | %55,6 / %29,1; %31,7 / %31,0 | BİLGİ (SORGULA) |
| AY2 | B | bilgi | 13 / -14,5 (-18,2) | 30 / +14,3 (+6,0) | 10 / -9,2 (-13,3) | %61,5 / %35,8; %33,3 / %31,9 | BİLGİ (SORGULA) |
| AYKK | B | bilgi | 33 / -17,0 (-20,8) | 79 / +12,4 (+4,1) | 29 / -16,1 (-20,2) | %63,6 / %32,0; %32,9 / %32,6 | BİLGİ (SORGULA) |
| AYC | B | bilgi | 130 / +5,8 (+2,0) | 105 / +13,7 (+5,4) | 127 / +6,8 (+2,7) | %33,8 / %29,2; %28,6 / %32,9 | BİLGİ (SORGULA) |
| AYT | B | bilgi | 71 / +12,7 (+9,0) | 63 / +7,7 (-0,6) | 65 / +13,5 (+9,4) | %29,6 / %25,9; %33,3 / %32,2 | BİLGİ (SORGULA) |
| AYt | B | ters | 0 / - (-) | 0 / - (-) | 0 / - (-) | - / -; - / - | BİLGİ (SORGULA) |
| DT | B | ana | 30 / +6,4 (+2,7) | 26 / -11,0 (-19,3) | 30 / +6,4 (+2,3) | %50,0 / %32,3; %26,9 / %32,7 | SORGULA |
| DT05 | B | bilgi | 23 / +4,2 (+0,5) | 15 / -15,6 (-23,8) | 23 / +4,2 (+0,1) | %52,2 / %36,6; %26,7 / %33,9 | BİLGİ (SORGULA) |
| DT2 | B | bilgi | 43 / +10,9 (+7,1) | 38 / -6,4 (-14,7) | 42 / +13,1 (+9,0) | %39,5 / %31,1; %34,2 / %34,5 | BİLGİ (SORGULA) |
| DTt | B | ters | 405 / +3,5 (-0,2) | 400 / +9,5 (+1,3) | 369 / +4,0 (-0,2) | %32,3 / %27,5; %32,5 / %31,5 | BİLGİ (SORGULA) |
| RV | B | ana | 30 / +16,4 (+12,7) | 16 / +27,8 (+19,6) | 28 / +20,5 (+16,3) | %30,0 / %22,6; %18,8 / %23,0 | SORGULA |
| RVq | B | bilgi | 78 / +14,6 (+10,9) | 87 / +7,5 (-0,7) | 77 / +16,0 (+11,9) | %26,9 / %25,4; %33,3 / %29,3 | BİLGİ (SORGULA) |
| RVt | B | ters | 156 / +3,1 (-0,6) | 122 / +7,9 (-0,3) | 142 / +3,5 (-0,6) | %32,7 / %29,5; %30,3 / %30,6 | BİLGİ (SORGULA) |
| NR7 | B | ana | 61 / +4,8 (+1,0) | 66 / +12,7 (+4,5) | 55 / +6,5 (+2,4) | %32,8 / %26,3; %31,8 / %33,7 | SORGULA |
| NR7a | B | bilgi | 27 / +17,8 (+14,0) | 41 / +10,0 (+1,7) | 25 / +19,1 (+15,0) | %22,2 / %24,4; %34,1 / %34,7 | BİLGİ (SORGULA) |
| NR7y | B | bilgi | 34 / -5,6 (-9,3) | 25 / +17,2 (+8,9) | 30 / -4,0 (-8,1) | %41,2 / %27,9; %28,0 / %32,1 | BİLGİ (SORGULA) |
| IDNR4 | B | bilgi | 17 / -5,9 (-9,6) | 25 / +12,7 (+4,4) | 17 / -5,9 (-10,1) | %41,2 / %29,0; %28,0 / %32,0 | BİLGİ (SORGULA) |
| NR7t | B | ters | 374 / +3,6 (-0,2) | 360 / +7,5 (-0,8) | 344 / +3,8 (-0,4) | %33,7 / %28,0; %32,2 / %31,2 | BİLGİ (SORGULA) |
| VCP | B | ana | 0 / - (-) | 1 / -7,2 (-15,5) | 0 / - (-) | - / -; %100,0 / %72,5 | SORGULA |
| VCP5 | B | bilgi | 0 / - (-) | 1 / -7,2 (-15,5) | 0 / - (-) | - / -; %100,0 / %72,5 | BİLGİ (SORGULA) |
| VCPt | B | ters | 435 / +3,7 (+0,0) | 425 / +8,3 (+0,0) | 399 / +4,1 (+0,0) | %33,6 / %27,8; %32,0 / %31,5 | BİLGİ (SORGULA) |
| W1 | B | ana | 68 / +8,5 (+4,8) | 57 / +10,1 (+1,8) | 67 / +5,5 (+1,3) | %25,0 / %29,0; %33,3 / %31,6 | SORGULA |
| W1t | B | ters | 115 / -1,2 (-4,9) | 122 / +2,4 (-5,8) | 97 / +0,8 (-3,3) | %37,4 / %26,7; %36,1 / %33,0 | BİLGİ (SORGULA) |
| W2 | B | ana | 41 / +8,3 (+4,5) | 29 / +15,4 (+7,1) | 38 / +8,0 (+3,8) | %24,4 / %28,3; %20,7 / %28,3 | SORGULA |
| W2t | B | ters | 100 / +8,8 (+5,1) | 123 / +5,6 (-2,6) | 93 / +9,9 (+5,7) | %31,0 / %26,9; %37,4 / %32,3 | BİLGİ (SORGULA) |
| W2D | B | ana | 66 / +4,8 (+1,1) | 88 / +5,6 (-2,7) | 66 / +5,8 (+1,6) | %36,4 / %26,7; %36,4 / %32,0 | SORGULA |
| W2Dt | B | ters | 59 / +6,8 (+3,1) | 42 / +13,9 (+5,6) | 52 / +3,2 (-0,9) | %23,7 / %26,3; %21,4 / %30,1 | BİLGİ (SORGULA) |
| taban | B | - | 435 / +3,7 | 426 / +8,3 | 399 / +4,1 | %33,6 / %27,8; %32,2 / %31,6 | - |

## 3. K1 tabaka (ABD+AVR; ana adaylar; MARJ yüzde puan, n; tabaka T0 / T1 / T2 = alt / orta / üst tercil)

| Aday | Kol | F10 T0 egi | F10 T0 sin | F10 T1 egi | F10 T1 sin | F10 T2 egi | F10 T2 sin | F15 T0 egi | F15 T0 sin | F15 T1 egi | F15 T1 sin | F15 T2 egi | F15 T2 sin | F7 T0 egi | F7 T0 sin | F7 T1 egi | F7 T1 sin | F7 T2 egi | F7 T2 sin |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | A | +1,0 (2376) | +0,8 (1622) | +0,7 (1979) | -0,5 (1026) | +1,1 (2008) | -1,1 (1142) | +2,1 (2058) | -0,3 (1498) | +0,7 (4305) | +0,3 (2292) | - (0) | - (0) | +1,2 (2383) | +0,5 (1373) | +1,2 (2104) | -0,6 (1277) | +0,5 (1876) | -0,2 (1140) |
| AY | A | -0,7 (715) | +0,6 (605) | +1,2 (858) | +1,1 (488) | -1,2 (1061) | +0,0 (551) | -1,2 (727) | +3,1 (655) | +0,1 (1907) | -1,1 (989) | - (0) | - (0) | -1,3 (871) | +0,0 (604) | +0,2 (848) | +0,4 (543) | -0,6 (915) | +0,9 (497) |
| AYK | A | +1,5 (1494) | +0,9 (1115) | +5,0 (917) | +1,5 (562) | -0,3 (883) | +1,3 (467) | +0,5 (1443) | +1,2 (1178) | +3,1 (1851) | +0,4 (966) | - (0) | - (0) | +0,7 (1266) | +0,2 (880) | +2,8 (1048) | +2,8 (670) | +4,2 (980) | +2,0 (594) |
| DT | A | -0,6 (818) | -1,5 (505) | +1,2 (677) | -3,2 (356) | -2,4 (1302) | +1,0 (719) | -2,7 (699) | +4,0 (483) | -0,3 (2098) | -2,7 (1097) | - (0) | - (0) | -1,8 (929) | -0,9 (543) | -1,0 (1119) | -1,1 (624) | -1,3 (749) | -2,6 (413) |
| RV | A | +2,7 (563) | +6,9 (296) | +3,6 (338) | +2,3 (134) | +4,8 (269) | -7,5 (110) | +2,5 (341) | +1,9 (173) | +5,0 (829) | +5,0 (367) | - (0) | - (0) | +6,2 (501) | +7,5 (216) | +0,6 (384) | +2,8 (175) | +4,1 (285) | -2,1 (149) |
| NR7 | A | -0,3 (597) | +0,8 (368) | +3,4 (640) | +4,2 (305) | +2,4 (539) | +0,0 (312) | +2,7 (606) | +1,4 (391) | +1,4 (1170) | +1,9 (594) | - (0) | - (0) | +2,0 (562) | +1,9 (330) | +1,1 (598) | +4,0 (321) | +2,7 (616) | -0,8 (334) |
| VCP | A | +2,9 (14) | +6,2 (14) | +4,7 (15) | -17,0 (5) | +12,7 (7) | +0,4 (2) | -21,2 (9) | -27,0 (4) | +15,6 (27) | +9,5 (17) | - (0) | - (0) | +7,3 (17) | -0,1 (13) | -2,7 (12) | +2,4 (6) | +15,5 (7) | -2,1 (2) |
| W1 | A | +0,7 (832) | +2,0 (557) | +2,0 (950) | +0,8 (459) | +0,0 (1255) | +2,1 (592) | +1,8 (883) | +2,7 (615) | +0,3 (2154) | +1,0 (993) | - (0) | - (0) | -1,1 (899) | +1,3 (540) | +1,9 (1013) | +0,8 (512) | +0,9 (1125) | +2,4 (556) |
| W2 | A | -2,6 (291) | +3,9 (243) | -0,3 (725) | -0,4 (385) | +0,1 (1707) | -1,0 (996) | -0,7 (617) | +2,1 (443) | -1,0 (2106) | -1,6 (1181) | - (0) | - (0) | -0,9 (187) | +4,6 (119) | +0,9 (799) | +0,6 (526) | -1,6 (1737) | -1,7 (979) |
| W2D | A | +1,0 (1168) | +2,1 (764) | +1,5 (686) | +3,9 (363) | -1,5 (871) | +0,7 (471) | -0,5 (940) | +1,9 (703) | +1,2 (1785) | +2,3 (895) | - (0) | - (0) | -0,2 (1793) | +2,7 (1060) | -1,1 (792) | -0,1 (441) | +4,5 (140) | -6,4 (97) |
| PP | B | +6,5 (113) | +0,5 (125) | -4,1 (48) | +7,0 (45) | +3,9 (31) | -4,1 (21) | +3,5 (192) | +1,6 (191) | - (0) | - (0) | - (0) | - (0) | +10,6 (83) | +0,3 (103) | +5,4 (55) | +6,5 (55) | -9,6 (54) | -2,5 (33) |
| AY | B | -13,0 (41) | +4,3 (84) | -3,1 (20) | +2,7 (27) | -11,3 (23) | -8,1 (16) | -9,8 (84) | +2,6 (127) | - (0) | - (0) | - (0) | - (0) | -14,8 (41) | +3,6 (72) | +0,4 (25) | +1,4 (38) | -13,6 (18) | +1,3 (17) |
| AYK | B | -1,2 (124) | +1,7 (151) | -2,9 (53) | -0,0 (55) | -13,6 (21) | -2,5 (16) | -3,1 (198) | +0,9 (222) | - (0) | - (0) | - (0) | - (0) | -5,8 (81) | -1,5 (119) | -4,7 (63) | +4,7 (59) | +2,9 (54) | +2,4 (44) |
| DT | B | +1,4 (17) | -26,6 (13) | -1,7 (6) | -22,6 (5) | +8,1 (7) | -7,5 (8) | +2,7 (30) | -19,3 (26) | - (0) | - (0) | - (0) | - (0) | +4,8 (13) | -12,6 (14) | -11,3 (12) | -35,3 (9) | +30,0 (5) | -1,7 (3) |
| RV | B | +14,7 (22) | +23,8 (12) | +15,3 (6) | +8,0 (4) | -15,1 (2) | - (0) | +12,7 (30) | +19,6 (16) | - (0) | - (0) | - (0) | - (0) | +13,9 (19) | +15,6 (8) | +0,0 (8) | +34,8 (7) | +32,6 (3) | -54,1 (1) |
| NR7 | B | +10,4 (31) | +8,8 (43) | -9,9 (22) | -0,8 (17) | -4,4 (8) | -10,8 (6) | +1,0 (61) | +4,5 (66) | - (0) | - (0) | - (0) | - (0) | -0,7 (23) | +8,4 (34) | +2,2 (18) | +11,1 (19) | +2,3 (20) | -15,6 (13) |
| VCP | B | - (0) | -16,0 (1) | - (0) | - (0) | - (0) | - (0) | - (0) | -15,5 (1) | - (0) | - (0) | - (0) | - (0) | - (0) | -15,0 (1) | - (0) | - (0) | - (0) | - (0) |
| W1 | B | -5,3 (37) | +2,9 (30) | +29,6 (22) | +4,4 (18) | -14,1 (9) | -6,2 (9) | +4,8 (68) | +1,8 (57) | - (0) | - (0) | - (0) | - (0) | +6,1 (33) | +2,7 (27) | +13,9 (19) | +0,2 (14) | -9,6 (16) | +1,5 (16) |
| W2 | B | +1,5 (10) | +10,6 (9) | -2,1 (16) | -2,9 (8) | +12,4 (15) | +9,5 (12) | +4,5 (41) | +7,1 (29) | - (0) | - (0) | - (0) | - (0) | -27,7 (3) | -8,8 (6) | +25,9 (15) | +23,7 (6) | -3,4 (23) | +6,1 (17) |
| W2D | B | -6,4 (38) | +2,5 (62) | +13,9 (19) | -10,5 (19) | +5,9 (9) | -27,5 (7) | +1,1 (66) | -2,7 (88) | - (0) | - (0) | - (0) | - (0) | -0,0 (57) | -1,7 (70) | +1,5 (7) | -10,2 (16) | -9,2 (2) | +38,2 (2) |

## BIST (bilgi)

| Aday | Kol | eğitim n / FARK (MARJ) | sınama n / FARK (MARJ) | ters n / FARK (MARJ) | stop olay / eş |
|---|---|---|---|---|---|
| taban | A | 2588 / -1,2 (-) | 2074 / -0,7 (-) | 2503 / -1,2 (-) | %28,3 / %26,3; %36,5 / %36,0 |
| PP | A | 2265 / -1,2 (+0,1) | 1688 / -0,9 (-0,1) | 2194 / -1,0 (+0,2) | %28,4 / %25,7; %37,2 / %36,5 |
| AY | A | 465 / +0,9 (+2,1) | 638 / -2,2 (-1,5) | 453 / +0,9 (+2,1) | %27,5 / %25,9; %37,9 / %37,1 |
| AYK | A | 647 / -0,9 (+0,3) | 652 / -2,0 (-1,3) | 463 / -3,5 (-2,3) | %29,5 / %27,7; %41,3 / %38,0 |
| DT | A | 396 / -3,2 (-2,0) | 189 / -0,8 (-0,0) | 388 / -3,0 (-1,7) | %24,7 / %23,1; %32,8 / %36,9 |
| RV | A | 1091 / -0,9 (+0,3) | 525 / -1,0 (-0,3) | 1065 / -0,8 (+0,4) | %30,0 / %26,5; %39,6 / %36,8 |
| NR7 | A | 381 / -1,6 (-0,3) | 311 / -2,1 (-1,3) | 369 / -1,7 (-0,5) | %27,3 / %24,6; %40,8 / %37,8 |
| VCP | A | 9 / +8,4 (+9,6) | 14 / -14,3 (-13,6) | 8 / +8,6 (+9,8) | %0,0 / %20,6; %35,7 / %33,0 |
| W1 | A | 572 / -0,4 (+0,8) | 423 / -3,0 (-2,2) | 549 / -1,0 (+0,2) | %29,5 / %26,2; %42,1 / %36,5 |
| W2 | A | 469 / -2,6 (-1,3) | 262 / -2,1 (-1,4) | 530 / -2,0 (-0,8) | %27,5 / %25,1; %29,0 / %32,2 |
| W2D | A | 469 / -7,1 (-5,9) | 309 / -0,0 (+0,7) | 454 / -6,4 (-5,2) | %27,5 / %22,2; %35,9 / %36,2 |
| taban | B | 238 / +0,2 (-) | 357 / +1,9 (-) | 236 / +0,6 (-) | %30,7 / %29,6; %29,1 / %31,2 |
| PP | B | 208 / +1,4 (+1,2) | 296 / +1,7 (-0,2) | 206 / +1,8 (+1,2) | %31,2 / %29,7; %31,8 / %33,1 |
| AY | B | 77 / +6,1 (+5,9) | 129 / -4,4 (-6,3) | 76 / +6,2 (+5,6) | %31,2 / %29,6; %37,2 / %32,5 |
| AYK | B | 101 / +0,2 (+0,0) | 180 / +0,5 (-1,4) | 79 / -5,6 (-6,2) | %27,7 / %29,6; %32,2 / %33,8 |
| DT | B | 33 / -2,6 (-2,8) | 16 / -2,4 (-4,3) | 32 / +0,4 (-0,2) | %36,4 / %29,5; %18,8 / %23,4 |
| RV | B | 112 / +1,4 (+1,1) | 103 / +2,4 (+0,5) | 111 / +2,2 (+1,6) | %35,7 / %30,0; %35,9 / %36,0 |
| NR7 | B | 44 / -5,3 (-5,5) | 52 / +1,7 (-0,2) | 44 / -5,3 (-5,9) | %27,3 / %26,5; %42,3 / %42,8 |
| VCP | B | 0 / - (-) | 0 / - (-) | 0 / - (-) | - / -; - / - |
| W1 | B | 56 / +0,2 (+0,0) | 84 / +4,4 (+2,5) | 55 / -1,2 (-1,8) | %35,7 / %26,3; %34,5 / %35,9 |
| W2 | B | 34 / -12,1 (-12,3) | 21 / +0,5 (-1,4) | 38 / -11,9 (-12,5) | %35,3 / %28,0; %19,0 / %21,6 |
| W2D | B | 43 / +2,8 (+2,6) | 63 / -2,6 (-4,5) | 41 / +5,2 (+4,6) | %30,2 / %28,9; %31,7 / %32,2 |

## YENİDEN ÜRETİM (K11; _yh_d2_yeniden: ham csv + eşik json'ları, düz pandas sorgusu)

| Aday | Kol | Pazar | Hücre | kod n / FARK | yeniden n / FARK | durum |
|---|---|---|---|---|---|---|
| AY | A | ABD | sinama | 1265 / +0,5 | 1265 / +0,5 | TUTTU |
| W2 | B | AVR | egitim | 4 / +35,8 | 4 / +35,8 | TUTTU |

## Notlar

- Evren bugün işlem gören hisseler (hayatta kalma yanlılığı): P olay ve P eş yukarı yanlı; FARK'ta kısmen götürür; RV kesit sırası da bugünün evreniyle.
- ABD / AVR 2023-26 hücreleri önceki turlarda görüldü (bakılmış): KATKI+ en fazla EMARE düzeyi okunur, iz değildir.
- 10 ana aday x 2 kol = 20 karar satırı: BH uygulanmaz (dört hücre + bootstrap + L3O + tabaka ikili kuralı); şansla KATKI+ notu raporda.
- DÜZ TAVAN 6 bar onay gecikmesi: 3-5 günlük küçük yapıyı geç yakalar (son 6 barın tepeleri sayılmaz).
- Kod değişti: Colab'da çalışma zamanını yeniden başlat.

## HATA

- SAPMA (iş tanımı): F-kodları 'F30'dan başla' denmişti; F30-F42 DEVİR 1'in (ozellik_Y1_d1) kodları olduğu için çakışmasın diye yeni ölçüler F43-F64 olarak kodlandı; DEVİR 1 YENİDEN adayları F30 / F31 / F32'yi aynen kullanır (ön kayıtta yazılı).
- SAPMA (iş tanımı): yh_devir_ozellik / yh_devir_kos adları DEVİR 1'e ait (üzerine yazmak DEVİR 1 regresyonunu bozardı); DEVİR 2 fonksiyonları yh_devir2_ozellik / yh_devir2_kos / yh_d2_* adlarıyla eklendi.
- TEST HATASI (koşudan ve ön kayıt commit'inden önce düzeltildi): VCP / ZigZag sentetik testinin beklentisi yanlıştı (pencere başındaki dip pivotu sayılmamış, son daralma hacmi yanlış aralığa konmuştu); kod değişmedi, test düzeltildi; 314 / 314 geçti.
- YORUM / MEKANİK İLİŞKİ: PP (F43 = 1) Y1 olaylarının ABD'de ~%48'inde, BIST'te ~%85'inde tutuyor (Y1 sinyal günü tanım gereği yukarı ve hacimli kırılım mumu); süzgeç ayırt edici değil, MARJ küçük çıkması beklenen mekanik sonuç.
- KAPALI KONU: PP ve RV 'giriş zamanlaması / onay / hacim' kapalı konusuna dokunur; ana model / Cemal onayı alınmadan yalnız yapı ölçüsü olarak koşuldu (ön kayıtta işaretli); ikisi de KATKI+ değil.
- GÜÇ: KOL-B (Y9) AVR tabanı küçük (eğitim 89, ambargolu sınama 72 olay) -> her kol B adayı AVR'de n < 30; karne v2'nin 'ABD ve AVR ayrı ayrı n >= 30' şartı kol B için yapısal olarak sağlanamaz (kol B satırları ÖLÇÜLEMEDİ okunmalı, iz değil sözü kurulmaz).
- GÜÇ: VCP kaynak eşikleriyle çok nadir (ABD+AVR eğitim 36, sınama 21 olay kol A) -> ÖLÇÜLEMEDİ.
- K1 TABAKA: n < 30 tabakada şart uygulanmadı; küçük n'li satırlarda 'tabaka tuttu' görünmesi boştur (bu satırlar zaten n şartından SORGULA). Kol A'da 9 ana adayın hepsinde en az bir tabakada MARJ <= 0 çıktı (İŞARET DEĞİŞTİ).
- BELİRSİZLİK (ön kayıtta sabitlendi): 'leave-3-out' iş tanımında tanımsızdı; 'tek tek çıkarıldığında MARJ'ı en çok düşüren 3 ay birlikte çıkarılır' olarak koşudan önce yazıldı.
- K7 / seçicilik: RV 'günün ilk 20'si' evren büyüklüğüne bağlı (ABD ~1.400 hisse, AVR / BIST ~580) ve kesit evreni bugünün listesi (batanlar yok); pazarlar arası seçicilik farklı.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | olay ve eş olay_Y1.csv.gz'den (aynı giriş günü, aynı OC momentum x likidite kovası, aynı d / hat / hedef / 15 bar takip geometrisi); MARJ kol tabanına göre (Y1 / Y9) aynı pazar x hücre x ambargo; K1 TABAKALI koşulur: her ana aday MARJ'ı F10, F15, F7 tercil tabakalarında (sınırlar devir2_esik.json, 2016-22 getirisiz) ölçülür, n >= 30 tabakada MARJ <= 0 -> SORGULA; mekanik ilişki Spearman tablosu (F3 / F10 / F13 / F15) ön kayıtta; RV kesit sırası aynı gün eşlerinden bağımsız değil (eşler aynı günün hisseleri) -> raporda |
| K2 | geleceğe bakma | EVET | F43-F64 yalnız [.., t] barları (t = sinyal günü kapanışı, giriş t+1 açılış); pivot onayı j+6 <= t; ZigZag yalnız onaylı pivot; yh_d2_bar dizileri t+1'de keser; yh_devir2_ozellik_yaz pazar başına 25 rastgele olayda veri t'de kesilince aynı değer (DURUR) ve panel R (kesit) = olay R (DURUR); kesit evreni o günün geçerli barları (evren_bas sonrası); eşikler getirisiz, ön kayıtta mühürlü |
| K3 | geçerli bar | EVET | geçerli bar süzgeci _yh_hazir (H > L, V > 0, O/H/L/C > 0, kriz kesiği 31.08.2026); pencereler geçerli bar sayımıyla; kesit evreninde o gün geçerli barı olmayan hisse yok; hacim 0 bar veri dizisinde yok |
| K4 | tekilleştirme | EVET | Y1 olayları OC 60 gün tekil (olay_Y1); n = bağımsız olay (h5 ve es_h5 olan); süzgeç yalnız seçer; FARK ortalama, P olay / P eş ayrı |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (olay_Y1 E0); yeni simülasyon yok, satırlar mühürlü olay_Y1 (Y1_OLAY_SHA) |
| K6 | veri birimi | EVET | aynı V_*.pkl tek kip (Yahoo düzeltilmiş); yeni ölçüler oran / pay / sıra / ikili (birimsiz); AVR yerel para ama hepsi hisse içi oran; RV kesit sırası oranla (birimden bağımsız) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batanlar yok): P olay ve P eş yukarı yanlı, FARK'ta kısmen götürür; kesit evreni de bugünün listesi (geçmiş günlerin batan hisseleri sırada yok) -> RV ilk-20 sırası yanlı; rapora yazılır |
| K8 | örneklem ve dönem | EVET | hücre n < 30 SORGULA (ölçülemedi); ABD ve AVR ayrı, eğitim + sınama dört hücre aynı yön şartı; 20 karar satırı BH yok -> şans notu; ABD / AVR 2023-26 önceki turlarda görüldü (bakılmış) -> KATKI+ en fazla EMARE düzeyi; küçük n bulgu değil |
| K9 | ön kayıt | EVET | DEVIR_2_ON_KAYIT.md: YH_ESIK_D2_SHA, YH_ESIK / 6 / 7 / D1 sha, kod / özellik d2 / eşik json d2 / d1 özellik / d1 eşik json / olay_Y1 / olay_Y9 sha + getirisiz huni; yh_d2_kapi hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt commit'i ('DEVİR 2 ön kayıt') koşudan önce; eşik sonuca göre oynanmaz; ikinci koşu DURUR |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV (V_*.pkl) ve mühürlü özellik / olay dosyaları |
| K11 | yeniden üretim | EVET | devir2_sonuc.json + ozellik_Y1_d2.csv.gz + olay_Y1.csv.gz; DEVIR_2_RAPOR.md 'YENİDEN ÜRETİM' iki hücre (AY A ABD sınama, W2 B AVR eğitim) ayrı kodla (_yh_d2_yeniden: düz pandas sorgusu + kendi ambargo hesabı) yeniden üretilir; fark > 1e-12 ise DURUR |
| K12 | ifade | EVET | etiket yalnız karne v2 kuralı (KATKI+ / KATKI− / SORGULA / BİLGİ); 'iz / emare' denmez; FARK yüzde puan; h5 hedef payı (stop'tan önce +%5), getiri değil; sayı ile yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_d2_ / yh_devir2_ / YH_ESIK_D2 / _YH_D2 önekli; DEVİR 1 adları ezilmez); yasak defter dosyalarına, GOZ_ETIKET.py'ye, üretim zincirine dokunulmadı (git diff --stat); e-posta / anahtar taraması (_yh_yaz); push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat'; PP / RV kapalı konuya dokunur -> raporda onay notu |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm ve süzgeç karnesi |

