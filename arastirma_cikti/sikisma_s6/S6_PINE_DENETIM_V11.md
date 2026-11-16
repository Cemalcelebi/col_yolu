# S6 v1.1 Pine bağımsız denetimi (16 Kasım 2026)

Denetçi: bağımsız alt ajan (B). Yazıcının raporu (S6_TASARIM.md v1.1 bölümü) OKUNMADI. Dosyalar salt okundu; yalnız bu rapor yazıldı.
Girdiler: COL_S6_TABAN.pine v1.1 (542 satır), COL_S6_TABAN_ascii.pine, S6_TABAN.py v1.1, S6_TABAN_IS_TANIMI.md §2, S6_V11_IS_TANIMI.md, v1.0 Pine (git beb8615), v1.0 Python (git beb8615:S6_TABAN.py), S6_PINE_DENETIM.md (v1.0 yöntemi).
Yöntem: derleyici yok. Pine satır satır okundu; Pine'ın kendi bağımsız Python çevirisi yazıldı (TUT = 400 kırpma, idxOf, ham seri = geçersiz barlar dahil, dolu + kesik kutu, tavan çizgisi, tarih etiketi, sönme etiketi ve canlanınca silinmesi, onay elması) ve S6_TABAN.s6_taban ile gerçek BIST verisinde (V_BIST) karşılaştırıldı.
Betikler: /tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad/denetci_s6_v11/ (pine11.py çeviri, kars.py karşılaştırma, hisse.py, bbkars.py, refkars.py, onek.py, kisa.py).

## TOPLAM KARAR: ONAY
Derleme engeli, mantık farkı, geleceğe bakma bulunmadı. Beş kip, 137 hisse-koşu, 308.160 ham bar, 5.710 kutuda Pine çevirisi ile Python arasında fark 0. Düzeltme şart olan kod satırı yok; 3 belge / bilgi notu var (aşağıda).

## Karşılaştırma (kendi Pine çevirim ile s6_taban)
Karşılaştırılan: n (ölçülür bar), AL, KIRILDI, onay günü, BB yüzdeliği (bit düzeyinde eşitlik), dolu kutu [onay, sağ, üst, alt], kesik kutu [sol, onay, üst, alt], kenar rengi (AL yeşil / KIRILDI kırmızı / SÖNDÜ gri / AÇIK sınıf), tavan çizgisi (x1, y, x2), tarih etiketi (x, y, ilk .. son), sönme etiketleri (yer; canlanan bölgenin etiketi silinmiş mi), geçersiz barda işaret.

| koşu | hisse | ham bar | kutu | sönme etiketi | fark (bütün alanlar) |
|---|---|---|---|---|---|
| v1.1 varsayılan (refOnce, BB 0,30; rastgele 24 tohum 11 + ENJSA, PAPIL, TUCLK, KNFRT, DESA, CCOLA) | 30 | 67.312 | 1.083 | 454 | 0 |
| gevşek: refOnce, BB 0,15, daralma 0,8, bant 0,20, net 0,05, kM 1,00, dipTol 0,02 (tohum 77) | 25 | 55.090 | 554 | 286 | 0 |
| refOnce KAPALI, BB 0,20 (tohum 5) | 26 | 61.080 | 815 | 356 | 0 |
| refOnce AÇIK, BB KAPALI (tohum 9) | 26 | 57.366 | 1.546 | 500 | 0 |
| v1.0 kipi (refOnce ve BB kapalı) Pine v1.1 çevirisi vs git v1.0 Python (n / AL / KIRILDI / kutu [sol, sağ, üst, alt]) | 30 | 67.312 | 1.712 | - | 0 |

v1.1 varsayılan koşu, hisse bazında (fark = bütün alanların toplamı):

