# K60 veri özeti (indirmelerden sonra elde ne var)

Yazım zamanı: 2026-11-11 10:45:05 UTC. Üreten: `python K60_veri.py ozet`. Yalnız sayım: sinyal ölçülmedi, getiri istatistiği hesaplanmadı.

## 1. Fiyat (Yahoo, günlük, 2010-01-01 .. 2026-08-31)
4.755 sembol istendi; fiyat serisi olan 4.678 (tür: EQUITY 4.673, MUTUALFUND 3, ETF 2); durumlar: fiyat 4.678, veri 44, yok 33. Bölünmesi olan 1.770, temettü olayı olan 1.785 hisse. İndirme: 2026-11-11 06:21:53 UTC → 2026-11-11 06:44:41 UTC, son durum 'tamam', inemeyen 0.
- Manifest: `/tmp/k60_fiyat`; 4.755 dosya (4.722 veri, 33 '404 yok' işareti), 1,36 GB; klasör özeti sha256 `df610ebf8cef28905c0c3f565aeef1e508ddb79c7b0f0c06bc7968c0c634425a`; diskle karşılaştırma: AYNI.

### İlk fiyat gününe göre dağılım
| ilk fiyat günü | hisse | % |
|---|---|---|
| 2010 başı (tam geçmiş) | 1.969 | 42,1 |
| 2010 içinde | 94 | 2,0 |
| 2011 içinde | 54 | 1,2 |
| 2012 içinde | 110 | 2,4 |
| 2013 içinde | 113 | 2,4 |
| 2014 içinde | 146 | 3,1 |
| 2015 içinde | 124 | 2,7 |
| 2016 içinde | 95 | 2,0 |
| 2017 içinde | 141 | 3,0 |
| 2018 içinde | 178 | 3,8 |
| 2019 içinde | 152 | 3,2 |
| 2020 içinde | 248 | 5,3 |
| 2021 içinde | 441 | 9,4 |
| 2022 içinde | 143 | 3,1 |
| 2023 içinde | 137 | 2,9 |
| 2024 içinde | 195 | 4,2 |
| 2025 içinde | 208 | 4,4 |
| 2026 içinde | 130 | 2,8 |

### Yıllara göre fiyat paneli ve uygun evren
Uygun evren kuralı (K59 ile aynı eşikler; her ay sonunda, yalnız o gün ve öncesi bilgiyle): tür EQUITY; en az 252 işlem günü geçmiş;
o günkü fiyat (bölünmeler geri alınmış kapanış) ≥ 2 $; son 20 günün medyan işlem değeri ≥ 1 milyon $; son 5 işlem gününde fiyatı var.

