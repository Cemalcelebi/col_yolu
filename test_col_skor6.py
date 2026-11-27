"""test_col_skor6 — COL_SKOR6 sentetik testleri (gerçek veri / sonuç görülmez; ağ yok).

Kapsam: altı ölçünün her biri elle hesaplanmış küçük örnekle ve iş tanımındaki (eski kod) formülün bağımsız döngü uygulamasıyla birebir; kırpma sınırları;
pencere sonrası barların ölçüleri etkilemediği; kitaplık fonksiyonunun bolge_bit'ten sonrasını okumadığı; ağırlıkların yalnız ABD 2016-19'dan öğrenildiği
(eski formül); ATRP içi KAT (elle + YO.yo_olc ile birebir); SAG10 / SOL10 / ATR2; ATRP20 = YO formülü; kesik assert; sonuç kapısı; uçtan uca sentetik
pazar (hazırla -> sayım -> sonuç -> keşif -> ölçüm -> özet -> rapor); çakışma kapısı.
Çalıştır: python test_col_skor6.py"""
import json
import os
import sys
import tempfile

import numpy as np
import pandas as pd

import COL_SKOR6 as CS
import YUKSELIS_ONCESI as YO

ISIM = []


def t(f):
    ISIM.append(f)
    return f


def _seri(m, tohum=1, son="2022-12-30", vol=1e5):
    r = np.random.default_rng(tohum); C = 10 * np.exp(np.cumsum(r.normal(0, 0.02, m)))
    O = C * (1 + r.normal(0, 0.008, m)); H = np.maximum(O, C) * (1 + np.abs(r.normal(0, 0.01, m))) + 1e-6
    L = np.minimum(O, C) * (1 - np.abs(r.normal(0, 0.01, m))) - 1e-6; V = vol * np.exp(r.normal(0, 0.5, m))
    ix = pd.bdate_range(end=son, periods=m)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=ix)


def _eski(d, s, t_):
    """İş tanımı 1. bölümündeki (eski kod) formüllerin bağımsız, döngülü uygulaması (pandas dilimleri)."""
    w = d.iloc[s:t_ + 1]; C = d.Close
    std = C.rolling(20).std(); sma = C.rolling(20).mean(); bbw = 4 * std / sma
    F1 = float(np.mean([abs(r.Close - r.Open) / (r.High - r.Low) < 0.40 for r in w.itertuples()]))
    b0 = bbw.iloc[s]; F2 = (b0 - bbw.iloc[s:t_ + 1].min()) / b0
    F3 = min(max(b0 / 0.6, 0), 1)
    hi, lo = w.High.max(), w.Low.min(); F4 = min(max(1 - (hi - lo) / ((hi + lo) / 2), 0), 1)
    m30 = d.High.iloc[s - 30:s].max(); F5 = min(max((m30 - lo) / m30, 0), 1)
    pv = d.Volume.iloc[max(0, s - 200):s]; F6 = min(max(1 - w.Volume.mean() / pv.mean(), 0), 1) if len(pv) >= 20 else np.nan
    return {"F1": F1, "F2": F2, "F3": F3, "F4": F4, "F5": F5, "F6": F6}


@t
def test_alti_olcu_eski_formul_birebir():
    d = _seri(400, 3)
    D = CS.cs_dizi(d.Open, d.High, d.Low, d.Close, d.Volume)
    for (s, t_) in [(30, 49), (100, 139), (150, 229), (250, 399), (35, 39), (210, 230)]:
        o = CS.cs_olcu(D, [s], [t_]); e = _eski(d, s, t_)
        for a in CS.CS_F:
            assert abs(o[a][0] - e[a]) < 1e-10, (a, s, t_, o[a][0], e[a])
        assert abs(o["PUAN_ESIT"][0] - 100 * np.mean([e[a] for a in CS.CS_F])) < 1e-8


