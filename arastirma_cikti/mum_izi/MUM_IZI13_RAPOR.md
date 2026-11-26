# MUM_IZI13 RAPOR (2026-11-26): göz ölçümünün İKİNCİ BAKIŞI (set 5) ve BİRLEŞİK (BİLGİ)

Ön kayıt: MUM_IZI13_ON_KAYIT.md (d95aa1b; set 5 getirilerinden önce). Tanımlar MUM_IZI11 ile AYNEN (MUM_IZI_GOZ.py değişmedi; ESIK11_SHA aynı). Kod: MUM_IZI_GOZ2.py,
test_mum_izi13.py (5 / 5). n < 30 hücreler 'örneklem yetersiz'; 'iz / tuttu' sözü yok; kasa açılmaz.

## SONUÇ (tek bakışta)

- İkinci bakış (yeni 24 bölge) ilk bakışın günlük yönünü TEKRARLAMADI (EVET - HAYIR eşli: ilk +5,7 puan, yeni -1,6 puan; EVET - eş: ilk +%3,6, yeni -%3,3); haftalıkta EVET yine eşlerinin gerisinde (ilk -%16,2, yeni -%15,1; aynı yön) ama yeni sette n 5 ve aralık çok geniş (-52,9..+9,1).
- Birleşik (128 bölge): haftalık BENZİYOR 20 bölge R15 -%4,5, eşlerinden -%15,9 (%95 -31,2..-3,8; işaret çevirme p 0,024); günlük BENZİYOR 16 bölge eşlerinden +%0,7 (p 0,88). EVET - HAYIR haftalık eşli -14,9 puan (p 0,075), günlük +2,7 (p 0,51).
- Cemal'in 'benziyor' dediği bölgelerin sonrası eşlerinden ya da 'benzemiyor'dan iyi değil; haftalıkta tutarlı biçimde geride (bilgi; n < 30).

## ÖRNEKLEM

| küme | EVET (günlük / haftalık) | KISMEN | HAYIR (günlük / haftalık) | toplam |
|---|---|---|---|---|
| set 5 (MUM_IZI12_ONAY) | 11 (5 / 6) | 8 (5 / 3) | 5 (4 / 1) | 24 |
| birleşik set 1-5 | 36 (16 / 20) | 16 (10 / 6) | 76 (40 / 36) | 128 |

