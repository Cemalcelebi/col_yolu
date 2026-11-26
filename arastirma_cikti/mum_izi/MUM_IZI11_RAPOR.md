# MUM_IZI11 RAPOR (2026-11-26): GÖZ ÖLÇÜMÜ — Cemal'in etiketli bölgelerinin 15 mumluk sonrası (BİLGİ)

İş tanımı: MUM_IZI11_IS_TANIMI.md (07cf050). Ön kayıt: MUM_IZI11_ON_KAYIT.md (cf5ad8d; getiriden önce iki SAPMA eki 4716783, 33053af). Kod: MUM_IZI_GOZ.py,
test_mum_izi11.py (8 / 8). Tespit = Cemal'in etiketi. Sonuç BİLGİ: n < 30 hücreler 'örneklem yetersiz'; 'iz / tuttu' sözü yok; kasa açılmaz.

## SONUÇ (tek bakışta)

- Cemal'in BENZİYOR dediği 25 bölge sonrasında BENZEMİYOR dediklerinden iyi gitmedi: günlükte R15 ortalaması -%2,3 (HAYIR +%1,8), haftalıkta -%2,6 (HAYIR +%7,0).
- Eşlere göre: günlük EVET eşli fark +%3,6 (%95 -8,6..+14,6; n 7) ile HAYIR -%2,1 arasındaki fark +5,7 puan (p 0,29); haftalık EVET eşli fark -%16,2 (%95 -31,6..-4,2; n 13), HAYIR -%0,5: fark -15,7 puan (p 0,084).
- Hiçbir karşılaştırma p < 0,05 değil; EVET / KISMEN hücrelerinin hepsi n < 30 (örneklem yetersiz). Bu bir sonuç değil, ilk bakış.

## ÖRNEKLEM

| set | EVET (günlük / haftalık) | KISMEN | HAYIR (günlük / haftalık) |
|---|---|---|---|
| set1 MUM_IZI4_ONAY | 7 (5 / 2) | - | 17 (7 / 10) |
| set2 MUM_IZI6_ETIKET (tekrar 8 ve karar dışı 3 hariç) | 9 (3 / 6) | - | 28 (16 / 12) |
| set3 MUM_IZI8_ONAY (karar dışı 5 hariç) | 2 (1 / 1) | - | 17 (8 / 9) |
| set4 MUM_IZI10_ONAY | 7 (2 / 5) | 8 (5 / 3) | 9 (5 / 4) |
| toplam (104) | 25 (11 / 14) | 8 (5 / 3) | 71 (36 / 35) |

- Ölçülemeyen: 0 (ufku kesiği aşan yok; en geç 15. mum 2022-12-30). Eşsiz: 10 (kova yok 4, eş < 5: 6): EVET günlük 4, EVET haftalık 1, KISMEN günlük 1, HAYIR 4.
- Pazar: EVET ABD 13 / AVR 5 / BIST 7; KISMEN ABD 7 / BIST 1; HAYIR ABD 51 / AVR 10 / BIST 10.
- Tekrar sayfalarında yanıtı değişen 2 bölge (duyarlılık aşağıda).

## TABLOLAR (giriş = sonraki mumun açılışı; ufuk 15 mum; dokunma stop'tan önce; stop = bölge dibi x 0,98)

