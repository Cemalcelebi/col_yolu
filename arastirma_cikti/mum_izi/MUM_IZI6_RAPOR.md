# MUM_IZI6 RAPOR (2026-11-25T15:18:34Z)

Sürüm: MUM_IZI_ETIKET2 v1.0 (2026-11-25): etiket seti 2 (8 tekrar + 40 katmanlı yeni), T1-T4 ön kayıtlı. Getiri / sonrası yok. Sayfa -> katman / etiket eşlemesi bu dosyada YOK (mühürlü anahtarda).

## SET

- Toplam 48 sayfa + kapak (MUM_IZI6_ETIKET.pdf, 49 sayfa).
- Katman başına sayfa: {'K1': 16, 'K2': 12, 'K3': 6, 'K4': 6, 'T': 8}
- Katman x zaman dilimi: {'K1|gunluk': 8, 'K1|haftalik': 8, 'K2|gunluk': 6, 'K2|haftalik': 6, 'K3|gunluk': 3, 'K3|haftalik': 3, 'K4|gunluk': 3, 'K4|haftalik': 3, 'T|gunluk': 3, 'T|haftalik': 5}
- Katman x pazar: {'K1|ABD': 13, 'K1|AVR': 3, 'K2|ABD': 9, 'K2|AVR': 3, 'K3|ABD': 4, 'K3|AVR': 2, 'K4|ABD': 3, 'K4|AVR': 3, 'T|ABD': 3, 'T|BIST': 5}
- Zaman dilimi: {'haftalik': 25, 'gunluk': 23}; pazar: {'ABD': 32, 'AVR': 11, 'BIST': 5}

## EVREN (evren içi pencere sayısı; pencere = hisse x son x uzunluk)

| zaman / pazar | hisse | pencere | evren içi | K1 | K2 | K3 | K4 |
|---|---|---|---|---|---|---|---|
| gunluk|ABD | 4402 | 29529067 | 19987850 | 129360 | 964900 | 3068882 | 19987850 |
| gunluk|AVR | 571 | 4718320 | 3669515 | 23403 | 179962 | 572107 | 3669515 |
| gunluk|BIST | 467 | 3270077 | 1627157 | 10241 | 75290 | 249485 | 1627157 |
| haftalik|ABD | 4303 | 13410948 | 8720842 | 46413 | 451360 | 1314051 | 8720842 |
| haftalik|AVR | 570 | 2484675 | 1793867 | 9538 | 90314 | 264375 | 1793867 |
| haftalik|BIST | 449 | 646637 | 328451 | 1448 | 17178 | 54022 | 328451 |

- P2 vektörlü maske denetimi (MH.mh_p2 ile): {'gunluk|ABD|acik': {'n': 1999, 'fark': 0, 'p2_pay': 0.5887943971985993}, 'gunluk|AVR|acik': {'n': 1995, 'fark': 0, 'p2_pay': 0.7588972431077694}, 'haftalik|ABD|p1': {'n': 1997, 'fark': 0, 'p2_pay': 0.5232849273910867}, 'haftalik|ABD|acik': {'n': 1998, 'fark': 0, 'p2_pay': 0.5955955955955956}, 'haftalik|AVR|p1': {'n': 1984, 'fark': 0, 'p2_pay': 0.6154233870967742}, 'haftalik|AVR|acik': {'n': 1985, 'fark': 0, 'p2_pay': 0.744080604534005}}
- KASA: 2022-12-31; sha: tarama c53fcd427010, anahtar 12bdea2a22f5, PDF fbf7f448b377

## SONUÇ

