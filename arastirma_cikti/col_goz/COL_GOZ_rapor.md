# COL_GOZ — D13 col_dip2 kutularının gözle değerlendirmesi (BIST 2024-26, 21 Ekim 2026)

Soru (Cemal): "Kod binlerce çöl bulmuş, kimi doğru kimi yanlış; sen karar ver, tek tek bak."

Yöntem: COL_TESPIT kazanan varyantının (D13) 2024-26 BIST sinyalleri; her (hisse, dip) için ilk sinyal günü = 1 kutu, 3100 kutu.
Üretim kapısı (col_olc: ≥20 bar, ≤6 ATR) uygulanınca 746 kutu kaldı; hepsi grafikle (dipten 130 bar önce → sinyalden 40 bar sonra) tek tek gözle değerlendirildi.
Grafikler: COL_GOZ_2024_26.pdf (sohbette gönderildi; repoda yok). Kararlar: col_goz_karar_2024_26.csv (sembol, sinyal, bar, yük, yuk_atr, alim, bozulma, ileri60, karar + onc_duz/toplam_duz/onc60/son_konum/kucuk ölçüleri).

## Sonuç
| karar | n | anlamı |
|---|---|---|
| COL | 45 | gerçek çöl bölgesi (düşüş sonrası dipte aylarca küçük mum) |
| SINIR | 105 | çöle benziyor ama kısa (1,5-3 ay) ya da şüpheli |
| KISA | 252 | 1-1,5 aylık sıkışma, "aylarca" değil |
| V | 155 | dip sıçraması, sıkışma yok |
| GENIS | 70 | kutu geniş, mumlar iri |
| TREND | 75 | trend içi düzeltme / raf, dipte değil |
| YUKSELIS | 16 | kutu yükselişin kendisi |
| VERI | 28 | bölünme / boşluk, değerlendirilemez |

Kodun bulduğu 746 kutunun yalnız %6'sı gözle çöl, %14'ü sınır; %80'i çöl değil. 3100 ham kutuya oranlanırsa çöl %1,5.

Kodun sistematik hatası: kutu "son 120 barın dibinden" başlıyor ve ilk şartı sağlayan günde (çoğu 20-40 bar) sinyal veriyor. Cemal'in çölü aylarca sürer; kodun bulduğu
çoğu kutu ya dipten sonraki V sıçraması (155) ya da bir aylık kısa duraklama (252). Gerçek çöllerde (ör. CLEBI, IHGZT, KLMSN, SEYKM, ORGE, YAYLA) düz bölge
kutudan çok önce başlıyor; kod bölgenin yalnız son parçasını işaretliyor.

## COL kutularının sonucu (sonradan bilgiyle, dikkat)
Alım gelme %89 (diğerleri %80), bozulma %4 (diğerleri %17),
60 bar ileri medyan +13.6 (diğerleri +0.1).
UYARI: grafiklerde sinyal sonrası 40 bar da görünüyordu; "çöl" kararım sonraki yükselişten etkilenmiş olabilir. n=45. Bu yüzden iz değil, ölçüm.

## Makineye öğretme denemesi (başarısız)
Gözle ayırdığımı basit ölçülerle yakalamayı denedim: kutu öncesi bant içi düz bar sayısı (toplam_duz), yükseklik (yuk_atr), kapanış konumu (son_konum), mum küçüklüğü (kucuk).
toplam_duz ≥ 60: 294 kutu kalır, COL 24/45 yakalar ama 237 DEĞİL de geçer. Kademeli eklemeler COL'ü de siliyor (+yuk_atr≤5 +son_konum≤0,7 +kucuk≤0,8 → 18 kutu, 5 COL, 9 DEĞİL).
Yani göz kararı bu dört ölçüye indirgenemedi. Doğru yol: ayırıcı ölçü aramak yerine Cemal'in bu 45+105 kutuya "evet/hayır" demesi, sonra o etiketle tespit kuralını yeniden kurmak.

## COL listesi
    sembol      sinyal  bar    yuk  yuk_atr  ileri60
2    A1CAP  2025-05-09   30  0.194     3.62   100.79
4    ACSEL  2026-04-10   28  0.270     4.86    13.57
17    AGYO  2024-10-22   28  0.141     3.70     2.70
41    ALKA  2024-11-13   27  0.079     1.44    21.25
47   ANELE  2026-03-31   20  0.165     4.07   663.92
59   ARTMS  2025-05-16   35  0.233     3.41    15.79
72   ATATP  2025-07-28   24  0.285     5.62    39.88
83   AVHOL  2026-04-27   38  0.184     5.42    -2.55
99   BAYRK  2024-12-06   37  0.308     2.73    -7.90
100  BAYRK  2025-04-15   32  0.205     4.29    23.42
101  BAYRK  2026-04-21   35  0.257     4.82    -7.32
137  BOBET  2026-01-07   56  0.148     4.56    -5.80
149  BURVA  2025-07-25   28  0.183     3.08    73.90
158  CLEBI  2025-12-03  115  0.301     3.37    12.59
212  DURDO  2026-04-15   31  0.233     4.31    23.86
214  DYOBY  2026-04-14   30  0.224     5.79    -9.67
243  ESCAR  2024-02-09   40  0.176     3.75    83.58
245  ESCAR  2025-12-19   27  0.219     5.45    35.50
248   ESEN  2026-04-17   33  0.233     3.96   -18.22
300  HDFGS  2025-07-02   42  0.354     4.03    82.55
303   HKTM  2024-12-26   59  0.156     2.53   -28.81
316  IHAAS  2024-02-05   67  0.283     2.32    -0.56
318  IHGZT  2025-07-11   72  0.198     2.54    21.38
328   INFO  2025-05-14   33  0.189     4.02    93.36
365  KARTN  2024-12-12   42  0.244     5.66     5.65
369  KATMR  2026-04-21   30  0.188     4.49   -17.01
382  KLMSN  2025-07-11   72  0.240     4.82    59.01
391  KNFRT  2026-04-10   28  0.111     2.08     4.94
456  MERCN  2026-02-10   31  0.301     5.23    27.26
457  MERCN  2026-04-16   32  0.258     4.79    34.48
474  MTRKS  2024-12-04   44  0.253     5.69    -4.03
496   ORGE  2026-01-19   64  0.109     2.68     5.98
503   OTTO  2025-04-10   56  0.217     2.54    36.71
510  OYLUM  2025-06-18   55  0.257     5.89    -2.44
526  PAPIL  2025-12-17   42  0.275     5.29   -10.11
572  RAYSG  2025-07-25   26  0.139     2.98    -2.14
592  SANFM  2025-08-05   42  0.770     3.64    -7.72
598  SAYAS  2025-01-07   59  0.224     4.50   -35.92
607  SEYKM  2025-07-02   65  0.276     4.30   148.84
638  TATGD  2024-10-28   32  0.189     4.59   -10.86
642  TEHOL  2026-03-13   27  0.346     2.49    93.56
690  TURGG  2025-06-12   51  0.213     4.02    38.66
717  VRGYO  2025-06-30   38  0.230     4.63    27.72
719  VSNMD  2026-02-24   61  0.209     2.60    -9.78
723  YAYLA  2024-01-15   60  0.305     4.88   282.48
