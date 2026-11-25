# MUM_IZI4 RAPOR (2026-11-25T11:31:46Z)

Sürüm: MUM_IZI_V2 v1.0 (2026-11-25): Cemal'in itirazı -> fark ölçümü, hata dökümü, v2 = v1 S + 7 zorunlu mum yapısı kapısı (getirisiz), görsel onay

## SONUÇ (düz dil)

- İtiraz edilen bölge bulundu: MUM_IZI3_HAFTALIK.pdf sayfa 3, ABD NEE, haftalık, 2007-07-16..2007-11-02 (16 hafta), S 0,66 (renk dizisi itiraz görüntüsüyle 15 / 15 aynı).
- O bölgede 39 ölçünün 20'si kalıba UYMUYOR (fark > 1 sd). Uymayanlar mum yapısı: küçük mum payı 0,31 / 0,55 (-3,8 sd), üst fitil baskınlığı 0,26 / 1,09 (-3,7 sd), üst fitil / boy 0,30 / 0,42 (-2,2 sd), uzun üst fitilli mum 0,25 / 0,45, gövde / boy 0,45 / 0,38, en büyük gövde / bant 0,55 / 0,39. Uyanlar gidiş ve bant yolu: %B başta 0,18 / 0,06, sonda 0,92 / 0,99, SMA geçişi, bant genişliği.
- v1'in S'si bunu ayıramadı: mum ölçüleri uzaklığı 0,62 (1 = tipik rastgele pencere) ama gidiş 0,37 ve bant 0,25 yakın; üçünün ortalaması S'yi 0,66'ya çıkardı (eşik 0,59).
- Bütün v1 eşleşmeleri (günlük ABD 19.368, haftalık ABD 8.794, AVR ve BIST): şablonun 15 ayırt edici ölçüsünden medyan 8'ini taşıyor; HEPSİNİ taşıyan eşleşme %0,01 (günlük ABD 2, haftalık ABD 1). Taşınanlar gidiş / bant (%B eğimi %99, son %B %82, üst fitil %82); taşınmayanlar küçük mum payı %25, boy değişkenliği %24, büyük mum payı %25, doji %37, örtüşme %44.
- Mumun banda göre büyüklüğü sanıldığı gibi değil: eşleşmelerin mum boyu / bant medyanı 0,29, şablonun 0,41 (şablon gerçek verinin %93'lük diliminde: bant dar, fitiller uzun). Gövde / bant eşit (0,125 / 0,122). Fark MUM İÇİNDE: gövde büyük, üst fitil kısa, boylar eşit.
- Karşı örnekler: mumları banda göre 2 kat büyütülmüş ama aynı gidiş (n3) v1'de S 0,87 alıyor (eşiğin çok üstünde; sentetikte %70 kabul). Fitilsiz büyük gövde (n1) 0,43 ve fitilleri ters (n2) 0,54 eşik altı. Aynı mumlar yatay gidişte (p1) tam 0,54, tepesiz 0,57 (tepesiz eşiği 0,56'yı GEÇİYOR).
- v2 (v1 S + 7 zorunlu kapı): rastgele seride kabul v1'in ~1 / 400'ü, n1 / n2 %0; ama tam şablonda n3 %7,1 (ölçüt %5: GEÇMEDİ), tepesizde %3,8 (geçti). Yakalama düştü: tam %90 -> %19, tepesiz %91 -> %11.
- Gerçek veride v2 bölge sayısı v1'in %0,2-%2,7'si (ör. günlük ABD tam 2016-19: 120 / 10.066; P2 içinde 25 / 5.566). v2 bölgeleri P2 dışında (küçük / likiditesi düşük hisse) daha sık.
- Onay seti hazır: 24 rastgele v2 bölgesi (12 haftalık + 12 günlük), hisse adı ve sonrası yok. Cemal 19 / 24 ✓ derse tespit geçerli sayılacak.

## FARK

### A1 itiraz edilen bölge

{'sayfa': 'MUM_IZI3_HAFTALIK.pdf sayfa 3 (ayri_ABD, en yüksek S)', 'pazar': 'ABD', 'sembol': 'NEE', 'bolge_bas': '2007-07-16', 'bolge_son': '2007-11-02', 'm': 16, 'renk': 'GRGGRGRRGGRGGRGR', 'S_bilesen': {'S': 0.6612287788465151, 'dizi': 0.37051024401859245, 'bant': 0.24549706811411331, 'oz': 0.6249588542860243}, 'uyuyor': 19, 'olcu': 39, 'uymayan': ['boy_cv', 'govde_oran', 'ust_fitil', 'ust_alt_log', 'uzun_ust_pay', 'kucuk_mum_pay', 'yuk_tepe_pay', 'yuk_kapanis_pay', 'govde_orta_egim', 'kapanis_egim', 'kapanis_r2', 'dipten_yukselis', 'dip_konum', 'tepe_konum', 'dip_sonrasi_ust_fitil', 'sma_mesafe_son', 'ust_bant_asim_pay', 'alt_bant_asim_pay', 'max_mum_bant', 'max_govde_bant']}

