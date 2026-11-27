# GT_PARMAK_IZI — Cemal'in çöl kitaplığının çok ölçülü parmak izi (ADIM A; yalnız tespit, getiri yok)

Kod: GOZ_TESPIT.py (sha 09455d76a79d); eşik sözlüğü sha 5d4c7975e408. Kitaplık: COL_SKOR6.CS_KITAPLIK 20 bölge; verisi olan **16** (veri yok: VENUS, BURLS, ECOGR, SURGT). Karşılaştırma evreni: BIST 2016-22 pencereleri (L* = 20 / 40 / 80; n = L20 124.729, L40 125.863, L80 124.645). Sıra = evrendeki yüzdelik ((küçük + 0,5 eşit) / n).

## 1. ÖZET: Cemal'in çöllerinin ortak yanı

**BULGU: İMZA ÖLÇÜSÜ YOK.** 40 ölçünün hiçbiri önceden yazılı imza kuralını geçmedi: verisi olan 16 çölün dörtte üçünün aynı uçta durduğu tek bir ölçü yok. Kitaplık tek tip değil.

En yakınlar şunlar: (1) küçük gövde: çöllerin 14'ünden 10'unda mum gövdesi önceki 120 mumun gövdesine göre küçük (GOVDE_ORAN medyan sıra %20, 10/14 = %71; büyük gövdeli çöl yok); (2) küçülmüş mum boyu (BOY_YUZDE_ORAN medyan %22, 9/14); (3) sert sol bacak: bölgeden önce güçlü düşüş (F5 medyan %87, 10/16; alt uçta hiç çöl yok; önceki 60 mum tepesinden dibe düşüş de derin: ONCEKI_DUSUS medyan %10, 8/14); (4) çölden önce oynaklık genişti (F3 medyan %79, 10/16).

Kısacası Cemal'in çöllerinin ortak yanı 'sert düşüşten sonra mumların ve gövdelerin küçülmesi'; ama bu ortaklık 16 çölün 10'unda var, hepsinde değil.

Ayırmayanlar: doji oranı (F1 medyan %58, 6/16), fiyat sıkışması (F4 %52), hacim azalması (F6 %60, ama 7 çölde hacim azalmamış, artmış: tutarlılık %19), üst fitil (%65, 6/14), dip savunması (DIP_DOKUNMA %65, 7/16). Bunlar çölleri sıradan pencerelerden ayırmıyor.

Dip 16 çölün 12'sinde bölgenin ilk üçte birinde, ama sıradan pencerelerde de bu sık (DIP_YER medyan sıra %38): ayırıcı değil.

Çoğunluğa uyan çöller: TEHOL (iki bölge), PAPIL, SMRVA, HDFGS, KTLEV (tutarlılığı >= %50 olan 14 ölçünün çoğunda kitaplık tarafında: 9-13 / 14; KTLEV 6 / 8). Çoğunluğa uymayanlar: NUGYO (10 mum), ENSRI, ESCAR (bu 14 ölçünün yalnız 2-3'ünde kitaplık tarafında, 4-6'sında karşı uçta); KAPLM, ASELS, KRVGD de yarıdan azında (5-6 / 14). Kitaplık en az iki farklı türden bölge içeriyor olabilir; bölge uzunlukları da 5 ile 190 mum arasında çok farklı.

## 2. İMZA ÖLÇÜLERİ

Kural (önceden): tutarlılık (medyan tarafında >= %70 / <= %30 kalan bölge payı) >= %75, medyan sıra >= %75 ya da <= %25, ölçüsü olan bölge >= 12 / 16; |rho| > 0,80 çiftlerden tutarlılığı düşük olan atılır.

| imza ölçüsü | ne ölçer | yön | medyan sıra | tutarlılık |
|---|---|---|---|---|
| (yok) | | | | |

## 3. Ölçü başına medyan sıra ve tutarlılık (40 ölçü + PUAN_ESIT bilgi)

