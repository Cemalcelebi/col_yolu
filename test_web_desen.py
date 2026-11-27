"""test_web_desen — WEB_DESEN sentetik testleri (gerçek veri / sonuç görülmez; ağ yok).

Kapsam: her kolun yapay pozitif / 'yakın ama değil' negatif seti (gürültüsüz: yakalama >= %90, yanlış kabul <= %5); geleceğe bakma (giriş barından
sonraki barlar bozulunca ve seri kesilince olaylar aynı); yerel tepe / dibin ancak sağ iki barı tamamlanınca kullanılması; PL / PH yaşı; W3 / W4 / W5 giriş
fiyatı kuralları (seviyede giriş; açılış seviyeyi geçmişse açılışta; ulaşılmazsa olay yok); stop ve +2R 'önce hangisi' (aynı bar = stop önce); R katı
(boşluklu stop); 5 bar tekilleştirme; +2R tabanı kaba kuvvetle; T1 R15'i YO.yo_sonuc_dizi ile birebir; uçtan uca sentetik pazar (olay -> sonuç -> ölçüm ->
hüküm); kesik assert; çakışma kapısı; eşik sözlüğü sabit.
Çalıştır: python test_web_desen.py"""
import os
import sys

import numpy as np
import pandas as pd

import WEB_DESEN as WD
import YUKSELIS_ONCESI as YO

ISIM = []


def t(f):
    ISIM.append(f)
    return f


def _rw(n, tohum, oyn=0.012, P0=50.0):
    r = np.random.default_rng(tohum); C = P0 * np.exp(np.cumsum(r.normal(0, oyn, n))); O = C * np.exp(r.normal(0, oyn / 2, n))
    H = np.maximum(O, C) * (1 + np.abs(r.normal(0, oyn / 2, n))) + 1e-6; L = np.minimum(O, C) * (1 - np.abs(r.normal(0, oyn / 2, n)))
    V = r.lognormal(np.log(1e5), 0.6, n)
    return O, H, L, C, V


def _kol_sutun(D):
    return D[["kol", "ilk", "t", "e", "giris", "stop", "seviye", "atr"]].sort_values(["kol", "e", "ilk"]).reset_index(drop=True)


# ---------------------------------------------------------------- sentetik pozitif / negatif
@t
def test_sentetik_hedef():
    E = dict(WD.WD_ESIK["sentetik"]); E["tohum_sayi"] = 6
    for kol in WD.WD_KOLLAR:
        p = WD.wd_sentetik_olc(kol, "poz", 0.0, E)["pay"]
        assert p >= 0.90, f"{kol} yakalama {p}"
        for tip in WD.WD_YAPI[kol][2]:
            q = WD.wd_sentetik_olc(kol, tip, 0.0, E)["pay"]
            assert q <= 0.05, f"{kol} {tip} yanlış kabul {q}"


@t
def test_ayna_geometri():
    Y = WD.wd_yapay("W1", "poz", 100.0, 0.004, 1); Z = WD.wd_yapay("W1T", "poz", 100.0, 0.004, 1)
    assert Y["e"] == Z["e"] and Y["ilk"] == Z["ilk"]
    D, _ = WD.wd_tara(Z["O"], Z["H"], Z["L"], Z["C"], Z["V"], ["W1T"]); assert (D.e == Z["e"]).any() and (D.yon == -1).all()


