# ESKİ 'İZ DEĞİL'LERİN RASTGELE GÜNE GÖRE YENİDEN OKUNMASI — birinci parti (27 Kasım 2026)

Yazan: ana model. Cemal (27 Kas): "bir iz bulununca aynı gün eşleri de çıkar; iz değil dediklerinin çoğu belki de iz"; "devam et". Envanter (ES_OLCUT_ENVANTER.md): olumsuz kararlı 221 kaydın 169'u aynı gün / aynı ay eşlerine göre (E) verildi; 103'ünün satır verisi elde; 78'i kapalı konu.

## 0. Kesin kurallar
- Başlamadan `python IZ_KARNE.py kontrol istanimi`. YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, mevcut bütün modüller, testler, rapor ve satır dosyaları (yalnız okunur). Yeni tek dosya ES_YENIDEN.py (+ test_es_yeniden.py; KURAL_MOTORU düzeni, çakışma kapısı); çıktılar arastirma_cikti/goz_tespit/ES_YENIDEN_*. `git add -A` / `commit -a` yasak.
- KAPALI KONULARA (envanterde işaretli) DOKUNULMAZ. 26 Kasım ve sonrası kayıtlar (zaten rastgele güne göre) alınmaz.
- Bu, AYNI VERİDE YENİDEN OKUMADIR (kör değil): hiçbir sonuç 'iz' diye yazılmaz; en fazla 'ZAMANLAMA ADAYI (yeniden okuma; ileri test gerekir)'. Yeni veri indirilmez; kasa kavramı değişmez (kayıtların kendi verisi kullanılır).
- Ön kayıt (ES_YENIDEN_ON_KAYIT.md: seçilen kayıt listesi, her kaydın dosyası / ufku / hücreleri / olay sayısı ve ayrı ay sayısı (getirisiz), karar kuralı, dolu KONTROL LİSTESİ) hesaptan ÖNCE commit + push; `IZ_KARNE.ik_kontrol_kapisi`; ölçüm bir kez. Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.

## 1. Seçim (getirisiz; ön kayıtta liste)
Envanterin Liste 1'inden: kapalı konu olmayan, tabanı E, satır dosyasında olay tarihi + hisse (+ getiri ya da giriş kuralı) bulunan, olay sayısı >= 300 olan kayıtlar; olay sayısı büyükten küçüğe en çok 20 kayıt. Aynı olay kümesini paylaşan kayıtlar tek satır sayılır (not düşülür). Bir kaydın dosyası okunamıyorsa atlanır ve yazılır.

## 2. Ölçü (her kayıt, kendi ufkuyla H ve kendi giriş kuralıyla; hücreler kaydın kendi pazar x dönem hücreleri)
- R = olayın H ufuklu getirisi (dosyadaki; yoksa aynı kuralla fiyattan). T1 = aynı hissenin aynı dönemdeki BÜTÜN günlerinde aynı giriş kuralıyla H ufuklu getirinin ortalaması. PİYASA(t) = olayın giriş günü, aynı pazarın evrenindeki bütün hisselerin H ufuklu getirisinin eşit ağırlıklı ortalaması. T2 = PİYASA'nın dönemdeki bütün günler üzerinden ortalaması.
- TOPLAM = R - T1. ZAMANLAMA = PİYASA(t) - T2 (o günlerde piyasa sıradan günden iyi mi). SEÇİM = TOPLAM - ZAMANLAMA.
- Her biri için hücre ortalaması ve ay kümeli bootstrap %95 (2.000; tohum 11); olayların düştüğü ayrı ay sayısı; eski hüküm ve eski eşli fark yan sütunda.
- KARAR (önceden): 'ZAMANLAMA ADAYI' <=> kaydın n >= 100 olan hücrelerinin HEPSİNDE (en az 2 hücre) ZAMANLAMA GA alt ucu > 0 VE ayrı ay sayısı her hücrede >= 12. 'TOPLAM ADAYI' aynı kuralla TOPLAM için. Kayıtlar arası yanlış keşif: aday çıkanların birleşik p değerlerine Benjamini-Hochberg q 0,10; geçemeyen 'EMARE'. Olayları birkaç aya yığılan kayıt (ayrı ay < 12) ÖLÇÜLEMEDİ.
- Uyarılar raporda zorunlu: aynı veride yeniden okuma; yaşayan evren; zamanlama farkı olayların belirli piyasa dönemlerine yığılmasından gelebilir (o yüzden ay kümesi ve ay sayısı şartı).

## 3. Çıktılar
ES_YENIDEN.py, test_es_yeniden.py; arastirma_cikti/goz_tespit/: ES_YENIDEN_ON_KAYIT.md, ES_YENIDEN_RAPOR.md (kayıt x hücre tablosu; en üstte aday listesi), es_yeniden_ozet.json. Satır dosyaları /root/.kasa/ham/es_yeniden/.
