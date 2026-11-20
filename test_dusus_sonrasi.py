"""test_dusus_sonrasi — DUSUS_SONRASI.py mekanik denetimleri (sentetik veri; gerçek veri / sonuç görülmez).

Kapsam: çakışma kapısı, DS olay tespiti, prefix (veri t'de kesilince aynı özellik), DS içi eş toplama, BH + permütasyon p, uçtan uca
sentetik ön kayıt + koşu (eşik eşitliği, yeniden üretim, bağımsız h5 simülasyonu, ikinci koşu durur).
Çalıştır:  python test_dusus_sonrasi.py   (ya da pytest -q test_dusus_sonrasi.py)
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import DUSUS_SONRASI as D  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402


def _seri(n: int, tohum: int, bas: str = "2018-01-02", cokus: int = 3, fiyat: float = 50.0) -> pd.DataFrame:
    rng = np.random.default_rng(tohum)
    r = rng.normal(0.0004, 0.02, n)
    for _ in range(cokus):
        a = int(rng.integers(150, n - 120)); r[a:a + 45] += -0.012
    C = fiyat * np.exp(np.cumsum(r))
    O = np.r_[C[0], C[:-1]] * (1 + rng.normal(0, 0.006, n))
    H = np.maximum(O, C) * (1 + np.abs(rng.normal(0, 0.008, n))) + 1e-6
    L = np.minimum(O, C) * (1 - np.abs(rng.normal(0, 0.008, n)))
    V = rng.lognormal(np.log(2e5), 0.4, n)
    ix = pd.bdate_range(bas, periods=n)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=ix)


def _bag_tek(df: pd.DataFrame) -> dict:
    rm = df.Close.pct_change(); return {"rm": rm, "E": (1 + rm.fillna(0)).cumprod(), "r21ref": {"X": df.Close * np.nan}}


_ESIK = {"DS05_q": 1.5, "DS05_m": 0.0}


def test_cakisma_kapisi():
    kaynak = open(os.path.join(KOK, "DUSUS_SONRASI.py"), encoding="utf-8").read()
    ns = {"__name__": "ds_test"}
    exec(compile(kaynak, "DUSUS_SONRASI.py", "exec"), ns)          # temiz bellek: geçer
    exec(compile(kaynak, "DUSUS_SONRASI.py", "exec"), ns)          # aynı dosya yeniden: geçer
    ns2 = {"__name__": "ds_test", "ds_veri": 1}
    exec(compile(kaynak, "DUSUS_SONRASI.py", "exec"), ns2)         # ds_ önekli ad: geçer
    ns3 = {"__name__": "ds_test", "KOK_DS": "başka modülün adı"}
    try:
        exec(compile(kaynak, "DUSUS_SONRASI.py", "exec"), ns3)
    except RuntimeError as ex:
        assert "EZDİ" in str(ex)
    else:
        raise AssertionError("çakışma kapısı önek dışı adı ezmeye izin verdi")


def test_olay_tespiti():
    n = 400; ix = pd.bdate_range("2019-01-01", periods=n)
    C = np.r_[np.full(150, 100.0), np.linspace(100, 55, 60), 55 + np.sin(np.arange(n - 210)) * 0.5]
    df = pd.DataFrame({"Open": C, "High": C * 1.01, "Low": C * 0.99, "Close": C, "Volume": np.full(n, 1e5), "Kur": 1.0}, index=ix)
    T, a, d = D.ds_ozellik_hisse(df, "ABD", _bag_tek(df), "X", None)
    assert len(T) > 50 and d.sum() == len(T)
    assert (T.dus <= -0.30).all() and (T.f15 <= 0.25).all()
    assert pd.Timestamp(T.tarih.min()) >= ix[180]
    up = df.copy(); up["Close"] = np.linspace(50, 150, n); up["Open"] = up.Close; up["High"] = up.Close * 1.01; up["Low"] = up.Close * 0.99
    T2, _, _ = D.ds_ozellik_hisse(up, "ABD", _bag_tek(up), "X", None)
    assert len(T2) == 0
    lo = df.copy(); lo["Volume"] = 100.0   # likidite 1 mn $ altı
    T3, _, _ = D.ds_ozellik_hisse(lo, "ABD", _bag_tek(lo), "X", None)
    assert len(T3) == 0


def test_prefix():
    df = _seri(900, 7); df["Kur"] = 1.0
    bag = _bag_tek(df)
    T, _, _ = D.ds_ozellik_hisse(df, "AVR", bag, "X", _ESIK)
    assert len(T) > 10
    rng = np.random.default_rng(3)
    for t in pd.to_datetime(T.tarih.to_numpy()[rng.choice(len(T), 8, replace=False)]):
        bk = {"rm": bag["rm"].loc[:t], "E": bag["E"].loc[:t], "r21ref": {"X": bag["r21ref"]["X"].loc[:t]}}
        Tt, _, _ = D.ds_ozellik_hisse(df.loc[:t], "AVR", bk, "X", _ESIK)
        a = Tt[pd.to_datetime(Tt.tarih) == t].iloc[0]; b = T[pd.to_datetime(T.tarih) == t].iloc[0]
        for k in D._DS_HAM:
            assert np.isclose(a[k], b[k], rtol=1e-9, atol=1e-12, equal_nan=True), (t, k, a[k], b[k])


def test_es_topla():
    A = pd.DataFrame({"x": [0, 0]}, index=[10, 20])
    Fall = pd.DataFrame({"F_DS01": [np.nan] * 30}); Fall.loc[[1, 2, 3, 4, 5], "F_DS01"] = [0, 0, 0, 1, 0]
    Cd = {"ce": np.array([10, 10, 10, 10, 20, 20]), "cr": np.array([1, 2, 3, 4, 5, 6]),
          "c5": np.array([1.0, 0.0, 1.0, 1.0, 1.0, 0.0]), "c10": np.zeros(6), "cst": np.array([0.0, 1.0, 0.0, 0.0, 0.0, 1.0])}
    r = D.ds_es_topla(A, Cd, Fall, "DS01", 3)
    assert r["n_es"].tolist() == [3.0, 1.0]
    assert np.isclose(r["es_h5"][0], 2 / 3) and np.isnan(r["es_h5"][1])
    h = D.ds_es_topla(A, Cd, Fall, "_hepsi", 2)
    assert h["n_es"].tolist() == [4.0, 2.0] and np.isclose(h["es_h5"][1], 0.5)


def test_bh_perm():
    assert YH._yh_bh([0.001, 0.01, 0.03, 0.5], 0.10) == [True, True, True, False]
    g = pd.DataFrame({"h5": np.ones(120), "es_h5": np.zeros(120), "giris": pd.date_range("2023-01-01", periods=120, freq="7D")})
    assert D.ds_perm_p(g, "+", 2000, 1) < 0.01 and D.ds_perm_p(g, "-", 2000, 1) > 0.99
    rng = np.random.default_rng(5)
    g2 = g.assign(h5=rng.integers(0, 2, 120).astype(float), es_h5=rng.integers(0, 2, 120).astype(float))
    assert 0.0 < D.ds_perm_p(g2, "?", 2000, 1) <= 1.0
    assert len(D.DS_HIP) == D.DS_ESIK["bh"]["m"] == 25


def _sentetik_vd(pazar: str, n_hisse: int, tohum: int) -> dict:
    V = {f"S{pazar[0]}{i:03d}": _seri(1950, tohum * 100 + i, cokus=4, fiyat=float(20 + i)) for i in range(n_hisse)}
    Vd = OC._oc_veri_sar(V, pazar); Vd["temiz"] = {}; Vd["temiz_n"] = 0
    return Vd


def test_uctan_uca_sentetik():
    """Sentetik üç pazar: ön kayıt -> koşu (git / kontrol kapısı kapalı) -> yeniden üretim + bağımsız h5 simülasyonu tutmalı; ikinci koşu durur."""
    tmp = tempfile.mkdtemp(prefix="ds_test_"); eski = D.ds_veri
    try:
        Vs = {p: _sentetik_vd(p, 48, k + 1) for k, p in enumerate(D.DS_PAZAR)}
        D.ds_veri = lambda pazar, klasor=None: {**Vs[pazar], "V": dict(Vs[pazar]["V"]), "not": []}
        y = D.ds_onkayit_yaz(cikti=tmp, veri=tmp, islem=1)
        assert os.path.exists(y) and os.path.exists(os.path.join(tmp, "ds_esik.json"))
        pre = json.load(open(os.path.join(tmp, "ds_prefix.json"), encoding="utf-8"))
        assert all(pre[p]["bozuk"] == 0 for p in D.DS_PAZAR)
        R = D.ds_kos(cikti=tmp, veri=tmp, islem=2, git=False, kontrol=False)   # çok işlemli yol
        J = R["json"]
        assert sum(J["etiket_sayim"].values()) == 25
        assert all(r["durum"] == "TUTTU" for r in J["yeniden_uretim"])
        assert J["elle_sim"]["n"] > 0 and not J["elle_sim"]["bozuk"]
        assert os.path.exists(os.path.join(tmp, "DS_RAPOR.md")) and os.path.exists(os.path.join(tmp, "ds_olay.csv.gz"))
        O = pd.read_csv(os.path.join(tmp, "ds_olay.csv.gz"))
        assert set(O.donem.unique()) <= {"egitim", "sinama"} and O.giris.min() >= "2016-01-01"
        try:
            D.ds_kos(cikti=tmp, veri=tmp, islem=1, git=False, kontrol=False)
        except D.DSHata:
            pass
        else:
            raise AssertionError("ikinci koşu durmadı")
    finally:
        D.ds_veri = eski
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    for ad, f in list(globals().items()):
        if ad.startswith("test_") and callable(f):
            f(); print("GEÇTİ", ad)
    print("HEPSİ GEÇTİ")
