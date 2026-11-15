# S6 Pine bağımsız denetimi (15 Kasım 2026)

Denetçi: bağımsız alt ajan B. Yazıcının raporu (S6_TASARIM.md) okunmadı. Dosyalar salt okundu; yalnız bu rapor yazıldı.
Girdiler: COL_S6_TABAN.pine (423 satır), COL_S6_TABAN_ascii.pine, S6_TABAN.py, S6_TABAN_IS_TANIMI.md §2 ve §5, COL_S5_OBEK.pine (derlenmiş kalıplar).
Derleyici yok. Sözdizimi satır satır okundu. Mantık için Pine'ın kendi bağımsız Python çevirim (TUT = 400 kırpma, idxOf, kutu ve çizgi işlemleri dahil) S6_TABAN.s6_taban ile gerçek BIST verisinde karşılaştırıldı.

## TOPLAM KARAR: ONAY
Derleme engeli ya da mantık farkı bulunmadı. Bloklamayan 4 iyileştirme önerisi aşağıda (biri belge, üçü yalnız çizim). Python ile Pine arasında ölçülmüş fark sıfır.

## Bağımsız sınama sonucu (kendi çevirim ile s6_taban karşılaştırması)
| koşu | hisse | bar | n farkı | AL farkı | KIRILDI farkı | kutu (sol / sağ / üst / alt / kenar rengi) farkı | kutu |
|---|---|---|---|---|---|---|---|
| varsayılan eşikler (rastgele 25 + ENJSA, PAPIL, TUCLK, KNFRT, DESA; tohum 11) | 30 | 67.311 | 0 | 0 | 0 | 0 | 1.706 |
| daralma AÇIK 0,8; bant 0,20; net 0,05; kM 1,00; dipTol 0,02 (rastgele 20 + 5; tohum 77) | 24 | 52.227 | 0 | 0 | 0 | 0 | 1.197 |
Geçersiz bar süzgeci de sınandı: Pine çevirisi ham (geçersiz barlar dahil) seride koştu, sonuç s6_taban'ın geçerli bar serisiyle eşleşti.
Beklenen çıktı yorumu (Pine satır 404-418): `python S6_TABAN.py liste TUCLK ...` ve `liste DESA ...` aynı tarihleri, uzunlukları, sınıfı, tavan / dibi verdi.
Betikler: /tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad/denetci_s6/pine_py.py, ikinci.py, uzun.py, asc_denet.py.

