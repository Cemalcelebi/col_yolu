# GELECEK_DUZELTME test notu (15 Kas 2026)

FON_IZI v1.40 (karar günü konumu t >= N-1) sonrası iki testin 'SAPMA-1 gerekçesi' bölümleri yeni davranışa çevrildi. Yalnız test_intem_ileri.py ve test_k24_yeniden.py değişti; modüller (FON_IZI, INTEM_ILERI, K24_YENIDEN, ORTAK_CETVEL) ve defter dosyaları değişmedi.

## Değişen bölümler
test_intem_ileri.py
- Docstring madde 3: "SAPMA-1 gerekçesi (kesik seride erken pencere yok)" -> "önek değişmezliği + SAPMA-1 süzgeci (i >= L + 199) artık satır düşürmez (düşen 0)".
- Bölüm 2 sonu: yeni sınama `dusen` = 30 hissede fi_k23_parmak çıktısında i < L+199 satır sayısı; `dusen` ya da `erken` > 0 ise hata. bilgi'ye `sapma1_dusen` eklendi.
- Bölüm 3 (eski satır 93-96: `P0["i"] == L + 100` -> IndexError): kaldırıldı; yerine (a) tam seride i < L+199 satırı yok, (b) önek değişmezliği: T in (L+100, L+199, L+200, L+260, 450, N-1) için fi_k23_parmak(d.iloc[:T]) = tam serinin index <= d.index[T-1] satırları (yon60 / yon20 hariç, DataFrame.equals), ayrıca ii_pencereler kesik / tam tarih kümesi aynı. bilgi'ye `onek_satir`.
test_k24_yeniden.py
- Docstring madde 3: aynı biçimde güncellendi (ileri sütunlar yon60 / yon20 / r120 hariç).
- Bölüm 2 (eski satır 90-91 "SAPMA-1 örneği yok"): şart tersine çevrildi; K24_YENIDEN SAPMA-1 süzgecinin (t_i >= 199) düşüreceği satır `s1` 0 değilse hata.
- Bölüm 3 (eski satır 108-115 `s, t = ornek_s1` -> TypeError): kaldırıldı; yerine 10 hissede (a) tam seride t < 199 satırı yok, (b) önek değişmezliği: T in (150, 199, 200, 201, 350, 600, N-1) için fi_k24_tara(d.iloc[:T]) = tam serinin tarih <= d.index[T-1] satırları (yon60 / yon20 / r120 hariç).
- Dönüş sayacı: `sapma1` -> `sapma1_dusen`, `onek_satir` eklendi. Bölüm sayısı değişmedi (10/10).

## Sonuç
- test_intem_ileri: {'eslesme': 90, 'sapma1_erken': 0, 'sapma1_dusen': 0, 'onek_satir': 773, 'k45_n': 35, 'oc_olay': 238} / 10/10 GEÇTİ
- test_k24_yeniden: {'sentetik_sinyal': 61, 'sapma1_dusen': 0, 'onek_satir': 82, 'L1_kontrol': 27} / 10/10 GEÇTİ
- test_fon_izi 63/63, test_dip_col_ayrim 11 GEÇTİ, test_k64 15/15.
- Ters sınama: aynı testler HEAD'deki eski FON_IZI.py ile (scratchpad kopyası) kırmızı: INTEM pencere 6000 / eşleşme 45 düşen, önek 2 kesikte farklı; K24 3 hissede t < 199 satırı, önek 18 kesikte farklı. Yani yeni sınamalar eski geleceğe bakma hatasını yakalıyor.

## HATA
- Bulunmadı (yeni hata yok). Not: eski bölüm 2'deki `erken` / `ref_s1` hesabı artık boş küme üzerinde çalışıyor (her zaman 0 / ref); kaldırılmadı, yeni `dusen` sınamasıyla 0 olduğu denetleniyor.
