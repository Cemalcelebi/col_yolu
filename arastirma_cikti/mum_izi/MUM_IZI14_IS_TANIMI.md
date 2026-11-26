# MUM_IZI EK 14 İŞ TANIMI — HAKEM v4: Cemal'in dokuzuncu ölçütü, etiketli tek öğrenme dosyası, iki aşamalı hakem, yeni onay seti (26 Kasım 2026)

Yazan: ana model. Cemal (26 Kas, işaretli MUM_IZI12_ONAY ile birlikte; harfiyen): "bölgenin komplesine bakınca düşüş ve bir tepki gibi durup düşeni kırmamış, genel yön adayıymış gibi görüntü sergiliyor ise olmaz / kısmen; düşüş bitmiş, net; ve o düşüşün durağında küçük mum, Bollinger daralması; ve son bölümde özellikle üst Bollinger bandını altında takip, birebir izleme ile o bölge geçiliyor bir görüntü olmalı."

Durum (Ç238, Ç240): hakem v3'ün seçtiği 24 bölgeden Cemal 11'ine BENZİYOR, 8'ine KISMEN, 5'ine BENZEMİYOR dedi (önceki tur 7 / 8 / 9). Onay eşiği: sayfaların en az %80'ine tam ✓ (24 sayfada 19). Tespit hâlâ GEÇERSİZ. Bu iş yalnız TESPİT içindir: getiri / sonrası hesaplanmaz, sonrası hiçbir sayfada gösterilmez.

## 0. Kesin kurallar (bütün alt ajanlar)

- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/. Önerilen kayıt metni raporda kalır.
- `git add -A` / `commit -a` YASAK; yalnız kendi yolların. Commit mesajına, rapora, koda etiket-sayfa eşlemesi, hisse adı-sayfa eşlemesi YAZILMAZ (25 Kas mühür sızıntısı dersi). Dal: ccr-82c0570b-j2nhsg.
- Veri <= 2022-12-31 (kasa açılmaz); /root/.kasa ve /tmp/veri* yalnız okunur. Sayfalarda hisse adı, tarih, fiyat ekseni etiketi, sonrası YOK.
- Kod işi başında `python IZ_KARNE.py kontrol istanimi` okunur; raporda KONTROL LİSTESİ (ölçüm olmadığı için uygulanmayan maddeler UYGULANMAZ + gerekçe) ve HATA başlıkları zorunludur.
- Beklenti cümlesi yalnız ölçülmüş orandan yazılır (hakem v3: 24'te 11 tam, 8 kısmen); tahmin yazılmaz.

## 1. İŞ A (kod; opus) — MUM_IZI_HAKEM.py'ye üç ek, çalışan kısma dokunmadan

A1. `aday --parti 3`: 600 YENİ aday, `arastirma_cikti/mum_izi/hakem_aday3/` (mum_izi14_aday_1..12.pdf, 50'şer sayfa, sayfa numarası 1-600, + mühürlü anahtar). Seçim kuralı, sayfa düzeni ve günlük / haftalık katman payları 2. partiyle AYNI; önceki bütün setler (MUM_IZI4 / 6 / 8 / 9 / 10 / 12) ve 1. - 2. parti hariç. 1. ve 2. partinin anahtar sha'ları değişmemeli (test). Haftalık aday yetmezse eksik raporlanır, günlükle doldurulmaz.

A2. `ogren`: ETİKETLİ TEK ÖĞRENME DOSYASI `arastirma_cikti/mum_izi/MUM_IZI14_OGREN.pdf`. Kaynak: MUM_IZI10_ONAY.pdf (bölge sayfaları 2-25) + MUM_IZI12_ONAY.pdf (2-25) = 48 sayfa; etiket kaynağı cemal_mum_izi10_onay.json ve cemal_mum_izi12_onay.json. Her sayfanın üstüne büyük, okunaklı etiket şeridi basılır: 'CEMAL: BENZİYOR' (yeşil) / 'CEMAL: KISMEN' (turuncu) / 'CEMAL: BENZEMİYOR' (kırmızı) + 'Örnek n / 48'. Sıra: önce BENZİYOR (18), sonra KISMEN (16), sonra BENZEMİYOR (14). Sayfadaki eski 'Sayfa N' başlığı ve işaret kutuları görünüyorsa kalabilir; hisse adı / tarih eklenmez. Sağlama: sınıf sayıları json ile eşit (18 / 16 / 14); rastgele 6 sayfa PNG'ye çevrilip basılı etiketin json'la aynı olduğu gözle doğrulanır (raporda). MUM_IZI4 seti alınmaz (o tur Cemal 'hepsi birebir değil, biraz benzeyen var' dedi; KISMEN sınıfı yoktu).

A3. `onay` iki aşamalı seçim: `--hakem` (1. aşama json'ları; karar EVET / KISMEN / HAYIR üçü de kabul) + yeni `--hakem2 <json>` (2. aşama). SEÇİM KURALI (önceden; sonuçtan sonra değişmez): aday = 1. aşama EVET. Sıra: (a) 2. aşama da EVET olanlar, puan1 + puan2 büyükten küçüğe; (b) 2. aşama KISMEN olanlar, aynı sırayla; eşitlikte küçük sayfa numarası. 2. aşama HAYIR olan sete girmez. Set = ilk 24 (varsa); PDF içi sayfa sırası tohumlu rastgele. Mühürlü anahtara iki hakemin karar + puanı ve (a) / (b) sınıfı yazılır; PDF'e yazılmaz. `--hakem2` verilmezse eski davranış aynen (geriye uyum testi). Kapak yer tutucuları {M} {N} {K} + yeni {N2} (iki hakemin de EVET dediği).

A4. Testler: mevcut hakem testleri + yeni sentetik testler (parti 3 hariç tutma, etiket şeridi sayımı, iki aşamalı sıra, KISMEN kabulü, geriye uyum). Çakışma kapısı korunur. Sonra `aday --parti 3` ve `ogren` koşulur, çıktı PDF'leri + kod + test + kısa rapor (MUM_IZI14_KOD_RAPOR.md) commit + push. Hakem json'ları ve onay PDF'i bu işte üretilmez.

## 2. İŞ B (1. aşama hakem; 4 x sonnet, her biri 150 aday)

Hakem v3 metni + 9. madde + tek öğrenme dosyası. Çıktı: hakem_aday3/mum_izi14_hakem_A..D.json ({"hakem", "ogrenme_notu", "ogrenme_bakilan", "sayfalar": {"n": {"karar", "puan", "gerekce"}}}). Hakemler anahtar, cemal_*, isaretli, öteki hakem dosyalarını açmaz.

## 3. İŞ C (2. aşama hakem; 1 x sonnet, bağımsız)

Ana model 1. aşama EVET sayfalarına aynı sayıda rastgele (tohum 14) 1. aşama KISMEN / HAYIR sayfası katar, karıştırır; 2. aşama hakemi hangisinin hangisi olduğunu bilmez, 1. aşama dosyalarını açmaz. Çıktı: hakem_aday3/mum_izi14_hakem2.json (aynı şema). Bilgi: iki aşamanın uyumu (kappa) kayda geçer.

## 4. Derleme ve mühür (ana model)

Hakem json'ları commit (mühür) -> `python MUM_IZI_HAKEM.py onay --hakem ...A-D --hakem2 ... --aday arastirma_cikti/mum_izi/hakem_aday3 --ad MUM_IZI14` -> ana model en az 6 sayfayı kalıbın yanında gözle karşılaştırır (tahmin yazmaz) -> MUM_IZI14_ONAY.pdf Cemal'e. Set 12 sayfadan azsa 4. parti (300 aday) aynı kuralla açılır. Onay eşiği: sayfaların >= %80'i tam ✓. Cemal'in yeni işaretleri (✓ / kısmen / ✗) sonra MUM_IZI_GOZ2 ile aynı tanımlarla sonrası ölçümüne 'set 6' olarak eklenir.
