"""test_mum_izi6 — MUM_IZI_ETIKET2 testleri (gerçek fiyat verisi ve Cemal'in işaretleri yok): tam permütasyon p (kaba kuvvetle aynı), katman sınırları,
P2 vektörlü maske = ORTAK_CETVEL.oc_olay_hazirla (sahte panel), seçim kuralları (yarı / BIST tavanı / hisse başına bir), etiket şeması (sıkı),
lojistik ve çapraz doğrulama, hisse taraması (sahte seri: sayım ve seçilen pencerenin katmanı), eşik mührü, kapak metni, çakışma kapısı.
Çalıştır: python test_mum_izi6.py"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

import MUM_IZI as MI
import MUM_IZI_ETIKET2 as E6
import MUM_IZI_V3 as V3


def test_perm_p_tam():
    rng = np.random.default_rng(4)
    for _ in range(5):
        x = np.round(rng.normal(size=10), 1); y = np.r_[np.ones(4, int), np.zeros(6, int)]; rng.shuffle(y)
        assert abs(E6.e6_perm_p(x, y) - V3.v3_perm_p(x, y)) < 1e-12
    x = np.arange(40.0); y = np.r_[np.ones(10, int), np.zeros(30, int)]
    p = E6.e6_perm_p(x, y); assert p > 0 and abs(p - 1 / 847660528) < 1e-15     # C(40, 10)


def test_katman_sinirlari():
    k = E6.e6_katman(np.array([0.0, 0.005, 0.0051, 0.05, 0.051, 0.2, 0.2001, 0.9]))
    assert k.tolist() == [1, 1, 2, 2, 3, 3, 0, 0]


def _sahte_P():
    idx = pd.bdate_range("2020-01-01", periods=40)
    vi = idx[[i for i in range(40) if i not in (5, 6, 7, 20)]]               # hissenin barları (bazı günler yok)
    ok = np.ones((40, 2), bool); ok[10, 0] = False; ok[30:, 0] = False
    Hh = np.zeros((40, 2), np.int64); Hh[12, 0] = -1
    return {"pazar": "ABD", "tarih": idx, "kol": {"AAA": 0}, "gecersiz": {"AAA": pd.DatetimeIndex([idx[15]])}, "Vidx": {"AAA": vi}, "ok": ok, "H": Hh, "kip": "p2"}, vi


def test_p2_maske_oc_ile_ayni():
    import ORTAK_CETVEL as OC
    P, vi = _sahte_P()
    for bz in (1, 2, 10):
        E = json.loads(json.dumps(OC.OC_ESIK)); E["olay"]["tekil_gun"] = 1; E["olay"]["giris_azami_bosluk"] = bz
        X, _ = OC.oc_olay_hazirla(pd.DataFrame({"sembol": "AAA", "tarih": vi}), P, E)
        beklenen = np.isin(vi, pd.DatetimeIndex(X.tarih))
        m = E6.e6_p2_maske(P, "AAA", vi, bz)
        assert m.tolist() == beklenen.tolist(), (bz, np.flatnonzero(m != beklenen))
    assert not E6.e6_p2_maske(P, "YOK", vi).any()


def test_secim_kurallari():
    rng = np.random.default_rng(1); aday = []
    for i in range(60):
        for z in ("gunluk", "haftalik"):
            p = ["ABD", "AVR", "BIST"][i % 3]
            say = {k: int(rng.integers(0, 50)) for k in ("K1", "K2", "K3", "K4")}
            aday.append({"sembol": f"S{i}", "zaman": z, "pazar": p, "say": say,
                         "sec": {k: {"t": 1, "tarih": "2020-01-01", "m": 20, "F1": 0.1, "F1_pct": 0.01} for k in say if say[k]}})
    sec = E6.e6_secim(aday, {"S0", "S1"})
    X = pd.DataFrame(sec)
    assert len(X) == 40 and X.sembol.is_unique and not X.sembol.isin(["S0", "S1"]).any()
    for k, n in (("K1", 16), ("K2", 12), ("K3", 6), ("K4", 6)):
        g = X[X.katman == k]; assert len(g) == n and (g.zaman == "gunluk").sum() == n // 2
        for z in ("gunluk", "haftalik"):
            assert ((g.zaman == z) & (g.pazar == "BIST")).sum() <= (n // 2) // 3
    assert E6.e6_secim(aday, {"S0", "S1"}) == sec                                  # tohumla aynı


def test_etiket_semasi():
    with tempfile.TemporaryDirectory() as d:
        y = os.path.join(d, "e.json")
        json.dump({"sayfalar": {"1": {"isaret": "YOK"}, "2": {"isaret": "EVET"}, "3": {"isaret": "hayır"}, "4": {"isaret": "IKISI"}, "5": {"isaret": "Belirsiz"}}},
                  open(y, "w", encoding="utf-8"), ensure_ascii=False)
        E = E6.e6_etiket_oku(y)
        assert E[2] == (1, "EVET") and E[3] == (0, "HAYIR") and E[4] == (None, "IKISI") and E[5] == (None, "BELIRSIZ") and E[1] == (None, "YOK")
        for kotu in ({"sayfalar": {"2": {"isaret": "benziyor"}}}, {"sayfalar": {"50": {"isaret": "EVET"}}}, {"2": {"isaret": "EVET"}}, {"sayfalar": {"2": "EVET"}}):
            json.dump(kotu, open(y, "w", encoding="utf-8"))
            try:
                E6.e6_etiket_oku(y); raise AssertionError(f"kabul etmemeliydi: {kotu}")
            except E6.E6Hata:
                pass


def test_lojistik_cv():
    rng = np.random.default_rng(2); n = 64; y = np.r_[np.ones(20, int), np.zeros(44, int)]
    X = rng.normal(size=(n, 51)); X[:, 0] += 3.0 * y
    cv = E6.e6_cv_auc(X, y, 1.0, 5, 5, 7); assert cv.mean() > 0.75, cv.mean()
    cv0 = E6.e6_cv_auc(rng.normal(size=(n, 51)), y, 1.0, 5, 5, 7); assert 0.25 < cv0.mean() < 0.75, cv0.mean()
    w = E6._e6_lojistik(np.c_[np.r_[-np.ones(10), np.ones(10)]], np.r_[np.zeros(10), np.ones(10)], 1.0); assert w[1] > 0


def test_hisse_tarama():
    S = V3.v3_sablon(); rng = np.random.default_rng(9)
    lO, lH, lL, lC = MI.mi_uret(rng, 300, None, "ry")
    d = pd.DataFrame({"Open": np.exp(lO), "High": np.exp(lH), "Low": np.exp(lL), "Close": np.exp(lC), "Volume": 1.0},
                     index=pd.bdate_range("2016-01-04", periods=300))
    dag = np.sort(rng.uniform(0.1, 1.0, 2000)); ev = np.ones(300, bool); ev[:150] = False
    R = E6.e6_hisse(d, "X", "gunluk", "ABD", S, dag, ["2016-01-01", "2022-12-31"], ev, 1)
    n_bek = sum(300 - (19 + m - 1) for m in V3.MV3_ESIK["uzunluklar"])
    assert R["n_pencere"] == n_bek and R["say"]["K4"] == R["n_evren"] and R["n_evren"] == 5 * 150
    for k, s in R["sec"].items():
        assert s["t"] >= 150
        kk = int(E6.e6_katman(np.array([s["F1_pct"]]))[0])
        assert k == "K4" or kk == int(k[1])
    R2 = E6.e6_hisse(d, "X", "gunluk", "ABD", S, dag, ["2016-01-01", "2022-12-31"], ev, 1); assert R2 == R


def test_esik_ve_kapak():
    assert E6.e6_esik_sha() == E6.e6_esik_sha(json.loads(json.dumps(E6.E6_ESIK)))
    assert sum(v["n"] for k, v in E6.E6_ESIK["katman"].items() if k.startswith("K")) == 40
    assert E6.E6_ESIK["T2"]["esik"] == {"uyumlu": 0.80, "alt_uc": 0.65, "kismen": 0.65} and E6.E6_ESIK["T1"]["hukum"] == {"tutarli": 7, "kismen": 5}
    assert "48 bölge" in E6.E6_KAPAK and "8'i daha önce gördüklerin" in E6.E6_KAPAK


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_ETIKET2 as M\nns = dict(vars(M))\nns['e6_katman'] = 1\nns['_CK_ONCE_E6'] = {'e6_katman': id(M.e6_katman)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_e6()')[0] + '_cakisma_kontrol_e6()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(E6.__file__)))
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