| hisse | ham bar | geçerli bar | kutu | AL | KIRILDI | sönme | fark |
|---|---|---|---|---|---|---|---|
| SAFKR | 2176 | 2144 | 38 | 15 | 2 | 21 | 0 |
| YKSLN | 1646 | 1640 | 25 | 9 | 6 | 10 | 0 |
| SEKUR | 2863 | 2800 | 36 | 12 | 4 | 20 | 0 |
| RYSAS | 2863 | 2817 | 45 | 20 | 7 | 19 | 0 |
| TMPOL | 2861 | 2812 | 43 | 24 | 3 | 17 | 0 |
| ENSRI | 1110 | 1099 | 8 | 3 | 2 | 3 | 0 |
| EMNIS | 2862 | 2572 | 42 | 19 | 10 | 15 | 0 |
| TRALT | 2862 | 2815 | 48 | 24 | 8 | 18 | 0 |
| SMART | 1829 | 1813 | 30 | 11 | 6 | 12 | 0 |
| ENDAE | 384 | 384 | 1 | 0 | 0 | 1 | 0 |
| BLUME | 2863 | 2814 | 45 | 19 | 6 | 22 | 0 |
| RODRG | 2863 | 2792 | 43 | 15 | 6 | 22 | 0 |
| KGYO | 2863 | 1823 | 31 | 10 | 3 | 19 | 0 |
| DENGE | 2862 | 2763 | 54 | 24 | 9 | 23 | 0 |
| BIOEN | 1334 | 1329 | 22 | 11 | 4 | 7 | 0 |
| VAKBN | 2862 | 2815 | 53 | 37 | 6 | 16 | 0 |
| ARASE | 1203 | 1196 | 20 | 15 | 5 | 6 | 0 |
| ORCAY | 987 | 986 | 11 | 5 | 2 | 5 | 0 |
| DOFER | 719 | 709 | 9 | 2 | 1 | 6 | 0 |
| AKCNS | 2862 | 2812 | 54 | 23 | 12 | 21 | 0 |
| TURSG | 2863 | 2815 | 59 | 34 | 13 | 18 | 0 |
| AYCES | 2862 | 2589 | 44 | 20 | 2 | 22 | 0 |
| AVGYO | 2862 | 2815 | 47 | 24 | 7 | 18 | 0 |
| ALTNY | 573 | 564 | 6 | 2 | 2 | 2 | 0 |
| ENJSA | 2159 | 2136 | 38 | 28 | 5 | 12 | 0 |
| PAPIL | 1669 | 1662 | 23 | 10 | 2 | 11 | 0 |
| TUCLK | 2862 | 2812 | 53 | 23 | 5 | 26 | 0 |
| KNFRT | 2862 | 2816 | 49 | 22 | 10 | 20 | 0 |
| DESA | 2863 | 2807 | 49 | 28 | 2 | 22 | 0 |
| CCOLA | 2863 | 2816 | 57 | 40 | 7 | 20 | 0 |

KGYO (1.040 geçersiz bar) ve EMNIS geçersiz bar süzgecini, ENDAE (< 400 bar) tampon kırpılmadan önceki kenarı sınadı. Canlanma (YENIDEN) var: 8 hissede 134 bar; canlanan bölgelerin sönme etiketleri silinmiş, yalnız SÖNDÜ biten bölgelerinkiler kalmış (fark 0).

