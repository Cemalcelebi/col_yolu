"""test_mum_izi — MUM_IZI testleri (gerçek fiyat verisi yok): sayısallaştırma = elle sayım, ölçüler sentetik mumlarda, şablonun kendine
uzaklığı 0, geleceğe bakma (prefix), düz S = vektörlü S, üretici / gömme geçerliliği, kesik ve kapı denetimi, çakışma kapısı, sızıntı.
Çalıştır: python test_mum_izi.py"""
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

import MUM_IZI as MI

# Cemal'in görüntüsünden ELLE sayım (turuncu dairenin içi, soldan sağa; Y yeşil, K kırmızı; doji gövdesi çizgi):
# 1 Y, 2 K, 3 Y, 4 Y, 5 K doji, 6 Y, 7 K, 8 K doji, 9 Y, 10 K, 11 Y, 12 K, 13 Y, 14 Y, 15 Y, 16 Y, 17 K doji, 18 Y, 19 Y (çok uzun üst fitil),
# 20 Y doji. Dairenin solunda: büyük kırmızı (çizgi altında, kısmen görünür), yeşil, kırmızı doji; çizgi altında gövdesi görünmeyen 1 mum;
# sağ kenarda kesilen 1 yeşil mum.
ELLE_RENK = "YKYYKYKKYKYKYYYYKYYY"
ELLE_DOJI = {5, 8, 17, 20}


def _D():
    if not hasattr(_D, "c"):
        _D.c = MI.mi_sayisallastir()
    return _D.c


def test_sayisallastirma_elle():
    D = _D(); T = D["tablo"]; B = T[T.sinif == "BOLGE"]
    assert D["n_bolge"] == 20 and "".join(B.renk) == ELLE_RENK, ("".join(B.renk), D["n_bolge"])
    assert set(B[B.doji_cizgi.astype(bool)].i.astype(int)) == ELLE_DOJI
    assert list(B.i.astype(int)) == list(range(1, 21))
    say = T.sinif.value_counts().to_dict()
    assert say == {"BOLGE": 20, "BAGLAM": 3, "GIZLI": 1, "KESIK": 1}, say
    assert D["n_tepe"] == 3
    # en uzun üst fitil 19. mumda; dip (en düşük Low) 3. mumda
    assert int(B.loc[(B.H - B[["O", "C"]].max(axis=1)).idxmax(), "i"]) == 19
    assert int(B.loc[B.L.idxmin(), "i"]) == 3
    # ızgara düzenli: mum aralığı 45 px civarı
    assert 44.5 < D["izgara"]["b"] < 45.8


def test_ozellik_basit():
    m = 10; x = np.arange(m, dtype=float)
    O = 100 + x; C = O + 0.5; H = C + 0.2; L = O - 0.3
    BU = C + 5; BO = C - 1; BA = C - 7
    F = MI.mi_ozellik(O, H, L, C, BU, BO, BA)
    assert F["yesil_pay"][0] == 1.0 and F["yuk_dip_pay"][0] == 1.0 and F["yuk_kapanis_pay"][0] == 1.0
    assert abs(F["govde_oran"][0] - 0.5) < 1e-12 and abs(F["ust_fitil"][0] - 0.2) < 1e-12 and abs(F["alt_fitil"][0] - 0.3) < 1e-12
    assert abs(F["kapanis_r2"][0] - 1.0) < 1e-12 and abs(F["kapanis_egim"][0] - 1.0) < 1e-12   # birim boy 1.0
    assert abs(F["pB_bas"][0] - 7 / 12) < 1e-12 and F["sma_ustu_pay"][0] == 1.0 and F["sma_gecis_konum"][0] == 0.0
    for v in F.values():
        assert np.isfinite(v).all()


