"""test_yukselis_oncesi — YUKSELIS_ONCESI sentetik testleri (gerçek veri / sonuç görülmez; ağ yok).

Kapsam: Y10 / Y5 / D10 'önce hangisine dokundu' (elle kurulmuş seriler; aynı barda iki sınır = stop önce), MUM_IZI_GOZ.gz_olc_bir ile rastgele serilerde
birebir; her özelliğin elle hesaplanmış küçük örneği; özelliklerin k + 1 ve sonrasını kullanmadığı (sonrası bozulunca aynı); her 5 barda örnekleme;
kesimlerin yalnız keşiften gelmesi; ATRP beşliği içi KAT; eşli kontrol tohumu; ay kümeli bootstrap; BH; kesik assert; ADIM 1 sonuç kapısı; uçtan uca
sentetik pazar (hazırla -> sonuç -> ADIM 1 -> ADIM 2); çakışma kapısı.
Çalıştır: python test_yukselis_oncesi.py"""
import os
import sys
import tempfile

import numpy as np
import pandas as pd

import YUKSELIS_ONCESI as YO
import MUM_IZI_GOZ as GZ

ISIM = []


def t(f):
    ISIM.append(f)
    return f


def _dep(O, H, L, C):
    m = len(C)
    return {"O": np.asarray(O, float), "H": np.asarray(H, float), "L": np.asarray(L, float), "C": np.asarray(C, float),
            "POS": np.arange(m, dtype=np.int64), "off": np.array([0, m], np.int64)}


def _seri(n, tohum=1, son="2022-12-30", s=0.02):
    ix = pd.bdate_range(end=son, periods=n); r = np.random.default_rng(tohum)
    C = 20 * np.exp(np.cumsum(r.normal(0, s, n))); O = C * np.exp(r.normal(0, s / 2, n))
    H = np.maximum(O, C) * (1 + np.abs(r.normal(0, s, n))) + 1e-6; L = np.minimum(O, C) * (1 - np.abs(r.normal(0, s, n)))
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1000.0, "Kur": 1.0}, index=ix)


# ---------------------------------------------------------------- dokunma
@t
def test_dokunma_elle():
    E0 = np.array([100.0])
    # hedef 3. barda, stop yok -> 1
    H = np.array([[101, 105, 110.5, 100]]); L = np.array([[99, 99, 99, 99]])
    assert YO.yo_ilk_dokunma(E0, H, L, 0.10, 0.05)[0] == 1
    # stop 2. barda, hedef 3. barda -> 0
    L2 = np.array([[99, 94.9, 99, 99]])
    assert YO.yo_ilk_dokunma(E0, H, L2, 0.10, 0.05)[0] == 0
    # aynı barda hedef ve stop -> stop önce -> 0
    H3 = np.array([[101, 111, 101, 101]]); L3 = np.array([[99, 94, 99, 99]])
    assert YO.yo_ilk_dokunma(E0, H3, L3, 0.10, 0.05)[0] == 0
    # sınır dahil: High = 110 tam (>=) ve Low = 95 tam (<=)
    assert YO.yo_ilk_dokunma(E0, np.array([[110.0000001, 100]]), np.array([[99.0, 95.0]]), 0.10, 0.05)[0] == 1   # 100 x 1,10 kayan noktada 110,00000000000001 (GZ ile aynı formül)
    assert YO.yo_ilk_dokunma(E0, np.array([[101.0, 110.0]]), np.array([[95.0, 99.0]]), 0.10, 0.05)[0] == 0
    # D10 aynası: Low <= 90 önce, High >= 105 sonra -> 1; aynı bar -> 0
    assert YO.yo_ilk_dokunma(E0, np.array([[101, 106.0]]), np.array([[89.9, 99]]), 0.10, 0.05, "asagi")[0] == 1
    assert YO.yo_ilk_dokunma(E0, np.array([[105.0, 100]]), np.array([[89.0, 99]]), 0.10, 0.05, "asagi")[0] == 0
    assert YO.yo_ilk_dokunma(E0, np.array([[105.0, 100]]), np.array([[95.0, 89]]), 0.10, 0.05, "asagi")[0] == 0
    # hiçbiri -> 0; NaN hücre dokunmaz
    assert YO.yo_ilk_dokunma(E0, np.array([[np.nan, 101]]), np.array([[np.nan, 99]]), 0.10, 0.05)[0] == 0


@t
def test_sonuc_dizi_elle():
    m = 40; C = np.full(m, 100.0); O = C.copy(); H = C * 1.01; L = C * 0.99
    O[11] = 100.0; H[13] = 111.0       # t = 10: giriş 11. bar açılışı 100, 13. barda +%11 -> Y10 = Y5 = 1
    C[25] = 104.0
    D = YO.yo_sonuc_dizi(_dep(O, H, L, C), np.array([0]), np.array([10]))
    assert D["E0"][0] == 100 and D["Y10"][0] == 1 and D["Y5"][0] == 1 and D["D10"][0] == 0 and abs(D["R15"][0] - 0.04) < 1e-12
    L2 = L.copy(); L2[12] = 94.0       # 12. barda -%6 (stop) -> Y10 = Y5 = 0
    D = YO.yo_sonuc_dizi(_dep(O, H, L2, C), np.array([0]), np.array([10]))
    assert D["Y10"][0] == 0 and D["Y5"][0] == 0
    try:
        YO.yo_sonuc_dizi(_dep(O, H, L, C), np.array([0]), np.array([30]))
    except YO.YOHata:
        pass
    else:
        raise AssertionError("pencere aşımı durmadı")


@t
def test_gz_ile_birebir():
    """Rastgele seriler: m = 1 bölgesinin dibi x 0,98 = E0 x 0,95 olacak biçimde t barı kurulur; gz_olc_bir d10 / d5 = Y10 / Y5."""
    say = 0
    for tohum in range(60):
        D = _seri(80, tohum, s=0.03)
        for tt in (20, 37, 50):
            D2 = D.copy(); E0 = float(D2.Open.iloc[tt + 1]); lo = E0 * 0.95 / 0.98
            D2.iloc[tt, D2.columns.get_loc("Low")] = lo; D2.iloc[tt, D2.columns.get_loc("Open")] = lo * 1.004
            D2.iloc[tt, D2.columns.get_loc("Close")] = lo * 1.006; D2.iloc[tt, D2.columns.get_loc("High")] = lo * 1.01
            g = GZ.gz_olc_bir(D2, None, {"zaman": "gunluk", "tarih": D2.index[tt], "m": 1}, YO.YO_KESIK)
            if not g["olculdu"]:
                continue
            dep = _dep(D2.Open, D2.High, D2.Low, D2.Close); y = YO.yo_sonuc_dizi(dep, np.array([0]), np.array([tt]))
            st = float(D2.Low.iloc[tt]) * 0.98
            Ls = D2.Low.to_numpy()[tt + 1:tt + 16]
            if np.isclose(Ls, st, rtol=1e-9, atol=0).any() or np.isclose(Ls, E0 * 0.95, rtol=1e-9, atol=0).any():
                continue
            assert y["Y10"][0] == g["d10"] and y["Y5"][0] == g["d5"], (tohum, tt, y, g)
            assert abs(y["R15"][0] - g["R15"]) < 1e-12
            say += 1
    assert say >= 150, say


