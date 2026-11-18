# YAPI_HEDEF 4. TUR — S7 "CEMAL BÖLGE SEÇİCİ" (Y10 / Y10b / Y10c) + TUR 4 ÖRNEKLEMİ — İŞ TANIMI
Yazan: ana model, 18 Kas 2026 (Cemal: "onca fikir ve 'bu şekilde olsun' dedik, bunu kodun bölge seçimine yansımalı, yoksa boşa kürek").
Alt ajan bu dosyayı okur, ön kayıt yazar, sonra koşar. Yasak dosyalar: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, HAKEM_DERSLER.md, KURAL_DEFTERI_TASLAK.md, CEMAL_COL_KURALLARI.md, TUR_DEFTERI.md, tur/1 ve tur/2 ve tur/3 klasörleri. `git add -A` yok, push yok. Çakışma kapılarını koru. Üretim zincirine (COL_v1.py, takip.py, BASLAT.py) DOKUNMA: üretim değişikliği Cemal'in ayrı "yaz" kararıdır.

## 0. ÖN UÇUŞ KONTROLÜ
`python IZ_KARNE.py kontrol istanimi` çıktısı (K1-K14) ön kayıt dosyasına tablo olarak konur, her satır EVET / UYGULANMAZ + kanıt; `IZ_KARNE.ik_kontrol_kapisi(onkayit_yolu)` koşudan önce çağrılır. Rapor 'KONTROL LİSTESİ' ve 'HATA' başlıkları zorunlu.

## 1. AMAÇ
Hakem turlarında ve YAPI_HEDEF'te kullanılan bölge seçimi S6 AL olaylarıdır (Y1). Cemal'in gözlemi (Ç193 ile doğrulandı): Y1'in %58'i tepede; "kodun bölgelerinin çoğu kötü bölge". Cemal'in kuralları (C1-C13, VD2-VD9, K16-K46) şimdiye kadar yalnız ETİKETLEME kurallarına girdi, bölge seçimine girmedi. Bu tur: kuralları MEKANİK SÜZGEÇ olarak S6 olaylarına uygulayan S7 seçicisi; aynı 15 bar cetveliyle ölçüm; TUR 4 örneklemi S7'den.

## 2. S7 TANIMI (Y1 olayı VE aşağıdaki şartlar; hepsi t'ye kadar bilinen bilgi; eşikler SABİT, sonuç görülünce değişmez)
Y1 olayı = olay_Y1.csv.gz satırı (OC tekil); özellikler ozellik_Y1.csv.gz (F1-F18, 6 anlamlı basamak), parmak_Y1_p11.csv.gz (F19). Yeni özellikler (F20-F23) ham fiyattan (oc_veri / ge_hazir: geçerli bar H>L, V>0, kriz kesiği) hesaplanır ve ozellik_Y1_s7.csv.gz dosyasına yazılır (sembol, tarih anahtarlı; prefix değişmezliği: yalnız [t-250, t] barları).
- Ş1 DİPTE (C6 / VD3; Y9 ile aynı): F15 <= 0,25 VE F17 <= -0,20.
- Ş2 HAT NET (C1; Y9b ile aynı): F1 >= 3.
- Ş3 DİP SAVUNULMUŞ (C2): F2 >= -0,01 (son dokunuş dibi ilk dokunuştan en çok %1 aşağıda).
- Ş4 MUMLAR KÜÇÜK (C3): F3 <= 0,90 (bölge medyan mum boyu / ATR250; parmak P1.1 eşiğiyle aynı).
- Ş5 ALT FİTİL KISA (C4): F4 <= 0,25 (bölge medyan alt fitil payı; P1.x eşiğiyle aynı).
- Ş6 KAZAN SAĞ KENARI DÖNMÜŞ (VD6 / VD9 şart 1): F20 = min Low[t-5..t-1] / min Low[t-15..t-6] - 1 >= 0 (geçerli bar sayımı; 15 bar yoksa NaN = tutmaz).
- Ş7 YAKIN TAVAN + GÖVDELİ ORTALAYAN KIRILIM (VD5 / VD8 / C5): F21 = tavan15 = max High[t-15..t-1]; F22 = C_t / F21 - 1 (kırılım payı, yakın tavana göre) > 0 VE O_t < F21 (gövde tavanı ortalıyor: açılış tavanın altında, kapanış üstünde; boşluklu açılış O_t >= F21 elenir) VE F23 = |C_t - O_t| / (H_t - L_t) >= 0,50 (gövdeli; H_t = L_t ise NaN = tutmaz).
- Ş8 YOL ALMAMIŞ (C10 / C11 / VD2): F18 <= 0,20.
Denemeler (hepsi yön +, giriş t+1 açılış, hat ve stop0 = Y1 ile AYNI; yalnız olay kümesi değişir):
- **Y10 S7 ÇEKİRDEK**: Ş1-Ş8 hepsi.
- **Y10b S7 + BÜYÜK RESİM**: Y10 VE F14 >= 0 (250 bar dip noktaları eğimi aşağı değil; VD9 şart 3).
- **Y10c ŞEKİL KURALLARI, KONUMSUZ (bilgi)**: Ş2-Ş8 (Ş1 yok): Cemal'in şekil kuralları tepede / ortada da işliyor mu, konum eşli KAT ile; bilgi satırı, karar değil.
- Huni: Y1 -> +Ş1 -> +Ş2 -> ... -> +Ş8 -> +F14 adım adım olay sayıları (pazar x dönem), GETİRİSİZ (ön kayıt dosyasına; sonuç görülmeden).