- Ölçülemeyen: 0 (set 5'te en geç 15. mum 2022-02-07). Eşsiz: set 5'te 1 (eş < 5); birleşikte 11 (eş < 5: 7, kova yok: 4).
- Set 5 pazar: ABD 21, AVR 2, BIST 1.
- Set 1-4 olayları birleşik koşuda yeniden hesaplandı: MUM_IZI11 ile 104 satırın hiçbirinde R15 / eş / eşli fark / eş sayısı farkı yok.

## TABLOLAR

İkinci bakış (yalnız set 5; hepsi örneklem yetersiz):

| sınıf | dilim | n (eşli) | R15 ort / medyan | eş ort | eşli fark ort (%95) | artıda | dokunma | stop |
|---|---|---|---|---|---|---|---|---|
| EVET | günlük | 5 (5) | -%0,4 / -%3,0 | +%2,9 | -%3,3 (-13,9..+10,9) | %20 | +5: %40, +10: %20 | %20 |
| KISMEN | günlük | 5 (5) | +%3,3 / +%1,9 | +%1,1 | +%2,1 (+0,2..+4,5) | %80 | +5: %60, +10: %0 | %0 |
| HAYIR | günlük | 4 (4) | -%2,8 / -%1,8 | -%1,1 | -%1,7 (-6,0..+2,6) | %0 | +5: %0, +10: %0 | %0 |
| EVET | haftalık | 6 (5) | -%9,1 / -%9,0 | +%12,9 | -%15,1 (-52,9..+9,1) | %33 | +10: %50, +20: %50 | %33 |
| KISMEN | haftalık | 3 (3) | +%18,3 / +%17,5 | +%6,4 | +%11,9 (+2,7..+20,9) | %100 | +10: %100, +20: %67 | %0 |
| HAYIR | haftalık | 1 (1) | +%10,7 | +%26,9 | -%16,2 | %100 | +10: %100, +20: %0 | %0 |

Birleşik (set 1-5):

| sınıf | dilim | n (eşli) | R15 ort / medyan | eş ort | eşli fark ort (%95) | artıda | dokunma | stop | etiket |
|---|---|---|---|---|---|---|---|---|---|
| EVET | günlük | 16 (12) | -%1,7 / -%2,0 | -%0,9 | +%0,7 (-7,9..+9,6) | %31 | +5: %62, +10: %38 | %12 | örneklem yetersiz |
| KISMEN | günlük | 10 (9) | -%1,3 / -%1,1 | -%0,9 | -%0,0 (-2,2..+2,3) | %40 | +5: %40, +10: %10 | %20 | örneklem yetersiz |
| HAYIR | günlük | 40 (38) | +%1,3 / -%0,4 | +%2,5 | -%2,0 (-5,4..+1,5) | %48 | +5: %55, +10: %28 | %12 | bilgi |
| EVET | haftalık | 20 (18) | -%4,5 / -%1,5 | +%12,2 | -%15,9 (-31,2..-3,8) | %40 | +10: %55, +20: %40 | %15 | örneklem yetersiz |
| KISMEN | haftalık | 6 (6) | +%12,2 / +%14,6 | +%6,1 | +%6,1 (-3,2..+14,1) | %83 | +10: %83, +20: %67 | %33 | örneklem yetersiz |
| HAYIR | haftalık | 36 (34) | +%7,1 / +%0,9 | +%6,9 | -%1,0 (-9,8..+8,0) | %53 | +10: %69, +20: %28 | %6 | bilgi |
| EVET+KISMEN | günlük | 26 (21) | -%1,5 / -%1,7 | -%0,9 | +%0,4 (-4,7..+5,6) | %35 | +5: %54, +10: %27 | %15 | örneklem yetersiz |
| EVET+KISMEN | haftalık | 26 (24) | -%0,7 / +%0,5 | +%10,7 | -%10,4 (-22,4..-0,5) | %50 | +10: %62, +20: %46 | %19 | örneklem yetersiz |

## KARŞILAŞTIRMA

| karşılaştırma | ilk bakış (set 1-4) | ikinci bakış (set 5) | aynı yön mü | birleşik (set 1-5) |
|---|---|---|---|---|
| EVET - HAYIR eşli, günlük | +5,7 puan (p 0,29) | -1,6 puan (p 0,86; n 5 / 4) | HAYIR | +2,7 puan (p 0,51) |
| EVET - HAYIR eşli, haftalık | -15,7 puan (p 0,084) | +1,1 puan (HAYIR n 1: p yok) | HAYIR (HAYIR n 1, anlamsız) | -14,9 puan (p 0,075) |
| EVET - eş, günlük | +%3,6 (p 0,60) | -%3,3 (p 0,62) | HAYIR | +%0,7 (p 0,88) |
| EVET - eş, haftalık | -%16,2 (p 0,018) | -%15,1 (p 0,75) | EVET | -%15,9 (p 0,024) |
| EVET - eş, iki dilim | -%9,3 (p 0,10) | -%9,2 (p 0,47) | EVET | -%9,3 (p 0,063) |
| (EVET + KISMEN) - HAYIR eşli, haftalık | -12,6 puan (p 0,14) | +11,2 puan (HAYIR n 1) | - | -9,4 puan (p 0,20) |

- EVET - eş p değerleri işaret çevirme permütasyonundan (ön kayıtta eklenen ölçü); EVET - HAYIR p değerleri MUM_IZI11 ile aynı iki örneklem permütasyonu.
- Duyarlılık (tekrar bölgeleri son işaretle, birleşik): EVET - HAYIR haftalık eşli -15,4 puan (p 0,058), günlük +2,7 (p 0,51).
- KISMEN haftalık (6 bölge) ilk iki bakışta da artıda (+%12,2; eşlerinden +%6,1): bilgi; n 6.

## KONTROL LİSTESİ

- K1 EVET: eş aynı gün aynı kova aynı takvim aralığı (117 / 128); HAYIR sınıfı aynı seçim hattından kontrol.
- K2 EVET: Cemal sonrasını görmeden işaretledi; ön kayıt (d95aa1b) set 5 getirilerinden önce; giriş sonraki barın açılışı; KASA kapısı açık.
- K3 EVET. K4 EVET: 128 bölge tekil (setler arası aynı bölge yok).
- K5 EVET. K6 EVET. K7 EVET (yaşayan evren; bilgi).
- K8 EVET: set 5'in bütün hücreleri ve birleşikte EVET / KISMEN hücreleri n < 30.
- K9 EVET: g2_kapi geçti; tanımlar MUM_IZI11 ile aynı (ESIK11_SHA ön kayıtta).
- K10 EVET: set 5 bölge başı anahtarla (ilk bar tarihi) denetlendi.
- K11 EVET: set 1-4 değerleri MUM_IZI11 ile birebir (104 satır, 0 fark); iki hücre csv'den yeniden üretildi.
- K12 EVET. K13 EVET: MUM_IZI_GOZ.py ve MUM_IZI11 çıktıları değişmedi. K14 UYGULANMAZ.

## HATA

- Yok (hesapta). Sunum: PDF kapağının son satırı ilk üretimde sağdan taştı; satır ikiye bölündü, PDF yeniden üretildi (SAPMA 1).

## SAPMA

1. Hesaptan sonra MUM_IZI_GOZ2.py'de yalnız PDF kapağındaki bir metnin satır kırılımı değişti (KOD13_SHA ön kayıttakinden farklı); hesap ön kayıtlı kodla koştu; ilk PDF silindi.
2. EVET - HAYIR haftalık karşılaştırması ikinci bakışta yapılamadı (HAYIR n 1; permütasyon en az 2'şer olay ister): ön kayıtta öngörülmüştü.

## ÖNERİLEN DEFTER SATIRLARI (ana model işler)

- IK_KAYIT Ç239: MUM_IZI EK 13 göz ölçümü ikinci bakış (bilgi). Set 5 (hakem v3 seçimi, Cemal EVET 11 / KISMEN 8 / HAYIR 5): ilk bakışın günlük yönü tekrarlamadı (EVET - eş +%3,6 -> -%3,3); haftalıkta EVET yine eşlerinin gerisinde (-%16,2 -> -%15,1; n 5). Birleşik 128: haftalık EVET eşlerinden -%15,9 (%95 -31,2..-3,8; p 0,024), EVET - HAYIR -14,9 puan (p 0,075); günlük EVET - eş +%0,7 (p 0,88). 'Benziyor' bölgelerinin sonrası eşlerinden iyi değil, haftalıkta geride (n < 30). Commit 8ae5ecf / d95aa1b / (sonuç).
- IK_GOREV: 26 Kas, EK 13 + MUM_IZI13_SONRASI.pdf (yeni 11 BENZİYOR + 8 KISMEN bölge).
- IK_ILERI: haftalık EVET'in eşlerinin gerisinde kalması iki bakışta aynı yönde: yeni etiketlerle (n >= 30) aynı komutla yeniden; ters yönde bir iddia (BENZİYOR = kaçın) ölçülmeden yazılmaz.