# ---------------------------------------------------------------- özellikler
def _oz(O, H, L, C, Lp=None):
    C = np.asarray(C, float)
    return YO.yo_hisse_ozellik(np.asarray(O, float), np.asarray(H, float), np.asarray(L, float), C, np.ones(len(C)) if Lp is None else Lp)


@t
def test_mikro_elle():
    m = 70; C = np.full(m, 10.0)
    # son 60 barın (k = 69: u_10 .. u_69) içinde iki seri >= 3 (20-23: 4 yükseliş; 40-42: 3), bir seri 2 (50-51)
    for a, b in ((20, 24), (40, 43), (50, 52)):
        for i in range(a, b):
            C[i] = C[i - 1] + 1
        for i in range(b, m):
            C[i] = C[b - 1]
    F = _oz(C, C + 1, C - 1, C)
    assert F["MIKRO"][69] == 2, F["MIKRO"][69]
    assert np.isnan(F["MIKRO"][59]) and np.isfinite(F["MIKRO"][60])


@t
def test_mikro_pencere_basi():
    m = 80; C = np.full(m, 10.0)
    for i in range(15, 25):
        C[i] = C[i - 1] + 0.5
    C[25:] = C[24]
    F = _oz(C, C + 1, C - 1, C)
    # k = 79: pencere u_20 .. u_79; seri u_15..u_24 pencere içinde u_20..u_24 (5) -> 1 seri
    assert F["MIKRO"][79] == 1
    # k = 81 olsaydı u_22..u_24 (3) -> hâlâ 1; k = 83 -> u_24 (1) -> 0 (seriyi kendimiz kontrol: k = 79 + 3 = 82: u_23, u_24 -> 0)
    C2 = np.r_[C, np.full(4, C[-1])]; F2 = _oz(C2, C2 + 1, C2 - 1, C2)
    assert F2["MIKRO"][81] == 1 and F2["MIKRO"][82] == 0


@t
def test_rs_konum_bayrak():
    m = 130; C = np.linspace(10, 20, m); Lp = np.linspace(1, 3, m)        # göreli güç düşüyor
    F = _oz(C, C * 1.01, C * 0.99, C, Lp)
    rs = C / Lp; k = 125
    assert abs(F["RS_UZAK"][k] - (rs[k] / rs[k - 59:k + 1].max() - 1)) < 1e-12
    lo, hi = C[k - 119:k + 1].min(), C[k - 119:k + 1].max()
    assert abs(F["KONUM120"][k] - (C[k] - lo) / (hi - lo)) < 1e-12
    assert F["RS_DIP_BIR"][k] == 0.0         # konum 1 (tepede) -> bayrak 0
    C2 = np.r_[np.linspace(20, 10, 100), np.linspace(10, 11, 30)]; Lp2 = np.r_[np.linspace(1, 0.4, 100), np.linspace(0.4, 0.39, 30)]
    F2 = _oz(C2, C2 * 1.01, C2 * 0.99, C2, Lp2)
    assert F2["KONUM120"][129] < 0.5 and F2["RS_UZAK"][129] >= -0.03 and F2["RS_DIP_BIR"][129] == 1.0
    assert np.isnan(F["RS_DIP_BIR"][50])


@t
def test_oyn_atrp_elle():
    D = _seri(120, 3); O, H, L, C = (D[c].to_numpy() for c in ("Open", "High", "Low", "Close")); F = _oz(O, H, L, C); k = 100
    lr = np.log(C[k - 59:k + 1] / C[k - 60:k])
    assert abs(F["_oyn60"][k] - np.std(lr, ddof=1)) < 1e-12
    pc = C[k - 20:k]; tr = np.maximum(H[k - 19:k + 1], pc) - np.minimum(L[k - 19:k + 1], pc)
    assert abs(F["ATRP20"][k] - tr.mean() / C[k]) < 1e-12
    assert abs(F["F15"][k] - (C[k] / C[k - 15] - 1)) < 1e-12


@t
def test_ma_elle():
    m = 260; C = np.linspace(10, 30, m)                     # düz yükselen: SMA20 > SMA50 > SMA200 -> 3
    F = _oz(C, C * 1.01, C * 0.99, C)
    assert F["MA_KOD"][250] == 3 and np.isnan(F["MA_KOD"][198]) and F["MA_KOD"][199] == 3
    Cd = C[::-1].copy(); Fd = _oz(Cd, Cd * 1.01, Cd * 0.99, Cd)
    assert Fd["MA_KOD"][250] == 0
    k = 100; s20 = lambda i: C[i - 19:i + 1].mean()  # noqa: E731
    e = lambda i: s20(i) / s20(i - 10) - 1  # noqa: E731
    assert abs(F["MA_EGIM_DEG"][k] - (e(k) - e(k - 10))) < 1e-12


@t
def test_dd_elle():
    m = 300; C = np.r_[np.linspace(10, 20, 150), np.linspace(20, 12, 100), np.linspace(12, 14, 50)]
    F = _oz(C, C * 1.01, C * 0.99, C); k = 299
    w = C[k - 249:k + 1]; pk = k - 249 + (249 - np.argmax(w[::-1])); dk = k - int(np.argmin(C[pk:k + 1][::-1]))
    assert pk == 150 and dk == 250                         # linspace sınırında iki eşit değer: SON görüldüğü bar
    assert F["ZIRVE_BAR"][k] == k - 150 and abs(F["ZIRVE_DUSUS"][k] - (C[k] / 20 - 1)) < 1e-12
    assert F["DIP_BAR"][k] == k - 250 and abs(F["DIP_HIZ"][k] - (C[k] / C[250] - 1) / (k - 250) * 100) < 1e-9
    assert np.isnan(F["ZIRVE_BAR"][248]) and np.isfinite(F["ZIRVE_BAR"][249])


