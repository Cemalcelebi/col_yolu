# SD (SANCILI DÜŞÜŞ) KARTI — İŞ TANIMI (ana model, 21 Kasım 2026)

Kaynak: Cemal'in "Çöl Yolu v3, BINBN sancılı düşüş debug" sohbetinden yapıştırdığı kod (BINBN_v4_final_colab.py, olduğu gibi saklandı). Eleştiri ve eşleme: SD_ELESTIRI_VE_ESLEME.md (29 kusur, K1-K14). Yeniden üretim: BINBN_yeniden_uretim_vbist.txt (V_BIST BINBN 510 bar: 10 kutu, 2 SD, ikisi de İHLAL; SD #10 fon krizi döneminde, kural gereği ölçülmez). Kodun indirdiği Drive CSV'si (id 1-eMtoi4bLxeQSwR3gdxxmGKetyvCzugg) bulunamadı; V_BIST fiyatı ham seriden 1,2067 kat (düzeltilmiş), oransal ölçüler aynı.

Bu iş AKTİF DALDA (ccr-27195a1e-djv6v3; CETVEL2 v2.2, KASA, KART_TUR1 yalnız orada) koşulur; kayıt o dalın sıradaki Ç numarasıyla (Ç206) yazılır. Alt ajan iş tanımının başına `python IZ_KARNE.py kontrol istanimi` çıktısı konur. Alt ajan IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md dosyalarına dokunmaz; KART_TUR1 ve SIKISMA_OBEK mühürlü olduğundan onlara kart / sınıf eklenmez.

## 1. Hipotez SD1 (yön '?')
Düşüş sonrası, dip bölgesinde, küçük (H-L) mumlarla HAFİF AŞAĞI sürünen kutu bittikten sonra hisse, aynı gün aynı kovadaki eşlerinden farklı getiri verir. Cemal'in BINBN yorumu '+' (sancılı düşüş yukarı çözülür); Cemal'in C2 / K6 / K40 kuralları ('alçalan dipler güven yok') ve SIKISMA_OBEK satır 4 ('yükselişteki bölge sancılı değil dinlenme olmalı') '-' der. Bu yüzden ön kayıtta yön '?' (iki yönlü), BH q 0,10 m = 2. Projede aşağı eğimli dip kutusu ayrı sınanmadı (S4 |net| <= %3, S5 eğim >= -%2); DS havuzu (87), KART TUR 1 (11) ve hipotez envanterinde yok. Kısmen örtüşen: S5_DİP (Ç184, 60 gün eşli ÖLÇÜLEMEDİ), DS20 alt bantta yürüme (Ç204 R15 SORGULA, yön ters), KT08 düşen bıçak (ÖLÇÜLEMEDİ).

