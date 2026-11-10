# K57 / K57-B / K57-C ve canlı taramalar: ana model denetimi (10 Kasım 2026)

Yöntem: CLAUDE.md "Çalışma düzeni" (10 Kas): alt ajanların teslim ettiği işler bağımsız sınandı. Kod yeniden yazılmadı; yalnız kontrol komutları.

| # | Sınanan | Nasıl | Sonuç |
|---|---|---|---|
| 1 | Ön kayıt ölçümden önce mi | Git commit zamanı + ön kayıt zamanı + koşu başlangıcı (k57*_kos_meta.json) | K57: ön kayıt 15:29, commit 15:32, koşu sonra: TUTTU. K57-B: 18:12, commit 18:22, koşu 18:29: TUTTU. K57-C: ön kayıt 18:44, koşu 18:45, commit 18:51 (sonuçla birlikte): ZAYIF. C1-C3 tanımları K57B_ON_KAYIT'ta 18:22'de commit'liydi; ama K57-C'de doldurulan 7 'BOŞLUK' (kapanış ölçütü dahil) git ile ölçümden önce kanıtlanamıyor, yalnız iç mühür var. |
| 2 | Geleceğe bakma | Olay dosyalarında her bilgi tarihi (bilgi_son, pay_filed, fon_bil) <= tepki günü; giriş > tepki günü | ABD 27.415 + 27.052, BIST 8.522 + 7.181 kayıt: 0 ihlal. Giriş sırası: 0 ihlal. TUTTU. |
| 3 | Fon krizi kesiği | r60 olan en geç giriş | ABD 5 Haz 2026, BIST 4 Haz 2026. TUTTU. |
| 4 | Hücreler dosyadan yeniden üretiliyor mu | olaylar_*.csv'den V0 ve V1 ortalama eşli fark ve n bağımsız hesaplandı | 10 hücrenin 10'u birebir aynı (ör. ABD V1 2024-26 n 31, +%10,27). TUTTU. |
| 5 | Tek olay getirisi | 5 rastgele ABD olayında r60 ham fiyattan yeniden hesaplandı | 5/5 aynı; tanım FON_IZI ile aynı (girişten itibaren 60. işlem günü kapanışı, c[e+59]). TUTTU. |
| 6 | F4 (seyrelme yok) bölünme kuralı | C1'in 85 olayında yıllık pay artışı > %10 olup kuraldan geçen | 4 olay (CRC, IMMR: birim hatası ~1000 kat, doğru elenmiş sayılır; SLDP 26 kat, TONX 76 kat: bölünme mi ihraç mı belirsiz). Etki küçük (85'te 2-4); C1 kararını değiştirmez. NOT. |
| 7 | YEOTK 3Ç kârı (Cemal'e 6 Kas'ta verilen) | temel_duz + BIST tarama notu | 6 Kas mesajında 3Ç ana ortaklık kârı ≈864 mn TL yazıldı (9A 1.534 - 6A 670). Enflasyona göre Eylül 2026 parasıyla yeniden düzenlenmiş 6A 707 mn TL olduğundan doğru 3Ç ≈827 mn TL. Sonuç ('3Ç kârı ilk yarıdan büyük') değişmiyor. DÜZELTME. |
| 8 | PNLSN rakamları | temel_duz 2026/3 + 2026/6 net kâr | 6A = -43,9 + 62,0 = 18,1 mn TL; notta 19 (yeniden düzenlenmiş). 3Ç 127 mn TL. TUTTU. |
| 9 | CENX rakamları | canli_abd_q3_tablo.csv satırı | Gelir 961,2 / 632,2 mn $ (+%52), kâr 302,6 / 249,3 mn $: TUTTU. Ama son 24 ayda S-3/S-1 kaydı var (fin_kayit_S3S1_24ay = 1); notta 'finansman izi yok' denmişti. Raf kaydı ihraç değil, yine de 'izi yok' ifadesi fazla kesin. DÜZELTME. |
| 10 | E-posta / anahtar sızıntısı | git grep | Repoda 0 dosya. TUTTU. |
| 11 | Testler | test_k57.py, test_iz_karne.py | 10/10 ve 7/7 geçti. TUTTU. |

Karar: K57, K57-B, K57-C sonuçları (İZ DEĞİL) denetimden geçti. İki küçük rakam düzeltmesi (YEOTK 3Ç, CENX finansman ifadesi) ve bir süreç zayıflığı (K57-C ön kaydının ölçümden önce commit edilmemesi) var; hiçbiri kararı değiştirmiyor.

Bundan sonra iş tanımına eklenecek: her ön kayıt dosyası ölçüm başlamadan ayrı commit ile dala gönderilir; alt ajan bunu yapamıyorsa ana model ön kayıt gelince commit eder, ölçüm komutunu ondan sonra verir.
