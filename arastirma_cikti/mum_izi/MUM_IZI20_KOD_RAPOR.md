# MUM_IZI EK 20 — kod raporu: katmanlı ölçekli onay seti (26 Kasım 2026)

İş tanımı: MUM_IZI20_IS_TANIMI.md (f218598), "Tasarım" ve "İŞ (kod)". Yalnız TESPİT: getiri / sonrası hesaplanmadı; sayfada sonrası, hisse adı,
tarih, fiyat, katman ve hakem kararı yok (katman / hakem kararı yalnız mühürlü anahtarda).

## Sonuç

- Getirisiz sayım (kod DUR kapısıyla doğruladı; iş tanımıyla aynı): kapıdan geçen 111 adaydan Cemal'e gösterilen 12 çıkınca kalan 99;
  KISMEN x oran <= 0,65: 16; KISMEN x 0,65 < oran <= 0,70: 23; HAYIR x oran <= 0,65: 34; HAYIR x 0,65 < oran <= 0,70: 26; kalanlarda hakem EVET yok.
  Test bağımsız sayımla da aynı sonucu verdi.
- Set: 24 bölge, katman başına 6 (6 / 6 / 6 / 6); günlük 18, haftalık 6. Kapak + 24 sayfa = 25 sayfa.
- 24 bölgede mum boyu (bölge medyanı, %): en küçük 0,40, medyan 2,41, en büyük 9,26; oran: en küçük 0,21, medyan 0,65, en büyük 0,70 (0,699).
- Dosyalar: MUM_IZI20_ONAY_OLCEKLI.pdf (sha be3dc6a4…7e6a), MUM_IZI20_onay_anahtar.json (mühürlü: yeni sayfa, aday sayfa, zaman, pazar, sembol,
  bölge başı / sonu, pencere, oran, hakem kararı / puanı, katman; sayım; hariç 12 aday sayfa; girdi sha'ları), MUM_IZI20_onay_olcekli.json
  (sayfa ölçüleri; hisse / tarih / katman / hakem kararı yok).

Kullanım:

`python MUM_IZI_HAKEM.py onay --olcek --katmanli --hakem arastirma_cikti/mum_izi/hakem_aday4/mum_izi18_hakem_A.json --aday arastirma_cikti/mum_izi/hakem_aday4 --haric arastirma_cikti/mum_izi/MUM_IZI18_onay_anahtar.json --ad MUM_IZI20`

## Kod (MUM_IZI_HAKEM.py, yeni bölüm 3d; çalışan kısım değişmedi)

- HK_ESIK_ONAY5 (HK-O5-1.0; sha 0b8a14dc…): tohum 20, katman başına 6, oran eşiği 0,65, kapı 0,70, dört katman ve iş tanımındaki beklenen sayım.
- hk_katman5: KISMEN / HAYIR x (oran <= 0,65 | 0,65 < oran <= 0,70); EVET, şema dışı karar, NaN ya da 0,70 üstü oran DUR.
- hk_katman_sec (saf): hariç sayfalar çıkar; hakem kapsamı eksikse, kalanlarda EVET varsa, sayım beklenenden farklıysa, bir katmanda < 6 aday varsa DUR.
  Tek rng (tohum 20): katman sırasıyla her katman aday sayfa sırasına dizilip karıştırılır, ilk 6; sonra 24 sayfanın PDF sırası aynı rng ile karıştırılır,
  yeni sayfa numaraları 2'den.
- hk_onay_katman: kapılar (DUR): --ad yok; çıktılardan biri zaten var; aday klasörü ölçekli parti (4) değil; hariç anahtarın aday_anahtar_sha'sı aday
  anahtarıyla aynı değil ya da hariç sayfaların zaman / pazar / sembol / bölge sonu aday anahtarıyla uyuşmuyor; hakemde yabancı sayfa; bölge başı ya da
  sayfa ORAN'ı aday anahtarından farklı; KESİK aşımı. Hata olursa yarım PDF silinir. Sayfa çizimi `_hk_sayfa_olcek` (EK 16: yüzde ekseni, mum boyu satırı,
  ✓ / K / × kutuları) aynen; kapak başlığı 'MUM BOYU ŞARTINI GEÇEN BÖLGELER', kapak metni iş tanımındaki metin aynen ({K} = 24).
- Argparse: `--katmanli` (yalnız `--olcek` ile), `--haric`. Eski komutların yolu değişmedi. Çakışma kapısı korundu.

## Testler (test_mum_izi10.py)

