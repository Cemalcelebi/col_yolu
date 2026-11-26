# MUM_IZI EK 14 — İŞ A kod raporu (26 Kasım 2026)

İş tanımı: MUM_IZI14_IS_TANIMI.md, bölüm 0 ve 1 (A1-A4). Bu iş yalnız TESPİT altyapısıdır: getiri / sonrası hesaplanmadı, hiçbir sayfada sonrası yok.
Hakem json'ları ve onay PDF'i bu işte üretilmedi (İŞ B / C / 4. bölüm).

## Sonuç

- A1 `aday --parti 3`: 600 aday, hakem_aday3/mum_izi14_aday_1..12.pdf (50'şer sayfa, toplam 600 sayfa, numara 1-600 kesintisiz) + mum_izi14_aday_anahtar.json (mühürlü).
  Günlük 300 / haftalık 300 (eksik yok). Pazar: günlük ABD 242, AVR 32, BIST 26; haftalık ABD 241, AVR 25, BIST 34 (BIST her dilimde <= %20). Tohum 25112131.
  Hariç: MUM_IZI4 / 6 / 8 / 9 anahtarları + 1. parti + 2. parti + mum_izi10_onay ve MUM_IZI12_onay anahtarları (1.012 hisse); 3. partiyle kesişim 0 (test).
  Seçim kuralı, sayfa düzeni, katman payları 2. partiyle aynı (HK_ESIK_P3; yalnız tohum, sürüm ve hariç listesi farklı). En geç bölge sonu 2022-12-12 (kesik içinde).
  Göz sağlaması: 2 rastgele aday sayfası PNG'ye çevrilip bakıldı: solda 'Senin kalıbın', sağda bölge turuncu kutu, başlık 'Sayfa N: bulunan bölge (… mum)', hisse / tarih / sonrası yok; 2. partiyle aynı düzen.
- A2 `ogren`: MUM_IZI14_OGREN.pdf, 48 sayfa; sınıf sayıları json ile aynı: BENZİYOR 18, KISMEN 16, BENZEMİYOR 14. Sıra: sınıf, sonra kaynak (10, 12), sonra sayfa.
  Kaynak sayfalar pypdf ile bozulmadan alındı; sayfa üstten 78 pt genişletildi, şerit eski sayfa sınırının üstünde (grafik örtülmez). Kaynak PDF sha'ları onay anahtarlarındaki pdf_sha ile denetlendi (işaretsiz özgün); etiket 'zaman' alanı onay anahtarıyla karşılaştırıldı (yanlış dosya kapısı).
  Göz sağlaması: 6 rastgele sayfa PNG'ye çevrilip bakıldı; altısında da basılı etiket json'daki etiketle aynı.
- A3 `onay --hakem2`: iki aşamalı seçim (HK_ESIK_ONAY2, tohum 25112141): aday = 1. aşama EVET; (a) 2. aşama EVET, (b) 2. aşama KISMEN; her sınıfta puan1 + puan2 büyükten küçüğe, eşitlikte küçük sayfa; HAYIR girmez; ilk 24; PDF sırası tohumlu. 1. aşama EVET olup 2. aşama dosyasında olmayan sayfa -> DUR; set 0 -> DUR; < 12 -> uyarı.
  Anahtara iki hakemin karar + puanı ve sınıf (a / b) yazılır, PDF'e yazılmaz. Hakem şeması artık KISMEN'i kabul eder; tek aşamalı onayda yalnız EVET seçilir (eski davranış).
  Kapak yer tutucuları {M} {N} {K} {N2}; --kapak yoksa iki aşamalıda nötr HK_KAPAK2 (beklenti cümlesi yok).
  Kullanım: `python MUM_IZI_HAKEM.py onay --hakem <A.json> <B.json> <C.json> <D.json> --hakem2 <hakem2.json> --aday arastirma_cikti/mum_izi/hakem_aday3 --ad MUM_IZI14 --kapak "<metin; {M} {N} {N2} {K}>"`
- A4 testler: test_mum_izi10.py 19 / 19 geçti (8 eski + 11 yeni).

## Testler (yeni)

1. / 2. parti anahtar sha'ları ve eşik sha'ları değişmedi; 2. parti seçimi anahtarla birebir yeniden üretilir; parti 3 eşik / hariç listesi (sentetik: hariç kesişimi 0, eksik anahtar DUR); parti 3 gerçek anahtar (1-600, kesişim 0, BIST payı, kesik, yeniden üretim); KISMEN kabulü; iki aşamalı sıra (a önce b, puan toplamı, eşitlik, HAYIR dışı, eksik 2. aşama DUR, boş set DUR, tohumlu sıra); kapak {N2}; öğrenme şeridi (sentetik 48 sayfa: sayım, sıra, şerit metni, sayfa yüksekliği, üzerine yazmama, eksik etiket DUR); gerçek öğrenme kaynakları (48, sınıf = json); geriye uyum (--hakem2 olmadan MUM_IZI12 onayı aynı girdilerle yeniden kuruldu: anahtar sayfaları, kapak ve PDF sha'sı eskisiyle birebir); iki aşamalı uçtan uca (gerçek 2. parti adayları, sentetik 2. aşama). Çakışma kapısı testi geçer.

## KONTROL LİSTESİ

| Madde | Durum | Kanıt / gerekçe |
|---|---|---|
| K1 kontrol grubu | UYGULANMAZ | ölçüm yok; yalnız aday / öğrenme / onay altyapısı |
| K2 geleceğe bakma | EVET | sayfalarda bölge sonrası yok; aday bölge sonu <= 2022-12-31 kodda denetlenir (KESİK AŞIMI) |
| K3 geçerli bar | UYGULANMAZ | aday olayları MUM_IZI8 taramasından aynen; yeni olay üretilmedi |
| K4 tekilleştirme | EVET | hisse başına bir aday; önceki setlerle kesişim 0 (test) |
| K5 giriş fiyatı | UYGULANMAZ | getiri yok |
| K6 veri birimi | UYGULANMAZ | çizim mevcut mv_veri ile; yeni veri yok |
| K7 hayatta kalma | UYGULANMAZ | ölçüm yok |
| K8 örneklem / dönem | UYGULANMAZ | ölçüm yok |
| K9 ön kayıt | EVET | iki aşamalı seçim kuralı iş tanımında (3905e89) önceden yazılı, HK_ESIK_ONAY2 aynen; hakem sonucu yok |
| K10 ayrıştırma | EVET | etiket json'ları kod içinde şema / sayfa / zaman / pdf sha denetiminden geçer; 6 sayfa gözle |
| K11 yeniden üretim | EVET | 1. / 2. parti seçim yeniden üretimi; MUM_IZI12 onayı birebir (pdf sha) |
| K12 ifade | EVET | beklenti / tahmin cümlesi yok |
| K13 süreç | EVET | çakışma kapısı korundu; yasak dosyalara dokunulmadı; yalnız kendi yollar commit; e-posta / anahtar yok |
| K14 boyut | UYGULANMAZ | öneri işi değil |

Kod değişti: Colab'da kullanılacaksa çalışma zamanını yeniden başlat.

## HATA

- Yok (bu işte yanlış hesap bulunmadı). Not: çalışma ağacında MUM_IZI_GOZ2.py başka bir işin (EK 15) commit edilmemiş değişikliğini taşıyordu; bu commit'e alınmadı.
