# T8_KALDIR — bağımsız denetim (15 Kas 2026)

Denetçi: bağımsız sınayıcı alt ajan. Yazıcı raporu okunmadı. Denetlenen: commit edilmemiş `git diff HEAD -- COL_v1.py takip.py test_takip.py`.
Eski kod: `git show HEAD:...` kopyaları scratchpad'de. Hiçbir repo dosyası değiştirilmedi (bu rapor dışında).

| # | Madde | Sonuç | Kanıt |
|---|---|---|---|
| 1 | Yasaklar | GEÇTİ | `git status`: değişen M COL_v1.py, takip.py, test_takip.py (+ .gitignore `!sektor_AVR.csv` ve ?? D9_AVR/sektor_AVR/test_d9_avr: başka iş, sayılmadı). `git diff HEAD --quiet -- IZ_DEFTERI.md IZ_KARNE.py CLAUDE.md COL_OZET.md ONERI_DEFTERI.md D9_YENIDEN.py ORTAK_CETVEL.py test_d9_yeniden.py` -> değişmedi |
| 2 | Değişmezler (ast) | GEÇTİ | uzun_col_olc, sektor_ruzgar, UZUN_W/BANT/MUM/KONUM, RUZ_GERI/ESIK/MIN_UYE/MUTLAK/BAYAT, SEKTOR_DOSYALAR, RUZGAR_LISTE: ast.dump HEAD ile AYNI. Değişen fonksiyonlar yalnız COL_v1 {bugun_liste, ruzgar_listesi}, takip {gun} |
| 3 | Davranış | GEÇTİ | gun(): `BEKLE  (hisse  tavana%  girilecek%  doji  fitil  ruz%)` / `Y0 -3% %12.0 0.2 0.1 +30  RUZGAR`; çıktıda 'SEKTOR RUZGARI' var, 'uzun colde' ve 'D9 RUZGAR LISTESI' yok; bugun_liste sütunları ['sembol','fon','ruz','ruzgar','bas',...], 'uzun' yok, RUZGAR yalnız 5 rüzgârlı hissede; uzun_col_olc çağrı sayacı 0 (eski kodda 29) |
| 4 | Kenar durumlar | GEÇTİ | yazdir=False: sütunlar ['alt','sepet','ruz','uye'], [{'alt':'XA','sepet':0.4,'ruz':0.7,'uye':6}], ekrana hiçbir şey basmadı; rüzgârsız: boş DataFrame (sütunlu), başlık "0 sektor", çökme yok; sektor_ruzgar istisna: "[col] ruzgar hesaplanamadi: yapay", boş DataFrame; ruzgar_listesi(V, n=40) çalışıyor; tablo sektörleri = sektor_ruzgar 'ruzgar' etiketli alt ['XA']; sektör özet satırları eski kodla birebir aynı (yalnız başlık değişti) |
| 5 | Tüketici kalıntısı | GEÇTİ | grep: _uz_rz yok; ruzgar_listesi dönüşünü kullanan yok (yalnız COL_v1:851/860 ve takip:303 dönüşsüz çağrı); bugun_liste çıktısını okuyan kod yok; 'uzun' anahtarını okuyanlar GOZ_ESLE.py:367 ve D9_YENIDEN (uzun_col_olc'yi doğrudan çağırır, etkilenmez); takip_*.csv başlıklarında 'uzun' yok; gh_gunluk.py / BASLAT.py'de uzun/ruz/BEKLE ayrıştırması yok |
| 6 | Testler | GEÇTİ | test_takip: SONUC: HEPSI OK (8a-8d OK); test_d9_yeniden: 22 geçti, 0 kaldı; test_col_dip2 5/5, test_k64 15/15, test_ruzgar_defteri 0 hata, test_tema_col 0 hata, test_tema_sepet 0 hata, test_vdyt 14/14, test_vdyt2 16/16, test_vdyt2b hepsi, test_vdyt_grafik 11/11, test_veri_koru 6/6, test_yeniden_tara 7/7. Yeni test_takip HEAD koduyla: `SONUC: HATA ['8a','8b','8c']` (KIRMIZI; 8d değişmezlik sınaması olduğu için eski kodda da yeşil, beklenen) |
| 7 | ast.parse + sızıntı | GEÇTİ | COL_v1, takip, BASLAT, gh_gunluk, test_takip ast OK; diff'te e-posta / anahtar / token deseni yok |
| 8 | Eski davranış yorumları | NOT (düzeltme yapılmadı) | aşağıda |

## 8. Kalan eski yorumlar (tarihsel değişiklik günlüğü; D14/T12 notu üstlerine yazılmış)
- COL_v1.py:50-51 — "bugun_liste(): adaylara 'uzun' (6ay/12ay) ... sonunda RUZGAR LISTESI: ruzgarli sektorlerde uzun colde olan TUM hisseler".
- COL_v1.py:152 — `UZUN_W` yorumu "120 ~ 6 ay da raporlanir" (artık ekranda raporlanmıyor; sabit satırı değişmez kuralı altında, dokunulmamalı).
- COL_v1.py [ok] print: D14 öneki eklendi ama "2026-10-18 D9: uzun col {UZUN_W} bar + sektor ruzgari ..." parçası duruyor.
- takip.py:25-28 — T8 notu "BEKLE satirlarina 'uzun' (6ay/12ay) ... eklenir".
- takip.py [ok] print: "2026-10-18 T8: D9 uzun col + ruzgar ekranda" parçası duruyor.
Hepsi tarihli günlük satırı; D14/T12 notu ve [ok] öneki kaldırıldığını açıkça yazıyor. Yanıltma riski düşük; istenirse [ok] satırlarındaki eski parça "(D14'te kaldirildi)" ile işaretlenebilir.

## HATA
- Engelleyici hata bulunmadı.
- Küçük not (hata değil): ruzgar_listesi, sektor_ruzgar istisna verdiğinde ya da boş döndüğünde sütunsuz `pd.DataFrame()` döndürür (eski davranış korunmuş); docstring'deki "(alt, sepet, ruz, uye)" şeması bu iki yolda yok. Dönüşü kullanan çağıran olmadığı için etkisi yok.
- Küçük not: `_sepet_ozet(a)` tablo kurulurken her sektör için 3 kez hesaplanıyor (verim; sonuç doğru).

## Karar: ONAY
Colab hatırlatması: COL_v1.py / takip.py exec ile yüklendiği için Drive kopyaları güncellenince çalışma zamanı yeniden başlatılmalı.