## 1. Pine v5 sözdizimi: GEÇTİ
- //@version=5 satır 30'da; önünde yalnız yorum var (S5'te de satır 91'de, derlendi; TradingView şablonu da lisans yorumuyla başlar). GEÇTİ.
- indicator (31): overlay, max_boxes / lines / labels_count = 500, tek satır. GEÇTİ.
- Girdiler (34-56): input.int / float / color / bool konumsal (defval, title) + adlı minval / maxval / step / group. GEÇTİ.
- Tipler ve var: dizi bildirimleri `var float[] x = array.new_float(0)` (66-73), `var box[] / line[]` (147-148), `var box kutu = na` (149), `var int x = na` (139, 142-144). GEÇTİ.
- `:=` yalnız önceden bildirilmiş adlara: global seri değişkenler (114-124) ve var'lar (127-150) yerel bloklarda `:=` ile değişiyor; fonksiyon içinde global değiştirilmiyor (ekle / ekleI yalnız dizi içeriğini değiştirir; S5 162-170 aynı). `nGec += 1` (163) global if bloğunda (S5 263 aynı). GEÇTİ.
- Gölgeleme: yerel adlar (i, sz, nn, hh, c1-c5, l1, med, wm, b, sinirY, solBar, ...) hiçbir global adla çakışmıyor; fonksiyon yerelleri j0 / sz0 / pos1 ayrı. Yerelde tanımlanan bir ad dışarıda kullanılmıyor (tablo yalnız global tN, tTav, tDip, vMed, vL1, vL2, atrP, rSinif, kutuBasZ ... okur). GEÇTİ.
- Girinti: bütün kod satırları 4'ün katı; tab 0, CR 0; sarmalı (devam) satır yok (kendi betiğimle tarandı; "devam?" çıkan 7 satır `=>` ile biten fonksiyon başlıkları). GEÇTİ.
- Üçlüler: 97, 102, 105, 108, 111, 153, 154, 160 (`na(cOnce) ? na : trv / cOnce`; S5 493'te aynı kalıp derlendi), 212, 235, 247, 255, 263, 272, 286, 310-311, 335-336, 367-391 dalları aynı tip. GEÇTİ.
- Fonksiyonlar (76-111): son ifade dönüş; sonOrt float / na, idxOf int, tarih / yz / sinifAd string. tarih ve yz S5 186-187, 452 ile birebir. GEÇTİ.
- Dizi imzaları: array.new_float(nMax + 1, na) (170-171), get / set / push / shift / size / sort(order.ascending) (210). İndeks aralıkları: ölçülür barda sz = min(nGec, 400) >= atrGun + 1 >= 101; satır 60 runtime.error nMax + daralmaGun <= atrGun, konum / SMA+eğim / hacim+1 <= atrGun + 1 şartını koyduğu için en küçük indeksler (sz - nn - daralmaGun, sz - smaGun - smaEgimGun, sz - 1 - hacimGun, sz - konumGun) >= 0; sufL[nn - hh] için nn - hh >= 2 <= nMax. Tablo 350 `size > tN + daralmaGun` korumalı. GEÇTİ.
- int / float karışımı: math.max / math.min int-int (287, 291, 300, 306) ve float-float (154, 175-176, 190, 228, 233-234, 301-302); `int(nn / 2)` (182, 211) Pine'ın int bölme kuralından bağımsız doğru (S5 279 aynı). GEÇTİ.
- Döngüler: hepsi yukarı sayar, alt <= üst garantili (174: 1..nMax; 180: 0..nMax-nMin; 189: hh >= 2; 196-260 sınırlar yukarıdaki indeks şartıyla). `by -1` yok. `break` (219) yalnız `for kk` içinde (S5 418 derlendi). Aynı blokta art arda iki `for j` (196, 199) geçerli (döngü sayacı döngüye yereldir). GEÇTİ.
- Çizim: box.new(sol int, üst, sağ bar_index, alt, adlı border_color / border_width / bgcolor / text / text_size / text_color / text_halign=text.align_left / text_valign=text.align_top) (312); box.set_right / left / top / bottom / text / border_color / border_width; line.new(x1, y1, x2, y2, color=, width=) (317); line.set_x2 / set_xy1 / set_xy2; box.delete / line.delete(array.shift(...)) (315, 320). Hepsi xloc.bar_index (varsayılan) ile int bar_index. GEÇTİ (bkz. kalan risk).
- plotshape (338-339) GLOBAL, girintisiz, her bar çağrılır; argüman sırası series, title, style, location, color + adlı size / text. bgcolor / plot / hline yok. GEÇTİ.
- table.new (341) var ile bir kez; table.cell(tb, sütun, satır, metin, text_size=) yalnız `gosterTab and barstate.islast` içinde (342); 2 x 15 tablo, satır 0-14 kullanılıyor. GEÇTİ.
- runtime.error(mesaj) (61) `barstate.isfirst` içinde. GEÇTİ.
- Türkçe karakter: kaynakta yalnız yorum ve dizelerde; kod kısmında ASCII dışı 0. GEÇTİ.
- Kalan risk (derleyici yok): S5'te derlenmemiş, ama v5 belgesinde olan yapılar: line.* (new, set_x2, set_xy1, set_xy2, delete), array.new_line, box.new'in text_* parametreleri, box.set_text / set_left / set_border_color / set_border_width, runtime.error. İmzaları v5 başvurusuna uyuyor; hata beklemiyorum, ama ilk yapıştırma bu satırlar için gerçek derleme sınamasıdır (312, 317, 323-329, 61).

## 2. Mantık birebirliği (Pine ile Python s6_taban): GEÇTİ
- Geçerli bar (64): high > low, volume > 0 (na değil), close > 0, open > 0 = SY.sy_veri_hazirla (H > L, V > 0, C > 0, O > 0, sonlu). GEÇTİ.
- ATR% (153-160, 168): TR = max(H, önceki geçerli C) - min(L, önceki geçerli C), / önceki geçerli C; ilk bar na; son atrGun değerin basit ortalaması, bir na varsa na = Python rolling(250, min_periods=250).mean(); ddof yok (ortalama). GEÇTİ.
- (1) bant 183: sonek max H / min L (172-178; sufH[k] = son k barın en yükseği) = rolling max / min. GEÇTİ.
- (2) sakin 184: C_t / aC[sz - n] = C_{i-n+1}. GEÇTİ.
- (3) dip 187-191: h = int(n / 2) = n // 2; L1 = min L [i-n+1, i-n+h]; L2 = sufL[n-h] = min L son n-h bar. GEÇTİ.
- (5) daralma 193-203: pencere ortalaması ve [i-n-59, i-n] ortalaması = Python ortW ve ortOnce (once kaydırma n); oran 0 -> şart yok. GEÇTİ (daralma AÇIK koşusunda da fark 0).
- (4) medyan 206-213: sıralı dizide tek n orta, çift n iki ortanın ortalaması = pandas rolling median; <= kM x ATR%. GEÇTİ.
- En büyük n: kk = 0.. ile n = nMax - kk, ilk tutanda break = Python argmax (n azalan sırada). GEÇTİ.
- Tavan / dip 220-228: ilk en yüksek High (sıkı `>`) = np.argmax; dip = min L. GEÇTİ.
- AL 250: önceki ölçülür geçerli barın tavanı na değil ve C > tavan(t-1); KIRILDI 251: AL değil ve C < dip(t-1) x (1 - kirTol). oncTav / oncDip yalnız ölçülür barda güncellenir (335-336) = Python (olculur değilse continue). GEÇTİ.
- Durum makinesi 252-334 = s6_durum: AL / KIRILDI açık bölgeyi kapatır (dogal = false), açık yoksa bölgesiz; taban varsa SÜRER / YENİDEN (dogal ve b <= rSon) / YENİ (sinir = rSon, kırpılmış kutu >= nMin) / KISA; taban yoksa SÖNDÜ. Pine 286 `rid >= 0 ? rSon : -1` Python'un `rSon if (rid >= 0 and not acik)` ile aynı (o dalda acik zaten false). GEÇTİ.
- Sınıf 230-247: konum ve tepe düşüşü son 120 geçerli kapanış (bugün dahil); SMA50 ve 20 bar önceki SMA50 = Python. GEÇTİ.
- AL mumu hacmi 258-263: önceki 20 geçerli bar ortalaması = Python hort (kaydırma 1). GEÇTİ.
- Bölge sürekliliği: Pine = Python varsayılanı (surTol = -1, 'birleşim': açık bölge taban sürdükçe sürer, pencere başlangıcı oynasa da). ŞÜPHELİ (ana model kararı): iş tanımı §2'nin harfi "başlangıç aynı (ya da ±2 bar) ise aynı bölge; başlangıç değişirse yeni bölge" diyor. Python bunu yalnız bilgi kipi (surTol >= 0) olarak tutuyor; Pine'da yok. Pine ile Python arasında fark değil, iş tanımından SAPMA; ana model onaylamalı ya da sapma olarak kaydetmeli.
- Küçük parametre farkı: Python s6_prm dipTol = 0 ve kirTol = 0'ı reddeder; Pine girdileri minval=0.0 ile kabul eder (38, 41). Varsayılanlarda etkisiz.

## 3. Geleceğe bakma ve tekrar boyama: GEÇTİ (belge için ŞÜPHELİ)
- Pine'da `[k]` geçmiş başvurusu, request.security, negatif kaydırma yok; bütün hesap t ve öncesindeki geçerli bar dizilerinden. Python önek değişmezliği testi (test_s6_taban.py) ve Pine çevirisinin s6_taban ile sıfır farkı birlikte geleceğe bakma olmadığını gösterir. GEÇTİ.
- Kutu sol kenarı sonradan sola kayabilir (rBas = pencere başlangıçlarının en eskisi; bilgi t'de belli, ama çizim geçmişe doğru değişir): PINE_S6_NASIL.md satır 19 söylüyor. GEÇTİ.
- Son (açık) mum: barstate.isconfirmed kullanılmıyor. Gün içinde kapanış tavanı geçerse AL üçgeni, kutu kapanışı ve yeşil kenar o tikte görünür; fiyat geri inerse kaybolur (var dizileri ve çizimler her tikte geri alınır, birikme yok). Seans içinde yarım bar 'geçerli' sayılır (K3 dersi). PINE_S6_NASIL.md bunu SÖYLEMİYOR. ŞÜPHELİ: belgeye bir madde gerek.

## 4. Kaynak sınırları: GEÇTİ
- Kutu ve çizgi 480'de en eski silinir (314-315, 319-320), sınır 500. Etiket kullanılmıyor. GEÇTİ.
- İşlem sayısı (kendi çevirimdeki sayaç, bar başına): ortalama ~660, %99 dilim ~1.100, en çok ~12.000 (varsayılan); daralma açık / gevşek eşiklerde ortalama ~940, en çok ~8.100. Pahalı kısım (sıralama ile medyan) yalnız (1)-(3) tutan n'lerde çalışıyor. 5.000-10.000 günlük barda toplam birkaç on milyon basit işlem: 'loop takes too long' (500 ms / bar) ve toplam süre sınırının çok altında. Önbellek gerekmiyor. GEÇTİ.
- idxOf kırpması (99-102): bölge 400 geçerli bardan uzun sürerse sol kenar / kutu başlangıç tarihi dizinin ilk elemanına kırpılır (yanlış sol kenar). BIST evreninde (V_BIST, 32.668 bölge) en uzun bölge 206 bar, 400 üstü 0. Yalnız çizim; ŞÜPHELİ (düşük).

## 5. ASCII kopya: GEÇTİ
- 424 / 424 satır (son satır sonu dahil); ASCII dışı karakter 0 (`grep -P '[^\x00-\x7F]'` 0 satır); dize ve yorum dışı kod kaynakla birebir (kendi betiğim: dize içleri maskelenip yorumlar atıldıktan sonra fark 0 satır); dize sayıları aynı. Kaynakta kod kısmında ASCII dışı 0.

## 6. Python tarafı: GEÇTİ
- `python test_s6_taban.py` (S6_VERI = scratchpad/veri): 50/50 TAMAM (Pine aynası = vektörel 4 gerçek hissede, önek değişmezliği, Pine girdi varsayılanları = S6_PRM, ASCII, e-posta / anahtar yok).
- S6_TABAN.py, test_s6_taban.py, .pine ve PINE_S6_NASIL.md'de e-posta / anahtar / token yok (grep; tek eşleşme testteki yasak kalıbın kendisi).
- Çakışma kapısı var: _CK_ONCE_S6 (dosya başı), _cakisma_kontrol_s6 (914-925), modül sonunda çağrı (928).
- git status: temiz (denetim dosya değiştirmedi; bu rapor hariç).

## DÜZELTME GEREKEN SATIRLAR (hiçbiri derleme ya da mantık engeli değil)
| dosya / satır | sorun | önerilen düzeltme |
|---|---|---|
| PINE_S6_NASIL.md 'Okurken dikkat' | Son mum kapanmadan AL / KIRILDI ve kutu kapanışı geçicidir; seans içinde yarım bar hesaba girer; belgede yok | Madde ekle: "AL / KIRILDI son mum KAPANINCA kesinleşir; seans içinde görünen üçgen fiyat geri inerse kaybolur. Karar için günlük kapanıştan sonra bak." |
| COL_S6_TABAN.pine 99-102, 304, 306 | Bölge > 400 geçerli bar sürerse idxOf ilk elemana kırpar: sol kenar / başlangıç tarihi yanlış (BIST'te görülmedi, en uzun 206) | rBas değiştiği anda (291, 300) `var int rBasBar` / `var int rBasZ` olarak bar_index ve time'ı sakla; ya da TUT'u 400'den nMax + atrGun'dan bağımsız büyük yap. Yalnız çizim. |
| COL_S6_TABAN.pine 328 | Tavan çizgisi o günkü pencerenin tavan mumundan başlar; pencere önceki kutunun içine taşıyorsa (b < sinir + 1) çizgi kutunun solundan dışarı taşar ve çizgi kutu üstünden (rTop) aşağıda kalabilir | Bilinçli ise (çizgi = AL eşiği = tavan(t-1)) PINE_S6_NASIL.md'ye "yeşil çizgi = bugünkü AL eşiği, kutunun üstü = bölgenin en yükseği; ikisi ayrı olabilir" yaz; değilse x1'i math.max(tavBar, solBar) yap. |
| S6_TABAN_IS_TANIMI.md §2 'BÖLGE SÜREKLİLİĞİ' ile Pine / Python | Uygulanan kural (birleşim: taban sürdükçe aynı bölge) iş tanımının harfinden (başlangıç ±2 bar) farklı | Ana model: sapmayı onayla ve kaydet ya da surTol kipini Pine'a taşıt. Pine-Python farkı DEĞİL. |
Kozmetik (düzeltme şart değil): str.tostring(x, "#.0") / "#.00" biçimi 1'den küçük değerlerde başta sıfırsız (".9") basabilir (S5'te de aynı); "0.0" / "0.00" daha okunaklı. §2'de "dip çizgisi" isteniyor, Pine'da dip yalnız kutunun alt kenarı.

## HATA
- Pine kodunda derleme ya da Python'dan ayrışma hatası BULUNMADI (iki eşik setinde 119.538 bar, 2.903 kutu, fark 0).
- H-1 (belge / süreç): PINE_S6_NASIL.md gün içi tekrar boyamayı (açık mumda geçici AL) yazmıyor; K3 'seans açıkken yarım bar' dersiyle aynı tür.
- H-2 (tanım sapması, ana model kararı): bölge sürekliliği iş tanımı §2'nin harfinden farklı (birleşim kipi); Python docstring'de 'yalnız bilgi kipi' olarak geçiyor, K9 uyarısındaki üç düzeltme arasında sayılmamış.
- H-3 (çizim, düşük): idxOf 400 bar kırpması; uzun bölgede sol kenar yanlış olur (BIST'te tetiklenmedi).
