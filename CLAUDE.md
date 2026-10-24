# Çöl Yolu — Claude Code çalışma kuralları

Bu repo, Cemal'in Google Drive `MyDrive/col_tarayici/` klasöründeki Çöl Yolu (BIST çöl formasyonu) kodlarının aynasıdır.
Kodlar Google Colab'da Drive'dan çalışır. Repodaki dosya adları Drive'dakiyle birebir aynıdır; yeni dosya açma, kopya üretme.

## İletişim
- Her zaman Türkçe yaz. Açıklamalar kısa ve öz olsun, önemli noktalar mutlaka belirtilsin.
- Cemal mobilden çalışır. Sonucu tek, indirilebilir dosya olarak ver; uzun kod bloğunu sohbete yapıştırma.
- Kod kutusunu yalnızca Colab'a yapıştırılacak komut için kullan ve kutunun üstüne "Colab'a yapıştır" yaz. Dosya adlarını ve yollarını (ör. col_tarayici içindeki COL_v1.py) düz metinle yaz, kutuya koyma. Cemal kutudaki her şeyi Colab'a yapıştırıyor; 20 Ekim'de dosya yolu yapıştırılınca SyntaxError çıktı.
- Cemal grafik okur ve alım-satım kararını kendisi verir. Claude kodu yazar, ölçer, veriyi toplar.
- Her yeni iz/bulgu için Cemal'e grafikli kısa bir DERS PDF'i hazırlanır (Cemal, 24 Ekim 2026): iz nedir, nerede saklanır, grafikte nasıl görünür ve görünmez, test sonucu (eşli kat + 1,3 çizgisi), kendisi nasıl bakar. Örnek: `arastirma_cikti/fon_izi/FON_IZI_ders.pdf` (FON_IZI K12). Çürüyen ölçü için de kısa ders verilir: neden iz değil.
- Görev bitmeden tur bitmez (Cemal, 21 Ekim 2026): bir iş akışı veya uzun ölçüm başlatıldığında Claude sonucu kendisi bekler (ön planda döngüyle, gerekirse birkaç kez) ve bütün sonucu tek mesajda yazar. "Çalışıyor, bitince yazarım" diye ara mesaj atıp Cemal'den yeni mesaj beklenmez; son görev de dahil hiçbir görevde bekleme moduna girilmez. Birden fazla görev verildiyse hepsi bitince tek rapor.

## Kod standardı (kesin kural)
- Basit veya geçici yama yok. Kod üretim kalitesinde olacak: KURAL_MOTORU mimarisi, tam hata yakalama, loglama, tek dosya.
- Düzeltmede çalışan kısma dokunma, yalnızca hatalı kısmı değiştir. Bağlam kopmasın, baştan yazma.
- Ölçüm modüllerinde "çakışma kapısı" bulunur: yüklenirken bellekteki mevcut bir adı ezerse durur. Bu kapıyı koru.
- Basit hatalar mekanik olarak yakalanmalı (ad çakışması, yanlış dosya, yanlış evren). Değişiklikten sonra ilgili `test_*.py` dosyasını çalıştır.
- Colab'da `exec()` önbelleği kalıcı sorun yaratır. Kod değiştiyse kullanıcıya "çalışma zamanını yeniden başlat" diye hatırlat.

## Dosyalar
- Üretim zinciri: `BASLAT.py` (tek satır başlatma) → `COL_v1.py` (segment + AL kuralı + `bugun_liste`) → `takip.py` (`gun()`, pozisyon takibi). Yardımcılar: `temel.py`, `fon_takip.py`, `onbellek.py`, `veri_koru.py`.
- Ölçüm: `OLCUM.py`, `olcum_denetimi.py`, `zincir_denetimi.py`, `DENETIM.py`.
- Proje özeti: `COL_OZET.md` (kurallar, dosyalar, bütün testler). Bulgu defteri: `IZ_DEFTERI.md`. Yeni bulgu bu deftere eklenir, ama yalnızca gerçek iz eklenir.
- `col_atilim_TEK.py`, `tema_col.py`, `tema_sepet.py` ve `selale.py` eski ve kapalı denemelerdir. Ana üretim zincirine karıştırma.

## Veri (repoda yok)
- Veri dosyaları Drive'da kalır, repoya konmaz: `.pkl`, `.csv` çıktıları ve büyük önbellekler.
- Günlük önbellek `/content/drive/MyDrive/col_tarayici/veri_1d_turkey.pkl` yolundadır. Yapısı `kayit` ve `veri` anahtarlı bir sözlük; 583 sembol, Haziran 2023'ten itibaren. Yeni tarayıcı veya test bu önbellekten okur, veriyi yeniden indirmez.
- Test önbellekleri: OB24, OB23, OBUS ve OBUS21 (`onbellek_ABD_2022_23.pkl`).
- İstisna (24 Ekim 2026, Cemal'in isteği): KAP fon portföy raporları paketi (liste, ayrıştırılmış tablolar, 25 bin ham rapor metni; 220 MB) repoda ayrı `kapfon-veri` dalında durur, `main`'e birleştirilmez. Açma `python FON_IZI.py k9ac kapfon`, güncelleme yalnız yeni raporları indirir (`k9indir` + `k10`), sonra `k9paket` ile dal yenilenir.
- Repodaki tek veri istisnası küçük ayar dosyalarıdır: `sektor_BIST.csv` (BIST alt endekslerinden kurulan sektörler; Yahoo sektör etiketleri hatalı), `sektor_ABD.csv` ve `.json` ayarları.
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
- Her test iki dönemde (2023 ve 2024-26) ve ABD verisinde çalıştırılır. Eşikler sabittir, kâr/zarar trail ile hesaplanır, slot simülasyonu yapılır, taban oranı en az 1,3x olmalıdır.
- Bir ölçü bir testte pozitif, başka bir testte negatif çıkıyorsa iz sayılmaz. Küçük örneklemden çıkan sonuç "bulgu" diye sunulmaz.
- Desene veya tek göstergeye göre alım-satım yoktur. Tarayıcı yalnızca aday bulur.
- Kapanmış konuları yeniden açma (`COL_OZET.md` listesine bak): giriş zamanlaması/onay/hacim, stop/erken kesme, sektör ısısı, KNN, VIX/DXY, 90'dan fazla şekil ölçüsü.
