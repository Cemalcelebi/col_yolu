"""test_uc_iz2 — UC_IZ2 sentetik testleri (gerçek veri yok): bilanço kabul saati sınırı (15:59 / 16:00 / 16:01, yaz / kış saati), olay günü
takvimi, 20 gün tekrar kuralı, FILING_DATE pencere sınırları (t - 90 / t), B eşiği ve B eşi dışlaması, konum eşi dışlaması (c2_es), E1 süzgeci
(form / madde / sınıf hisseleri), kesik denetimi, uc2_hucre = UC_IZ.uc_hucre (H 15), çakışma kapısı. Çalıştır: python test_uc_iz2.py"""
import os
import pickle
import sys
import tempfile

import numpy as np
import pandas as pd

import UC_IZ as U
import UC_IZ2 as U2


def test_kabul_saati_sinir():
    # yaz saati (EDT = UTC-4) ve kış saati (EST = UTC-5)
    utc = ["2022-07-15T19:59:00.000Z", "2022-07-15T20:00:00.000Z", "2022-07-15T20:01:00.000Z",
           "2022-01-14T20:59:00.000Z", "2022-01-14T21:00:00.000Z", "2022-01-14T21:01:00.000Z",
           "2022-07-15T11:30:00.000Z", None]
    D0, ts = U2.uc2_kabul_d0(utc)
    exp = ["2022-07-15", "2022-07-16", "2022-07-16", "2022-01-14", "2022-01-15", "2022-01-15", "2022-07-15"]
    for i, e in enumerate(exp):
        assert pd.Timestamp(D0.iloc[i]) == pd.Timestamp(e), (i, D0.iloc[i], e)
    assert pd.isna(D0.iloc[7])
    assert ts.iloc[0].strftime("%H:%M") == "15:59" and ts.iloc[3].strftime("%H:%M") == "15:59"


def test_olay_gunu_takvim():
    tk = pd.bdate_range("2022-07-11", "2022-07-22")         # hafta içi
    D0 = pd.to_datetime(["2022-07-15", "2022-07-16", "2022-07-17", "2022-07-23"])
    t = U2.uc2_olay_gunu(D0, tk)
    assert pd.Timestamp(t[0]) == pd.Timestamp("2022-07-15")
    assert pd.Timestamp(t[1]) == pd.Timestamp("2022-07-18") and pd.Timestamp(t[2]) == pd.Timestamp("2022-07-18")
    assert np.isnat(t[3])


def test_tekrar_20_gun():
    t = pd.to_datetime(["2020-01-01", "2020-01-16", "2020-01-21", "2020-01-22", "2020-02-10", "2020-01-01"])
    cik = np.array([1, 1, 1, 1, 1, 2])
    tut = U2.uc2_tekrar_at(cik, t, 20)
    # 01-01 tut; 01-16 (15 g) at; 01-21 (20 g, <= 20) at; 01-22 (21 g) tut; 02-10 (19 g sonra 01-22'den) at; başka CIK tut
    assert list(tut) == [True, False, False, True, False, True], tut


def test_i_pencere_sinirlari():
    t0 = pd.Timestamp("2020-06-30")
    A1 = pd.DataFrame({"issuer_cik": [10, 10, 10, 10, 20], "D": pd.to_datetime([t0 - pd.Timedelta(days=90), t0 + pd.Timedelta(days=1),
                                                                              t0 - pd.Timedelta(days=89), t0, t0])})
    # yalnız t-90 (dışarıda) ve t+1 (gelecek) olan CIK
    A_dis = A1.iloc[[0, 1]]
    b, n, s = U2.uc2_i(np.array([10]), np.array([t0]), A_dis)
    assert not b[0] and n[0] == 0 and np.isnat(s[0])
    b, n, s = U2.uc2_i(np.array([10]), np.array([t0]), A1.iloc[[0, 1, 2]])
    assert b[0] and n[0] == 1 and pd.Timestamp(s[0]) == t0 - pd.Timedelta(days=89)
    b, n, s = U2.uc2_i(np.array([10, 30]), np.array([t0, t0]), A1)
    assert b[0] and n[0] == 2 and pd.Timestamp(s[0]) == t0 and not b[1]


