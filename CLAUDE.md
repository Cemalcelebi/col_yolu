# Çöl Yolu — Claude Code çalışma kuralları

Bu repo, Cemal'in Google Drive `MyDrive/col_tarayici/` klasöründeki Çöl Yolu (BIST çöl formasyonu) kodlarının aynasıdır.
Kodlar Google Colab'da Drive'dan çalışır. Repodaki dosya adları Drive'dakiyle birebir aynıdır; yeni dosya açma, kopya üretme.

## İletişim
- Her zaman Türkçe yaz. Açıklamalar kısa ve öz olsun, önemli noktalar mutlaka belirtilsin.
- Cemal mobilden çalışır. Sonucu tek, indirilebilir dosya olarak ver; uzun kod bloğunu sohbete yapıştırma.
- Cemal grafik okur ve alım-satım kararını kendisi verir. Claude kodu yazar, ölçer, veriyi toplar.

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
- Repodaki tek veri istisnası küçük ayar dosyalarıdır: `sektor_BIST.csv` (BIST alt endekslerinden kurulan sektörler; Yahoo sektör etiketleri hatalı), `sektor_ABD.csv` ve `.json` ayarları.
- Token, şifre, Telegram anahtarı gibi bilgiler asla koda yazılmaz. Bunlar `.env` dosyasında tutulur ve `.env` git dışındadır.

## GitHub Actions günlük tarama (2026-10-19)
- `.github/workflows/gunluk_tarama.yml` iş günleri 19:35 TR saatinde `gh_gunluk.py` dosyasını çalıştırır. Bu dosya `BASLAT.py`'yi exec eder, ardından `gun()`'ü çağırır.
- Kodlardaki sabit Drive yolu, iş akışında `/content/drive/MyDrive/col_tarayici → repo kökü` sembolik bağlantısıyla karşılanır. Bu yüzden Colab koduna Actions için değişiklik yapılmaz.
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
