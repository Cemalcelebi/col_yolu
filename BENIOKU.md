# kapfon-veri — KAP fon portföy raporları veri paketi (FON_IZI v1.5)

Bu dal yalnız veri taşır; kod `main` dalındadır (FON_IZI.py). `main`'e birleştirilmez.

İçerik (`kapfon/`, her dosyanın boyu ve sha256'sı `manifest.json`'da):
- `liste.csv.gz` — KAP 'Portföy Dağılım Raporu' listesi (Ara 2022 → 23 Eki 2026, 45.740 rapor)
- `ekler.csv.gz` — indirilen raporlar ve durumu (ok / muaf / hata), metin yolları `txt/...`
- `k9_pozisyon.csv.gz`, `k9_islem.csv.gz`, `k9_kontrol.csv.gz` — ayrıştırılmış tablolar (ayrıştırıcı v1.5)
- `metin.tar.xz.000-003` — 25.007 ham rapor metni (2,3 GB açılınca)

Açma (sha256 doğrulamalı): `FI_KAPFON=<klasör> python FON_IZI.py k9ac kapfon`
Güncelleme (yalnız yeni raporlar): `FI_KAPFON=<klasör> python FON_IZI.py k9indir` sonra `... python FON_IZI.py k10`
Yeniden paketleme: `FI_KAPFON=<klasör> python FON_IZI.py k9paket kapfon` ve bu dala commit.