| ölçü | şablon | olay | fark (sd) | sonuç |
|---|---|---|---|---|
| boy_cv | 0.780 | 0.437 | -5.62 | UYMUYOR |
| govde_oran | 0.379 | 0.454 | +1.28 | UYMUYOR |
| ust_fitil | 0.419 | 0.300 | -2.16 | UYMUYOR |
| alt_fitil | 0.203 | 0.246 | +0.90 | UYUYOR |
| ust_alt_log | 1.085 | 0.255 | -3.66 | UYMUYOR |
| yesil_pay | 0.600 | 0.562 | -0.43 | UYUYOR |
| doji_pay | 0.300 | 0.250 | -0.66 | UYUYOR |
| uzun_ust_pay | 0.450 | 0.250 | -2.24 | UYMUYOR |
| buyuk_mum_pay | 0.200 | 0.188 | -0.31 | UYUYOR |
| kucuk_mum_pay | 0.550 | 0.312 | -3.82 | UYMUYOR |
| yuk_dip_pay | 0.632 | 0.667 | +0.48 | UYUYOR |
| yuk_tepe_pay | 0.684 | 0.600 | -1.33 | UYMUYOR |
| yuk_kapanis_pay | 0.632 | 0.467 | -2.44 | UYMUYOR |
| ortusme | 0.811 | 0.779 | -0.64 | UYUYOR |
| govde_orta_egim | 0.115 | 0.147 | +1.58 | UYMUYOR |
| kapanis_egim | 0.116 | 0.171 | +2.55 | UYMUYOR |
| kapanis_r2 | 0.845 | 0.755 | -1.70 | UYMUYOR |
| net_hareket | 2.282 | 2.453 | +0.62 | UYUYOR |
| dipten_yukselis | 3.072 | 3.465 | +1.56 | UYMUYOR |
| dip_konum | 0.105 | 0.067 | -1.21 | UYMUYOR |
| tepe_konum | 0.947 | 1.000 | +7.89 | UYMUYOR |
| dip_sonrasi_alt_fitil | 0.208 | 0.250 | +0.78 | UYUYOR |
| dip_sonrasi_ust_fitil | 0.453 | 0.300 | -2.48 | UYMUYOR |
| pB_bas | 0.061 | 0.176 | +0.42 | UYUYOR |
| pB_son | 0.987 | 0.924 | -0.95 | UYUYOR |
| pB_egim | 0.053 | 0.057 | +0.20 | UYUYOR |
| sma_ustu_pay | 0.500 | 0.562 | +0.27 | UYUYOR |
| sma_mesafe_son | 1.351 | 1.908 | +2.19 | UYMUYOR |
| sma_gecis_konum | 0.500 | 0.500 | +0.00 | UYUYOR |
| bant_gen_bas | 2.538 | 3.023 | +0.13 | UYUYOR |
| bant_gen_oran_log | 0.074 | 0.077 | +0.00 | UYUYOR |
| bant_dar_konum | 0.632 | 0.733 | +0.40 | UYUYOR |
| sma_egim | -0.017 | -0.010 | +0.06 | UYUYOR |
| ust_bant_asim_pay | 0.400 | 0.125 | -1.74 | UYMUYOR |
| alt_bant_asim_pay | 0.150 | 0.062 | -1.90 | UYMUYOR |
| mum_bant | 0.411 | 0.324 | -0.75 | UYUYOR |
| govde_bant | 0.122 | 0.163 | +0.93 | UYUYOR |
| max_mum_bant | 1.217 | 0.616 | -2.55 | UYMUYOR |
| max_govde_bant | 0.393 | 0.548 | +1.09 | UYMUYOR |

### A2 v1 eşleşmeleri

Ayırt edici ölçüler: {'boy_cv': 'Y', 'ust_fitil': 'Y', 'ust_alt_log': 'Y', 'doji_pay': 'Y', 'uzun_ust_pay': 'Y', 'buyuk_mum_pay': 'Y', 'kucuk_mum_pay': 'Y', 'yuk_tepe_pay': 'Y', 'ortusme': 'Y', 'kapanis_r2': 'Y', 'dip_sonrasi_ust_fitil': 'Y', 'pB_bas': 'D', 'pB_son': 'Y', 'pB_egim': 'Y', 'ust_bant_asim_pay': 'Y'}