@t
def test_clv_dip_kontrol_elle():
    D = _seri(320, 5); O, H, L, C = (D[c].to_numpy() for c in ("Open", "High", "Low", "Close")); F = _oz(O, H, L, C); k = 300
    clv = (C - L) / (H - L)
    assert abs(F["CLV10"][k] - clv[k - 9:k + 1].mean()) < 1e-12
    assert abs(F["CLV_FARK"][k] - (clv[k - 9:k + 1].mean() - clv[k - 39:k - 9].mean())) < 1e-12
    assert abs(F["MOM_12_1"][k] - (C[k - 21] / C[k - 252] - 1)) < 1e-12 and np.isnan(F["MOM_12_1"][251])
    r = (H - L) / C
    assert abs(F["BOY_YUZDE_ORAN"][k] - np.median(r[k - 15:k + 1]) / np.median(r[k - 135:k - 15])) < 1e-12
    assert abs(F["ONCEKI_DUSUS"][k] - (L[k - 15:k + 1].min() / H[k - 75:k - 15].max() - 1)) < 1e-12


@t
def test_yukselen_dip_elle():
    m = 80; L = np.full(m, 20.0)
    for i, v in ((30, 10.0), (40, 11.0), (50, 12.0), (60, 11.5), (70, 13.0)):
        L[i] = v
    C = L + 2; H = L + 3
    F = _oz(C, H, L, C)
    # k = 79: pencere [22, 77] dipler 30 (10), 40 (11), 50 (12), 60 (11,5), 70 (13): son dipten geri: 13 > 11,5 (1), 11,5 < 12 kırar -> 1
    assert F["YUKSELEN_DIP"][79] == 1
    L2 = L.copy(); L2[60] = 12.5; F2 = _oz(C, H, L2, C)
    assert F2["YUKSELEN_DIP"][79] == 4          # 10 < 11 < 12 < 12,5 < 13
    # k = 71: 70 barının dibi henüz bilinmiyor (i + 2 <= k şartı) -> son dip 60
    assert F2["YUKSELEN_DIP"][71] == 3
    # pencere sınırı: k = 89 -> pencere [32, 87]: 30 barı dışarıda -> dipler 40, 50, 60, 70 -> 3
    L3 = np.r_[L2, np.full(10, 20.0)]; F3 = _oz(L3 + 2, L3 + 3, L3, L3 + 2)
    assert F3["YUKSELEN_DIP"][89] == 3


@t
def test_gelecege_bakma_yok():
    D = _seri(400, 9); O, H, L, C = (D[c].to_numpy() for c in ("Open", "High", "Low", "Close")); Lp = np.exp(np.cumsum(np.random.default_rng(2).normal(0, 0.01, 400)))
    F = _oz(O, H, L, C, Lp); k = 330
    r = np.random.default_rng(7); O2, H2, L2, C2 = O.copy(), H.copy(), L.copy(), C.copy()
    f = np.exp(r.normal(0, 0.2, 400 - k - 1)); C2[k + 1:] *= f; O2[k + 1:] *= f[::-1]; H2[k + 1:] = np.maximum(O2[k + 1:], C2[k + 1:]) * 1.05; L2[k + 1:] = np.minimum(O2[k + 1:], C2[k + 1:]) * 0.9
    Lp2 = Lp.copy(); Lp2[k + 1:] *= 3
    F2 = _oz(O2, H2, L2, C2, Lp2)
    for a in YO.YO_OZ + ["_oyn60", "_u20", "_u50", "_u200", "_d20", "_z60", "_d60", "_r20"]:
        if a not in F:
            continue
        x, y = F[a][:k + 1], F2[a][:k + 1]
        assert np.array_equal(np.isnan(x), np.isnan(y)) and np.allclose(x[np.isfinite(x)], y[np.isfinite(y)], rtol=0, atol=1e-12), a
    # kısaltılmış seri de aynı
    F3 = _oz(O[:k + 1], H[:k + 1], L[:k + 1], C[:k + 1], Lp[:k + 1])
    for a in YO.YO_OZ:
        if a in F:
            x, y = F[a][:k + 1], F3[a]
            assert np.array_equal(np.isnan(x), np.isnan(y)) and np.allclose(x[np.isfinite(x)], y[np.isfinite(y)], atol=1e-12), a


@t
def test_ornek_her_5_bar():
    n = 200; idx = pd.bdate_range("2015-10-01", periods=n); pos = np.arange(n); p2 = np.ones(n, bool)
    k = YO.yo_ornek_maske(n, pos, p2, idx)
    assert (k % 5 == 0).all() and (np.diff(k) == 5).all()
    assert (idx[pos[k + 1]] >= pd.Timestamp("2016-01-01")).all() and k.max() + 15 <= n - 1
    p2b = p2.copy(); p2b[k[3] + 1] = False
    assert k[3] not in YO.yo_ornek_maske(n, pos, p2b, idx)
    pos2 = pos.copy(); pos2[k[5] + 1:] += 11                       # giriş boşluğu 12 satır > 10
    assert k[5] not in YO.yo_ornek_maske(n, pos2, np.ones(n + 20, bool), pd.bdate_range("2015-10-01", periods=n + 20))


# ---------------------------------------------------------------- istatistik
@t
def test_kat_atrp_ici_elle():
    # iki beşlik: q0 oran 0,1 (100 satır), q1 oran 0,5 (100); uç: q1'den 20 satır, 12'si Y = 1 -> O = 12, E = 20 x 0,5 = 10 -> KAT 1,2; ham KAT = 0,6 / 0,3 = 2
    q = np.r_[np.zeros(100, int), np.ones(100, int)]; Y = np.r_[np.r_[np.ones(10), np.zeros(90)], np.r_[np.ones(50), np.zeros(50)]]
    uc = np.zeros(200, bool); uc[100:112] = True; uc[160:168] = True          # 12 Y = 1 + 8 Y = 0
    D = np.zeros(200); TF = np.zeros(200); ay = np.array([f"2017-{1 + i % 12:02d}" for i in range(200)])
    o = YO.yo_olc(uc, q, Y, D, TF, ay, "test", B=300, nq=2)
    assert o["n"] == 20 and abs(o["KAT"] - 1.2) < 1e-12 and abs(o["KAT_HAM"] - 2.0) < 1e-12
    assert abs(o["ASIMETRI"] - (0.6 - 0.5)) < 1e-12 and o["KAT_alt"] <= o["KAT"] <= o["KAT_ust"]
    o2 = YO.yo_olc(uc, q, Y, D, TF, ay, "test", B=300, nq=2)
    assert o2["KAT_alt"] == o["KAT_alt"] and o2["p"] == o["p"]