@t
def test_elle_kucuk_ornek():
    m = 60; ix = pd.bdate_range("2020-01-01", periods=m)
    C = np.full(m, 10.0); C[:30] = np.linspace(14, 10.5, 30)            # sol bacak düşüş
    O = C.copy(); H = C + 0.2; L = C - 0.2; V = np.full(m, 100.0)
    s, t_ = 40, 49                                                      # pencere 10 bar
    O[s:t_ + 1] = C[s:t_ + 1] + np.array([0.01, 0.30, 0.05, 0.30, 0.10, 0.30, 0.15, 0.30, 0.20, 0.30])   # gövde / boy: 0,025 0,75 0,125 ...
    V[s:t_ + 1] = 50.0; H[35] = 13.0
    d = pd.DataFrame({"Open": O, "High": np.maximum(H, O + 0.01), "Low": np.minimum(L, O - 0.01), "Close": C, "Volume": V}, index=ix)
    D = CS.cs_dizi(d.Open, d.High, d.Low, d.Close, d.Volume); o = CS.cs_olcu(D, [s], [t_])
    gb = np.abs(d.Close - d.Open).to_numpy()[s:t_ + 1] / (d.High - d.Low).to_numpy()[s:t_ + 1]
    assert abs(o["F1"][0] - (gb < 0.40).mean()) < 1e-12 and abs(o["F1"][0] - 0.4) < 1e-12, (o["F1"], gb)
    hi = d.High.iloc[s:t_ + 1].max(); lo = d.Low.iloc[s:t_ + 1].min()
    assert abs(o["F4"][0] - (1 - (hi - lo) / ((hi + lo) / 2))) < 1e-12
    assert abs(o["F5"][0] - (13.0 - lo) / 13.0) < 1e-12                  # önceki 30 barın en yükseği H[35] = 13
    pv = d.Volume.iloc[0:s].mean(); assert abs(o["F6"][0] - (1 - 50.0 / pv)) < 1e-12


@t
def test_kirpma_sinirlari():
    m = 300; ix = pd.bdate_range("2019-01-01", periods=m); r = np.random.default_rng(5)
    C = np.r_[np.full(150, 10.0) * np.exp(r.normal(0, 0.3, 150)), np.linspace(10, 80, 150)]        # çok oynak -> BBW > 0,6
    O = C * 1.01; H = np.maximum(C, O) * 1.6; L = np.minimum(C, O) * 0.4                              # aralık > orta -> F4 < 0
    V = np.r_[np.full(200, 10.0), np.full(100, 1000.0)]                                               # hacim artışı -> F6 < 0
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=ix)
    D = CS.cs_dizi(d.Open, d.High, d.Low, d.Close, d.Volume)
    o = CS.cs_olcu(D, [230, 60], [299, 99])
    for a in CS.CS_F:
        v = o[a][np.isfinite(o[a])]; assert ((v >= 0) & (v <= 1)).all(), (a, v)
    assert o["F4"][0] == 0.0 and o["F6"][0] == 0.0
    C2 = np.linspace(10, 40, m); d2 = pd.DataFrame({"Open": C2, "High": C2 * 1.001, "Low": C2 * 0.999, "Close": C2, "Volume": 1.0}, index=ix)
    D2 = CS.cs_dizi(d2.Open, d2.High, d2.Low, d2.Close, d2.Volume)
    assert CS.cs_olcu(D2, [200], [239])["F5"][0] == 0.0                         # yükselişte pencere dibi önceki 30 barın tepesinin üstünde -> 0
    assert CS.cs_olcu(D, [60], [99])["F3"][0] == 1.0 or CS.cs_bbw(C)[60] < 0.6
    e = CS.cs_olcu(D, [29], [60])                                                    # ön şart s >= 30
    assert all(np.isnan(e[a][0]) for a in CS.CS_F)


@t
def test_pencere_sonrasi_etkisiz():
    d = _seri(500, 7); D = CS.cs_dizi(d.Open, d.High, d.Low, d.Close, d.Volume)
    s = np.array([50, 120, 300]); t_ = s + 39
    o1 = CS.cs_olcu(D, s, t_)
    for k in range(len(s)):
        d2 = d.copy(); d2.iloc[t_[k] + 1:] = d2.iloc[t_[k] + 1:] * 7.3; d2.iloc[t_[k] + 1:, 4] = 1e9
        D2 = CS.cs_dizi(d2.Open, d2.High, d2.Low, d2.Close, d2.Volume); o2 = CS.cs_olcu(D2, s[k:k + 1], t_[k:k + 1])
        for a in CS.CS_F + ["PUAN_ESIT"]:
            assert abs(o1[a][k] - o2[a][0]) < 1e-12, (a, k)
    a1 = CS.cs_atrp20(d.High, d.Low, d.Close); d3 = d.copy(); d3.iloc[201:] *= 3
    assert np.allclose(a1[:201], CS.cs_atrp20(d3.High, d3.Low, d3.Close)[:201], equal_nan=True)