39 / 39 geçti (34 eski + 5 yeni). Yeni: katman sınırı (0,65 dahil alt katman, 0,6501 üst; 0,70 dahil; EVET / NaN / 0,7001 DUR); sentetik seçim
(6 / 6 / 6 / 6, hariç, tohum tekrarı, tohum değişince seçim değişir, sıra karışık, beş kapı DUR); gerçek getirisiz sayım (99; 16 / 23 / 34 / 26, bağımsız sayımla);
uçtan uca (iki koşu aynı pdf ve anahtar sha; 25 sayfa; kapak metni; PDF metninde katman adları, KISMEN / HAYIR / EVET, 'katman', hakem gerekçesi, hisse, tarih yok;
json'da hisse / tarih / katman / hakem yok; repodaki MUM_IZI20 set birebir; mühürlü EK 18 dosyaları (hakem_A, hakem2, MUM_IZI18 PDF, MUM_IZI18 anahtar)
sha'ları değişmez; üç kapı DUR); MUM_IZI18 ölçekli onay seti aynı girdilerle yeniden kurulup pdf sha (75e563dd…3187), sayfalar ve kapak birebir.
Test dosyasına süzgeç eklendi: `python test_mum_izi10.py ek20` yalnız adında 'ek20' geçen testleri koşar (argümansız: hepsi).

Göz sağlaması (PNG, 60 dpi): kapak (başlık + iş tanımı metni + 'Senin kalıbın'), sayfa 2 (günlük), 10 ve 25 (haftalık):
sağda yüzde ekseni (0 = son kapanış), turuncu bölge kutusu, mum boyu satırı ve oran, üç kutu var; katman, hakem kararı, hisse, tarih, fiyat yok.

## KONTROL LİSTESİ

| Madde | Durum | Kanıt / gerekçe |
|---|---|---|
| K1 kontrol grubu | UYGULANMAZ | ölçüm / getiri yok; yalnız onay seti |
| K2 geleceğe bakma | EVET | sayfa çizimi ve ORAN yalnız bölge sonuna kadarki barlar (`_hk_sayfa_olcek` / `hk_boy_olcu`, EK 16 testleri); sayfa ORAN'ı aday anahtarıyla birebir (DUR); KESİK DUR |
| K3 geçerli bar | UYGULANMAZ | adaylar 4. partiden aynen; ORAN tanımı EK 16 ile aynı |
| K4 tekilleştirme | EVET | 4. parti hisse başına bir; 24 sayfada aday sayfa tekil (test); Cemal'e gösterilmiş 12 bölge hariç (test) |
| K5 giriş fiyatı | UYGULANMAZ | getiri yok |
| K6 veri birimi | UYGULANMAZ | yeni ölçü yok; oran birimsiz, aday anahtarındakiyle aynı |
| K7 hayatta kalma | UYGULANMAZ | ölçüm yok |
| K8 örneklem / dönem | UYGULANMAZ | ölçüm yok; ön kayıtlı sorular (H1 / H2) Cemal'in işaretlerinden sonra, n küçük, karar vermez (iş tanımı) |
| K9 ön kayıt | EVET | katmanlar, tohum 20, 6'şar seçim, kapak metni iş tanımında (f218598) koddan önce; HK_ESIK_ONAY5 iş tanımıyla aynı; seçim sonucuna göre değiştirilmedi |
| K10 ayrıştırma | EVET | hakem json şeması (`hk_hakem_oku`), hariç anahtar sayfaları aday anahtarıyla alan alan denetlenir; 3 veri sayfası + kapak gözle |
| K11 yeniden üretim | EVET | sayım bağımsız kodla aynı; iki koşu aynı pdf sha; MUM_IZI18 seti birebir yeniden üretildi |
| K12 ifade | EVET | sayfalarda yorum / beklenti yok; kapak iş tanımındaki metin aynen |
| K13 süreç | EVET | çakışma kapısı korundu; yasak dosyalara ve öteki alt ajanın dosyalarına dokunulmadı; yalnız kendi yollar commit; e-posta / anahtar yok |
| K14 boyut | UYGULANMAZ | öneri işi değil |

Kod değişti: Colab'da kullanılacaksa çalışma zamanını yeniden başlat.

## SAPMA / YORUM

- Sıra kuralı yazıya döküldü (iş tanımı yalnız 'tohumlu rastgele' diyordu): tek rng (tohum 20), katman sırası KISMEN <= 0,65, KISMEN > 0,65, HAYIR <= 0,65,
  HAYIR > 0,65; her katmanda aday sayfa sırası, sonra karıştırma; PDF sırası aynı rng'nin sonraki permütasyonu. HK_ESIK_ONAY5 'secim' metninde mühürlü.
- Sayfa düzeni (kutular, mum boyu satırı) EK 18 onay sayfasıyla aynı; yalnız kapak başlığı farklı ('GÖRSEL HAKEMİN SEÇTİĞİ' yerine 'MUM BOYU ŞARTINI GEÇEN BÖLGELER',
  çünkü bu sette hakem seçmedi).
- Sayfadaki oran satırı (tasarım gereği) katmanın oran yarısını iki ondalıkla gösterir (ör. 0,65 yuvarlaması iki katmana da düşebilir); hakem yarısı sayfada yok.

## HATA

- Test hatası (düzeltildi): ilk sentetik seride oranlar 0,40-0,70 arası tekdüze çekildiği için bir katmanda 6'dan az aday kaldı (beklenti yanlıştı, kod değil);
  sentetik oranlar dört katmana yayıldı.
- Yanlış hesap bulunmadı.

## Kalan kısıt

- Haftalık bölge az: kalan 99 adayın 14'ü haftalık; sette 6 haftalık (seçim katmanla, zaman dengesi kuralı yok).
- Tam test dosyası ~11 dk (gerçek veri; MUM_IZI18 ve MUM_IZI20 setleri yeniden kuruluyor).
- H = L (kilitli) barlar ORAN'da 0 boy sayılır (EK 16 tanımı; EK 18 kısıtı aynen).
