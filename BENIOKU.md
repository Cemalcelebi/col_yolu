# islenmis-veri — Çöl Yolu işlenmiş veri paketi (main'e birleştirilmez)

Cemal'in izniyle (26 Ekim 2026), KAP paketi (kapfon-veri) gibi ayrı dal. Yeni oturum veriyi yeniden kurmasın diye.

İçerik (veri/, xz + 45 MB parçalar, manifest.json içinde boy ve sha256):
- V_BIST.pkl: BIST günlük fiyat sözlüğü (fi_k1_veri çıktısı, bölünme/marj düzeltmeli), 2016-09 → 2026-10
- V_ABD.pkl: ABD günlük fiyat sözlüğü (1.411 hisse), 2015-06 → 2026-10-22
- G.pkl, oran.pkl, dol.pkl: K25 fon payı tabloları (KAP raporlu fon pozisyonları, bölünme oranı, dolaşım)

Açma (repo kökünde, main dalındaki FON_IZI.py ile):
    git fetch origin islenmis-veri && git worktree add /tmp/iv origin/islenmis-veri
    python FON_IZI.py vpac /tmp/iv/veri /tmp/veri

Sonra sürücülere V_hazir olarak verilir, ör. fon_izi_k26(A, {"BIST": pickle.load(open("/tmp/veri/V_BIST.pkl","rb")), "ABD": ...}).
Her parça sha256 ile doğrulanır; bozuk ya da eksik parçada açma durur.