@t
def test_kitaplik_bitis_sonrasi_okunmaz():
    d = _seri(700, 11, son="2025-12-31"); bas, bit = "2025-06-02", "2025-07-15"
    r1 = CS.cs_kitaplik_bolge(d, bas, bit)
    ek = pd.DataFrame({"Open": 1e6, "High": 2e6, "Low": 1.0, "Close": 1e6, "Volume": 1e12}, index=pd.bdate_range("2025-07-16", periods=50))
    d2 = d.copy(); d2.loc[d2.index > pd.Timestamp(bit)] = [1e6, 2e6, 1.0, 1e6, 1e12]
    r2 = CS.cs_kitaplik_bolge(pd.concat([d[d.index <= bit], ek]), bas, bit); r3 = CS.cs_kitaplik_bolge(d2, bas, bit)
    for a in CS.CS_F + ["PUAN_ESIT", "bar", "L"]:
        assert r1[a] == r2[a] == r3[a], (a, r1[a], r2[a], r3[a])
    assert r1["son"] <= bit and r1["durum"] == "tamam"
    # bağımsız: tam seri bit'te kesilip eski formülle
    x = d[d.index <= bit]; ix = np.flatnonzero((x.index >= bas)); e = _eski(x, int(ix[0]), int(ix[-1]))
    for a in CS.CS_F:
        assert abs(r1[a] - e[a]) < 1e-10
    yok = CS.cs_kitaplik_bolge(d, "2030-01-01", "2030-02-01"); assert yok["durum"] == "veri yok"
    kisa = CS.cs_kitaplik_bolge(d.iloc[:40], d.index[10], d.index[20]); assert kisa["durum"] == "veri yok"
    # L*: en yakın
    assert min(CS.CS_L, key=lambda L: (abs(5 - L), L)) == 20 and min(CS.CS_L, key=lambda L: (abs(190 - L), L)) == 80
    assert min(CS.CS_L, key=lambda L: (abs(30 - L), L)) == 20 and min(CS.CS_L, key=lambda L: (abs(61 - L), L)) == 80


@t
def test_kitaplik_listesi_aynen():
    K = CS.CS_KITAPLIK
    assert len(K) == 20 and K[0] == ("BINBN", "2024-12-23", "2025-01-22") and K[7] == ("TEHOL", "2026-01-26", "2026-03-02")
    assert K[-1] == ("KRVGD", "2025-04-01", "2025-09-01") and K[12] == ("EUREN", "2026-04-01", "2026-04-07")


@t
def test_agirlik_eski_formul_ve_kapi():
    r = np.random.default_rng(2); n = 4000
    F = {a: r.random(n) for a in CS.CS_F}; y = (F["F1"] + 0.3 * r.random(n) > 0.9).astype(float)
    w = CS.cs_agirlik(F, y)
    ham = {a: abs(F[a][y == 1].mean() - F[a][y == 0].mean()) / F[a].std() for a in CS.CS_F}
    tt = sum(ham.values())
    for a in CS.CS_F:
        assert abs(w[a] - ham[a] / tt) < 1e-12
    assert abs(sum(w.values()) - 1) < 1e-12 and max(w, key=w.get) == "F1"
    po = CS.cs_puan_ogr(F, w); assert abs(po[0] - 100 * sum(w[a] * F[a][0] for a in CS.CS_F)) < 1e-10
    X = pd.DataFrame({"hucre": ["ABD|d1619", "ABD|d2022"]})
    try:
        CS.cs_kesif_hesap(X, pd.DataFrame({"SAG10": [1.0, 0.0]}), {})
    except CS.CSHata as ex:
        assert "yalnız ABD 2016-19" in str(ex)
    else:
        raise AssertionError("ağırlık kapısı çalışmadı")