| ölçü | kaynak | ne ölçer | n | medyan sıra | >= %70 | <= %30 | yön | tutarlılık | imza |
|---|---|---|---|---|---|---|---|---|---|
| F1 | COL_SKOR6 | doji oranı (gövde / boy < 0,40 mum payı) | 16 | %58 | 6 | 2 | YÜKSEK | %38 |  |
| F2 | COL_SKOR6 | Bollinger genişliği daralması | 16 | %70 | 8 | 3 | YÜKSEK | %50 |  |
| F3 | COL_SKOR6 | daralmanın başladığı genişlik (BBW başı / 0,6) | 16 | %79 | 10 | 4 | YÜKSEK | %62 |  |
| F4 | COL_SKOR6 | fiyat sıkışması (1 - aralık / orta) | 16 | %52 | 5 | 5 | YÜKSEK | %31 |  |
| F5 | COL_SKOR6 | sol bacak düşüşü (önceki 30 bar tepesinden bölge dibine) | 16 | %87 | 10 | 0 | YÜKSEK | %62 |  |
| F6 | COL_SKOR6 | hacim azalması (1 - bölge / önceki 200 bar) | 16 | %60 | 3 | 7 | YÜKSEK | %19 |  |
| BOY_YUZDE_ORAN | MUM_IZI_UC | mum boyu (%) / önceki 120 barın mum boyu | 14 | %22 | 1 | 9 | DÜŞÜK | %64 |  |
| BOY_GRAFIK_ORAN | MUM_IZI_UC | mum boyu (fiyat) / önceki 120 bar | 14 | %24 | 1 | 8 | DÜŞÜK | %57 |  |
| BOY_MUTLAK | MUM_IZI_UC | mum boyu medyanı (% fiyat) | 14 | %64 | 6 | 5 | YÜKSEK | %43 |  |
| GOVDE_ORAN | MUM_IZI_UC | gövde (%) / önceki 120 bar | 14 | %20 | 0 | 10 | DÜŞÜK | %71 |  |
| GOVDE_BOY | MUM_IZI_UC | gövde / mum boyu medyanı | 14 | %36 | 2 | 5 | DÜŞÜK | %36 |  |
| UST_FITIL | MUM_IZI_UC | üst fitil / mum boyu medyanı | 14 | %65 | 6 | 0 | YÜKSEK | %43 |  |
| ALT_FITIL | MUM_IZI_UC | alt fitil / mum boyu medyanı | 14 | %48 | 3 | 3 | DÜŞÜK | %21 |  |
| UST_ALT_PAY | MUM_IZI_UC | üst fitili alttan uzun mum payı | 14 | %66 | 7 | 4 | YÜKSEK | %50 |  |
| SON_UST_FITIL | MUM_IZI_UC | son üçte birde üst fitil medyanı | 14 | %56 | 3 | 1 | YÜKSEK | %21 |  |
| DARALMA | MUM_IZI_UC | bant genişliği bitiş / başlangıç - 1 | 14 | %19 | 3 | 8 | DÜŞÜK | %57 |  |
| BANT_SON | MUM_IZI_UC | son üçte birde banttaki yerin 0,85'e yakınlığı (-|bc - 0,85|) | 14 | %61 | 5 | 1 | YÜKSEK | %36 |  |
| ONCEKI_DUSUS | MUM_IZI_UC | bölge dibi / önceki 60 bar tepesi - 1 (%) | 14 | %10 | 0 | 8 | DÜŞÜK | %57 |  |
| MIKRO | YUKSELIS_ONCESI | son 60 barda art arda >= 3 yükselen kapanış serisi sayısı | 16 | %39 | 4 | 8 | DÜŞÜK | %50 |  |
| RS_UZAK | YUKSELIS_ONCESI | göreli güç / son 60 bar en yüksek göreli güç - 1 | 16 | %30 | 4 | 8 | DÜŞÜK | %50 |  |
| OYN_SIRA | YUKSELIS_ONCESI | 60 günlük oynaklığın aynı gün pazar içi sırası | 16 | %69 | 8 | 3 | YÜKSEK | %50 |  |
| MA_KOD | YUKSELIS_ONCESI | SMA20 / 50 / 200 dizilim kodu (0 aşağı .. 3 yukarı) | 15 | %47 | 5 | 6 | DÜŞÜK | %40 |  |
| MA_EGIM_DEG | YUKSELIS_ONCESI | SMA20 eğiminin 10 barlık değişimi | 16 | %70 | 7 | 2 | YÜKSEK | %44 |  |
| ZIRVE_BAR | YUKSELIS_ONCESI | 250 bar zirvesinden bu yana bar | 15 | %53 | 4 | 1 | YÜKSEK | %27 |  |
| ZIRVE_DUSUS | YUKSELIS_ONCESI | kapanış / 250 bar zirvesi - 1 | 15 | %24 | 3 | 8 | DÜŞÜK | %53 |  |
| DIP_BAR | YUKSELIS_ONCESI | zirveden sonraki dipten bu yana bar | 15 | %70 | 7 | 2 | YÜKSEK | %47 |  |
| DIP_HIZ | YUKSELIS_ONCESI | dipten toparlanma hızı (% / bar) | 15 | %60 | 4 | 1 | YÜKSEK | %27 |  |
| CLV10 | YUKSELIS_ONCESI | son 10 barda kapanışın mum içindeki yeri | 16 | %36 | 3 | 7 | DÜŞÜK | %44 |  |
| YUKSELEN_DIP | YUKSELIS_ONCESI | art arda yükselen yerel dip sayısı | 16 | %60 | 5 | 6 | YÜKSEK | %31 |  |
| MOM_12_1 | YUKSELIS_ONCESI | 12-1 ay momentumu | 15 | %39 | 4 | 6 | DÜŞÜK | %40 |  |
| F15 | YUKSELIS_ONCESI | 15 barlık geçmiş getiri | 16 | %58 | 4 | 4 | YÜKSEK | %25 |  |
| KONUM120 | YUKSELIS_ONCESI | son 120 kapanış aralığında konum | 15 | %51 | 4 | 6 | YÜKSEK | %27 |  |
| ATRP20 | YUKSELIS_ONCESI | ATR20 / kapanış | 16 | %66 | 8 | 5 | YÜKSEK | %50 |  |
| DIP_YER | EK | bölge dibinin bölgedeki yeri (0 = ilk bar, 1 = son bar) | 16 | %38 | 2 | 5 | DÜŞÜK | %31 |  |
| DIP_DOKUNMA | EK | dip savunması: dipten en çok 0,5 ATR yukarıda kapanan bar payı | 16 | %65 | 7 | 1 | YÜKSEK | %44 |  |
| SON_KONUM | EK | bölge sonu kapanışının bölge aralığındaki yeri | 16 | %68 | 7 | 2 | YÜKSEK | %44 |  |
| BOLGE_L | EK | bölge uzunluğu (bar) | 16 | %100 | 10 | 6 | YÜKSEK | %62 | bilgi |
| YUK_KAPANIS | EK | bölge içi yükselen kapanış payı | 16 | %55 | 4 | 3 | YÜKSEK | %25 |  |
| HACIM_ORAN | EK | bölge hacmi / önceki 200 bar hacmi | 16 | %40 | 2 | 3 | DÜŞÜK | %19 |  |
| HACIM_SON5 | EK | bölge sonu 5 barın hacmi / bölge ortalaması | 16 | %60 | 5 | 2 | YÜKSEK | %31 |  |
| PUAN_ESIT | COL_SKOR6 | altı ölçü eşit puan (D1) | 16 | %77 | 11 | 2 | YÜKSEK | %69 | bilgi |