- Set hazır: MUM_IZI6_ETIKET.pdf (kapak + 48 bölge). Cemal işaretleyince `python MUM_IZI_ETIKET2.py olc` (işaret dosyası cemal_mum_izi6_etiket.json, şema ön kayıtta) T1-T4'ü önceden yazılı eşiklerle koşar. Bu işte etiket, AUC ya da hüküm YOK.
- Yeni 40 sayfanın hiçbiri BIST değil: seçim katman pencereleri arasında düzgün; BIST evren içi pencerelerin ~%5'i (günlük 1,63 M / 25,3 M; haftalık 0,33 M / 10,8 M), beklenen ~2 sayfa. Tavan (üçte bir) üst sınırdır, alt sınır değil. BIST yalnız tekrar sayfalarında (5).
- Seçilen sayfaların F1 yüzdelikleri katman sınırları içinde (K1 0,0004-0,0048; K2 0,0074-0,049; K3 0,063-0,146; K4 0,19-0,90); en geç pencere sonu 2022-09-16 (<= 2022-12-31); hisseler tekil; seçilen 40 pencerede veri pencere sonunda kesilince F1 aynı (en büyük fark 0); tekrar sayfalarında v1 S MUM_IZI4 anahtarıyla aynı; F1-F3 düz döngüyle aynı (72 sayfa).
- PDF metninde katman / pazar / tarih / hisse yok (pdftotext denetimi: 0 eşleşme); sayfa düzeni MUM_IZI4_ONAY ile aynı fonksiyonlarla (MV._mv_ciz, aynı eksen kutuları ve metinler).

## KONTROL LİSTESİ

Ön kayıttaki K1-K14 (MUM_IZI6_ON_KAYIT.md) gerçekleşti: K2 prefix 40 pencerede 0 fark; K3 / K10 P2 vektörlü maske 6 parçada 2.000'er çiftte MH.mh_p2 ile birebir (fark 0); K4 hisse tekil; K9 e6_kapi taramadan önce geçti (ön kayıt 59a0742); K11 düz döngü ve v1 S denetimi; K12 rapor ve commit mesajlarında eşleme yok; K13 v1 / v2 / v3 / defterler değişmedi.

## HATA

1. (test kurgusu; benim) test_lojistik_cv ilk sürümde zayıf sinyalle (tek girdide +2 sd, 51 girdi) CV AUC 0,735 < 0,75 sınırında kaldı; kod hatası değil, test sinyali +3 sd yapıldı (ön kayıttan önce).
2. (bilgi) 'Sayfa N: bulunan bölge' başlığı rastgele (K4) ve tekrar sayfalarında da aynı: düzen birebir aynı kalsın ve katman sızmasın diye değiştirilmedi; 'bulunan' sözü rastgele sayfalar için tam doğru değil (kapak 'bir kısmı rastgele' diyor).

## SAPMA

- Ön kayıttan ÖNCE kuru koşu: pazar başına 70 hisselik alt evrende, kapı yamalı, /tmp'de uçtan uca (tarama -> seçim -> PDF -> rapor -> SAHTE rastgele etiketle olc). Yalnız kod sınaması; seçimi ve sahte sonucu kullanılmadı (ön kayıtta yazılı).
- Başka sapma yok.

## ÖNERİLEN DEFTER SATIRLARI (ana model işler; eşleme yazılmaz)

- IK_KAYIT Ç232: MUM_IZI EK 6 etiket seti 2 hazır: 48 sayfa (8 tekrar + 40 yeni: K1 16 / K2 12 / K3 6 / K4 6; her katman yarı günlük yarı haftalık; yeni 40'ta pazar ABD 29 / AVR 11 / BIST 0), donmuş V3 F1 katmanlı, katman içi rastgele; evren içi pencere K1 220 bin, K2 1,78 M, K3 5,52 M, K4 36,1 M. Ön kayıt 59a0742 (T1 >= 7 / 8 tutarlı; T2 F1 AUC >= 0,80 ve alt uç >= 0,65 UYUMLU, 0,65-0,80 KISMEN). Getiri yok. Sonuç Cemal'in işaretinden sonra.
- IK_GOREV: 25 Kas, EK 6 etiket seti 2 (kod, ön kayıt, tarama, PDF, mühürlü anahtar); açık: Cemal MUM_IZI6_ETIKET.pdf'i işaretleyecek -> olc.
- IK_ACIK: Cemal MUM_IZI6_ETIKET.pdf (49 sayfa) işaretler; sonra `python MUM_IZI_ETIKET2.py olc` (işaret dosyası şeması ön kayıtta).