- gunluk|ABD: n 19368, ayırt edici ölçü sayısı medyan 8 / 15, hepsini taşıyan %0.01; en çok kaçan ['boy_cv', 'kucuk_mum_pay', 'tepe_konum', 'ust_alt_log', 'max_mum_bant', 'doji_pay', 'kapanis_r2', 'net_hareket', 'buyuk_mum_pay', 'dipten_yukselis']; ayırt edici payları {boy_cv: %24, ust_fitil: %82, ust_alt_log: %79, doji_pay: %37, uzun_ust_pay: %72, buyuk_mum_pay: %25, kucuk_mum_pay: %25, yuk_tepe_pay: %47, ortusme: %44, kapanis_r2: %44, dip_sonrasi_ust_fitil: %65, pB_bas: %74, pB_son: %82, pB_egim: %99, ust_bant_asim_pay: %24}
- gunluk|AVR: n 2455, ayırt edici ölçü sayısı medyan 8 / 15, hepsini taşıyan %0.00; en çok kaçan ['boy_cv', 'kucuk_mum_pay', 'ust_alt_log', 'tepe_konum', 'max_mum_bant', 'doji_pay', 'buyuk_mum_pay', 'kapanis_r2', 'net_hareket', 'dip_sonrasi_ust_fitil']; ayırt edici payları {boy_cv: %13, ust_fitil: %78, ust_alt_log: %76, doji_pay: %38, uzun_ust_pay: %69, buyuk_mum_pay: %18, kucuk_mum_pay: %16, yuk_tepe_pay: %56, ortusme: %42, kapanis_r2: %49, dip_sonrasi_ust_fitil: %59, pB_bas: %73, pB_son: %83, pB_egim: %99, ust_bant_asim_pay: %23}
- gunluk|BIST: n 3984, ayırt edici ölçü sayısı medyan 9 / 15, hepsini taşıyan %0.08; en çok kaçan ['tepe_konum', 'boy_cv', 'yuk_tepe_pay', 'kapanis_r2', 'kucuk_mum_pay', 'ust_alt_log', 'max_mum_bant', 'doji_pay', 'net_hareket', 'dip_konum']; ayırt edici payları {boy_cv: %46, ust_fitil: %91, ust_alt_log: %93, doji_pay: %43, uzun_ust_pay: %83, buyuk_mum_pay: %45, kucuk_mum_pay: %50, yuk_tepe_pay: %25, ortusme: %52, kapanis_r2: %34, dip_sonrasi_ust_fitil: %83, pB_bas: %66, pB_son: %78, pB_egim: %98, ust_bant_asim_pay: %29}
- haftalik|ABD: n 8794, ayırt edici ölçü sayısı medyan 8 / 15, hepsini taşıyan %0.01; en çok kaçan ['boy_cv', 'tepe_konum', 'ust_alt_log', 'kucuk_mum_pay', 'max_mum_bant', 'doji_pay', 'kapanis_r2', 'dip_sonrasi_ust_fitil', 'uzun_ust_pay', 'net_hareket']; ayırt edici payları {boy_cv: %31, ust_fitil: %82, ust_alt_log: %83, doji_pay: %35, uzun_ust_pay: %70, buyuk_mum_pay: %31, kucuk_mum_pay: %34, yuk_tepe_pay: %45, ortusme: %48, kapanis_r2: %43, dip_sonrasi_ust_fitil: %68, pB_bas: %78, pB_son: %74, pB_egim: %99, ust_bant_asim_pay: %20}
- haftalik|AVR: n 1244, ayırt edici ölçü sayısı medyan 8 / 15, hepsini taşıyan %0.00; en çok kaçan ['ust_alt_log', 'boy_cv', 'kucuk_mum_pay', 'tepe_konum', 'max_mum_bant', 'doji_pay', 'uzun_ust_pay', 'dip_sonrasi_ust_fitil', 'buyuk_mum_pay', 'ust_fitil']; ayırt edici payları {boy_cv: %16, ust_fitil: %75, ust_alt_log: %70, doji_pay: %34, uzun_ust_pay: %60, buyuk_mum_pay: %19, kucuk_mum_pay: %20, yuk_tepe_pay: %56, ortusme: %43, kapanis_r2: %57, dip_sonrasi_ust_fitil: %62, pB_bas: %80, pB_son: %77, pB_egim: %100, ust_bant_asim_pay: %18}
- haftalik|BIST: n 1118, ayırt edici ölçü sayısı medyan 9 / 15, hepsini taşıyan %0.00; en çok kaçan ['tepe_konum', 'boy_cv', 'kapanis_r2', 'ust_alt_log', 'doji_pay', 'yuk_tepe_pay', 'net_hareket', 'kucuk_mum_pay', 'dip_konum', 'dipten_yukselis']; ayırt edici payları {boy_cv: %52, ust_fitil: %97, ust_alt_log: %97, doji_pay: %40, uzun_ust_pay: %87, buyuk_mum_pay: %50, kucuk_mum_pay: %54, yuk_tepe_pay: %35, ortusme: %42, kapanis_r2: %29, dip_sonrasi_ust_fitil: %92, pB_bas: %66, pB_son: %69, pB_egim: %98, ust_bant_asim_pay: %28}

### A3 mum / bant

- gunluk|ABD: mum_bant medyan 0.291 (şablon 0.411, şablondan büyük %14), govde_bant medyan 0.125 (şablon 0.122, şablondan büyük %53), max_mum_bant medyan 0.613 (şablon 1.217, şablondan büyük %8), max_govde_bant medyan 0.383 (şablon 0.393, şablondan büyük %47)
- gunluk|AVR: mum_bant medyan 0.290 (şablon 0.411, şablondan büyük %14), govde_bant medyan 0.128 (şablon 0.122, şablondan büyük %55), max_mum_bant medyan 0.588 (şablon 1.217, şablondan büyük %5), max_govde_bant medyan 0.385 (şablon 0.393, şablondan büyük %48)
- gunluk|BIST: mum_bant medyan 0.297 (şablon 0.411, şablondan büyük %18), govde_bant medyan 0.122 (şablon 0.122, şablondan büyük %50), max_mum_bant medyan 0.711 (şablon 1.217, şablondan büyük %12), max_govde_bant medyan 0.406 (şablon 0.393, şablondan büyük %53)
- haftalik|ABD: mum_bant medyan 0.292 (şablon 0.411, şablondan büyük %15), govde_bant medyan 0.127 (şablon 0.122, şablondan büyük %55), max_mum_bant medyan 0.645 (şablon 1.217, şablondan büyük %11), max_govde_bant medyan 0.398 (şablon 0.393, şablondan büyük %51)
- haftalik|AVR: mum_bant medyan 0.286 (şablon 0.411, şablondan büyük %11), govde_bant medyan 0.126 (şablon 0.122, şablondan büyük %54), max_mum_bant medyan 0.587 (şablon 1.217, şablondan büyük %5), max_govde_bant medyan 0.371 (şablon 0.393, şablondan büyük %43)
- haftalik|BIST: mum_bant medyan 0.319 (şablon 0.411, şablondan büyük %22), govde_bant medyan 0.131 (şablon 0.122, şablondan büyük %58), max_mum_bant medyan 0.765 (şablon 1.217, şablondan büyük %16), max_govde_bant medyan 0.447 (şablon 0.393, şablondan büyük %61)

### A4 karşı örnekler (şablon bantlarıyla)