Dibin yeri: 12 / 16 bölgede bölge dibi ilk üçte birde (DIP_YER <= 1/3).

## 4. Bölge x ölçü yüzdelik sıra tablosu (%; '-' = ölçü yok: kısa geçmiş)

| ölçü | 1 BINBN | 2 NUGYO | 3 ENSRI | 4 TEHOL | 5 PAPIL | 6 ESCAR | 7 KTLEV | 8 TEHOL | 9 HDFGS | 10 ASELS | 13 EUREN | 16 SMRVA | 17 DOGUB | 18 MANAS | 19 KAPLM | 20 KRVGD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bar / L* | 22/20 | 10/20 | 38/40 | 27/20 | 126/80 | 113/80 | 190/80 | 26/20 | 37/40 | 16/20 | 5/20 | 26/20 | 21/20 | 32/40 | 30/20 | 103/80 |
| F1 | %98 | %10 | %50 | %89 | %45 | %94 | %34 | %95 | %68 | %61 | %80 | %27 | %54 | %94 | %54 | %34 |
| F2 | %100 | %27 | %27 | %85 | %94 | %47 | %55 | %100 | %79 | %91 | %8 | %77 | %47 | %64 | %46 | %93 |
| F3 | %95 | %21 | %23 | %64 | %98 | %44 | %80 | %98 | %83 | %71 | %30 | %77 | %96 | %89 | %11 | %81 |
| F4 | %94 | %81 | %48 | %83 | %29 | %61 | %18 | %27 | %56 | %93 | %88 | %37 | %11 | %4 | %49 | %56 |
| F5 | %90 | %33 | %58 | %99 | %99 | %55 | %100 | %100 | %75 | %62 | %84 | %93 | %96 | %93 | %56 | %68 |
| F6 | %85 | %71 | %61 | %23 | %26 | %92 | %59 | %68 | %25 | %68 | %64 | %64 | %23 | %25 | %23 | %26 |
| BOY_YUZDE_ORAN | - | %9 | %68 | %2 | %21 | %35 | - | %12 | %55 | %24 | %5 | %15 | %53 | %84 | %16 | %29 |
| BOY_GRAFIK_ORAN | - | %10 | %68 | %0 | %1 | %49 | - | %1 | %35 | %30 | %1 | %0 | %46 | %72 | %22 | %26 |
| BOY_MUTLAK | - | %22 | %77 | %22 | %88 | %60 | - | %69 | %72 | %29 | %22 | %80 | %96 | %98 | %44 | %27 |
| GOVDE_ORAN | - | %23 | %48 | %1 | %10 | %19 | - | %17 | %35 | %8 | %4 | %56 | %61 | %15 | %22 | %21 |
| GOVDE_BOY | - | %63 | %38 | %4 | %70 | %16 | - | %8 | %27 | %34 | %30 | %77 | %40 | %3 | %56 | %48 |
| UST_FITIL | - | %30 | %94 | %73 | %62 | %67 | - | %82 | %94 | %57 | %52 | %47 | %53 | %99 | %88 | %38 |
| ALT_FITIL | - | %34 | %55 | %86 | %32 | %49 | - | %31 | %64 | %81 | %72 | %9 | %46 | %29 | %19 | %67 |
| UST_ALT_PAY | - | %24 | %96 | %43 | %79 | %60 | - | %85 | %71 | %24 | %24 | %85 | %43 | %87 | %96 | %19 |
| SON_UST_FITIL | - | %37 | %89 | %66 | %65 | %63 | - | %65 | %83 | %49 | %21 | %50 | %40 | %99 | %37 | %45 |
| DARALMA | - | %67 | %74 | %9 | %10 | %17 | - | %1 | %12 | %9 | %58 | %16 | %34 | %78 | %85 | %21 |
| BANT_SON | - | %2 | %73 | %71 | %43 | %64 | - | %62 | %49 | %61 | %56 | %40 | %71 | %54 | %73 | %91 |
| ONCEKI_DUSUS | - | %69 | %53 | %0 | %2 | %55 | - | %0 | %9 | %50 | %9 | %0 | %2 | %11 | %45 | %42 |
| MIKRO | %50 | %95 | %12 | %28 | %50 | %87 | %12 | %87 | %12 | %12 | %28 | %28 | %50 | %12 | %71 | %50 |
| RS_UZAK | %11 | %52 | %61 | %0 | %91 | %93 | %74 | %0 | %37 | %58 | %24 | %9 | %12 | %19 | %13 | %73 |
| OYN_SIRA | %90 | %22 | %53 | %100 | %73 | %28 | %71 | %97 | %63 | %34 | %66 | %94 | %98 | %96 | %56 | %4 |
| MA_KOD | - | %47 | %79 | %29 | %11 | %79 | %79 | %29 | %29 | %47 | %11 | %11 | %47 | %47 | %79 | %79 |
| MA_EGIM_DEG | %92 | %14 | %53 | %47 | %72 | %43 | %50 | %98 | %26 | %70 | %87 | %88 | %98 | %91 | %69 | %56 |
| ZIRVE_BAR | - | %68 | %90 | %46 | %95 | %44 | %87 | %51 | %53 | %38 | %65 | %53 | %50 | %20 | %47 | %96 |
| ZIRVE_DUSUS | - | %40 | %73 | %2 | %5 | %88 | %2 | %2 | %24 | %67 | %6 | %0 | %20 | %37 | %81 | %70 |
| DIP_BAR | - | %74 | %89 | %71 | %82 | %74 | %98 | %10 | %70 | %53 | %39 | %61 | %58 | %23 | %65 | %74 |
| DIP_HIZ | - | %41 | %60 | %50 | %65 | %45 | %57 | %10 | %43 | %69 | %91 | %68 | %90 | %100 | %55 | %71 |
| CLV10 | %5 | %6 | %9 | %62 | %30 | %89 | %60 | %18 | %63 | %75 | %34 | %13 | %82 | %6 | %38 | %67 |
| YUKSELEN_DIP | %24 | %89 | %24 | %60 | %60 | %99 | %24 | %79 | %60 | %89 | %24 | %24 | %24 | %60 | %79 | %60 |
| MOM_12_1 | - | %47 | %37 | %19 | %1 | %87 | %2 | %89 | %20 | %88 | %39 | %42 | %77 | %13 | %41 | %16 |
| F15 | %57 | %17 | %80 | %48 | %78 | %57 | %19 | %20 | %19 | %57 | %67 | %62 | %92 | %95 | %65 | %59 |
| KONUM120 | - | %24 | %83 | %9 | %57 | %82 | %62 | %2 | %16 | %60 | %14 | %5 | %42 | %51 | %73 | %80 |
| ATRP20 | %12 | %22 | %77 | %26 | %77 | %35 | %84 | %76 | %72 | %22 | %24 | %75 | %91 | %99 | %59 | %37 |
| DIP_YER | %74 | %96 | %48 | %10 | %59 | %36 | %34 | %47 | %21 | %10 | %43 | %39 | %10 | %37 | %20 | %64 |
| DIP_DOKUNMA | %100 | %65 | %76 | %36 | %35 | %78 | %35 | %36 | %76 | %65 | %100 | %36 | %94 | %97 | %18 | %35 |
| SON_KONUM | %47 | %4 | %77 | %66 | %52 | %87 | %69 | %4 | %39 | %96 | %99 | %67 | %85 | %43 | %73 | %74 |
| BOLGE_L | %100 | %0 | %0 | %100 | %100 | %100 | %100 | %100 | %0 | %0 | %0 | %100 | %100 | %0 | %100 | %100 |
| YUK_KAPANIS | %90 | %1 | %79 | %27 | %27 | %87 | %55 | %55 | %42 | %63 | %82 | %55 | %55 | %66 | %70 | %49 |
| HACIM_ORAN | %15 | %29 | %39 | %67 | %61 | %8 | %41 | %32 | %89 | %32 | %36 | %36 | %63 | %92 | %54 | %56 |
| HACIM_SON5 | %67 | %42 | %24 | %76 | %58 | %10 | %32 | %82 | %34 | %42 | %58 | %84 | %65 | %62 | %74 | %80 |
| PUAN_ESIT | %100 | %30 | %31 | %89 | %97 | %84 | %75 | %100 | %76 | %89 | %49 | %80 | %79 | %63 | %25 | %74 |

