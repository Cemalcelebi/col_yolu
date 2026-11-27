"""test_goz_tespit — GOZ_TESPIT sentetik testleri (gerçek veri / sonuç görülmez; ağ yok).

Kapsam: ek bölge içi ölçülerin elle hesaplanmış küçük örneği; içe alınan ölçülerin kaynak modüllerle birebir olduğu; hiçbir ölçü / kitaplık / sayfa
fonksiyonunun bölge bitişinden sonraki barı okumadığı (bozunca aynı); kitaplık bölgelerinin ve örtüşen pencerelerin havuzdan çıktığı; sayfada sonrası
çizilmediği; onay seti kol sayıları (6 / 8 / 6 / 6 / 4) ve karışık sıra tohumu 2715; aynı girdi -> aynı PDF sha; PDF metninde kol / hisse / tarih yok;
yüzdelik / tutarlılık / D2 sınırı / tekilleştirme / AUC elle; çakışma kapısı; eşik sözlüğü sabit.
Çalıştır: python test_goz_tespit.py"""
import os
import sys
import tempfile

import numpy as np
import pandas as pd

import GOZ_TESPIT as GT
import COL_SKOR6 as CS
import MUM_IZI_UC as UC
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


def _P(d):
    return GT.gt_on(d, np.ones(len(d)))


@t
def test_ek_olcu_elle():
    # 6 barlık elle örnek: pencere s = 25 .. t = 30 (önceki 25 bar hacmi 10)
    n = 31; C = np.full(n, 10.0); O = C.copy(); H = C + 0.5; L = C - 0.5; V = np.full(n, 10.0)
    C[25:31] = [10, 9, 9.2, 9.1, 9.6, 9.5]; O[25:31] = C[25:31]; H[25:31] = C[25:31] + 0.2; L[25:31] = C[25:31] - 0.2
    L[26] = 8.7; V[25:31] = [5, 5, 5, 5, 10, 10]
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=pd.bdate_range("2020-01-01", periods=n))
    P = _P(d); s, t_ = 25, 30
    o = GT.gt_ek_olcu(P, [s], [t_])
    assert abs(o["DIP_YER"][0] - 1 / 5) < 1e-12                           # dip (8,7) 2. barda: 1 / (6 - 1)
    atr = P["YO"]["ATRP20"][t_] * C[t_]; dip = 8.7
    bek = np.mean([C[i] <= dip + 0.5 * atr for i in range(s, t_ + 1)])
    assert abs(o["DIP_DOKUNMA"][0] - bek) < 1e-12
    hi = max(H[s:t_ + 1]); assert abs(o["SON_KONUM"][0] - (9.5 - 8.7) / (hi - 8.7)) < 1e-12
    assert o["BOLGE_L"][0] == 6
    assert abs(o["YUK_KAPANIS"][0] - 2 / 6) < 1e-12                     # 9,2 > 9 ve 9,6 > 9,1
    assert abs(o["HACIM_ORAN"][0] - (40 / 6) / 10) < 1e-12               # önceki 25 bar (>= 20) ortalama 10
    assert abs(o["HACIM_SON5"][0] - (35 / 5) / (40 / 6)) < 1e-12
    o2 = GT.gt_ek_olcu(P, [10], [15])                                      # önceki 10 bar (< 20): hacim oranı yok
    assert not np.isfinite(o2["HACIM_ORAN"][0])


@t
def test_icerilen_olculer_kaynakla_birebir():
    d = _seri(600, 3); P = _P(d); s = np.array([150, 200, 300, 400]); tt = np.array([169, 239, 379, 450])
    o = GT.gt_olcu(P, s, tt); c = CS.cs_olcu(P["CS"], s, tt)
    for a in CS.CS_F + ["PUAN_ESIT"]:
        assert np.allclose(o[a], c[a], equal_nan=True), a
    for i in range(len(s)):
        u = UC.uc_olcu(P["UC"], [tt[i]], tt[i] - s[i] + 1)
        for a in GT.GT_UC_AD:
            assert np.allclose(o[a][i], u[a][0], equal_nan=True), a
    Y = YO.yo_hisse_ozellik(*(d[c_].to_numpy(float) for c_ in ("Open", "High", "Low", "Close")), np.ones(len(d)))
    for a in GT.GT_YO_AD:
        if a != "OYN_SIRA":
            assert np.allclose(o[a], Y[a][tt], equal_nan=True), a
    assert len(GT.GT_OLCU_AD) == 40 and len(set(GT.GT_OLCU_AD)) == 40
    o3 = GT.gt_olcu(P, [100], [119])                                       # s < 120: MUM_IZI_UC ölçüleri boş (tanım AYNEN)
    assert all(not np.isfinite(o3[a][0]) for a in GT.GT_UC_AD) and np.isfinite(o3["F1"][0])


