"""test_goz_kural4 — GOZ_KURAL4 sentetik testleri (getiri yok; etiket - ölçü ilişkisi gerçek veride hesaplanmaz).

Kapsam: sayım (beş set işaretli sayfa 126; GT9 s. 1 işaretsiz dışarıda); ölçüler t'den sonraki barı okumaz (bozunca / kesince aynı); yeni ölçüler elle;
Wilson alt ucu elle; gömülü iki şartlı kural set dışında bulunur (B), lojistik (C) doğrusal kuralı bulur; karıştırılmış etikette bulunmaz; set içi
karıştırma set x sınıf sayısını korur; H2 ayıran ölçüyü bulur, ayırmayanı aday saymaz; kapı (ön kayıt yok -> durur; ikinci koşu durur); çakışma kapısı;
tablo varsa uc_set_tablo.json'daki 82 sayfayla birebir (K11).
Çalıştır: python test_goz_kural4.py"""
import json
import os
import sys
import tempfile

import numpy as np
import pandas as pd

import GOZ_KURAL4 as G4

ISIM = []


def t(f):
    ISIM.append(f)
    return f


def _seri(m, tohum=1):
    r = np.random.default_rng(tohum); C = 10 * np.exp(np.cumsum(r.normal(0, 0.02, m)))
    O = C * (1 + r.normal(0, 0.008, m)); H = np.maximum(O, C) * (1 + np.abs(r.normal(0, 0.01, m))) + 1e-6
    L = np.minimum(O, C) * (1 - np.abs(r.normal(0, 0.01, m))) - 1e-6
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1e5}, index=pd.bdate_range(end="2022-12-30", periods=m))


def _sentetik(n_set=5, n=60, k=12, tohum=3, kural=True):
    r = np.random.default_rng(tohum); X = r.normal(0, 1, (n_set * n, k)); ad = [f"m{j}" for j in range(k)]
    T = pd.DataFrame(X, columns=ad); T["set"] = np.repeat([f"S{i}" for i in range(n_set)], n); T["kol"] = "D1"
    T.loc[T.index % 10 == 0, "kol"] = "RASTGELE"
    ev = (X[:, 0] > 0.3) & (X[:, 1] < 0.0) if kural else r.random(len(X)) < 0.2
    c = r.choice(["KISMEN", "ERKEN", "HAYIR"], len(X)); c[ev] = "EVET"; T["cemal"] = c
    return T, ad


@t
def test_sayim():
    P = G4.gk4_sayfalar()
    assert len(P) == 126 and P.groupby("set").size().to_dict() == {"GT1": 30, "GT3": 32, "GT4": 20, "GT5": 21, "GT9": 23}
    assert not ((P["set"] == "GT9") & (P.sayfa == 1)).any()                         # işaretsiz sayfa dışarıda
    assert set(P.cemal) <= set(G4.GK4["sinif"])


@t
def test_sonrasi_okunmaz():
    d = _seri(400, 5); s, tt = 200, 259; o1 = G4.gk4_olc(d, s, tt)
    d2 = d.copy(); r = np.random.default_rng(9); d2.iloc[tt + 1:, :4] *= r.uniform(0.3, 3.0, (len(d) - tt - 1, 1))
    o2 = G4.gk4_olc(d2, s, tt); o3 = G4.gk4_olc(d.iloc[:tt + 1], s, tt)
    for k in o1:
        a, b, c = (np.float64(x) for x in (o1[k], o2[k], o3[k]))
        assert (np.isnan(a) and np.isnan(b) and np.isnan(c)) or (a == b == c), k
    assert set(G4.GK4["yeni_olcu"]) <= set(o1)


