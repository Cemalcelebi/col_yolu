# MUM_IZI EK 18 — İŞ A kod raporu (26 Kasım 2026)

İş tanımı: MUM_IZI18_IS_TANIMI.md (21ff575), bölüm 0, 1 ve 2 (A1-A5). Yalnız TESPİT altyapısı: getiri / sonrası hesaplanmadı, hiçbir sayfada sonrası,
hisse adı, tarih ya da fiyat yok. Hakem json'ları ve onay PDF'i bu işte üretilmedi (3. bölüm).

## Sonuç

### A1 havuz sayımı (getirisiz; MUM_IZI8 v5M taraması, evren içi olaylar)

ORAN = hk_boy_olcu (ölçekli sayfanın mum boyu satırıyla aynı fonksiyon; ikinci tanım yok). Paylar ORAN hesaplanabilen olaylar üzerinden
(önceki >= 40 bar). Dosya: hakem_aday4/mum_izi18_havuz_sayim.json.

| Grup | Dilim | Olay n | ORAN var n | <= 0,85 | <= 0,70 | <= 0,50 | Kapıdan geçen olay / hisse |
|---|---|---|---|---|---|---|---|
| Bütün havuz | günlük | 4.612 | 4.607 | %29,9 | %6,6 | %0,4 | 306 / 279 |
| Bütün havuz | haftalık | 1.399 | 1.361 | %26,9 | %10,8 | %0,4 | 147 / 141 |
| 1.-3. partide gösterilen bölgeler | günlük | 750 | 750 | %31,1 | %6,4 | %0,3 | 48 / 48 |
| 1.-3. partide gösterilen bölgeler | haftalık | 750 | 725 | %26,2 | %10,5 | %0,4 | 76 / 76 |
| Hissesi hiç gösterilmemiş | günlük | 1.723 | 1.718 | %28,0 | %5,8 | %0,4 | 99 / 96 |
| Hissesi hiç gösterilmemiş | haftalık | 192 | 187 | %21,9 | %8,0 | %1,1 | 15 / 15 |

Hariç tutulan hisse: 1.612 (MUM_IZI4 / 6 / 8 / 9 anahtarları, 1.-3. parti, MUM_IZI10 / 12 / 14 onay anahtarları). Hiç gösterilmemiş havuzda kapıdan
geçen: 111 hisse (günlük 96, haftalık 15; iki dilimde ortak hisse yok). Katman (olay): günlük ÇOK KÜÇÜK 7 / KÜÇÜK 92, haftalık 2 / 13.

### A2 `aday --parti 4`