@t
def test_bootstrap_ay_kumeli():
    x = np.r_[np.full(50, 1.0), np.full(50, 3.0)]; ay = np.r_[np.full(50, "2017-01"), np.full(50, "2017-02")]
    b = YO.yo_boot_ort(x, ay, "a", B=2000)
    assert b["ort"] == 2.0 and b["alt"] == 1.0 and b["ust"] == 3.0          # iki küme: yeniden örnekleme yalnız 1, 2, 3
    c = YO.yo_boot_ort(np.full(30, 2.5), np.array([f"2018-{1 + i % 6:02d}" for i in range(30)]), "b", B=500)
    assert c["alt"] == c["ust"] == 2.5
    assert YO.yo_boot_ort(x, ay, "a", B=2000) == b
    k1, W1 = YO.yo_ay_W(ay, "z", 50); k2, W2 = YO.yo_ay_W(ay, "z", 50)
    assert np.array_equal(W1, W2) and (W1.sum(1) == 2).all()


@t
def test_bh():
    q = YO.yo_bh([0.01, 0.04, 0.03, 0.20, None], 0.10)
    assert abs(q[0] - 0.04) < 1e-12 and abs(q[1] - 0.04 * 4 / 3 * 1.0) < 1e-12 or abs(q[1] - 0.0533333) < 1e-6
    assert q[4] is None and abs(q[3] - 0.20) < 1e-12


@t
def test_esle_tohum():
    rng = np.random.default_rng(1); n = 3000
    tr = rng.integers(0, 30, n); q = rng.integers(0, 5, n); Y = (rng.random(n) < 0.1).astype(float)
    ev, ct = YO.yo_esle(tr, q, Y); ev2, ct2 = YO.yo_esle(tr, q, Y)
    assert np.array_equal(ev, ev2) and np.array_equal(ct, ct2) and len(ev) == int(Y.sum())
    for i, row in zip(ev, ct):
        r = row[row >= 0]
        assert len(r) == 5 and (tr[r] == tr[i]).all() and (q[r] == q[i]).all() and (Y[r] == 0).all() and len(set(r)) == 5


@t
def test_besli_ve_uc():
    s = [1.0, 2.0, 3.0, 4.0]
    assert YO.yo_besli(np.array([0.5, 1.0, 1.5, 4.0, 4.5, np.nan]), s).tolist() == [0, 0, 1, 3, 4, -1]
    x = np.array([1.0, 2.0, 3.0, np.nan])
    assert YO.yo_uc_maske(x, "F15", "BÜYÜK", 2.0).tolist() == [False, True, True, False]
    assert YO.yo_uc_maske(x, "F15", "KÜÇÜK", 2.0).tolist() == [True, True, False, False]
    assert YO.yo_uc_maske(np.array([0.0, 1.0, 3.0]), "MA_KOD", "BÜYÜK", None).tolist() == [False, False, True]
    assert YO.yo_uc_maske(np.array([0.0, 1.0, 3.0]), "MA_KOD", "KÜÇÜK", None).tolist() == [True, False, False]


@t
def test_kesim_yalniz_kesif():
    X = pd.DataFrame({"hucre": ["ABD|d1619"] * 100, "F15": np.arange(100.0)})
    k = YO.yo_kesim_belirle(X, "F15", "BÜYÜK")
    assert abs(k["0.10"] - np.quantile(np.arange(100.0), 0.9)) < 1e-12
    for h in ("ABD|d2022", "AVR|d1619"):
        Xb = X.copy(); Xb.loc[0, "hucre"] = h
        try:
            YO.yo_kesim_belirle(Xb, "F15", "BÜYÜK")
        except YO.YOHata:
            pass
        else:
            raise AssertionError("kesim keşif dışı satırla belirlendi")


@t
def test_adim1_sonuc_kapisi():
    X = pd.DataFrame({"hucre": ["ABD|d1619", "ABD|d2022"], "j": [0, 0], "k": [0, 5], "d_row": [1, 6]}); G = pd.DataFrame({"hucre": ["ABD|d1619"], "d_row": [1]})
    for XX, pz in ((X, "ABD"), (X.iloc[:1], "AVR")):
        try:
            YO.yo_sonuc(pz, XX, G, "adim1", depo={})
        except YO.YOHata as ex:
            assert "SIRA" in str(ex)
        else:
            raise AssertionError("ADIM 1 doğrulama sonucunu açtı")


@t
def test_kesik_assert():
    ok = {"A": pd.DataFrame({"Close": [1.0]}, index=pd.to_datetime(["2022-12-30"]))}
    assert YO.yo_kesik_kapi(ok) == pd.Timestamp("2022-12-30")
    try:
        YO.yo_kesik_kapi({"A": pd.DataFrame({"Close": [1.0]}, index=pd.to_datetime(["2023-01-02"]))})
    except YO.YOHata as ex:
        assert "KESİK" in str(ex)
    else:
        raise AssertionError("kesik aşımı durmadı")


@t
def test_logit():
    rng = np.random.default_rng(3); n = 20000; x = rng.normal(size=(n, 2)); p = 1 / (1 + np.exp(-(-1 + 0.8 * x[:, 0])))
    y = (rng.random(n) < p).astype(float); X = np.c_[np.ones(n), x]
    w = YO.yo_logit_newton(X, y)
    assert abs(w[1] - 0.8) < 0.08 and abs(w[2]) < 0.06 and abs(w[0] + 1) < 0.08
    w1 = YO.yo_logit_l1(X, y, 0.01, 400)
    assert w1[2] == 0.0 and 0.5 < w1[1] < 0.85


# ---------------------------------------------------------------- uçtan uca sentetik
def _sentetik_pazar(pazar, u=40, n=1950, tohum=0):
    idx = pd.bdate_range("2015-01-02", "2022-12-30")[:n]; V = {}
    for j in range(u):
        D = _seri(len(idx), tohum * 1000 + j, son=str(idx[-1].date()), s=0.01 + 0.03 * (j % 5) / 4)
        D.index = idx
        if j % 7 == 3:
            D = D.iloc[:-5]                                    # bazıları erken biter
        V[f"{pazar}{j:03d}"] = D
    S = sorted(V); pos_l, O_l, H_l, L_l, C_l, off = [], [], [], [], [], [0]
    for s in S:
        p = idx.get_indexer(V[s].index); pos_l.append(p); off.append(off[-1] + len(p))
        for l_, c in ((O_l, "Open"), (H_l, "High"), (L_l, "Low"), (C_l, "Close")):
            l_.append(V[s][c].to_numpy(float))
    dep = {"O": np.concatenate(O_l), "H": np.concatenate(H_l), "L": np.concatenate(L_l), "C": np.concatenate(C_l), "POS": np.concatenate(pos_l).astype(np.int64),
           "off": np.array(off, np.int64)}
    dep["m"] = np.diff(dep["off"])
    Op = pd.DataFrame({s: V[s].Open for s in S}).reindex(idx).to_numpy(float); Cl = pd.DataFrame({s: V[s].Close for s in S}).reindex(idx).to_numpy(float)
    P2 = np.isfinite(Op) & (np.arange(len(idx))[:, None] >= 80)
    Pn = {"tarih": idx, "sembol": S, "dep": dep, "Op": Op, "Cl": Cl}
    return {"V": V}, Pn, P2