def _pb(u=12, n=6, kv=None, ret=None, atp=None):
    idx = pd.bdate_range("2021-03-01", periods=n)
    S = [f"S{j:02d}" for j in range(u)]
    P = {"tarih": idx, "sembol": S, "kol": {s: j for j, s in enumerate(S)}}
    KV = np.zeros((n, u), int) if kv is None else kv
    return {"P": P, "KV": KV}, (np.zeros((n, u)) if ret is None else ret), (np.full((n, u), 0.02) if atp is None else atp)


def test_b_esik_ve_dislama():
    u, n = 12, 6
    ret = np.zeros((n, u)); d = 3
    ret[d, :] = np.array([0.0, 0.010, 0.020, 0.030, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090, 0.100, 0.110])
    kv = np.zeros((n, u), int); kv[d, 6:] = 1                 # kova 0: S00-S05, kova 1: S06-S11
    atp = np.full((n, u), 0.02)
    Pb, RET, ATP = _pb(u, n, kv, ret, atp)
    t = Pb["P"]["tarih"][d]
    # S05 (kova 0): eşler S00-S04 (5) -> medyan 0.02 -> EAR 0.03, BVAL 1.5 -> B 1
    E1 = pd.DataFrame({"sembol": ["S05"], "tarih": [t]})
    B = U2.uc2_b(E1, Pb, RET, ATP, pd.DataFrame({"sembol": ["S05"], "tarih": [t]}))
    assert abs(B.ear.iloc[0] - 0.03) < 1e-12 and abs(B.bval.iloc[0] - 1.5) < 1e-12 and B.B.iloc[0] == 1 and B.n_es_b.iloc[0] == 5
    # dışlama: S04 de o gün E1 -> eş 4 < 5 -> NaN
    B = U2.uc2_b(E1, Pb, RET, ATP, pd.DataFrame({"sembol": ["S05", "S04"], "tarih": [t, t]}))
    assert np.isnan(B.bval.iloc[0]) and np.isnan(B.B.iloc[0]) and B.n_es_b.iloc[0] == 4
    # eşik tam 1,0 -> B 1; 0,999 -> B 0; -1,0 -> Bm 1
    for r_, bexp, bmexp in ((0.02 + 0.02, 1.0, 0.0), (0.02 + 0.01998, 0.0, 0.0), (0.02 - 0.02, 0.0, 1.0)):
        ret2 = ret.copy(); ret2[d, 5] = r_
        B = U2.uc2_b(E1, Pb, ret2, ATP, pd.DataFrame({"sembol": ["S05"], "tarih": [t]}))
        assert B.B.iloc[0] == bexp and B.Bm.iloc[0] == bmexp, (r_, B.bval.iloc[0])
    # kova 1 (S06-S11): S11'in eşleri S06-S10 -> medyan 0.08 -> EAR 0.03
    B = U2.uc2_b(pd.DataFrame({"sembol": ["S11"], "tarih": [t]}), Pb, RET, ATP, pd.DataFrame({"sembol": ["S11"], "tarih": [t]}))
    assert abs(B.ear.iloc[0] - 0.03) < 1e-12
    # kova yok -> NaN
    kv2 = kv.copy(); kv2[d, 5] = -1; Pb2, _, _ = _pb(u, n, kv2, ret, atp)
    B = U2.uc2_b(E1, Pb2, RET, ATP, pd.DataFrame({"sembol": ["S05"], "tarih": [t]}))
    assert np.isnan(B.B.iloc[0])


def test_ret_atrp_gecmis():
    idx = pd.bdate_range("2021-01-01", periods=40)
    rng = np.random.default_rng(3)
    C = 10 * np.cumprod(1 + rng.normal(0, 0.01, 40)); Hh = C * 1.01; L = C * 0.99
    df = pd.DataFrame({"Open": C, "High": Hh, "Low": L, "Close": C, "Volume": 1.0}, index=idx)
    Pb = {"P": {"tarih": idx, "sembol": ["A"]}, "Vd": {"V": {"A": df}}}
    RET, ATP = U2.uc2_ret_atrp(Pb, 20)
    assert abs(RET[5, 0] - (C[5] / C[4] - 1)) < 1e-12
    pC = np.r_[np.nan, C[:-1]]; TR = np.where(np.isfinite(pC), np.maximum(Hh, pC) - np.minimum(L, pC), Hh - L)
    # satır 25'teki ATRP = bar 24'ün (önceki) ATR20 / C24: bar 5..24 TR ortalaması
    assert abs(ATP[25, 0] - TR[5:25].mean() / C[24]) < 1e-12
    assert np.isnan(ATP[19, 0]) and np.isfinite(ATP[20, 0])
    # geleceğe bakma: bar 25'i değiştirmek satır 25'in ATRP'sini değiştirmez
    df2 = df.copy(); df2.iloc[25, df2.columns.get_loc("High")] *= 3
    _, ATP2 = U2.uc2_ret_atrp({"P": Pb["P"], "Vd": {"V": {"A": df2}}}, 20)
    assert ATP2[25, 0] == ATP[25, 0] and ATP2[26, 0] != ATP[26, 0]