## 1. Pine v5 sözdizimi: GEÇTİ
- //@version=5 (37; önünde yalnız yorum), indicator (38) tek satır, max_boxes / lines / labels = 500. GEÇTİ.
- Girdiler (41-72): input.int / float / bool / color; yeni bool girdiler (48, 51, 72) ve int / float girdiler (49-55) v5 imzasıyla. GEÇTİ.
- Yeni diziler / var'lar (92-95, 175, 179-187): `var float[] aCum`, `var float[] aBB`, `var float cumT = 0.0`, `var box[] kesikler`, `var label[] tarihler / sonmeler = array.new_label(0)`, `var box kesik = na`, `var label tarihEt / sonmeEt = na`. GEÇTİ.
- Yeni fonksiyonlar kenarRenk / solukRenk (134-138): int -> color üçlüsü. GEÇTİ.
- Ad çakışması (betikle tarandı): yerel adların hiçbiri global ad ya da fonksiyon parametresiyle çakışmıyor; global iki kez tanım yok; tanımsız atama yok; kullanılan bütün adlar tanımlı ya da Pine yerleşiği. GEÇTİ.
- Kullanılan bütün nokta-adları v5'te var: box.new / set_left / set_right / set_top / set_bottom / set_text / set_border_color / set_border_width / delete; line.new / set_x2 / set_xy1 / set_xy2 / delete / style_dashed; label.new / set_xy / set_text / delete / style_label_down / style_label_upper_left; array.new_label / pop / shift / push / sort; xloc.bar_index; yloc.price / abovebar; shape.diamond / triangleup / xcross; color.purple; runtime.error; table.new / cell. GEÇTİ.
- box.new sıfır genişlik (395: sol = sağ = bar_index): geçerli (dikey çizgi gibi çizilir, sonra set_right ile uzar). GEÇTİ.
- box.new border_style=line.style_dashed (400): box.new'in adlı parametresi, line.style_* sabitini alır. GEÇTİ.
- label.new (410, 444): (x, y, text, xloc=, yloc=, color=, style=, textcolor=, size=) adlı. yloc.abovebar ile y yok sayılır (sorun değil). GEÇTİ.
- label.set_xy(id, x, y) (426), label.set_text (352, 427), label.delete (413, 432, 447). GEÇTİ.
- array.pop (434) deyim olarak (dönüş değeri kullanılmadan) geçerli; `array.size > 0` korumalı. Silinen etiketin dizinin SON elemanı olduğu kanıtlandı: sönme yalnız açık bölgede olur, açık bölge yalnız yeni ya da canlanma ile açılır; yeni bölgede sonmeEt := na (415). GEÇTİ.
- plotshape (452-454) global, girintisiz; onay: shape.diamond, location.belowbar, size.tiny. Onay günü AL günüyle çakışamaz (AL barı yeni bölge açmaz). GEÇTİ.
- table 2 x 17 (456), satır 0-16 kullanılıyor (479-512). GEÇTİ.
- runtime.error (77, 79) barstate.isfirst içinde; 78: refMin <= refGun, nMax + refGun <= 399, bbDagilim <= 399. GEÇTİ.
- int / float: `say * 1.0 / bbDagilim` (229) float; `smB / bbGun`, `vsB / bbGun` (212, 217) float; `int cnt = math.min(refGun, i - nn)` (281) int; `(...) / cnt` (283) float; `int(nn / 2)` Pine int bölme kuralından bağımsız doğru. GEÇTİ.
- `if bbOk` altındaki n döngüsü ve break (246-294): break `for kk` içinde, `if c4` altında (v1.0'da ve S5 v1.2'de aynı yapı). GEÇTİ.
- Döngü yönleri: bütün for'lar yukarı sayar ve alt <= üst garantili: 112 (m >= 100), 210 / 214 (bbGun >= 5), 223 (bbDagilim >= 20), 239, 247 (nMin <= nMax runtime.error ile), 256 (hh >= 2), 263 / 266 (daralmaGun >= 10), 275, 299, 307, 313, 317, 334, 472, 475. `by -1` yok. GEÇTİ.
- İndeks sınırları: aCum[sz-1-nn-cnt] >= 0 (nn + cnt <= nMax + refGun <= 399 ve nGec <= 400 iken cnt <= i - nn); aBB[szP-1-bbDagilim] (szP > bbDagilim korumalı); öteki indeksler v1.0 ile aynı. TUT kırpması çevirimde aynen var, fark 0. GEÇTİ.
- na kontrolleri: na(bbP) (245), na(bw) (220), na(vB) (225), na(kutu) / na(tavCizgi) / na(tarihEt) (345, 349, 351), na(sonmeEt) (431), na(vRef) (469). GEÇTİ.
- Sarmalı satır / tab / CR: 0 (betik; "devam?" çıkan 9 satır `=>` ile biten fonksiyon başlıkları). Girinti 4'ün katı. Kod kısmında ASCII dışı karakter 0. GEÇTİ.
- Kalan risk (derleyici yok): S5 / v1.0'da derlenmemiş, v5 başvurusuna uyan yeni yapılar: label.* (new, set_xy, set_text, delete, style_label_upper_left), array.new_label / array.pop, box.new border_style, shape.diamond. Hata beklemiyorum; ilk yapıştırma bu satırlar için (395, 400, 410, 426, 434, 444, 454) gerçek derleme sınamasıdır.