def test_uctan_uca_sentetik():
    with tempfile.TemporaryDirectory() as td:
        XS, GS, SS, SG = {}, {}, {}, {}
        for i, p in enumerate(YO.YO_PAZAR):
            Vd, Pn, P2 = _sentetik_pazar(p, tohum=i)
            r = YO.yo_hazirla_pazar(p, td, Vd, Pn, P2)
            assert r["hisse_gun"] > 1000
            X, G = YO.yo_yukle(p, td)
            assert not any(c in X.columns for c in ("Y10", "R15", "P15")) and set(X.hucre.unique()) <= set(YO.YO_HUCRE)
            assert (X.k % 5 == 0).all() and (X.giris > X.tarih).all()
            XS[p], GS[p] = X, G
        S = YO.yo_sayim(XS, GS)
        assert set(S["hisse"]) == set(YO.YO_HUCRE) and "Y10" not in str(S["hisse"])
        assert YO.HV.hv_json_sha(S) == YO.HV.hv_json_sha(YO.yo_sayim_kos(td))
        for p in YO.YO_PAZAR:
            SS[p], SG[p] = YO.yo_sonuc(p, XS[p], GS[p], "test", td)
            assert set(SS[p].columns) >= {"Y10", "Y5", "D10", "R15", "KALICI", "P15"} and SS[p].Y10.notna().all()
        Xk = XS["ABD"][XS["ABD"].hucre == YO.YO_KESIF].reset_index(drop=True); Gk = GS["ABD"][GS["ABD"].hucre == YO.YO_KESIF].reset_index(drop=True)
        Sk, Sgk = YO.yo_sonuc("ABD", Xk, Gk, "adim1", td)
        m = (XS["ABD"].hucre == YO.YO_KESIF).to_numpy()
        assert np.allclose(Sk.R15.to_numpy(), SS["ABD"].R15.to_numpy()[m])
        XA = XS["AVR"][XS["AVR"].hucre == "AVR|d1619"].reset_index(drop=True); GA = GS["AVR"][GS["AVR"].hucre == "AVR|d1619"].reset_index(drop=True)
        try:
            YO.yo_adim1_hesap(XS["ABD"], SS["ABD"], Gk, Sgk, XA, GA, B=100)
        except YO.YOHata:
            pass
        else:
            raise AssertionError("ADIM 1 doğrulama satırını kabul etti")
        K = YO.yo_adim1_hesap(Xk, Sk, Gk, Sgk, XA, GA, B=100)
        K = YO.MI._mi_json(K); K = __import__("json").loads(__import__("json").dumps(K))
        assert set(K["yon"]) == set(YO.YO_OZ) and len(K["kesif_olc"]) == 40 and len(K["atrp_besli"]["ABD"]) == 4
        J = YO.yo_adim2_hesap(XS, SS, GS, SG, K, B=100)
        assert len(J["satir"]) == 40 and all(r["hukum"] in ("TUTAR", "YALNIZ OYNAKLIK", "TEK DÖNEM", "TERS", "TUTMADI", "ÖLÇÜLEMEDİ") for r in J["satir"].values())
        assert all(r["hukum"] == "ÖLÇÜLEMEDİ" for r in J["satir"].values() if r["olc"]["ABD|d2022"].get("n", 0) < 1000)
        assert len(J["piyasa"]) == 32 and set(J["puan"]) == {"0.10", "0.02"}
        yol = YO.yo_ozet_csv(J, K, os.path.join(td, "o.csv")); D = pd.read_csv(yol)
        assert len(D) >= 40 * 4 and {"KAT", "ASIMETRI", "TOPLAM_FARK", "hukum"} <= set(D.columns)
        # ATRP içi KAT bağımsız yeniden üretim (bir satır, keşif)
        a = "F15|0.10"; o = J["satir"][a]["olc"][YO.YO_KESIF]
        x = Xk; v = x.F15.to_numpy(float); pop = np.isfinite(v) & np.isfinite(x.ATRP20.to_numpy(float))
        qq = np.searchsorted(K["atrp_besli"]["ABD"], x.ATRP20.to_numpy(float)); thr = K["kesim"]["ABD"]["F15"]["0.10"]
        uc = (v >= thr if K["yon"]["F15"]["yon"] == "BÜYÜK" else v <= thr) & pop; y = Sk.Y10.to_numpy(float)
        pq = {i: y[pop & (qq == i)].mean() for i in range(5)}
        E = sum(pq[i] for i in qq[uc]); assert abs(y[uc].sum() / E - o["KAT"]) < 1e-9 and o["n"] == int(uc.sum())


@t
def test_cakisma_kapisi():
    kod = open(os.path.join(os.path.dirname(os.path.abspath(YO.__file__)), "YUKSELIS_ONCESI.py"), encoding="utf-8").read()
    ns = {"__name__": "yo_test", "__file__": YO.__file__}
    exec(compile(kod, "YUKSELIS_ONCESI.py", "exec"), ns)          # temiz ad alanı: geçer
    ns2 = {"__name__": "yo_test2", "__file__": YO.__file__, "yo_kapi": 1}
    try:
        exec(compile(kod, "YUKSELIS_ONCESI.py", "exec"), ns2)
    except RuntimeError as ex:
        assert "çakışma" in str(ex)
    else:
        raise AssertionError("çakışma kapısı çalışmadı")


@t
def test_esik_sabit():
    E = YO.YO_ESIK
    assert E["tohum"] == 28 and E["boot"]["B"] == 10000 and E["kesim"]["uc"] == [0.10, 0.02] and E["hukum"]["n_min"] == 1000 and E["bh"]["q"] == 0.10
    assert E["yukselis"]["Y10"] == [0.10, 0.05] and E["yukselis"]["D10"] == [0.10, 0.05] and E["yukselis"]["ufuk"] == 15 and E["ornek"]["adim"] == 5
    assert len(YO.YO_OZ) == 21 and len(YO.YO_PIYASA_OZ) == 16 and set(YO.YO_KONTROL) == {f"K{i}" for i in range(1, 15)}