def test_olcek_bagimsiz():
    rng = np.random.default_rng(3); m = 20
    C = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, m))); O = C * np.exp(rng.normal(0, 0.005, m))
    H = np.maximum(O, C) * 1.004; L = np.minimum(O, C) * 0.996; BU, BO, BA = C * 1.05, C * 0.99, C * 0.94
    F1 = MI.mi_ozellik(O, H, L, C, BU, BO, BA); F2 = MI.mi_ozellik(*(7.3 * v + 0 for v in (O, H, L, C, BU, BO, BA)))
    for k in F1:
        assert abs(F1[k][0] - F2[k][0]) < 1e-9, k


def test_sablon_kendine():
    D = _D(); S = MI.mi_sablon_kur(D, {"tam": {"tau": [1, 1, 1], "sd": {k: 1.0 for k in MI.MI_ESIK["benzerlik"]["ozellik_alt"]}},
                                     "tepesiz": {"tau": [1, 1, 1], "sd": {k: 1.0 for k in MI.MI_ESIK["benzerlik"]["ozellik_alt"]}}})
    for ad, s in S.items():
        a = s["ohlc"]
        v = MI.mi_S_pencere(*(a[c] for c in ("O", "H", "L", "C", "BU", "BO", "BA")), s)
        assert abs(v[0] - 1.0) < 1e-12, (ad, v)
    assert S["tam"]["L"] == 20 and S["tepesiz"]["L"] == 17
    assert S["tam"]["uzunluklar"] == [16, 18, 20, 22, 24] and S["tepesiz"]["uzunluklar"] == [14, 15, 17, 19, 20]


def _sab_kal():
    D = _D()
    k = {"tau": [1.3, 0.46, 1.9], "sd": {kk: 0.2 for kk in MI.MI_ESIK["benzerlik"]["ozellik_alt"]}}
    S = MI.mi_sablon_kur(D, {"tam": k, "tepesiz": k})
    for s in S.values():
        s["esik"] = 0.5
    return S


def _seri(n=400, tohum=7):
    rng = np.random.default_rng(tohum)
    lO, lH, lL, lC = MI.mi_uret(rng, n, None, "ry")
    return np.exp(lO), np.exp(lH), np.exp(lL), np.exp(lC)


def test_prefix_ve_duz():
    S = _sab_kal(); O, H, L, C = _seri()
    for ad, s in S.items():
        best, bm = MI.mi_tara_seri(O, H, L, C, s)
        for t in (60, 150, 299, 399):
            b2, _ = MI.mi_tara_seri(O[:t + 1], H[:t + 1], L[:t + 1], C[:t + 1], s)
            assert abs(b2[-1] - best[t]) < 1e-12, (ad, t)          # gelecek barlar S(t)'yi değiştirmez
            assert abs(MI.mi_duz_S(O, H, L, C, t, int(bm[t]), s) - best[t]) < 1e-9, (ad, t)
        assert np.isnan(best[:MI.MI_ESIK["benzerlik"]["bant"]["n"] - 1 + min(s["uzunluklar"]) - 1]).all()


def test_uretec_gecerli():
    rng = np.random.default_rng(11)
    havuz = {"desc": [np.column_stack([rng.normal(0, 0.003, 500), rng.normal(0, 0.02, 500), np.abs(rng.normal(0, 0.01, 500)),
                                       np.abs(rng.normal(0, 0.01, 500))])], "sembol": ["X"]}
    for tip in ("blok", "ry"):
        lO, lH, lL, lC = MI.mi_uret(rng, 300, havuz, tip)
        O, H, L, C = map(np.exp, (lO, lH, lL, lC))
        assert (H >= np.maximum(O, C) - 1e-12).all() and (L <= np.minimum(O, C) + 1e-12).all() and (L > 0).all()


