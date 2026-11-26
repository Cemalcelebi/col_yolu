# MUM_IZI16 RAPOR — ölçek: sayfadaki 'küçük mum' gerçekte küçük mü; gerçek mum boyu sonrasını ayırıyor mu (İŞ A)

Etiket: **BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK**. Sınır: Cemal sonrasını gördü ve gerçek grafiğe yalnız gitmeyenlerde baktı -> sonrası tablosu GERİYE DÖNÜK; eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240).

- Kod commit'i: 9b96b3bcd6da962492df8b7f74103611b26d51a4 (test_mum_izi13.py 18 / 18).
- Ön kayıt: 3695c21fd57f481212ea5e9b887216434922d352 2026-11-26T12:15:51+00:00 (kapı geçti: ik_kontrol_kapisi + sha + temiz ağaç); sonrası hesabı bundan sonra (`python MUM_IZI_GOZ2.py olcek`).
- Çıktılar: mum_izi16_sonuc.json, mum_izi16_olay.csv (128 satır; sha 6bfb9ae9741e05d4…). PDF yok.

## KONTROL LİSTESİ

Ön kayıttaki tablo (K1-K13 EVET, K14 UYGULANMAZ) aynen geçerli; koşu sonrası denetim:
- K2: ölçüler bölge sonunda kesik diziden; sentetik testte sonraki barlar 3,7 kat değiştirildi, ölçüler ve sayfa y sınırları birebir aynı kaldı. 120 bar penceresi bölgeyi içermiyor (test: bölge barı öncesine girmiyor; 121. önceki bar dışarıda, 120. içeride). A1 ve grup sayımı csv'nin yalnız getirisiz sütunlarıyla (usecols) üretildi.
- K9: ön kayıt commit zamanı 12:15:51Z; sonrası koşusu ondan sonra; grup / eşik / ana ölçü değişmedi.
- K10: notlu on sayfa PDF başlığından okundu ve csv set5 satırlarıyla birebir eşleşti (TRMET, SLDB, TOON, SIG, SANM, NCMI, ALNY, EBAY, EFOR, IESC); sayfa y sınırı yeniden üretimi gerçek sayfa fonksiyonuyla (HAKEM._hk_sayfa) bir set5 bölgesinde ve sentetikte birebir; set3 formülü (V5) sentetikte birebir.
- K11: bağımsız pandas koduyla EVET|BOY_OZ günlük ve haftalık iki yarısı (n, eşli fark ort / medyan, artıda payı, eşinden iyi payı) ve HEPSI|BOY_MUTLAK|haftalık KÜÇÜK yeniden üretildi: birebir. BOY_MUTLAK / BOY_OZ iki bölgede (SANM günlük, SLDB haftalık) düz döngüyle ham veriden yeniden hesaplandı: birebir.
- K8: bütün yarılar n < 30 (EVET yarıları 8-10): örneklem yetersiz; aile içi BH bilgi.

## HATA

- H1 (süreç, kendi yakaladım, commit öncesi düzeltildi): test taslağında bir assert `... or True` ile boş kalmıştı (120. önceki barın pencereye girdiğini sınamıyordu); commit'ten önce anlamlı sınamayla değiştirildi. Sonuca etkisi yok.
- H2 (veri sınırı, hata değil ama not): EVET haftalık iki bölgede (INMD 2020, TRMET 2016) bölgeden önce 40'tan az hafta var (37, 32): BOY_OZ / SON_BOY_OZ boş; EVET haftalık BOY_OZ yarıları 9 + 9 = 18 bölge (iş tanımındaki 20 değil).
- Başka hesap / veri hatası bulunmadı.

## SAPMA

- Yok. Ön kayıt anında yazılmış yorum notu: iş tanımının 'aile: 5 ölçü x 2 zaman' sayımına uymak için SISME A2 dışında, A1'de olgu.

## SONUÇ

### A1 OLGU (getirisiz)

