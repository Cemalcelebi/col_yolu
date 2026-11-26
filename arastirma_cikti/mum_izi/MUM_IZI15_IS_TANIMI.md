# MUM_IZI EK 15 İŞ TANIMI — KOPMA AYRIMI: Cemal'in işaretlediği bölgelerde 'düşüşten kopmuş' / 'düşüş baskısı altında' ayrımı sonrasını ayırıyor mu (26 Kasım 2026)

Yazan: ana model. Cemal (26 Kas, MUM_IZI13_SONRASI'yı gördükten sonra; yazdığı gibi): "Ama bak sen göndermeden demiştim bir kaç bölgede bir kopmayı göstermeli özelikle son bölüm mumları kötü olsn düşüş baskısının altında sobradini görünce". Ana modelin okuması (yorum): kalıp düşüşten KOPMAYI göstermeli; sonrası kötü giden bölgeler, son bölüm mumları kötü ve düşüş baskısı altında kalanlardır. Bu, dokuzuncu ölçütün (EK 14: 'düşüş içinde tepki gibi durup düşeni kırmamışsa olmaz / kısmen; düşüş net bitmiş; sonda üst bandı alttan birebir izleyerek o bölge geçiliyor') sonrasına dair iddiasıdır.

SINIR (önceden yazılı): ölçüt, Cemal ilk bakışın sonrasını (MUM_IZI11, 104 bölge) gördükten SONRA söylendi ve Cemal 128 bölgenin sonrasını gördü. Bu yüzden ayrımı Cemal değil, sonrasını GÖRMEYEN hakemler yapar; yine de ölçütün kendisi bu bölgelerden esinlenmiş olabilir: sonuç GERİYE DÖNÜK BİLGİDİR, karar vermez. Asıl sınama EK 14 setidir (Cemal sonrasını görmeden işaretler; set 6).

## 0. Kesin kurallar

- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/. `git add -A` / `commit -a` yasak; yalnız kendi yolların. Aynı dalda başka alt ajanlar çalışıyor (MUM_IZI_HAKEM.py, hakem_aday3/): onların dosyalarına dokunma; index.lock görürsen bekle, yeniden dene.
- Hakemler: sonrasını, Cemal'in işaretlerini, olay dosyalarını görmez (yasak liste hakem metninde). Hesap ajanı hakem json'larını commit'ten (mühür) SONRA okur.
- Tanımlar MUM_IZI11 / 13 ile AYNEN (mum_izi13_olay.csv satırları değişmez: R15, es_R15, fark = R15 - es_R15, sinif, zaman). Yeni getiri hesabı yok; yalnız gruplama.
- Kod işi başında `python IZ_KARNE.py kontrol istanimi`; ön kayıt (MUM_IZI15_ON_KAYIT.md: kod sha, hakem json sha, getirisiz sayımlar, KONTROL LİSTESİ) hesaptan ÖNCE commit; `IZ_KARNE.ik_kontrol_kapisi(onkayit)` geçmeden hesap başlamaz. Rapor başlıkları: KONTROL LİSTESİ, HATA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.

## 1. Hakem (2 x sonnet, bağımsız: K1, K2)

Sayfalar (işaretsiz PDF'ler; anahtar = dosyanın fiziksel sayfa sırası): set1 = MUM_IZI4_ONAY.pdf 3-26; set2 = MUM_IZI6_ETIKET.pdf 2-49; set3 = MUM_IZI8_ONAY.pdf 3-26; set4 = MUM_IZI10_ONAY.pdf 2-25; set5 = MUM_IZI12_ONAY.pdf 2-25. Her sayfa için k: KOPMUS / BASKI / BELIRSIZ, puan 0-10 (10 = net kopmuş), gerekçe.
- KOPMUS: önceki düşüş net bitmiş; fiyat düşeni (düşen tepeler hattını, düşüş baskısını) kırmış; bölge o düşüşün durağında küçük mum + Bollinger daralması; son bölümde mumlar üst bandı alttan birebir izleyerek bölgeyi geçiyor.
- BASKI: bölgenin bütününe bakınca düşüş + tepki; düşen kırılmamış; son bölüm mumları kötü (iri kırmızı, bandın altına sarkan, yukarı yol almayan), düşüş baskısı sürüyor.
Çıktı: mum_izi15_kopma_K1.json / _K2.json.

## 2. Gruplama (hesaptan önce sabit)

- UZLAŞI: iki hakem de KOPMUS -> 'KOPMUS'; ikisi de BASKI -> 'BASKI'; ötekiler 'KARISIK'. Duyarlılık: ortalama puan >= 6 'KOPMUS*', <= 4 'BASKI*'. Hakem uyumu (kappa) ve set2'deki 8 tekrar sayfasında hakemin kendi tutarlılığı raporlanır.
- ANA TABLO: Cemal EVET bölgeleri (36; haftalık 20, günlük 16) x UZLAŞI: n, R15 ortalama / medyan, eşli fark ortalama / medyan, artıda payı (R15 > 0), eşinden iyi payı (fark > 0); KOPMUS - BASKI eşli fark farkı, permütasyon p (10.000, tohum 15). Haftalık, günlük ve birlikte.
- İKİNCİ: EVET + KISMEN (52). ÜÇÜNCÜ: 128 bölgenin tamamı (ölçüt tek başına, Cemal'in işaretinden bağımsız).
- OKUMA KURALI: 'AYRIM YÖNÜ CEMAL'İN DEDİĞİ GİBİ' <=> EVET içinde KOPMUS eşli fark ortalaması > 0 VE KOPMUS - BASKI > 0, haftalıkta ve günlükte aynı yönde. Hangi sonuç çıkarsa çıksın etiket 'BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK' (bütün gruplar n < 30); eşik / gruplama sonuca göre değişmez; değişirse SAPMA.
- Eş sınırı (Ç229 / Ç240): eşler bölgenin kendi koşusuyla eşlenmedi; raporda yazılır.

## 3. Çıktılar

MUM_IZI_GOZ2.py'ye `kopma` komutu (çalışan kısma dokunmadan) + testi; MUM_IZI15_ON_KAYIT.md, MUM_IZI15_RAPOR.md, mum_izi15_sonuc.json, mum_izi15_olay.csv (128 satır + iki hakem etiketi + uzlaşı). PDF üretilmez.