- 111 aday (hedef 600'ün altında: kapıdan geçen her yeni hisse alındı). Günlük 96 (eksik 204), haftalık 15 (eksik 285); öteki dilimle doldurulmadı.
- Pazar: günlük ABD 69, AVR 5, BIST 22; haftalık ABD 10, BIST 5. BIST tavanı uygulanmadı (iş tanımı: 600'den azsa hepsi); BIST payı günlükte %23.
- Katman: günlük KÜÇÜK 89, ÇOK KÜÇÜK 7; haftalık KÜÇÜK 13, ÇOK KÜÇÜK 2.
- Dosyalar: hakem_aday4/mum_izi18_aday_1.pdf (sayfa 1-50), _2.pdf (51-100), _3.pdf (101-111) + mum_izi18_aday_anahtar.json (mühürlü; sha a859f799…1744;
  her sayfada ORAN, katman, boy, önceki, önceki_n). Tohum 25112181; eşik HK_ESIK_P4 (HK-P4-1.0).
- Sayfa: _hk_sayfa_olcek ile (yüzde ekseni, uç fitil kesimi, mum boyu satırı + oran), işaret kutusu yok. Her sayfada sayfanın oranı seçimdeki oranla birebir
  denetlendi (değilse DUR).
- Hisse başına bir aday (önceki partilerle aynı): günlükte kapıdan geçen 99 olay 96 hisseye düştü (3 olay aynı hissenin ikinci olayı).
- Göz sağlaması (PNG): sayfa 7 (günlük, ORAN 0,47, ÇOK KÜÇÜK) ve sayfa 105 (günlük, ORAN 0,63, 'önceki 80 mumunda'): yüzde ekseni sağda, 0 = son kapanış,
  eksi işaretleri var; mum boyu satırı anahtardaki boy / önceki / oranla aynı; kutu yok; hisse / tarih / sonrası yok.

### A3 `ogren --olcek`

- MUM_IZI18_OGREN.pdf, 65 sayfa (sha a6854ddd…6cdb). Önce MUM_IZI14 ölçekli 17 bölge (şerit 'CEMAL (ölçekli sayfada): …'): BENZİYOR 4, KISMEN 7,
  BENZEMİYOR 6; sonra MUM_IZI10 + 12 48 bölge (şerit 'CEMAL (eski, ölçeksiz sayfada): …'): BENZİYOR 18, KISMEN 16, BENZEMİYOR 14. Sayılar json'larla eşit (test).
- Bölgeler mühürlü onay anahtarlarından yeniden çizildi (kutusuz ölçekli sayfa, başlık 'Örnek n'); sayfa üstten 78 pt genişletildi, şerit grafiğin üstünde.
  Denetimler: etiket sayfaları tam aralık, etiket zamanı anahtarla aynı, bölge başı anahtarla aynı, MUM_IZI10 / 12 anahtarlarının pdf_sha'sı özgün PDF'le aynı,
  MUM_IZI14 anahtarının sha'sı ölçekli json'daki eski_anahtar_sha ile aynı.
- 17 ölçekli bölgenin ORAN'ı MUM_IZI14_onay_olcekli.json'dakiyle 17 / 17 aynı (ayrı kodla yeniden hesap).
- Göz sağlaması: 6 sayfa (11, 14, 20, 53, 55, 64; tohumla seçildi; iki grup) PNG'ye çevrildi: şeritteki etiket altısında da json'daki etiketle aynı
  (KISMEN, BENZEMİYOR, BENZİYOR, BENZEMİYOR, BENZEMİYOR, BENZEMİYOR); zaman (günlük / haftalık) başlıkla aynı; yüzde ekseni ve mum boyu satırı var.

### A4 `onay --olcek` parti 4

Aday klasörünün anahtarı ölçekli partiye (4) aitse YENİ ölçekli set kurulur (eski yeniden basım yolu 1-3 için aynen). Kullanım:

`python MUM_IZI_HAKEM.py onay --hakem <1.aşama.json> [<…>] --hakem2 <2.aşama.json> --aday arastirma_cikti/mum_izi/hakem_aday4 --ad MUM_IZI18 --olcek [--kapak "<metin; {M} {N} {N2} {K}>"]`

Çıktı: MUM_IZI18_ONAY_OLCEKLI.pdf (kapak + set, üç kutu, mum boyu satırında ORAN), MUM_IZI18_onay_anahtar.json (mühürlü: hisse, tarih, iki hakemin
kararı / puanı, sınıf), MUM_IZI18_onay_olcekli.json (hisse / tarih yok). Seçim HK-O4: a / b sınıfı EK 14 kuralı aynen (hk_onay_sec2, tohum 25112141;
doldurma yoksa sonuç onunla birebir, test); set 12'den azsa 1. aşama KISMEN ve puan1 >= 6 ile 12'ye tamamlanır ve kapağa 'Set 12 sayfadan az kaldığı için
ilk hakemin kısmen dediği C sayfayla 12'ye tamamlandı.' eklenir. Kapılar (DUR): --ad / --hakem2 yok; çıktılardan biri var; 1. aşama hakemleri bütün aday
sayfalarını kapsamıyor; yabancı sayfa; sayfa ORAN'ı aday anahtarındakinden farklı. --kapak verilmezse HK_KAPAK4 (adayların ORAN <= 0,70 kapısından geçtiği yazılı).

### A5 testler

test_mum_izi10.py: 34 / 34 geçti (25 eski + 9 yeni). Yeni: eski mühürler (parti 1-3 anahtar sha'ları, P3 / ölçek / onay2 eşik sha'ları, MUM_IZI14_OGREN.pdf
yeniden üretilip sha birebir; 1-3 partileri yeni onay yoluna sapmaz); kapı sınırı (0,70 dahil, 0,7001 hariç, NaN hariç; katman 0,50 sınırı); 40 bar kuralı
(40 aday, 39 değil); geleceğe bakma (bölge sonrası bozulunca ORAN aynı); KESİK aşımı DUR; parti 4 seçimi (kapı, hariç, hisse başına bir, eksik dilim
doldurulmaz, BIST tavanı yok, eksik anahtar DUR); havuz sayımı; HK-O4 (doldurma yokken EK 14 ile birebir, 12'ye tamamlama sırası, puan < 6 girmez, boş DUR);
parti 4 gerçek anahtar (6 sayfanın ORAN'ı bağımsız kodla yeniden, seçim ve havuz sayımı yeniden üretimi, dosya sha'ları, kutusuz ölçekli sayfa); yeni onay
uçtan uca (sentetik iki hakem; json'da hisse / tarih yok; üç kapı DUR); ölçekli öğrenme (65 sayfa, her şerit = json, eksik etiket DUR). Eski onay / ölçekli
onay testleri (MUM_IZI12 ve MUM_IZI14 PDF sha birebir) geçti. Çakışma kapısı testi geçer.

## KONTROL LİSTESİ

| Madde | Durum | Kanıt / gerekçe |
|---|---|---|
| K1 kontrol grubu | UYGULANMAZ | ölçüm / getiri yok; yalnız aday, öğrenme ve onay altyapısı |
| K2 geleceğe bakma | EVET | ORAN yalnız bölge sonu t'ye kadarki barlar (hk_boy_olcu diziyi t + 1'de keser, assert); test: sonrası bozulunca aynı; bölge sonu <= 2022-12-31 kodda (KESİK DUR) |
| K3 geçerli bar | UYGULANMAZ | olaylar MUM_IZI8 taramasından aynen; ORAN tanımı EK 16 ile aynı (H = L barı 0 boy; kısıt aşağıda) |
| K4 tekilleştirme | EVET | hisse başına bir aday; önceki bütün set / partilerle hisse kesişimi 0 (test) |
| K5 giriş fiyatı | UYGULANMAZ | getiri yok |
| K6 veri birimi | EVET | ORAN birimsiz (oran); veri mevcut mv_veri ile |
| K7 hayatta kalma | UYGULANMAZ | ölçüm yok (havuz sayımı yalnız betimleme) |
| K8 örneklem / dönem | UYGULANMAZ | ölçüm yok; havuz sayıları betimleme |
| K9 ön kayıt | EVET | kapı eşiği 0,70 ve katmanlar iş tanımında (21ff575) önceden; HK_ESIK_P4 / HK_ESIK_ONAY4 aynen; eşik sonuca göre oynanmadı |
| K10 ayrıştırma | EVET | etiket json'ları sayfa aralığı / sınıf / zaman / anahtar sha denetiminden geçer; 6 öğrenme + 2 aday sayfası gözle |
| K11 yeniden üretim | EVET | ORAN 6 aday + 17 öğrenme bölgesinde bağımsız kodla aynı; seçim ve havuz sayımı yeniden üretilir; eski PDF'ler birebir |
| K12 ifade | EVET | sayfalarda yorum / beklenti yok; kapakta yalnız kapı tanımı |
| K13 süreç | EVET | çakışma kapısı korundu; yasak dosyalara ve MUM_IZI_GOZ2.py / test_mum_izi13.py / mum_izi17_* dosyalarına dokunulmadı; yalnız kendi yollar commit; e-posta / anahtar yok |
| K14 boyut | UYGULANMAZ | öneri işi değil |

Kod değişti: Colab'da kullanılacaksa çalışma zamanını yeniden başlat.

## SAPMA / YORUM

- BIST tavanı: 1.-3. partideki '%20 BIST' kuralı parti 4'te uygulanmadı; iş tanımı '600'den azsa hepsini al' diyor. Günlükte BIST 22 / 96.
- 'Hepsini al' hisse başına bir okundu (önceki partilerle aynı, K4): aynı hissenin ikinci / üçüncü kapı olayı (3 olay) alınmadı.
- 12'ye tamamlama (iş tanımı 3. bölüm) koda eklendi; c sınıfında 2. aşama kararına bakılmaz (kural metninde yok). Ana model isterse değiştirilir.
- Öğrenme sayfaları kutusuz çizildi (etiket şeritte); başlık 'Sayfa N' yerine 'Örnek n' (öğrenme dosyasında sayfa numarası karışmasın).

## HATA

- Test hatası (düzeltildi): KESİK testinde sentetik serinin son tarihi 2022 içinde kalıyordu; test başlangıcı 2022-06'ya alındı.
- Test hatası (düzeltildi): HK-O4 testindeki sentetik KISMEN puanları 12'ye tamamlamaya yetmiyordu (beklenti yanlıştı, kod değil).
- Yanlış hesap bulunmadı.

## Kalan kısıt

- Kapıdan geçen yeni aday 111 (hedef 600): günlük 204, haftalık 285 eksik. Havuzda haftalık hiç gösterilmemiş hisse yalnız 192 olay; kapı payı %8.
  Daha çok aday için yeni tarama (kural / dönem) gerekir; bu iş tanımının dışında.
- 111 adayda 1. aşama tek hakemle (150'lik dilim) kapsanır; iki aşamalı seçimde set 12'nin altında kalabilir (12'ye tamamlama kuralı hazır).
- H = L (kilitli) barlar ORAN'da 0 boy sayılır (EK 16 tanımı); BIST tavan / taban serilerinde ORAN'ı küçük gösterebilir.
- MUM_IZI18_OGREN.pdf 5,2 MB (65 sayfa; şerit yazı tipi her sayfada gömülü).