def test_gom_birebir():
    S = _sab_kal(); s = S["tam"]; rng = np.random.default_rng(5)
    lO, lH, lL, lC = MI.mi_uret(rng, 300, None, "ry"); p = 200
    MI.mi_baglam_uygula(lO, lH, lL, lC, p, "dip")
    Le = MI.mi_gom(rng, lO, lH, lL, lC, p, s, 0.0, 1.0, 1.0)
    assert Le == 20
    O, H, L, C = map(np.exp, (lO[p:p + Le], lH[p:p + Le], lL[p:p + Le], lC[p:p + Le]))
    Z, _ = MI.mi_dizi(O, H, L, C, C, C, 20)
    # gürültüsüz, esnemesiz, ölçek 1 gömme: normalleştirilmiş mum dizisi şablonla birebir (doğrusal fiyat uzayında gömme)
    assert np.abs(Z[0] - s["Z"]).max() < 1e-9
    # gömme sonrası seri sürekli: p+Le açılışı ile önceki kapanış arasında üretici boşluğu kadar fark
    assert abs(lO[p + Le] - lC[p + Le - 1]) < 0.2
    # bağlam: dip -> [p-40, p-1] net düşüş ~ %20
    rng = np.random.default_rng(6); a, b, c, d = MI.mi_uret(rng, 300, None, "ry"); MI.mi_baglam_uygula(a, b, c, d, 200, "dip")
    assert abs((d[199] - d[159]) - (-0.005 * 40)) < 1e-9


def test_tekil():
    e = np.array([3, 5, 10, 17, 18, 40, 54, 55])
    assert list(MI._mi_tekil(e, 15)) == [3, 18, 40, 55]


def test_konum():
    C = np.r_[np.linspace(100, 200, 130), np.linspace(200, 100, 130)]
    k = MI.mi_konum_seri(C, np.array([50, 129, 140, 259]))
    assert list(k) == ["KISA", "TEPE", "ORTA", "DIP"]


def test_kesik():
    i1 = pd.date_range("2022-12-28", "2023-01-03")
    V = {"A": pd.DataFrame({"Open": 1.0, "High": 2.0, "Low": 0.5, "Close": 1.5, "Volume": 1.0}, index=i1),
         "B": pd.DataFrame({"Open": 1.0, "High": 2.0, "Low": 0.5, "Close": 1.5, "Volume": 1.0}, index=pd.date_range("2023-01-02", "2023-01-05"))}
    W, say = MI.mi_kes_fiyat(V, "2015-01-01")
    assert list(W) == ["A"] and W["A"].index.max() <= MI.MI_KESIK and say["bos"] == 1


def test_kapi_kapali():
    with tempfile.TemporaryDirectory() as d:
        try:
            MI.mi_kapi(d)
        except MI.MIHata:
            pass
        else:
            raise AssertionError("ön kayıtsız kapı açıldı")


def test_sizinti():
    try:
        MI.mi_sizinti("iletişim: ornek@ornek.com", "deneme")
    except MI.MIHata:
        pass
    else:
        raise AssertionError("e-posta yakalanmadı")
    MI.mi_sizinti("S 0,64 eşik; giriş t+1 açılış", "deneme")


def test_cakisma_kapisi():
    kod = ("import MUM_IZI as M\nns = dict(vars(M))\nns['mi_bant'] = 1\nns['_CK_ONCE_MI'] = {'mi_bant': id(M.mi_bant)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_mi()')[0] + '_cakisma_kontrol_mi()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(MI.__file__)))
    assert "KAPALI" in r.stdout, (r.stdout, r.stderr[-500:])


def test_esik_sha_sabit():
    assert MI.mi_esik_sha() == MI.mi_esik_sha(dict(MI.MI_ESIK))
    assert len(MI.MI_OZELLIK) + len(MI.MI_BAGLAM_OZ) <= 40


if __name__ == "__main__":
    adlar = [k for k in list(globals()) if k.startswith("test_")]
    hata = 0
    for k in adlar:
        try:
            globals()[k](); print("GEÇTİ", k)
        except Exception as ex:   # her test ayrı raporlanır
            hata += 1; print("KALDI", k, type(ex).__name__, ex)
    print(f"{len(adlar) - hata} / {len(adlar)} geçti")
    sys.exit(1 if hata else 0)
