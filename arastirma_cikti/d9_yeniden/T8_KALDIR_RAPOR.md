# T8_KALDIR RAPORU — 'uzun çöl' (D9) etiketinin üretim ekranından kaldırılması (15 Kas 2026)

İş tanımı: arastirma_cikti/d9_yeniden/T8_KALDIR_IS_TANIMI.md. Yazan: alt ajan (yazıcı). Defter metni §7'de; defter dosyalarına dokunulmadı.

## 1. ÖZET
- takip.py gun(): BEKLE tablosundan 'uzun' sütunu kalktı; uzun_col_olc artık çağrılmaz. 'ruz%' ve ' RUZGAR' bayrağı aynen duruyor.
- COL_v1.py ruzgar_listesi(): uzun çöl süzgeci ve "uzun colde (...) N hisse" tablosu kalktı; sektör rüzgârı özeti (sektör sepeti, piyasa farkı, üyeler, AZ DUSEN) aynen basılıyor; başlık "=== D9 RUZGAR LISTESI" -> "=== SEKTOR RUZGARI". Dönüş artık rüzgârlı sektör tablosu (alt, sepet, ruz, uye; sepet büyükten küçüğe). Hisse listesi olmadığı için fon süzgeci burada uygulanmıyor (FON_ELE başka yerde değişmedi).
- COL_v1.py bugun_liste(): uzun_col_olc çağrısı ve 'uzun' sütunu kalktı ('ruz', 'ruzgar' kaldı).
- uzun_col_olc, UZUN_W / UZUN_BANT / UZUN_MUM / UZUN_KONUM, sektor_ruzgar, RUZ_*, SEKTOR_DOSYALAR DEĞİŞMEDİ (test_d9_yeniden 22/22).
- Başlık notları: COL_v1 D14, takip T12; her iki [ok] satırına "2026-11-15 D14/T12: uzun col etiketi kaldirildi" eki.
- Colab: COL_v1.py ve takip.py exec ile yüklenir -> **çalışma zamanını yeniden başlat**. Drive kopyalarını (col_tarayici kökü) ana model günceller.

## 2. DEĞİŞEN SATIRLAR (eski -> yeni)
COL_v1.py
- Başlık: D13 bloğunun sonuna "2026-11-15 D14: UZUN COL ETIKETI KALDIRILDI" notu (6 satır, yalnız yorum).
- ruzgar_listesi docstring: "D9: ruzgarli sektorlerde UZUN COLDE olan hisseler ... Fon suzgeci uygulanir" -> "D9/D14: sektor ruzgari ozeti ... Donus: ruzgarli sektor tablosu (alt, sepet, ruz, uye)".
- ruzgar_listesi gövdesi: hisse döngüsü (uzun_col_olc + fon_etiket + R listesi) silindi; piy / tum / _sepet_ozet / sekt yazdir bloğunun dışına alındı (değişmeden) ve t = sektör tablosu ['alt','sepet','ruz','uye'] (ruz = sepet - piyasa medyanı, uye = 60g getirisi olan üye sayısı).
- print "=== D9 RUZGAR LISTESI — ..." -> "=== SEKTOR RUZGARI — ..." (kalan metin aynı).
- Silindi: "ruzgarli sektorde uzun colde hisse yok", "uzun colde (dipte, ...) N hisse:" + tablo, "FON ELENDI: ..." (ruzgar_listesi içindeki).
- bugun_liste: `u = uzun_col_olc(df) or {}  # D9` silindi; R.append içinden `'uzun':u.get('uzun','')` silindi.
- [ok] satırı: "(2026-10-21 D13 ..." -> "(2026-11-15 D14: uzun col etiketi kaldirildi | 2026-10-21 D13 ...".
takip.py
- Başlık: T11'in altına T12 notu (3 satır yorum).
- `def _uz_rz(s, df)` (uzun_col_olc çağrısı + ruz) -> `def _rz(s)` (yalnız ruz ve var; ruz/var hesabı satır satır aynı); `return u, rz, var` -> `return rz, var`.
- `ucl,rz,var=_uz_rz(r.sembol,df)` -> `rz,var=_rz(r.sembol)`; rows tuple'ından ucl çıktı.
- BEKLE başlığı "(hisse  tavana%  girilecek%  doji  fitil  uzun  ruz%)" -> "(hisse  tavana%  girilecek%  doji  fitil  ruz%)"; satırdan `{ucl or '-':4s}  ` çıktı.
- RUZGAR_LISTE bloğu kodu aynı; yorum "# T8" -> "# T8/T12: sektor ruzgari ozeti" (çağrılan ruzgar_listesi artık sektör özeti).
- [ok] satırı: başa "2026-11-15 T12: uzun col etiketi kaldirildi | " eki.
test_takip.py
- Docstring'e T12/D14; 7 mevcut testten sonra 8a-8d eklendi (aşağıda). Mevcut 1-7 dokunulmadı.

