# K60-B ÖN KAYIT — piyango havuzu İÇİNDE koşullu ayrım

Yazım: 2026-11-11, K60 (Ç154) bittikten sonra, K60-B ölçümünden ÖNCE. Yazan: ana model. K60.py ve K60 ön kayıtları DEĞİŞMEZ;
K60B.py ayrı tek dosyadır, K60 fonksiyonlarını (veri yükleme, uygunluk, sinyaller, ileri getiri, bootstrap çekiliş dizini) içe aktarır.

## Soru
K60: oynak hisselerde ikiye katlanma olasılığı 2-2,7 kat, yarıya inme 2,8-3,8 kat, medyan eksi. Cemal bu havuzdan hisse alıyor
(DGXX, QMLS tipi). Soru: HAVUZUN İÇİNDE hangi ölçülebilir özellik kazananı kaybedenden ayırıyor (ikiye katlanma olasılığını
havuz tabanına göre artırıp yarıya inmeyi artırmıyor ya da yarıya inmeyi azaltıyor)?

## Havuz (sabit, basit)
Her ay sonu t, K60 uygun evreninde 60 günlük oynaklığı (K60 VOL_60D'nin ham değeri; en az K60'taki gözlem şartı) en yüksek %20.
Havuz < 150 hisse olan ay atlanır. Havuz tabanı = havuzun bütün hisse-ayları.

## Sınanacaklar
K60 kütüphanesindeki 77 sinyal + 12 bileşik (K60'taki tanım ve bilgi tarihi kuralları aynen). Sürekli sinyalde havuz içi ÜST ve ALT
%20 (sayı = max(1, yuvarla(0.2 x havuzda sinyali olan hisse)); sinyali olan havuz hissesi < 100 olan ay o sinyal için atlanır).
Bayrakta havuz içi bayraklı grup (ayda en az 10). Ölçülebilirlik: en az 12 oluşum ayı ve uçta en az 200 hisse-ay.
Sıralama yüzdelikleri HAVUZ içinde yeniden hesaplanır (bileşikler dahil: üye sinyallerin havuz içi yüzdelik ortalaması).

## Ölçü (12 ay ana ufuk; 6 ay bilgi)
- P(+%100), P(-%50), ortalama, medyan: uç ve havuz. kat_p100 = P uç / P havuz; kat_m50 aynı; ASIM = kat_p100 / kat_m50.
- Aralık: K60 §5 bootstrap (ay kümeli dairesel blok 12 ay, 500 çekiliş, tohum 60002), %95.
- Aylık portföy (bilgi): uç eşit ağırlık, 1 ay tutma, tek yön 10 bp; kıyas = havuz eşit ağırlık; net fazla ve NW(6) t(alfa).
- Plasebo: 200 rastgele sinyal (havuz içinde rastgele sıra, default_rng(60200 + i)), ÜST %20; aynı ölçüler.
- Dönemler ve kesik K60 ile aynı: KEŞİF 2012-01..2021-12, DOĞRULAMA 2022-01..2023-12, KASA 2024-01.. (12 ay penceresi 2026-08-31'i
  aşmayan oluşum ayları).

## KEŞİF seçimi (mekanik; sonuç görülmeden yazıldı)
- 'KOŞULLU FIRSAT adayı' ⇔ kat_p100 %95 alt sınırı > 1 VE ASIM %95 alt sınırı > 1 VE uç ortalaması > havuz ortalaması VE
  ASIM > plasebo en-büyük eşiği (200 plasebo ASIM'inden hipotez sayısı kadar yerine koyarak çekilen kümenin en büyüğü, 2000 tekrar,
  tohum 60203; %95 dilimi).
- 'KOŞULLU KORUMA adayı' ⇔ kat_m50 %95 üst sınırı < 1 VE kat_p100 nokta >= 0,90 VE uç medyanı > havuz medyanı VE
  kat_m50 < plasebo en-küçük eşiği (aynı yöntem, en küçüğün %5 dilimi).
- Ayrıca BH %10 (p = ASIM > 1 için z yaklaşımı; koruma için kat_m50 < 1) raporlanır; seçim şartı değildir (plasebo eşiği daha sıkı).

## DOĞRULAMA ve KASA (yalnız KEŞİF adayları; aynı yön)
- FIRSAT geçer ⇔ kat_p100 alt > 1 VE ASIM alt > 1 VE uç ort. > havuz ort. VE ASIM > o dönemin 200 plasebo ASIM'inin %95 dilimi.
- KORUMA geçer ⇔ kat_m50 üst < 1 VE kat_p100 >= 0,90 VE uç medyanı > havuz medyanı VE kat_m50 < plasebo kat_m50'lerinin %5 dilimi.
- Etiket: 'K60B-KOŞULLU FIRSAT' / 'K60B-KOŞULLU KORUMA' ⇔ KEŞİF adayı VE DOĞRULAMA geçti VE KASA geçti. İki dönem geçip üçüncüde
  yalnız aralık / plasebo şartını kaçıran (nokta değerler doğru yönde) 'YAKIN'.
- Cetvel sağlaması: bir dönemde plasebonun tek başına FIRSAT ya da KORUMA şartlarını (plasebo dilim şartı hariç) sağlama oranı
  yazılır; > %5 ise o dönem için 'aralık dar' notu düşer.

## Önceden adı konan başlık satırları (seçilsin seçilmesin raporda üç dönem yan yana yazılır)
DOSYA_Y ÜST, COMP4 ÜST, SP ÜST, NEF ÜST, SALES_ACCEL ÜST, REV_YOY (varsa) ÜST, EAR_ANN ÜST, RUNWAY ÜST ve ALT, NSI_1Y ÜST ve ALT,
E_S3 bayraklı, E_424B5 bayraklı, E_RSPLIT bayraklı, HIGH52 ÜST ve ALT, MOM_12_1 ÜST ve ALT, SIZE_ME iki uç, PRICE_LVL iki uç,
ROA_Q iki uç, BM ÜST.

## Sınırlar (beyan)
- KASA bu sinyallerin MARJİNAL sonuçları için K60'ta bir kez açıldı; havuz içi koşullu sonuçlar görülmedi. Yine de KASA ikinci kez
  kullanılıyor: etiketler 'bilgi' düzeyindedir, İZ değildir.
- Yalnız yaşayanlar: havuz batanlara en açık yerdir; P(-%50) alt sınırdır, 'FIRSAT' yukarı yanlıdır.
- Kapalı konular (hacim, giriş zamanlaması) kütüphanede K60'taki gibi durur; ayrı karar üretmez.

## Çıktı
K60B.py, test_k60b.py (kök dizin; sentetik test: geleceğe bakma, havuz kuralı, elle kat hesabı, plasebo tohumu, seçim kuralı),
arastirma_cikti/k60_kutuphane/k60b_tablo.csv, k60b_aylik.csv (aylık sayımlar; her sayı buradan yeniden üretilir),
k60b_plasebo.csv, k60b_meta.json (bu dosyanın sha256'sı, K60.py sha256, veri sha'ları, koşu zamanı), K60B_RAPOR.md.