def test_es_dislama_c2():
    import CETVEL2 as C2
    n, u = 3, 9
    R = np.tile(np.arange(u, dtype=float) / 100, (n, 1)); KV = np.zeros((n, u), int)
    Pn = {"KV": KV, "R15": R}
    C2._c2_havuz(Pn)
    # olay j=0, gün 1; dışlanan j=1 (aynı gün E1) -> eş = j 2..8 ortalaması
    e = C2.c2_es(Pn, np.array([1]), np.array([0]), np.array([R[1, 0]]), np.array([1]), np.array([1]), es_min=5)
    assert abs(e["es_r15"][0] - R[1, 2:].mean()) < 1e-12 and e["n_es"][0] == 7
    # dışlanan başka gün -> etkisiz
    e = C2.c2_es(Pn, np.array([1]), np.array([0]), np.array([R[1, 0]]), np.array([2]), np.array([1]), es_min=5)
    assert e["n_es"][0] == 8


def test_e1_suzgec():
    tk = pd.bdate_range("2019-01-01", "2019-12-31")
    V = {s: pd.DataFrame({"Close": 1.0}, index=tk[(tk != pd.Timestamp("2019-05-02"))] if s == "BBB" else tk) for s in ("AAA", "AAB", "BBB")}
    Vd = {"V": V}
    K8 = pd.DataFrame({
        "accessionNumber": ["a1", "a2", "a3", "a4", "a5", "a6"],
        "filingDate": ["2019-02-01", "2019-02-10", "2019-04-30", "2019-05-01", "2019-03-01", "2019-06-03"],
        "acceptanceDateTime": ["2019-02-01T21:05:00.000Z", "2019-02-10T13:00:00.000Z", "2019-04-30T12:00:00.000Z",
                               "2019-05-01T20:30:00.000Z", "2019-03-01T12:00:00.000Z", "2019-06-03T12:00:00.000Z"],
        "form": ["8-K", "8-K", "8-K/A", "8-K", "8-K", "8-K"], "items": ["2.02,9.01", "2.02", "2.02", "2.02,9.01", "7.01,9.01", "2.02"],
        "reportDate": [""] * 6, "cik": [1, 1, 1, 2, 2, 3]})
    sc = {"AAA": 1, "AAB": 1, "BBB": 2}          # CIK 1 iki sınıf (AAA / AAB), CIK 3 sembolsüz
    E1, EX, say = U2.uc2_e1_ham(K8, sc, Vd, tk)
    # a1: 16:05 ET (EST) -> D0 02-02 (Cumartesi) -> t 02-04 Pazartesi; a2 (9 gün sonra) atılır; a3 8-K/A; a5 madde yok; a6 sembolsüz
    # a4: 2019-05-01 16:30 EDT -> D0 05-02 -> BBB'de 05-02 geçersiz bar -> düşer
    assert len(E1) == 1 and E1.sembol.iloc[0] == "AAA" and pd.Timestamp(E1.tarih.iloc[0]) == pd.Timestamp("2019-02-04"), E1
    assert say["tekrar_atilan_tum"] == 1 and say["olay_gunu_gecersiz_bar"] == 1 and say["cik_sembolsuz_satir"] == 1
    assert set(EX.sembol) == {"AAA", "AAB"}


def test_cik_sembol_secimi():
    V = {"X": pd.DataFrame(index=range(10)), "XA": pd.DataFrame(index=range(12)), "Y": pd.DataFrame(index=range(5)),
         "YB": pd.DataFrame(index=range(5))}
    sec, tum = U2.uc2_cik_sembol({"X": 1, "XA": 1, "Y": 2, "YB": 2, "Z": 3}, V)
    assert sec == {1: "XA", 2: "Y"} and tum == {1: ["X", "XA"], 2: ["Y", "YB"]}


