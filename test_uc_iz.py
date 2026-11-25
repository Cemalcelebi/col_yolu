"""test_uc_iz — UC_IZ sentetik testleri (gerçek veri yok): pencere bayrağı yalnız geçmişten, N sayımı, taban formülü = kaba kuvvet,
kesik denetimi, ÜST10 / ALT10 sınıflaması. Çalıştır: python test_uc_iz.py"""
import itertools
import sys

import numpy as np
import pandas as pd

import UC_IZ as U


def test_pencere_gecmis():
    gi = pd.bdate_range("2020-01-01", periods=60)
    t = np.array([gi[30]])
    # olay t'den 1 gün sonra: bayrak OLMAMALI
    b, s = U.uc_pencere_bayrak(gi, t, np.array([gi[31]]), 15)
    assert not b[0] and pd.isna(s[0])
    # olay t günü: bayrak var
    b, s = U.uc_pencere_bayrak(gi, t, np.array([gi[30]]), 15)
    assert b[0] and pd.Timestamp(s[0]) == gi[30]
    # olay t-14 geçerli bar: var; t-15: yok
    b, _ = U.uc_pencere_bayrak(gi, t, np.array([gi[16]]), 15); assert b[0]
    b, _ = U.uc_pencere_bayrak(gi, t, np.array([gi[15]]), 15); assert not b[0]
    # gelecek + geçmiş olay birlikte: en son <= t olan seçilir
    b, s = U.uc_pencere_bayrak(gi, t, np.array([gi[20], gi[40]]), 15)
    assert b[0] and pd.Timestamp(s[0]) == gi[20]


def test_n_sayim():
    R = np.array([0, 1, 1, 1, 0]); Y1 = np.array([0, 0, 1, 1, 1]); Y2 = np.array([0, 0, 0, 1, 1])
    assert list(U.uc_n(R, Y1, Y2)) == [0, 1, 2, 3, 2]


def test_taban_kaba_kuvvet():
    for N in list(range(1, 40)) + [57, 100, 123]:
        tu, ta = U.uc_taban(np.array([N]))
        # olay N eşle birlikte rastgele sırada: k = olaydan küçük eş sayısı 0..N eşit olasılık; SIRA = k / N
        k = np.arange(N + 1); s = k / N
        bu = np.mean(s >= 0.9 - 1e-12); ba = np.mean(s <= 0.1 + 1e-12)
        assert abs(tu[0] - bu) < 1e-12, (N, tu[0], bu)
        assert abs(ta[0] - ba) < 1e-12, (N, ta[0], ba)
    # sınıflama ile tutarlı: rastgele permütasyon benzetimi
    rng = np.random.default_rng(1)
    N = 13; deg = []
    for _ in range(20000):
        x = rng.normal(size=N + 1); k = int((x[1:] < x[0]).sum()); deg.append(k / N)
    u, a = U.uc_ust_alt(np.array(deg))
    tu, ta = U.uc_taban(np.array([N]))
    assert abs(u.mean() - tu[0]) < 0.01 and abs(a.mean() - ta[0]) < 0.01


def test_kesik():
    X = pd.DataFrame({"D": pd.to_datetime(["2022-12-30", "2022-12-31", "2023-01-02"]), "v": [1, 2, 3]})
    Y = U.uc_kes(X, "D", "deneme")
    assert len(Y) == 2 and Y.D.max() <= U.UC_KESIK


def test_ust_alt_nan():
    u, a = U.uc_ust_alt(np.array([0.95, 0.5, np.nan, 0.05, 0.9, 0.1]))
    assert list(u[[0, 1, 3, 4, 5]]) == [1, 0, 0, 1, 0] and np.isnan(u[2])
    assert list(a[[0, 1, 3, 4, 5]]) == [0, 0, 1, 0, 1]


def test_karar_kurali():
    def c(f, uf, up, n=100, g=0.9, hk="TUTMADI"):
        return {"fark": f, "ust_eksi_taban": uf, "ust_eksi_taban_p": up, "n": n, "guc": g, "hukum": hk}
    H = {"R=1|d1619": c(0.01, 0.02, 0.02), "R=0|d1619": c(0.0, 0, 0), "R=1|d2022": c(0.01, 0.01, 0.01), "R=0|d2022": c(0.005, 0, 0)}
    assert U.uc_iz_karar(H, "R")["karar"] == "YÖN TUTARLI"
    H["R=1|d2022"] = c(0.01, 0.01, -0.01)
    assert U.uc_iz_karar(H, "R")["karar"] == "TUTMADI"
    H["R=1|d2022"] = c(0.01, 0.01, -0.01, n=20)
    assert U.uc_iz_karar(H, "R")["karar"] == "ÖLÇÜLEMEDİ"
    B = {f"{g}|{h}": {"fark": f, "boot_alt": ba} for h in ("d1619", "d2022") for g, f, ba in
         (("N=0", 0.0, -1), ("N=1", 0.01, -1), ("N>=2", 0.02, 0.001 if h == "d1619" else -0.01))}
    assert U.uc_birlikte(B)["birlikte_artiyor"]
    B["N=1|d2022"]["fark"] = 0.03
    assert not U.uc_birlikte(B)["birlikte_artiyor"]


if __name__ == "__main__":
    n = 0
    for ad, f in list(globals().items()):
        if ad.startswith("test_") and callable(f):
            f(); n += 1; print("tamam:", ad)
    print(f"{n} test geçti")
    sys.exit(0)
