# sektor_AVR.csv — eşleme tablosu (ham Wikipedia sektör adı -> ust = ICB süpersektör)

D9_AVR v1.0 (2026-11-15): D9b sektör rüzgârı AVRUPA'da (sektor_AVR.csv 'ust'), D9_YENIDEN v1.0 + ORTAK CETVEL v1.0. Üretim: `python D9_AVR.py sektor` (islenmis-veri dalı avr/evren_avr_ham.csv + V_AVR.pkl anahtarları). Evren: V_AVR.pkl 581 sembol (ham 692 satırın V_AVR'de olanları: STOXX600 354, FTSE250 227).

Rüzgâr sınıfı sütunu: **ust** (ön kayıtta sabit; ikinci sütunla ikinci koşu yok). BIST 'alt_bist' (~30 sınıf) kabalığına yakın (21 sınıf); ABD 'endustri' daha incedir — fark ön kayıtta yazılır.

## Eşleme (ham ad -> ust)

| ham sektör adı | ust | hisse (V_AVR) | hisse (ham 692) |
|---|---|---|---|
| Automobiles and Parts | Automobiles and Parts | 11 | 14 |
| Banking | Banks | 1 | 1 |
| Banks | Banks | 26 | 31 |
| Basic Resources | Basic Resources | 12 | 14 |
| Industrial Metals and Mining | Basic Resources | 2 | 3 |
| Precious Metals and Mining | Basic Resources | 1 | 1 |
| Chemicals | Chemicals | 18 | 22 |
| Construction | Construction and Materials | 1 | 1 |
| Construction & Materials | Construction and Materials | 6 | 6 |
| Construction and Materials | Construction and Materials | 16 | 21 |
| Engineering and Construction | Construction and Materials | 1 | 1 |
| Consumer Products and Services | Consumer Products and Services | 21 | 27 |
| Consumer Staples | Consumer Products and Services | 1 | 1 |
| Home Construction | Consumer Products and Services | 2 | 2 |
| Household goods & home construction | Consumer Products and Services | 1 | 1 |
| Leisure Goods | Consumer Products and Services | 1 | 1 |
| Personal Goods | Consumer Products and Services | 1 | 1 |
| Alternative Energy | Energy | 1 | 1 |
| Energy | Energy | 10 | 17 |
| Oil & Gas Producers | Energy | 3 | 3 |
| Oil, Gas and Coal | Energy | 1 | 1 |
| Financial Services | Financial Services | 34 | 41 |
| General Financial | Financial Services | 3 | 3 |
| Investment Banking and Brokerage Services | Financial Services | 1 | 1 |
| Beverages | Food, Beverage and Tobacco | 1 | 1 |
| Food Producers | Food, Beverage and Tobacco | 4 | 4 |
| Food and drink | Food, Beverage and Tobacco | 0 | 1 |
| Food, Beverage and Tobacco | Food, Beverage and Tobacco | 15 | 21 |
| Health Care | Health Care | 29 | 39 |
| Health Care Equipment & Services | Health Care | 1 | 1 |
| Pharmaceuticals & Biotechnology | Health Care | 2 | 2 |
| Pharmaceuticals and Biotechnology | Health Care | 1 | 1 |
| Aerospace & Defence | Industrial Goods and Services | 3 | 3 |
| Electronic & Electrical Equipment | Industrial Goods and Services | 3 | 3 |
| General Industrials | Industrial Goods and Services | 2 | 2 |
| Industrial Engineering | Industrial Goods and Services | 3 | 3 |
| Industrial Goods and Services | Industrial Goods and Services | 71 | 83 |
| Industrial Support Services | Industrial Goods and Services | 1 | 1 |
| Industrial Transportation | Industrial Goods and Services | 2 | 2 |
| Industrials | Industrial Goods and Services | 1 | 1 |
| Support Services | Industrial Goods and Services | 9 | 9 |
| Insurance | Insurance | 19 | 27 |
| Life Insurance | Insurance | 1 | 1 |
| Nonlife Insurance | Insurance | 1 | 1 |
| Collective Investments | Investment Trusts | 3 | 3 |
| Equity Investments | Investment Trusts | 3 | 3 |
| Hedge Funds | Investment Trusts | 1 | 1 |
| Investment Trusts | Investment Trusts | 70 | 70 |
| Media | Media | 14 | 21 |
| Food & Drug Retailers | Personal Care, Drug and Grocery Stores | 2 | 2 |
| Personal Care, Drug and Grocery Stores | Personal Care, Drug and Grocery Stores | 5 | 7 |
| Personal Products | Personal Care, Drug and Grocery Stores | 1 | 1 |
| Real Estate | Real Estate | 17 | 19 |
| Real Estate Investment & Services | Real Estate | 2 | 2 |
| Real Estate Investment Trusts | Real Estate | 8 | 8 |
| Retail | Retail | 15 | 20 |
| Retailers | Retail | 11 | 11 |
| Consumer Digital Services | Technology | 1 | 1 |
| Software & Computer Services | Technology | 2 | 2 |
| Software and Computer Services | Technology | 3 | 3 |
| Technology | Technology | 16 | 23 |
| Telecomms | Telecommunications | 2 | 2 |
| Telecommunications | Telecommunications | 15 | 17 |
| Travel & Leisure | Travel and Leisure | 5 | 5 |
| Travel and Leisure | Travel and Leisure | 17 | 19 |
| Travel and leisure | Travel and Leisure | 1 | 1 |
| Electricity | Utilities | 1 | 1 |
| Gas, Water & Multiutilities | Utilities | 1 | 1 |
| Utilities | Utilities | 21 | 25 |

