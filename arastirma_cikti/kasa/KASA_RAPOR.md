# KASA — mühürlü veri blokları aracı: teslim raporu (21 Kasım 2026)

Kod: `KASA.py` (tek dosya, çakışma kapısı, KasaHata ile tam hata yakalama, `col.kasa` logu; muhurle / ac sırasında `<kasa dizini>/kasa.log`).
Test: `python test_kasa.py` -> 15/15 bölüm GEÇTİ (yalnız sentetik veri). Gerçek veri MÜHÜRLENMEDİ; yalnız şifrelemesiz kuru sayım yapıldı.

## Kullanım (5 satır)
1. `KASA_GIZLI=<repo ve scratchpad DIŞI yol> python KASA.py kur` -> açık anahtar `arastirma_cikti/kasa/kasa_acik_anahtar.pem` (repoya girer), gizli anahtar yalnız o yola (0600). Yol hiçbir çıktıya yazılmaz.
2. `python KASA.py muhurle --kesik 2025-12-31 --cikti /tmp/kasa` -> `/tmp/kasa/acik/V_*.pkl` (alt modele verilen tek veri, `oc_veri(klasor=...)` biçimi aynı) + `/tmp/kasa/muhurlu/*.kasa` + `arastirma_cikti/kasa/KASA_MANIFEST.json`.
3. Alt model ölçümden önce `kasa_kapisi(veri_yolu)` ya da `python KASA.py denetim <dosya...>` çağırır; açık kesikten sonra tarih varsa çıkış kodu 2.
4. `KASA_GIZLI=<yol> python KASA.py ac --blok 2026Q1 --hipotez <kod> --onkayit <yol>` (ön kayıtta `KASA_HIPOTEZ: <kod>` ve `KASA_KOD: <repo içi yol> <sha256>` + dolu KONTROL LİSTESİ; git'e işlenmiş). Sonra `KASA_DEFTERI.md` commit edilir.
5. `python KASA.py durum` (açık kesik, bloklar, defter); yeni veri gelince `python KASA.py muhurle --ekle --kaynak <yeni veri klasörü>`.

## Şifreleme
Hibrit ECIES: blok başına geçici X25519 anahtarı + alıcı açık anahtarla ECDH, HKDF-SHA256 (RFC 5869), AES-256-GCM (cryptography 50.0.1; başlık AAD).
cryptography yoksa openssl CLI: aynı X25519 + HKDF, AES-256-CBC + HMAC-SHA256 (şifrele-sonra-MAC). PEM biçimleri iki yolda ortak (testte çapraz tur).
`KASA_PAROLA` ortam değişkeni varsa gizli PEM parolayla şifrelenir. Kasa dosyası manifestteki sha256 ile, çözülen düz metin `duz_sha256` ile denetlenir.

## Kuru sayım (kesik 2025-12-31, takvim çeyreği; şifreleme yok; `python KASA.py say --kesik 2025-12-31`)

| Dosya | Blok | Satır | Sembol | İlk | Son |
|---|---|---:|---:|---|---|
| V_ABD.pkl | AÇIK | 3.148.675 | 1.411 | 2015-06-01 | 2025-12-31 |
| V_ABD.pkl | 2026Q1 | 86.071 | 1.411 | 2026-01-02 | 2026-03-31 |
| V_ABD.pkl | 2026Q2 | 87.482 | 1.411 | 2026-04-01 | 2026-06-30 |
| V_ABD.pkl | 2026Q3 | 90.304 | 1.411 | 2026-07-01 | 2026-09-30 |
| V_ABD.pkl | 2026Q4 | 22.568 | 1.411 | 2026-10-01 | 2026-10-22 |
| V_AVR.pkl | AÇIK | 1.526.609 | 581 | 2015-01-01 | 2025-12-31 |
| V_AVR.pkl | 2026Q1 | 36.461 | 580 | 2026-01-02 | 2026-03-31 |
| V_AVR.pkl | 2026Q2 | 35.440 | 580 | 2026-04-01 | 2026-06-30 |
| V_AVR.pkl | 2026Q3 | 37.951 | 580 | 2026-07-01 | 2026-09-30 |
| V_AVR.pkl | 2026Q4 | 10.453 | 580 | 2026-10-01 | 2026-10-27 |
| V_BIST.pkl | AÇIK | 1.155.527 | 581 | 2015-06-01 | 2025-12-31 |
| V_BIST.pkl | 2026Q1 | 36.022 | 581 | 2026-01-02 | 2026-03-31 |
| V_BIST.pkl | 2026Q2 | 34.279 | 581 | 2026-04-01 | 2026-06-30 |
| V_BIST.pkl | 2026Q3 | 37.765 | 581 | 2026-07-01 | 2026-09-30 |
| V_BIST.pkl | 2026Q4 | 9.296 | 581 | 2026-10-01 | 2026-10-22 |
| k34_yahoo.pkl (veri2) | AÇIK | 2.402.902 | 2.051 | 2020-10-01 | 2025-12-31 |
| k34_yahoo.pkl (veri2) | 2026Q1 | 125.124 | 2.065 | 2026-01-02 | 2026-03-31 |
| k34_yahoo.pkl (veri2) | 2026Q2 | 128.344 | 2.077 | 2026-04-01 | 2026-06-30 |
| k34_yahoo.pkl (veri2) | 2026Q3 | 133.207 | 2.089 | 2026-07-01 | 2026-09-30 |
| k34_yahoo.pkl (veri2) | 2026Q4 | 39.494 | 2.225 | 2026-10-01 | 2026-10-27 |

Notlar: 2026Q4 yarım çeyrek (veri sonu; açılınca açık kesik veri sonu olur, çeyrek sonu değil). Kesikten sonra doğan semboller açık kısma girmez
(k34_yahoo'da 2026Q4'te 2.225 sembol, açıkta 2.051). Aylık bloklar (`--blok ay`) da sayıldı: V_ABD 10 ay blok, 22.568-31.042 satır.
Fon krizi kesiği (31.08.2026) KASA'nın işi değil; ölçüm modülleri kendi kesiğini uygulamaya devam eder.

## Sınırlar
- Kasa fiziksel engel değil SÜREÇ KAPISIDIR: aynı fiyatlar islenmis-veri dalında, /tmp/veri'de ve Yahoo'da açık durur. Alt modele yalnız `/tmp/kasa/acik` verilir, ölçüm koşusu `kasa_kapisi` / `denetim` ile başlar, tek kullanım defteri (`KASA_DEFTERI.md`) iz bırakır.
- Aynı konteynerde çalışan alt model gizli anahtar dosyasını teknik olarak okuyabilir; gizli anahtar bu yüzden repo / scratchpad dışında tutulur ve yolu yalnız ana modelin ortamında (KASA_GIZLI) durur. İstenirse `KASA_PAROLA` ile ek koruma.
- ORTAK_CETVEL.oc_veri ABD için `/tmp/veri2/k34_yahoo.pkl`'yi ayrıca okur: k34_yahoo da mühürlenmezse SIZINTI olur. Öneri: dört dosyayı tek kaynak klasörde bağla (komutlar teslim mesajında) ve alt modele `oc_veri(p, klasor="/tmp/kasa/acik", veri2="/tmp/kasa/acik")` ver.
- Evren bugünün listesidir (hayatta kalma yanlılığı); kesikten sonra doğan sembollerin varlığı açık kısımdan gizlenir, ama evren listesi (sektor_*.csv, evren_disi) gizlenmez.
- Gerçek kör veri bugünden sonra gelen veridir: yeni veri `muhurle --ekle` ile doğrudan mühürlenir (dönem zaten varsa parça adı `2026Q4-2`). Ekle, manifestteki son tarihten (bütün dosyalarda ortak) sonrasını mühürler; ondan önce kalıp eski mühürde olmayan satırlar mühürlenmez ve manifestte `taban_oncesi_kayip_satir` olarak yazılır.
- Bir blok bir hipotez için açıldıktan sonra başka hipotez o bloğu yalnız ön kaydı İLK açılıştan önce git'e işlenmişse kullanabilir (defter satırı 'kayıt'); sonra yazılmış ön kayıt durur.
- `/tmp/kasa` silinirse açık kısım ve şifreli bloklar kaybolur (manifest ve defter repoda kalır); kasa aynı kaynakla `muhurle --uzerine` ile yeniden kurulur, eski defter yeni mühür kimliğiyle karışmaz.

## HATA
- H1 (test kurgusu, düzeltildi): 13. bölümde ekle verisi aynı tohumla ama farklı uzunlukta üretildi; seriler ilk mühürdekinin devamı değildi. Test, tam seriden kesilmiş kopyayla yeniden kuruldu.
- H2 (test kurgusu, düzeltildi): açık anahtar gizli anahtarla aynı klasöre konunca kur durdu (tasarım gereği doğru); test açık anahtarı ayrı klasöre aldı.
- H3 (kod, düzeltildi): openssl hata mesajı dosya yolu içerebilirdi; `_ossl` artık bütün yol argümanlarını ve KASA_GIZLI değerini mesajdan siler.
- H4 (kod, önlendi): `--dosya` mutlak yol olsaydı açık kısım kaynağın üzerine yazılabilirdi; `_dosya_adlari` yalnız .pkl dosya adı kabul eder (testte).
- Gerçek veride sırasız seri yok (V_ABD / V_AVR / V_BIST: 0). Sırasız seri olsaydı bölmeden önce kararlı sıralanırdı (birleşim sıralı özgüne eşit; test 9).

## KONTROL LİSTESİ
| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | araç ölçüm yapmaz; eş / plasebo ölçüm modülünde kalır |
| K2 | geleceğe bakma | EVET | açık kısım tarih <= kesik (test 3); kasa_kapisi / denetim kesik aşımında durur (test 10); kesik sonrası doğan sembol açık kısımda yok |
| K3 | geçerli bar | UYGULANMAZ | KASA satır süzmez; geçerli bar süzgeci ORTAK_CETVEL.oc_veri_hazirla'da aynen kalır (biçim korunur) |
| K4 | tekilleştirme | UYGULANMAZ | olay sayımı yok; tek kullanım defteri aynı (blok, hipotez) çiftini ikinci kez açmaz (test 8) |
| K5 | giriş fiyatı | UYGULANMAZ | fiyat hesaplanmaz |
| K6 | veri birimi | EVET | veri baytı değişmeden bölünür / birleşir: birleşim özgünle değer, dizin, dtype eşit (test 9, 13); Kur sütunu korunur |
| K7 | hayatta kalma | EVET | evren bugünün listesi; raporda 'Sınırlar' bölümünde yazılı |
| K8 | örneklem ve dönem | UYGULANMAZ | sonuç / bulgu yok; blok sayım tablosu yukarıda |
| K9 | ön kayıt | EVET | ac kapısı: ön kayıt git'e işlenmiş + değişmemiş, kod sha eşit, IZ_KARNE kontrol tablosu dolu (test 6) |
| K10 | ayrıştırma | UYGULANMAZ | ham kaynak ayrıştırılmaz; pickle sözlükleri aynen bölünür |
| K11 | yeniden üretim | EVET | kuru sayım toplamı özgün satır toplamına eşit (test 14); çözülen blok duz_sha256 ve satır sayısıyla denetlenir |
| K12 | ifade | EVET | rapor yalnız araç özelliği ve sayım; iz / bulgu iddiası yok |
| K13 | süreç | EVET | çakışma kapısı (test 1); defter / üretim / cetvel2 dosyalarına dokunulmadı; e-posta / anahtar taraması (test 15); gizli yol hiçbir çıktıda yok (test 11) |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / alım işi değil |
