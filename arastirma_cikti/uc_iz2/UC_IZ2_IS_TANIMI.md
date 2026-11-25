# UC_IZ2 İŞ TANIMI — üç fiyat dışı iz (sektör rüzgârı R, bilanço B, içeriden alım İ) aynı olayda birlikte, ABD 2016-22 (25 Kasım 2026)

Yazan: ana model. Cemal (25 Kas): "SEC'ten 2016-22 Form 4 alımlarını ve bilanço günlerini indir, üç izi aynı olayda birlikte ölç". Ç225'in açık kalan seçeneği (a). Ç225 ÖLÇÜLEMEDİ çıktı: B ve İ verisi 2022'den başlıyordu, KT02 dip olayı dardı (329), ön sayım yapılmamıştı (IK_HATA). Bu iş üçünü de giderir.

## 0. Kesin kurallar

- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, kural defteri. Bunlara dokunulmaz; önerilen kayıt metni raporda yazılır.
- KASA AÇILMAZ. Açık veri = 2022-12-31'e kadar. Fiyat 2022-12-31'de kesilir; ölçüm penceresi bu tarihi aşan olay ölçülmez. 2023+ fiyatlar diske inse de ölçüm koduna verilmez (kod en büyük tarihi assert eder).
- SEC User-Agent yalnız `/root/.sec_ua` dosyasından okunur (tek satır). İçeriği ekrana, loga, koda, repoya yazılmaz. Commit öncesi `git grep -n "@gmail\|@hotmail\|sec_ua içeriği"` sızıntı taraması yapılır. SEC sınırı saniyede en çok 8 istek, 429 / 403'te bekle ve yeniden dene.
- SEC ham verisi repoya girmez (CLAUDE.md). İşlenmiş küçük tablolar (olay listesi) xz ile `/root/.kasa/ham/sec2016` altında kalır; repoya yalnız kod, ön kayıt, rapor, özet json.
- Ön kayıt ölçümden ÖNCE commit edilir (kod sha + eşik sözlüğü sha + getirisiz sayımlar + güç + KONTROL LİSTESİ). `IZ_KARNE.ik_kontrol_kapisi(onkayit)` geçmeden `kos` çalışmaz. Eşik sonuca göre değişmez; değişirse SAPMA diye yazılır.
- Çakışma kapısı korunur (UC_IZ.py'deki `_cakisma_kontrol_uc` örneği). Yeni modül UC_IZ2.py tek dosya, KURAL_MOTORU düzeni, tam hata yakalama, loglama; test_uc_iz2.py sentetik testler.
- Rapor başlıkları zorunlu: KONTROL LİSTESİ, HATA (bulunan her hata ayrı satır), SONUÇ (sayılar), ÖNERİLEN DEFTER SATIRLARI (Ç226 kayıt, görev, hata, açık kalan taslağı).

## 1. Veri (indirme ve kurma)

V1. Fiyat paneli: Ç225 ile aynı (TEZGÂH 2 P2 havuzu + CETVEL2 v2.2). Konteyner sıfırlandı: `git worktree add /tmp/iv origin/islenmis-veri`, `python FON_IZI.py vpac /tmp/iv/veri /tmp/veri`, `python FON_IZI.py vpac /tmp/iv/veri2 /tmp/veri2`, `python TEZGAH2_VERI.py` (veri `/root/.kasa/ham/veri3`). Sonra 2022-12-31 kesikli açık kopya (UC_IZ'in uc_kes yolu) ve TEZGAH2_DOGRULAMA'nın 21 sınaması yeniden: hepsi geçmezse dur, rapor et.

V2. İÇERİDEN ALIM (Form 4): SEC Insider Transactions Data Sets, 2015Q4-2022Q4 (29 çeyrek zip). `FON_IZI.fi_k30_indir` / `fi_k30_alimlar` mantığı aynen (A1 = açık piyasa alımı, işlem kodu P, adi hisse, tutar >= 10.000 $; FI_K30 eşikleri). BİLGİ TARİHİ = FILING_DATE (işlem tarihi değil). Sağlama: 2022 çeyreklerinden üretilen A1 tablosu islenmis-veri `k30_alim.pkl` ile aynı satırları vermeli (örtüşen dönemde satır sayısı ve rastgele 5 satır elle); tutmazsa dur.

V3. BİLANÇO GÜNLERİ: 8-K Item 2.02 (Results of Operations) başvuruları, 2015-10-01..2022-12-31, P2 evrenindeki ABD hisselerinin CIK'leri için. Önce islenmis-veri `k55/sec_ozet.json` ve `k55/sembol_cik.json` okunur: 8-K madde kodu ve kabul saati 2016-22'yi kapsıyorsa indirme yapılmaz. Kapsamıyorsa `data.sec.gov/submissions/CIK##########.json` (+ ek sayfa dosyaları) indirilir: form 8-K, items içinde 2.02, acceptanceDateTime. OLAY GÜNÜ t: kabul saati New York 16:00'dan önceyse o işlem günü, sonraysa sonraki işlem günü. Aynı hissede 20 takvim günü içinde ikinci 2.02 (düzeltme) atılır. Sağlama: rastgele 5 olayın EDGAR sayfası WebFetch ile açılıp tarih / saat / madde kodu karşılaştırılır; 1'i bile tutmazsa dur.

V4. Sembol-CIK eşlemesi: CIK -> sembol karar günündeki haliyle (K2). Eşlenemeyen olay sayısı raporda.

## 2. Olay ve izler (sabit; değişmez)

- E1 (ANA OLAY) = BİLANÇO GÜNÜ: P2 evrenindeki ABD hissesinde V3 olay günü t. Giriş = t + 1 açılış (K5). Tekil: aynı hissede bir bilanço = bir olay.
- B (bilanço tepkisi, olay günü bilgisi): EAR_t = (C_t / C_{t-1} - 1) - aynı gün aynı kova eşlerinin medyan günlük getirisi; ATRP20_{t-1} (t-1'e kadar 20 günlük ATR / kapanış). B = EAR_t / ATRP20_{t-1} >= +1,0. BİLGİ: B- = <= -1,0.
- İ (içeriden alım): (t - 90, t] takvim aralığında FILING_DATE'li >= 1 A1 alımı. Not: bilanço öncesi ~30 gün içeriden işlem yasağı (blackout) olağandır; 90 gün bu yüzden.
- R (sektör rüzgârı): Ç225 / KT10 aynen (KART_TUR2.k2_d9_durum -> D9_YENIDEN.d9_satir 'c'; sektor_ABD.csv; D9_PARAM eşikleri) t günü.
- N = R + B + İ (0-3).
- E2 (BİLGİ) = Ç225'in KT02 dip olayı aynen, bu kez gerçek B (dip olayından önceki son 15 geçerli barda bir E1 bilanço günü ve o gün B) ve gerçek İ (t-90, t] ile. Karar vermez; Ç225 ile kıyas satırı.

## 3. Ölçü, eş, taban, hücre

- Eş ve sıra: Ç225 / CETVEL2 v2.2 konum eşi aynen (aynı giriş günü, aynı kova ATRP x likidite x F15, >= 5 eş; aynı gün E1 olayı olan hisseler eşten dışlanır). FARK = olay R - eş ortalaması; SIRA; ÜST10 / ALT10.
- Ufuk: KARAR iki ufukta ayrı satır: R60 (CLAUDE.md: olay izleri 60 günde) ve R15 (Ç225 / kasa kuralıyla kıyas). R30 bilgi.
- Taban: UC_IZ.uc_taban formülü VE plasebo (her olay yerine aynı gün aynı kovadan rastgele hisse, 200 tekrar) SAYIYLA (KASA KURALI: varsayılmaz).
- Hücreler (KARAR): ABD d1619 (giriş 2016-01-01..2019-12-31), ABD d2022 (2020-01-01..2022-12-31). AVRUPA: SEC verisi yok -> 'AVRUPA VERİSİ YOK', karar en fazla ABD-ADAY. BIST yok.

## 4. Karar kuralı (Ç225 aynen, iki ufukta)

YÖN TUTARLI(iz, ufuk) <=> iki hücrede de FARK(iz var) > 0 VE FARK(var) - FARK(yok) > 0 VE ÜST10 - taban_formül > 0 VE ÜST10 - taban_plasebo > 0. TUTAR <=> ayrıca iki hücrede c2 hükmü TUTAR (C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum). Aksi: iki hücrede iz-var n >= 30 ve güç >= 0,80 ise TUTMADI, değilse ÖLÇÜLEMEDİ. BİRLİKTE ARTIYOR <=> iki hücrede FARK(N=0) < FARK(N=1) < FARK(N>=2) VE N>=2 FARK boot alt > 0 en az bir hücrede, ötekinde FARK > 0. KASA ADAYI (yalnız öneri, kasa açılmaz) <=> en az iki iz YÖN TUTARLI VE BİRLİKTE ARTIYOR, aynı ufukta. BH q 0,10, aile = (R, B, İ, N>=2) x (R60, R15) = 8; p = iki hücrenin en büyük permütasyon p'si. Evren bugün yaşayanlar (K7): sonuç yukarı yanlı yazılır.

## 5. Sıra

1) V1-V4 veri + sağlamalar -> 2) UC_IZ2.py + test_uc_iz2.py (sentetik: bilanço saati sınırı 15:59 / 16:01, FILING_DATE pencere sınırları t-90 / t, B eşiği, eş dışlama, kesik assert, çakışma) -> 3) GETİRİSİZ SAYIM (hücre x iz x N olay sayısı, R / B / İ örtüşmesi phi, güç cetvel2_guc_v2.2 delta +0,02) -> 4) ön kayıt UC_IZ2_ON_KAYIT.md + KONTROL LİSTESİ + commit -> 5) kapı + kos (açık veriye bir bakış) -> 6) UC_IZ2_RAPOR.md + uc_iz2_sonuc.json -> 7) commit + push (dal ccr-82c0570b-j2nhsg).

Getirisiz sayımda bir iz iki hücreden birinde n < 30 ise ön kayda 'beklenen ÖLÇÜLEMEDİ' yazılır ve ölçüm yine koşulur (tanım değiştirilmez).