| yıl | fiyat serisi olan | tam yıl (≥ 200 gün) | hisse-gün | uygun evren: ay sonu ort. | en az | en çok | yıl sonu uygun | yıl sonu: işlem gören | geçmişi yeten | fiyat ≥ 2 $ | likit ≥ 1 mn $ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2010 | 2.063 | 1.977 | 507.227 | 100 | 0 | 1.196 | 1.196 | 2.062 | 1.963 | 1.695 | 1.240 |
| 2011 | 2.117 | 2.076 | 527.398 | 1.215 | 1.199 | 1.239 | 1.204 | 2.116 | 2.063 | 1.663 | 1.237 |
| 2012 | 2.227 | 2.141 | 543.970 | 1.219 | 1.190 | 1.243 | 1.233 | 2.226 | 2.116 | 1.753 | 1.270 |
| 2013 | 2.340 | 2.251 | 574.728 | 1.309 | 1.244 | 1.382 | 1.382 | 2.338 | 2.229 | 1.915 | 1.450 |
| 2014 | 2.486 | 2.371 | 609.806 | 1.424 | 1.398 | 1.456 | 1.456 | 2.485 | 2.338 | 2.010 | 1.532 |
| 2015 | 2.610 | 2.501 | 641.568 | 1.500 | 1.456 | 1.532 | 1.522 | 2.609 | 2.487 | 2.080 | 1.601 |
| 2016 | 2.705 | 2.620 | 667.885 | 1.557 | 1.507 | 1.628 | 1.628 | 2.703 | 2.609 | 2.180 | 1.682 |
| 2017 | 2.845 | 2.732 | 695.846 | 1.658 | 1.621 | 1.725 | 1.725 | 2.844 | 2.703 | 2.326 | 1.794 |
| 2018 | 3.024 | 2.888 | 739.156 | 1.744 | 1.714 | 1.784 | 1.756 | 3.023 | 2.844 | 2.388 | 1.854 |
| 2019 | 3.176 | 3.048 | 781.434 | 1.808 | 1.756 | 1.876 | 1.876 | 3.175 | 3.025 | 2.548 | 1.961 |
| 2020 | 3.424 | 3.203 | 826.299 | 1.953 | 1.865 | 2.111 | 2.111 | 3.422 | 3.177 | 2.873 | 2.343 |
| 2021 | 3.864 | 3.543 | 925.445 | 2.256 | 2.212 | 2.307 | 2.302 | 3.863 | 3.427 | 3.229 | 2.607 |
| 2022 | 4.007 | 3.907 | 991.012 | 2.261 | 2.219 | 2.296 | 2.256 | 4.005 | 3.863 | 3.007 | 2.347 |
| 2023 | 4.143 | 4.032 | 1.019.434 | 2.287 | 2.225 | 2.353 | 2.353 | 4.142 | 4.005 | 3.129 | 2.459 |
| 2024 | 4.339 | 4.172 | 1.067.399 | 2.389 | 2.319 | 2.511 | 2.511 | 4.336 | 4.143 | 3.307 | 2.668 |
| 2025 | 4.548 | 4.382 | 1.111.648 | 2.544 | 2.426 | 2.653 | 2.635 | 4.540 | 4.334 | 3.379 | 2.843 |
| 2026 | 4.675 | 0 | 763.642 | 2.690 | 2.653 | 2.745 | 2.718 | 4.666 | 4.482 | 3.568 | 2.923 |

### K60 dönemlerinde uygun evren
| dönem | aylar | ay sayısı | uygun evren ort. | en az | en çok |
|---|---|---|---|---|---|
| KEŞİF | 2016-01 .. 2021-12 | 72 | 1.830 | 1.507 | 2.307 |
| DOĞRULAMA | 2022-01 .. 2023-12 | 24 | 2.274 | 2.219 | 2.353 |
| KASA | 2024-01 .. 2026-08 | 32 | 2.522 | 2.319 | 2.745 |

Not: 252 gün geçmiş şartı yüzünden fiyatı 2010 başında başlayan hisseler ilk kez Ocak 2011'de uygun olur; 2010 satırındaki uygun evren bu yüzden sıfıra yakındır.
12 aylık momentum gibi ölçüler KEŞİF başlangıcı (2016) için fazlasıyla geçmişe sahiptir.

## 2. Temel veri (SEC XBRL frames)
SEC indirmesi HENÜZ YAPILMADI (yeni önbellek boş). Eski önbellekte (K59 girdisi) 206 çerçeve var; inecek 1.710 çerçeve için komut: `K60_SEC_UA='<ad> <iletişim adresi>' python K60_veri.py indir_sec`.
- Manifest: manifest yok (indirme yapılmamış)
Etiket x dönem şirket sayıları: `python K60_veri.py denetle` → `K60_VERI_DENETIM.md` ve `sec_sayim.csv`.