| sınıf | dilim | n (eşli) | R15 ort / medyan | eş ort | eşli fark ort / medyan (%95 ort) | artıda | dokunma | stop | en yüksek / en derin medyan | etiket |
|---|---|---|---|---|---|---|---|---|---|---|
| EVET | günlük | 11 (7) | -%2,3 / -%1,6 | -%3,7 | +%3,6 / +%2,5 (-8,6..+14,6) | %36 | +5: %73, +10: %45 | %9 | +%7,9 / -%9,2 | örneklem yetersiz |
| KISMEN | günlük | 5 (4) | -%5,8 / -%4,6 | -%3,5 | -%2,7 / -%3,4 (-4,5..-0,3) | %0 | +5: %20, +10: %20 | %40 | +%1,0 / -%8,8 | örneklem yetersiz |
| HAYIR | günlük | 36 (34) | +%1,8 / +%0,8 | +%2,9 | -%2,1 / -%1,3 (-5,7..+1,9) | %53 | +5: %61, +10: %31 | %14 | +%6,3 / -%5,6 | bilgi |
| EVET+KISMEN | günlük | 16 (11) | -%3,4 / -%3,2 | -%3,6 | +%1,3 / +%0,9 (-6,6..+8,8) | %25 | +5: %56, +10: %38 | %19 | +%5,5 / -%9,0 | örneklem yetersiz |
| EVET | haftalık | 14 (13) | -%2,6 / -%1,2 | +%12,0 | -%16,2 / -%10,5 (-31,6..-4,2) | %43 | +10: %57, +20: %36 | %7 | +%14,1 / -%13,0 | örneklem yetersiz |
| KISMEN | haftalık | 3 (3) | +%6,1 / +%11,6 | +%5,8 | +%0,2 / +%7,1 (-15,3..+8,9) | %67 | +10: %67, +20: %67 | %67 | +%25,6 / -%37,3 | örneklem yetersiz |
| HAYIR | haftalık | 35 (33) | +%7,0 / +%0,3 | +%6,3 | -%0,5 / -%4,6 (-9,3..+8,8) | %51 | +10: %69, +20: %29 | %6 | +%14,0 / -%11,8 | bilgi |
| EVET+KISMEN | haftalık | 17 (16) | -%1,0 / -%0,9 | +%10,8 | -%13,2 / -%9,5 (-26,5..-3,0) | %47 | +10: %59, +20: %41 | %18 | +%16,4 / -%14,4 | örneklem yetersiz |

- R30 ortalaması (bilgi): EVET günlük +%4,8, haftalık -%2,8; HAYIR günlük +%6,5, haftalık +%21,2.
- BIST ayrı (bilgi): EVET günlük n 5 R15 +%0,6 (eşli -%3,0); HAYIR günlük n 6 +%11,6; EVET haftalık n 2 +%22,0; HAYIR haftalık n 4 +%49,5.

## KARŞILAŞTIRMA (permütasyon iki yönlü, 10.000)

| karşılaştırma | dilim | R15 farkı (p) | eşli fark farkı (p) |
|---|---|---|---|
| EVET - HAYIR | günlük | -4,0 puan (0,43) | +5,7 puan (0,29; n 7 / 34) |
| EVET - HAYIR | haftalık | -9,5 puan (0,32) | -15,7 puan (0,084; n 13 / 33) |
| (EVET + KISMEN) - HAYIR | günlük | -5,1 puan (0,23) | +3,4 puan (0,42) |
| (EVET + KISMEN) - HAYIR | haftalık | -8,0 puan (0,37) | -12,6 puan (0,14) |
| EVET - HAYIR | iki dilim birleşik (eşli) | | -8,0 puan (0,16; n 20 / 67) |
| (EVET + KISMEN) - HAYIR | iki dilim birleşik (eşli) | | -5,9 puan (0,22) |

- Duyarlılık (tekrar bölgeleri son işaretle): EVET - HAYIR haftalık eşli -16,2 puan (p 0,068), günlük +5,7 (0,29), birleşik -8,5 (0,13): yön ve büyüklük aynı.
- Okuma: Cemal'in gözüyle 'benziyor' sınıfı 15 mumda HAYIR'dan ya da eşlerinden daha iyi bir sonrası göstermiyor; haftalıkta yön tersine (eşlerin gerisinde) ama n 13 ve p 0,08. Not (Cemal, 26 Kas, SINANMADI): 'haftalık mumda daha net, kesin sert yükselir' bu örneklemde görülmedi (haftalık EVET R15 medyanı -%1,2; +%20'ye stop'tan önce dokunan %36, HAYIR %29).

## KONTROL LİSTESİ

