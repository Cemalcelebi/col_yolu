# K60-EK ÖN KAYIT — asimetri ölçütü (KASA açılmadan önce yazıldı)

Yazım: 2026-11-11, KEŞİF ve DOĞRULAMA görüldükten SONRA, KASA açılmadan ÖNCE (kasa_acildi.json yok; bu dosyanın commit zamanı
kasa_meta.json 'kos_baslangic' değerinden öncedir). Yazan: ana model. K60_ON_KAYIT.md (mühür e1749249eeb8) ve K60.py DEĞİŞMEZ;
K60'ın kendi etiketleri (§7) aynen üretilir. Bu ek, onların YANINA üç etiket koyar.

## Neden
KEŞİF'te R2 ailesinde 167 hipotezin 106'sı BH'den geçti, DOĞRULAMA'ya giren 125 çiftin 109'u geçti. Sebep sinyal değil OYNAKLIK:
herhangi bir ölçünün uç onluğu evren ortalamasından daha oynak hisselerden oluşur ve hem +%100 hem -%50 olasılığı birlikte artar
(96 çift R2, 93 çift R2K geçti; ikisi birden). '+%100 lift > 1' tek başına karar bilgisi değildir. Karar bilgisi ASİMETRİdir:
kazanma olasılığı, batma olasılığından daha çok artıyor mu.

## Tanımlar (12 ay ufuk; <dönem>_r2_aylik.csv aylık sayımlarından; ufuk sütunu varsa 12)
- lift_p100, lift_m50: K60 §5 ile aynı (havuz oranı / evren oranı).
- ASIM = lift_p100 / lift_m50.
- Aralık: K60 §5 ile AYNI çekilişler (ay kümeli dairesel blok bootstrap, blok 12 ay, 500 çekiliş, tohum 60002; K60'ın çekiliş
  dizini fonksiyonu içe aktarılır). Her çekilişte ASIM yeniden hesaplanır; %95 aralık = %2.5 ve %97.5 dilimleri. Bir çekilişte
  payda sıfırsa o çekiliş atlanır; geçerli çekiliş < 400 ise 'ölçülemez'.
- Uç ortalama / medyan 12 ay getirisi ve evren karşılıkları: <dönem>_r2.csv (ort, medyan, taban_ort, taban_medyan).
- R1 net fazla: <dönem>_r1.csv (yillik_fazla).

## Etiketler (her şart ÜÇ dönemin HER BİRİNDE: KEŞİF, DOĞRULAMA, KASA; KASA'ya girmeyen çift etiket alamaz)
- 'EK-ASİMETRİK FIRSAT' ⇔ lift_p100 %95 alt sınırı > 1 VE ASIM %95 alt sınırı > 1 VE uç ortalaması > evren ortalaması.
- 'EK-GÜVENLİ UÇ' ⇔ lift_m50 %95 üst sınırı < 1 VE R1 net yıllık fazla > 0.
- 'EK-PİYANGO UCU (kaçın)' ⇔ lift_m50 %95 alt sınırı > 1 VE ASIM nokta değeri < 1 VE uç medyanı < evren medyanı.
- 'YAKIN' (bilgi): şartları iki dönemde sağlayıp üçüncüde yalnız aralık şartını kaçıran (nokta değeri doğru yönde) çift.

## Yanlış keşif sınaması
Aynı üç etiket kuralı plasebolara uygulanır (dönem plasebolarının aylık sayımları K60 fonksiyonları içe aktarılarak yeniden
üretilebiliyorsa; K60.py değiştirilmez). Bir dönemde tek başına şartı sağlayan plasebo oranı yazılır. Üretilemiyorsa
'plasebo sınaması yok' yazılır ve etiketler 'bilgi' düzeyinde kalır.

## Sınırlar
- Ek, KEŞİF ve DOĞRULAMA nokta değerleri görüldükten sonra yazıldı: o iki dönem bu etiketler için örneklem içidir; bağımsız sınama
  yalnız KASA'dır (R2'de 20 oluşum ayı; aralık geniş olacaktır).
- Yalnız yaşayanlar evreni: -%50 olasılığı ve lift_m50 alt sınırdır; 'GÜVENLİ UÇ' faydası olduğundan küçük, 'PİYANGO UCU' zararı
  olduğundan küçük ölçülür; 'ASİMETRİK FIRSAT' yukarı yanlıdır (batanlar paydada yok).
- Hiçbir etiket İZ değildir (karar hücreleri ve batanları içeren evren şartı sürer).

## Çıktı
arastirma_cikti/k60_kutuphane/k60_ek.py (yalnız çıktı dosyalarını okur), ek_tablo.csv, K60_EK_RAPOR.md.
