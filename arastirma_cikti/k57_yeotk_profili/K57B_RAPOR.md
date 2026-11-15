# K57-B — V1 çevresinde önceden yazılı 3 devam: RAPOR

Ön kayıt: 2026-11-09 18:12:08 UTC (K57B sha abc73b49f1df; K57 mührü 2a6cc6f6d1fd değişmedi); koşu 2026-11-09 18:29:41 UTC → 2026-11-09 18:35:58 UTC. K57-B v1.0 (2026-11-09): V1 çevresinde önceden yazılı 3 devam (B1 geniş ABD evreni, B2 20 gün ufuk, B3 F3'süz)

## KARAR: İZ DEĞİL

Düz dille: YEOTK profiline en yakın çıkan basit kural (bilanço gününe güçlü tepki + satış büyümesi + çeyrek ivmesi + sağlam bilanço, fiyat şartı yok) üç yoldan yeniden sınandı: daha geniş ABD evreni, daha kısa ufuk (20 gün), bilanço şartı olmadan. B1 (geniş ABD evreni): ABD 2023'te 16 olay, eşlerine göre +%11,4; ABD 2024-26'da 58 olay, +%4,8 → İZ DEĞİL. B2 (20 gün ufuk): ABD 2023'te 7 olay, eşlerine göre +%20,0; ABD 2024-26'da 34 olay, +%4,3 → İZ DEĞİL. B3 (F3'süz (F7+F1+F2)): ABD 2023'te 11 olay, eşlerine göre +%8,8; ABD 2024-26'da 46 olay, +%14,9 → İZ DEĞİL. Hiçbirinde iki ABD hücresi birden dört şartı geçmedi; kural Amerika'da eşlerini sistematik olarak geçmiyor. Bilanço gününe sert tepki veren büyüyen şirketlerin bir kısmı çok iyi gidiyor ama ortalamada ve güvenle değil.

## Karar tablosu (iki ABD hücresi karar; BIST bilgi)
| Deneme | Ne değişti | ABD 2023 | ABD 2024-26 | BIST 2024-26 (bilgi) | Karar |
|---|---|---|---|---|---|
| B1 | geniş ABD evreni | n 16, +%11,4 (-%5,0 .. +%28,8), sıra 0,59, portföy %91,0 → tutmaz | n 58, +%4,8 (-%10,2 .. +%18,7), sıra 0,57, portföy %72,5 → tutmaz | — | **İZ DEĞİL** |
| B2 | 20 gün ufuk | n 7, +%20,0 (+%14,4 .. +%24,2), sıra 0,84, portföy %100,0 → tutmaz | n 34, +%4,3 (-%5,3 .. +%13,5), sıra 0,53, portföy %77,5 → tutmaz | n 96, +%2,5 (-%2,0 .. +%7,8), sıra 0,53, portföy %98,5 → tutmaz | **İZ DEĞİL** |
| B3 | F3'süz (F7+F1+F2) | n 11, +%8,8 (-%11,4 .. +%42,9), sıra 0,55, portföy %86,5 → tutmaz | n 46, +%14,9 (-%0,1 .. +%31,5), sıra 0,62, portföy %98,5 → tutmaz | n 99, +%5,4 (-%5,2 .. +%21,2), sıra 0,53, portföy %89,5 → tutmaz | **İZ DEĞİL** |

Neden tutmadı:
- B1: ABD 2023 — n 16 < 30, aralık alt ucu ≤ 0; ABD 2024-26 — aralık alt ucu ≤ 0, portföy ≤ %90.
- B2: ABD 2023 — n 7 < 30; ABD 2024-26 — aralık alt ucu ≤ 0, portföy ≤ %90.
- B3: ABD 2023 — n 11 < 30, aralık alt ucu ≤ 0, portföy ≤ %90; ABD 2024-26 — aralık alt ucu ≤ 0.

## B1 — geniş ABD evreni (V1, 60 gün)
- Evren: SEC frames'te gelir + kâr + özkaynak verisi ve borsa kodu olan 4475 şirket; Yahoo'dan fiyatı alınan 4261
  (Yahoo durumları: fiyat 4261, kısa 117, veri yok 45, yok 33, inmedi 14, tür dışı 5; 'yok' = 404, 'inmedi' = denemelerden sonra inemedi, 'kısa' < 150 gün, 'tür dışı' = EQUITY değil).
  Yahoo: engellemedi (ardışık engel yok); ilk indirme 2026-11-09 18:12:28 UTC (ön kayıttan sonra); b_kos bu koşuda önbellekten 4461
  dosya okudu, inemeyen 14 hisseyi yeniden denedi.
- Olay: 71156 bilanço günü; 20 gün medyan işlem değeri >= 1 milyon $ olan 50161 (3126 hisse;
  1122 tanesi V_ABD'de de var). V1 olayı 150, ölçülen olay 47408.
| Varyant | Hücre | Rol | n | Eşli fark | %95 aralık | Sıra | Portföy yüzdeliği | Tutar |
|---|---|---|---|---|---|---|---|---|
| V1 | ABD 2021-22 | BİLGİ | 64 | +%3,9 | -%1,7 .. +%8,5 | 0,56 | 0,83 | tutmaz |
| V1 | ABD 2023 | KARAR | 16 | +%11,4 | -%5,0 .. +%28,8 | 0,59 | 0,91 | tutmaz |
| V1 | ABD 2024-26 | KARAR | 58 | +%4,8 | -%10,2 .. +%18,7 | 0,57 | 0,72 | tutmaz |

## B2 — 20 gün ufuk (V1; özgün V_ABD / V_BIST, K57 olayları)
| Varyant | Hücre | Rol | n | Eşli fark | %95 aralık | Sıra | Portföy yüzdeliği | Tutar |
|---|---|---|---|---|---|---|---|---|
| V1 | BIST 2022-23 | BİLGİ | 8 | +%3,8 | +%1,2 .. +%22,4 | 0,57 | 0,76 | tutmaz |
| V1 | BIST 2024-26 | BİLGİ | 96 | +%2,5 | -%2,0 .. +%7,8 | 0,53 | 0,98 | tutmaz |
| V1 | ABD 2021-22 | BİLGİ | 29 | +%1,8 | -%1,7 .. +%5,8 | 0,56 | 0,83 | tutmaz |
| V1 | ABD 2023 | KARAR | 7 | +%20,0 | +%14,4 .. +%24,2 | 0,84 | 1,00 | tutmaz |
| V1 | ABD 2024-26 | KARAR | 34 | +%4,3 | -%5,3 .. +%13,5 | 0,53 | 0,78 | tutmaz |

## B3 — F3'süz (F7 + F1 + F2, 60 gün; özgün evrenler)
| Varyant | Hücre | Rol | n | Eşli fark | %95 aralık | Sıra | Portföy yüzdeliği | Tutar |
|---|---|---|---|---|---|---|---|---|
| V1-F3 | BIST 2022-23 | BİLGİ | 8 | +%14,0 | +%5,0 .. +%76,9 | 0,59 | 0,85 | tutmaz |
| V1-F3 | BIST 2024-26 | BİLGİ | 99 | +%5,4 | -%5,2 .. +%21,2 | 0,53 | 0,90 | tutmaz |
| V1-F3 | ABD 2021-22 | BİLGİ | 48 | +%3,8 | -%4,8 .. +%13,6 | 0,55 | 0,45 | tutmaz |
| V1-F3 | ABD 2023 | KARAR | 11 | +%8,8 | -%11,4 .. +%42,9 | 0,55 | 0,86 | tutmaz |
| V1-F3 | ABD 2024-26 | KARAR | 46 | +%14,9 | -%0,1 .. +%31,5 | 0,62 | 0,98 | tutmaz |

## Eşiğe en yakın hücreler (n >= 30, aralık alt ucuna göre)
- B3 ABD 2024-26: n 46, +%14,9 (-%0,1 .. +%31,5), sıra 0,62, portföy yüzdeliği 0,98
- B1 ABD 2021-22: n 64, +%3,9 (-%1,7 .. +%8,5), sıra 0,56, portföy yüzdeliği 0,83
- B2 BIST 2024-26: n 96, +%2,5 (-%2,0 .. +%7,8), sıra 0,53, portföy yüzdeliği 0,98
- B3 ABD 2021-22: n 48, +%3,8 (-%4,8 .. +%13,6), sıra 0,55, portföy yüzdeliği 0,45
- B3 BIST 2024-26: n 99, +%5,4 (-%5,2 .. +%21,2), sıra 0,53, portföy yüzdeliği 0,90

## Akıl sağlığı: B1'in en son 12 V1 olayı (geniş evren)
| Hisse | Açıklama | Tepki (ham) | Satış yıllık | 20g medyan işlem (milyon $) | r60 | Eşli fark |
|---|---|---|---|---|---|---|
| UMAC | 2026-05-14 | +%8,2 | +%296 | 51,4 | +%70,4 | +%61,6 |
| MU | 2026-06-24 | +%15,4 | +%346 | 53009,3 | — | — |
| AEHR | 2026-07-14 | +%29,1 | +%34 | 147,6 | — | — |
| NVEC | 2026-07-22 | +%52,3 | +%81 | 22,8 | — | — |
| AXTI | 2026-07-30 | +%63,5 | +%165 | 427,9 | — | — |
| PBF | 2026-07-30 | +%14,1 | +%56 | 193,6 | — | — |
| FTK | 2026-08-04 | +%34,8 | +%70 | 8,6 | — | — |
| COMP | 2026-08-04 | +%9,2 | +%109 | 123,7 | — | — |
| EGY | 2026-08-06 | +%7,8 | +%40 | 5,8 | — | — |
| WLDN | 2026-08-06 | +%16,3 | +%33 | 15,9 | — | — |
| FF | 2026-08-10 | +%25,1 | +%121 | 1,3 | — | — |
| ETON | 2026-08-13 | +%41,6 | +%99 | 24,6 | — | — |

## Notlar ve sınırlar
- B2 / B3 K57'nin mühürlü olay dosyalarından koşuldu; K57 ANA V1 hücreleri aynı dosyalardan yeniden üretildi: tuttu (BIST 2022-23 n 8, BIST 2024-26 n 96, ABD 2021-22 n 29, ABD 2023 n 7, ABD 2024-26 n 31).
- B1 evreni bugünkü company_tickers.json'dan (SEC): borsadan çıkmış / kodu değişmiş şirketler yok (hayatta kalma yanlılığı V_ABD'ye göre
  küçük ama sıfır değil). Fiyatlar Yahoo düzeltmeli (temettü + bölünme), 31.08.2026'da kesik. Likidite tabanı yalnız olaylara, eşlere uygulanmadı (FI_OLCUT
  paneli değişmeden; ön kayıt).
- Frames değerleri son başvurudaki (düzeltilmiş) değerdir (K57 notu); bilgi tarihi kuralı K57 ile aynı.
- Çoklu deneme: K57 (5 varyant + 3 devam) + K57-B (3); ABD-ADAY çıksa bile aday, canlı izleme olmadan üretime girmez.
- SEC'e yeni istek yapılmadı (frames önbelleği); kişisel e-posta kullanılmadı.

## Sıradaki 3 (ön kayıtta yazılı; bu görevde koşulmadı, karar ana oturumda)
- C1: V1 + F4 (seyrelme yok) geniş ABD evreninde, 60 gün.
- C2: V1 geniş ABD evreninde, likidite tabanı 5 milyon $.
- C3: V1 geniş ABD evreninde, F7 yerine yalnız 'ear' üst %10 (ham şartı aynı).

## IZ_KARNE önerisi (Ç149; IZ_KARNE.py'ye ana oturum işler)
```
_ik_k("Ç149", "2026-11-09", "K57-B: YEOTK profili V1 (güçlü tepki + büyüme + ivme + sağlam bilanço, fiyat şartı yok) çevresinde önceden yazılı 3 devam: B1 geniş ABD evreni (SEC frames + Yahoo fiyat, 20 gün medyan işlem değeri >= 1 milyon $), B2 20 gün ufuk, B3 F3'süz", "K57.py, test_k57.py", "K57 eşiğe en yakın V1 geniş evrende / kısa ufukta / bilanço şartsız tutar mı?", "Devam (ön kayıt K57B_ON_KAYIT.md, sha abc73b49f1df; ölçüt FI_OLCUT; karar ABD 2023 + 2024-26, Avrupa verisi yok)", "", 3, cikti="arastirma_cikti/k57_yeotk_profili/ (K57B_ON_KAYIT.md, K57B_RAPOR.md, hucre_b.csv, olaylar_b1_abd.csv.gz, evren_b1.csv, k57b_kos_meta.json)", notu="İZ DEĞİL. B1 geniş ABD evreni [İZ DEĞİL]: ABD 2021-22: n 64, +%3,9 (-%1,7 .. +%8,5), sıra 0,56, portföy %83,0, tutmaz; ABD 2023: n 16, +%11,4 (-%5,0 .. +%28,8), sıra 0,59, portföy %91,0, tutmaz; ABD 2024-26: n 58, +%4,8 (-%10,2 .. +%18,7), sıra 0,57, portföy %72,5, tutmaz. B2 20 gün ufuk [İZ DEĞİL]: BIST 2022-23: n 8, +%3,8 (+%1,2 .. +%22,4), sıra 0,57, portföy %76,0, tutmaz; BIST 2024-26: n 96, +%2,5 (-%2,0 .. +%7,8), sıra 0,53, portföy %98,5, tutmaz; ABD 2021-22: n 29, +%1,8 (-%1,7 .. +%5,8), sıra 0,56, portföy %83,0, tutmaz; ABD 2023: n 7, +%20,0 (+%14,4 .. +%24,2), sıra 0,84, portföy %100,0, tutmaz; ABD 2024-26: n 34, +%4,3 (-%5,3 .. +%13,5), sıra 0,53, portföy %77,5, tutmaz. B3 F3'süz (F7+F1+F2) [İZ DEĞİL]: BIST 2022-23: n 8, +%14,0 (+%5,0 .. +%76,9), sıra 0,59, portföy %85,0, tutmaz; BIST 2024-26: n 99, +%5,4 (-%5,2 .. +%21,2), sıra 0,53, portföy %89,5, tutmaz; ABD 2021-22: n 48, +%3,8 (-%4,8 .. +%13,6), sıra 0,55, portföy %44,5, tutmaz; ABD 2023: n 11, +%8,8 (-%11,4 .. +%42,9), sıra 0,55, portföy %86,5, tutmaz; ABD 2024-26: n 46, +%14,9 (-%0,1 .. +%31,5), sıra 0,62, portföy %98,5, tutmaz. B1 evreni: 4475 aday, 4261 hisse fiyatlı (Yahoo durumları: fiyat 4261, kısa 117, veri yok 45, yok 33, inmedi 14, tür dışı 5), taban üstü olay 50161 (3126 hisse), V1 150."),
```