@t
def test_olcu_bitis_sonrasi_okunmaz():
    d = _seri(500, 5); s, t_ = 300, 359
    a = GT.gt_olcu(_P(d), [s], [t_])
    d2 = d.copy(); d2.iloc[t_ + 1:] = d2.iloc[t_ + 1:] * 7.3; d2.iloc[t_ + 1:, 4] = 1.0
    b = GT.gt_olcu(_P(d2), [s], [t_])
    for k in a:
        assert np.allclose(a[k], b[k], equal_nan=True), k


def _V(n_hisse=35, m=420, son="2026-04-30"):
    return {f"H{i:02d}": _seri(m, 100 + i, son=son) for i in range(n_hisse)}


@t
def test_kitaplik_bolge_kesilir_bozunca_ayni():
    V = _V(); sem = "H03"; d = V[sem]; bas = str(d.index[300].date()); bit = str(d.index[340].date())
    r1 = GT.gt_kitaplik_bolge(V, {}, sem, bas, bit)
    V2 = {}
    for k, x in V.items():
        y = x.copy(); y.loc[y.index > pd.Timestamp(bit)] = y.loc[y.index > pd.Timestamp(bit)] * 3.1; V2[k] = y
    r2 = GT.gt_kitaplik_bolge(V2, {}, sem, bas, bit)
    assert r1["durum"] == "tamam" and r1["bar"] == 41 and r1["L"] == 40 and r1["son"] == bit
    for k in GT.GT_OLCU_AD + ["PUAN_ESIT"]:
        assert (r1[k] is None and r2[k] is None) or abs(r1[k] - r2[k]) < 1e-12, k
    assert r1["OYN_SIRA"] is not None
    assert GT.gt_kitaplik_bolge(V, {}, "YOK", bas, bit)["durum"] == "veri yok"


@t
def test_havuz_kitaplik_ve_ortusenler_cikar():
    ix = pd.bdate_range("2019-01-01", periods=400); n = 6
    X = pd.DataFrame({"sembol": ["A", "A", "A", "B", "B", "C"], "t": [200, 230, 300, 210, 330, 250], "s": [181, 191, 221, 171, 251, 211],
                      "L": [20, 40, 80, 40, 80, 40]})
    X["tarih"] = ix[X.t]; X["bas_tarih"] = ix[X.s]
    X["KIL"] = 0.0; X["PUAN_ESIT"] = 50.0; X["govdesiz_pay"] = 0.0; X["F5"] = 0.5
    haric = pd.DataFrame([{"sembol": "A", "bas": str(ix[195].date()), "son": str(ix[205].date()), "kaynak": "kitaplik"},
                          {"sembol": "B", "bas": str(ix[340].date()), "son": str(ix[360].date()), "kaynak": "mumizi"}])
    o = GT.gt_ortusme(X, haric[haric.kaynak == "kitaplik"])
    assert o.tolist() == [True, True, False, False, False, False]
    m, say = GT.gt_havuz_maske(X, ["F5"], haric)
    assert m.tolist() == [False, False, True, True, True, True] and say["kitaplik_ortusen"] == 2 and say["mumizi_ortusen"] == 0
    X.loc[4, "bas_tarih"] = ix[345]; X.loc[4, "tarih"] = ix[350]; m2, say2 = GT.gt_havuz_maske(X, ["F5"], haric)
    assert not m2[4] and say2["mumizi_ortusen"] == 1
    X.loc[5, "govdesiz_pay"] = 0.5; X.loc[3, "s"] = 100
    m3, _ = GT.gt_havuz_maske(X, ["F5"], haric)
    assert not m3[5] and not m3[3] and m3[2]


