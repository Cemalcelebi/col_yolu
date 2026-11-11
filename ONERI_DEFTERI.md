# ÖNERİ DEFTERİ — gerçek para karnesi

Yalnız ana model yazar (CLAUDE.md 'Defter yetkisi'). Her satır: gerçek bir pozisyon ya da verilmiş bir öneri. Kapılar: TARAMA (ölçülmüş sinyal), DOSYA (birincil kaynak denetimi), RİSK (yazılı giriş / boyut / çıkış). Fiyatlar Cemal'in ekran görüntülerinden ya da Yahoo kapanışından; kaynak yazılır.

## Açık pozisyonlar (11 Kasım 2026 itibarıyla bilinenler)

| İsim | Alım | Adet / maliyet | Kapılar | Çıkış kuralları (yazılı) | Son durum | Kaynak |
|---|---|---|---|---|---|---|
| DGXX | 6 Kas 2026 öncesi; Cemal'in kararı, Claude'un sıralamasında izleme 1. | 175 adet, ort. 2,01 $ (ekran 6 ve 9 Kas) | TARAMA: yok (ölçülmüş sinyal yok). DOSYA: var (ABD 10x raporu: Cerebras sözleşmesi SEC ekli, borçsuz; finansman ve teslim kanıtsız). RİSK: var. | 2x kuralı: 4,02 $'da 88 adet sat (anapara). Bilanço günü (13 Kas) +%25 ve üstü: 1/3 sat. Kötü bilanço (nakit < kalan yatırım ya da teslim kayması): beklemeden sat. Teslim 15 Ara. Ekleme: 104 adet limit 2,12 $ (12 Kas'a kadar; dolduysa yeni ort. ≈2,05, 2x ≈4,10). | 10 Kas: 2,16 $ (maliyete göre +%7,5; rapor referansı 2,27 $'dan -%4,8; aynı sürede emsal sepeti -%10,5, IWM +%0,3) | Midas ekranı, Yahoo |
| QMLS | Tem-Kas 2026, 7 alış; Cemal'in kararı (Claude önermedi) | Kalan 83 adet, ort. 4,58 $; QMLS'e net giren 913 $ | TARAMA: yok. DOSYA: olumsuz (going-concern, ATW tahvili, PR-yalnız sözleşmeler). RİSK: çıkış planı var. | Bilanço (16-23 Kas) iyi ve sıçrama: o gün sat. Gecikme (NT 10-Q) ya da ağırlaşan going-concern: ertesi sabah sat. Hiçbiri: en geç 8 Oca 2027 (kilit 19 Oca). Ekleme yok. | 9 Kas: 3,22-3,32 $; toplam gerçekleşmiş + açık ≈ -640 $ | Midas ekranı, işlem geçmişi |
| YEOTK | 6 Kas 2026 (tavan günü), Cemal'in kararı; Claude'un BIST sıralamasında izleme 1. | Adet ve maliyet bildirilmedi | TARAMA: yok (K57: profil İZ DEĞİL). DOSYA: var (BIST raporu; 3Ç26 güçlü; borç yüksek, dolaşım belirsiz). RİSK: eksik (boyut tavanı ve çıkış olayı yazılmadı). | Ekleme yalnız olayla: Reap'in isimli ihracat sözleşmesi ya da 4Ç'de kârın tekrarı. Çıkış olayı ve boyut tavanı Cemal'le yazılacak. | 10 Kas: 28,00 TL (rapor referansı 24,32 TL'den +%15,1; XU100 +%1,6; 6 Kas kapanışı 25,64'e göre +%9,2) | Yahoo, KAP aktarımı |

Hesap (Midas, 7 Kas 2026): toplam 62.577 TL, yatırılan ≈99.400 TL, toplam -36.833 TL (-%53); nakit 445 $.

## Verilmiş öneriler (üç kapıdan geçen)
Henüz yok. K59 (basit sinyaller + bileşik) ölçülüyor; sonuç gelmeden 'TARAMA' kapısı açık değil.

## İzleme listesi (öneri değil)
BIST: PNLSN, FORTE, GWIND, EUPWR (3Ç26 taraması ve BIST raporu). ABD: CENX, AEHR, DUOT, AIB.

## Karne (ayda bir yenilenir; kod arastirma_cikti/oneri_karne/karne.py)

| Tarih | Pencere | Sonuç | Okuma |
|---|---|---|---|
| 11 Kas 2026 | Raporlardan beri 3-5 işlem günü; 76 ad (alınmayanlar dahil) | ABD: izleme 1-3 ortalama -%12,1, elenenler -%11,1, emsal sepeti -%10,5. BIST: izleme 1-3 +%5,3, izleme listesi +%2,9, elenenler +%8,9 (en çok çıkanlar lekeli adlar: ANELE, MANAS, IEYHO), XU100 +%1,6 | Erken karne, kanıt değil. Sıralama elenenleri geçmedi (fark şanstan ayrılmıyor). YEOTK ve DGXX'in artısı büyük ölçüde bilanço günü ve sektör tepkisi. Ayda 2 seçimle, aylık 10 puanlık gerçek bir üstünlüğü görmek için 16-25 ay gerekir. |

## Kapanan pozisyonlar
| İsim | Dönem | Sonuç | Ders |
|---|---|---|---|
| QMLS (yarısı) | Tem - 6 Kas 2026 | ≈83 adet ≈3,10 $'dan satıldı; QMLS toplam zararı ≈ -650 $ (≈33 bin TL) | Düşen hisseye üç ayda yedi alım; boyut ve olaysız ekleme |