@t
def test_yeni_olcu_elle():
    n = 30; H = np.full(n, 11.0); L = np.full(n, 10.0); O = np.full(n, 10.5); C = np.full(n, 10.5)
    L[25] = 9.0; L[27] = 8.5                                                       # son üçte birde (10 bar) iki yeni dip
    O[-10:] = 10.8; C[-10:] = 10.6                                                 # alt fitil (min(O,C) - L) / (H - L)
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C}); o = G4.gk4_yeni_olcu(d, 0, n - 1)
    assert abs(o["YENI_DIP_SON"] - 2 / 10) < 1e-12
    exp = np.mean([(10.6 - L[i]) / (11.0 - L[i]) for i in range(n - 10, n)]); assert abs(o["ALT_FITIL_SON10"] - exp) < 1e-12
    hl = H - L; assert abs(o["SON_BOY_ORAN"] - np.median(hl[-10:]) / np.median(hl)) < 1e-12
    C2 = np.r_[np.linspace(12, 10, 10), np.full(10, 10.0), np.linspace(10, 11, 10)]; d2 = pd.DataFrame({"Open": C2, "High": C2 + 0.1, "Low": C2 - 0.1, "Close": C2})
    o2 = G4.gk4_yeni_olcu(d2, 0, 29); kutu = 12.1 - 9.9; e1 = np.polyfit(np.arange(10), C2[:10], 1)[0]; e2 = np.polyfit(np.arange(10), C2[-10:], 1)[0]
    assert abs(o2["EGIM_FARK"] - (e2 - e1) * 10 / kutu) < 1e-12 and o2["EGIM_FARK"] > 0


@t
def test_wilson_elle():
    k, n, z = 7, 10, 1.96; p = 0.7
    e = (p + z * z / 20 - z * np.sqrt(p * 0.3 / 10 + z * z / 400)) / (1 + z * z / 10)
    assert abs(G4.gk4_wilson(np.array([k]), np.array([n]))[0] - e) < 1e-12 and G4.gk4_wilson(np.array([0]), np.array([0]))[0] == -np.inf


@t
def test_gomulu_kural_set_disi():
    T, ad = _sentetik(); y = (T.cemal == "EVET").astype(int).to_numpy(); H = G4.gk4_hat(T, y, ad, kural_yaz=True)
    mB = G4.gk4_metrik(H["B"], T, boot=False); mC = G4.gk4_metrik(H["C"], T, boot=False)
    assert mB["kabul"] >= 25 and mB["EVET_pay"] >= 0.80 and mB["set_kabul_var"] == 5, mB
    assert all({s["olcu"] for s in K["sart"]} >= {"m0", "m1"} for K in H["kural"]["B"].values())
    assert mC["kabul"] >= 25 and mC["EVET_pay"] >= 0.60, mC
    assert all({"m0", "m1"} <= set(K["olcu"]) for K in H["kural"]["C"].values())


@t
def test_karisik_etikette_bulunmaz():
    T, ad = _sentetik(kural=False, tohum=4); y = (T.cemal == "EVET").astype(int).to_numpy(); H = G4.gk4_hat(T, y, ad)
    for a in G4.GK4_AILE:
        m = G4.gk4_metrik(H[a], T, boot=False)
        assert m["kabul"] == 0 or m["EVET_pay"] < 0.45, (a, m["kabul"], m["EVET_pay"])
    T2, _ = _sentetik(); c = T2.cemal.to_numpy().copy(); r = np.random.default_rng(1)
    for g in T2["set"].unique():
        ii = np.flatnonzero(T2["set"].to_numpy() == g); c[ii] = c[ii][r.permutation(len(ii))]
    y2 = (c == "EVET").astype(int); H2 = G4.gk4_hat(T2, y2, ad); T2b = T2.assign(cemal=c)
    assert all(G4.gk4_metrik(H2[a], T2b, boot=False)["EVET_pay"] in (None,) or G4.gk4_metrik(H2[a], T2b, boot=False)["EVET_pay"] < 0.5 for a in G4.GK4_AILE)