## 5. BİLGİ: mum izi ✓ / ✗ (Cemal'in BENZİYOR / BENZEMİYOR dediği günlük bölgeler; mum_izi23_olay.csv)

✓ (EVET) 36, ✗ (HAYIR) 60 bölge (ABD|EVET 23, ABD|HAYIR 45, AVR|EVET 1, AVR|HAYIR 8, BIST|EVET 12, BIST|HAYIR 7); sıralar kendi pazarının L = 20 evreninde; AUC = P(✓ sırası > ✗ sırası). Küçük örneklem: bilgi, bulgu değil.

| ölçü | AUC | ✓ medyan sıra | ✗ medyan sıra | n ✓ / ✗ | çöl imzası mı |
|---|---|---|---|---|---|
| BOY_YUZDE_ORAN | 0,29 | %9 | %41 | 34 / 58 |  |
| BOY_GRAFIK_ORAN | 0,30 | %12 | %27 | 34 / 58 |  |
| BANT_SON | 0,68 | %93 | %85 | 34 / 58 |  |
| F2 | 0,67 | %83 | %51 | 36 / 60 |  |
| GOVDE_ORAN | 0,34 | %18 | %33 | 34 / 58 |  |
| HACIM_SON5 | 0,66 | %68 | %45 | 36 / 60 |  |
| RS_UZAK | 0,36 | %39 | %64 | 36 / 60 |  |
| SON_UST_FITIL | 0,63 | %86 | %75 | 34 / 58 |  |
| CLV10 | 0,37 | %47 | %61 | 36 / 60 |  |
| DARALMA | 0,38 | %32 | %46 | 34 / 58 |  |
| HACIM_ORAN | 0,38 | %31 | %40 | 36 / 60 |  |
| UST_ALT_PAY | 0,61 | %94 | %87 | 34 / 58 |  |
| YUKSELEN_DIP | 0,61 | %61 | %61 | 36 / 60 |  |
| UST_FITIL | 0,61 | %93 | %89 | 34 / 58 |  |
| MA_EGIM_DEG | 0,60 | %87 | %80 | 36 / 60 |  |
| F6 | 0,60 | %69 | %60 | 36 / 60 |  |
| BOLGE_L | 0,59 | %75 | %0 | 36 / 60 |  |
| F5 | 0,59 | %68 | %56 | 36 / 60 |  |
| DIP_BAR | 0,58 | %62 | %55 | 31 / 56 |  |
| F1 | 0,58 | %71 | %62 | 36 / 60 |  |
| F15 | 0,57 | %82 | %78 | 36 / 60 |  |
| DIP_DOKUNMA | 0,43 | %36 | %71 | 36 / 60 |  |
| ONCEKI_DUSUS | 0,43 | %34 | %46 | 34 / 58 |  |
| SON_KONUM | 0,44 | %78 | %85 | 36 / 60 |  |
| F3 | 0,56 | %65 | %55 | 36 / 60 |  |
| BOY_MUTLAK | 0,44 | %37 | %36 | 34 / 58 |  |
| ZIRVE_DUSUS | 0,44 | %39 | %50 | 31 / 56 |  |
| ALT_FITIL | 0,45 | %29 | %31 | 34 / 58 |  |
| F4 | 0,45 | %49 | %59 | 36 / 60 |  |
| OYN_SIRA | 0,55 | %51 | %42 | 36 / 60 |  |
| GOVDE_BOY | 0,45 | %33 | %37 | 34 / 58 |  |
| MIKRO | 0,54 | %63 | %55 | 36 / 60 |  |
| MA_KOD | 0,46 | %29 | %33 | 33 / 56 |  |
| KONUM120 | 0,46 | %43 | %47 | 34 / 59 |  |
| ATRP20 | 0,47 | %29 | %33 | 36 / 60 |  |
| YUK_KAPANIS | 0,52 | %77 | %77 | 36 / 60 |  |
| DIP_YER | 0,52 | %28 | %25 | 36 / 60 |  |
| MOM_12_1 | 0,49 | %36 | %37 | 31 / 56 |  |
| DIP_HIZ | 0,49 | %62 | %56 | 31 / 56 |  |
| ZIRVE_BAR | 0,51 | %60 | %65 | 31 / 56 |  |

