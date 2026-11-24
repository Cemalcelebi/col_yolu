# MACD_UYUM — U1n RAPOR (Ç218: net derin ikinci dip, Cemal'in görsel düzeltmesi)

Ön kayıt: UYUM_N_ON_KAYIT.md (git ff9a3ba, 2026-11-24 18:20:40 UTC). Hesap ön kayıttan sonra. Betik ana modelin: Ç217 satır dosyası (uyum_satir.csv.gz, sha seçim dosyasıyla aynı) alt kümesi. Hücre hükmü MACD_UYUM ile aynı fonksiyonlar (C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum), plasebo HARİÇ. Sonuç dosyası: uyum_n_sonuc.json.

Doğrulama: aynı betik Ç217 U1 ABD 2016-19'u birebir üretti (n 1279, FARK -0,39, SIRA 0,481, L3O -0,83, güç 1,00, TUTMADI).

## KARAR (önceden yazılı kural): **TUTMADI**
U1n'nin dört karar hücresi de TUTMADI. Güç 0,99-1,00, yani sonuç "ölçülemedi" değil. U1n − U1e farkı yön değiştiriyor.

## Cemal'in işaretleri (UYUM_ORNEK20, 20 rastgele U1 sayfası)
- YANLIŞ 9, DOĞRU 11.
- İki dip arası fark %1'den az olan 6 sayfanın 6'sı YANLIŞ: 1, 2, 3, 13, 17, 19 ('Eşit', 'Eşit seviye', 'Net değil').
- Öteki 3 YANLIŞ başka nedenli:
  - 6: 1. dip yanlış yerde, MACD dipleri daire içine alınmış.
  - 11: 'Net değil'.
  - 15: 'Net değil'; 2. dip tek uzun fitil.
- Yeni kural U1n = U1 VE ikinci dip birinciden en az %1 aşağı. Cemal'le uyumu 16 / 20 (kappa 0,58). Eski kod 20 sayfanın 20'sine VAR demişti; uyumu 11 / 20.
- U1n olayları 4.546 / 5.838 (%78).

## Bulgu (R15 = 15 mum getirisi; FARK = olay − konum eşleri, puan)

| hip | pazar | dönem | n | FARK [%95] | SIRA [alt] | L3O | güç | hüküm | +%5 olay / eş | stop olay / eş | r15 olay / eş |
|---|---|---|---|---|---|---|---|---|---|---|---|
| U1n | ABD | 2016-19 | 974 | -0,22 [-0,94; +0,39] | 0,490 [0,465] | -0,61 | 1,00 | TUTMADI | 46,5 / 45,8 | 34,9 / 30,0 | +1,18 / +1,39 |
| U1n | ABD | 2020-22 | 1539 | +0,08 [-0,61; +0,86] | 0,501 [0,485] | -0,42 | 1,00 | TUTMADI | 48,0 / 48,5 | 40,5 / 39,0 | +1,82 / +1,74 |
| U1n | AVR | 2016-19 | 470 | +0,42 [-0,31; +1,18] | 0,498 [0,465] | -0,20 | 1,00 | TUTMADI | 43,3 / 40,8 | 29,3 / 27,1 | +1,59 / +1,17 |
| U1n | AVR | 2020-22 | 485 | +0,30 [-0,49; +1,16] | 0,518 [0,490] | -0,41 | 0,99 | TUTMADI | 52,9 / 50,1 | 32,8 / 33,0 | +3,45 / +3,15 |
| U1n | BIST (bilgi) | 2016-19 | 503 | +0,63 [-0,81; +2,41] | 0,511 [0,477] | -0,69 | 1,00 | TUTMADI | 41,1 / 43,1 | 38,7 / 38,6 | +0,50 / -0,13 |
| U1n | BIST (bilgi) | 2020-22 | 236 | -1,27 [-3,54; +0,37] | 0,464 [0,425] | -2,42 | 0,78 | ÖLÇÜLEMEDİ | 43,2 / 46,3 | 40,7 / 36,9 | +0,57 / +1,84 |
| U1e | ABD | 2016-19 | 305 | -0,93 [-1,90; +0,10] | 0,452 [0,420] | -1,55 | 0,87 | TUTMADI | 40,5 / 41,8 | 34,8 / 31,4 | -0,44 / +0,49 |
| U1e | ABD | 2020-22 | 354 | +0,12 [-0,86; +1,45] | 0,502 [0,473] | -0,56 | 0,82 | TUTMADI | 49,4 / 47,4 | 34,8 / 38,7 | +1,48 / +1,36 |
| U1e | AVR | 2016-19 | 161 | -0,07 [-0,76; +0,62] | 0,492 [0,447] | -0,47 | 0,80 | ÖLÇÜLEMEDİ | 42,8 / 35,1 | 29,6 / 27,3 | +0,47 / +0,55 |
| U1e | AVR | 2020-22 | 151 | +0,71 [-0,43; +2,12] | 0,531 [0,481] | +0,00 | 0,65 | ÖLÇÜLEMEDİ | 46,7 / 44,9 | 35,3 / 36,5 | +2,30 / +1,59 |

U1n − U1e (FARK farkı, puan): ABD 2016-19 +0,71, ABD 2020-22 -0,04, AVR 2016-19 +0,50, AVR 2020-22 -0,41. Yön karışık: dipler net olunca kazanç tutarlı biçimde artmıyor.

## Cemal'in 20 sayfası (bilgi; n 20, bulgu değil)
| | sayfa | +%5 (15 mum, stoptan önce) | stop | ort r15 olay / eş | eşli fark |
|---|---|---|---|---|---|
| DOĞRU | 11 | %64 | %36 | +2,9 / +3,5 | -0,6 puan |
| YANLIŞ | 9 | %33 | %22 | +2,5 / +0,8 | +1,7 puan |

DOĞRU dedikleri +%5'e daha sık gitti, ama aynı günkü eşlere göre geride kaldı. YANLIŞ dedikleri ise eşlerinin önünde. Göstergeler ters yönde; 20 sayfayla ayrım yok.

## Sınırlar
- Plasebo kapısı alt küme için koşulmadı. Hiçbir hücre öteki şartları geçmediği için karara etkisi yok.
- Evren yalnız bugün işlem görenler. Dipteki olaylarda sonuç yukarı yanlıdır.
- Yalnız açık veri (2016-22). KASA açılmadı.

## Sıradaki 3 deneme (önceden yazılı; koşmak Cemal'in kararı)
1. Uzun fitilli dip dışlama (sayfa 15 itirazı): ikinci dipte alt fitil mum boyunun yarısından büyükse olay yok. Ayrıca ikinci dip kapanışla da birinciden en az %1 aşağı olmalı.
2. MACD dibini MACD'nin kendi en düşük noktasında okumak (sayfa 6 itirazı): fiyat dibinin ±5 barı içindeki MACD minimumu.
3. Teyitli giriş: ikinci dipten sonraki ilk tepenin kapanışla geçildiği gün giriş. Bu "giriş zamanlaması / onay" kapalı konusuna dokunuyor; Cemal izni gerekir.
