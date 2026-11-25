"""test_macd_uyum_kasa.py — MACD_UYUM_KASA sentetik testleri (veri gerekmez).

Kapsam: zincir sırası (60 bar, daha düşük Low(L2)), PFc / MRc (sıra 1'de F65 / MR), T eşikleri (sınır dahil), zincirin geçmişe bağlılığı (sonraki
olaylar öncekileri değiştirmez), ÜST10 / ALT10 sayımı, karar kuralı (TUTTU / KISMEN / TUTMADI / ÖLÇÜLEMEDİ), K11 yeniden üretim, çakışma kapısı.
Çalıştır: python test_macd_uyum_kasa.py
"""
from __future__ import annotations

import os
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
if KOK not in sys.path:
    sys.path.insert(0, KOK)

import MACD_UYUM_KASA as MK  # noqa: E402


def _olay(sat):
    """sat: (sembol, i, low_L1, low_L2, F66, F66m, close_L2)."""
    X = pd.DataFrame(sat, columns=["sembol", "i", "low_L1", "low_L2", "F66", "F66m", "close_L2"])
    X["pazar"] = "ABD"; X["tarih"] = pd.Timestamp("2020-01-01") + pd.to_timedelta(X.i, "D")
    return X


def test_zincir_sira():
    X = _olay([("A", 100, 10.0, 9.0, 0.02, 0.01, 9.5), ("A", 150, 9.5, 8.5, 0.01, 0.005, 9.0), ("A", 210, 9.0, 8.0, 0.01, 0.0, 8.4),
               ("A", 271, 8.0, 7.0, 0.01, 0.0, 7.5), ("A", 300, 7.5, 7.5, 0.01, 0.0, 7.8), ("B", 310, 5.0, 4.0, 0.01, 0.0, 4.2)])
    Z = MK.mk_zincir(X)
    assert Z.zincir.tolist() == [1, 2, 3, 1, 1, 1], Z.zincir.tolist()   # 271-210 = 61 > 60 -> 1; 7,5 < 7,0 değil -> 1; başka hisse -> 1


def test_pfc_mrc():
    X = _olay([("A", 100, 10.0, 9.0, 0.02, 0.01, 9.5), ("A", 150, 9.5, 8.5, 0.01, 0.005, 9.0)])
    Z = MK.mk_zincir(X)
    m1_ilk = (0.01 - 0.02) * 9.5
    assert np.isclose(Z.PFc[0], 9.0 / 10.0 - 1) and np.isclose(Z.MRc[0], 0.02 / abs(0.01 - 0.02))      # sıra 1: F65 ve MR
    assert np.isclose(Z.PFc[1], 8.5 / 10.0 - 1)
    assert np.isclose(Z.MRc[1], (0.005 * 9.0 - m1_ilk) / abs(m1_ilk))


def test_T_esik_sinir():
    X = _olay([("A", 100, 10.0, 8.99, 0.03, 0.0, 9.0), ("B", 100, 10.0, 8.99, 0.2, 0.9, 9.0), ("C", 100, 10.0, 9.01, 0.03, 0.0, 9.0)])
    Z = MK.mk_zincir(X).set_index("sembol")
    # A: PFc -0,101, MRc = 0,03 / 0,03 = 1 -> T; B: MRc 0,2 / 0,7 = 0,286 -> T değil; C: PFc -0,099 -> T değil
    assert bool(Z.loc["A", "T"]) and not bool(Z.loc["B", "T"]) and not bool(Z.loc["C", "T"])
    Y = _olay([("D", 100, 10.0, 8.0, 0.3, 1.0, 9.0)])          # MRc = 0,3 / |0,7| = 0,43 -> T
    assert bool(MK.mk_zincir(Y)["T"].iloc[0])
    W = _olay([("E", 100, 10.0, 8.0, 0.2, 1.0, 9.0)])          # MRc = 0,2 / 0,8 = 0,25 -> T değil
    assert not bool(MK.mk_zincir(W)["T"].iloc[0])


def test_zincir_gecmis():
    rng = np.random.default_rng(1)
    sat = []; i = 0; lo = 10.0
    for _ in range(40):
        i += int(rng.integers(15, 80)); lo *= float(rng.uniform(0.85, 1.1))
        sat.append(("A", i, lo * 1.05, lo, float(rng.normal(0.01, 0.01)), float(rng.normal(0, 0.01)), lo * 1.02))
    X = _olay(sat); Z = MK.mk_zincir(X)
    for k in (5, 17, 33):
        Zk = MK.mk_zincir(X.iloc[:k])
        assert np.array_equal(Zk[["zincir", "PFc", "MRc", "T"]].to_numpy(float), Z.iloc[:k][["zincir", "PFc", "MRc", "T"]].to_numpy(float), equal_nan=True)