@t
def test_karistirma_yapisi():
    T, ad = _sentetik(n=40); c4 = T.cemal.to_numpy(); K = G4.gk4_karistir(T, c4, 4, 7, ad)
    assert K["B"] == 4 and len(K["T"]) == 4 and all(0 <= x <= 1 for x in K["T"])
    r = np.random.default_rng(7); st = T["set"].to_numpy(); c = c4.copy()                 # aynı tohumla ilk karıştırma set x sınıf sayısını korur
    for g in pd.unique(st):
        ii = np.flatnonzero(st == g); c[ii] = c4[ii][r.permutation(len(ii))]
    assert pd.crosstab(st, c).equals(pd.crosstab(st, c4)) and not (c == c4).all()


@t
def test_h2():
    r = np.random.default_rng(2); n = 200; T = pd.DataFrame({"set": np.repeat([f"S{i}" for i in range(5)], 40), "ayiran": r.normal(0, 1, n), "gurultu": r.normal(0, 1, n)})
    y = (r.random(n) < 0.5).astype(int); T.loc[y == 1, "ayiran"] += 2.0
    H = G4.gk4_h2(T, y, ["ayiran", "gurultu"])
    assert H["ayiran"]["aday"] and H["ayiran"]["havuz_auc"] > 0.85 and H["ayiran"]["ayni_yon_set"] == 5
    assert not H["gurultu"]["aday"]
    T["ters"] = -T["ayiran"]; H = G4.gk4_h2(T, y, ["ters"]); assert H["ters"]["havuz_auc"] > 0.85 and H["ters"]["aday"]   # yön eğitimden


@t
def test_uygula_bos_deger():
    T = pd.DataFrame({"a": [1.0, np.nan, 3.0], "b": [0.0, 0.0, np.nan]})
    K = {"aile": "B", "bos": False, "sart": [{"olcu": "a", "yon": ">=", "esik": 1.0}, {"olcu": "b", "yon": "<=", "esik": 0.0}]}
    assert G4.gk4_uygula(K, T).tolist() == [True, False, False]
    assert G4.gk4_uygula({"aile": "C", "bos": True}, T).tolist() == [False] * 3


@t
def test_kapi():
    with tempfile.TemporaryDirectory() as d:
        try:
            G4.gk4_kapi(cikti=d, ham=d); assert False
        except G4.GK4Hata as ex:
            assert "yok" in str(ex)
        open(os.path.join(d, "kos_kilit.json"), "w").write("{}")
        try:
            G4.gk4_kos(cikti=d, ham=d); assert False
        except G4.GK4Hata as ex:
            assert "BİR KEZ" in str(ex)


@t
def test_cakisma_kapisi():
    try:
        G4._cakisma_kontrol_gk4(_once={"GK4": -1}); assert False
    except RuntimeError as ex:
        assert "çakışma" in str(ex)
    G4._cakisma_kontrol_gk4()


@t
def test_tablo_uc_set_ile_ayni():
    yol = G4._gk4_yol("tablo")
    if not os.path.exists(yol):
        print("  (gt10_tablo.json yok: atlandı)"); return
    T = G4.gk4_tablo_oku(); U = pd.DataFrame(json.load(open(os.path.join(G4.GK4_YOL["cikti"], "uc_set_tablo.json"), encoding="utf-8")))
    M = U.merge(T, on=["set", "sayfa"], suffixes=("_u", ""))
    assert len(M) == 82 and (M.cemal_u == M.cemal).all()
    for c in [c for c in U.columns if c not in ("set", "sayfa", "kol", "pazar", "cemal")]:
        a = M[c + "_u"].to_numpy(float); b = M[c].to_numpy(float)
        assert np.allclose(a, b, rtol=1e-6, atol=1e-9, equal_nan=True), c
    assert len(T) == 126 and T.K3.isin([0, 1]).all()


if __name__ == "__main__":
    hata = 0
    for f in ISIM:
        try:
            f(); print("OK  ", f.__name__)
        except Exception as ex:
            hata += 1; print("HATA", f.__name__, repr(ex))
    print(f"{len(ISIM) - hata} / {len(ISIM)} geçti")
    sys.exit(1 if hata else 0)
