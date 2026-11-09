# Çöl Yolu — Claude Code çalışma kuralları

Bu repo, Cemal'in Google Drive `MyDrive/col_tarayici/` klasöründeki Çöl Yolu (BIST çöl formasyonu) kodlarının aynasıdır.
Kodlar Google Colab'da Drive'dan çalışır. Repodaki dosya adları Drive'dakiyle birebir aynıdır; yeni dosya açma, kopya üretme.

## İletişim
- Her zaman Türkçe yaz. Açıklamalar kısa ve öz olsun, önemli noktalar mutlaka belirtilsin.
- Cemal mobilden çalışır. Sonucu tek, indirilebilir dosya olarak ver; uzun kod bloğunu sohbete yapıştırma.
- Kod kutusunu yalnızca Colab'a yapıştırılacak komut için kullan ve kutunun üstüne "Colab'a yapıştır" yaz. Dosya adlarını ve yollarını (ör. col_tarayici içindeki COL_v1.py) düz metinle yaz, kutuya koyma. Cemal kutudaki her şeyi Colab'a yapıştırıyor; 20 Ekim'de dosya yolu yapıştırılınca SyntaxError çıktı.
- Cemal grafik okur ve alım-satım kararını kendisi verir. Claude kodu yazar, ölçer, veriyi toplar.
- Her yeni iz/bulgu için Cemal'e grafikli kısa bir DERS PDF'i hazırlanır (Cemal, 24 Ekim 2026): iz nedir, nerede saklanır, grafikte nasıl görünür ve görünmez, test sonucu (eşli kat + 1,3 çizgisi), kendisi nasıl bakar. Örnek: `arastirma_cikti/fon_izi/FON_IZI_ders.pdf` (FON_IZI K12). Değişiklik (Cemal, 26 Ekim 2026): PDF YALNIZ GERÇEK İZ çıkınca verilir ve gönderilir. İz çıkmayan çalışmada PDF gönderilmez (SendUserFile yok); 'neden iz değil' birkaç satırla mesajda ve IZ_DEFTERI/IZ_KARNE'de kalır. Dosya gönderme (Claude uygulamasında 'yapıtlar' kartı) yalnız Cemal istediğinde, kör set gibi onun işaretleyeceği bir dosya gerektiğinde ya da gerçek iz dersinde yapılır.
- Görev bitişi ve son mesaj (Cemal, 24 Ekim 2026): görev bitince son mesajın ilk satırı açıkça "GÖREV TAMAMLANDI" (ya da neyin açık kaldığıyla "GÖREV TAMAMLANDI, AÇIK: …") olur; arka planda iş kalmadığı belli olsun. Son mesaj kısa maddelerdir: ne yapıldı, sonuç, Cemal'in bilmesi/öğrenmesi gereken, açık kalan, karar gereken. Uzun düz yazı yok. Her görev IZ_KARNE.py IK_GOREV görev günlüğüne bir satır olarak yazılır ve indeks yenilenir (`python IZ_KARNE.py indeks`).
- İndeks (Cemal, 24 Ekim 2026): IZ_DEFTERI.md başındaki "0. İNDEKS" IZ_KARNE.py'den üretilir, elle düzenlenmez. Her yeni çalışma IK_KAYIT'a bir Ç satırı ekler; iz iddiası varsa sinyali IK_SINYAL'e girer ve TEK CETVEL ile puanlanır (eşli taban, BIST 2023, BIST 2024-26, ABD 2023, ABD 2024-26). test_iz_karne.py kayıt, defter kapsamı ve indeks eşitliğini denetler.
- Grafik dersi (Cemal, 24 Ekim 2026): gerçek iz ve eşiğe yakın adaylar için ders PDF'inde grafik üzerinde şablon gösterilir (sinyal günü, giriş, eşik çizgileri, hacim; hisse adı yok). İz olmayanlar indekste bir satırla kalır.
- Yeni oturum (Cemal, 26 Ekim 2026): yeni konuşma önceki sohbetin hafızasını taşımaz. Başlarken IZ_DEFTERI.md '0. İNDEKS' bölümündeki görev günlüğünün son satırları ve 'Açık kalanlar' okunur; iş oradan sürer, Cemal'e geçmiş yeniden sorulmaz. Açık kalanlarda DRIVE maddesi varsa önce o yapılır.
- Görev bitmeden tur bitmez (Cemal, 21 Ekim 2026): bir iş akışı veya uzun ölçüm başlatıldığında Claude sonucu kendisi bekler (ön planda döngüyle, gerekirse birkaç kez) ve bütün sonucu tek mesajda yazar. "Çalışıyor, bitince yazarım" diye ara mesaj atıp Cemal'den yeni mesaj beklenmez; son görev de dahil hiçbir görevde bekleme moduna girilmez. Birden fazla görev verildiyse hepsi bitince tek rapor.