@t
def test_atrp_ici_kat_elle_ve_yo_birebir():
    # elle: iki beşlik, uçlar yüksek oynaklıkta
    q = np.array([0] * 50 + [1] * 50); Y = np.r_[np.zeros(45), np.ones(5), np.zeros(30), np.ones(20)]
    uc = np.zeros(100, bool); uc[[80, 81, 82, 83, 98, 99]] = True; D = np.zeros(100); TF = np.zeros(100); ay = np.array(["2017-01", "2017-02"] * 50)
    o = CS.cs_olc(uc, q, Y, D, TF, ay, "elle", B=50, nq=2)
    assert abs(o["KAT"] - (6 / (6 * 0.4))) < 1e-12 and abs(o["KAT_HAM"] - 1.0 / 0.25) < 1e-12
    r = np.random.default_rng(9); N = 5000
    q = r.integers(0, 5, N); Y = (r.random(N) < 0.1 + 0.05 * q).astype(float); D = (r.random(N) < 0.12).astype(float)
    TF = r.normal(0, 0.05, N); ay = np.array([f"20{16 + i % 4}-{1 + i % 12:02d}" for i in range(N)]); uc = r.random(N) < 0.1
    a = CS.cs_olc(uc, q, Y, D, TF, ay, "x", B=200); b = YO.yo_olc(uc, q, Y, D, TF, ay, "x", B=200)
    for k in ("n", "P_uc", "P_taban", "P_beklenen", "KAT_HAM", "KAT", "ASIMETRI", "TOPLAM_FARK", "ay"):
        assert abs(a[k] - b[k]) < 1e-12, (k, a[k], b[k])
    c = CS.cs_olc(uc, q, Y, D, TF, ay, "x", B=200); assert c["KAT_alt"] == a["KAT_alt"]          # tohum tekrarlanabilir


@t
def test_sonuc_dizi_elle():
    m = 60; C = np.full(m, 100.0); O = C.copy(); H = C + 1; L = C - 1
    H[25] = 111.0; L[28] = 89.0                                                     # t = 20: SAG10 (25) ve SOL10 (28)
    dep = {"O": O, "H": H, "L": L, "C": C, "POS": np.arange(m), "off": np.array([0, m])}
    r = CS.cs_sonuc_dizi(dep, np.array([0, 0]), np.array([20, 30]), np.array([0.02, 0.02]))
    assert r["SAG10"].tolist() == [1.0, 0.0] and r["SOL10"].tolist() == [1.0, 0.0]
    assert abs(r["R15"][0] - (C[35] / O[21] - 1)) < 1e-12
    assert r["ATR2_YUK"][0] == 1.0 and r["ATR2_ASG"][0] == 0.0                       # +%4 hedefi 25'te, -%2 stop 28'de (sonra)
    H2 = H.copy(); H2[22] = 104.5; L2 = L.copy(); L2[22] = 97.5                     # aynı bar: stop önce
    r2 = CS.cs_sonuc_dizi({**dep, "H": H2, "L": L2}, np.array([0]), np.array([20]), np.array([0.02]))
    assert r2["ATR2_YUK"][0] == 0.0
    try:
        CS.cs_sonuc_dizi(dep, np.array([0]), np.array([45]), np.array([0.02]))
    except CS.CSHata:
        pass
    else:
        raise AssertionError("sonuç penceresi aşımı yakalanmadı")


@t
def test_atrp20_yo_birebir():
    d = _seri(300, 4)
    a = CS.cs_atrp20(d.High, d.Low, d.Close)
    b = YO.yo_hisse_ozellik(d.Open.to_numpy(), d.High.to_numpy(), d.Low.to_numpy(), d.Close.to_numpy(), np.ones(300))["ATRP20"]
    assert np.allclose(a, b, equal_nan=True)


@t
def test_kesik_assert():
    try:
        CS.cs_kesik_kapi({"X": _seri(50, 1, son="2023-01-10")}, "deneme")
    except CS.CSHata as ex:
        assert "KESİK" in str(ex)
    else:
        raise AssertionError("kesik kapısı çalışmadı")
    CS.cs_kesik_kapi({"X": _seri(50, 1)}, "deneme")