Çöl imza ölçüleri mum izi ✓'lerinde de aynı uçta mı (AUC kitaplık yönünde > 0,5): 0 / 0 ().

İmzaya en yakın ama geçemeyen 5 ölçü (bilgi) mum izi ✓'lerinde kitaplık yönünde mi: 5 / 5 (GOVDE_ORAN DÜŞÜK evet AUC 0,34; BOY_YUZDE_ORAN DÜŞÜK evet AUC 0,29; F5 YÜKSEK evet AUC 0,59; F3 YÜKSEK evet AUC 0,56; ONCEKI_DUSUS DÜŞÜK evet AUC 0,43).

## 6. Yorum noktaları

- Kitaplık: COL_SKOR6.CS_KITAPLIK (20 bölge); tam BIST verisinde (/tmp/veri) sembolü olanlar ölçülür (COL_SKOR6 kitaplık.json ile aynı 16 bölge beklenir); veri yoksa sayısı yazılır, tutarlılık eşiği aynı oranla (%75) uygulanır.
- Bölge ölçüleri bölgenin kendi bar sayısıyla (COL_SKOR6'nın kitaplık kuralı); MUM_IZI_UC ölçüleri uzunluk parametreli (uc_olcu(m)) olduğu için bölgenin kendi uzunluğuyla; YUKSELIS_ONCESI ölçüleri bölge son barında (tanımları sabit geri bakışlı); karşılaştırma dağılımı bölgeye en yakın L* (20 / 40 / 80; eşitlikte küçük) sınıfının pencereleridir (COL_SKOR6 kuralı).
- MUM_IZI_UC ölçüleri bölgeden önce 120 bar ister (tanım AYNEN); daha kısa geçmişli bölgede (BINBN 50, KTLEV 63 bar) bu 12 ölçü boştur; MOM_12_1 / ZIRVE / DIP ölçüleri 250+ bar ister. Ölçüsü olmayan bölge o ölçünün tutarlılık paydasına girmez; imza için ölçüsü olan bölge >= %75 şartı aranır.
- RS_UZAK ve OYN_SIRA pazar düzeyi bilgi ister: YO'nun P2 havuzu yerine o gün geçerli barı olan bütün hisseler (BIST'te P2 yok; üç pazarda aynı kural).
- BANT_SON MUM_IZI_UC'deki tanımıyla (-|bc - 0,85|: banda yakınlık); ham konum bilgi olarak tutulmaz.
- DIP_DOKUNMA: dip = bölgenin en düşük L'si; ATR = bölge son barındaki ATR20 (YO ATRP20 x kapanış); C_i <= dip + 0,5 ATR olan bölge barlarının payı.
- DIP_YER: bölgenin en düşük L'sinin (ilk görülen) bar sırası / (n - 1); 'dip ilk üçte birde' <=> DIP_YER <= 1/3 (raporda sayılır).
- HACIM_ORAN = ort V(bölge) / ort V(bölgeden önceki en çok 200 bar; en az 20) (F6'nın kırpılmamış ham oranı); HACIM_SON5 = son 5 bar / bölge ortalaması.
- BOLGE_L evrende sabittir (= L*); sırası anlamsız olduğu için imzaya girmez, bilgi olarak yazılır.
- Spearman ilişkisi BIST evreninde her L için ayrı (en çok 200.000 pencere, sabit tohumlu alt örnek), üç L'nin en büyük |rho|'su kullanılır.
- Mum izi bilgi tablosu: mum_izi23_olay.csv günlük satırlar, sinif EVET (✓) / HAYIR (✗) (KISMEN dışarıda); ölçüler aynı fonksiyonlarla, sıralar kendi pazarının L = 20 evreninde (bölgeler 16-24 bar); AUC = P(✓ sırası > ✗ sırası) + 0,5 P(eşit). Getiri sütunları OKUNMAZ.
- D2 sınırı sıra uzayında: BIST'te ham değer sınırıyla aynı; ABD'de pazarın kendi evren sırası (ham değerler pazarlar arasında karşılaştırılamaz).
- D3'te kitaplık çölünün boş ölçüsü (kısa geçmiş) uzaklığa girmez (ortak sonlu boyutlar); komşu çölün L* sınıfından seçilir.
- Havuzdan ayrıca Cemal'e daha önce gösterilmiş mum izi bölgeleriyle örtüşen pencereler çıkarılır (körlük); kitaplık 2024-26, havuz <= 2022: örtüşme beklenmez, kural yine uygulanır ve sayılır.
- Sayfa: MUM_IZI_HAKEM geçmişli sayfanın grafik fonksiyonu (_hk_grafik_gecmis) ve sınır / yüzde ekseni kuralları içe alınır; sayfa fonksiyonu bu modülde (kutu yazıları '✓ çöl / K kısmen / × değil'; 'Senin kalıbın' mum izi şablonu ve mum boyu satırı bu sette YOK: kalıp Cemal'in kendi çölü, sayfada ölçü ipucu verilmez); yakın görünümde önceki 10 bar (iş tanımı).
- Kitaplık sayfaları tam BIST verisinden (2024-26) bölge bitişinde kesilerek çizilir; tarih / hisse yok.
