# KARAR KAYDI — K57 (araştırma denetimi ve yeni iz keşif planı)

Sürüm kimliği: K57-DENETIM-v1.0 (1 Kasım 2026 başladı). Klasör: arastirma_cikti/k57_denetim/ (Drive: COLAB_VERILER/OUTPUT/K57_DENETIM). Kaynak dosyaların sha256 kaydı: KAYNAK_MANIFEST.csv (392 dosya, depo commit 56cdbcd).

| No | Tarih | Karar | Gerekçe / kaynak |
|---|---|---|---|
| K57-K01 | 2026-11-01 | K51-K56 sonuçları, kodları, ön kayıtları ve çıktıları DEĞİŞTİRİLMEZ. Denetim yalnız okur; her dosya sha256 ile kaydedildi; test_k57.py değişmezliği denetler. | Cemal'in ana görevi, madde 2 ve 7 |
| K57-K02 | 2026-11-01 | Test sınıfları A (geçerli ve yeterli), B (geçerli fakat sınırlı), C (yöntemsel olarak sorunlu), D (veri yetersizliği). E (hiç test edilmemiş) soru / hipotez düzeyindedir; test satırı değildir. | Cemal'in sınıf listesi; E'nin tanımı gereği test satırı olamaz |
| K57-K03 | 2026-11-01 | Test = (hipotez ya da denetim sorusu, ölçüm, karar kuralı) üçlüsü. Aynı ölçümün yıl / varyant tekrarları tek satırda toplanır (örn. K55'in 1.318 varyant satırı dal düzeyinde 16 test satırı). | Denetlenebilir boyut; hücre kimlikleri satırın notunda |
| K57-K04 | 2026-11-01 | Her test satırı iki bağımsız doğrulayıcıdan (V1 kaynak doğruluğu, V2 sınıf / mantık / eksiklik) geçti; sınıf itirazlarında üçüncü okuyucu (hakem) karar verdi; V2'nin bulduğu eksik testler ayrı bir ajanla eklendi ve onlar da ayrıca V1'den geçti. Ön kayıt / kod hash'leri ajan değil KAYNAK_MANIFEST.csv'den bağlanır. | Aynı ajanın kendi işini doğrulamaması; hash uydurma riskini kapatma |
| K57-K05 | 2026-11-01 | Düzeltmeler üzerine yazılmaz: duzeltme_kaydi sütunu eski ve yeni değeri tutar; ham ajan çıktıları ham/ klasöründe olduğu gibi saklanır. | "Test başarısızlıklarını silme veya gizleme" |
| K57-K06 | 2026-11-01 | Yeni araştırma kartı hazırlanır ama HİÇBİR yeni test başlatılmaz; toplu veri indirme başlatılmaz. İlk teslimattan sonra araştırma sahibinin (Cemal) değerlendirmesi beklenir. | Cemal'in ana görevi, madde 5 ve 8 |
| K57-K07 | 2026-11-02 | K56-EVREN2 Tiingo indirmesi (356 fiyat dosyası; Cemal'in 31 Ekim kararı madde 6 ile 1 Kasım'da başlamıştı) bu görev başlamadan önce başladığı için SÜRDÜRÜLÜR; bu görevin yeni indirmesi değildir. Cemal isterse durdurulur. | Önceki kararın devamı; yeni karar araştırma sahibinindir |
| K57-K08 | 2026-11-02 | Çıktılar repoda ve Drive OUTPUT altında tutulur; sohbette dosya gönderme (yapıtlar kartı) yapılmaz. Çıktı yolları K57 klasörüyle sınırlıdır (K57_envanter_birlestir.cikti_yolu). | Cemal 1 Kasım: 'yapıtlar' kartı rahatsız ediyor; ana görev madde 7 |
| K57-K09 | 2026-11-02 | BIST ve diğer pazar verileri (örn. Finmar ekran görüntüsü) K57 kapsamı dışıdır; ABD önceliklidir. Üyelik açma, e-posta doğrulama ve anahtar edinme Cemal'dedir; anahtarlar yalnız .env'de tutulur. | CLAUDE.md (BIST karar hücresi değil; anahtar koda yazılmaz) |