@t
def test_sonuc_kapisi():
    X = pd.DataFrame({"hucre": ["AVR|d1619"], "uygun": [True], "j": [0], "t": [0], "ATRP20": [0.02], "d_row": [1]})
    for p, X_ in (("AVR", X), ("ABD", X.assign(hucre="ABD|d2022"))):
        try:
            CS.cs_sonuc(p, X_, "kesif", depo={})
        except CS.CSHata as ex:
            assert "SIRA" in str(ex)
        else:
            raise AssertionError("keşif sonuç kapısı çalışmadı")


def _pazar(n_hisse, tohum, son="2022-12-30", m=1900):
    V = {f"S{i:03d}": _seri(m, tohum + i, son=son, vol=1e5 * (1 + i)) for i in range(n_hisse)}
    for i, d in enumerate(V.values()):                            # bazı çöller: dar aralık, küçük mum, hacim düşüşü
        a = 400 + 37 * i
        c = float(d.Close.iloc[a - 1])
        d.iloc[a:a + 40, 3] = c * (1 + 0.002 * np.sin(np.arange(40))); d.iloc[a:a + 40, 0] = d.iloc[a:a + 40, 3] * 1.0005
        d.iloc[a:a + 40, 1] = d.iloc[a:a + 40, 3] * 1.004; d.iloc[a:a + 40, 2] = d.iloc[a:a + 40, 3] * 0.996; d.iloc[a:a + 40, 4] *= 0.2
    return {"V": V, "gecersiz": {s: pd.DatetimeIndex([]) for s in V}}


@t
def test_uctan_uca_sentetik():
    tmp = tempfile.mkdtemp(prefix="cs_test_"); ham = os.path.join(tmp, "ham"); cikti = os.path.join(tmp, "cikti"); os.makedirs(cikti)
    VD = {"ABD": _pazar(14, 100), "AVR": _pazar(10, 300), "BIST": _pazar(10, 500)}
    for p, Vd in VD.items():
        S = sorted(Vd["V"]); idx = pd.DatetimeIndex(sorted(set().union(*[d.index for d in Vd["V"].values()])))
        P2 = None
        if p != "BIST":
            P2 = np.ones((len(idx), len(S)), bool)
        CS.cs_hazirla_pazar(p, ham, Vd=Vd, P2=P2, idx=idx, S=S)
    S, _ = CS.cs_sayim_kos(ham, kitaplik=False)
    assert S["hucre"]["ABD|d1619|40"]["n"] > 0 and set(S["kesim"]) == {f"{p}|{L}" for p in CS.CS_PAZAR for L in CS.CS_L}
    XS = {p: CS.cs_yukle(p, ham) for p in CS.CS_PAZAR}
    X = XS["ABD"]
    # pencere sonu her 5 barda; ölçüler panelde cs_olcu ile aynı
    assert (X.t % 5 == 0).all()
    r = X[np.isfinite(X.F1_40)].iloc[3]; d = VD["ABD"]["V"][r.sembol]
    e = _eski(d, int(r.t) - 39, int(r.t))
    for a in CS.CS_F:
        assert abs(float(r[f"{a}_40"]) - e[a]) < 1e-5
    # kitaplık dağılımı
    dag = CS.cs_dagilim_bist(XS["BIST"]); assert len(dag[40]["PUAN_ESIT"]) > 0
    tam = {"V": {"S001": VD["BIST"]["V"]["S001"]}, "gecersiz": {}}
    KT = CS.cs_kitaplik(dag, tam=tam); assert KT["ozet"]["veri_var"] == 0 and len(KT["satir"]) == 20
    # keşif: yalnız ABD|d1619
    Xk = X[(X.hucre == "ABD|d1619") & X.uygun & X.EVREN]
    Sk = CS.cs_sonuc("ABD", Xk, "kesif", ham)
    K = CS.cs_kesif_hesap(Xk, Sk, XS); K["getirisiz"] = S["kesim"]
    assert abs(sum(K["agirlik"]["40"][a] for a in CS.CS_F) - 1) < 1e-12
    # ölçüm
    XX, SS = {}, {}
    for p in CS.CS_PAZAR:
        Xp = XS[p]; Xp = Xp[Xp.uygun & Xp.EVREN & Xp.hucre.str.split("|").str[1].isin(CS.CS_DONEM)]
        XX[p] = Xp; SS[p] = CS.cs_sonuc(p, Xp, "test", ham)
    R = CS.cs_olcum_hesap(XX, SS, K, B=50)
    assert len(R["satir"]) == 48 and set(R["hukum"].values()) <= {"ÖLÇÜLEMEDİ", "TUTAR", "YALNIZ OYNAKLIK", "TEK DÖNEM", "TERS", "TUTMADI"}
    assert all(v == "ÖLÇÜLEMEDİ" for v in R["hukum"].values())          # küçük sentetik pazar: n < 1000
    # bağımsız yeniden üretim (bir hücre): ham KAT ve taban
    p, L = "ABD", 40; Xp = XX[p]; m = CS.cs_pop(Xp, L) & (Xp.hucre == "ABD|d2022").to_numpy()
    x = Xp[f"F1_{L}"].to_numpy(float)[m]; y = SS[p].SAG10.to_numpy(float)[m]; uc = x >= K["getirisiz"]["ABD|40"]["F1"]["uc10"]
    o = R["satir"]["F1|uc10|40"]["ABD|d2022"]; assert o["n"] == int(uc.sum()) and abs(o["P_taban"] - y.mean()) < 1e-12
    # özet + rapor
    J = {"zaman": "t", "kapi": {"onkayit_commit": "x", "kontrol": {"gecti": True}}, "kesim_kapi": {"cs_kesim.json": "y"}, "agirlik": K["agirlik"], **R}
    with open(os.path.join(cikti, "cs_sonuc.json"), "w", encoding="utf-8") as f:
        json.dump(CS.MI._mi_json(J), f, ensure_ascii=False)
    CS.MI._mi_jyaz(os.path.join(ham, "kitaplik.json"), {**KT, "dagilim_n": {"20": 1, "40": 1, "80": 1}}, "k")
    CS.cs_ozet_csv(J, os.path.join(cikti, "cs_ozet.csv"))
    yol = CS.cs_rapor_yaz(cikti, ham, yeniden=["deneme"]); metin = open(yol, encoding="utf-8").read()
    assert "KİTAPLIK TESPİTİ" in metin and "OLASILIK TABLOSU" in metin and "## HATA" in metin and "ÖNERİLEN DEFTER SATIRLARI" in metin
    md = CS.cs_kesim_md({**K, "zaman": "t", "onkayit_commit": "x", "CS_KOD_SHA": "a", "CS_ESIK_SHA": "b"}, "s"); assert "KESIM_SHA: s" in md