# ================================================================ EK 2 (YO2): haftalık geriye doğru doğrulama
def _wdf(O, H, L, C, bas=None, bosluk=None, son="2010-12-31"):
    m = len(C); ix = pd.date_range(end=son, periods=m, freq="W-FRI")
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1.0}, index=ix)
    d["bas"] = ix - pd.Timedelta(days=4) if bas is None else bas; d["n_gun"] = 5
    d["bosluk"] = np.zeros(m, bool) if bosluk is None else bosluk
    return d


@t
def test_yo2_sonuc_elle():
    O = np.array([10, 10, 10, 10, 10, 10, 10.]); H = np.array([11, 11, 11, 10.2, 10.6, 10.3, 10.3]); L = np.array([9.5, 9, 9.4, 9.6, 9.7, 9.6, 9.6])
    C = np.array([10, 10, 10, 10, 10.4, 10.2, 10.])
    R = YO.yo2_sonuc_dizi(_dep(O, H, L, C), np.array([0]), np.array([2]))
    assert R["E0"][0] == 10 and R["Y5"][0] == 1.0 and abs(R["R3"][0] - (10.2 / 10 - 1)) < 1e-12 and R["KOTU20"][0] == 0.0
    L2 = L.copy(); L2[3] = 8.81                       # stop = 9 x 0,98 = 8,82: ilk hafta stop, hedef 2. hafta -> 0
    assert YO.yo2_sonuc_dizi(_dep(O, H, L2, C), np.array([0]), np.array([2]))["Y5"][0] == 0.0
    H3 = H.copy(); H3[3] = 10.6                       # aynı hafta hedef + stop -> stop önce -> 0
    assert YO.yo2_sonuc_dizi(_dep(O, H3, L2, C), np.array([0]), np.array([2]))["Y5"][0] == 0.0
    L4 = L.copy(); L4[4] = 8.83                       # stop seviyesinin hemen üstü: stop yok -> 1
    assert YO.yo2_sonuc_dizi(_dep(O, H, L4, C), np.array([0]), np.array([2]))["Y5"][0] == 1.0
    C5 = C.copy(); C5[5] = 7.9                        # R3 = -%21 -> KOTU20
    r5 = YO.yo2_sonuc_dizi(_dep(O, H, L, C5), np.array([0]), np.array([2]))
    assert r5["KOTU20"][0] == 1.0 and abs(r5["R3"][0] + 0.21) < 1e-12
    try:
        YO.yo2_sonuc_dizi(_dep(O, H, L, C), np.array([0]), np.array([4])); raise AssertionError("pencere aşımı yakalanmadı")
    except YO.YOHata:
        pass


@t
def test_yo2_ozellik_elle():
    r = np.random.default_rng(5); m = 40
    C = 10 + np.cumsum(r.normal(0, 0.3, m)); H = C + r.uniform(0.1, 1, m); L = C - r.uniform(0.1, 1, m)
    F = YO.yo2_ozellik(H, L, C)
    for i in (14, 20, 39):
        assert abs(F["DUSUS_W"][i] - (L[i - 2:i + 1].min() / H[i - 14:i - 2].max() - 1)) < 1e-12
        rr = (H - L) / C; ref = rr[max(0, i - 26):i - 2]
        assert abs(F["BOY_W"][i] - np.median(rr[i - 2:i + 1]) / np.median(ref)) < 1e-12
    assert np.isnan(F["DUSUS_W"][13]) and np.isnan(F["BOY_W"][13])
    assert F["U40"][39] == float(C[39] > C[:40].mean()) and np.isnan(F["U40"][38])


@t
def test_yo2_gelecege_bakma_yok():
    r = np.random.default_rng(7); m = 80
    C = 10 * np.exp(np.cumsum(r.normal(0, 0.05, m))); H = C * 1.05; L = C * 0.95
    F = YO.yo2_ozellik(H, L, C); k = 50; H2, L2, C2 = H.copy(), L.copy(), C.copy()
    H2[k + 1:] *= 3; L2[k + 1:] *= 0.2; C2[k + 1:] *= 1.7
    F2 = YO.yo2_ozellik(H2, L2, C2)
    for a in F:
        assert np.allclose(F[a][:k + 1], F2[a][:k + 1], equal_nan=True)


@t
def test_yo2_ornek_maske():
    m = 30; d = _wdf(np.ones(m) * 10, np.ones(m) * 11, np.ones(m) * 9, np.ones(m) * 10)
    ev = np.ones(m, bool); i = YO.yo2_ornek_maske(d, ev)
    assert i.min() == 2 and i.max() == m - 4
    b = np.zeros(m, bool); b[10] = True; d2 = d.copy(); d2["bosluk"] = b
    i2 = YO.yo2_ornek_maske(d2, ev)
    assert not set(range(7, 12)) & set(i2.tolist()) and {6, 12} <= set(i2.tolist())     # bosluk[10] -> i = 7..11 atılır
    ev2 = ev.copy(); ev2[15] = False
    assert 15 not in set(YO.yo2_ornek_maske(d, ev2).tolist())
    d3 = _wdf(np.ones(m) * 10, np.ones(m) * 11, np.ones(m) * 9, np.ones(m) * 10, son="2000-03-31")
    assert all(pd.DatetimeIndex(d3.bas)[j + 1] >= pd.Timestamp("2000-01-01") for j in YO.yo2_ornek_maske(d3, ev))


@t
def test_yo2_kesim_yalniz_2016_22():
    r = np.random.default_rng(3); n = 4000
    gir = pd.to_datetime(r.choice(pd.date_range("2000-01-07", "2022-12-02", freq="W-MON"), n))
    X = pd.DataFrame({"giris": gir, "DUSUS_W": r.normal(-0.1, 0.1, n), "BOY_W": r.lognormal(0, 0.3, n)}); X["donem"] = YO.yo2_donem(X.giris)
    G = pd.DataFrame({"giris": pd.date_range("2000-01-03", "2022-12-05", freq="W-MON")}); G["G40"] = r.uniform(0, 1, len(G)); G["donem"] = YO.yo2_donem(G.giris)
    K = YO.yo2_kesim({"ABD": X}, {"ABD": G})
    m = X.donem.isin(YO.YO2_KESIM_DONEM)
    assert abs(K["ABD"]["DUSUS_W"] - np.quantile(X.DUSUS_W[m], 0.10)) < 1e-12 and abs(K["ABD"]["G40"] - np.quantile(G.G40[G.donem.isin(YO.YO2_KESIM_DONEM)], 0.10)) < 1e-12
    X2 = X.copy(); X2.loc[~m, "DUSUS_W"] = -5.0; X2.loc[~m, "BOY_W"] = 0.0           # 2000-2015 değişir -> kesim aynı
    G2 = G.copy(); G2.loc[~G.donem.isin(YO.YO2_KESIM_DONEM), "G40"] = 0.0
    assert YO.HV.hv_json_sha(YO.yo2_kesim({"ABD": X2}, {"ABD": G2})) == YO.HV.hv_json_sha(K)
    for kol in ("R3", "Y5", "P3"):
        try:
            YO.yo2_kesim({"ABD": X.assign(**{kol: 0.0})}, {"ABD": G}); raise AssertionError("sonuç sütunlu kesim yakalanmadı")
        except YO.YOHata:
            pass