| ilişki | zaman | n | Spearman rho | p |
|---|---|---|---|---|
| BOY_SAYFA~BOY_MUTLAK | birlikte | 128 | -0,051 | 0,5689 |
| BOY_SAYFA~BOY_OZ | birlikte | 126 | -0,023 | 0,7988 |
| BOY_SAYFA~BOY_MUTLAK | gunluk | 66 | -0,069 | 0,5813 |
| BOY_SAYFA~BOY_OZ | gunluk | 66 | +0,061 | 0,6260 |
| BOY_SAYFA~BOY_MUTLAK | haftalik | 62 | -0,349 | 0,0055 |
| BOY_SAYFA~BOY_OZ | haftalik | 60 | -0,146 | 0,2648 |

- Sayfada küçük (BOY_SAYFA <= 0,0664) ama kendi geçmişine göre büyük (BOY_OZ >= 1,217): **14 / 126 bölge** (EVET|gunluk 1, EVET|haftalik 4, HAYIR|gunluk 4, HAYIR|haftalik 2, KISMEN|gunluk 1, KISMEN|haftalik 2).

| ölçü | zaman | medyan EVET | medyan HAYIR | fark | Mann-Whitney p |
|---|---|---|---|---|---|
| BOY_MUTLAK | gunluk | 3,377 (n 16) | 2,539 (n 40) | +0,838 | 0,3597 |
| BOY_OZ | gunluk | 0,839 (n 16) | 1,065 (n 40) | -0,225 | 0,0045 |
| SON_BOY_OZ | gunluk | 0,815 (n 16) | 1,044 (n 40) | -0,229 | 0,0103 |
| BOY_BANT | gunluk | 0,198 (n 16) | 0,196 (n 40) | +0,001 | 0,7926 |
| BOY_SAYFA | gunluk | 0,065 (n 16) | 0,100 (n 40) | -0,036 | 0,0108 |
| SISME | gunluk | 2,949 (n 16) | 1,764 (n 40) | +1,184 | 0,0431 |
| BOY_MUTLAK | haftalik | 10,284 (n 20) | 7,786 (n 36) | +2,498 | 0,3973 |
| BOY_OZ | haftalik | 1,137 (n 18) | 1,207 (n 36) | -0,070 | 0,6398 |
| SON_BOY_OZ | haftalik | 1,038 (n 18) | 1,064 (n 36) | -0,025 | 0,9634 |
| BOY_BANT | haftalik | 0,205 (n 20) | 0,195 (n 36) | +0,010 | 0,1795 |
| BOY_SAYFA | haftalik | 0,073 (n 20) | 0,105 (n 36) | -0,032 | 0,0025 |
| SISME | haftalik | 2,384 (n 20) | 1,633 (n 36) | +0,751 | 0,0445 |
| BOY_MUTLAK | birlikte | 5,311 (n 36) | 4,524 (n 76) | +0,787 | 0,2049 |
| BOY_OZ | birlikte | 1,004 (n 34) | 1,075 (n 76) | -0,071 | 0,2252 |
| SON_BOY_OZ | birlikte | 0,917 (n 34) | 1,051 (n 76) | -0,134 | 0,0847 |
| BOY_BANT | birlikte | 0,201 (n 36) | 0,196 (n 76) | +0,006 | 0,4834 |
| BOY_SAYFA | birlikte | 0,065 (n 36) | 0,104 (n 76) | -0,038 | 0,0001 |
| SISME | birlikte | 2,660 (n 36) | 1,706 (n 76) | +0,955 | 0,0046 |

KISMEN medyanları ön kayıtta (sınıf tablosu).

Cemal'in not yazdığı on bölge (R15 ve eşli fark yalnız burada, sonradan eklendi):

