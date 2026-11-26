# MUM_IZI EK 22 — kod raporu: geçmişli onay sayfası ve yeni katmanlı set (26 Kasım 2026)

İş tanımı: MUM_IZI22_IS_TANIMI.md (303ae24), "Tasarım" ve "İŞ (kod)". Yalnız TESPİT: getiri / sonrası hesaplanmadı; sayfada sonrası, hisse adı,
tarih, fiyat, katman ve hakem kararı yok (katman / hakem kararı yalnız mühürlü anahtarda).

## Sonuç

- Getirisiz sayım (kod DUR kapısıyla doğruladı; iş tanımıyla aynı): kapıdan geçen 111 adaydan Cemal'e gösterilmiş 36 (MUM_IZI18: 12, MUM_IZI20: 24;
  iki anahtar çakışmıyor) çıkınca kalan 75; KISMEN x oran <= 0,65: 10; KISMEN x 0,65 < oran <= 0,70: 17; HAYIR x oran <= 0,65: 28;
  HAYIR x 0,65 < oran <= 0,70: 20; kalanlarda hakem EVET yok. Test bağımsız sayımla da aynı sonucu verdi.
- Set: 24 bölge, katman başına 6 (6 / 6 / 6 / 6); günlük 20, haftalık 4. Kapak + 24 sayfa = 25 sayfa.
- Uzak görünümde kullanılan önceki bar sayısı: en küçük 57, medyan 120, en büyük 120 (24 sayfanın 21'inde tam 120; üçünde hissenin geçmişi kısa: 57 / 74 / 97).
- Oran: en küçük 0,25, medyan 0,65, en büyük 0,70 (0,6996).
- Dosyalar: MUM_IZI22_ONAY_GECMISLI.pdf (sha 58b9e964…7f40), MUM_IZI22_onay_anahtar.json (mühürlü: yeni sayfa, aday sayfa, zaman, pazar, sembol,
  bölge başı / sonu, pencere, oran, hakem kararı / puanı, katman, uzak_onceki_bar; sayım; iki hariç anahtar ve sha'ları; hariç 36 aday sayfa; girdi sha'ları;
  özet), MUM_IZI22_onay_olcekli.json (sayfa ölçüleri: oran, mum boyu, iki grafiğin pencere / kutu / dikey sınır / kesim sayıları; hisse / tarih / katman /
  hakem kararı yok).

Kullanım:

`python MUM_IZI_HAKEM.py onay --olcek --katmanli --gecmis --hakem arastirma_cikti/mum_izi/hakem_aday4/mum_izi18_hakem_A.json --aday arastirma_cikti/mum_izi/hakem_aday4 --haric arastirma_cikti/mum_izi/MUM_IZI18_onay_anahtar.json arastirma_cikti/mum_izi/MUM_IZI20_onay_anahtar.json --ad MUM_IZI22`

## Kod (MUM_IZI_HAKEM.py, yeni bölüm 3e; çalışan kısım değişmedi)

- HK_ESIK_ONAY6 (HK-O6-1.0): tohum 22, katman başına 6, oran eşiği 0,65, kapı 0,70, EK 20 ile aynı dört katman, iş tanımındaki beklenen sayım (75; 10 / 17 / 28 / 20),
  uzak görünüm 120 önceki mum (en az 40, yoksa DUR), sayfa boyu 8,3 x 14,5 inç ve ince mum ölçüleri.
- hk_haric_birlesik: birden çok hariç onay anahtarı; her biri aynı aday anahtarına ait (aday_anahtar_sha), her sayfası aday anahtarıyla alan alan uyuşmalı;
  aynı anahtar iki kez, boş liste, olmayan / okunamayan dosya DUR.
- Seçim: EK 20'nin saf seçim fonksiyonu (hk_katman_sec) aynen, yalnız HK-O6 eşikleriyle (tek rng, tohum 22: katman sırasıyla her katmanda aday sayfa sırası,
  karıştırma, ilk 6; sonra PDF sırası aynı rng ile karıştırılır, yeni sayfa numaraları 2'den).
- _hk_sayfa_gecmis: ÜST uzak görünüm (önceki <= 120 mum + bölge; ince mum çizimi: gövde 0,74 bar, fitil 0,55 pt; Bollinger 20 + SMA20; turuncu kutu),
  ALT yakın görünüm (EK 16 grafiği: öncesi 15 mum + bölge, MV._mv_ciz). İki grafikte de sağda yüzde ekseni (0 = bölgenin son kapanışı), sağlam dikey sınır ve
  uç fitil / bant kesimi + işaret (HK-OL kuralı, her grafik kendi penceresiyle). Altında mum boyu satırı ve ✓ / K / × kutuları; 'Senin kalıbın' paneli ve açıklama
  küçültüldü, açıklamanın ilk satırı 'Üst: bölgenin gerisi (önceki 120 mum) + bölge. Alt: yakından bölge.'. Sonrası yok: yalnız d[:t + 1] kullanılır (assert);
  bölge kutusunun iki grafikte aynı mutlak barları kapsadığı assert ile denetlenir.
- hk_onay_gecmis: kapılar (DUR): --ad yok; çıktılardan biri var; aday klasörü ölçekli parti değil; hariç anahtar kapıları; hakem kapsamı / yabancı sayfa; sayım;
  bölge başı ya da sayfa ORAN'ı aday anahtarından farklı; KESİK aşımı; < 40 önceki mum. Hata olursa yarım PDF silinir. Kapak başlığı
  'MUM BOYU ŞARTINI GEÇEN BÖLGELER (GERİSİYLE)', kapak metni iş tanımındaki metin aynen ({K} = 24).
- Argparse: `--gecmis` (yalnız `--olcek --katmanli` ile; değilse DUR), `--haric` artık bir ya da çok dosya alır; `--gecmis` yokken (EK 20 yolu) tek dosya
  zorunlu, birden çoksa DUR. Eski komutların çıktısı değişmedi (test: MUM_IZI20 komut satırından yeniden kuruldu, pdf / anahtar / json sha birebir). Çakışma
  kapısı korundu.

## Testler (test_mum_izi10.py)

Yeni 6 test (`python test_mum_izi10.py ek22`, ~2,5 dk): eşik ve kapak metni (iş tanımıyla aynı; HK-O5 / HK-OL sha'ları MUM_IZI20 anahtarındakiyle aynı);
hariç birleşimi (12 + 24 = 36, çakışma yok; beş kapı DUR); gerçek getirisiz sayım (75; 10 / 17 / 28 / 20, bağımsız sayımla; 6 / 6 / 6 / 6; gösterilmiş 36 seçilmez;
tekrar aynı; tohum seçimi belirler; tek hariçle sayım kapısı DUR); sayfa geleceğe bakmaz (bölge sonrası barlar 7 ile çarpılınca ya da seri bölge sonunda
kesilince ölçü ve PNG baytları aynı; uzak 120 / 61 / < 40 DUR; kutu iki grafikte pencerenin son m barı; ORAN EK 16 ölçüsüyle aynı); uçtan uca (iki koşu aynı pdf
ve anahtar sha; 25 sayfa; kapak; PDF metninde katman adları, KISMEN / HAYIR / EVET, 'katman', hakem gerekçesi, hisse, tarih yok; json'da hisse / tarih / katman /
hakem yok; seri_uzunluk_kullanilan = son bar + 1; repodaki MUM_IZI22 set birebir; mühürlü EK 18 / EK 20 dosyaları değişmez; dört kapı DUR, yarım PDF yok);
eski komut birebir (MUM_IZI20 komut satırından; iki --haric --gecmis olmadan DUR; --gecmis --katmanli olmadan DUR).
Tam dosya: 45 / 45 geçti (39 eski + 6 yeni; ~11 dk).

Göz sağlaması (PNG, 70-110 dpi): kapak; sayfa 2 (haftalık, 57 önceki mum), 5 (günlük, 120), 19 (haftalık, 120), 25 (günlük, 120): uzak görünümde ~140 mum
ayrı ayrı seçiliyor (gövde rengi ve fitil görünür); bölge kutusu iki grafikte aynı barları kapsıyor (kutudaki mum dizilimi iki grafikte aynı); iki grafiğin de
sağ kenarı bölgenin son mumu (sonrası yok); sağda yüzde ekseni; mum boyu satırı ve üç kutu var; katman, hakem kararı, hisse, tarih, fiyat yok.

## KONTROL LİSTESİ

| Madde | Durum | Kanıt / gerekçe |
|---|---|---|
| K1 kontrol grubu | UYGULANMAZ | ölçüm / getiri yok; yalnız onay seti |
| K2 geleceğe bakma | EVET | sayfa yalnız d[:t + 1] (assert); test: sonrası bozulunca / kesilince PNG baytı aynı; ORAN aday anahtarıyla birebir (DUR); KESİK DUR |
| K3 geçerli bar | UYGULANMAZ | adaylar 4. partiden aynen; ORAN tanımı EK 16 ile aynı |
| K4 tekilleştirme | EVET | 24 sayfada aday sayfa tekil (test); Cemal'e gösterilmiş 36 bölge hariç (test); aynı hariç anahtar iki kez DUR |
| K5 giriş fiyatı | UYGULANMAZ | getiri yok |
| K6 veri birimi | UYGULANMAZ | yeni ölçü yok; eksen yüzde, oran birimsiz |
| K7 hayatta kalma | UYGULANMAZ | ölçüm yok |
| K8 örneklem / dönem | UYGULANMAZ | ölçüm yok; ön kayıtlı soru Cemal'in işaretlerinden sonra, n 24: BİLGİ (iş tanımı) |
| K9 ön kayıt | EVET | katmanlar, tohum 22, 6'şar seçim, beklenen sayım, sayfa düzeni, kapak metni iş tanımında (303ae24) koddan önce; seçim sonucuna göre değiştirilmedi |
| K10 ayrıştırma | EVET | hakem json şeması (hk_hakem_oku); hariç anahtar sayfaları aday anahtarıyla alan alan denetlenir; 4 veri sayfası + kapak gözle |
| K11 yeniden üretim | EVET | sayım bağımsız kodla aynı; iki koşu aynı pdf sha; repodaki set testte yeniden üretildi; MUM_IZI20 seti eski komutla birebir |
| K12 ifade | EVET | sayfada yorum / beklenti yok; kapak iş tanımındaki metin aynen |
| K13 süreç | EVET | çakışma kapısı korundu; yasak dosyalara dokunulmadı; yalnız kendi yollar commit; e-posta / anahtar yok |
| K14 boyut | UYGULANMAZ | öneri işi değil |

Kod değişti: Colab'da kullanılacaksa çalışma zamanını yeniden başlat.

## SAPMA / YORUM

- Sayfa boyu A4 değil, 8,3 x 14,5 inç (iş tanımı 'gerekirse sayfayı dikey uzat' diyordu; iki grafik telefonda okunsun diye).
- Açıklama satırı her sayfada '(önceki 120 mum)' der; geçmişi kısa üç sayfada uzak görünümde 57 / 74 / 97 mum var (mum boyu satırı gerçek sayıyı yazar:
  'bu hissenin önceki N mumunda').
- Uzak görünüm grafiği yakın görünümün çizimini değil, aynı renk / bant / kutu / kesim kuralıyla ince mum çizimini kullanır (140 mumda gövde seçilsin diye).
- Kapak sayfası da 14,5 inç boyunda (sayfalar aynı boyda olsun diye); alt kısmı boş.

## HATA

- Yanlış hesap bulunmadı. Testler ilk koşuda geçti.

## Kalan kısıt

- Haftalık bölge az: kalan 75 adayın 8'i haftalık; sette 4 haftalık (seçim katmanla, zaman dengesi kuralı yok).
- Tam test dosyası ~11 dk (gerçek veri; MUM_IZI18, MUM_IZI20 ve MUM_IZI22 setleri yeniden kuruluyor).
- H = L (kilitli) barlar ORAN'da 0 boy sayılır (EK 16 tanımı aynen).
