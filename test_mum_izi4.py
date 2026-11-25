"""test_mum_izi4 — MUM_IZI_V2 testleri (gerçek fiyat verisi yok): EK ölçüler, karşı örneklerin kapanış yolu, v1 S'nin MUM_IZI ile birebir
olması (kapısız), haftalık eksik hafta kuralı, şablonun kendi kapılarından geçmesi (eşik tablosu varsa), kapı mantığı, çakışma kapısı.
Çalıştır: python test_mum_izi4.py"""
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

import MUM_IZI as MI
import MUM_IZI_V2 as MV


def test_ek_olcu():
    O = np.array([1.0, 2.0]); C = np.array([2.0, 1.5]); H = np.array([2.5, 2.2]); L = np.array([0.5, 1.4]); BU = np.array([4.0, 4.0]); BA = np.array([0.0, 2.0])
    E = MV.mv_ek_olcu(O, H, L, C, BU, BA)
    assert abs(E["mum_bant"][0] - (2.0 / 4 + 0.8 / 2) / 2) < 1e-12 and abs(E["max_mum_bant"][0] - 0.5) < 1e-12
    assert abs(E["govde_bant"][0] - (1.0 / 4 + 0.5 / 2) / 2) < 1e-12 and abs(E["max_govde_bant"][0] - 0.25) < 1e-12


def test_karsi_ornek_kapanis():
    sab = MV.mv_sablon(); s = sab["tam"]; K = MV.mv_karsi_ornek(s)
    for k in ("n1", "n2", "n3"):
        assert np.allclose(K[k]["C"], s["ohlc"]["C"]), k
        assert (K[k]["H"] >= np.maximum(K[k]["O"], K[k]["C"]) - 1e-9).all() and (K[k]["L"] <= np.minimum(K[k]["O"], K[k]["C"]) + 1e-9).all()
    assert np.allclose(K["n1"]["H"], np.maximum(K["n1"]["O"], K["n1"]["C"]))          # fitil yok
    assert np.allclose(np.abs(K["n1"]["C"] - K["n1"]["O"]), (s["ohlc"]["H"] - s["ohlc"]["L"]).mean())
    S = MV.mv_S_bilesen(s, {k: s["ohlc"][k] for k in ("O", "H", "L", "C", "BU", "BO", "BA")})
    assert abs(S["S"] - 1.0) < 1e-12


def test_v1_ayni():
    sab = MV.mv_sablon(); rng = np.random.default_rng(3)
    lO, lH, lL, lC = MI.mi_uret(rng, 400, None, "ry"); O, H, L, C = map(np.exp, (lO, lH, lL, lC))
    for ad, s in sab.items():
        b, m = MI.mi_tara_seri(O, H, L, C, s)
        R = MV.mv_tara_seri(O, H, L, C, s, None)
        assert np.allclose(np.nan_to_num(b, nan=-9), np.nan_to_num(R["v1"], nan=-9), atol=1e-12, rtol=0) and (m == R["v1m"]).all()


def test_eksik_hafta():
    gun = pd.bdate_range("2010-01-04", "2012-12-31")
    gun = gun[(gun < "2011-03-07") | (gun > "2011-03-11")]                     # bir hafta tamamen yok
    rng = np.random.default_rng(1); C = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(gun))))
    d = pd.DataFrame({"Open": C, "High": C * 1.01, "Low": C * 0.99, "Close": C, "Volume": 1.0}, index=gun)
    W = MV.mv_haftalik_panel({"X": d})["X"]
    assert int(W.bosluk.sum()) == 1 and W.index[W.bosluk.to_numpy()][0] == pd.Timestamp("2011-03-18")
    e = MV.mv_gecerli_uclar(W, 20, ["2010-01-01", "2012-12-31"]); j = W.index.get_loc(pd.Timestamp("2011-03-18"))
    assert not any(j <= x <= j + 18 for x in e) and (j + 19) in e and (j - 1) in e   # boşluğu içeren 19 pencere sonu atıldı


def test_kapi_mantik():
    q = {"ust_fitil": 0.3, "uzun_ust_pay": 0.2, "alt_fitil": 0.25, "govde_oran": 0.4, "doji_pay": 0.15, "kucuk_mum_pay": 0.4, "mum_bant": 0.5,
         "max_govde_bant": 0.6, "yuk_dip_pay": 0.6, "ortusme": 0.75}
    F = {"ust_fitil": np.array([0.4, 0.2]), "uzun_ust_pay": np.array([0.3, 0.3]), "alt_fitil": np.array([0.2, 0.2]), "govde_oran": np.array([0.3, 0.3]),
         "doji_pay": np.array([0.2, 0.2]), "kucuk_mum_pay": np.array([0.5, 0.5]), "yuk_dip_pay": np.array([0.7, 0.7]), "ortusme": np.array([0.8, 0.8]),
         "pB_bas": np.array([0.1, 0.1]), "pB_son": np.array([0.9, 0.9])}
    EK = {"mum_bant": np.array([0.4, 0.4]), "max_govde_bant": np.array([0.5, 0.9])}
    k = MV.mv_kapilar(F, EK, q)
    assert list(k["k1"]) == [True, False] and list(k["k4"]) == [True, False] and all(k[x].all() for x in ("k2", "k3", "k5", "k6", "k7"))


def test_sablon_kendi_kapilari():
    y = MV._mv_yol("esikler")
    if not os.path.exists(y):
        print("  (eşik tablosu yok: atlandı)"); return
    Q = json.load(open(y, encoding="utf-8")); sab = MV.mv_sablon()
    for z in Q:
        for ad, s in sab.items():
            k = MV.mv_kapilar({a: np.array([b]) for a, b in s["F"].items()}, {a: np.array([b]) for a, b in s["EK"].items()}, Q[z][ad][str(s["L"])])
            assert all(bool(v[0]) for v in k.values()), (z, ad, {a: bool(b[0]) for a, b in k.items()})


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_V2 as M\nns = dict(vars(M))\nns['mv_pct'] = 1\nns['_CK_ONCE_MV'] = {'mv_pct': id(M.mv_pct)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_mv()')[0] + '_cakisma_kontrol_mv()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(MV.__file__)))
    assert "KAPALI" in r.stdout, (r.stdout, r.stderr[-500:])


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