{'tam': {'n1': {'S': 0.4348556242442261, 'dizi': 0.4587856273919788, 'bant': 0.0, 'oz': 2.039437976427068}, 'n2': {'S': 0.5449100942790436, 'dizi': 0.45405927565106075, 'bant': 0.0, 'oz': 1.3673441120069239}, 'n3': {'S': 0.8676612000373799, 'dizi': 0.27835934608305996, 'bant': 0.0, 'oz': 0.14750254308205177}, 'p1': {'S': 0.5374922356994286, 'dizi': 0.5567186921661199, 'bant': 0.8166588071408417, 'oz': 0.48914539357809106}, 'p1b': {'S': 0.31811864466959866, 'dizi': 1.1134373843322398, 'bant': 1.6333176142816834, 'oz': 0.6892376094056364}}, 'tepesiz': {'n1': {'S': 0.42987779493424105, 'dizi': 0.4603462399048084, 'bant': 0.0, 'oz': 2.072416685636384}, 'n2': {'S': 0.5520654618854577, 'dizi': 0.46602948328721217, 'bant': 0.0, 'oz': 1.316236464805142}, 'n3': {'S': 0.8644646150736298, 'dizi': 0.2705563545503309, 'bant': 0.0, 'oz': 0.16637836280590046}, 'p1': {'S': 0.5709455197866373, 'dizi': 0.5411127091006618, 'bant': 0.6814687206077202, 'oz': 0.4588030277230239}, 'p1b': {'S': 0.36266983203435293, 'dizi': 1.0822254182013236, 'bant': 1.3629374412154402, 'oz': 0.5976243772928804}}, 'esik': {'tam': 0.59, 'tepesiz': 0.56}}

Küme S (haftalık): {'n': 11156, 'kume_max_sonra_pay': 0.6117784152025816, 'S_ilk_med': 0.5990649591690655, 'S_kume_max_med': 0.6111975236977342, 'kume_max_ge_069_ilk_lt_069': 0.013714593044101829, 'kume_max_ge_069': 153}

## v2 SENTETİK

{'surum': "MUM_IZI_V2 v1.0 (2026-11-25): Cemal'in itirazı -> fark ölçümü, hata dökümü, v2 = v1 S + 7 zorunlu mum yapısı kapısı (getirisiz), görsel onay", 'tohum': 200, 'tam': {'poz': {'v1': 0.905, 'v2': 0.19194444444444445, 'n': 3600, 'gurultu': {'0.0': {'v1': 0.9483333333333334, 'v2': 0.31833333333333336}, '0.1': {'v1': 0.915, 'v2': 0.1775}, '0.2': {'v1': 0.8516666666666667, 'v2': 0.08}}, 'baglam': {'dip': {'v1': 0.9858333333333333, 'v2': 0.38083333333333336}, 'tepe': {'v1': 0.795, 'v2': 0.04}, 'yatay': {'v1': 0.9341666666666667, 'v2': 0.155}}}, 'n1': {'v1': 0.0002777777777777778, 'v2': 0.0, 'n': 3600, 'gurultu': {'0.0': {'v1': 0.0, 'v2': 0.0}, '0.1': {'v1': 0.0, 'v2': 0.0}, '0.2': {'v1': 0.0008333333333333334, 'v2': 0.0}}, 'baglam': {'dip': {'v1': 0.0008333333333333334, 'v2': 0.0}, 'tepe': {'v1': 0.0, 'v2': 0.0}, 'yatay': {'v1': 0.0, 'v2': 0.0}}}, 'n2': {'v1': 0.003611111111111111, 'v2': 0.0, 'n': 3600, 'gurultu': {'0.0': {'v1': 0.0, 'v2': 0.0}, '0.1': {'v1': 0.0016666666666666668, 'v2': 0.0}, '0.2': {'v1': 0.009166666666666667, 'v2': 0.0}}, 'baglam': {'dip': {'v1': 0.005833333333333334, 'v2': 0.0}, 'tepe': {'v1': 0.0, 'v2': 0.0}, 'yatay': {'v1': 0.005, 'v2': 0.0}}}, 'n3': {'v1': 0.6961111111111111, 'v2': 0.07138888888888889, 'n': 3600, 'gurultu': {'0.0': {'v1': 0.7508333333333334, 'v2': 0.1075}, '0.1': {'v1': 0.7091666666666666, 'v2': 0.07583333333333334}, '0.2': {'v1': 0.6283333333333333, 'v2': 0.030833333333333334}}, 'baglam': {'dip': {'v1': 0.9391666666666667, 'v2': 0.14166666666666666}, 'tepe': {'v1': 0.38666666666666666, 'v2': 0.0125}, 'yatay': {'v1': 0.7625, 'v2': 0.06}}}, 'rastgele': {'blok': {'v1_1000': 1.9639376218323588, 'v2_1000': 0.004873294346978557, 'oran': 0.0024813895781637717}, 'ry': {'v1_1000': 3.3528265107212474, 'v2_1000': 0.004873294346978557, 'oran': 0.0014534883720930232}}, 'olcut': {'negatif_le_5': {'n1': True, 'n2': True, 'n3': False}, 'rastgele_le_1_5': {'blok': True, 'ry': True}, 'gecti': False}}, 'tepesiz': {'poz': {'v1': 0.9105555555555556, 'v2': 0.10527777777777778, 'n': 3600, 'gurultu': {'0.0': {'v1': 0.9566666666666667, 'v2': 0.15916666666666668}, '0.1': {'v1': 0.9291666666666667, 'v2': 0.09583333333333334}, '0.2': {'v1': 0.8458333333333333, 'v2': 0.060833333333333336}}, 'baglam': {'dip': {'v1': 0.9908333333333333, 'v2': 0.19916666666666666}, 'tepe': {'v1': 0.8133333333333334, 'v2': 0.021666666666666667}, 'yatay': {'v1': 0.9275, 'v2': 0.095}}}, 'n1': {'v1': 0.0016666666666666668, 'v2': 0.0, 'n': 3600, 'gurultu': {'0.0': {'v1': 0.0, 'v2': 0.0}, '0.1': {'v1': 0.0, 'v2': 0.0}, '0.2': {'v1': 0.005, 'v2': 0.0}}, 'baglam': {'dip': {'v1': 0.004166666666666667, 'v2': 0.0}, 'tepe': {'v1': 0.0008333333333333334, 'v2': 0.0}, 'yatay': {'v1': 0.0, 'v2': 0.0}}}, 'n2': {'v1': 0.01638888888888889, 'v2': 0.0, 'n': 3600, 'gurultu': {'0.0': {'v1': 0.0008333333333333334, 'v2': 0.0}, '0.1': {'v1': 0.006666666666666667, 'v2': 0.0}, '0.2': {'v1': 0.041666666666666664, 'v2': 0.0}}, 'baglam': {'dip': {'v1': 0.03166666666666667, 'v2': 0.0}, 'tepe': {'v1': 0.0, 'v2': 0.0}, 'yatay': {'v1': 0.0175, 'v2': 0.0}}}, 'n3': {'v1': 0.7541666666666667, 'v2': 0.03833333333333333, 'n': 3600, 'gurultu': {'0.0': {'v1': 0.7808333333333334, 'v2': 0.0475}, '0.1': {'v1': 0.7825, 'v2': 0.0475}, '0.2': {'v1': 0.6991666666666667, 'v2': 0.02}}, 'baglam': {'dip': {'v1': 0.97, 'v2': 0.0775}, 'tepe': {'v1': 0.47333333333333333, 'v2': 0.005833333333333334}, 'yatay': {'v1': 0.8191666666666667, 'v2': 0.03166666666666667}}}, 'rastgele': {'blok': {'v1_1000': 5.520428015564202, 'v2_1000': 0.029182879377431907, 'oran': 0.0052863436123348016}, 'ry': {'v1_1000': 9.644941634241246, 'v2_1000': 0.04377431906614786, 'oran': 0.0045385779122541605}}, 'olcut': {'negatif_le_5': {'n1': True, 'n2': True, 'n3': True}, 'rastgele_le_1_5': {'blok': True, 'ry': True}, 'gecti': True}}, 'sure_sn': 383}