## 3. ÖLÇÜM (3. turla AYNI cetvel; değişiklik yok)
- 15 bar cetveli: h5 / h10 (kapanış +%5 / +%10 stop'tan önce), st5, eş payı (aynı gün aynı momentum x likidite kovası, aynı mekanik kural), KAT5 = olay / eş, ay kümeli bootstrap %95; KONUM EŞLİ KAT (eş = aynı kova VE F15 aynı çeyrek) zorunlu; plasebo (aynı hisse rastgele gün); takip stoplu getiri ve çıkış barı bilgi.
- Karar hücreleri: ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26; DIŞ SINAMA ABD 2016-22 ve AVR 2016-22; BIST üç dönem bilgi. Etiket kuralı 3. turla AYNI (yh_etiket; İZ / EMARE / ÖLÇÜLEMEDİ / DESTEKLENMEDİ + TERS; ÖLÇÜLEMEDİ için n < 30 ya da güç yetersiz). Bakılmış hücre notu: Y9 hücreleri daha önce görüldü; Y10 Y9'un alt kümesi olduğu için ABD / AVR 2023 ve 2024-26 yine 'BAKILMIŞ' işaretli (etiket en fazla EMARE); bağımsız kanıt dış sınama ve BIST.
- Çoklu karşılaştırma: Y10 / Y10b x 4 karar hücresi (8 p) BH q 0,10 (aile 'bh_tur4'); Y10c bilgi.
- Regresyon kapısı: Y1-Y9 eşikleri AYNEN (YH_ESIK'ten Y10* çıkarılınca sha = ON_KAYIT_3.md YH_ESIK_SHA); Y10* satırları olay_Y1.csv.gz'deki aynı (sembol, tarih) satırıyla h5, h10, st5, es_h5, getiri sütunlarında eşit (göreli 1e-4), değilse DURUR.
- Güç: her karar hücresi için n ile güç (3. tur tablosu yöntemi); n < 30 hücre 'ÖLÇÜLEMEDİ (n)'.

## 4. CEMAL'İN GÖZÜYLE UYUM (bilgi; ölçümden bağımsız, sonuç içermez)
Cemal'in etiketlediği sayfalar: hakem seti (hakem_anahtar.json + hakem_cevap_cemal_duz.json, 40 sayfa), TUR 1 (tur_1_anahtar.json + tur_1_cemal.json), TUR 2 (tur_2_anahtar.json + tur_2_cemal.json). Her sayfa için S7 şartlarının (Ş1..Ş8, F14) tutup tutmadığını hesapla. Tablo: Cemal OLUR / OLMAZ / BELİRSİZ x (S7 tutan / tutmayan) ve şart başına Cemal OLUR payı. Soru: S7, Cemal'in OLUR dediklerini OLMAZ dediklerinden ayırıyor mu (Fisher p, n küçük: yorum 'bilgi'). Bu bölüm sonuç (h5) OKUMAZ; yalnız etiket ve özellik.

## 5. TUR 4 ÖRNEKLEMİ (GOZ_ETIKET)
- ge_tur_esik(4): sürüm T1.4: deneme = "Y10" (S7 çekirdek), tohum_taban aynı, katman = ABD 20, AVR 5, BIST 5 (parmak katmanı YOK; F19 bilgi sütunu olarak satır dosyasına yazılır), sembol_azami aynı, daha önce gösterilen olay / hisse dışarıda (300'lük örneklem + hakem + TUR 1-3). Kota dolmazsa (uygun olay az) DURUR ve rapora yazar (kota düşürülmez; ana model karar verir).
- `tur ac --no 4` HENÜZ KOŞULMAZ (Cemal TUR 3'ü yanıtlamadan sonraki tur açılmaz; CLAUDE.md). Yalnız uygun olay sayıları (pazar x dönem, gösterilmemiş) rapora yazılır; test: ge_tur_esik(4) ile örneklem fonksiyonu kuru koşu (tohum sabit, dosya yazmadan).
- Kör PDF sayfasında S7 bölge çizimi: tavan çizgisi = F21 (yakın tavan, 15 bar), hat = S6 hat (değişmedi); başlıkta 'S7' yazılır. Bu çizim değişikliği ge_tur_sayfa_png'ye `tavan_kaynak` parametresiyle girer; varsayılan davranış (TUR 1-3) DEĞİŞMEZ (TUR 3 PDF'i yeniden üretilince bayt bayt aynı olmalı: kapı).

## 6. ÇIKTILAR
- YAPI_HEDEF.py: YH_ESIK['denemeler'] Y10 / Y10b / Y10c; YH_DENEMELER_4; yh_s7_ozellik (F20-F23, ozellik_Y1_s7.csv.gz); `kos --deneme Y10,Y10b,Y10c` ON_KAYIT_4.md kapısı; test_yapi_hedef.py'ye S7 testleri (F20-F23 yapay vakalar; prefix değişmezliği; Ş7 boşluklu açılış elenir; Y1-Y9 regresyon).
- GOZ_ETIKET.py: ge_tur_esik(4) T1.4; tavan_kaynak; test_goz_etiket.py'ye testler (TUR 1-3 çıktıları değişmedi kapısı).
- arastirma_cikti/yapi_hedef/ON_KAYIT_4.md (kontrol tablosu, eşik sha'ları, huni, git kaydı; koşudan ÖNCE commit), RAPOR_4.md (3. tur biçimi: SONUÇ tablosu, huni, hücre tablosu, konum eşli KAT, olasılık tablosu, dış sınama, BIST, iki yönlü, bilgi, çoklu karşılaştırma, veri sınırları, YENİDEN ÜRETİM iki hücre satır dosyasından, KONTROL LİSTESİ, HATA), olay_Y10*.csv.gz, sonuc.json güncel, bölüm 4 tablosu RAPOR_4.md'de ayrı başlık.
- Commit sırası: (1) kod + ON_KAYIT_4.md (ölçüm koşmadan; 'ön kayıt' mesajı), (2) koşu çıktıları + RAPOR_4.md. Mesaj sonunda:
  Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01F7vgWZPNpBhrsGQEHDtRis

## 7. RAPOR (kısa, Türkçe)
Huni sayıları; SONUÇ tablosu (etiket + 4 karar hücresi n / KAT5 / konum eşli / plasebo); dış sınama; BIST; bölüm 4 uyum tablosu; TUR 4 uygun olay sayıları; kapı sonuçları; commit hash'leri; HATA; KONTROL LİSTESİ; 'Colab'da çalışma zamanını yeniden başlat' notu. Yorum yazma: 'tutmadı' çıkarsa da sayılarla bırak; n küçükse ÖLÇÜLEMEDİ.
