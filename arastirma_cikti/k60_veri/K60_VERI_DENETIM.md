# K60 veri denetimi

Yazım zamanı: 2026-11-11 10:50:42 UTC. Üreten: `python K60_veri.py denetle`. Önbellekler değiştirilmedi; getiri hesaplanmadı.

## 1. Manifest (sha256)
- SEC frames (yeni): manifest yok (indirme yapılmamış)
- Yahoo fiyat (yeni): `/tmp/k60_fiyat`; 4.755 dosya (4.722 veri, 33 '404 yok' işareti), 1,36 GB; klasör özeti sha256 `a795410c999b166d8e8e12a20d638b2ad07ec63ec963b5334f0d6abe99470408`; diskle karşılaştırma: AYNI.
Klasör özeti kuralı: ada göre sıralı 'dosya adı:sha256' satırlarının sha256'sı (K59 ön kaydındaki kuralla aynı; K60 ön kaydına bu değerler girer).

## 2. SEC çerçeveleri
İstenen 1.916 çerçeve: yeni önbellekte 0, eski önbellekte (K59 girdisi, yalnız okundu) 206, inmemiş 1.710.
Yeni önbellekteki durumlar: —. 'filed' alanı: eski çeyreklerde (≤ 2019) 0 / 0 dosyada, 2020+ çeyreklerde 0 / 178 dosyada var.
Görülen veri alanları: accn, cik, end, entityName, loc, start, val. EDGAR dizin dosyası: 0.

Şirket sayısı (ayrı CIK), etiket x yıl; çeyreklik ve çeyrek sonu çerçevelerde yılın ortalaması (· = çerçeve yok / inmedi). Dönem dönem ayrıntı: `sec_sayim.csv`.

| etiket | çerçeve | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---|---|---|---|---|---|---|---|
| Revenues | çeyreklik | 2.044 | 1.852 | 1.821 | 1.735 | 1.645 | 1.523 | 1.684 |
| Revenues | yıllık | 2.762 | 2.775 | 2.793 | 2.681 | 2.511 | 2.259 | · |
| RevenueFromContractWithCustomerExcludingAssessedTax | çeyreklik | 2.348 | 2.272 | 2.227 | 2.194 | 2.109 | 2.007 | 2.311 |
| RevenueFromContractWithCustomerExcludingAssessedTax | yıllık | 3.163 | 3.206 | 3.228 | 3.142 | 2.973 | 2.713 | · |
| SalesRevenueNet | çeyreklik | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| SalesRevenueNet | yıllık | 0 | 0 | 0 | 0 | 0 | 0 | · |
| NetIncomeLoss | çeyreklik | 5.009 | 5.117 | 5.097 | 4.694 | 4.417 | 4.228 | 5.020 |
| NetIncomeLoss | yıllık | 6.375 | 6.922 | 6.813 | 6.390 | 6.082 | 5.707 | · |
| StockholdersEquity | çeyrek sonu | 6.206 | 6.751 | 6.626 | 6.128 | 5.808 | 5.589 | 5.238 |
| Liabilities | çeyrek sonu | 5.117 | 5.779 | 5.908 | 5.569 | 5.288 | 5.175 | 4.996 |
| LiabilitiesAndStockholdersEquity | çeyrek sonu | 5.990 | 6.598 | 6.643 | 6.216 | 5.865 | 5.716 | 5.462 |

## 3. Yahoo fiyat kapsamı
Hisse durumu: fiyat 4.678, yok 33, veri yok (kırpık) 22, veri yok 22; kırpık seri 29. Ayrıntı: `fiyat_kapsam.csv`.
