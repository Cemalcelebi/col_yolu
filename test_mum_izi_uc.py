"""test_mum_izi_uc — MUM_IZI_UC (EK 27, uç pencereler) sentetik testleri: her ölçünün tanımı elle (düz döngüyle) hesaplanmış küçük örnekle; uç yönleri;
kesimlerin YALNIZ keşif örneğinden hesaplanıp ötekilere aynen uygulanması; kilitli / fiyat adımına yapışmış pencerelerin atılması; E1 15 bar tekilleştirme ve
E2'de örtüşmesiz sonuç pencereleri; geleceğe bakma (pencere sonrası barlar bozulunca ölçüler aynı); kesik assert; ay kümeli bootstrap tohumu; BH; hüküm
kuralı; çakışma kapısı. Çalıştır: python test_mum_izi_uc.py"""
import math
import os
import statistics
import sys

import numpy as np
import pandas as pd

import MUM_IZI_UC as UC


def _seri(n: int = 200, son: str = "2019-12-31", tohum: int = 1) -> pd.DataFrame:
    ix = pd.bdate_range(end=son, periods=n); r = np.random.default_rng(tohum)
    C = 10 * np.exp(np.cumsum(r.normal(0, 0.02, n))); O = C * (1 + r.normal(0, 0.01, n))
    H = np.maximum(O, C) * (1 + np.abs(r.normal(0, 0.01, n)) + 1e-4); L = np.minimum(O, C) * (1 - np.abs(r.normal(0, 0.01, n)) - 1e-4)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1000.0}, index=ix)


def _elle(d: pd.DataFrame, t: int, m: int) -> dict:
    """Düz döngüyle (statistics.median) tanımın kendisi."""
    O, H, L, C = (d[c].tolist() for c in ("Open", "High", "Low", "Close")); s = t - m + 1
    rg = [H[i] - L[i] for i in range(len(C))]; boy = [rg[i] / C[i] for i in range(len(C))]; gov = [abs(C[i] - O[i]) / C[i] for i in range(len(C))]
    ust = [(H[i] - max(O[i], C[i])) / rg[i] for i in range(len(C))]; alt = [(min(O[i], C[i]) - L[i]) / rg[i] for i in range(len(C))]
    W = range(s, t + 1); P = range(s - 120, s); q = math.ceil(m / 3); S3 = range(t - q + 1, t + 1)

    def bant(i):
        w = C[i - 19:i + 1]; mu = sum(w) / 20; sd = (sum((x - mu) ** 2 for x in w) / 20) ** 0.5
        return mu + 2 * sd, mu, mu - 2 * sd
    bw = lambda i: (bant(i)[0] - bant(i)[2]) / bant(i)[1]
    bc = lambda i: (C[i] - bant(i)[1]) / (bant(i)[0] - bant(i)[1])
    med = statistics.median
    return {"BOY_YUZDE_ORAN": med([boy[i] for i in W]) / med([boy[i] for i in P]), "BOY_GRAFIK_ORAN": med([rg[i] for i in W]) / med([rg[i] for i in P]),
            "BOY_MUTLAK": 100 * med([boy[i] for i in W]), "GOVDE_ORAN": med([gov[i] for i in W]) / med([gov[i] for i in P]),
            "GOVDE_BOY": med([abs(C[i] - O[i]) / rg[i] for i in W]), "UST_FITIL": med([ust[i] for i in W]), "ALT_FITIL": med([alt[i] for i in W]),
            "UST_ALT_PAY": sum(1 for i in W if H[i] - max(O[i], C[i]) > min(O[i], C[i]) - L[i]) / m, "SON_UST_FITIL": med([ust[i] for i in S3]),
            "DARALMA": bw(t) / bw(s) - 1, "BANT_SON": -abs(med([bc(i) for i in S3]) - 0.85),
            "ONCEKI_DUSUS": 100 * (min(L[i] for i in W) / max(H[i] for i in range(s - 60, s)) - 1)}