## v2 SAYIM

| zaman | pazar | şablon | dönem | v1 | v2 | v2 / v1 | v1 evren | v2 evren | oran evren |
|---|---|---|---|---|---|---|---|---|---|
| gunluk | ABD | tam | d1619 | 10066 | 120 | 0.0119 | 5566 | 25 | 0.0045 |
| gunluk | ABD | tam | d2022 | 9302 | 71 | 0.0076 | 5101 | 16 | 0.0031 |
| gunluk | ABD | tepesiz | d1619 | 23352 | 186 | 0.0080 | 13764 | 43 | 0.0031 |
| gunluk | ABD | tepesiz | d2022 | 21716 | 105 | 0.0048 | 13036 | 21 | 0.0016 |
| gunluk | AVR | tam | d1619 | 1326 | 10 | 0.0075 | 963 | 4 | 0.0042 |
| gunluk | AVR | tam | d2022 | 1129 | 4 | 0.0035 | 758 | 0 | 0.0000 |
| gunluk | AVR | tepesiz | d1619 | 3414 | 14 | 0.0041 | 2571 | 6 | 0.0023 |
| gunluk | AVR | tepesiz | d2022 | 2874 | 6 | 0.0021 | 2078 | 2 | 0.0010 |
| gunluk | BIST | tam | d1619 | 2152 | 54 | 0.0251 | 2152 | 54 | 0.0251 |
| gunluk | BIST | tam | d2022 | 1832 | 40 | 0.0218 | 1832 | 40 | 0.0218 |
| gunluk | BIST | tepesiz | d1619 | 3695 | 71 | 0.0192 | 3695 | 71 | 0.0192 |
| gunluk | BIST | tepesiz | d2022 | 3083 | 53 | 0.0172 | 3083 | 53 | 0.0172 |
| haftalik | ABD | tam | h0107 | 1880 | 11 | 0.0059 | 1026 | 0 | 0.0000 |
| haftalik | ABD | tam | h0815 | 2555 | 21 | 0.0082 | 1299 | 9 | 0.0069 |
| haftalik | ABD | tam | h1622 | 4130 | 60 | 0.0145 | 2235 | 19 | 0.0085 |
| haftalik | ABD | tepesiz | h0107 | 4413 | 23 | 0.0052 | 2403 | 9 | 0.0037 |
| haftalik | ABD | tepesiz | h0815 | 6559 | 43 | 0.0066 | 3763 | 15 | 0.0040 |
| haftalik | ABD | tepesiz | h1622 | 9604 | 98 | 0.0102 | 5662 | 33 | 0.0058 |
| haftalik | AVR | tam | h0107 | 310 | 3 | 0.0097 | 238 | 3 | 0.0126 |
| haftalik | AVR | tam | h0815 | 414 | 1 | 0.0024 | 273 | 0 | 0.0000 |
| haftalik | AVR | tam | h1622 | 510 | 3 | 0.0059 | 386 | 3 | 0.0078 |
| haftalik | AVR | tepesiz | h0107 | 773 | 3 | 0.0039 | 563 | 3 | 0.0053 |
| haftalik | AVR | tepesiz | h0815 | 1160 | 2 | 0.0017 | 776 | 0 | 0.0000 |
| haftalik | AVR | tepesiz | h1622 | 1356 | 3 | 0.0022 | 1040 | 2 | 0.0019 |
| haftalik | BIST | tam | h1622 | 1112 | 27 | 0.0243 | 1112 | 27 | 0.0243 |
| haftalik | BIST | tepesiz | h1622 | 1737 | 47 | 0.0271 | 1737 | 47 | 0.0271 |