def test_ust10():
    x = pd.DataFrame({"r15": np.zeros(10), "es_r15_temiz": np.zeros(10), "sira_temiz": [0.0, 0.05, 0.1, 0.3, 0.5, 0.7, 0.89, 0.9, 0.95, 1.0],
                      "giris": pd.date_range("2023-01-01", periods=10, freq="MS")})
    u = MK.mk_ust10(x, 1)
    assert u["n"] == 10 and np.isclose(u["ust10"], 0.3) and np.isclose(u["alt10"], 0.3) and u["lo"] <= 0.3 <= u["hi"]
    x2 = x.copy(); x2.loc[0, "es_r15_temiz"] = np.nan
    assert MK.mk_ust10(x2, 1)["n"] == 9


def test_karar():
    iyi = {"n": 300, "ust10": 0.18, "lo": 0.12, "alt10": 0.10}
    a = {"ust10": 0.15}; v = {"ust10": 0.12}
    assert MK.mk_karar(iyi, a, v, 0.01)["karar"] == "TUTTU"
    assert MK.mk_karar({**iyi, "lo": 0.09}, a, v, 0.01)["karar"] == "KISMEN"
    assert MK.mk_karar({**iyi, "lo": 0.10}, a, v, 0.01)["karar"] == "KISMEN"          # alt uç > 0,10 şartı kesin büyük
    assert MK.mk_karar(iyi, a, {"ust10": 0.10}, 0.01)["karar"] == "TUTMADI"             # (c) nokta > 0,10 kesin
    assert MK.mk_karar(iyi, a, v, 0.0)["karar"] == "TUTMADI"                            # (d) FARK > 0
    assert MK.mk_karar({**iyi, "alt10": 0.18}, a, v, 0.01)["karar"] == "TUTMADI"        # (b) ÜST10 > ALT10
    assert MK.mk_karar({**iyi, "lo": 0.05, "alt10": 0.2}, a, v, 0.01)["karar"] == "TUTMADI"
    k = MK.mk_karar({**iyi, "n": 99}, a, v, 0.01)
    assert k["karar"] == "ÖLÇÜLEMEDİ" and all(k["madde"].values())                     # yön yine yazılır


def test_yeniden():
    S = pd.DataFrame({"pazar": ["ABD"] * 4 + ["AVR"] * 2, "T": [True, True, False, True, True, True],
                      "r15": [0.1, -0.05, 0.2, 0.03, 0.0, 0.01], "es_r15_temiz": [0.0, 0.0, 0.0, 0.01, 0.0, np.nan],
                      "sira_temiz": [0.95, 0.05, 0.5, 0.6, 0.92, 0.5]})
    with tempfile.TemporaryDirectory() as d:
        y = os.path.join(d, "s.csv.gz"); S.to_csv(y, index=False, compression="gzip")
        J = {"O1": {"T|birlesik": {"n": 4, "ust10": 0.5, "alt10": 0.25}}, "O2": {"T|ABD": {"n": 3, "fark": (0.1 - 0.05 + 0.02) / 3}}}
        assert MK.mk_yeniden(y, J)["tuttu"]
        J["O2"]["T|ABD"]["fark"] = 0.5
        try:
            MK.mk_yeniden(y, J)
            raise AssertionError("yanlış referansta DURMALIYDI")
        except MK.MKHata:
            pass


def test_cakisma():
    G ={"__file__": os.path.join(KOK, "MACD_UYUM_KASA.py"), "__name__": "mk_test", "mk_zincir": lambda: None}
    G["_CK_KAYIT"] = {"mk_zincir": "BASKA.py"}
    try:
        exec(open(os.path.join(KOK, "MACD_UYUM_KASA.py"), encoding="utf-8").read().replace('if __name__ == "__main__"', "if False"), G)
        raise AssertionError("çakışma kapısı durmalıydı")
    except RuntimeError as ex:
        assert "EZDİ" in str(ex)


if __name__ == "__main__":
    n = 0
    for ad, f in list(globals().items()):
        if ad.startswith("test_") and callable(f):
            f(); n += 1; print("TAMAM", ad)
    print(f"{n} test geçti")