def test_olcu_elle():
    d = _seri(220)
    D = UC.uc_bar(d.Open, d.High, d.Low, d.Close)
    for t, m in ((150, 16), (200, 21), (180, 24)):
        O = UC.uc_olcu(D, [t], m); E = _elle(d, t, m)
        for a in UC.UC_OLCU_AD:
            assert abs(O[a][0] - E[a]) <= 1e-9 * max(1.0, abs(E[a])), (a, t, m, O[a][0], E[a])
    # el ile kurulmuş tam sayılı örnek: pencerede bütün mumlar üst fitilli, dip 10, önceki 60 barın tepesi 20 -> ONCEKI_DUSUS -50, UST_ALT_PAY 1
    n = 160; ix = pd.bdate_range("2018-01-01", periods=n); C = np.full(n, 15.0); O = np.full(n, 15.0); H = np.full(n, 16.0); L = np.full(n, 14.0)
    C[::2] = 15.5; H[100] = 20.0
    s, t = 140, 155; O[s:t + 1] = 11.0; C[s:t + 1] = 11.2; H[s:t + 1] = 12.0; L[s:t + 1] = 10.9; L[147] = 10.0; H[147] = 13.0
    D2 = UC.uc_bar(O, H, L, C); O2 = UC.uc_olcu(D2, [t], 16)
    assert abs(O2["ONCEKI_DUSUS"][0] - (-50.0)) < 1e-12 and O2["UST_ALT_PAY"][0] == 1.0
    assert abs(O2["GOVDE_BOY"][0] - 0.2 / 1.1) < 1e-12 and abs(O2["UST_FITIL"][0] - 0.8 / 1.1) < 1e-12 and abs(O2["ALT_FITIL"][0] - 0.1 / 1.1) < 1e-12
    assert abs(O2["BOY_GRAFIK_ORAN"][0] - 1.1 / 2.0) < 1e-12


def test_uc_yonleri():
    X = pd.DataFrame({a: [1.0, 2.0] for a in UC.UC_OLCU_AD})
    for a, y in UC.UC_OLCU:
        u = UC.uc_skor(X, a)
        assert (u[0] > u[1]) if y == "KUCUK" else (u[1] > u[0]), a
    assert dict(UC.UC_OLCU)["ONCEKI_DUSUS"] == "KUCUK" and dict(UC.UC_OLCU)["DARALMA"] == "KUCUK" and dict(UC.UC_OLCU)["BANT_SON"] == "BUYUK"
    assert dict(UC.UC_OLCU)["UST_FITIL"] == "BUYUK" and dict(UC.UC_OLCU)["ALT_FITIL"] == "KUCUK" and len(UC.UC_OLCU) == 12 and len(UC.UC_SATIR) == 16
    # BANT_SON: değer -|ham - 0,85|; 0,85'e en yakın olan en uç (BUYUK)
    assert -abs(0.84 - 0.85) > -abs(0.99 - 0.85) > -abs(0.5 - 0.85)


