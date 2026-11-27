# GOZ_TESPIT EK 7 İŞ TANIMI — ÇÖL-K2 x PİYASA REJİMİ: piyasa genişliği dipteyken oluşan bölgeler, aynı günün evren ortalamasından iyi mi (27 Kasım 2026)

Yazan: ana model. Gerekçe: Ç271 / Ç272'de beş şart tek başına getiri vermedi. Cemal'in kuralı 'tek izle kasa açılmaz; en az iki-üç olay aynı anda' ve sözü 'asıl derdimiz piyasanın yükselişini tahmin etmek'. Ç255 / Ç257: ABD'de uzun ortalamasının üstündeki hisse payı çok düşükken sonraki 15 günde +%5 olasılığı bütün hisselerde yüksek (bilgi; 2000-2015'te 8 ayrı dönem; kesim sabitlendi). Soru: o günlerde ÇÖL-K2 bölgesi olan hisse, aynı gün öteki hisselerden daha iyi mi gidiyor. Tespit Cemal'in görsel onayını bekliyor: başlık 'DEDEKTÖRÜN BULDUĞU BÖLGELER (Cemal'in görsel onayı bekliyor; kalıp hükmü değil)'.

## 0. Kesin kurallar
- Başlamadan `python IZ_KARNE.py kontrol istanimi`. YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, cemal_*.json, GT*_onay_anahtar.json, goz2/, GT5_* / gt5_* / GT6_* / gt6_* dosyaları (yalnız okunur), öteki modüller ve testleri (yalnız import). `git add -A` / `commit -a` yasak. Push reddedilirse fetch + merge.
- Olaylar DONDURULMUŞ (/root/.kasa/ham/goz_tespit/k2/k2_olay.pkl; sha GT5_ON_KAYIT.md'de; assert); yalnız ABD. Veri <= 2022-12-31. Kod GOZ_TESPIT.py'ye yeni bölüm (komutlar k2rejsay / k2rejolc) + testler; mevcut 36 test aynen geçer.
- Ön kayıt (GT7_ON_KAYIT.md) getiri hesaplanmadan ÖNCE commit + push; `IZ_KARNE.ik_kontrol_kapisi`; ölçüm bir kez. Ön kayıtta YALNIZ getirisiz sayımlar: rejim günü sayısı, ayrı dip dönemi sayısı, kol x dönem x rejim olay sayısı. Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI. Commit sonu yalnız ana modelin verdiği iki satır.

## 1. Tanımlar (sabit)
- REJİM SERİSİ: Ç257 (arastirma_cikti/yukselis_oncesi/YO2_IS_TANIMI.md, YO2_RAPOR.md; YUKSELIS_ONCESI.py) ile AYNI tanım ve AYNI sabit kesim (2000-2015 verisinden; 2016-22'ye bakılarak değiştirilmez). Tanım ve kesim değeri o dosyalardan okunur ve ön kayda yazılır; günlük seri yoksa haftalık seri bir sonraki haftaya taşınır (her gün için yalnız o günden ÖNCE bilinen değer; geleceğe bakma testi). DİP günü = seri <= kesim. AYRI DİP DÖNEMİ = aralarında en az 20 işlem günü olan DİP günü öbekleri.
- OLAY: K2 (ANA), YMSB, Y bölgeleri; bölge sonu günü t DİP ise 'DİPTE', değilse 'DİP DIŞI'. Giriş = t + 1 açılış; R15 (Ç271 ile aynı fonksiyon).
- KONTROL (K1; aynı gün, aynı rejim): SEÇİM = R15 - o gün girişi yapılabilen bütün evren hisselerinin (ABD; evren şartları pencere paneliyle aynı; olayın kendi hissesi dahil) R15 ortalaması. Ayrıca OYNAKLIK EŞİ: SEÇİM_O = R15 - aynı gün aynı ATRP20 beşliğindeki hisselerin R15 ortalaması (çöl hisseleri en oynak beşlikte toplanıyor; Ç271). Simetrik ilk dokunuş (+%5 / -%5; stop yok) payı ve aynı gün aynı beşlik tabanı.
- Hücreler: ABD 2016-19, ABD 2020-22; her biri DİPTE ve DİP DIŞI.

## 2. Karar (önceden)
- DİPTE hücresi TUTAR <=> n >= 30 VE ayrı dip dönemi >= 5 (olayı olan) VE SEÇİM_O ortalamasının dip dönemi kümeli bootstrap %95 GA alt ucu > 0 (2.000; tohum 7; küme = dip dönemi) VE medyan SEÇİM_O > 0 VE simetrik +%5 farkı > 0. n < 30 ya da dip dönemi < 5 ise ÖLÇÜLEMEDİ.
- 'EMARE (yaşayan evren)' <=> ANA kol DİPTE hücresi iki dönemde de TUTAR. Ek okuma (karar değil): DİPTE - DİP DIŞI farkı; K2 - Y farkı (beş şart yalnız yere göre bir şey katıyor mu).
- K7 uyarısı zorunlu (yaşayan evren; dip dönemlerinde batanların yokluğu sonucu yukarı yanlı yapar). Sağlama: bir DİPTE hücresinin SEÇİM_O'su satır dosyasından bağımsız kısa kodla yeniden üretilir.

## 3. Çıktılar
GOZ_TESPIT.py, test_goz_tespit.py; arastirma_cikti/goz_tespit/: GT7_ON_KAYIT.md, GT7_RAPOR.md, gt7_sayim.json, gt7_ozet.json. Satır dosyaları /root/.kasa/ham/goz_tespit/k2/.