@t
def test_sayfa_sonrasi_cizilmez_ve_ayni_sha():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    d = _seri(400, 7); s, t_ = 250, 289
    fig = plt.figure(figsize=(8.3, 14.5)); o = GT.gt_sayfa(fig, d, s, t_, 1); plt.close(fig)
    assert o["son_bar_index"] == t_ and o["seri_uzunluk_kullanilan"] == t_ + 1
    assert o["uzak"]["pencere_bar"] == 120 + (t_ - s + 1) and o["uzak"]["kutu"] == [120, 120 + t_ - s]
    assert o["yakin"]["pencere_bar"] == 10 + (t_ - s + 1) and o["yakin"]["kutu"][1] == o["yakin"]["pencere_bar"] - 1
    d2 = d.copy(); d2.iloc[t_ + 1:] = d2.iloc[t_ + 1:] * 5
    sf = [{"sayfa": 1, "pazar": "ABD", "sembol": "ZZTOPX", "s": s, "t": t_, "kaynak": "acik"}]
    with tempfile.TemporaryDirectory() as k:
        a = GT.gt_pdf(os.path.join(k, "a.pdf"), sf, lambda p, x, y: d)
        b = GT.gt_pdf(os.path.join(k, "b.pdf"), sf, lambda p, x, y: d)
        c = GT.gt_pdf(os.path.join(k, "c.pdf"), sf, lambda p, x, y: d2)
        assert a["sha"] == b["sha"] == c["sha"], "aynı girdi (ve bölge sonrası bozulmuş girdi) aynı PDF vermeli"
        GT.gt_pdf_denetim(os.path.join(k, "a.pdf"), ["ZZTOPX"])
        m = GT.gt_pdf_metin(os.path.join(k, "a.pdf"))
        assert "✓" in m or "çöl" in m and "kısmen" in m and "değil" in m
    try:
        GT.gt_sayfa(plt.figure(), d, 20, 40, 1)
    except GT.GTHata:
        pass
    else:
        raise AssertionError("önceki < 40 bar durmalı")


@t
def test_pdf_denetim_yasak_metni_yakalar():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    with tempfile.TemporaryDirectory() as k:
        for yazi in ("ZZTOPX", "2021-03-04", "D2 kol", "RASTGELE"):
            y = os.path.join(k, "x.pdf")
            with PdfPages(y) as pdf:
                fig = plt.figure(); fig.text(0.1, 0.5, f"Sayfa 3 {yazi}"); pdf.savefig(fig); plt.close(fig)
            try:
                GT.gt_pdf_denetim(y, ["ZZTOPX"])
            except GT.GTHata:
                pass
            else:
                raise AssertionError(f"yasak metin yakalanmadı: {yazi}")


def _aday(n=60, pazar="BIST"):
    ix = pd.bdate_range("2017-01-02", periods=2000); r = np.random.default_rng(len(pazar))
    def tab(kol, k):
        rows = []
        for i in range(k):
            t_ = 300 + 3 * i; L = [20, 40, 80][i % 3]
            rows.append({"sembol": f"{pazar[:1]}{kol}{i:03d}", "t": t_, "s": t_ - L + 1, "L": L, "tarih": ix[t_], "bas_tarih": ix[t_ - L + 1],
                         "PUAN_ESIT": 50.0, "PUAN_ESIT_r": 0.95, "skor": 1 - i / 1000, **({"kitaplik_no": i + 1} if kol == "D3" else {})})
        return pd.DataFrame(rows)
    h = tab("H", 400)
    return {"D1": tab("D1", n), "D2": tab("D2", n), "D3": tab("D3", 16), "havuz": h}


def _kit():
    return [{"no": i + 1, "sembol": f"K{i:02d}", "s": 200 + i, "t": 230 + i, "bar": 31, "ilk": "2025-01-01", "son": "2025-02-01", "bit": "2025-02-02"}
            for i in range(16)]


