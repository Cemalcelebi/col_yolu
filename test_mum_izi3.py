"""test_mum_izi3 — MUM_IZI_HAFTALIK testleri (sentetik; gerçek veri yok): günlük -> haftalık O / H / L / C / V, yarım hafta, tatil haftası,
yıl dönümü ISO haftası, prefix (veri t haftasında kesilince S(t) aynı), hücre sınırları, çakışma kapısı. Çalıştır: python test_mum_izi3.py"""
import os
import subprocess
import sys

import numpy as np
import pandas as pd

import MUM_IZI as MI
import MUM_IZI_HAFTALIK as MH


def _gunluk(gun, tohum=1):
    rng = np.random.default_rng(tohum); n = len(gun)
    C = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n))); O = C * np.exp(rng.normal(0, 0.004, n))
    H = np.maximum(O, C) * (1 + np.abs(rng.normal(0, 0.004, n))) + 1e-6; L = np.minimum(O, C) * (1 - np.abs(rng.normal(0, 0.004, n)))
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.uniform(1, 2, n)}, index=gun)


def test_haftalik_ohlcv():
    gun = pd.bdate_range("2022-01-03", "2022-03-31"); d = _gunluk(gun)
    W = MH.mh_haftalik(d, pd.Timestamp("2022-03-31"))
    for wk, g in d.groupby([d.index.isocalendar().year, d.index.isocalendar().week]):
        if g.index[-1] not in W.index:
            continue
        r = W.loc[g.index[-1]]
        assert r.Open == g.Open.iloc[0] and r.Close == g.Close.iloc[-1] and r.High == g.High.max() and r.Low == g.Low.min()
        assert abs(r.Volume - g.Volume.sum()) < 1e-9 and r.bas == g.index[0] and r.n_gun == len(g)


def test_yarim_hafta_ve_tatil():
    gun = pd.bdate_range("2022-01-03", "2022-02-09")           # 2022-02-09 çarşamba: son hafta yarım
    gun = gun.drop(pd.Timestamp("2022-01-17"))                   # tatil: o hafta 4 gün
    d = _gunluk(gun)
    W = MH.mh_haftalik(d, pd.Timestamp("2022-02-09"))
    assert W.index[-1] == pd.Timestamp("2022-02-04")             # yarım hafta atıldı
    assert int(W.loc[pd.Timestamp("2022-01-21")].n_gun) == 4 and W.loc[pd.Timestamp("2022-01-21")].bas == pd.Timestamp("2022-01-18")
    W2 = MH.mh_haftalik(d, pd.Timestamp("2022-02-11"))           # veri sonu cuma -> son hafta tam sayılır
    assert W2.index[-1] == pd.Timestamp("2022-02-09")


def test_iso_yil_donumu():
    gun = pd.bdate_range("2020-12-28", "2021-01-15"); d = _gunluk(gun)
    W = MH.mh_haftalik(d, pd.Timestamp("2021-01-15"))
    assert W.index[0] == pd.Timestamp("2021-01-01") and W.bas.iloc[0] == pd.Timestamp("2020-12-28")   # ISO 2020-W53


def test_prefix():
    gun = pd.bdate_range("2010-01-04", "2016-12-30"); d = _gunluk(gun, 7)
    sab = MI.mi_sablon_yukle()
    W = MH.mh_haftalik(d, pd.Timestamp("2016-12-30"))
    for ad, s in sab.items():
        b, _ = MI.mi_tara_seri(*(W[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), s)
        for t in (60, 150, 250, len(W) - 1):
            tt = W.index[t]
            Wk = MH.mh_haftalik(d[d.index <= tt], tt + pd.Timedelta(days=6))
            bk, _ = MI.mi_tara_seri(*(Wk[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), s)
            assert Wk.index[-1] == tt and abs(bk[-1] - b[t]) < 1e-12, (ad, t)


def test_hucre():
    h = MH.mh_hucre(pd.to_datetime(["2000-12-29", "2001-01-02", "2007-12-31", "2008-01-02", "2015-12-31", "2016-01-04", "2022-12-30"]))
    assert list(h) == ["dis", "h0107", "h0107", "h0815", "h0815", "h1622", "h1622"]


def test_esik_ayni():
    sab = MI.mi_sablon_yukle()
    assert abs(sab["tam"]["esik"] - MH.MH_ESIK["esik"]["tam"]) < 1e-12 and abs(sab["tepesiz"]["esik"] - MH.MH_ESIK["esik"]["tepesiz"]) < 1e-12


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_HAFTALIK as M\nns = dict(vars(M))\nns['mh_hucre'] = 1\nns['_CK_ONCE_MH'] = {'mh_hucre': id(M.mh_hucre)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_mh()')[0] + '_cakisma_kontrol_mh()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(MH.__file__)))
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