@t
def test_yo2_sonuc_kapisi():
    X = pd.DataFrame({"donem": ["a0007", "d1619"], "j": [0, 0], "i": [2, 3]}); G = pd.DataFrame({"donem": ["d1619"]})
    for asama, x in (("kesim", X), ("sayim", X), ("adim0", X), ("adim1", X), ("adim1", X[X.donem == "d1619"])):
        try:
            YO.yo2_sonuc("ABD", x, G, asama, depo={}); raise AssertionError(f"izin dışı sonuç yakalanmadı: {asama}")
        except YO.YOHata as ex:
            assert "SIRA" in str(ex)


@t
def test_yo2_bootstrap_tohum():
    ce = np.array(["2001-Q1", "2001-Q2", "2001-Q1", "2002-Q4"]); k, W, u = YO.yo2_W(ce, 50); k2, W2, _ = YO.yo2_W(ce, 50)
    assert np.array_equal(W, W2) and list(u) == ["2001-Q1", "2001-Q2", "2002-Q4"] and np.allclose(W.sum(1), 3)
    assert np.array_equal(W, np.random.default_rng(2000).multinomial(3, np.full(3, 1 / 3), size=50).astype(float))
    assert list(YO.yo2_ceyrek(pd.to_datetime(["2003-02-03", "2003-12-29", "2008-07-07"]))) == ["2003-Q1", "2003-Q4", "2008-Q3"]
    # çeyrek kümeli ortalama: tek kümede tüm uçlar -> aralık nokta değerde
    x = np.array([-0.5, -0.4, 0.1, 0.2, 0.3]); S = pd.DataFrame({"R3": [0.1, 0.2, 0, 0, 0.], "TF": [0.05, 0.15, 0, 0, 0], "Y5": [1, 0, 0, 0, 0.],
                                                                "p_h": [0.5] * 5, "KOTU20": [0.] * 5, "q_h": [0.1] * 5})
    o = YO.yo2_olc_hisse(x, -0.3, S, np.array(["2001-Q1", "2001-Q1", "2001-Q2", "2001-Q3", "2001-Q4"]), 200)
    assert o["n"] == 2 and abs(o["TOPLAM_FARK"] - 0.10) < 1e-12 and abs(o["KAT"] - 1.0) < 1e-12 and o["ceyrek"] == 1
    assert abs(o["TOPLAM_FARK_alt"] - 0.10) < 1e-12 and abs(o["TOPLAM_FARK_ust"] - 0.10) < 1e-12


@t
def test_yo2_obek_ve_piyasa():
    assert YO.yo2_obek(np.array([100, 101, 105, 114, 115, 140])) == [(100, 105), (114, 115), (140, 140)]   # 105 -> 114 fark 9: yeni öbek
    assert YO.yo2_obek(np.array([100, 108])) == [(100, 108)]                                             # fark 8 (arada 7 hafta): aynı öbek
    g = np.array([0.05, 0.5, 0.6, 0.04, 0.7, 0.8]); v = np.array([0.06, 0.01, -0.06, 0.02, 0.0, 0.01]); h = np.array([10, 11, 12, 30, 31, 32])
    o = YO.yo2_olc_piyasa(g, 0.1, v, h, np.array(["2001-Q1"] * 3 + ["2001-Q3"] * 3), 100)
    assert o["n_dusuk"] == 2 and o["obek"] == 2 and abs(o["FARK"] - (0.04 - (-0.04 / 4))) < 1e-12
    assert abs(o["P5_dusuk"] - 0.5) < 1e-12 and abs(o["M5_oteki"] - 0.25) < 1e-12


@t
def test_yo2_2023_assert():
    try:
        YO.yo2_donem(pd.to_datetime(["2022-12-30", "2023-01-02"])); raise AssertionError("2023 girişi yakalanmadı")
    except YO.YOHata:
        pass
    m = 60; d = _wdf(np.ones(m) * 10, np.ones(m) * 11, np.ones(m) * 9, np.ones(m) * 10, son="2023-01-13")
    with tempfile.TemporaryDirectory() as td:
        try:
            YO.yo2_hazirla_pazar("ABD", td, W={"A": d}, evren={"A": np.ones(m, bool)}); raise AssertionError("kesik aşımı yakalanmadı")
        except YO.YOHata as ex:
            assert "KESİK" in str(ex)


@t
def test_yo2_eski_ciktilar_degismedi():
    import hashlib
    import subprocess
    kok = os.path.dirname(os.path.abspath(YO.__file__))
    for ad in YO.YO_DOSYA.values():
        yol = os.path.join("arastirma_cikti", "yukselis_oncesi", ad)
        eski = subprocess.run(["git", "show", f"{YO.YO2_ESKI_SHA_COMMIT}:{yol}"], cwd=kok, capture_output=True).stdout
        assert eski and hashlib.sha256(eski).hexdigest() == hashlib.sha256(open(os.path.join(kok, yol), "rb").read()).hexdigest(), ad
    for ad in YO.YO2_DOSYA:
        assert os.path.basename(YO._yo2_yol(ad)) not in set(YO.YO_DOSYA.values())


@t
def test_yo2_endeks():
    with tempfile.TemporaryDirectory() as td:
        assert YO.yo2_endeks_durum(td)["durum"] == "YOK"
        t_ = pd.bdate_range("2001-01-01", "2005-12-30"); r = np.random.default_rng(2); c = 100 * np.exp(np.cumsum(r.normal(0, 0.01, len(t_)))); o = c * 0.999
        pd.DataFrame({"date": t_.strftime("%Y-%m-%d"), "adjOpen": o, "adjClose": c}).to_csv(os.path.join(td, "SPY.csv"), index=False)
        assert YO.yo2_endeks_durum(td)["durum"] == "VAR"
        hn = YO.yo2_hno(t_); w = int(hn[100]); G = pd.DataFrame({"hno": [w]})
        a = np.flatnonzero(hn == w + 1)[0]; b = np.flatnonzero(hn == w + 3)[-1]
        assert abs(YO.yo2_endeks_R3(G, td)[0] - (c[b] / o[a] - 1)) < 1e-12