| s. | sınıf | sembol | zaman | BOY_MUTLAK % | BOY_OZ | SON_BOY_OZ | BOY_BANT | BOY_SAYFA | SISME | R15 | eşli fark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | EVET | TRMET | haftalik | 10,00 | - | - | 0,14 | 0,042 | 5,88 | -0,433 | - |
| 5 | EVET | SLDB | haftalik | 18,52 | 1,11 | 1,04 | 0,20 | 0,039 | 4,95 | -0,729 | -0,886 |
| 7 | EVET | TOON | haftalik | 20,20 | 1,09 | 0,86 | 0,19 | 0,020 | 7,13 | -0,166 | -0,043 |
| 8 | EVET | SIG | gunluk | 3,47 | 1,08 | 1,21 | 0,06 | 0,038 | 4,82 | -0,031 | -0,094 |
| 9 | EVET | SANM | gunluk | 1,68 | 0,77 | 0,63 | 0,11 | 0,043 | 3,21 | -0,176 | -0,195 |
| 10 | EVET | NCMI | gunluk | 3,01 | 0,87 | 0,71 | 0,15 | 0,041 | 4,78 | +0,232 | +0,230 |
| 11 | EVET | ALNY | gunluk | 3,28 | 0,87 | 0,82 | 0,29 | 0,031 | 5,23 | -0,030 | -0,059 |
| 12 | EVET | EBAY | gunluk | 1,12 | 0,76 | 0,71 | 0,27 | 0,051 | 3,74 | -0,016 | -0,050 |
| 13 | KISMEN | EFOR | haftalik | 11,12 | 1,22 | 0,87 | 0,17 | 0,071 | 2,91 | +0,175 | +0,209 |
| 14 | KISMEN | IESC | haftalik | 12,40 | 1,12 | 1,08 | 0,20 | 0,072 | 3,42 | +0,019 | +0,027 |