- K1 EVET: eş aynı gün aynı kova aynı takvim aralığı, aynı stop geometrisi (94 / 104 olayda); HAYIR sınıfı aynı seçim hattından kontrol.
- K2 EVET: Cemal sonrasını görmeden işaretledi; giriş bölgeden sonraki barın açılışı; ön kayıt (cf5ad8d) getirilerden önce; KASA kapısı açık (en geç 2022-12-30).
- K3 EVET: geçerli bar; haftalık tamamlanmış ISO haftaları.
- K4 EVET: 104 bölge tekil (tekrar sayfaları ayrı sayılmadı; aynı bölge iki kez yok denetlendi).
- K5 EVET: giriş = sonraki barın açılışı; giriş <= stop olay çıkmadı.
- K6 EVET: oransal getiri; pazarlar arası para birimi farkı eşli farkla.
- K7 EVET: evren bugün yaşayan hisseler (yanlılık var; bilgi).
- K8 EVET: EVET / KISMEN hücreleri n < 30 'örneklem yetersiz'.
- K9 EVET: ön kayıt + iki SAPMA eki getiriden önce; gz_kapi koşudan önce geçti.
- K10 EVET: etiket şeması; set4 bölge başı anahtarla (ilk bar tarihi) denetlendi.
- K11 EVET: olay ölçüsü elle hesapla aynı (test: günlük, haftalık, stop-önce); iki hücre (EVET haftalık, HAYIR günlük) csv'den yeniden üretildi, birebir.
- K12 EVET: 'iz / tuttu' yok; 'ilk bakış'.
- K13 EVET: eski kodlar, defterler değişmedi; yalnız kendi yollarım commit.
- K14 UYGULANMAZ.

## HATA

1. (kod; benim; getiriden önce yakalandı) K10 denetiminde boş alan DataFrame'de NaN olunca 'dolu' sayıldı; ilk koşu durdu, getiri yazılmadı. Düzeltildi (SAPMA 1).
2. (tanım uyuşmazlığı; benim; getiriden önce yakalandı) MUM_IZI_HAKEM anahtarındaki 'bolge_bas' haftalıkta ilk barın tarihi (haftanın son günü); denetim haftanın ilk günüyle karşılaştırıyordu; ikinci koşu durdu. Denetim düzeltildi (SAPMA 2). Ders: bir anahtar alanının tanımı, onu yazan modülün tanımıyla okunur.

## SAPMA

1. Ön kayıttan sonra, getiriden önce iki kod düzeltmesi (yukarıdaki HATA 1-2); ikisi de ön kayda 'EK SAPMA' olarak yeni KOD11_SHA ile eklendi ve commit edildi (4716783, 33053af). Ölçü tanımları (ESIK11_SHA) değişmedi.
2. Başka sapma yok.

## ÖNERİLEN DEFTER SATIRLARI (ana model işler)

- IK_KAYIT Ç237: MUM_IZI EK 11 göz ölçümü (bilgi). Cemal'in sonrasını görmeden etiketlediği 104 bölge (EVET 25 / KISMEN 8 / HAYIR 71). 15 mum: EVET günlük R15 -%2,3 (eşli +%3,6, n 7), haftalık -%2,6 (eşli -%16,2, %95 -31,6..-4,2, n 13); HAYIR günlük +%1,8, haftalık +%7,0. EVET - HAYIR eşli: günlük +5,7 puan (p 0,29), haftalık -15,7 puan (p 0,084). EVET / KISMEN hücreleri n < 30: örneklem yetersiz. 'Benziyor' bölgelerinin sonrası HAYIR'dan ya da eşlerinden iyi değil (bilgi; ölçülemedi değil, ama n küçük). Commit 66b043e / cf5ad8d / 4716783 / 33053af / (sonuç).
- IK_GOREV: 26 Kas, EK 11 göz ölçümü + MUM_IZI11_SONRASI.pdf (Cemal'e: 25 BENZİYOR + 8 KISMEN bölge, hisse / tarih açık).
- IK_HATA: anahtar alanının tanımı farklı modülde farklı okundu (hakem anahtarı 'bolge_bas' = ilk barın tarihi); getiriden önce yakalandı.
- IK_ILERI: 'haftalık mumda kesin sert yükselir' (Cemal, SINANMADI): bu örneklemde görülmedi (haftalık EVET n 14); yeni etiketler biriktikçe aynı komutla yeniden (n >= 30 hücre).