## Kod standardı (kesin kural)
- Basit veya geçici yama yok. Kod üretim kalitesinde olacak: KURAL_MOTORU mimarisi, tam hata yakalama, loglama, tek dosya.
- Düzeltmede çalışan kısma dokunma, yalnızca hatalı kısmı değiştir. Bağlam kopmasın, baştan yazma.
- Ölçüm modüllerinde "çakışma kapısı" bulunur: yüklenirken bellekteki mevcut bir adı ezerse durur. Bu kapıyı koru.
- Basit hatalar mekanik olarak yakalanmalı (ad çakışması, yanlış dosya, yanlış evren). Değişiklikten sonra ilgili `test_*.py` dosyasını çalıştır.
- Colab'da `exec()` önbelleği kalıcı sorun yaratır. Kod değiştiyse kullanıcıya "çalışma zamanını yeniden başlat" diye hatırlat.

## Dosyalar
- Üretim zinciri: `BASLAT.py` (tek satır başlatma) → `COL_v1.py` (segment + AL kuralı + `bugun_liste`) → `takip.py` (`gun()`, pozisyon takibi). Yardımcılar: `temel.py`, `fon_takip.py`, `onbellek.py`, `veri_koru.py`.
- Ölçüm: `OLCUM.py`, `olcum_denetimi.py`, `zincir_denetimi.py`, `DENETIM.py`. ABD Çöl Yolu akademik araştırması (K51, 29 Ekim 2026): `COL_YOLU_ABD.py` (tek dosya, Colab; testi `test_col_yolu_abd.py`; çıktılar `arastirma_cikti/col_yolu_abd/` ve Drive `COLAB_VERILER/OUTPUT/COL_YOLU_ABD`).
- Proje özeti: `COL_OZET.md` (kurallar, dosyalar, bütün testler). Bulgu defteri: `IZ_DEFTERI.md`. Yeni bulgu bu deftere eklenir, ama yalnızca gerçek iz eklenir.
- `col_atilim_TEK.py`, `tema_col.py`, `tema_sepet.py` ve `selale.py` eski ve kapalı denemelerdir. Ana üretim zincirine karıştırma.

