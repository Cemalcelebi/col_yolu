"""test_mum_izi11 — MUM_IZI_GOZ testleri: işaret şeması (KISMEN dahil; bilinmeyen DUR), örneklem sayımı (104 bölge; tekrarlar ayrı değil), olay ölçüsü elle
hesapla aynı (günlük ve haftalık; K11), stop-önce kuralı, kesik, permütasyon / bootstrap, çakışma kapısı.
Çalıştır: python test_mum_izi11.py"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

import MUM_IZI_GOZ as GZ
import MUM_IZI_V2 as MV


def _gunluk(n=200, tohum=2):
    rng = np.random.default_rng(tohum); ix = pd.bdate_range("2019-01-01", periods=n)
    C = 100 * np.exp(np.cumsum(rng.normal(0, 0.02, n))); O = C * np.exp(rng.normal(0, 0.01, n))
    H = np.maximum(O, C) * (1 + np.abs(rng.normal(0, 0.01, n))); L = np.minimum(O, C) * (1 - np.abs(rng.normal(0, 0.01, n)))
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1000.0}, index=ix)


def test_isaret_sema():
    with tempfile.TemporaryDirectory() as d:
        y = os.path.join(d, "e.json")
        json.dump({"sayfalar": {"2": {"isaret": "KISMEN"}, "3": {"isaret": "evet"}, "4": {"isaret": "YOK"}}}, open(y, "w", encoding="utf-8"))
        assert GZ.gz_isaret_oku(y) == {2: "KISMEN", 3: "EVET", 4: "YOK"}
        json.dump({"sayfalar": {"2": {"isaret": "belki"}}}, open(y, "w", encoding="utf-8"))
        try:
            GZ.gz_isaret_oku(y); raise AssertionError("kabul etmemeliydi")
        except GZ.GZHata:
            pass


def test_ornek():
    if not all(os.path.exists(v[0]) for v in GZ.GZ_YOL["set"].values()):
        print("  (etiket dosyaları yok: atlandı)"); return
    X = GZ.gz_ornek(); S = GZ.gz_ornek_sayim(X)
    assert S["toplam"] == 104 and S["sinif"] == {"HAYIR": 71, "EVET": 25, "KISMEN": 8}, S["sinif"]
    assert not X.duplicated(["zaman", "sembol", "tarih"]).any() and S["tekrar_degisen"] == 2


def test_olcu_gunluk_elle():
    D = _gunluk(); t = 120; m = 18; r = {"zaman": "gunluk", "tarih": D.index[t], "m": m}
    rec = GZ.gz_olc_bir(D, None, r, pd.Timestamp("2030-01-01"))
    E0 = D.Open.iloc[t + 1]; stop = D.Low.iloc[t - m + 1:t + 1].min() * 0.98
    assert abs(rec["E0"] - E0) < 1e-12 and abs(rec["stop"] - stop) < 1e-12
    if E0 > stop:
        assert abs(rec["R15"] - (D.Close.iloc[t + 15] / E0 - 1)) < 1e-12
        assert abs(rec["max15"] - (D.High.iloc[t + 1:t + 16].max() / E0 - 1)) < 1e-12 and abs(rec["min15"] - (D.Low.iloc[t + 1:t + 16].min() / E0 - 1)) < 1e-12
        ilk_stop = next((i for i in range(t + 1, t + 16) if D.Low.iloc[i] <= stop), None)
        for x, k in ((0.05, "d5"), (0.10, "d10")):
            ilk = next((i for i in range(t + 1, t + 16) if D.High.iloc[i] >= E0 * (1 + x)), None)
            assert rec[k] == float(ilk is not None and (ilk_stop is None or ilk < ilk_stop))
        assert abs(rec["R30"] - (D.Close.iloc[t + 30] / E0 - 1)) < 1e-12
    rec2 = GZ.gz_olc_bir(D, None, r, D.index[t + 10]); assert rec2["neden"] == "ufuk_kesik"


def test_olcu_haftalik_elle():
    D = _gunluk(600, 5); W = MV.mv_haftalik_panel({"X": D})["X"]; t = 60; m = 16
    rec = GZ.gz_olc_bir(D, W, {"zaman": "haftalik", "tarih": W.index[t], "m": m}, pd.Timestamp("2030-01-01"))
    g = W.bas.iloc[t + 1]; E0 = D.Open.loc[g]; assert abs(rec["E0"] - E0) < 1e-12 and rec["giris"] == g
    if rec["olculdu"]:
        e = W.index[t + 15]; assert abs(rec["R15"] - (D.Close.loc[e] / E0 - 1)) < 1e-12 and abs(rec["R15"] - (W.Close.iloc[t + 15] / E0 - 1)) < 1e-12
        assert abs(rec["max15"] - (D.High.loc[g:e].max() / E0 - 1)) < 1e-12 and "d20" in rec


def test_stop_once():
    ix = pd.bdate_range("2020-01-01", periods=80); C = np.full(80, 100.0); O = C.copy(); H = C + 0.5; L = C - 0.5
    L[62] = 90.0; H[62] = 112.0                              # aynı gün hem stop hem +%10: stop önce
    D = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1.0}, index=ix)
    rec = GZ.gz_olc_bir(D, None, {"zaman": "gunluk", "tarih": ix[50], "m": 16}, pd.Timestamp("2030-01-01"))
    assert rec["stop15"] == 1.0 and rec["d10"] == 0.0 and rec["d5"] == 0.0


def test_perm_boot():
    a = np.arange(20.0); b = np.arange(20.0) + 100
    assert GZ.gz_perm(a, b, 2000, 1) < 0.01 and GZ.gz_perm(a, a.copy(), 2000, 1) > 0.9
    B = GZ.gz_boot(np.arange(50.0), 1000, 1); assert B["ort95"][0] < 24.5 < B["ort95"][1]


def test_esik_sabit():
    E = GZ.GZ_ESIK["olcu"]; assert E["ufuk"] == 15 and E["hedef"] == {"gunluk": [0.05, 0.10], "haftalik": [0.10, 0.20]} and E["stop_carpan"] == 0.98
    assert GZ.GZ_ESIK["tablo"]["n_az"] == 30 and GZ.gz_esik_sha() == GZ.gz_esik_sha(json.loads(json.dumps(GZ.GZ_ESIK)))


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_GOZ as M\nns = dict(vars(M))\nns['gz_perm'] = 1\nns['_CK_ONCE_GZ'] = {'gz_perm': id(M.gz_perm)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_gz()')[0] + '_cakisma_kontrol_gz()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(GZ.__file__)))
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