## 3. ŞEMA KARARI ('uzun' sütunu)
- grep sonucu: 'uzun' anahtarını okuyan üretim kodu yok. bugun_liste dönüşü hiçbir yerde CSV / pkl'e yazılmıyor (yalnız ekrana basılıyor; çağıran yok: BASLAT / gh_gunluk / takip bugun_liste'yi çağırmıyor, KALIBRE yalnız docstring'de anıyor). takip CSV şemaları (A_KOL: sembol,eklendi,tavan,taban,bas,kural,doji,alt_fitil,dar,gecerli_oran,atr_ref; P_KOL, K_KOL) 'uzun' taşımıyor; takip_adaylar.csv başlığı da taşımıyor. v1_final_BIST.csv / yeni_BIST_2023.csv'deki 'uzunluk' farklı alan.
- rapor/*.txt eski ekran çıktıları (ör. "BEKLE (... uzun ruz%)", "ruzgarli sektorde uzun colde hisse yok") kod tarafından okunmuyor; tarihsel kayıt olarak dokunulmadı.
- KARAR: şema taşımadığı için sütun TAMAMEN kaldırıldı (boş dize bırakılmadı).
- uzun_col_olc'yi doğrudan çağıran öteki kod: GOZ_ESLE.py (araştırma, kendi ad alanında) ve D9_YENIDEN — fonksiyon durduğu için etkilenmez.

## 4. KONTROL LİSTESİ (K1-K14)
| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | Ölçüm yok; yalnız ekran / etiket kaldırma. |
| K2 | geleceğe bakma | UYGULANMAZ | Yeni bilgi alanı eklenmedi; sektor_ruzgar ve tarih kesimi değişmedi (test_d9_yeniden "geleceğe bakma: rüzgâr t'de kesilince aynı" OK). |
| K3 | geçerli bar | UYGULANMAZ | Bar / ölçü mantığı değişmedi. |
| K4 | tekilleştirme | UYGULANMAZ | Olay sayımı yok. |
| K5 | giriş fiyatı | UYGULANMAZ | AL kuralı / giriş değişmedi (test_takip 1-7 OK). |
| K6 | veri birimi | UYGULANMAZ | Veri okuma değişmedi. |
| K7 | hayatta kalma | UYGULANMAZ | Evren değişmedi. |
| K8 | örneklem ve dönem | UYGULANMAZ | Ölçüm yok; dayanak Ç181a (ana model kaydı). |
| K9 | ön kayıt | UYGULANMAZ | Ölçüm koşusu yok; iş tanımı değişiklikten önce yazılı (T8_KALDIR_IS_TANIMI.md). |
| K10 | ayrıştırma | UYGULANMAZ | Ham kaynak ayrıştırma yok. |
| K11 | yeniden üretim | EVET | Yeni testler HEAD sürümü (git show HEAD:COL_v1.py / takip.py, scratchpad kopyası) ile koşuldu: 8a, 8b, 8c HATA verdi (eski kod 'uzun' basıyor, uzun_col_olc 29 kez çağrıldı); yeni kodla 8a-8d OK. Testlerin değişikliği gerçekten yakaladığı gösterildi. |
| K12 | ifade | EVET | Raporda yalnız kod değişikliği; iz / emare sözü yok (dayanak kayıtları ana modelin). |
| K13 | süreç | EVET | Çakışma kapılarına dokunulmadı; "çalışma zamanını yeniden başlat" §1'de; git diff'te e-posta / anahtar taraması boş; yasak dosyalar değişmedi (§8 git status); commit / push / stash / checkout yapılmadı. |
| K14 | boyut (gerçek para) | UYGULANMAZ | Öneri / boyut işi değil; AL / SAT / çarpan mantığı değişmedi. |

## 5. TEST (çıktı son satırları)
test_takip.py (yeni 8a-8d dahil):
```
7 seans kapali tam bar: OK [{'neden': 'maliyet'}]
8a BEKLE uzun yok/ruz : OK BEKLE  (hisse  tavana%  girilecek%  doji  fitil  ruz%)   [tavana -8% icindekiler, toplam aday 1] | Y0       -3%   %12.0   0.2  0.1   +30  RUZGAR
8b ruzgar ozeti       : OK {'sektor_ruzgari': True, 'uzun_colde': False}
8c donus + cagri yok  : OK [{'alt': 'XYUKSELEN', 'sepet': 0.30000000000000004, 'ruz': 0.30000000000000004, 'uye': 5}] {'uzun_cagri': 0, 'bugun_liste_sutun': ['sembol', 'fon', 'ruz', 'ruzgar', 'bas']}
8d uzun_col_olc duruyor: OK
SONUC: HEPSI OK
```
- 8a: sentetik 13 hisse (5'i 'XYUKSELEN' sektöründe son 60 günde +%30, 8'i 'XDUZ' düz), takip_adaylar.csv'ye bir aday; gun(oneki='takip') ekranında BEKLE başlığında 'uzun' yok, 'ruz%' var, aday satırında ruz +30 ve RUZGAR bayrağı var.
- 8b: aynı gun() çıktısında "SEKTOR RUZGARI" ve rüzgârlı sektör var; "uzun colde" ve "D9 RUZGAR LISTESI" yok.
- 8c: ruzgar_listesi dönüşü ['alt','sepet','ruz','uye'] tablosu (XYUKSELEN, 5 üye, sepet 0,30); uzun_col_olc çağrı sayacı 0 (gun + ruzgar_listesi + bugun_liste); bugun_liste (sabit col_olc taklidiyle 13 aday) 'uzun' sütunu yok, 'ruz' / 'ruzgar' var ve RUZGAR etiketi tam 5 Y hissesinde.
- 8d: uzun_col_olc, UZUN_* ve RUZ_* COL_v1'de duruyor (UZUN_* = 250, 1.5, 0.04, 0.5).
- Eski kodla (HEAD) aynı test: "SONUC: HATA ['8a', '8b', '8c']".

test_d9_yeniden.py: "OK D9_PARAM == COL_v1 sabitleri", "OK d9_uzun_ref == COL_v1.uzun_col_olc (fark 0)", "OK d9_ruzgar_ref == COL_v1.sektor_ruzgar (fark 0)" ... "22 geçti, 0 kaldı".

COL_v1 / takip kullanan öteki testler (grep COL_v1|takip.py test_*.py, ayrıca iş tanımı listesindekiler; hepsi rc=0):
- test_col_dip2: 5/5 OK
- test_k64: TAMAM (15/15)
- test_ruzgar_defteri: SONUÇ: 0 hata — hepsi geçti
- test_tema_col: SONUÇ: 0 hata — hepsi geçti
- test_tema_sepet: SONUÇ: 0 hata — hepsi geçti
- test_vdyt2b: hepsi geçti
- test_veri_koru: 6/6 test geçti
- test_yeniden_tara: 7/7 test geçti
- test_vdyt: TAMAM (14/14) (logdaki Traceback testin kasıtlı hata yolu 'cikti_hata')
- test_vdyt2: TAMAM (16/16)
- test_vdyt_grafik: TAMAM (11/11)
- Sözdizimi: ast.parse COL_v1.py, takip.py, gh_gunluk.py, BASLAT.py -> ok.

## 6. HATA
- H-a (iş tanımı, süreç): T8_KALDIR_IS_TANIMI.md §3 TESTLER bölümü bozuk: içine test_d9_yeniden ve zincir_denetimi test çıktıları yapışmış, cümle ortadan kesilmiş ("10/10 test geçti (veri gerektiriyorsa ... yine de test_col_dip2.py ... ile bulduklarını koştur") ve "sözdizimi için ." boş kalmış. Etki: yok; listedeki testlerin hepsi ve grep ile bulunanlar koşuldu, sözdizimi ast ile denetlendi. Ders: iş tanımı dosyası yazıldıktan sonra okunup denetlenmeli.
- H-b (yorum, bilgi): COL_v1.py başlığındaki D9 notu (satır ~50-51: "bugun_liste(): adaylara 'uzun' ... sutunu; sonunda RUZGAR LISTESI: ruzgarli sektorlerde uzun colde olan TUM hisseler") ve takip.py T8 notu artık eski davranışı anlatıyor. Tarihsel not oldukları ve "yeniden yazma yok" kuralı yüzünden değiştirilmedi; D14 / T12 notları geçersiz kıldıklarını yazıyor.
- H-c (tasarım notu): ruzgar_listesi dönüşündeki 'ruz' ve 'uye' sektör düzeyindedir (sepet = tüm üyelerin ortalaması, ruz = sepet - piyasa medyanı); sektor_ruzgar'ın hisse düzeyi 'ruz' / 'uye' alanlarından (hisse hariç sepet) farklıdır. Ekrandaki "piyasa farkı" ile aynı tanım; karar etiketini (hisse RUZGAR) etkilemez.
- Kodda başka hata bulunmadı.

## 7. ÖNERİLEN DEFTER METNİ (ana model işler)
IK_GOREV: "2026-11-15 | T8_KALDIR (Cemal 'uzun çöl etiketini kaldır'; Ç181a D9 İZ DEĞİL) | COL_v1 D14 + takip T12: BEKLE 'uzun' sütunu, bugun_liste 'uzun' sütunu ve ruzgar_listesi uzun çöl hisse listesi kaldırıldı; ruzgar_listesi artık '=== SEKTOR RUZGARI' özeti, dönüş sektör tablosu (alt, sepet, ruz, uye). ruz% + RUZGAR bayrağı (Ç181c EMARE) aynen. uzun_col_olc / UZUN_* / RUZ_* değişmedi (test_d9_yeniden 22/22). Şema: 'uzun' hiçbir CSV/pkl'de yoktu -> tamamen kaldırıldı. test_takip 8a-8d eklendi (HEPSI OK; eski kodda 8a-8c HATA). Colab: çalışma zamanını yeniden başlat; Drive COL_v1.py ve takip.py güncellenecek (ana model)."

## 8. DOKUNULAN DOSYALAR
Bu işin değiştirdiği: COL_v1.py, takip.py, test_takip.py, arastirma_cikti/d9_yeniden/T8_KALDIR_RAPOR.md (yeni).
```
git status --short
 M .gitignore                 <- BU İŞİN DEĞİL (11:07, '!sektor_AVR.csv'; eşzamanlı D9_AVR işi)
 M COL_v1.py
 M takip.py
 M test_takip.py
?? D9_AVR.py                  <- BU İŞİN DEĞİL (11:08)
?? arastirma_cikti/d9_yeniden/T8_KALDIR_RAPOR.md
?? sektor_AVR.csv             <- BU İŞİN DEĞİL (11:07)
?? sektor_AVR_eslesme.md      <- BU İŞİN DEĞİL (11:07)
?? test_d9_avr.py             <- BU İŞİN DEĞİL (11:09)

git diff --stat
 .gitignore    |  1 +   (bu işin değil)
 COL_v1.py     | 52 +++++++++++++++++++++-------------------------------
 takip.py      | 23 ++++++++++++-----------
 test_takip.py | 54 +++++++++++++++++++++++++++++++++++++++++++++++++++++-
```
Yasak dosyalar (IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, D9_YENIDEN.py, ORTAK_CETVEL.py, test_d9_yeniden.py) değişmedi.