# ---------------------------------------------------------------- geleceğe bakma
@t
def test_gelecege_bakma_bozma_ve_kesme():
    seriler = [_rw(500, s) for s in range(6)]
    for kol in ("W1", "W2", "W3", "W4", "W4Y", "W5", "W5Y", "W2E"):
        Y = WD.wd_yapay(kol, "poz", 50.0, 0.004, 2); seriler.append(tuple(Y[c] for c in ("O", "H", "L", "C", "V")))
    toplam = 0
    for O, H, L, C, V in seriler:
        Dt, _ = WD.wd_tara(O, H, L, C, V); m = len(C)
        for c in sorted(set([m // 3, m // 2, (2 * m) // 3] + [int(x) for x in Dt.e.unique() if 30 < x < m - 1][:15])):
            r = np.random.default_rng(c)
            O2, H2, L2, C2, V2 = (a.copy() for a in (O, H, L, C, V))
            k = slice(c + 1, None); n2 = m - c - 1
            C2[k] = C2[k] * np.exp(r.normal(0, 0.2, n2)); O2[k] = C2[k] * 1.01; H2[k] = np.maximum(O2[k], C2[k]) * 1.05; L2[k] = np.minimum(O2[k], C2[k]) * 0.95
            V2[k] = V2[k] * 7
            A = _kol_sutun(Dt[Dt.e <= c])
            B, _ = WD.wd_tara(O2, H2, L2, C2, V2); B = _kol_sutun(B[B.e <= c])
            pd.testing.assert_frame_equal(A, B, check_dtype=False)
            Pk, _ = WD.wd_tara(O[:c + 1], H[:c + 1], L[:c + 1], C[:c + 1], V[:c + 1]); Pk = _kol_sutun(Pk[Pk.e <= c])
            pd.testing.assert_frame_equal(A, Pk, check_dtype=False)
            toplam += len(A)
    assert toplam > 50


@t
def test_yerel_uc_sag_iki_bar():
    L = np.array([10, 9, 8, 7, 5, 6, 7, 8, 9, 10.0]); H = L + 1
    D, T = WD.wd_yerel(L, H)
    assert D[4] and D.sum() == 1
    son = WD.wd_son_uc(D, 3)
    assert son[6] == -1 and son[7] == 4            # i = 4 ancak s >= 7 (i + 2 <= s - 1) iken kullanılır
    # seri i + 1'de biterse yerel dip yoktur
    D2, _ = WD.wd_yerel(L[:6], H[:6]); assert not D2.any()


@t
def test_pl_yasi():
    L = np.r_[np.full(25, 10.0), [9.0], np.full(6, 10.0)]
    v, y = WD.wd_uc(L, 20, "min")
    assert v[26] == 9.0 and y[26] == 1 and y[29] == 4 and y[31] == 6
    L2 = L.copy(); L2[28] = 9.0                     # eşit uç: SON görülen
    v2, y2 = WD.wd_uc(L2, 20, "min"); assert y2[31] == 3


# ---------------------------------------------------------------- giriş fiyatı kuralları
def _w3_seri(o_e, h_e):
    O, H, L, C, V = (np.asarray(x, float) for x in _rw(60, 7, oyn=0.002, P0=100.0))
    L[30] = 95.0; O[30] = 96; C[30] = 96; H[30] = 96.5                       # PL
    for i in range(31, 40):
        O[i] = C[i] = 98.0; H[i] = 98.4; L[i] = 97.6
    O[40] = 98; C[40] = 94.0; L[40] = 93.5; H[40] = 98.2                      # C <= PL
    O[41] = o_e; H[41] = h_e; L[41] = min(o_e, 93.8); C[41] = max(min(h_e, 96.0), L[41] + 0.1)
    H[41] = max(H[41], O[41], C[41])
    return O, H, L, C, V


@t
def test_w3_giris():
    D, s = WD.wd_tara(*_w3_seri(94.2, 96.5), kollar=["W3"]); r = D[D.e == 41].iloc[0]
    assert r.giris == 95.0 and abs(r.stop - 93.5 * 0.999) < 1e-12 and r.seviye == 95.0
    D, _ = WD.wd_tara(*_w3_seri(95.6, 96.5), kollar=["W3"]); r = D[D.e == 41].iloc[0]
    assert r.giris == 95.6                                                    # açılış seviyenin üstünde -> açılışta
    D, s = WD.wd_tara(*_w3_seri(94.0, 94.9), kollar=["W3"])
    assert not (D.e == 41).any() and s["W3"].get("girissiz", 0) >= 1          # ulaşmadı -> olay yok


@t
def test_w4_giris():
    Y = WD.wd_yapay("W4", "poz", 100.0, 0.004, 0); e = Y["e"]
    D, _ = WD.wd_tara(Y["O"], Y["H"], Y["L"], Y["C"], Y["V"], ["W4"]); r = D[D.e == e].iloc[0]
    lv = r.seviye; assert r.giris == lv and Y["O"][e] < lv and r.stop == Y["H"][int(r.ilk)]
    assert Y["C"][int(r.bos)] < lv and int(r.bos) <= int(r.ilk) + 10 and e <= int(r.bos) + 5
    O = Y["O"].copy(); H = Y["H"].copy(); O[e] = lv + 0.3; H[e] = max(H[e], O[e])           # açılış seviyenin üstünde -> açılışta satış
    D2, _ = WD.wd_tara(O, H, Y["L"], Y["C"], Y["V"], ["W4"]); r2 = D2[D2.e == e].iloc[0]
    assert r2.giris == O[e]
    # yapı kırılımı olmadan geri test -> olay yok
    Yn = WD.wd_yapay("W4", "bos_yok", 100.0, 0.004, 0)
    D3, s3 = WD.wd_tara(Yn["O"], Yn["H"], Yn["L"], Yn["C"], Yn["V"], ["W4"])
    assert not ((D3.e >= Yn["ilk"]) & (D3.e <= Yn["e"] + 2)).any() and s3["W4"].get("bos_yok", 0) >= 1


@t
def test_w5_giris():
    Y = WD.wd_yapay("W5Y", "poz", 100.0, 0.004, 4)
    D, _ = WD.wd_tara(Y["O"], Y["H"], Y["L"], Y["C"], Y["V"], ["W5Y"]); r = D[D.e == Y["e"]].iloc[0]
    assert r.giris == Y["O"][Y["e"]] and r.stop == Y["L"][int(r.ilk):int(r.t) + 1].min() and Y["C"][int(r.ilk)] < r.seviye < Y["C"][int(r.t)]


# ---------------------------------------------------------------- önce hangisi / R katı
@t
def test_ilk_dokunma():
    H = np.array([[101, 105, 110.5, 100.0]]); L = np.array([[99, 99, 99, 99.0]])
    assert WD.wd_ilk_dokunma(H, L, [110.0], [95.0], [1])[0] == 1
    L2 = np.array([[99, 94.9, 99, 99.0]]); assert WD.wd_ilk_dokunma(H, L2, [110.0], [95.0], [1])[0] == 0
    H3 = np.array([[101, 111, 101, 101.0]]); L3 = np.array([[99, 94, 99, 99.0]]); assert WD.wd_ilk_dokunma(H3, L3, [110.0], [95.0], [1])[0] == 0   # aynı bar
    assert WD.wd_ilk_dokunma(np.array([[101, 106.0]]), np.array([[89.9, 99.0]]), [90.0], [105.0], [-1])[0] == 1
    assert WD.wd_ilk_dokunma(np.array([[105.0, 100]]), np.array([[89.0, 99]]), [90.0], [105.0], [-1])[0] == 0
    assert WD.wd_ilk_dokunma(np.array([[np.nan, 101]]), np.array([[np.nan, 99]]), [110.0], [95.0], [1])[0] == 0
    # YO ile aynı (yüzde sınırlarda) rastgele serilerde
    r = np.random.default_rng(3); E0 = 100 * np.exp(r.normal(0, 0.1, 400)); Hs = E0[:, None] * np.exp(np.abs(r.normal(0, 0.05, (400, 15))))
    Ls = E0[:, None] * np.exp(-np.abs(r.normal(0, 0.05, (400, 15))))
    a = WD.wd_ilk_dokunma(Hs, Ls, E0 * 1.10, E0 * 0.95, np.ones(400, int)); b = YO.yo_ilk_dokunma(E0, Hs, Ls, 0.10, 0.05, "yukari")
    assert (a == b).all()


@t
def test_r_kati():
    Os = np.array([[100, 101, 97.0], [100, 102, 103.0], [100, 99, 98.0]]); Hs = Os + 1; Ls = Os - 1; Cs = Os.copy()
    rk = WD.wd_r_kati(Os, Hs, Ls, Cs, np.array([100.0, 100.0, 100.0]), np.array([98.0, 98.0, 97.5]), np.array([1, 1, 1]))
    assert abs(rk[0] - (97.0 - 100) / 2) < 1e-12           # 3. barda açılış stopun altında -> açılışta çıkış (boşluk kaybı)
    assert abs(rk[1] - 1.5) < 1e-12                         # stop yok -> son kapanış
    assert abs(rk[2] - (-1.0)) < 1e-12                      # 2. bar L = 98 > 97,5; 3. bar L = 97 <= 97,5, açılış 98 > 97,5 -> stopta


@t
def test_taban_2R_kaba():
    r = np.random.default_rng(5); Hn = np.exp(np.abs(r.normal(0, 0.03, (40, 15)))); Ln = np.exp(-np.abs(r.normal(0, 0.03, (40, 15))))
    rr = np.array([0.01, 0.02, 0.03, 0.015]); yon = np.array([1, -1, 1, -1]); f = WD.wd_taban_2R(Hn, Ln, rr, yon)
    for i in range(4):
        say = 0
        for d in range(40):
            res = 0
            for b in range(15):
                hit = Hn[d, b] >= 1 + 2 * rr[i] if yon[i] == 1 else Ln[d, b] <= 1 - 2 * rr[i]
                st = Ln[d, b] <= 1 - rr[i] if yon[i] == 1 else Hn[d, b] >= 1 + rr[i]
                if st:
                    break
                if hit:
                    res = 1; break
            say += res
        assert abs(f[i] - say / 40) < 1e-12


@t
def test_tekil():
    D = pd.DataFrame({"kol": ["W1"] * 4 + ["W2"], "j": [0] * 5, "e": [10, 12, 15, 16, 11]})
    T, at = WD.wd_tekil(D, 5, ("kol", "j"))
    assert at == 2 and sorted(T[T.kol == "W1"].e) == [10, 15] and list(T[T.kol == "W2"].e) == [11]


@t
def test_t1_yo_ile_ayni():
    O, H, L, C, V = _rw(200, 11); dep = {"O": O, "H": H, "L": L, "C": C, "POS": np.arange(200), "off": np.array([0, 200])}
    k = np.arange(0, 180, 5); j = np.zeros(len(k), int)
    a = WD.wd_taban_gun(dep, WD.wd_atr_dizi(dep), j, k)["R15"]; b = YO.yo_sonuc_dizi(dep, j, k)["R15"]
    assert np.allclose(a, b, equal_nan=True)
    A = WD.wd_ortak(O, H, L, C); assert np.allclose(WD.wd_atr_dizi(dep), A["ATR"], equal_nan=True)


# ---------------------------------------------------------------- uçtan uca sentetik pazar
def _sentetik_pazar(n_hisse=12, n=1600, pazar="ABD"):
    idx = pd.bdate_range(end="2022-12-30", periods=n); S = [f"S{i:02d}" for i in range(n_hisse)]
    O_, H_, L_, C_, V_ = [], [], [], [], []; Vd = {"V": {}, "gecersiz": {}}
    for i, s in enumerate(S):
        O, H, L, C, V = _rw(n, 100 + i)
        for q, kol in enumerate(["W1", "W2", "W4", "W5Y", "W6", "W7", "W3T", "W2TE"]):   # gömülü desenler
            Y = WD.wd_yapay(kol, "poz", float(C[300 + q * 150]), 0.006, i)
            a0 = 300 + q * 150; L_y = len(Y["C"]); b0 = min(a0 + L_y, n)
            for arr, c in ((O, "O"), (H, "H"), (L, "L"), (C, "C"), (V, "V")):
                arr[a0:b0] = Y[c][:b0 - a0]
        Vd["V"][s] = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V, "Kur": 1.0}, index=idx)
        Vd["gecersiz"][s] = pd.DatetimeIndex([])
        O_.append(O); H_.append(H); L_.append(L); C_.append(C)
    off = np.arange(n_hisse + 1) * n
    P = {"O": np.concatenate(O_), "H": np.concatenate(H_), "L": np.concatenate(L_), "C": np.concatenate(C_), "POS": np.tile(np.arange(n), n_hisse),
         "off": off, "Op": np.column_stack(O_), "Cl": np.column_stack(C_), "P2": np.ones((n, n_hisse), bool), "tarih": idx.values, "sembol": np.array(S)}
    rows = []
    for j in range(n_hisse):
        for k in range(0, n - 16, 5):
            g = idx[k + 1]
            if pd.Timestamp("2016-01-01") <= g <= pd.Timestamp("2022-12-31") and idx[k + 15] <= pd.Timestamp("2022-12-31"):
                rows.append((j, k, HV_hucre(g, pazar)))
    Xs = pd.DataFrame(rows, columns=["j", "k", "hucre"])
    return P, Vd, Xs


def HV_hucre(g, pazar):
    import MUM_IZI_HAVUZ as HV
    return HV.hv_hucre_ad(g, pazar)


@t
def test_uctan_uca_sentetik():
    P, Vd, Xs = _sentetik_pazar()
    T, info = WD.wd_olay_pazar("ABD", P, Vd, Xs)
    assert len(T) > 50 and set(T.hucre) <= {"ABD|d1619", "ABD|d2022"} and (T.giris_tarih >= pd.Timestamp("2016-01-01")).all()
    assert "R15" not in T.columns                                           # olay dosyası getirisiz
    assert all(sum(v.values()) >= 0 for v in info["atma"].values())
    # tekil: aynı hisse aynı kolda giriş farkı >= 5
    for (k, j), g in T.groupby(["kol", "j"]):
        assert (np.diff(np.sort(g.e.to_numpy())) >= 5).all()
    S = WD.wd_sonuc_pazar(T, P, Xs)
    assert np.isfinite(S.TF).mean() > 0.95 and np.isfinite(S.ATR_TABAN).all() and S.R2_TABAN.between(0, 1).all()
    # T1 = aynı hisse aynı hücre örnek günlerinin R15 ortalaması (bağımsız hesap)
    r = S.iloc[0]; d = Xs[(Xs.j == r.j) & (Xs.hucre == r.hucre)]; a0 = int(P["off"][int(r.j)])
    t1 = np.mean(P["C"][a0 + d.k.to_numpy() + 15] / P["O"][a0 + d.k.to_numpy() + 1] - 1); assert abs(t1 - r.T1) < 1e-12
    # R15 bağımsız
    g = a0 + int(r.e); assert abs(P["C"][g + 14] / r.giris - 1 - r.R15) < 1e-12
    J = WD.wd_olcum_hesap({"ABD": S}, B=300)
    for kol in WD.WD_KOLLAR:
        assert J["kol"][kol]["hukum"] in ("ÖLÇÜLEMEDİ", "TUTAR", "TERS", "TEK DÖNEM", "TUTMADI")
    assert J["kol"]["W1"]["hukum"] == "ÖLÇÜLEMEDİ"                           # n < 300


@t
def test_hukum_kurali():
    def h(tf, alt, ust, kat, kalt, n=500, ay=30):
        return {"n": n, "ay": ay, "TF": {"ort": tf, "alt": alt, "ust": ust}, "ATR": {"kat": kat, "alt": kalt}}
    iyi = h(0.01, 0.002, 0.02, 1.2, 1.05); kotu = h(-0.01, -0.02, -0.002, 0.8, 0.7)
    o = {"ABD|d1619": iyi, "ABD|d2022": iyi, "AVR|d1619": h(0.001, -1, 1, 1, 1, n=150), "AVR|d2022": h(0.001, -1, 1, 1, 1, n=50)}
    assert WD.wd_hukum(o, True)[0] == "TUTAR" and WD.wd_hukum(o, False)[0] == "TUTMADI"
    assert WD.wd_hukum({**o, "AVR|d1619": h(-0.001, -1, 1, 1, 1, n=150)}, True)[0] == "TUTMADI"
    assert WD.wd_hukum({**o, "ABD|d2022": kotu}, True)[0] == "TEK DÖNEM"
    assert WD.wd_hukum({**o, "ABD|d1619": kotu, "ABD|d2022": kotu}, True)[0] == "TERS"
    assert WD.wd_hukum({**o, "ABD|d1619": h(0.01, 0.002, 0.02, 1.2, 1.05, n=299)}, True)[0] == "ÖLÇÜLEMEDİ"
    assert WD.wd_hukum({**o, "ABD|d1619": h(0.01, 0.002, 0.02, 1.2, 1.05, ay=11)}, True)[0] == "ÖLÇÜLEMEDİ"


@t
def test_bootstrap():
    ay = np.repeat([f"2017-{m:02d}" for m in range(1, 13)], 20); x = np.random.default_rng(1).normal(0.01, 0.05, len(ay))
    k, W = WD.wd_ay_W(ay, "deneme", 2000); o = WD.wd_boot_ort(x, k, W)
    assert o["alt"] < o["ort"] < o["ust"] and abs(o["ort"] - x.mean()) < 1e-15
    k2, W2 = WD.wd_ay_W(ay, "deneme", 2000); assert (W == W2).all()          # tohum tekrarlanır
    hit = (x > 0).astype(float); tb = np.full(len(x), 0.5); kk = WD.wd_boot_kat(hit, tb, k, W)
    assert abs(kk["kat"] - hit.sum() / tb.sum()) < 1e-12 and kk["alt"] <= kk["kat"] <= kk["ust"]


# ---------------------------------------------------------------- kesik / çakışma / eşik
@t
def test_kesik_assert():
    try:
        WD.wd_tarih_kapi(pd.bdate_range("2022-12-20", "2023-01-05").values, "deneme")
    except WD.WDHata as ex:
        assert "KESİK" in str(ex)
    else:
        raise AssertionError("kesik kapısı çalışmadı")
    WD.wd_tarih_kapi(pd.bdate_range("2022-12-01", "2022-12-30").values, "deneme")
    V = {"A": pd.DataFrame({"Close": [1.0]}, index=[pd.Timestamp("2023-01-03")])}
    try:
        WD.wd_kesik_kapi(V, "deneme")
    except WD.WDHata:
        pass
    else:
        raise AssertionError("kesik kapısı (V) çalışmadı")


@t
def test_cakisma_kapisi():
    kod = open(os.path.join(os.path.dirname(os.path.abspath(WD.__file__)), "WEB_DESEN.py"), encoding="utf-8").read()
    ns = {"__name__": "wd_test", "__file__": WD.__file__}
    exec(compile(kod, "WEB_DESEN.py", "exec"), ns)
    ns2 = {"__name__": "wd_test2", "__file__": WD.__file__, "wd_kapi": 1}
    try:
        exec(compile(kod, "WEB_DESEN.py", "exec"), ns2)
    except RuntimeError as ex:
        assert "çakışma" in str(ex)
    else:
        raise AssertionError("çakışma kapısı çalışmadı")


@t
def test_esik_sabit():
    E = WD.WD_ESIK
    assert E["W1"]["tepe_pay"] == 0.25 and E["W2"]["fitil_pay"] == 0.5 and E["W2"]["stop_atr"] == 0.1 and E["W2E"]["atr_pay"] == 0.25
    assert E["W3"]["tik"] == 0.999 and E["W4"]["bos_bar"] == 10 and E["W4"]["test_bar"] == 5 and E["W5"]["geri_bar"] == 3
    assert E["W6"] == {**E["W6"], "alt_govde": 2.0, "ust_pay": 0.1, "boy_ort": 0.8, "dip_bar": 10}
    assert E["W7"] == {**E["W7"], "hacim_kat": 2.0, "hacim_pencere": 20, "kapanis_pay": 0.5, "dip_bar": 20}
    assert E["ortak"]["uc_yas"] == 4 and E["ortak"]["uc_yas_w3"] == 3 and E["ortak"]["uc_pencere"] == 20 and E["ortak"]["ort_boy"] == 10
    assert E["olcu"]["ufuk"] == 15 and E["olcu"]["atr_hedef"] == 2.0 and E["olcu"]["atr_stop"] == 1.0 and E["olcu"]["R_hedef"] == 2.0
    assert E["boot"]["B"] == 10000 and E["boot"]["tohum"] == 2711 and E["bh"]["q"] == 0.10
    assert E["hukum"]["n_min"] == 300 and E["hukum"]["ay_min"] == 12 and E["hukum"]["avr_n"] == 100 and E["filtre"]["tekil_bar"] == 5
    assert set(WD.WD_KONTROL) == {f"K{i}" for i in range(1, 15)} and len(WD.WD_KOLLAR) == 17


if __name__ == "__main__":
    bas = 0
    for f in ISIM:
        try:
            f(); print("GEÇTİ", f.__name__)
        except Exception as ex:  # noqa: BLE001
            bas += 1; print("KALDI", f.__name__, type(ex).__name__, ex)
    print(f"{len(ISIM) - bas} / {len(ISIM)} geçti")
    sys.exit(1 if bas else 0)