@t
def test_onay_kol_sayilari_ve_tohum():
    A = {"BIST": _aday(pazar="BIST"), "ABD": _aday(pazar="ABD")}
    s1, y1 = GT.gt_onay_sec(A, _kit()); s2, y2 = GT.gt_onay_sec(A, _kit())
    assert y1["kol"] == {"D1": 6, "D2": 8, "D3": 6, "RASTGELE": 6, "KITAPLIK": 4} and y1["toplam"] == 30
    assert y1["pazar"] == {"BIST": 17, "ABD": 13} and not y1["eksik"]
    assert [r["sayfa"] for r in s1] == list(range(1, 31))
    assert [(r["kol"], r["sembol"]) for r in s1] == [(r["kol"], r["sembol"]) for r in s2], "tohum 2715 ile aynı sıra"
    assert len({(r["pazar"], r["sembol"]) for r in s1}) == 30, "her hisse bir kez"
    s3, _ = GT.gt_onay_sec(A, _kit(), tohum=1)
    assert [(r["kol"], r["sembol"]) for r in s3] != [(r["kol"], r["sembol"]) for r in s1]
    assert GT.GT_ESIK["tohum"] == 2715
    rng = np.random.default_rng(2715); uy = _kit(); k = sorted(rng.choice(len(uy), 4, replace=False).tolist())
    assert sorted(r["kitaplik_no"] for r in s1 if r["kol"] == "KITAPLIK") == [uy[i]["no"] for i in k]
    for r in s1:                                                          # dedektör sayfaları sıralamanın en üstünden
        if r["kol"] in ("D1", "D2"):
            assert int(r["sembol"][-3:]) < 8
    Ls = sorted(r["L"] for r in s1 if r["kol"] == "RASTGELE")
    assert all(L in (20, 40, 80) for L in Ls)


@t
def test_d2_eksik_rastgeleye_eklenmez():
    A = {"BIST": _aday(pazar="BIST"), "ABD": _aday(pazar="ABD")}
    A["BIST"]["D2"] = A["BIST"]["D2"].head(2); A["ABD"]["D2"] = A["ABD"]["D2"].head(3)
    s, y = GT.gt_onay_sec(A, _kit())
    assert y["kol"]["D2"] == 5 and y["eksik"] == {"D2|BIST": 2, "D2|ABD": 1}, y
    assert y["kol"]["RASTGELE"] == 6 and y["toplam"] == 27
    A["ABD"]["D2"] = _aday(pazar="ABD")["D2"]
    s, y = GT.gt_onay_sec(A, _kit())
    assert y["kol"]["D2"] == 8 and y["tasinan"].get("D2|BIST->ABD") == 2 and not y["eksik"]


@t
def test_yuzdelik_cs_ile_ayni():
    r = np.random.default_rng(3); dag = np.sort(np.round(r.normal(size=500), 2))
    for x in [-5, -0.3, 0.0, 0.12, 9]:
        assert abs(GT.gt_yuzdelik([x], dag)[0] - CS.cs_yuzdelik(float(x), dag)) < 1e-12
    assert GT.gt_Lyildiz(5) == 20 and GT.gt_Lyildiz(30) == 20 and GT.gt_Lyildiz(60) == 40 and GT.gt_Lyildiz(190) == 80


@t
def test_tutarlilik_ve_imza_elle():
    r = [0.9] * 12 + [0.5, 0.4, 0.2, 0.75]
    T = GT.gt_tutarlilik(r)
    assert T["yon"] == "YÜKSEK" and T["tut_k"] == 13 and abs(T["tut"] - 13 / 16) < 1e-12 and abs(T["medyan"] - 0.9) < 1e-12
    assert GT.gt_imza_aday(T, 16)
    T2 = GT.gt_tutarlilik([0.1] * 11 + [0.6] * 5)
    assert T2["yon"] == "DÜŞÜK" and T2["tut_k"] == 11 and not GT.gt_imza_aday(T2, 16)        # 11 / 16 < %75
    T3 = GT.gt_tutarlilik([0.1] * 11 + [None] * 5)
    assert T3["n"] == 11 and not GT.gt_imza_aday(T3, 16)                                      # ölçüsü olan 11 < 12
    T4 = GT.gt_tutarlilik([0.8] * 12 + [0.1] * 4)
    assert GT.gt_imza_aday(T4, 16)