## 2. Mantık birebirliği: GEÇTİ
- BB yüzdeliği (205-229): bbw = 2 x bbK x sqrt(sum (C - ort)^2 / bbGun) / ort (std bölen bbGun = ddof 0), sıralı toplam; bbP = önceki bbDagilim (250) bbw değerinden bugünküne <= olanların payı; içlerinde na varsa na. ta.percentrank yok. Python s6_bb ile bit düzeyinde aynı (fark 0). SIKISMA_OBEK.so_s5 tanımıyla (bb_gun 20, bb_k 2, ddof 0, dağılım 250, `<=` payı) aynı tanım. GEÇTİ (sayısal not aşağıda, B-2).
- Referans ATR% (280-285): cnt = min(refGun, i - n); ref = (cum[i-n] - cum[i-n-cnt]) / cnt = ortalama TR/C_önceki, aralık [i-n-249, i-n] (250 bar; pencerenin hemen öncesi); cnt < refMin (120) ise şart tutmaz. Kaba kuvvetle (trp[i-n-249 .. i-n] ortalaması) 63.126 (bar, n) noktasında karşılaştırıldı: en büyük göreli fark 2,4e-14, na uyumsuzluğu 0. Varsayılanda ölçülür barda (i >= 250) cnt >= 180, refMin bağlamıyor. GEÇTİ.
- (6) BB şartı n'den bağımsız, pencerenin son gününde (245): tutmazsa o bar taban yok = Python `ok &= (bbp <= bbEsik)[:, None]`; na -> taban yok (ikisinde de). GEÇTİ.
- Onay günü (376-377, 454): bölgenin açıldığı bar (YENI) = Python onay = s6_bolgeler 'onay'. GEÇTİ.
- Kesik kısım (400, 420-422): kesik [solBar = kutu sol, onay barı], dolu [onay barı, son bölge barı]; sol kenar sonradan sola kayarsa kesik.left güncellenir, dolu.left onayda kalır = Python sol_i / onay_i / sag_i. GEÇTİ.
- SÖNDÜ (436-448): açık bölgede taban yok ve AL / KIRILDI yok -> acik = false, dogal = true, gri kenar + 'sonme' etiketi = Python durum SONDU, bolge_son_tur SONDU. Canlanma (360-363, 428-435): aynı taban (b <= rSon) dönerse kenar sınıf rengine döner, etiket silinir, kutu sürer = Python YENIDEN. GEÇTİ.
- Tarih etiketi (410, 426-427, 351-352): (sol, alt) noktasında 'ilk .. son'; AL / KIRILDI günü son = o gün; sönmede değişmez = Python [sol_i, sag_i]. GEÇTİ.
- v1.0 kipi (refOnce = false, bbSart = false): kod farkı yalnız `if bbOk` (bbSart kapalıyken hep doğru) ve 280/286 dalı (else = v1.0 satırı aynen); durum makinesine eklenen canlandi yalnız çizim. Pine v1.1 çevirisi v1.0 kipinde git v1.0 Python ile 30 hissede fark 0; test_s6_taban 'v1.0 kipi = git v1.0 kodu' ve '16 etiket v1.0 json ile birebir' TAMAM. GEÇTİ.
- Beklenen çıktı yorumu (521-541): `python S6_TABAN.py liste` KNFRT, TUCLK (2 dönem), PAPIL, ENJSA, DESA, CCOLA için aynı kutu tarihleri, uzunluk, onay günü, sınıf, AL / söndü, tavan / dip. GEÇTİ.