Onay seti: 24 sayfa; tohum 25112044
Prefix: {'gunluk|ABD': {'n': 30, 'en_buyuk_fark': 0.0, 'tuttu': True}, 'gunluk|AVR': {'n': 30, 'en_buyuk_fark': 0.0, 'tuttu': True}, 'gunluk|BIST': {'n': 30, 'en_buyuk_fark': 0.0, 'tuttu': True}, 'haftalik|ABD': {'n': 30, 'en_buyuk_fark': 0.0, 'tuttu': True}, 'haftalik|AVR': {'n': 15, 'en_buyuk_fark': 0.0, 'tuttu': True}, 'haftalik|BIST': {'n': 30, 'en_buyuk_fark': 0.0, 'tuttu': True}}
Kapı: {'kontrol': {'gecti': True}, 'onkayit_commit': '6758f5fc67b1fc94e2c6b58bcef6158175f1e1c5 2026-11-25T11:17:55+00:00', 'KOD4_SHA': '1bb586cb825b8b437b97df4ec193a682bc626ecc796e9130d27e4906b68d81dc', 'ESIK4_SHA': '656584bafa35df1fbda028fa6ea3ca31f32ed0f2e0fd4c9cb9b7741f9bc7ab6f', 'KAPI_ESIK_SHA': '8b6cbdfc5d59ee0ac717862b1f2d3598ee1d59e23d1e13c6940cf88db5fe35cd', 'SENTETIK4_SHA': 'a6c72463ad2a9d7059410f483877fd8c167d100cfcb57c8fa4ae522d95f20731', 'MI_KOD_SHA': '370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9', 'MH_KOD_SHA': '8f7440d199dfcf018f838da77da5cf0eabd89062fdc67cf26a0a5678ed4da200'}
KASA: {'kesik': '2022-12-31', 'dosya': {'/tmp/mum_izi/acik/V_ABD.pkl': '2022-12-30', '/tmp/mum_izi/acik/V_AVR.pkl': '2022-12-30', '/tmp/mum_izi/acik/V_BIST.pkl': '2022-12-30', '/tmp/mum_izi/haftalik/tam/V_ABD.pkl': '2022-12-30', '/tmp/mum_izi/haftalik/tam/V_AVR.pkl': '2022-12-30', '/tmp/mum_izi/haftalik/tam/V_BIST.pkl': '2022-12-30'}}

## HATA DÖKÜMÜ