def _X_rastgele(n: int = 4000, tohum: int = 5) -> pd.DataFrame:
    r = np.random.default_rng(tohum); h = np.array(["ABD|d1619"] * (n // 2) + ["ABD|d2022"] * (n // 4) + ["AVR|d1619"] * (n - n // 2 - n // 4))
    X = pd.DataFrame({a: r.normal(0, 1, n) for a in UC.UC_OLCU_AD}); X["hucre"] = h; X["durum"] = "TAMAM"
    X.loc[::97, "durum"] = "KILITLI"
    return X


def test_kesim_yalniz_kesif():
    X = _X_rastgele(); K1 = UC.uc_kesim(X)
    Y = X.copy(); m = Y.hucre != "ABD|d1619"
    for a in UC.UC_OLCU_AD:
        Y.loc[m, a] = Y.loc[m, a] * 50 + 7                                  # keşif dışı değerler bozulur
    Y.loc[(Y.hucre == "ABD|d1619") & (Y.durum != "TAMAM"), UC.UC_OLCU_AD] = 999.0   # atılan keşif pencereleri de kesime girmez
    K2 = UC.uc_kesim(Y)
    for a in UC.UC_OLCU_AD:
        for k in ("UC10", "UC2", "B4_30", "B4_10"):
            assert K1["olcu"][a][k] == K2["olcu"][a][k], (a, k)
        assert K1["olcu"][a]["besli"] == K2["olcu"][a]["besli"]
    for b in UC.UC_BILESIK:
        assert K1["bilesik"][b]["besli"] == K2["bilesik"][b]["besli"]
    Z = UC.uc_uygula(X, K1); kz = (Z.hucre == "ABD|d1619") & (Z.durum == "TAMAM")
    for a in UC.UC_OLCU_AD + ["B1_KUCUK_MUM", "B3_HEPSI"]:
        p10 = Z[f"{a}_UC10"][kz].mean(); p2 = Z[f"{a}_UC2"][kz].mean()
        assert 0.095 <= p10 <= 0.105 and 0.015 <= p2 <= 0.025, (a, p10, p2)
        b = Z[f"{a}_BES"][kz]; assert set(b.unique()) == {1, 2, 3, 4, 5} and abs((b == 5).mean() - 0.2) < 0.01
    # B4: altı bileşen kendi uç %30'unda; bağımsız normalde ~ 0,3^6
    assert Z["B4_HEPSI_VE_UC10"][kz].mean() < 0.01 and Z["B4_HEPSI_VE_UC2"][kz].sum() <= Z["B4_HEPSI_VE_UC10"][kz].sum()
    # aynı kesim ötekine aynen: keşif dışında bir pencerenin bayrağı kendi değeri ve KEŞİF sınırıyla
    a = "BOY_MUTLAK"; j = int(np.flatnonzero((Z.hucre == "ABD|d2022").to_numpy())[0]); u = -X[a].iloc[j]
    assert bool(Z[f"{a}_UC10"].iloc[j]) == bool(u >= K1["olcu"][a]["UC10"])
    J = UC.uc_kesim_json({"E2|gunluk": K1}); assert "_sirali" not in J["E2|gunluk"]["olcu"][a] and len(J["E2|gunluk"]["olcu"][a]["sirali_sha"]) == 64


def _blok_sentetik(monkey: dict):
    V = {}; GEC = {}
    for j, s in enumerate(["S0", "S1", "S2"]):
        d = _seri(600, "2019-12-31", tohum=20 + j); V[s] = d
    # S1: pencere 2 civarında takvimin %40'ı geçersiz (kilitli / hacimsiz) gün
    ix = V["S1"].index; t2 = 150; bas, son = ix[t2 - 15], ix[t2]
    tum = pd.bdate_range(bas, son); kal = tum[::2]; gec = tum.difference(kal)
    V["S1"] = V["S1"].drop(index=V["S1"].index.intersection(gec))
    GEC["S1"] = pd.DatetimeIndex(gec); GEC["S0"] = pd.DatetimeIndex([]); GEC["S2"] = pd.DatetimeIndex([ix[300]])
    monkey["uc_blok_veri"] = UC.uc_blok_veri; monkey["uc_evren_e2"] = UC.uc_evren_e2
    UC.uc_blok_veri = lambda z, p: (V, None, GEC)
    UC.uc_evren_e2 = lambda z, p, B, aday: {s: np.ones(len(t), bool) for s, t in aday.items()}
    return V, GEC


def test_blok_kilitli_tekil_ortusmesiz():
    mk: dict = {}; V, GEC = _blok_sentetik(mk)
    try:
        E1 = pd.DataFrame({"zaman": ["gunluk"] * 2, "pazar": ["ABD"] * 2, "sembol": ["S0", "S0"], "t": [300, 315], "m": [18, 16],
                           "tarih": [str(V["S0"].index[300].date()), str(V["S0"].index[315].date())], "evren": [True, True]})
        X = UC.uc_blok_pencere("gunluk", "ABD", E1)
    finally:
        UC.uc_blok_veri = mk["uc_blok_veri"]; UC.uc_evren_e2 = mk["uc_evren_e2"]
    e2 = X[X.evren == "E2"]
    for s, g in e2.groupby("sembol"):
        t = np.sort(g.t.to_numpy()); assert (np.diff(t) == 15).all()
        assert ((t - 135) % 15 == 0).all() and t.min() >= 135
        assert (t[1:] + 1 > t[:-1] + 15).all()                              # sonuç pencereleri (t+1 .. t+15) örtüşmez
    k = X[(X.sembol == "S1") & (X.durum == "KILITLI")]
    assert len(k) >= 1 and (k.kilitli_pay > 0.20).all()
    assert (X[X.durum == "TAMAM"].kilitli_pay <= 0.20).all()
    # S2'de tek geçersiz gün: pay 1 / 17 < 0,20 -> atılmaz
    assert not (X[(X.sembol == "S2")].durum == "KILITLI").any()
    # sınır: pay tam 0,20 atılmaz (> 0,20 kuralı)
    gun = pd.bdate_range("2019-01-01", periods=8); gec = pd.bdate_range("2019-01-11", periods=2)
    assert abs(UC.uc_kilitli_pay(gec, gun, [gun[0]], [gec[-1]])[0] - 0.20) < 1e-12 and not (UC.uc_kilitli_pay(gec, gun, [gun[0]], [gec[-1]]) > 0.20).any()
    e1 = X[X.evren == "E1"]; assert len(e1) == 2 and set(e1.m) == {18, 16}
    assert (X.durum.isin(UC.UC_ESIK["atma"]["sira"] + ["TAMAM"])).all()
    # E2 giriş t + 1 açılışı, stop pencere dibi x 0,98
    r = X[(X.durum == "TAMAM") & (X.evren == "E2")].iloc[0]; d = V[r.sembol]
    assert abs(r.E0 - d.Open.iloc[r.t + 1]) < 1e-12 and abs(r.stop - d.Low.iloc[r.t - 15:r.t + 1].min() * 0.98) < 1e-12 and r.giris == d.index[r.t + 1]


def test_e1_tekil_dosya():
    if not os.path.exists(UC.UC_YOL["ham8"]):
        print("  (atlandı: MUM_IZI8 ham dosyası yok)"); return
    E = UC.uc_e1_olaylar()
    assert E.evren.all() and E.attrs["tekil_atilan"] >= 0
    for (z, s), g in E.groupby(["zaman", "sembol"]):
        t = np.sort(g.t.to_numpy())
        assert (np.diff(t) >= 15).all(), (z, s)
    assert (E.m >= 16).all() and (E.m <= 24).all()


def test_gelecege_bakma():
    d = _seri(260); D = UC.uc_bar(d.Open, d.High, d.Low, d.Close); t = 180
    A = UC.uc_olcu(D, [t], 16)
    d2 = d.copy(); d2.iloc[t + 1:, :4] = d2.iloc[t + 1:, :4].to_numpy() * np.random.default_rng(3).uniform(0.3, 3.0, (len(d2) - t - 1, 4))
    d2["High"] = d2[["Open", "High", "Low", "Close"]].max(axis=1) * 1.01; d2.iloc[:t + 1] = d.iloc[:t + 1]
    D2 = UC.uc_bar(d2.Open, d2.High, d2.Low, d2.Close); B = UC.uc_olcu(D2, [t], 16)
    for a in A:
        assert (A[a][0] == B[a][0]) or (np.isnan(A[a][0]) and np.isnan(B[a][0])), a
    try:
        UC.uc_olcu(D, [100], 16)                                            # önceki 120 bar yok
    except UC.UCHata:
        pass
    else:
        raise AssertionError("önceki 120 bar yokken ölçü durmadı")


def test_kesik_assert():
    ok = {"A": pd.DataFrame({"Close": [1.0]}, index=pd.to_datetime(["2022-12-30"]))}
    assert UC.uc_kesik_kapi(ok) == pd.Timestamp("2022-12-30")
    try:
        UC.uc_kesik_kapi({"A": pd.DataFrame({"Close": [1.0]}, index=pd.to_datetime(["2023-01-02"]))})
    except UC.UCHata as ex:
        assert "KESİK" in str(ex)
    else:
        raise AssertionError("kesik aşımı durmadı")
    assert UC.UC_KESIK == pd.Timestamp("2022-12-31")


def test_boot_tohum_ve_bh():
    r = np.random.default_rng(1); x = r.normal(0.01, 0.05, 600); ay = np.array([f"2019-{1 + i % 12:02d}" for i in range(600)])
    a = UC.uc_boot(x, ay, "deneme", B=2000); b = UC.uc_boot(x, ay, "deneme", B=2000); c = UC.uc_boot(x, ay, "baska", B=2000)
    assert a == b and a["alt"] != c["alt"] and a["alt"] < a["ort"] < a["ust"] and 0 < a["p"] < 1
    assert UC.UC_ESIK["tohum"] == 27 and UC.UC_ESIK["boot"]["B"] == 10000
    f1 = UC.uc_boot_fark(x[:300], ay[:300], x[300:], ay[300:], "f", B=1000); f2 = UC.uc_boot_fark(x[:300], ay[:300], x[300:], ay[300:], "f", B=1000)
    assert f1 == f2
    q = UC.uc_bh([0.01, 0.04, 0.03, 0.5, None])
    p = [0.01, 0.04, 0.03, 0.5]; m = 4; s = sorted(p); el = [min(1, min(s[k] * m / (k + 1) for k in range(i, m))) for i in range(m)]
    beq = {v: el[i] for i, v in enumerate(s)}
    assert all(abs(q[i] - beq[p[i]]) < 1e-12 for i in range(4)) and q[4] is None


def test_hukum_kurali():
    def r(n, ay, ort, alt, ust):
        return {"n": n, "ay": ay, "TF": {"ort": ort, "alt": alt, "ust": ust}}
    k = r(500, 40, 0.01, 0.002, 0.02); d = r(400, 30, 0.01, 0.001, 0.02); av = [r(50, 20, 0.003, -0.01, 0.01), r(5, 3, -0.02, -0.05, 0.0)]
    assert UC.uc_hukum(k, d, av, 0.05) == "TUTAR"
    assert UC.uc_hukum(k, d, av, 0.2) == "KISMİ"                               # BH geçmedi
    assert UC.uc_hukum(k, d, [r(50, 20, -0.003, -0.01, 0.01)], 0.05) == "KISMİ"  # AVR işareti eksi (n >= 10)
    assert UC.uc_hukum(k, r(400, 30, -0.01, -0.02, -0.001), av, 0.05) == "TERS"
    assert UC.uc_hukum(k, r(400, 30, 0.002, -0.001, 0.01), av, 0.5) == "TEK DÖNEM"
    assert UC.uc_hukum(r(500, 40, -0.01, -0.02, 0.0), r(400, 30, 0.002, -0.001, 0.01), av, 0.5) == "TUTMADI"
    assert UC.uc_hukum(k, r(25, 30, 0.01, 0.001, 0.02), av, 0.05) == "ÖLÇÜLEMEDİ" and UC.uc_hukum(k, r(300, 11, 0.01, 0.001, 0.02), av, 0.05) == "ÖLÇÜLEMEDİ"
    assert UC.uc_hukum(k, {"n": 0, "ay": 0, "TF": float("nan")}, av, None) == "ÖLÇÜLEMEDİ"
    assert abs(UC.uc_spearman5([1, 2, 3, 4, 5]) - 1.0) < 1e-12 and abs(UC.uc_spearman5([1, 3, 2, 4, 5]) - 0.9) < 1e-12 and UC.uc_spearman5([1, None, 2, 3, 4]) is None


def test_hafta_no_ve_iso():
    cal = pd.bdate_range("2020-12-28", "2021-01-15"); h = UC.uc_hafta_no(cal)
    assert (np.diff(h) >= 0).all() and len(np.unique(h)) == 3 and h[0] == h[4] and h[5] == h[0] + 1
    assert list(np.unique(UC._uc_iso(cal))) == [202053, 202101, 202102]


def test_cakisma_kapisi():
    yol = os.path.join(os.path.dirname(os.path.abspath(UC.__file__)), "MUM_IZI_UC.py")
    g = {"__name__": "x", "__file__": yol, "uc_olcu": object()}
    try:
        exec(compile(open(yol, encoding="utf-8").read(), yol, "exec"), g)
    except RuntimeError as ex:
        assert "çakışma kapısı" in str(ex)
    else:
        raise AssertionError("çakışma kapısı durmadı")


def test_sha():
    assert len(UC.uc_esik_sha()) == 64 and UC.uc_esik_sha() == UC.uc_esik_sha(dict(UC.UC_ESIK))
    E = dict(UC.UC_ESIK); E["surum"] = "x"; assert UC.uc_esik_sha(E) != UC.uc_esik_sha()


def _sent_pazar(n_his: int, tohum: int) -> dict:
    V = {}
    for j in range(n_his):
        d = _seri(2100, "2022-12-30", tohum=tohum * 100 + j); V[f"S{j}"] = d
    return V


def test_uctan_uca_sentetik():
    """Getirisiz pencere -> kesim -> getiri -> takvim -> tablolar -> rapor / png / csv (sentetik; B küçültülür)."""
    import tempfile
    VV = {p: _sent_pazar(36 if p == "ABD" else 12, k + 1) for k, p in enumerate(UC.UC_PAZAR)}
    eski = (UC.uc_blok_veri, UC.uc_evren_e2, UC.uc_takvim_veri, UC.UC_ESIK["boot"]["B"])
    try:
        UC.uc_blok_veri = lambda z, p: (VV[p], (UC.MV.mv_haftalik_panel(VV[p]) if z == "haftalik" else None), {})
        UC.uc_evren_e2 = lambda z, p, B, aday: {s: (np.arange(len(t)) % 4 != 0) for s, t in aday.items()}
        UC.uc_takvim_veri = lambda p: VV[p]
        UC.UC_ESIK["boot"]["B"] = 300
        E1 = pd.DataFrame(columns=["zaman", "pazar", "sembol", "t", "m", "tarih", "evren"])
        rows = []
        for z in UC.UC_ZAMAN:
            for p in UC.UC_PAZAR:
                B = VV[p] if z == "gunluk" else UC.MV.mv_haftalik_panel(VV[p])
                for s, d in B.items():
                    for t in range(160, len(d) - 20, 37):
                        rows.append({"zaman": z, "pazar": p, "sembol": s, "t": t, "m": 16 + t % 9, "tarih": str(d.index[t].date()), "evren": True})
        E1 = pd.DataFrame(rows)
        X0 = pd.concat([UC.uc_blok_pencere(z, p, E1) for z in UC.UC_ZAMAN for p in UC.UC_PAZAR], ignore_index=True)
        assert (X0.evren == "E1").any() and (X0.durum == "EVREN_DISI").any() and (X0.durum == "TAMAM").sum() > 1000
        X, KS = UC.uc_hazir(X0); S = UC.uc_sayim(X, KS); X2, KS2 = UC.uc_hazir(X0)
        assert UC.uc_json_sha(UC.uc_kesim_json(KS)) == UC.uc_json_sha(UC.uc_kesim_json(KS2))       # kesim tekrarlanabilir
        S["takvim"] = UC.uc_takvim_sayim(X, {p: UC.uc_takvim_cal(p) for p in UC.UC_PAZAR})
        PJ = {}
        for z in UC.UC_ZAMAN:
            for p in UC.UC_PAZAR:
                Y, PJ[f"{z}|{p}"] = UC.uc_getiri_blok(z, p, X, denetim=40)
                for c in ("R15", "d5", "d10", "T1", "tb5", "tb10", "PIY", "PIY_don"):
                    if c not in X:
                        X[c] = np.nan
                    X.loc[Y.index, c] = Y[c]
        m = X.durum == "TAMAM"
        assert np.isfinite(X.R15[m]).all() and np.isfinite(X.T1[m]).all() and X.d5[m].isin([0.0, 1.0]).all() and (X.tb5[m].between(0, 1)).all()
        assert np.isfinite(X.PIY[m & (X.zaman == "gunluk")]).mean() > 0.95 and np.isfinite(X.PIY[m & (X.zaman == "haftalik")]).mean() > 0.9
        TK = UC.uc_takvim_hesap(X); T = UC.uc_tablolar(X, PJ, TK)
        assert len(T["hukum"]) == 128 and set(T["genel"]) == {"E1|gunluk", "E1|haftalik", "E2|gunluk", "E2|haftalik", "hepsi"}
        assert all(v["hukum"] in ("TUTAR", "TERS", "KISMİ", "TEK DÖNEM", "TUTMADI", "ÖLÇÜLEMEDİ") for v in T["hukum"].values())
        # bir satır elle: E2 günlük BOY_MUTLAK UC10 ABD|d1619
        g = X[m & (X.evren == "E2") & (X.zaman == "gunluk") & (X.hucre == "ABD|d1619") & X.BOY_MUTLAK_UC10]
        r = [x for x in T["satir"] if (x["evren"], x["zaman"], x["satir"], x["uc"], x["hucre"]) == ("E2", "gunluk", "BOY_MUTLAK", "UC10", "ABD|d1619")][0]
        assert r["n"] == len(g) and abs(r["TF"]["ort"] - float((g.R15 - g.T1).mean())) < 1e-12 and abs(r["d5"] - g.d5.mean()) < 1e-12
        with tempfile.TemporaryDirectory() as d:
            J = {"tablo": T}
            md = UC.uc_rapor_tablo(J); assert "OLASILIK TABLOSU E2 gunluk" in md and "TAKVİM" in md
            UC.uc_png(J, d); UC.uc_ozet_csv(J, d)
            assert os.path.getsize(os.path.join(d, UC.UC_DOSYA["png"])) > 10000
            C = pd.read_csv(os.path.join(d, UC.UC_DOSYA["ozet"])); assert len(C) == len(T["satir"]) and "TF_alt" in C
        # tohum: aynı girdiyle aynı T1 / taban
        Y2, _ = UC.uc_getiri_blok("gunluk", "AVR", X, denetim=5)
        assert np.array_equal(Y2.tb5.to_numpy(), X.loc[Y2.index, "tb5"].to_numpy()) and np.array_equal(Y2.T1.to_numpy(), X.loc[Y2.index, "T1"].to_numpy())
    finally:
        UC.uc_blok_veri, UC.uc_evren_e2, UC.uc_takvim_veri, UC.UC_ESIK["boot"]["B"] = eski


if __name__ == "__main__":
    t = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in t:
        f(); print("GEÇTİ", f.__name__)
    print(f"{len(t)} test geçti")
    sys.exit(0)