## ust sınıfları (V_AVR evreni)

| ust | üye | not |
|---|---|---|
| Automobiles and Parts | 11 |  |
| Banks | 27 |  |
| Basic Resources | 15 |  |
| Chemicals | 18 |  |
| Construction and Materials | 24 |  |
| Consumer Products and Services | 27 |  |
| Energy | 15 |  |
| Financial Services | 38 |  |
| Food, Beverage and Tobacco | 20 |  |
| Health Care | 33 |  |
| Industrial Goods and Services | 95 |  |
| Insurance | 21 |  |
| Investment Trusts | 77 | işletme değil FON sınıfı; (c) için 'hariç' bilgi sayımı |
| Media | 14 |  |
| Personal Care, Drug and Grocery Stores | 8 |  |
| Real Estate | 27 |  |
| Retail | 26 |  |
| Technology | 22 |  |
| Telecommunications | 17 |  |
| Travel and Leisure | 23 |  |
| Utilities | 23 |  |

- Sektörü boş sembol: 0.
- Not: RUZ_MIN_UYE = 4 'öteki üye' sayısıdır; bir sınıf en az 5 üyeyle rüzgâr üretir. Günlük taze üye sayısı (veri başlangıcı, geçersiz bar) bu sayıdan az olabilir; panel her gün yeniden sayar.

## Wikipedia tamamlamaları (ham csv'de sektör boş)

- ATCO-A.ST: Industrial Goods and Services — en.wikipedia.org/wiki/STOXX_Europe_600 satırı: Atlas Copco | ATCO A | SE0017486889 | Industrial Goods and Services
- ERIC-B.ST: Telecommunications — en.wikipedia.org/wiki/STOXX_Europe_600 satırı: Ericsson | ERIC B | SE0000108656 | Telecommunications
- BT.A.L: Telecommunications — en.wikipedia.org/wiki/STOXX_Europe_600 satırı: BT Group | BT.A | GB0030913577 | Telecommunications (V_AVR'de yok; tabloya girmez)

## Notlar

- 'Investment Trusts': FTSE 250 'Investment Trusts' (70) + fon etiketli 'Equity Investments' (3), 'Collective Investments' (3), 'Hedge Funds' (1) -> tek fon sınıfı (işletme değil fon). ICB'de bunlar Financial Services / Closed End Investments altındadır; iş tanımı gereği ayrı sınıf.
- Etiket isimden: FTSE 250 listesinde bazı fonlar 'Financial Services' (3IN, INPP, SEQI, SOI, PPET), 'General Financial' (GCP, VEIL, VOF) ya da 'Energy' (SEIT) etiketlidir; Man Group (işletme) 'Investment Trusts' etiketlidir. Etikete dokunulmadı (ham ad -> ust tek kural).
- 'Consumer Staples' (tek üye Coats Group, iplik / tekstil) -> Consumer Products and Services (ICB Personal Goods karşılığı).
- 'Home Construction', 'Household goods & home construction', 'Leisure Goods', 'Personal Goods' -> Consumer Products and Services; 'Food & Drug Retailers', 'Personal Products' -> Personal Care, Drug and Grocery Stores; 'Consumer Digital Services' -> Technology; 'Alternative Energy' -> Energy (ICB 2019 yapısı).
- Sektör etiketi BUGÜNKÜ listedir (K2 / K7 sınırı).