@t
def test_cakisma_kapisi():
    kod = open(CS.CS_YOL["kod"], encoding="utf-8").read()
    ns = {"__name__": "cs_test", "__file__": CS.__file__}
    exec(compile(kod, "COL_SKOR6.py", "exec"), ns)
    ns2 = {"__name__": "cs_test2", "__file__": CS.__file__, "cs_kapi": 1}
    try:
        exec(compile(kod, "COL_SKOR6.py", "exec"), ns2)
    except RuntimeError as ex:
        assert "çakışma" in str(ex)
    else:
        raise AssertionError("çakışma kapısı çalışmadı")


@t
def test_esik_sabit():
    E = CS.CS_ESIK
    assert E["tohum"] == 2713 and E["boot"]["B"] == 10000 and E["kesim"]["uc"] == [0.10, 0.02] and E["hukum"]["n_min"] == 1000 and E["bh"]["q"] == 0.10
    assert E["olcu"]["doji_esik"] == 0.40 and E["olcu"]["bbw_bolen"] == 0.6 and E["olcu"]["sol"] == 30 and E["olcu"]["hacim_onceki"] == 200
    assert E["pencere"]["L"] == [20, 40, 80] and E["pencere"]["adim"] == 5 and set(CS.CS_KONTROL) == {f"K{i}" for i in range(1, 15)}


if __name__ == "__main__":
    hata = 0
    for f in ISIM:
        try:
            f(); print("GEÇTİ", f.__name__)
        except Exception as ex:  # noqa: BLE001
            hata += 1; print("KALDI", f.__name__, type(ex).__name__, ex)
            import traceback; traceback.print_exc()
    print(f"{len(ISIM) - hata}/{len(ISIM)} geçti")
    sys.exit(1 if hata else 0)