@t
def test_d2_sinir_elle():
    q = [0.05, 0.3, 0.6, 0.71, 0.72, 0.8, 0.8, 0.85, 0.9, 0.9, 0.91, 0.95, 0.96, 0.97, 0.99, 1.0]
    s = GT.gt_d2_sinir(q, "YÜKSEK")
    assert s["n"] == 16 and s["k"] == 13 and abs(s["sinir_kitaplik"] - 0.71) < 1e-12 and abs(s["sinir"] - 0.71) < 1e-12
    assert sum(x >= s["sinir"] for x in q) == 13
    s2 = GT.gt_d2_sinir([1 - x for x in q], "DÜŞÜK")
    assert abs(s2["sinir_kitaplik"] - 0.71) < 1e-12
    s3 = GT.gt_d2_sinir([0.1, 0.2, 0.3, 0.9] * 4, "YÜKSEK")
    assert s3["sinir"] == 0.5                                                                  # taraf şartı 0,50
    assert GT.gt_d2_sinir([0.9] * 12 + [None] * 4, "YÜKSEK")["k"] == 10


@t
def test_tekil_elle():
    df = pd.DataFrame({"sembol": ["A", "A", "A", "A", "B"], "t": [100, 130, 180, 130, 100], "L": [20, 20, 40, 80, 20], "skor": [0.9, 0.95, 0.8, 0.96, 0.1]})
    g = GT.gt_tekil(df, "skor")
    assert sorted(zip(g.sembol, g.t, g.L)) == [("A", 130, 80), ("A", 180, 40), ("B", 100, 20)]
    g2 = GT.gt_tekil(df, "skor", artan=True)
    assert ("A", 100, 20) in set(zip(g2.sembol, g2.t, g2.L))


@t
def test_auc_elle():
    assert GT.gt_auc([3, 4], [1, 2]) == 1.0 and GT.gt_auc([1], [1]) == 0.5 and abs(GT.gt_auc([1, 3], [2, 2]) - 0.5) < 1e-12
    assert abs(GT.gt_auc([2, 3, np.nan], [1, 3]) - 0.625) < 1e-12


@t
def test_kesik_kapi():
    try:
        GT.gt_kesik_kapi({"A": _seri(50, son="2023-01-05")}, "x")
    except GT.GTHata:
        pass
    else:
        raise AssertionError("2022 sonrası veri durmalı")
    GT.gt_kesik_kapi({"A": _seri(50)}, "x")


@t
def test_cakisma_kapisi():
    kod = open(GT.GT_YOL["kod"], encoding="utf-8").read()
    ns = {"__name__": "gt_test", "__file__": GT.__file__}
    exec(compile(kod, "GOZ_TESPIT.py", "exec"), ns)
    ns2 = {"__name__": "gt_test2", "__file__": GT.__file__, "gt_onay": 1}
    try:
        exec(compile(kod, "GOZ_TESPIT.py", "exec"), ns2)
    except RuntimeError as ex:
        assert "çakışma" in str(ex)
    else:
        raise AssertionError("çakışma kapısı çalışmadı")


@t
def test_esik_sabit():
    E = GT.GT_ESIK
    assert E["tohum"] == 2715 and E["kol"] == {"D1": 6, "D2": 8, "D3": 6, "RASTGELE": 6, "KITAPLIK": 4}
    assert all(sum(v.values()) == E["kol"][k] for k, v in E["kol_pazar"].items())
    assert E["imza"]["tutarlilik"] == 0.75 and E["imza"]["rho"] == 0.80 and E["D1"]["ust"] == 0.90 and E["D2"]["gevsek"] == 0.20
    assert E["tekil"]["bar"] == 40 and E["sayfa"]["kutu"] == ["✓  çöl", "K  kısmen", "×  değil"] and E["sayim"]["tutuyor_pay"] == 0.70
    assert set(GT.GT_KONTROL) == {f"K{i}" for i in range(1, 15)}


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