@t
def test_yo2_uctan_uca_sentetik():
    import MUM_IZI_V2 as MV
    r = np.random.default_rng(11); ix = pd.bdate_range("2000-01-03", "2022-12-30"); n = len(ix); W = {}
    for k in range(40):
        C = 20 * np.exp(np.cumsum(r.normal(0, 0.02, n))); O = C * np.exp(r.normal(0, 0.005, n))
        H = np.maximum(O, C) * (1 + np.abs(r.normal(0, 0.01, n))) + 1e-6; L = np.minimum(O, C) * (1 - np.abs(r.normal(0, 0.01, n)))
        W[f"S{k:02d}"] = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1000.0}, index=ix)
    WP = MV.mv_haftalik_panel(W); ev = {s: np.ones(len(d), bool) for s, d in WP.items()}
    with tempfile.TemporaryDirectory() as td:
        for p in YO.YO2_PAZAR:
            YO.yo2_hazirla_pazar(p, td, W=WP, evren=ev)
        S, K = YO.yo2_sayim_kos(td); S2, K2 = YO.yo2_sayim_kos(td)
        assert YO.HV.hv_json_sha(S) == YO.HV.hv_json_sha(S2) and S["yil"]["ABD"]["2010"]["evren_hisse"] == 40
        X, G = YO.yo2_yukle("ABD", td)
        assert X.giris.min() >= pd.Timestamp("2000-01-01") and X.giris.max() <= pd.Timestamp("2022-12-31") and set(X.donem) == set(YO.YO2_DONEM)
        Sx, Sg = YO.yo2_sonuc("ABD", X, G, "test", td, endeks=False)
        # P3 bir hafta için elle
        w = int(G.hno.iloc[300]); m = (X.hno == w).to_numpy()
        assert abs(Sg.P3.iloc[300] - Sx.R3[m].mean()) < 1e-12
        # T1 bir hisse-dönem için elle
        q = (X.sembol == "S03") & (X.donem == "a0815"); assert abs(Sx.T1[q].iloc[0] - Sx.R3[q].mean()) < 1e-12
        # R3 bir satır için doğrudan haftalık barlardan
        row = X.iloc[5000]; d = WP[row.sembol]; i = int(row.i)
        assert abs(Sx.R3.iloc[5000] - (d.Close.iloc[i + 3] / d.Open.iloc[i + 1] - 1)) < 1e-12 and row.giris == d.bas.iloc[i + 1]
        XS = {"ABD": X[X.donem.isin(YO.YO2_SINAMA_DONEM)].reset_index(drop=True)}; GS = {"ABD": G[G.donem.isin(YO.YO2_SINAMA_DONEM)].reset_index(drop=True)}
        SS, SG = YO.yo2_sonuc("ABD", XS["ABD"], GS["ABD"], "adim1", td, endeks=False)
        A = YO.yo2_adim_hesap(XS, GS, {"ABD": SS}, {"ABD": SG}, K, YO.YO2_SINAMA_DONEM, B=200)
        h1 = YO.yo2_hukum_hisse("H1", A["ABD"]["H1"]["tum"], {d: A["ABD"]["H1"][d] for d in YO.YO2_SINAMA_DONEM}, True)
        assert h1 in ("ÖLÇÜLEMEDİ", "TERS", "GÖSTERİLEMEDİ", "YAŞAYAN EVRENDE DOĞRULANDI (batanlar yok)")
        assert YO.yo2_hukum_piyasa(A["ABD"]["H3"]["P3"]["tum"], False, True) == "ENDEKS YOK: ÖLÇÜLEMEDİ"
        assert YO.yo2_hukum_hisse("H2", {"n": 10}, {}, False).startswith("ÖLÇEK UYMADI | ÖLÇÜLEMEDİ")


@t
def test_yo2_hukum_kurali():
    alt_p = {"a0007": {"TOPLAM_FARK": 0.01}, "a0815": {"TOPLAM_FARK": 0.002}}
    tum = {"n": 5000, "ceyrek": 60, "TOPLAM_FARK": 0.005, "TOPLAM_FARK_alt": 0.001, "TOPLAM_FARK_ust": 0.009}
    assert YO.yo2_hukum_hisse("H1", tum, alt_p, True) == "YAŞAYAN EVRENDE DOĞRULANDI (batanlar yok)"
    assert YO.yo2_hukum_hisse("H1", tum, {**alt_p, "a0815": {"TOPLAM_FARK": -0.001}}, True) == "GÖSTERİLEMEDİ"
    assert YO.yo2_hukum_hisse("H1", {**tum, "TOPLAM_FARK_alt": -0.001}, alt_p, True) == "GÖSTERİLEMEDİ"
    assert YO.yo2_hukum_hisse("H2", tum, alt_p, True) == "TERS"
    assert YO.yo2_hukum_hisse("H1", {**tum, "n": 999}, alt_p, True) == "ÖLÇÜLEMEDİ"
    o = {"n_dusuk": 40, "obek": 4, "FARK": 0.01, "FARK_alt": 0.002, "P5_FARK": 0.05}
    assert YO.yo2_hukum_piyasa(o, True, True) == "DOĞRULANDI" and YO.yo2_hukum_piyasa({**o, "obek": 3}, True, True) == "ÖLÇÜLEMEDİ"
    assert YO.yo2_hukum_piyasa({**o, "P5_FARK": -0.01}, True, True) == "GÖSTERİLEMEDİ" and YO.yo2_hukum_piyasa(o, False, True) == "ENDEKS YOK: ÖLÇÜLEMEDİ"
    E = YO.YO2_ESIK
    assert E["boot"]["tohum"] == 2000 and E["boot"]["B"] == 10000 and E["kesim"]["duzey"] == 0.10 and E["sonuc"] == {**E["sonuc"], "ufuk": 3, "hedef": 0.05,
                                                                                                                "stop_carpan": 0.98, "kotu": -0.20}
    assert set(YO.YO2_KONTROL) == {f"K{i}" for i in range(1, 15)}


t(test_uctan_uca_sentetik)


if __name__ == "__main__":
    bas = 0
    for f in ISIM:
        try:
            f(); print("GEÇTİ", f.__name__)
        except Exception as ex:  # noqa: BLE001
            bas += 1; print("KALDI", f.__name__, type(ex).__name__, ex)
    print(f"{len(ISIM) - bas} / {len(ISIM)} geçti")
    sys.exit(1 if bas else 0)