| # | nerede | ne | tür | kanıt | karara etkisi | ders | sonuç |
|---|---|---|---|---|---|---|---|
| 1 | ana model iş tanımı (MUM_IZI_IS_TANIMI §4) + alt ajan sentetik tasarımı | eşik yalnız YAKALAMA (%80) ile seçildi; aynı gidiş farklı mum negatifleri hiç sınanmadı | ölçüt | v1 sentetikte n3 kabul %70 (tam) / %75 (tepesiz); rastgele seride 2,0-3,4 tekil / 1.000 bar; 15 ayırt edici ölçünün hepsini taşıyan eşleşme %0,01 | v1 bölgeleri kalıbı temsil etmiyor: Ç227 İZ DEĞİL ve EK 3 sonuçları kalıp için geçersiz | eşik pozitif + aynı-gidiş negatifleri + rastgele ile birlikte, kabul ölçütü önceden | DOĞRULANDI |
| 2 | alt ajan rapor yorumu (MUM_IZI_RAPOR), ana model kabul etti | gerçek / rastgele eşleşme oranı ~1 'kalıp nadir değil' diye yorumlandı; doğru okuma 'dedektör ayırt edemiyor' | yanlış yorum | gerçek / rastgele 0,8-1,9; A2 medyan 8 / 15 ayırt edici ölçü | dedektör özgüllüğü sorgulanmadı | rastgeleyle eşit sıklık önce dedektörün kendisini şüpheli yapar | DOĞRULANDI |
| 3 | alt ajan kodu (MI.mi_S_bilesen) | S üç uzaklığın ORTALAMASI: gidiş ve bant yakınsa mum yapısı uzaklığı örtülüyor | ölçüt | NEE: mum 0,62, gidiş 0,37, bant 0,25 -> S 0,66 >= 0,59; ama aşırı mum farkında (n1 0,43, n2 0,54) eşik altı | orta derece mum farklı bölgeler kabul edildi | ayrı bileşen eşiği ya da zorunlu kapı | DOĞRULANDI (kısmen: aşırı farkları ayırıyor) |
| 4 | alt ajan kodu (birim = bölgenin ortalama mum boyu) | mumun banda göre büyüklüğü S'ye girmiyor | ölçüt | n3 (mumlar banda göre 2 kat) S 0,87; sentetikte %70 kabul | mekanizma var; ama gerçek eşleşmelerde mumlar banda göre büyük DEĞİL (medyan 0,29 < şablon 0,41) | banda göre boy ayrı ölçü (v2 k4) | MEKANİZMA DOĞRULANDI, gözlem ÇÜRÜDÜ |
| 5 | alt ajan kodu (MI._mi_tekil 'ilk kalır') | haftalık kümede ilk eşik haftası alındı, en iyi hizalanan hafta değil | hesap | haftalık 11.156 olayın %61'inde kümede daha yüksek S'li hafta var; medyan S 0,599 -> 0,611; 153 kümede (%1,4) sonraki hafta S >= 0,69 iken ilk hafta < 0,69 | gösterilen S ve TAM UYAN ayrımı yanlış hafta üzerinden | tekil olayda kümenin en iyi penceresi | DOĞRULANDI |
| 6 | ana model iş tanımı (görsel kontrol seti onay kapısı değildi) + alt ajan uygulaması | tespit Cemal'in gözüyle doğrulanmadan getiri ölçüldü, hüküm yazıldı | süreç | Ç227 İZ DEĞİL (6ed010a) ve EK 3 (6b564eb) onay adımı olmadan; kontrol PDF'i aynı commit'te, onaya sunulmadı | yanlış nesnenin getirisi ölçüldü | önce göz onayı (>= %80 ✓), sonra getiri | DOĞRULANDI |
| 7 | ana model seçim kuralı ('tam şablonda en yüksek S') + alt ajan ESIK listesinden seçti | PDF'te 'kalıba TAM uyan' beklenen sayfalar eşik listesinden geldi | süreç | ön kayıtlı 40 sayfanın S'si 0,577-0,674 (hepsi < 0,69); NEE 0,661; yalnız EK'teki 12 sayfa TAM UYAN | Cemal'e kalıbın en iyi örnekleri yerine sınırdaki eşleşmeler gösterildi | gösterilen örnek seviyesi açık yazılır | DOĞRULANDI |
| 8 | ana model göz karşılaştırması (bu iş tanımı) | 'kalıpta mumlar banda göre küçük' | yanlış yorum | şablon mum boyu / bant 0,41 = gerçek verinin %93'lük dilimi; eşleşmelerin %86'sı daha küçük | k4'ün ortalama mum / bant kolu bağlayıcı değil; asıl ayırt eden mum içi oran | göz iddiası ölçülmeden kapı yapılmaz | YENİ, DOĞRULANDI |
| 9 | alt ajan tasarımı (tau = rastgele medyan uzaklık) | eşik 0,59 = ortalama normalize uzaklık 0,53 ('rastgele pencerenin yarısı kadar uzak'): gevşek benzerlik | ölçüt | rastgele seride 2,0-3,4 tekil / 1.000 bar; v2 kapılarıyla 0,005 | sık ve ayrımsız eşleşme | benzerlik eşiği negatiflerle ayarlanır | YENİ, DOĞRULANDI |
| 10 | alt ajan tasarımı (EK 2) | ENSRI aylık mumlarının yüzdeliği günlük dağılıma göre alındı | ölçüt | şablonun günlük / haftalık yüzdelikleri yakın (üst fitil 0,984 / 0,991) ama aylık dağılım yok | EK 2 ortak nokta sayısı yaklaşık | aynı zaman dilimi dağılımı | YENİ (etki küçük) |
| 11 | alt ajan kodu (EK 3 haftalık) | eksik haftalı pencere atılmıyordu | veri | ABD haftalık eşik seviyesi v1 olayı (iki şablon) EK 3'te 29.870, boşluk kuralıyla 29.141 (-729, %2,4) | EK 3 sayıları ~%2,4 fazla | haftalıkta boşluklu pencere atılır (v2'de uygulandı) | DOĞRULANDI |

## v2 SENTETİK (kabul ölçütü önceden: n1 / n2 / n3 <= %5, rastgele <= v1 / 5)

| şablon | yakalama v1 -> v2 (%0 / %10 / %20 gürültü) | n1 v1 / v2 | n2 v1 / v2 | n3 v1 / v2 | rastgele 1.000 bar v1 / v2 (blok; ry) | ölçüt |
|---|---|---|---|---|---|---|
| tam | %90,5 -> %19,2 (%31,8 / %17,7 / %8,0) | %0,0 / %0,0 | %0,4 / %0,0 | %69,6 / %7,1 | 1,96 / 0,005; 3,35 / 0,005 | GEÇMEDİ (n3) |
| tepesiz | %91,1 -> %10,5 (%15,9 / %9,6 / %6,1) | %0,2 / %0,0 | %1,6 / %0,0 | %75,4 / %3,8 | 5,52 / 0,029; 9,64 / 0,044 | GEÇTİ |

Bağlama göre v2 yakalama (tam): dip %38, yatay %16, tepe %4. Kapılar gevşetilmedi.

## ONAY SETİ