Okuma (A1): sayfadaki boy (BOY_SAYFA) gerçek boyla ilişkisiz (128'de rho -0,05 ile BOY_MUTLAK, -0,02 ile BOY_OZ; haftalıkta BOY_MUTLAK ile ters, -0,35). Cemal'in EVET'leri sayfada belirgin küçük (BOY_SAYFA medyanı 0,065 / HAYIR 0,104, p 0,0001) ve sayfaları daha 'şişirilmiş' (SISME 2,66 / 1,71, p 0,005), ama yüzde boyları farklı değil (BOY_MUTLAK p 0,20). Kendi geçmişine göre: günlükte EVET'ler sakin (BOY_OZ 0,84 / 1,07, p 0,0045), haftalıkta değil (1,14 / 1,21, p 0,64). Notlu on bölgenin hepsi sayfada küçük (BOY_SAYFA 0,020-0,072) ve sıkıştırılmış (SISME 2,9-7,1); haftalık olanların BOY_OZ'u 1'in üstünde (1,09-1,22; TRMET boş): o haftalık mumlar hissenin kendi olağanından büyük.

### A2 SONRASI (geriye dönük; ana ölçü BOY_OZ)

| grup | ölçü | zaman | Spearman n / rho / p | KÜÇÜK n / n_es | KÜÇÜK eşli ort / med | KÜÇÜK artıda / eşinden iyi | KÜÇÜK R15 ort / med | BÜYÜK n / n_es | BÜYÜK eşli ort / med | BÜYÜK artıda / eşinden iyi | BÜYÜK R15 ort / med | KÜÇÜK - BÜYÜK | p (BH bilgi) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EVET | BOY_OZ | gunluk | 12 / -0,22 / 0,499 | 8 / 4 | +0,003 / -0,012 | %25 / %50 | -0,035 / -0,016 | 8 / 8 | +0,009 / -0,020 | %38 / %50 | +0,001 / -0,027 | -0,006 | 0,9708 (0,97) |
| EVET | BOY_OZ | haftalik | 17 / -0,27 / 0,295 | 9 / 8 | -0,142 / -0,059 | %33 / %38 | -0,056 / -0,014 | 9 / 9 | -0,210 / -0,131 | %44 / %22 | -0,059 / -0,015 | +0,068 | 0,6352 (0,97) |
| EVET | BOY_MUTLAK | gunluk | 12 / +0,20 / 0,527 | 8 / 6 | +0,013 / -0,054 | %38 / %33 | +0,020 / -0,011 | 8 / 6 | +0,001 / +0,022 | %25 / %67 | -0,054 / -0,027 | +0,012 | 0,8943 (0,97) |
| EVET | BOY_MUTLAK | haftalik | 18 / -0,42 / 0,079 | 10 / 8 | -0,050 / -0,079 | %40 / %38 | -0,001 / -0,012 | 10 / 10 | -0,247 / -0,160 | %40 / %30 | -0,089 / -0,038 | +0,197 | 0,2028 (0,97) |
| EVET | SON_BOY_OZ | gunluk | 12 / -0,12 / 0,713 | 8 / 5 | +0,049 / +0,025 | %25 / %60 | -0,007 / -0,016 | 8 / 7 | -0,023 / -0,059 | %38 / %43 | -0,026 / -0,027 | +0,071 | 0,4687 (0,97) |
| EVET | SON_BOY_OZ | haftalik | 17 / -0,10 / 0,694 | 9 / 8 | -0,217 / -0,109 | %22 / %25 | -0,108 / -0,053 | 9 / 9 | -0,143 / -0,083 | %56 / %33 | -0,006 / +0,043 | -0,073 | 0,6074 (0,97) |
| EVET | BOY_BANT | gunluk | 12 / +0,05 / 0,880 | 8 / 6 | -0,011 / -0,037 | %38 / %50 | +0,008 / -0,012 | 8 / 6 | +0,025 / -0,012 | %25 / %50 | -0,042 / -0,027 | -0,037 | 0,7032 (0,97) |
| EVET | BOY_BANT | haftalik | 18 / -0,17 / 0,499 | 10 / 8 | -0,122 / -0,059 | %50 / %38 | -0,003 / +0,069 | 10 / 10 | -0,189 / -0,118 | %30 / %30 | -0,087 / -0,035 | +0,067 | 0,6472 (0,97) |
| EVET | BOY_SAYFA | gunluk | 12 / +0,10 / 0,762 | 8 / 7 | -0,005 / -0,050 | %12 / %43 | -0,013 / -0,027 | 8 / 5 | +0,023 / +0,019 | %50 / %60 | -0,021 / -0,003 | -0,028 | 0,7866 (0,97) |
| EVET | BOY_SAYFA | haftalik | 18 / +0,05 / 0,829 | 10 / 9 | -0,270 / -0,086 | %30 / %22 | -0,183 / -0,090 | 10 / 9 | -0,048 / -0,083 | %50 / %44 | +0,093 / +0,014 | -0,222 | 0,1406 (0,97) |
| EVET+KISMEN | BOY_OZ | gunluk | 21 / -0,08 / 0,724 | 13 / 9 | +0,019 / -0,002 | %38 / %44 | -0,010 / -0,016 | 13 / 12 | -0,007 / +0,003 | %31 / %50 | -0,021 / -0,023 | +0,027 | 0,6473 (0,88) |
| EVET+KISMEN | BOY_OZ | haftalik | 23 / -0,05 / 0,819 | 12 / 11 | -0,107 / -0,043 | %42 / %45 | -0,048 / -0,012 | 12 / 12 | -0,124 / -0,094 | %58 / %42 | +0,023 / +0,095 | +0,017 | 0,8828 (0,88) |
| EVET+KISMEN | BOY_MUTLAK | gunluk | 21 / +0,15 / 0,515 | 13 / 11 | -0,004 / -0,002 | %46 / %45 | -0,006 / -0,005 | 13 / 10 | +0,013 / +0,008 | %23 / %50 | -0,025 / -0,023 | -0,017 | 0,7582 (0,88) |
| EVET+KISMEN | BOY_MUTLAK | haftalik | 24 / -0,25 / 0,238 | 13 / 11 | -0,031 / -0,074 | %46 / %45 | +0,028 / -0,009 | 13 / 13 | -0,166 / -0,043 | %54 / %46 | -0,041 / +0,019 | +0,135 | 0,2616 (0,88) |
| EVET+KISMEN | SON_BOY_OZ | gunluk | 21 / -0,11 / 0,622 | 13 / 10 | +0,024 / +0,009 | %31 / %50 | -0,007 / -0,016 | 13 / 11 | -0,014 / -0,002 | %38 / %45 | -0,023 / -0,023 | +0,038 | 0,4888 (0,88) |
| EVET+KISMEN | SON_BOY_OZ | haftalik | 23 / -0,05 / 0,812 | 12 / 11 | -0,144 / -0,086 | %33 / %36 | -0,075 / -0,034 | 12 / 12 | -0,089 / -0,023 | %67 / %50 | +0,050 / +0,087 | -0,055 | 0,6423 (0,88) |
| EVET+KISMEN | BOY_BANT | gunluk | 21 / -0,04 / 0,867 | 13 / 11 | -0,005 / -0,004 | %38 / %45 | -0,005 / -0,016 | 13 / 10 | +0,013 / +0,004 | %31 / %50 | -0,026 / -0,023 | -0,018 | 0,7468 (0,88) |
| EVET+KISMEN | BOY_BANT | haftalik | 24 / -0,39 / 0,057 | 13 / 11 | -0,048 / +0,071 | %62 / %55 | +0,050 / +0,146 | 13 / 13 | -0,152 / -0,105 | %38 / %38 | -0,063 / -0,017 | +0,104 | 0,3951 (0,88) |
| EVET+KISMEN | BOY_SAYFA | gunluk | 21 / +0,04 / 0,876 | 13 / 12 | -0,002 / -0,015 | %23 / %42 | -0,011 / -0,023 | 13 / 9 | +0,012 / +0,009 | %46 / %56 | -0,019 / -0,005 | -0,013 | 0,8110 (0,88) |
| EVET+KISMEN | BOY_SAYFA | haftalik | 24 / -0,08 / 0,716 | 13 / 12 | -0,185 / -0,059 | %46 / %42 | -0,099 / -0,014 | 13 / 12 | -0,023 / -0,037 | %54 / %50 | +0,086 / +0,019 | -0,162 | 0,1804 (0,88) |
| HEPSI | BOY_OZ | gunluk | 59 / -0,16 / 0,228 | 33 / 28 | +0,000 / -0,003 | %39 / %46 | -0,001 / -0,008 | 33 / 31 | -0,022 / -0,004 | %45 / %48 | +0,005 / -0,005 | +0,022 | 0,4503 (0,90) |
| HEPSI | BOY_OZ | haftalik | 57 / -0,09 / 0,522 | 30 / 28 | -0,043 / -0,038 | %47 / %43 | +0,038 / -0,012 | 30 / 29 | -0,062 / -0,083 | %57 / %38 | +0,037 / +0,050 | +0,019 | 0,8089 (0,92) |
| HEPSI | BOY_MUTLAK | gunluk | 59 / -0,13 / 0,316 | 33 / 32 | -0,008 / +0,007 | %48 / %53 | +0,004 / -0,003 | 33 / 27 | -0,016 / -0,042 | %36 / %41 | -0,001 / -0,023 | +0,008 | 0,7959 (0,92) |
| HEPSI | BOY_MUTLAK | haftalik | 58 / -0,16 / 0,244 | 31 / 29 | -0,001 / -0,046 | %52 / %41 | +0,076 / +0,003 | 31 / 29 | -0,097 / -0,060 | %52 / %41 | +0,001 / +0,019 | +0,096 | 0,1902 (0,90) |
| HEPSI | SON_BOY_OZ | gunluk | 59 / -0,19 / 0,157 | 33 / 29 | +0,000 / -0,004 | %36 / %48 | -0,003 / -0,013 | 33 / 30 | -0,023 / -0,003 | %48 / %47 | +0,007 / -0,003 | +0,023 | 0,4364 (0,90) |
| HEPSI | SON_BOY_OZ | haftalik | 57 / -0,04 / 0,740 | 30 / 29 | -0,069 / -0,060 | %43 / %38 | +0,007 / -0,024 | 30 / 28 | -0,036 / -0,059 | %60 / %43 | +0,067 / +0,050 | -0,032 | 0,6684 (0,92) |
| HEPSI | BOY_BANT | gunluk | 59 / -0,17 / 0,206 | 33 / 31 | -0,008 / +0,009 | %45 / %52 | +0,009 / -0,007 | 33 / 28 | -0,015 / -0,013 | %39 / %43 | -0,005 / -0,013 | +0,007 | 0,8244 (0,92) |
| HEPSI | BOY_BANT | haftalik | 58 / -0,01 / 0,925 | 31 / 29 | -0,018 / -0,074 | %55 / %38 | +0,088 / +0,096 | 31 / 29 | -0,080 / -0,032 | %48 / %45 | -0,012 / -0,015 | +0,062 | 0,4110 (0,90) |
| HEPSI | BOY_SAYFA | gunluk | 59 / +0,00 / 0,991 | 33 / 31 | -0,012 / -0,004 | %36 / %45 | -0,010 / -0,016 | 33 / 28 | -0,011 / +0,001 | %48 / %50 | +0,013 / -0,003 | -0,001 | 0,9835 (0,98) |
| HEPSI | BOY_SAYFA | haftalik | 58 / +0,11 / 0,414 | 31 / 30 | -0,076 / -0,038 | %55 / %43 | +0,023 / +0,096 | 31 / 28 | -0,020 / -0,072 | %48 / %39 | +0,053 / -0,015 | -0,056 | 0,4474 (0,90) |

OKUMA KURALI: günlük KÜÇÜK +0,003 / BÜYÜK +0,009 (sağlanmadı); haftalık KÜÇÜK -0,142 / BÜYÜK -0,210 (sağlandı) -> **YÖN CEMAL'İN DEDİĞİ GİBİ DEĞİL** (BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK).

Okuma (A2): EVET bölgelerinde gerçek mum boyunun hiçbir ölçüsü sonrasını ayırmıyor: on karşılaştırmanın en küçük p'si 0,14 (BH sonrası 0,97); farklar iki yönde dağınık. Haftalıkta KÜÇÜK ve BÜYÜK yarı ikisi de eşlerinin gerisinde (-14 / -21 puan); günlükte ikisi de eşine yakın (+0,3 / +0,9). EVET + KISMEN ve 128 bölgede de aynı: fark yok (p >= 0,18).

## ÖNERİLEN DEFTER SATIRLARI (ana model işler; alt ajan deftere dokunmadı)

- IK_KAYIT Ç (MUM_IZI16 İŞ A, MUM_IZI_GOZ2.py `olcek`): ölçek olgusu: sayfadaki mum boyu gerçek boyla ilişkisiz (rho -0,05 / -0,02); EVET'ler sayfada küçük (p 0,0001) ama yüzde boyları HAYIR'dan farklı değil (p 0,20); günlük EVET'ler kendi geçmişine göre sakin (BOY_OZ 0,84, p 0,0045), haftalık değil (1,14, p 0,64); 14 / 126 bölge sayfada küçük ama kendi geçmişine göre büyük. Sonrası (geriye dönük): BOY_OZ KÜÇÜK - BÜYÜK eşli fark günlük -0,006 (p 0,97), haftalık +0,068 (p 0,64) -> YÖN CEMAL'İN DEDİĞİ GİBİ DEĞİL; etiket BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK.
- IK_ILERI: MUM_IZI14 ölçekli onay seti (Cemal sonrasını görmeden) işaretlenince aynı `olcek` ölçüleri o 17 bölgede getirisiz yazılır; sonrası ancak yeni ön kayıtla (temiz sınama).
- IK_HATA: H1 (vacuous assert, commit öncesi düzeltildi; ders: her sınır testinde değişikliğin ölçüyü OYNATTIĞI da sınanır).