## 2. Tanım (eşikler SABİT; ön kayıttan sonra oynanmaz)
- Geçerli bar: O / H / L / C > 0, H > L, V > 0; her ölçü yalnız t'ye kadarki barlarla.
- Küçük mum (Cemal'in tanımı, COL_v1 MUM_OLCU='aralik'): maske günü u için medyan_{u-9..u}((H-L) / C_önceki) <= 0,75 x ATR250%_u (u-249..u; S5 (a) birimi, k_m 0,75). Gövde ölçüsü (Cemal'in kodu) yalnız SD_GOVDE varyantında BİLGİ.
- Kutu yüksekliği: (maxH - minL) / orta (u-9..u) %2 - %28 (Cemal'in bandı).
- Kutu: ardışık maske günleri; en çok 2 ardışık maske-dışı bar tolere (GAP_TOL 2); bas = ilk maske günü - 9; son = son maske günü; en az 5 maske günü. Kutu birleştirme YOK.
- SD şartları (üçü birden): (i) sl = (C_son - C_son-9) / (orta x 10) < -0,0003 (Cemal; alt sınır yok, 10 barda -%25 de SD sayılır, bu BİLGİ varyantında ayrılır); (ii) dip_yakin = (C_bas - min L_{bas-30..bas-1}) / min L < 0,35 (Cemal); (iii) pslope = OLS eğimi(C_{bas-25..bas-1}) / ortalama < 0 (Cemal'in kod yorumundaki niyet; kodda karara girmiyordu).
- Sinyal günü t = son + 3 (kutunun bittiği gerçek zamanda bilinir); giriş t+1 açılış; aynı hissede yeni olay en az H bar sonra (R15 için 15, R30 için 30); fon krizi kesiği: 31.08.2026 sonrası olay ve pencere yok.
- Negatif kontroller (aynı kod, tek şart farkı): NK1 dip_yakin >= 0,35; NK2 sl >= +0,0003; KUTU (tip şartsız bütün kutular); KT00 momentum kontrolü aynı koşuda (KT00'ı görmeyen cetvel = ÖLÇÜLEMEDİ (cetvel)).
- Varyantlar (BİLGİ): SD_HAFIF (sl >= -0,005), SD_SAVUNMALI (kutu min L >= önceki 30 bar dibi x 0,98), SD_GOVDE (medyan |C-O| / C_önceki, geçmiş 250 gün medyanıyla).

## 3. Cetvel ve karar
- Karar: CETVEL2 v2.2 c2_olc22, R15 ve R30 (giriş t+1 açılış, stop YOK; R45 BİLGİ); konum eşi aynı gün, aynı pazar, ATRP tercil x likidite üçlüsü x F15 çeyreği (>= 5 eş); plasebo kapısı 200 tohum (|FARK| < 0,005, TUTAR payı <= %7).
- Karar hücreleri: ABD ve AVR açık dönem (giriş 2016-01-01 .. 2022-12-31); BIST BİLGİ. Güç: R15 ABD n >= ~325, AVR >= ~208; R30 ABD ~934, AVR ~325 (CETVEL2 güç eğrisi); altında ÖLÇÜLEMEDİ, 'iz değil' denmez.
- Kör ileri test: KASA 2024Q1'den sırayla (2023 blokları KART TUR 1 için 21 Kas 12:57 UTC'de açıldı, 2023 SD için kör değil, BİLGİ); karar bakışı 4 blok (2024Q1-Q4) ve 8 blok (2024Q1-2025Q4); ön kayıt commit'inden önce blok açılmaz.
- BİLGİ ölçüleri: 60 gün eşli (OC.oc_olc) + olasılık tablosu (+%100 / -%50, 250 gün, olay / eş katı); düzeltilmiş sağ ayak (t+1'den 30 bar: kutu altı x 0,99 altında 2 ardışık kapanış = İHLAL, giriş x 1,10 üstünde 2 ardışık kapanış = TUTUNMA, hangisi ÖNCE; olay payı / eş payı); P(+%10 / +%25 / +%50 / +%100) 30 bar (Cemal'in puan basamakları). Dinamik tolerans ve stop ÖLÇÜLMEZ (stop / erken kesme kapalı konu).

## 4. Modül ve sıra
1. SANCILI_DUSUS.py (tek dosya; çakışma kapısı, log, SDHata; test_sancili_dusus.py: geçerli bar, kutu sınırı, SD şartları, sinyal günü son+3, kriz kesiği, tekilleştirme, yapay veride sıfır beklenti).
2. Getirisiz huni sayımı (kutu, SD, NK1, NK2 sayıları; pazar x dönem) -> ön kayıt dosyasına yazılır (beklenen n tahmini: ABD açık 1.000-6.000, AVR 400-2.000, BIST 300-1.500; gerçek sayı ölçümden önce).
3. Ön kayıt (SD_ON_KAYIT.md): tanım, eşik sha, kasa hipotez kimliği SD1, karar kuralı, yeniden üretim hücreleri (SD ABD açık R15, SD AVR açık R30), K1-K14 tablosu (K10, K14 UYGULANMAZ; ötekiler EVET + kanıt) -> commit -> `IZ_KARNE.ik_kontrol_kapisi` -> KASA kapısı -> koşu.
4. Bağımsız denetim: sonnet >= 2 hücre satır verisinden yeniden üretim + sızıntı taraması; iddia (EMARE / ADAY / İZ) çıkarsa opus çürütme.
5. Kayıt (aktif dalın ana modeli): Ç206, görev satırı, IK_ILERI satırı (sonraki test: 2024Q1-Q4 blokları), hata satırları; indeks.

## 5. Çıktılar
arastirma_cikti/sancili_dusus/: SD_ON_KAYIT.md, SD_RAPOR.md, SD_olay_*.csv (satır verisi), SD_huni.csv, denetim raporu. Grafik / kör set yalnız iddia çıkarsa (Cemal'in görme hakkı: kör set 40 sayfa).