MUM_IZI4_ONAY.pdf, 26 sayfa: fark sayfası + hata sayfası + 24 bölge (12 haftalık + 12 günlük; tohum 25112044; günlük 12'nin 9'u BIST, çünkü P2 içindeki günlük v2 bölgelerinin çoğu BIST'te). Anahtar mum_izi4_onay_anahtar.json'da (PDF'te hisse / tarih / sonrası yok). Onay eşiği: 24'ün >= 19'u ✓ -> tespit GEÇERLİ.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | v2 sentetik testinde negatif kontroller (n1 / n2 / n3 aynı gidiş farklı mum yapısı) ve rastgele seri tabanı SAYIYLA; v1 ile yan yana; getiri / eş bu işte yok (bölge sayımı) |
| K2 | geleceğe bakma | EVET | kapı ölçüleri ve S pencere içi, t'ye kadarki barlar (MI.mi_bant / mi_ozellik); mv_prefix 30 olayda veri t'de kesilince kabul ve S aynı (assert); veri <= 2022-12-31 + KASA kapısı |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar süzgeci; haftalıkta eksik hafta içeren pencere atılır (bağımsız denetçi bulgusu, v2'de kural) |
| K4 | tekilleştirme | EVET | aynı hissede 15 bar (günlük) / 15 hafta tekil (ilk kabul) |
| K5 | giriş fiyatı | UYGULANMAZ | giriş / getiri hesaplanmaz (bölge sayımı ve görsel onay) |
| K6 | veri birimi | EVET | ölçüler ölçek bağımsız; EK ölçüler mum / bant oranı; TEZGAH2 bölünme düzeltmeli fiyat |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler; sayım bilgi; onay seti görsel (getiri yok) |
| K8 | örneklem ve dönem | EVET | sentetik 200 tohum / koşul; kabul ölçütü önceden; gerçek veride yalnız sayım (pazar x dönem) |
| K9 | ön kayıt | EVET | MUM_IZI4_ON_KAYIT.md: KOD4_SHA, ESIK4_SHA, kapı eşik tablosu sha, sentetik sonuç sha, onay seçim tohumu; gerçek veri sayımından ÖNCE commit; mv_kapi kontrol + sha + git |
| K10 | ayrıştırma | EVET | itiraz edilen bölge mum renk dizisiyle bulundu (15 / 15); onay PDF'i Cemal'in gözü (✓ / ✗) = görsel doğrulama |
| K11 | yeniden üretim | EVET | mv_tara_seri S'si kapısız durumda MI.mi_tara_seri ile birebir (test); 2 hücre sayımı olay dosyasından düz pandas |
| K12 | ifade | EVET | v1 sonuçları 'v1 dedektörünün bölgeleri için' diye yazılır; kalıp için hüküm yok (ÖLÇÜLEMEDİ); 'iz' sözü yok |
| K13 | süreç | EVET | çakışma kapısı; v1 dosyaları / defterler / UC_IZ2 değişmez; yalnız kendi yolları git add |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

Uygulama kanıtı: kapı geçti (ön kayıt 6758f5f); prefix 6 x 30 (AVR haftalık 15) olayda kabul ve S aynı; 2 hücre sayımı düz pandas = json; v1 günlük ABD olay sayısı 64.436 = MUM_IZI taramasıyla birebir (bağımsız yeniden üretim); test_mum_izi4 7 / 7 (şablon kendi kapılarından 7 / 7, iki zaman dilimi, iki şablon).

## SAPMA

1. A3'ün 3 ölçüsüne k4'ün 'en büyük gövde / bant' ölçüsü eklendi: 4 EK ölçü.
2. A2'de eşleşmelerin yüzdeliği L 20 dağılımına göre (günlük eşleşme günlük L 20, haftalık eşleşme haftalık L 20); kapı eşikleri ise her L için ayrı (iş tanımı).
3. Sentetik kabul ölçütü tam şablonda GEÇMEDİ; iş tanımı gereği kapılar gevşetilmeden sayım ve onay seti yapıldı.
4. Haftalık sayımda boşluklu pencere kuralı v1'e de uygulandı (v1 / v2 oranı aynı kuralla).

## COMMIT'LER (UTC)

- 0eec910 2026-11-25T11:17:43Z: kod + fark (A1-A4) + kapı eşikleri + sentetik (gerçek veride v2 sayımından önce)
- 6758f5f 2026-11-25T11:17:55Z: ön kayıt
- sayım 11:17:58Z - 11:28:50Z; sonuç commit'i bu raporla

## ÖNERİLEN DEFTER SATIRLARI (ana model işler)

- Ç (taslak): "MUM_IZI EK 4 (Cemal'in itirazı): itiraz edilen bölge EK 3 PDF s.3 (ABD NEE 2007, S 0,66), 39 ölçünün 20'si uymuyor (mum yapısı: küçük mum payı -3,8 sd, üst fitil baskınlığı -3,7 sd); v1 S gidiş + bant yakınlığıyla mum farkını örtüyor; v1 eşleşmelerinin 15 ayırt edici ölçünün hepsini taşıyanı %0,01. v1 bölgeleri kalıbı temsil etmiyor -> Ç227 ve EK 3 sonuçları 'v1 dedektörünün bölgeleri' içindir, kalıp ÖLÇÜLEMEDİ. v2 (S + 7 zorunlu kapı): rastgele kabul v1'in 1 / 400'ü, n3 tam %7,1 (ölçüt geçmedi), yakalama %19 / %11; gerçek veride v1'in %0,2-%2,7'si. Onay seti (24 rastgele bölge) Cemal'de; >= 19 ✓ ise tespit geçerli. Getiri yok."
- IK_GOREV: "2026-11-25 | MUM_IZI EK 4 (itiraz: fark + hata dökümü + v2 + onay seti) | v1 yanlış nesneyi ölçtü; v2 sayıldı, onay bekliyor | MUM_IZI_V2.py, test_mum_izi4 7 / 7, MUM_IZI4_ONAY.pdf"
- IK_HATA: HATA DÖKÜMÜ 1-11 (ana model: 1, 6, 7, 8; alt ajan: 1, 2, 3, 4, 5, 7, 9, 10, 11).
- IK_ACIK: "(a) Cemal'in onay işaretleri (24 sayfa) -> >= 19 ✓ ise sonrası yeni ön kayıtla; değilse ✗ sayfalarının ortak nedeni yeni kapı. (b) v2 tam şablonda n3 ölçütü geçmedi (%7,1): banda göre boy kapısı (k4) yetersiz. (c) Ç227 ve EK 3 kayıtlarına DÜZELTME notu: 'v1 dedektörünün bölgeleri için; kalıp ÖLÇÜLEMEDİ'."