## 3. Geleceğe bakma / tekrar boyama: GEÇTİ
- `[k]` geçmiş başvurusu, request.security, ta.*, negatif kaydırma yok; bütün hesap t ve önceki geçerli bar dizilerinden (bbP önceki 250 bbw + bugünkü; ref önceki 250 TR/C). Python önek değişmezliği: kendi sınamam 3 hisse x 6 rastgele kesik, 12 sütun, fark 0; test_s6_taban önek testleri TAMAM.
- Kesik kısım ve sol kenarın sonradan sola kayması geçmişe doğru çizim değişikliğidir (bilgi t'de belli); kesik çizim bunu açıkça gösteriyor (v1.1'in amacı). GEÇTİ.
- Açık mum: barstate.isconfirmed yok; AL / KIRILDI gibi ONAY elması ve 'sonme' etiketi de seans içinde görünüp kaybolabilir (Pine açık mumda var'ları ve çizimleri her tikte geri alır, birikme yok). PINE_S6_NASIL.md 68 yalnız AL / KIRILDI'yı yazıyor -> B-3 (belge).

## 4. Kaynak sınırları: GEÇTİ
- BB döngüsü bar başına BİR kez (n döngüsünün dışında): 2 x 20 + 250 = 290 işlem; 250 x 70 DEĞİL. Referans ATR her n için O(1) (kümülatif fark).
- Çevirimdeki işlem sayacı (bar başına): varsayılan ortalama ~594, %99 ~1.030, en çok ~10.200; gevşek eşikler ortalama ~652, %99 ~2.700, en çok ~7.900. 5.000 günlük barda birkaç milyon basit işlem: süre sınırının çok altında.
- Nesneler: dolu kutu 240 + kesik kutu 240 = 480 <= 500; çizgi 480 <= 500; tarih etiketi 240 + sönme etiketi 240 = 480 <= 500; en eski silinir (397-398, 402-403, 407-408, 412-413, 446-447). Tablo ve plotshape sayılmaz. GEÇTİ.

## 5. ASCII kopya: GEÇTİ
- 543 / 543 satır; ASCII dışı 0; iş tanımındaki eşleme kaynağın TAMAMINA (yorumlar dahil) uygulanınca ASCII dosyasıyla bayt bayt aynı; dize / yorum dışı kod birebir.

## 6. Python testi ve sızıntı: GEÇTİ
- `S6_VERI=<scratchpad>/veri python test_s6_taban.py`: 105/105 TAMAM.
- E-posta / anahtar / token: S6_TABAN.py, test_s6_taban.py, .pine (iki), PINE_S6_NASIL.md, S6_V11_IS_TANIMI.md'de yok (tek eşleşme testteki yasak kalıbın kendisi).
- git status: denetim dosya değiştirmedi (bu rapor hariç; FITIL_OBEK.py / test_fitil_obek.py başka işin izlenmeyen dosyaları).

## DÜZELTME GEREKEN SATIRLAR
Kod: YOK (derleme ya da mantık engeli bulunmadı).
Belge / bilgi (bloklamaz):
| yer | sorun | öneri |
|---|---|---|
| PINE_S6_NASIL.md satır 68 | Açık mumda geçici görünme notu yalnız AL / KIRILDI'yı söylüyor; mor elmas ve 'sonme' etiketi de açık mumda gelip gidebilir | "AL / KIRILDI, mor elmas ve 'sonme' son mum KAPANINCA kesinleşir" |
| S6_V11_IS_TANIMI.md §1 | "pencereden ÖNCEKİ 250 geçerli bar ... referans [t-n-250, t-n]" (bu aralık 251 bar); kod [t-n-249, t-n] = 250 bar | İş tanımına "[t-n-249, t-n]" yaz (kod doğru, metin tutarsız) |
| COL_S6_TABAN.pine 45, 56 (v1.0'dan kalan) | dipTol / kirTol minval 0.0; Python s6_prm 0'ı reddeder | minval 0.001 (varsayılanda etkisiz) |

## HATA
- Pine kodunda derleme hatası, Python'dan ayrışma ya da geleceğe bakma BULUNMADI (5 kip, 308.160 ham bar, 5.710 kutu, fark 0).
- B-1 (belge, iş tanımı): S6_V11_IS_TANIMI.md referans aralığı metni "[t-n-250, t-n]" kendi "250 bar" sözüyle çelişiyor; uygulama 250 bar [t-n-249, t-n].
- B-2 (bilgi, sayısal): S6 bbp ile SIKISMA_OBEK.so_s5 bbp tanımı aynı, ama so_s5 pandas rolling std (çevrimiçi algoritma) kullanıyor, S6 sıralı toplam (Pine ile bit eşitliği için). 8 hissede 18.518 barın 22'sinde (%0,12) yüzdelik 1-2 / 250 farklı (eşit genişlik bağları; en çok 0,008). Pine = S6; etki yalnız eşik sınırında.
- B-3 (belge): açık mumda geçici onay elması / sönme etiketi PINE_S6_NASIL.md'de yok (v1.0 H-1'in v1.1 uzantısı).
- B-4 (yorum, ana model bilgisi): onay günü = bölgenin AÇILDIĞI gün (kırpılmış kutu >= nMin). İş tanımı "n ilk kez >= nMin olduğu gün" diyor; önceki bölgenin bitişiyle kırpılan durumda taban birkaç gün KISA (kutusuz) kalıp sonra açılıyor: 16 hissede 585 bölgenin 35'inde (%6) onay, tabanın ilk görüldüğü günden medyan 4 (en çok 7) gün sonra. Python = Pine; çizim açısından doğru olan 'kutunun ilk çizilebildiği gün'dür, ama metinden sapma olarak not edilmeli.