def test_kesik():
    idx = pd.to_datetime(["2022-12-29", "2022-12-30", "2023-01-03"])
    V = {"A": pd.DataFrame({"Close": [1.0, 2.0, 3.0]}, index=idx), "B": pd.DataFrame({"Close": [1.0]}, index=pd.to_datetime(["2023-02-01"]))}
    W, say = U2.uc2_kes_fiyat(V)
    assert list(W) == ["A"] and W["A"].index.max() <= U2.UC2_KESIK and say["bos"] == 1 and say["atilan_satir"] == 2
    W2, _ = U2.uc2_kes_fiyat(V, bas="2022-12-30")
    assert len(W2["A"]) == 1
    with tempfile.TemporaryDirectory() as d:
        pickle.dump(V, open(os.path.join(d, "V_ABD.pkl"), "wb"))
        try:
            U2.uc2_kesik_kapi(d)
            raise AssertionError("kesik aşımı durdurmadı")
        except U2.UC2Hata:
            pass
        pickle.dump(W, open(os.path.join(d, "V_ABD.pkl"), "wb"))
        assert U2.uc2_kesik_kapi(d)["dosya"]


def test_hucre_uc_iz_ile_ayni():
    rng = np.random.default_rng(11); n = 240
    g = pd.bdate_range("2016-01-04", "2022-12-30"); gi = np.sort(rng.choice(len(g), n, replace=False))
    S = pd.DataFrame({"giris": g[gi], "r15": rng.normal(0.01, 0.08, n), "es_r15": rng.normal(0.0, 0.03, n), "sira": rng.uniform(0, 1, n),
                      "n_es": rng.integers(5, 60, n).astype(float)})
    S["fark"] = S.r15 - S.es_r15; S["donem"] = U.uc_donem(S.giris)
    tu, ta = U.uc_taban(S.n_es.to_numpy()); S["taban_ust10"] = tu; S["taban_alt10"] = ta
    u, a = U.uc_ust_alt(S.sira.to_numpy()); S["ust10"] = u; S["alt10"] = a
    m = rng.uniform(size=n) < 0.6
    PL = {"U": rng.uniform(size=(n, 20)) < 0.12, "A": rng.uniform(size=(n, 20)) < 0.12}
    PL = {k: v.astype(float) for k, v in PL.items()}
    for hc in ("d1619", "d2022"):
        a_ = U.uc_hucre(S, m, hc, 123, PL)
        b_ = U2.uc2_hucre(S, m, hc, 123, PL, U2.uc2_egri(15, hc))
        for k, v in a_.items():
            w = b_.get(k)
            if isinstance(v, float) and np.isnan(v):
                assert w is None or np.isnan(w), (hc, k)
            else:
                assert v == w or (isinstance(v, float) and abs(v - w) < 1e-12), (hc, k, v, w)


def test_cakisma_kapisi():
    kaynak = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "UC_IZ2.py"), encoding="utf-8").read()
    g = {"__name__": "uc_iz2_test", "uc2_b": object()}
    try:
        exec(compile(kaynak, "UC_IZ2.py", "exec"), g)
        raise AssertionError("çakışma kapısı durdurmadı")
    except RuntimeError as ex:
        assert "çakışma kapısı" in str(ex) and "uc2_b" in str(ex)
    g2 = {"__name__": "uc_iz2_test2"}
    exec(compile(kaynak, "UC_IZ2.py", "exec"), g2)      # temiz ad alanında geçer


def test_ua_sizinti_yok():
    kaynak = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "UC_IZ2.py"), encoding="utf-8").read()
    assert "@gmail" not in kaynak and "@hotmail" not in kaynak
    assert "print(ua" not in kaynak and "log.info(ua" not in kaynak.replace(" ", "")


if __name__ == "__main__":
    testler = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    hata = 0
    for t in testler:
        try:
            t(); print(f"GEÇTİ  {t.__name__}")
        except Exception as ex:   # bütün testler koşsun, sonda özet
            hata += 1; print(f"KALDI  {t.__name__}: {type(ex).__name__}: {ex}")
    print(f"{len(testler) - hata} / {len(testler)} test geçti")
    sys.exit(1 if hata else 0)
