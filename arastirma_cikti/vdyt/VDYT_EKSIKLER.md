# VDYT eksik veri raporu

Üretim: 2026-11-12 06:14:02 UTC. İkame / uydurma yapılmadı. Engellenen analizler Faz 2 raporunda 'EKSİK' olarak kalır.

| eksik veri | pazar | engellediği analiz | VDYT'deki karşılık |
|---|---|---|---|
| BIST açılış / yüksek / düşük, 2015-06 öncesi ve kotasyondan çıkanlar | BIST | T1 (ATR), T5, TR genişlemesi, mum / fitil / gövde ölçüleri, savunma hattı (gövde, fitil) 2008-2015 ve batanlarda yapılamaz; BIST OHLC analizleri yalnız yaşayanlarla | K62 kapanışıyla T2-T4 + RV genişlemesi (yanlılık kontrolü) |
| ABD kotasyondan çıkan / batan şirket fiyatları | ABD | hayatta kalma yanlılığı düzeltilemez; sıkışmadan sonra batanlar eksik (aşağı yönlü genişlemeler eksik sayılır) | beyan; sonuç 'yaşayan evren' koşullu |
| KAP özel durum açıklamaları (sözleşme, ihale, ortaklık, sermaye artırımı KARARI, genel kurul, temettü KARARI, yönetim, dava, ürün) | BIST | B kategorisinin çoğu, olay türüne göre ayrım, BIST 'habersiz kırılım' kontrol grubunun temizliği (habersiz = 'kayıtlı veri setlerinde olay yok') | yok; KAP API'den indirilebilir (ana oturum kararı, Faz 2 öncesi) |
| BIST genel kurul ve temettü duyuru günleri | BIST | planlı olayın önceden bilinme günü; yalnız hak kullanım günü (K62) var | hak kullanım günü (bilgi = o gün) |
| ABD 8-K madde kodları | ABD | 8-K içeriği (sözleşme / yönetim / satın alma) ayrılamaz; bilanço 8-K'sı yalnız tarih yakınlığıyla (+-3 iş günü) çıkarılır | 8-K tek tür |
| ABD bilanço açıklama günü 2010 → 2022-11 | ABD | gerçek açıklama günü yerine 10-Q / 10-K başvuru günü (çoğu kez açıklamadan sonra) → olay penceresinde kayma | VEKİL olarak işaretli; 2022-12+ Nasdaq ile ayrı rapor |
| Nasdaq bilanço saati | ABD | %99 'time-not-supplied' → olay günü 0 / +1 ayrımı belirsiz | g0 = takvim günü; [0] ve [1,5] pencereleri ayrı raporlanır |
| ABD CPI / istihdam yayın günleri (BLS) | ABD | makro C kategorisinde enflasyon / istihdam günleri | yok (bls.gov 403); FOMC var |
| TÜİK enflasyon yayın günleri | BIST | makro C kategorisinde enflasyon günü | yok; PPK var |
| Makro içerik / beklenti / sürpriz | ikisi | 'sürpriz' etkisi ayrılamaz; yalnız 'planlı makro gün' etkisi | beyan |
| Sektör haberleri | ikisi | C kategorisinde sektör haberi | VERİ YOK; yalnız rakip bilançosu (sektörün çeyrekteki ilk bilanço günü) |
| Endeks giriş / çıkış günleri | ikisi | endeks gelişmesi olayı | yok |
| Emtia / kur / faiz serileri 2010-2014 | ABD | 2015 öncesi emtia şoku olayı | 2015+ ile sınırlı |
| İçeriden işlem 2022-07 öncesi (BIST); Form 4 yönü (ABD) | ikisi | B içeriden olayı yalnız BIST 2022-07+; ABD'de yok | BIST 2022-07+ |
| Fon raporları 2023 öncesi | BIST | fon girişi olayı yalnız 2023+ | 2023+ |
| Gün içi (saatlik) hisse verisi | ikisi | kırılımın gün içi sırası, KAP saatine göre tepki | yok |
| Kod değişikliği / eski kod eşlemesi (EDGAR CIK → bugünkü kod) | ABD | kodu değişmiş şirketlerin eski başvuruları eşlenmez (eksik olay) | beyan |

Makro takvim durumu: {"FOMC": 154, "FOMC_planli": 151, "PPK": 126, "ilk_FOMC": "2009-01-28", "ilk_PPK": "2015-01-20", "EKSIK": {"CPI_BLS": "bls.gov 403 (erişim engeli)", "ISTIHDAM_BLS": "bls.gov 403", "TUIK_ENFLASYON": "data.tuik.gov.tr yayın takvimi alınmadı", "sayfa": ["PPK2009", "PPK2010", "PPK2011", "PPK2012", "PPK2013", "PPK2014"]}}
