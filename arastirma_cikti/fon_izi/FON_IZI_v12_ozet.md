# Fon hisseleri: para nerede iz bıraktı? (FON_IZI v1.2, 23 Ekim 2026)

## Kısa cevap
- Para iz bıraktı, ama **fiyat grafiğinde ve göstergelerde değil**. 62 gösterge sinyalinden (RSI, MACD, MFI, CMF, OBV, ADX, Ichimoku, Bollinger, Fibonacci, 15 çeşit uyumsuzluk...) **hiçbiri** BIST+ABD 4 dilimde alım izi vermedi.
- İzler üç yerde: **(1) sahiplik** (fonun payı: OZATD'de Tera %8 → %26), **(2) blok devir günleri** (tek günde dev hacim), **(3) borsanın kendi bayrakları** (olağan dışı fiyat sorusu, VBTS tedbiri, devre kesici).
- Bunlar emir defterinde iz bırakmadan alınabildi, çünkü: kilitli tavanda alım emri kuyrukta bekler, satıcı yoksa hacim yazmaz; paketler önce fon sahiplerince toplanıp sonra fona **tek günde blok** devredildi (savcılık yazısı); ortak payları "borsada işlem gören tipe dönüşüm" + toptan satış ile el değiştirdi.

## Web'de bulunanlar (iddia aşaması, mahkeme kararı yok)
- Savcılık yazısı: hisselerin büyük kısmı fonlar aracılığıyla toplandı; bazı fon sahipleri aynı hisseleri önce bireysel aldı, talep fiyatı yükseltti, sonra hisseler fonlara satıldı ve yeni alım dalgası oluştu. Bazı hisselerde ~100 kat artış. Suç: SPK 107 (piyasa dolandırıcılığı). 217 şüpheli, 56+ tutuklu; 131 fon TEFAS'ta kapatıldı.
- OZATD (Özata Denizcilik): Fatma Betül Sayan Kaya Nisan 2026'da 250 bin lot, eşi 150 bin lot (toplam ~163 mn TL iddiası), Ağustos-Eylül'de sattılar (~2,17 mlr TL); kazanç TMSF'ye iade edildi. Hisse Nisan'da 220-250 TL, 27 Nis-14 May tavan serisi, 14 May 878 TL; **14 Mayıs'ta TLY ve TMV fonları 13 mn lot aldı, Tera Portföy'ün payı %8,14'ten %26,41'e çıktı**; 16 Eyl tepe 5.115 TL.
- Bizim veride OZATD: 30 Nis 15,7 mn lot (kilitli tavan, komşu günler ~0,09 mn), 14 May 13,6 mn lot (önceki 5 gün kilitli tavan). Yani fon alımı **iki günde** yazdı; arada hacim yok.
- Borsada işlem gören tipe dönüşüm: ortakların borsa dışı payları toptan alış satış (TAS) ile satılır hale gelir; KAP'ta ayrı duyuru.

## Fon hisselerinde blok hacim günleri (hacim ≥ 20× önceki 20 gün medyanı, dip → tepe)
| sembol   | tarih      |   r_yzd |   hacim_kat |   kilit_tavan_onceki5 | faz   |
|:---------|:-----------|--------:|------------:|----------------------:|:------|
| ANELE    | 2025-07-29 |     3.7 |        20.3 |                     0 | ERKEN |
| ANELE    | 2026-04-10 |     9.9 |        34.3 |                     0 | KOSU  |
| BIGEN    | 2026-07-23 |    10   |        57.4 |                     0 | KOSU  |
| DURDO    | 2024-09-17 |    -2.4 |        24.6 |                     0 | KOSU  |
| DURDO    | 2024-09-20 |    -5.6 |        22.6 |                     0 | KOSU  |
| DURDO    | 2024-09-25 |    10   |        29.5 |                     0 | KOSU  |
| GUNDG    | 2025-10-22 |     0.6 |        21.7 |                     0 | KOSU  |
| OZATD    | 2026-04-30 |     9.9 |        26.3 |                     2 | KOSU  |
| OZATD    | 2026-05-14 |     9.9 |        27.6 |                     5 | KOSU  |
| PASEU    | 2026-04-29 |    -5.5 |        36.6 |                     0 | KOSU  |
| PASEU    | 2026-04-30 |     8.8 |        24   |                     0 | KOSU  |
| SELEC    | 2026-06-15 |    10   |        35.2 |                     0 | KOSU  |
| SELEC    | 2026-06-19 |     2.1 |        21.1 |                     2 | KOSU  |
| TRHOL    | 2025-01-10 |     0   |       191.6 |                     0 | ERKEN |
| UFUK     | 2025-10-20 |     9.9 |        25.1 |                     0 | KOSU  |

23 hissede yalnız 15 gün, 13'ü ilk 2 kattan SONRA (koşu içinde). Erken uyarı olarak az ve geç.

## Fon hisselerinde gösterge sıklığı (fon / diğer BIST 2024-26; 1 = aynı)
ONCE = dipten önceki 120 bar, ERKEN = dip → ilk 2 kat, KOSU = 2 kat → tepe.
| sinyal            |   ONCE/DIGER |   ERKEN/DIGER |   KOSU/DIGER |
|:------------------|-------------:|--------------:|-------------:|
| rsi_70_ustu       |         1.26 |          1.73 |         4.53 |
| cci_100_ustu      |         0.74 |          1.5  |         1.66 |
| mfi_80_ustu       |         1.25 |          1.78 |         2.91 |
| cmf_pozitif       |         1.55 |          1.3  |         2.77 |
| bb_ust_kirilim    |         0.76 |          1.6  |         1.85 |
| fib_618_bolge     |         1.4  |          0.77 |         0.3  |
| blok_hacim        |         1.58 |          1.15 |         2.43 |
| kilit_tavan       |         2.4  |          2.4  |         5.4  |
| uy_rsi_boga       |         0.99 |          0.82 |         0.35 |
| uy_obv_boga       |         1.1  |          0.77 |         0.65 |
| uy_mfi_boga       |         0.89 |          0.69 |         0.45 |
| kap_vbts_tedbir   |         1.48 |          1.13 |         3.03 |
| kap_tipe_donusum  |         1.6  |          0.8  |         1.02 |
| kap_toptan        |         0.83 |          2.41 |         8.06 |
| kap_olagan_disi   |         0.86 |          1.88 |         4.49 |
| kap_fiili_dolasim |         1.86 |          1.35 |         5.95 |

Okuma: ERKEN'de görülen RSI>70, MFI>80, Bollinger üst kırılım, kilitli tavan = yükselen hisse görüntüsü (momentum). Dipten önce boğa uyumsuzluğu diğer hisselerle aynı (0,9–1,15). Borsa bayrağı (olağan dışı, VBTS) fon hisselerinin çoğunda dipten 1,4–2 kattayken geldi; sonra 10–170 kat daha gittiler.

## Evren testi (BIST 581 + ABD 1411 hisse, 2016-21 / 2022-26; kat = sinyal / her 5. gün)
Yukarı sinyallerde kat_k20 = 60 bar içinde önce +%20; aşağı sinyallerde kat_dus = 60 bar içinde önce −%20. İz = 4 dilimde ≥ 1,3.
| sinyal                 | yon    |   dilim |   n_min |   kat_k20_min |   kat_k20_ort |   kat_x2_min |   kat_dus_min |   kat_dus_ort | iz    |
|:-----------------------|:-------|--------:|--------:|--------------:|--------------:|-------------:|--------------:|--------------:|:------|
| blok_taban             | asagi  |       4 |      80 |          0.32 |          1.05 |         0.51 |          1.63 |          2.06 | True  |
| kap_olagan_disi        | asagi  |       2 |    1082 |          0.97 |          0.97 |         0.93 |          1.49 |          1.57 | False |
| kap_vbts_tedbir        | asagi  |       2 |    2437 |          0.93 |          0.95 |         0.98 |          1.34 |          1.37 | False |
| kap_devre_kesici       | asagi  |       2 |    8004 |          0.93 |          0.99 |         0.94 |          1.17 |          1.26 | False |
| kap_tipe_donusum       | asagi  |       2 |    2495 |          0.92 |          0.93 |         0.93 |          1.14 |          1.22 | False |
| force_guclu            | yukari |       4 |   17417 |          1.05 |          1.14 |         1.03 |          1.05 |          1.16 | False |
| cmf_negatif            | asagi  |       4 |   18951 |          0.96 |          1.03 |         0.95 |          1.01 |          1.05 | False |
| obv_lider              | yukari |       4 |    5376 |          1.01 |          1.1  |         1.04 |          1.06 |          1.15 | False |
| kap_spk_yasak          | asagi  |       2 |    1101 |          1.02 |          1.05 |         1.01 |          1    |          1.2  | False |
| tenkan_kijun_kesme     | yukari |       4 |   11952 |          1    |          1.01 |         0.99 |          0.94 |          0.97 | False |
| kap_pay_alim_satim     | yukari |       2 |    2408 |          1    |          1.02 |         0.99 |          1.11 |          1.13 | False |
| rsi_50_kesme           | yukari |       4 |   14440 |          0.99 |          1    |         0.96 |          0.97 |          0.99 | False |
| macd_al_sifir_alti     | yukari |       4 |    9251 |          0.98 |          1.02 |         0.91 |          0.94 |          1.01 | False |
| bb_alt_kirilim         | asagi  |       4 |    8938 |          0.85 |          0.97 |         0.91 |          0.97 |          1.04 | False |
| macd_sifir_kesme       | yukari |       4 |    7853 |          0.97 |          1.02 |         0.95 |          0.88 |          0.95 | False |
| kap_soylenti           | yukari |       2 |     276 |          0.96 |          0.99 |         0.85 |          1.12 |          1.12 | False |
| rsi_70_ustu            | asagi  |       4 |    8098 |          0.86 |          1.02 |         0.93 |          0.96 |          0.99 | False |
| mfi_80_ustu            | asagi  |       4 |    8973 |          0.93 |          1.02 |         1.07 |          0.96 |          1.03 | False |
| stoch_20_donus         | yukari |       4 |   15926 |          0.96 |          1.01 |         0.95 |          1.02 |          1.03 | False |
| bb_sikisma             | yukari |       4 |   10626 |          0.95 |          0.97 |         0.82 |          0.86 |          0.93 | False |
| uy_obv_boga            | yukari |       4 |    4837 |          0.95 |          0.99 |         0.86 |          0.98 |          1.03 | False |
| uy_macd_gizli_boga     | yukari |       4 |    5257 |          0.94 |          0.99 |         0.95 |          0.9  |          0.99 | False |
| bulut_ustu_kesme       | yukari |       4 |    7958 |          0.94 |          1    |         0.91 |          0.9  |          0.95 | False |
| uy_cmf_gizli_boga      | yukari |       4 |    5435 |          0.94 |          0.98 |         0.93 |          0.9  |          0.99 | False |
| uy_mfi_gizli_boga      | yukari |       4 |    5056 |          0.93 |          0.98 |         0.92 |          0.89 |          0.99 | False |
| fib_618_bolge          | yukari |       4 |    4344 |          0.93 |          0.98 |         0.89 |          1.01 |          1.13 | False |
| uy_obv_gizli_boga      | yukari |       4 |    2525 |          0.93 |          0.98 |         0.89 |          0.92 |          0.95 | False |
| fib_dip_bolge          | yukari |       4 |    5747 |          0.93 |          1.11 |         0.97 |          0.75 |          1.14 | False |
| altin_kesisim          | yukari |       4 |    1773 |          0.93 |          0.99 |         1.05 |          0.93 |          0.94 | False |
| fib_382_bolge          | yukari |       4 |    6139 |          0.92 |          0.96 |         0.83 |          0.91 |          1.08 | False |
| uy_macd_boga           | yukari |       4 |    4027 |          0.92 |          1    |         0.83 |          0.97 |          1.02 | False |
| squeeze_yukari_cozulme | yukari |       4 |    5616 |          0.92 |          0.99 |         0.99 |          0.85 |          0.95 | False |
| cci_100_ustu           | yukari |       4 |   12581 |          0.92 |          1.02 |         0.96 |          0.92 |          0.95 | False |
| bb_ust_kirilim         | yukari |       4 |   12358 |          0.91 |          1.03 |         0.95 |          0.94 |          0.96 | False |
| kap_piyasa_yapici      | yukari |       2 |     103 |          0.91 |          1    |         0.65 |          0.61 |          0.73 | False |
| uy_rsi_gizli_boga      | yukari |       4 |    3924 |          0.91 |          0.96 |         0.84 |          0.89 |          1.02 | False |
| uy_rsi_boga            | yukari |       4 |    2786 |          0.91 |          1.04 |         0.81 |          0.9  |          0.99 | False |
| uy_mfi_boga            | yukari |       4 |    3988 |          0.91 |          1.02 |         0.84 |          0.93 |          1.02 | False |
| aroon_yukari           | yukari |       4 |   13132 |          0.91 |          1.01 |         0.91 |          0.89 |          0.93 | False |
| uy_cmf_boga            | yukari |       4 |    4448 |          0.9  |          1.02 |         0.86 |          0.91 |          1    | False |
| cmf_pozitif            | yukari |       4 |   11359 |          0.9  |          0.99 |         0.91 |          0.95 |          0.99 | False |
| adx_25_trend           | yukari |       4 |    5401 |          0.9  |          1.01 |         0.97 |          0.81 |          0.93 | False |
| uy_cmf_ayi             | asagi  |       4 |    5297 |          0.95 |          0.99 |         0.9  |          0.89 |          0.96 | False |
| wr_80_alti             | yukari |       4 |   17288 |          0.89 |          0.99 |         0.94 |          1.04 |          1.04 | False |
| uy_rsi_ayi             | asagi  |       4 |    3688 |          0.92 |          0.98 |         0.77 |          0.89 |          1.01 | False |
| mfi_20_alti            | yukari |       4 |    4490 |          0.89 |          1.04 |         0.9  |          0.97 |          1.12 | False |
| rsi_30_alti            | yukari |       4 |    4545 |          0.88 |          1.04 |         0.86 |          0.92 |          1.08 | False |
| kap_fiili_dolasim      | yukari |       2 |     528 |          0.88 |          0.99 |         0.88 |          1.33 |          1.44 | False |
| uy_macd_ayi            | asagi  |       4 |    4485 |          0.94 |          0.99 |         0.91 |          0.87 |          0.95 | False |
| blok_tavan             | yukari |       4 |      80 |          0.87 |          1.22 |         0.64 |          1.43 |          1.72 | False |
| uy_mfi_ayi             | asagi  |       4 |    4606 |          0.92 |          0.98 |         0.84 |          0.86 |          0.98 | False |
| uy_obv_ayi             | asagi  |       4 |    1935 |          0.96 |          0.98 |         0.84 |          0.86 |          0.95 | False |
| cci_100_alti           | yukari |       4 |   10066 |          0.85 |          0.96 |         0.9  |          1    |          1.04 | False |
| ulcer_sakin_trend      | yukari |       4 |    8812 |          0.81 |          0.98 |         0.64 |          0.79 |          0.82 | False |
| kap_toptan             | yukari |       2 |      72 |          0.8  |          0.87 |         0.98 |          1.27 |          1.3  | False |
| blok_hacim             | yukari |       4 |     284 |          0.78 |          1.02 |         0.86 |          1.08 |          1.36 | False |
| ad_birikim_yatay       | yukari |       4 |    1236 |          0.74 |          0.86 |         0.76 |          0.78 |          0.88 | False |
| fib_tepe_bolge         | asagi  |       4 |    5730 |          0.74 |          0.99 |         0.59 |          0.7  |          0.91 | False |
| kilit_tavan            | yukari |       4 |      39 |          0.3  |          1.06 |         0.65 |          1.01 |          1.94 | False |
| blok_seri_ici          | yukari |       4 |       1 |          0    |          1.64 |         0    |          0    |          2.04 | False |

## Sonuç
- Alım izi: YOK. Göstergeler, uyumsuzluklar ve Fibonacci evrende yazı-tura (kat ~1,0).
- Tek 4 dilim geçen: **blok hacimli taban günü** → sonraki 60 günde −%20 olasılığı 1,6–2,9 kat (A14, ADAY; BIST 2022-26'da n=80).
- BIST-yalnız risk bayrağı: **olağan dışı fiyat sorusu / VBTS tedbiri** → −%20 olasılığı 1,3–1,6 kat, yukarı etkisi yok (A15, ADAY). Fon hisselerinde bu bayrak koşunun başında geldiği için alım işareti değil.
- Gerçek iz sahiplik verisinde: fonların aylık portföy raporları (KAP/TEFAS) ile her hissede fon payı ve artışı. Elimizdeki fon_holdings.csv 24 fon × 11 ay; 2020-26 geçmişi kurulursa "fon payı hızla artan hisse" test edilebilir. Bu ayrı bir veri toplama işi.
- Üretim değişmedi.

## Kaynaklar
- Savcılık yazısı ve mekanizma: https://ntv.com.tr/turkiye/fon-sorusturmasini-baslatan-yazi-ortaya-cikti-1742881 , https://www.istiklal.com.tr/gundem/fon-sorusturmasinin-fitilini-atesleyen-gizli-spk-yazisi-ortaya-cikti-1105970h
- OZATD alım-satım ve fon payı: https://www.ekonomigazetesi.com/kose-yazisi/400-bin-lotun-arkasindaki-yatirim-akli-ne-89361 , https://haber.sol.org.tr/haber/ekonomim-fatma-betul-sayan-kaya-hisse-vurgunundan-elde-ettigi-22-milyar-lirayi-iade-etti , https://halktv.com.tr/turkiye/son-dakika-fatma-betul-sayan-kayanin-fon-sorusturmasindaki-ifadesi-ortaya-cikti-1060160h
- SPK suç duyuruları: https://medyascope.tv/2026/10/17/fon-sorusturmasi-spkdan-37-kisi-hakkinda-suc-duyurusu-karari/ , https://www.ntv.com.tr/ntvpara/spkdan-38-kisi-hakkinda-suc-duyurusu-1742242
- Soruşturma kapsamı: https://www.ntv.com.tr/turkiye/fon-sorusturmasinda-yeni-operasyon-34-gozalti-karari-1744195 , https://tr.euronews.com/business/2026/09/17/turk-piyasalarinda-fon-skandali-tam-olarak-ne-oldu-ve-sirketler-neyle-suclaniyor
- Tipe dönüşüm / TAS: https://www.ekonomist.com.tr/kap-haberleri/borsada-islem-goren-tipe-donsm-duyurusu/243243