## Veri (repoda yok)
- Veri dosyaları Drive'da kalır, repoya konmaz: `.pkl`, `.csv` çıktıları ve büyük önbellekler.
- Günlük önbellek `/content/drive/MyDrive/col_tarayici/veri_1d_turkey.pkl` yolundadır. Yapısı `kayit` ve `veri` anahtarlı bir sözlük; 583 sembol, Haziran 2023'ten itibaren. Yeni tarayıcı veya test bu önbellekten okur, veriyi yeniden indirmez.
- Test önbellekleri: OB24, OB23, OBUS ve OBUS21 (`onbellek_ABD_2022_23.pkl`).
- İstisna (24 Ekim 2026, Cemal'in isteği): KAP fon portföy raporları paketi (liste, ayrıştırılmış tablolar, 25 bin ham rapor metni; 220 MB) repoda ayrı `kapfon-veri` dalında durur, `main`'e birleştirilmez. Açma `python FON_IZI.py k9ac kapfon`, güncelleme yalnız yeni raporları indirir (`k9indir` + `k10`), sonra `k9paket` ile dal yenilenir.
- İstisna 2 (26 Ekim 2026, Cemal 'koy'): işlenmiş veri paketi repoda ayrı `islenmis-veri` dalında durur, `main`'e birleştirilmez: V_BIST.pkl, V_ABD.pkl (fi_k1_veri çıktıları) ve K25 fon tabloları (G, oran, dol); xz + 45 MB parça, manifest sha256. Yeni oturumda açma: `git worktree add /tmp/iv origin/islenmis-veri` ve `python FON_IZI.py vpac /tmp/iv/veri /tmp/veri`; sürücülere V_hazir olarak verilir. Veri yenilenirse fi_veri_paketle ile dal yeniden yazılır. Genişletme (28 Ekim 2026, Cemal 'verileri repoya kaydet, sen kaydet'): veri/ artık V_AVR.pkl'yi de içerir; veri2/ (xz paket): K34 Yahoo fiyatları (nakdi biten 2.246 ABD şirketi), k34_bildirim (SEC özeti), k31_fin, k30_alim, k28_X_bist / k28_X_abd, olcut_panel_AVR; secfs/ SEC finansal tablo özütleri 2021-26 + company_tickers.json; k34/ eski kodlar ve örneklem; k35/ SIC kodları; k36/ sürücü serileri; avr/ Avrupa evren listesi. Tiingo fiyatları (batan şirketler) lisans gereği repoya konmaz, anahtar .env'de kalır, gerekince fi_k34_tiingo_indir ile yeniden iner. Açma: `python FON_IZI.py vpac /tmp/iv/veri /tmp/veri` ve `python FON_IZI.py vpac /tmp/iv/veri2 /tmp/veri2`.
- SEC (27 Ekim 2026, Cemal'in izni): ABD Form 4 veri setleri repoya konmaz; `fi_k30_indir(eposta)` ile SEC'ten yeniden indirilir. SEC kuralı User-Agent'ta iletişim e-postası ister; Cemal'in e-postası yalnız bu indirmede kullanılır, koda ve repoya yazılmaz.
- Repodaki tek veri istisnası küçük ayar dosyalarıdır: `sektor_BIST.csv` (BIST alt endekslerinden kurulan sektörler; Yahoo sektör etiketleri hatalı), `sektor_ABD.csv`, `evren_disi_ABD.csv` (Cemal, 30 Ekim 2026 'ETF'leri evrenden çıkar': ABD evreninden çıkarılan fonlar; COL_YOLU_ABD.py `cy_veri_yukle` bu listeyi uygular, dosya yoksa main'den indirir, yine yoksa durur) ve `.json` ayarları.
- Token, şifre, Telegram anahtarı gibi bilgiler asla koda yazılmaz. Bunlar `.env` dosyasında tutulur ve `.env` git dışındadır.

## Drive düzeni ve arşiv (temizlik 2026-10-20)
- Bir dosya `col_tarayici` kökünde yoksa önce arşive bak; yeni kopya üretme.
- `IZ_DEFTERI.md`'nin Drive'daki tek kopyası `MyDrive/COLAB_VERILER/col_tarayici/` klasöründedir, `col_tarayici` kökünde değil. Güncellerken orada güncelle.
- Drive bağlayıcısı dosya içeriğini yerinde değiştiremez. Bu yüzden önce Drive'daki eski kopyanın repodaki beklenen sürümle bayt bayt aynı olduğu doğrulanır, sonra yeni dosya aynı klasöre aynı adla yüklenir. Yüklenen dosya geri indirilip bayt bayt karşılaştırılır; ancak eşitse eski dosya çöpe atılır, böylece klasörde tek kopya kalır (20 Ekim'de COL_v1.py, takip.py, COL_OZET.md ve IZ_DEFTERI.md böyle güncellendi).
- `col_tarayici/arsiv/` yerinden oynatılmaz: `tema_col.py`, `tema_sepet.py` ve `ruzgar_defteri.py`, `arsiv/desen/DESEN_TAM.py` dosyasını okur.
- `col_tarayici/arsiv/col_kodlarim/`: Eylül – 2 Ekim araştırma kodları. BUYUK_COL (v2–v8), RUZGAR_COL, RUZGAR_ZAMAN, COL_KIRILIM_ATLAS, BUYUK_YUKSELIS, TEYIT_BILETI, SIKISMA_TESTI, BEKLEME_TESTI, COL_KANIT, akümülasyon, segment ve backtest hücreleri. Veri yolları sabit (`K=.../col_tarayici`) olduğu için kodlar buradan da çalışır.
- `col_tarayici/arsiv/eski_ciktilar/`: Ağustos–Eylül test çıktıları (yon_v3…v10, hbaglam, hcol_geri, iki_asamali, evre2, replay, liste, bekleme, ruzgar_*, col_ruzgar_*, tara4h ...). Ayrıca:
  - Eylül OB24/OB23 test setinin (n=2064/820) tek kaydı: `onbellek_*.pkl.yedek_20261008_0913`
  - `onbellek_*.yedek_0923/0942` ve `onbellek_v1_*`: boyutları güncel önbellekle aynı, ama içerik eşitliği kanıtlanmadı
  - `veri_1d_turkey.pkl.yedek_evren_20261008_0721`
  - `ASAGI_KIRDI` atlas grafikleri: eski sınıflandırma, yeniden üretilemez
- `QMLS_Tarayici/arsiv/`: QMLS'in eski sürümleri (`.bak`, `_eski_`, `-1/-2`). Güncel sürümler `QMLS_Tarayici` kökünde.
- Yerinde kalması zorunlu olanlar:
  - `veri_1d_turkey.pkl.yedek_bolunme_*`: `bolunme_onar.py` ham veri olarak okur
  - `veri_1d_turkey.pkl.yedek_20261008`: `zincir_denetimi` için VERI_ESKI
  - `buyuk_col_kor_anahtar*.pkl`, `buyuk_col_olaylar.csv`, `buyuk_col_haftalik.pkl`: BUYUK_COL kör testi; Cemal'in etiketleri henüz çözülmedi
  - `onbellek_v2_*`: Ekim col_v2 ölçümü
  - kalibre_*, goz_*, kor_test/, `iyi_kotu_coller.pdf`, `cemal_vs_kod.pdf`
- Silinenler (Drive çöp kutusunda ~19 Kasım 2026'ya kadar geri alınabilir):
  - birebir kopyalar (aynı ad, aynı bayt)
  - `COLAB_VERILER/col_tarayici/atlas*/` altındaki sınıf klasörleri (972 PNG, COL_KIRILIM_ATLAS çıktısı). Atlas CSV'leri, `taban_serisi_izleme.csv` ve `motor_karne.csv` yerinde.
  - `__pycache__`
- Cemal'in kişisel fotoğraf ve belgelerine, "Dizüstü Bilgisayarım" yedeğine dokunulmaz.

## GitHub Actions günlük tarama (2026-10-19)
- `.github/workflows/gunluk_col_tarama.yml` iş günleri 19:35 TR saatinde `gh_gunluk.py` dosyasını çalıştırır. Bu dosya `BASLAT.py`'yi exec eder, ardından `gun()`'ü çağırır.
- Kodlardaki sabit Drive yolu, iş akışında `/content/drive/MyDrive/col_tarayici → repo kökü` sembolik bağlantısıyla karşılanır. Bu yüzden Colab koduna Actions için değişiklik yapılmaz.
- 20 Ekim: eski `gunluk_tarama.yml` iş akışı 19 Ekim 21:01'de GitHub arayüzünden elle kapatılmıştı (API durumu disabled_manually), bu yüzden zamanlanmış tarama hiç çalışmadı. İş akışı aynı içerikle `gunluk_col_tarama.yml` adıyla yeniden kuruldu; yeni dosya açık başlar. Tarama yine çalışmıyorsa önce iş akışı durumuna bak.
- Rapor `rapor/son_rapor.txt` dosyasına yazılır, günlük kopyası `rapor/YYYY-MM-DD.txt` adıyla saklanır. Kurulum çıktısı `rapor/kurulum_log.txt` dosyasındadır.
- Takip durumunun asıl yeri artık bu repodur: `takip_adaylar.csv`, `takip_pozisyonlar.csv`, `takip_kapanan.csv`. Colab'da `gun()` ayrıca çalıştırılırsa iki kopya ayrışır.
- Veri önbelleği (`veri_1d_turkey.pkl`) repoya girmez, Actions önbelleğinde tutulur.
- Repodaki girdi kopyaları Drive'dan 2026-10-19'da alınmıştır: `v1_final_BIST.csv`, `kirilim_sonrasi_w.csv`, `yeni_BIST_2023.csv`, `temel_duz.csv`, `cds_2022.csv`.

## Cemal'in çöl tanımı (kodu buna göre yorumla)
- Çöl, düşüş sonrası dipte aylarca süren sıkışmadır: dip savunulur, mumlar küçüktür. Tepede oluşan sıkışma dağıtımdır, çöl değildir.
- "Küçük mum" mumun gövdesi değil, fitiller dahil boyudur (H−L). `COL_v1.py` içinde `MUM_OLCU='aralik'` olarak tanımlıdır.
- Tam desen üç evrelidir. (1) Aylarca süren küçük mumlu sıkışma. (2) Kırılım, ardından yükselen SMA'nın üstünde oturan bir raf. (3) O bölgeye sert bir test, ardından hareket. "İki kutu" kuralı: ilk giriş, 2. kutu oluştuktan sonraki hafif silkelemedir; bölge testi yukarı dönerse ekleme yapılır.
- Sektör rüzgârı veya katalizör olmadan çöl aranmaz.
- Çöl, ardından gelen yükselişle değerlendirilir. Sabit bir ufuktaki kapanış başarı ölçüsü değildir.

## Test ve bulgu standardı
- Her test iki dönemde (2023 ve 2024-26) ve ABD verisinde çalıştırılır. Eşikler sabittir, slot simülasyonu yapılır.
- YENİ ÖLÇÜT (Cemal, 26 Ekim 2026, 'ölçütü değiştir'; K27'den itibaren, FON_IZI.py FI_OLCUT): olay başına giriş = olaydan sonraki ilk işlem günü açılışı, r60 = 60. gün kapanışı / giriş − 1 (fon krizi 31.08.2026'da kesik). EŞLİ FARK = r60 − aynı giriş günü, aynı 60 gün momentum beşliği × likidite üçlüsündeki öteki hisselerin ortalama r60'ı. Bir hücre (pazar × 2023 / 2024-26) şu dört şartla TUTAR: n ≥ 30; ortalama eşli fark > 0 ve ay kümeli bootstrap %95 güven aralığının alt ucu > 0; ortalama hücre içi sıra > 0,50; 10 yuvalı slot portföyü (60 gün tut) olay getirileriyle, her olay yerine aynı gün aynı hücreden rastgele hisse alınan 200 portföyün %90'ından büyük (rastgele olay sağlamasıyla düzeltildi: tek hisse çarpıklığı yüzünden 'medyan fark' ve 'eşli ortalama portföyü' yanlıydı). İZ = dört hücre (BIST 2023, BIST 2024-26, ABD 2023, ABD 2024-26); ABD verisi yoksa en fazla BIST-ADAY. Eski 'önce +%20 oranı ≥ 1,3 kat' (tek cetvel) eski çalışmaların kaydıdır; yeniden açılmaz.
- KARAR HÜCRELERİ DEĞİŞTİ (Cemal, 28 Ekim 2026, 'Amerika ve Avrupa tutan iz kabul edilsin, yaz md'; K38'den itibaren, FON_IZI FI_OLCUT 'karar'): BIST öngörülemez (siyaset, tedbir, fon olayları), bu yüzden şart değil. İZ = ABD 2023, ABD 2024-26, AVRUPA 2023, AVRUPA 2024-26 dört hücrede FI_OLCUT şartları. BIST hücreleri BİLGİ olarak yine ölçülür ve yazılır (BIST'te de tutuyorsa 'İZ + BIST' denir). Çin sonra bakılır (Cemal: BIST gibi güven olmaz). Avrupa evreni: STOXX Europe 600 + FTSE 250 (Wikipedia bileşen listeleri, 28 Ekim 2026; Yahoo kodları; yalnız bugün işlem görenler, hayatta kalma yanlılığı büyük hisselerde küçük), fiyat yerel para, likidite için işlem değeri EUR'ya çevrilir (`Kur` sütunu). Veri: islenmis-veri dalında V_AVR.pkl (fi_veri_paketle). Avrupa'da içeriden alım / bilanço listesi gibi olay verisi bedava yok; yalnız fiyat-hacim ölçüleri Avrupa'da ölçülebilir, olay ölçüleri için 'AVRUPA VERİSİ YOK' yazılır ve karar en fazla ABD-ADAY olur.
- Fon krizi (Cemal, 27 Ekim 2026): 31 Ağustos 2026 sonrası olağanüstü dönemdir. O tarihten sonraki çöl ve sinyaller testlere girmez; fiyatlar 31.08.2026'da kesilir, 60 günlük ölçüm penceresi bu tarihi aşan olay ölçülmez (FI_OLCUT 'kriz'). Ölçülen en geç giriş Haziran 2026 başıdır.
- Bir ölçü bir testte pozitif, başka bir testte negatif çıkıyorsa iz sayılmaz. Küçük örneklemden çıkan sonuç "bulgu" diye sunulmaz.
- Desene veya tek göstergeye göre alım-satım yoktur. Tarayıcı yalnızca aday bulur.
- Kapanmış konuları yeniden açma (`COL_OZET.md` listesine bak): giriş zamanlaması/onay/hacim, stop/erken kesme, sektör ısısı, KNN, VIX/DXY, 90'dan fazla şekil ölçüsü.
- İz yok çıkarsa durma (Cemal, 24 Ekim 2026): ne denendiğini, eşiğe (1,3) en çok yaklaşan hücreleri ve sıradaki 3 denemeyi yaz, sonra o denemeleri Claude kendisi yapar. Cemal'e yalnız karar gereken yerde sorulur (üretim "yaz", kapalı konuya dokunan deneme, veri/ücret/izin). Sıradaki denemeler sonuç görülmeden, sabit eşikle önceden yazılır; eşik sonuca göre oynanmaz.

## Cemal'in son talimatı (9 Kasım 2026, "tek ve son talimat")
- Kripto kapandı (Ç147: İZ DEĞİL). Odak: YEOTK gibi "sıkı dosya" hisseleri bulmak, BIST'te ve özellikle ABD'de. Cemal'in tezi: YEOTK daha da çıkar, DGXX kazanır; gerisi gürültü.
- "Sıkı dosya" = YEOTK profili (ölçülebilir hali K57'de): gerçek iş ve isimli sözleşme, son çeyrekte satış/kâr ivmesi, nakit seyrelme yok, fon krizi lekesi yok, fiyat tepeden düşmüş ve bilanço günü güçlü tepki.
- Bulunan bütün ölçüler her açıdan ele alınır ("kuantum düşünce": aynı anda birçok hipotez, hepsi test edilir, hiçbiri test edilmeden seçilmez). Gerekirse makine öğrenmesi, web araştırması ve ajan görevlendirme kullanılır; sonuna kadar gidilir.
- Gerçek ve değerli bilgi basit ve erişilebilir olandır: karmaşık ölçü, basit ölçüyü geçmiyorsa seçilmez; sonuçlar Cemal'e tek sayfada, düz dille yazılır.
- Bağlam kopmasın: her adım IZ_KARNE (IK_KAYIT, IK_GOREV, IK_ACIK) üzerinden IZ_DEFTERI.md'ye işlenir; yeni oturum buradan sürer.
- Mevcut pozisyon kuralları (6-7 Kas): DGXX 2x kuralı (maliyetin 2 katında anaparayı çek), bilanço günü kuralları, QMLS kalan yarı için olay kuralları; ayrıntı IK_GOREV'de.