## 3. Bilinen yanlılıklar ve sınırlar
1. **Yalnız yaşayanlar.** Evren, Kasım 2026'da borsa kodu olan şirketlerdir (K57-B evren tablosu + V_ABD). Borsadan çıkan (iflas, birleşme) hiçbir
   şirket yok; Yahoo çıkanların fiyatını vermez. Geriye gidildikçe evren küçülür ve "16 yıl hayatta kalmış" şirketlere yaslanır (yukarıdaki
   tabloda 2011 ile 2026 arasındaki fark bunun ölçüsüdür). Getiriler yukarı yanlıdır; en açık aileler küçüklük, düşük fiyat, sıkıntı (EVREN_SECENEKLERI bölüm 4).
2. **Frames son bildirilen değeri verir.** Bir çeyreğin değeri sonradan düzeltildiyse (yeniden sunum, sınıflama değişikliği) çerçevede düzeltilmiş
   hali durur; o gün bilinen sayı değildir. `accn` alanı da değeri EN SON bildiren başvurudur (çoğu kez bir yıl sonraki karşılaştırmalı tablo).
3. **Başvuru günü (`filed`).** Eski çeyrekler henüz inmedi; eldeki 2020+ çerçevelerde (178 dosya) `filed` alanı olan dosya sayısı 0. Uç ve yanıt şeması bütün dönemlerde aynıdır; indirmeden sonra `denetle` / `ozet` eski çeyrekleri de sayar.
   Frames yanıtında `filed` alanı YOK (alanlar: accn, cik, end, entityName, loc, start, val). 2021+ için bilgi tarihi SEC finansal özütlerinden (`/tmp/secfs`, K57 `_k57_abd_bilgi_tarihleri`) geliyor; 2020 ve öncesi için
   özüt yok. **Yedek kural: bilgi tarihi = çeyrek sonu + 90 gün** (10-Q yasal süresi 40–45 gün, 10-K 60–90 gün; +90 gün çeyrek raporları için tutucudur, küçük
   şirketlerin yıllık raporu için sınırdadır; geç başvuranlarda (NT 10-K / 10-Q) geleceğe bakma riski kalır). Daha iyisi: EDGAR çeyreklik başvuru
   dizini (`indir_sec --dizin evet`; şu an 0 dizin dosyası var) her 10-Q / 10-K'nın gerçek gününü verir.
4. **XBRL'e geçiş takvimi.** XBRL zorunluluğu kademeli geldi: en büyük şirketler 2009 ortası, öteki büyükler 2010 ortası, küçük şirketler 2011 ortasından
   sonra biten dönemler. 2009–2011 çerçevelerinde küçük şirketler yoktur; temel veride tam kapsam fiilen 2011Q2'den, yıllık büyüme ölçülerinde 2012'den başlar.
5. **Nakit akış kalemleri yalnız yıllık** (plan bölüm 2). Çeyreklik OCF, yatırım harcaması, geri alım, ihraç bu veriyle kurulamaz.
6. **Pay sayısı.** Kapak sayfası pay sayısının tarihi çeyrek sonu değildir; çok sınıflı şirketlerde boyutlu bildirildiği için çerçevede olmayabilir
   (yedekler: bilanço pay sayısı, ağırlıklı ortalama pay). Bölünme düzeltmesi Yahoo bölünme olaylarıyla yapılır.
7. **CIK → borsa kodu eşlemesi bugünkü.** `company_tickers.json` bugünün kodunu verir; kod değiştirmiş şirketin eski fiyatı Yahoo'da yeni kod altında
   durur (sorun yok), ama yeniden kullanılmış kodlarda (K54: 9 örnek) fiyat ile temel veri farklı şirketlere ait olabilir.
8. **Yahoo fiyatı.** `close` bölünme düzeltmeli, `adjclose` temettü de düzeltilmiş; düzeltme katsayıları indirme günündeki haliyledir. Tekil hatalı
   günler (sıfır hacim, uç fiyat) temizlenmedi; K59'daki "en büyük tek hisse getirisi" denetimi K60'ta da gerekir.
9. **Fon krizi kesimi.** Okuyucular fiyatı 2026-08-31'de keser (KASA dönemi Ağustos 2026'da biter).
