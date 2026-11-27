"""test_goz_tespit — GOZ_TESPIT sentetik testleri (gerçek veri / sonuç görülmez; ağ yok).

Kapsam: ek bölge içi ölçülerin elle hesaplanmış küçük örneği; içe alınan ölçülerin kaynak modüllerle birebir olduğu; hiçbir ölçü / kitaplık / sayfa
fonksiyonunun bölge bitişinden sonraki barı okumadığı (bozunca aynı); kitaplık bölgelerinin ve örtüşen pencerelerin havuzdan çıktığı; sayfada sonrası
çizilmediği; onay seti kol sayıları (6 / 8 / 6 / 6 / 4) ve karışık sıra tohumu 2715; aynı girdi -> aynı PDF sha; PDF metninde kol / hisse / tarih yok;
yüzdelik / tutarlılık / D2 sınırı / tekilleştirme / AUC elle; çakışma kapısı; eşik sözlüğü sabit.
ÇÖL-K2 (EK 5): beş şart goz2 ile birebir (sentetik), yapay pozitif / negatifler, dip parabolü yedi yapay tip, elle örnekler, sonrası okunmaz, sonrası kapısı.
ÇÖL-K2 KIRILIM (EK 6): yön kuralı elle (yukarı / aşağı / kırılmadı / aynı bar / kesik), izleme t + 20 ve 2022 sınırı, giriş = kırılımdan sonraki açılış,
simetrik ilk dokunuş ve belirsiz, tekil 15, kontrol pencereleri YER sağlamaz, kapı, karar anından sonrası okunmaz, karar elle, uçtan uca sentetik.
KURAL-3 (EK 8): DIPTEN_BAR elle (dip ilk / orta / son bar, eşit dipte ilk görülen), kolların ayrıklığı, D1 sırası evren içinde ve 2016-22 dışı veriyi
kullanmaz, şartlar bölge sonrasını okumaz, tekil 40, karar elle + kapı, uçtan uca sentetik (A + B + Kontrol 2 denetimi), GT5'in 21 sayfası (gerçek veri).
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


# ================================================================ ÇÖL-K2 (EK 5): beş şart
def _k2_seri(tip="poz", tohum=3):
    """Yapay seri: 100 bar düşüş (100 -> 41, iri mum) + 20 bar 41 civarı + 60 bar bölge (küçük mum; 3 ayrı taban dokunuşu; son 20 barda dip parabolü)."""
    r = np.random.default_rng(tohum)
    on = np.r_[np.linspace(100, 41, 100), np.full(20, 41.0)]
    if tip == "tepe":                                                  # tepede sıkışma: önce yükseliş
        on = np.r_[np.linspace(20, 41, 100), np.full(20, 41.0)]
    Lo = on - 1.0 - np.abs(r.normal(0, 0.2, 120)); Ho = on + 1.0 + np.abs(r.normal(0, 0.2, 120))
    Oo = on + 0.8 * np.where(np.arange(120) % 2, 1, -1); Co = on - 0.8 * np.where(np.arange(120) % 2, 1, -1)
    Lb = 39.0 + r.normal(0, 0.03, 60)
    for i in ((3, 17, 30) if tip != "tek" else (3,)):
        Lb[i] = 38.0 + 0.02 * r.random()
    x = np.linspace(-1, 1, 20); Lb[40:] = 38.95 + 0.9 * (x + 0.3) ** 2 + r.normal(0, 0.01, 20)
    if tip == "yenidip":
        Lb[-2] = 37.5
    boy = 2.4 if tip == "iri" else 0.6
    Hb = Lb + boy; Ob = Lb + 0.25 * boy + 0.05 * r.random(60); Cb = Lb + 0.3 * boy
    if tip == "iri":
        Ob = Lb + 0.1 * boy; Cb = Lb + 0.9 * boy
    O = np.r_[Oo, Ob]; H = np.r_[Ho, Hb]; L = np.r_[Lo, Lb]; C = np.r_[Co, Cb]
    H = np.maximum.reduce([H, O, C]); L = np.minimum.reduce([L, O, C])
    return O, H, L, C, 120, 179


@t
def test_k2_bes_sart_yapay_pozitif_ve_negatifler():
    o = GT.gt_k2(*_k2_seri("poz"))
    assert o["Y"] == o["M"] == o["S"] == o["B"] == o["Z"] == o["K2"] == o["YMSB"] == 1, o
    beklenen = {"iri": ("M", 0), "tek": ("S", 0), "yenidip": ("B", 0), "tepe": ("Y", 0)}
    for tip, (sart, deger) in beklenen.items():
        o = GT.gt_k2(*_k2_seri(tip)); assert o[sart] == deger and o["K2"] == 0, (tip, o)
    assert GT.gt_k2(*_k2_seri("tek"))["dokunus"] == 1
    assert GT.gt_k2(*_k2_seri("yenidip"))["Z"] == 0                    # sonda daha derin dip: parabol de yok
    for tohum in range(4, 24):                                         # gürültü tohumuna dayanıklı
        assert GT.gt_k2(*_k2_seri("poz", tohum))["K2"] == 1
        assert GT.gt_k2(*_k2_seri("tepe", tohum))["Y"] == 0 and GT.gt_k2(*_k2_seri("tek", tohum))["S"] == 0


@t
def test_k2_sart_elle():
    # dip savunması: dip 5, kutu 5 -> taban <= 6,25; dokunuşlar 0, 3, 7 (aralar >= 3) -> 3, yayılım 7 >= 0,25 x 12
    Lb = np.array([5, 9, 9, 5.5, 9, 9, 9, 5.2, 9, 9, 9, 9.0]); Hb = np.full(12, 10.0)
    assert GT.gt_k2_savunma(Lb, Hb) == (True, 3)
    Lb2 = Lb.copy(); Lb2[1] = 5.5                                        # 0 ve 1 bitişik: tek dokunuş sayılır
    assert GT.gt_k2_savunma(Lb2, Hb) == (True, 3)
    Lb3 = Lb.copy(); Lb3[7] = 9                                         # iki dokunuş
    assert GT.gt_k2_savunma(Lb3, Hb) == (False, 2)
    Lb4 = np.array([9, 9, 9, 9, 9, 5, 9, 9, 5.1, 9, 5.2, 9.0])         # 5, 8, 10: 10 - 8 = 2 < 3 -> 10 ayrı değil: 2 dokunuş
    assert GT.gt_k2_savunma(Lb4, Hb) == (False, 2)
    Lb4[10] = 9; Lb4[11] = 5.2; assert GT.gt_k2_savunma(Lb4, Hb) == (True, 3)   # 5, 8, 11; yayılım 6 >= 3
    Lb5 = np.full(40, 9.0); Lb5[[0, 3, 6]] = 5                          # 3 dokunuş, yayılım 6 < 0,25 x 40
    assert GT.gt_k2_savunma(Lb5, np.full(40, 10.0)) == (False, 3)
    # derin dip bitti: bölge [30, 49], önceki 20 bar [10, 29]; dip 44'te -> 49 - 44 = 5 >= 5
    L = np.full(50, 10.0); L[44] = 5
    assert GT.gt_k2_dip_bitti(L, 30, 49) is True
    L[44] = 10; L[45] = 5; assert GT.gt_k2_dip_bitti(L, 30, 49) is False
    L[45] = 10; L[12] = 1; assert GT.gt_k2_dip_bitti(L, 30, 49) is True   # daha derin dip önceki 20 barda
    # yer + küçük mum: önceki 120 bar H 100 / L 90 / gövde 5; bölge 20 bar H 42 / L 40 / gövde 0,5
    n = 140; H = np.r_[np.full(120, 100.0), np.full(20, 42.0)]; L = np.r_[np.full(120, 90.0), np.full(20, 40.0)]
    O = np.r_[np.full(120, 92.0), np.full(20, 41.0)]; C = np.r_[np.full(120, 97.0), np.full(20, 41.5)]
    g = GT.gt_goz_olcu(O, H, L, C, 120, 139)
    assert abs(g["KUTU_ORAN"] - 2 / 60) < 1e-12 and abs(g["KUTU_YER"] - 1 / 60) < 1e-12 and abs(g["TEPE_KAT"] - 100 / 42) < 1e-12
    assert abs(g["BOY_ORAN"] - 0.2) < 1e-12 and abs(g["GOV_ORAN"] - 0.1) < 1e-12
    o = GT.gt_k2(O, H, L, C, 120, 139); assert o["Y"] == 1 and o["M"] == 1 and o["S"] == 1 and o["dokunus"] == 7   # düz dip: 0, 3, ..., 18 ayrı dokunuş
    assert GT.gt_k2_yer_vek(H, L, np.array([120]), np.array([139]))[0]
    assert GT.gt_goz_olcu(O, H, L, C, 30, 49) is None                   # uzak görünüm < 40 bar
    # dip parabolü: tam parabol dipler (son 10 bar; s = 0, t = 29): r2 = 1, eğrinin dibi x = -0,3
    x = np.linspace(-1, 1, 10); Ld = np.r_[np.full(20, 12.0), 10 + (x + 0.3) ** 2]; Hd = Ld + 0.5
    p = GT.gt_dip_parabol(Hd, Ld, 0, 29); ar = Hd[20:].max() - Ld[20:].min()
    assert p["n"] == 10 and abs(p["r2"] - 1) < 1e-9 and abs(p["tepe_x"] + 0.3) < 1e-9 and abs(p["a"] - 1 / ar) < 1e-9
    assert abs(p["yukselis"] - ((1.3 ** 2) / ar)) < 1e-9 and GT.gt_dip_parabol_var(p)
    p2 = GT.gt_dip_parabol(Hd[::-1].copy(), Ld[::-1].copy(), 0, 29)    # ters (dibi sonda): yok
    assert not GT.gt_dip_parabol_var(p2)


def _dip_uret(rng, tip, g):
    """goz2/dip_sina.py uret() AYNEN (yapay dip tipleri; test içi kopya, goz2 dosyası import edilmez çünkü yüklenirken veri okur)."""
    x = np.arange(60); son = np.linspace(-1, 1, 20)
    if tip in ("U dönüş", "U + sonda daha derin dip"):
        d = np.r_[100 - 0.10 * x[:40], 96 + 2.0 * (son + 0.3) ** 2 - 0.98]
    elif tip == "düz":
        d = np.full(60, 100.0)
    elif tip == "düzenli aşağı kayma":
        d = 100 - 0.12 * x
    elif tip == "yavaşlayan düşüş (dibi sonda)":
        d = 100 - 8 * (1 - np.exp(-x / 25.0))
    elif tip == "kubbe (ters)":
        d = np.r_[np.full(40, 100.0), 100 - 2.0 * (son + 0.3) ** 2 + 0.98]
    else:
        d = 100 + np.cumsum(rng.normal(0, 0.25, 60))
    lo = d + rng.normal(0, g, 60)
    if tip == "U + sonda daha derin dip":
        lo[-2] = lo.min() - 0.8
    h = lo + 0.3 + np.abs(rng.normal(0, 1.2, 60))
    return h, lo


_DIP_TIP = ["U dönüş", "U + sonda daha derin dip", "düz", "düzenli aşağı kayma", "yavaşlayan düşüş (dibi sonda)", "kubbe (ters)", "rastgele yürüyüş"]
_DIP_SINIR = {"U dönüş": (">=", 0.90), "U + sonda daha derin dip": ("<=", 0.02), "düz": ("<=", 0.10), "düzenli aşağı kayma": ("<=", 0.02),
              "yavaşlayan düşüş (dibi sonda)": ("<=", 0.05), "kubbe (ters)": ("<=", 0.01), "rastgele yürüyüş": ("<=", 0.10)}
K2_YAPAY_PAY: dict = {}


@t
def test_k2_dip_parabol_yapay_tipler():
    rng = np.random.default_rng(28)                                    # dip_sina.py ile aynı tohum ve çekim sırası
    ORN = {(tp, g): [_dip_uret(rng, tp, g) for _ in range(400)] for tp in _DIP_TIP for g in (0.10, 0.30)}
    for (tp, g), v in ORN.items():
        pay = float(np.mean([GT.gt_dip_parabol_var(GT.gt_dip_parabol(h, lo, 0, 59)) for h, lo in v])); K2_YAPAY_PAY[f"{tp}|{g}"] = pay
        y, s = _DIP_SINIR[tp]
        assert (pay >= s) if y == ">=" else (pay <= s), (tp, g, pay)


@t
def test_k2_goz2_ile_birebir_sentetik():
    import importlib.util
    import json as _j
    D = os.path.join(GT.GT_YOL["cikti"], "goz2")
    sp = importlib.util.spec_from_file_location("goz2_k2", os.path.join(D, "k2.py")); m = importlib.util.module_from_spec(sp)
    import logging as _lg
    eski = _lg.root.manager.disable
    try:
        sp.loader.exec_module(m)
    finally:
        _lg.disable(eski)
    K2 = _j.loads(_j.dumps(m.K2))
    assert K2 == {k: GT.GT_K2[k] for k in ("Y", "M", "S", "B", "Z")}, "GT_K2 eşikleri goz2 ile aynı değil"
    assert _j.load(open(os.path.join(D, "dip_parabol_kural.json"))) == GT.GT_K2["Z"]
    r = np.random.default_rng(9); n = 0
    seriler = [_k2_seri(tp, 3)[:4] for tp in ("poz", "iri", "tek", "yenidip", "tepe")]
    for k in range(6):
        d = _seri(700, tohum=40 + k); seriler.append(tuple(d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")))
    for O, H, L, C in seriler:
        for _ in range(60):
            Lw = int(r.choice([20, 40, 60, 80])); tt = int(r.integers(min(len(C) - 1, 130), len(C))); ss = tt - Lw + 1
            a = m.k2(O, H, L, C, ss, tt); b = GT.gt_k2(O, H, L, C, ss, tt); n += 1
            assert (a is None and b is None) or a == b, (ss, tt, a, b)
            if b:
                assert int(GT.gt_k2_yer_vek(H, L, np.array([ss]), np.array([tt]))[0]) == b["Y"]
    for O, H, L, C in seriler[:5]:
        assert m.k2(O, H, L, C, 120, 179) == GT.gt_k2(O, H, L, C, 120, 179)
    assert n >= 600


@t
def test_k2_bolge_sonrasi_okunmaz():
    O, H, L, C, s, t_ = _k2_seri("poz")
    O2, H2, L2, C2 = (np.r_[a[:t_ + 1], np.full(40, v)] for a, v in ((O, 1.0), (H, 500.0), (L, 0.5), (C, 300.0)))
    O3, H3, L3, C3 = (np.r_[a[:t_ + 1]] for a in (O, H, L, C))
    assert GT.gt_k2(O2, H2, L2, C2, s, t_) == GT.gt_k2(O3, H3, L3, C3, s, t_) == GT.gt_k2(O, H, L, C, s, t_)
    for Lw in (20, 40, 60):
        assert GT.gt_k2_yer_vek(H2, L2, np.array([t_ - Lw + 1]), np.array([t_]))[0] == GT.gt_k2_yer_vek(H3, L3, np.array([t_ - Lw + 1]), np.array([t_]))[0]


@t
def test_k2_tekil_besli_karar_elle():
    df = pd.DataFrame({"sembol": ["A"] * 6 + ["B"], "t": [100, 100, 120, 140, 200, 239, 100], "L": [40, 20, 80, 40, 20, 20, 40]})
    T = GT.gt_k2_tekil(df)
    assert list(zip(T.sembol, T.t, T.L)) == [("A", 100, 20), ("A", 140, 40), ("A", 200, 20), ("B", 100, 40)]   # 239 - 200 = 39 < 40
    assert list(GT.gt_k2_besli(np.array([0.5, 1.0, 1.5, 4.0, 9.0]), [1.0, 2.0, 3.0, 4.0])) == [1, 1, 2, 4, 5]
    tf = {"alt": 0.001}; iyi = {"n": 30, "TF15": tf, "medyan_fark": 0.01, "besli_arti": 4, "kat5": 1.1}
    assert GT.gt_k2_karar(iyi) == "TUTAR"
    for k, v in (("n", 29), ("medyan_fark", 0.0), ("besli_arti", 3), ("kat5", 1.0)):
        assert GT.gt_k2_karar({**iyi, k: v}) == ("ÖLÇÜLEMEDİ" if k == "n" else "TUTMAZ"), k
    assert GT.gt_k2_karar({**iyi, "TF15": {"alt": -0.001}}) == "TUTMAZ"


@t
def test_k2_sonrasi_kapi_ve_tanim():
    import MUM_IZI_HAVUZ as HV
    d = _seri(400, tohum=77); A = HV.hv25_dizi(d, None); tt = 300
    try:
        GT.gt_k2_olay_olc(A, np.array([tt]), np.array([40]), ["d2022"])
    except GT.GTHata:
        pass
    else:
        raise AssertionError("kapı kapalıyken getiri hesaplanmamalı")
    GT._GT_K2_DURUM["kapi"] = True
    try:
        Y = GT.gt_k2_olay_olc(A, np.array([tt, 390]), np.array([40, 40]), ["d2022", "d2022"])
        Hh, Ll, Oo, Cc = (d[c].to_numpy(float) for c in ("High", "Low", "Open", "Close"))
        E0 = Oo[tt + 1]; st = Ll[tt - 39:tt + 1].min() * 0.98
        assert Y.durum[0] in ("TAMAM", "STOP_ALTI") and Y.durum[1] == "KESIK"
        if Y.durum[0] == "TAMAM":
            assert abs(Y.R15[0] - (Cc[tt + 15] / E0 - 1)) < 1e-12 and abs(Y.R5[0] - (Cc[tt + 5] / E0 - 1)) < 1e-12 and abs(Y.stop[0] - st) < 1e-12
            hit = next((i for i in range(tt + 1, tt + 16) if Hh[i] >= E0 * 1.05), None); sk = next((i for i in range(tt + 1, tt + 16) if Ll[i] <= st), None)
            assert Y.d5[0] == float(hit is not None and (sk is None or hit < sk))
        tb = GT.gt_k2_taban(A, "d2022"); tu = HV.hv25_uygun(A, 20, [], "2020-01-01", "2022-12-31", GT.GT_KESIK)
        R = np.array([Cc[k + 15] / Oo[k + 1] - 1 for k in tu]); assert abs(tb["T1"] - R.mean()) < 1e-12 and tb["t1_n"] == len(tu)
    finally:
        GT._GT_K2_DURUM["kapi"] = False


@t
def test_k2_olc_hesap_ve_tablo_sentetik():
    V = {f"S{i}": _seri(1500, tohum=200 + i) for i in range(12)}; satir = []
    for sem, d in V.items():
        for tt in range(200, 1450, 45):
            g = d.index[tt + 1]; h = "ABD|d1619" if g <= pd.Timestamp("2019-12-31") else ("ABD|d2022" if g >= pd.Timestamp("2020-01-01") else "ABD|dis")
            satir.append({"pazar": "ABD", "sembol": sem, "L": 40, "s": tt - 39, "t": tt, "tarih": d.index[tt], "ATRP20": 0.01 * (1 + (tt // 45) % 5), "kol": "K2",
                          "hucre": h, "giris_tarih": g})
    OL = pd.DataFrame(satir); eski = GT.MI.mi_veri
    GT.MI.mi_veri = lambda p, a: {"V": V}
    GT._GT_K2_DURUM["kapi"] = True
    try:
        G = GT.gt_k2_olc_hesap(OL, {"ABD": {"d1619": [0.015, 0.025, 0.035, 0.045], "d2022": [0.015, 0.025, 0.035, 0.045]}})
    finally:
        GT.MI.mi_veri = eski; GT._GT_K2_DURUM["kapi"] = False
    assert len(G) == len(OL) and set(G.durum) <= {"TAMAM", "KESIK", "STOP_ALTI", "DIS", "T1_YOK"} and (G.durum == "TAMAM").sum() > 100
    T = G[G.durum == "TAMAM"]; assert set(T.besli) == {1, 2, 3, 4, 5}
    o = GT.gt_k2_hucre(T[T.hucre == "ABD|d2022"])
    assert abs(o["TF15"]["ort"] - (T[T.hucre == "ABD|d2022"].R15 - T[T.hucre == "ABD|d2022"].T1).mean()) < 1e-12 and o["TF15"]["alt"] is not None
    TB = GT.gt_k2_tablo(G); assert TB["K2"]["AVR|d1619"]["karar"] == "ÖLÇÜLEMEDİ" and "EMARE" in TB["_karar"]["sonuc"]
    md = GT.gt_k2_tablo_md(TB); assert GT.GT_K2_BASLIK in md and "K7 UYARISI" in md

@t
def test_k2_esik_sabit():
    assert GT.GT_K2["Z"]["r2"] == 0.60 and GT.GT_K2["Z"]["yukselis"] == 0.25 and GT.GT_K2["S"]["dokunus"] == 3 and GT.GT_K2["Y"]["TEPE_KAT"] == 2.0
    assert GT.GT_K2_OLAY["tekil"] == 40 and GT.GT_K2_OLAY["s_min"] == 120 and GT.GT_K2_OLAY["kollar"] == ["K2", "YMSB", "Y"]
    assert GT.GT_K2_OLC["boot"] == {"B": 2000, "tohum": 5} and GT.GT_K2_OLC["karar"] == {"n": 30, "besli_arti": 4, "kat5": 1.0}
    assert GT.GT_K2_OLC["taban_m"] == 20 and GT.GT_K2_OLC["ufuk"] == 15 and GT.GT_K2_OLC["stop_carpan"] == 0.98


# ---------------------------------------------------------------- ÇÖL-K2 KIRILIM (EK 6)
def _k2k_df(C, H=None, L=None, O=None, son="2022-12-30"):
    """Elle seri: C verilir; H / L / O verilmezse C +- 0,1 (geçerli bar)."""
    C = np.asarray(C, float); H = C + 0.1 if H is None else np.asarray(H, float); L = C - 0.1 if L is None else np.asarray(L, float)
    O = C.copy() if O is None else np.asarray(O, float); ix = pd.bdate_range(end=son, periods=len(C))
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1e5}, index=ix)


def _k2k_yon1(d, s, t):
    y = GT.gt_k2k_yon(d.High.to_numpy(float), d.Low.to_numpy(float), d.Close.to_numpy(float), d.index, np.array([s]), np.array([t]))
    return int(y["yon"][0]), int(y["b"][0]), int(y["k"][0])


@t
def test_k2k_yon_elle():
    # bölge 0..9: TAVAN = 10,1 (High), DİP = 8,9 (Low); izleme 10..29
    base = np.r_[np.full(10, 9.5), np.full(30, 9.5)]; base[4] = 10.0; base[6] = 9.0
    up = base.copy(); up[13] = 10.2; up[16] = 8.5                     # yukarı önce (13. indeks = izlemenin 4. barı), sonra aşağı
    assert _k2k_yon1(_k2k_df(up), 0, 9) == (1, 13, 4)
    dn = base.copy(); dn[12] = 8.7; dn[15] = 10.5                     # aşağı önce
    assert _k2k_yon1(_k2k_df(dn), 0, 9) == (-1, 12, 3)
    assert _k2k_yon1(_k2k_df(base), 0, 9) == (0, -1, 0)              # kırılmadı
    d = _k2k_df(base); d.iloc[11, d.columns.get_loc("High")] = 12.0; d.iloc[11, d.columns.get_loc("Low")] = 7.0
    assert _k2k_yon1(d, 0, 9) == (0, -1, 0)                           # aynı bar iki yönü fitille deler, kapanış içeride: kırılım değil
    d.iloc[11, d.columns.get_loc("Close")] = 10.15
    assert _k2k_yon1(d, 0, 9) == (1, 11, 2)                           # aynı bar: Low < DİP ama Close > TAVAN -> yukarı (kapanış kuralı)
    late = base.copy(); late[30] = 10.5                               # kırılım 21. barda: 20 barlık izlemenin dışında
    assert _k2k_yon1(_k2k_df(late), 0, 9) == (0, -1, 0)
    assert _k2k_yon1(_k2k_df(base[:29]), 0, 9) == (-9, -1, 0)         # kesik: 20. bar veride yok (yukarı kırılım olsa da)
    up2 = up[:29]; assert _k2k_yon1(_k2k_df(up2), 0, 9)[0] == -9
    assert _k2k_yon1(_k2k_df(up, son="2023-01-20"), 0, 9)[0] == -9     # kesik: 20. bar (indeks 29) 2023-01-06, 2022-12-31'den sonra
    assert _k2k_yon1(_k2k_df(up, son="2023-01-13"), 0, 9) == (1, 13, 4)  # 20. bar 2022-12-30: kesik değil


@t
def test_k2k_izleme_sinir_ve_gecerli_bar():
    d = _seri(400, tohum=61, son="2023-03-31"); H, L = d.High.to_numpy(float), d.Low.to_numpy(float); tt = np.arange(100, 395)
    IX, kes = GT.gt_k2k_izleme(H, L, d.index, tt)
    assert (IX[~kes] > tt[~kes][:, None]).all() and (IX[~kes, -1] <= tt[~kes] + 20).all() and (IX[kes] == -1).all()
    assert (d.index[IX[~kes, -1]] <= GT.GT_KESIK).all() and kes.sum() > 0
    son_ok = tt[~kes].max(); assert d.index[son_ok + 20] <= GT.GT_KESIK and d.index[son_ok + 21] > GT.GT_KESIK
    Y = GT.gt_k2k_yon(H, L, d.Close.to_numpy(float), d.index, tt - 39, tt)
    k = Y["b"] >= 0; assert (Y["b"][k] <= tt[k] + 20).all() and (Y["b"][k] > tt[k]).all() and (Y["yon"][kes] == -9).all()
    H2 = H.copy(); L2 = L.copy(); H2[205] = L2[205]                    # geçersiz bar (High = Low) izlemeden atlanır
    IX2, _ = GT.gt_k2k_izleme(H2, L2, d.index, np.array([200])); assert 205 not in IX2[0] and IX2[0, -1] == 221


@t
def test_k2k_giris_kirilim_sonrasi_acilis():
    import MUM_IZI_HAVUZ as HV
    d = _seri(300, tohum=62); A = HV.hv25_dizi(d, None); b = np.array([100, 200, 284, 285])
    G = GT.gt_k2k_giris(A, b); O, C = d.Open.to_numpy(float), d.Close.to_numpy(float)
    for i in (0, 1, 2):
        assert not G["kesik"][i] and G["E0"][i] == O[b[i] + 1] and abs(G["R15"][i] - (C[b[i] + 15] / O[b[i] + 1] - 1)) < 1e-12
        assert pd.Timestamp(G["giris_tarih"][i]) == d.index[b[i] + 1]
    assert G["kesik"][3] and np.isnan(G["R15"][3])                    # b + 15 veride yok
    d2 = _seri(300, tohum=62, son="2023-01-06"); G2 = GT.gt_k2k_giris(HV.hv25_dizi(d2, None), np.array([280]))
    assert G2["kesik"][0]                                             # 15. bar 2022-12-31'den sonra


@t
def test_k2k_simetrik_elle_ve_belirsiz():
    E0 = 100.0; H = np.full(30, 101.0); L = np.full(30, 99.0)
    H1 = H.copy(); H1[5] = 105.0; L1 = L.copy(); L1[8] = 94.0         # önce +%5
    H2 = H.copy(); H2[9] = 106.0; L2 = L.copy(); L2[4] = 95.0         # önce -%5 (eşitlik dokunuş sayılır)
    H3 = H.copy(); H3[6] = 105.5; L3 = L.copy(); L3[6] = 94.5         # aynı bar -> belirsiz
    H4 = H.copy(); H4[20] = 120.0                                     # pencere (1..15) dışında: hiçbiri
    r = [int(GT.gt_k2k_simetrik(h, l, np.array([1]), np.array([15]), np.array([E0]), 0.05)[0]) for h, l in ((H1, L1), (H2, L2), (H3, L3), (H4, L))]
    assert r == [1, -1, 2, 0]
    assert int(GT.gt_k2k_simetrik(H1, L1, np.array([1]), np.array([15]), np.array([E0]), 0.10)[0]) == 0
    up, dn, bel = GT._gt_k2k_pay(np.array([1, 1, -1, 0, 2, 2])); assert (up, dn, bel) == (0.5, 0.25, 2)   # belirsiz paydan da çıkar


@t
def test_k2k_tekil_15():
    assert list(GT.gt_k2k_tekil(np.array([40, 10, 20, 24, 25, 40]))) == [10, 25, 40]
    assert list(GT.gt_k2k_tekil(np.array([5, 19, 20, 34, 35]))) == [5, 20, 35] and GT.GT_K2K["tekil"] == 15


def _k2k_panel(V, Ls=(20, 40, 80), adim=5):
    rows = []
    for sem, d in V.items():
        for Lw in Ls:
            for tt in range(130, len(d) - 1, adim):
                rows.append({"sembol": sem, "L": Lw, "s": tt - Lw + 1, "t": tt, "tarih": d.index[tt], "ATRP20": 0.01 + 0.002 * (tt % 50) / 5})
    P = pd.DataFrame(rows); AD = []
    for sem, g in P.groupby("sembol"):
        d = V[sem]; y = GT.gt_k2_yer_vek(d.High.to_numpy(float), d.Low.to_numpy(float), g.s.to_numpy(), g.t.to_numpy())
        AD.append(g[y].assign(pazar="ABD"))
    return P, pd.concat(AD) if AD else P.iloc[:0].assign(pazar="ABD")


@t
def test_k2k_kontrol_y_saglamaz_ve_kapi():
    O, H, L, C, s, t_ = _k2_seri("poz"); n = len(C); ek = 900
    r = np.random.default_rng(9); Ce = C[-1] * np.exp(np.cumsum(r.normal(0, 0.01, ek)))
    d = _k2k_df(np.r_[C, Ce], H=np.r_[H, Ce * 1.01], L=np.r_[L, Ce * 0.99], O=np.r_[O, Ce])
    V = {"X": d, "Y": _seri(len(d), tohum=63)}; P, AD = _k2k_panel(V)
    assert len(AD) > 0 and len(AD) < len(P)
    OL = pd.DataFrame(columns=["pazar", "sembol", "kol", "hucre", "L", "s", "t", "tarih"])
    R = GT.gt_k2k_pazar("ABD", OL, V, P, AD, olc=False); KP = R["kontrol"]
    assert len(KP) == len(P) - len(AD) and "yon" not in KP.columns               # sayımda yön yok
    ad = set(zip(AD.sembol, AD.L, AD.t)); assert not (set(zip(KP.sembol, KP.L, KP.t)) & ad)
    for sem, g in KP.groupby("sembol"):
        dd = V[sem]; assert not GT.gt_k2_yer_vek(dd.High.to_numpy(float), dd.Low.to_numpy(float), (g.t - g.L + 1).to_numpy(), g.t.to_numpy()).any()
    try:
        GT.gt_k2k_pazar("ABD", OL, V, P, AD.iloc[1:], olc=False)
    except GT.GTHata:
        pass
    else:
        raise AssertionError("YER kümesi k2_aday ile aynı değilse durmalı")
    for f in (lambda: GT.gt_k2k_pazar("ABD", OL, V, P, AD, olc=True), lambda: GT.gt_k2k_kir_olay(OL.assign(yon=[]), {}, pd.DataFrame(), {})):
        try:
            f()
        except GT.GTHata:
            pass
        else:
            raise AssertionError("kapı kapalıyken yön / getiri hesaplanmamalı")


@t
def test_k2k_karar_sonrasi_okunmaz():
    base = np.r_[np.full(10, 9.5), np.full(60, 9.5)]; base[4] = 10.0; base[6] = 9.0; up = base.copy(); up[13] = 10.2
    d = _k2k_df(up); ref = _k2k_yon1(d, 0, 9)
    for bozuk_bas in (14, 30):                                          # kırılım barından sonrası ve izleme sonrası bozulur
        d2 = d.copy(); d2.iloc[bozuk_bas:, :4] = d2.iloc[bozuk_bas:, :4].to_numpy() * np.where(np.arange(len(d2) - bozuk_bas) % 2, 0.5, 2.0)[:, None]
        d2["High"] = d2[["Open", "High", "Low", "Close"]].max(axis=1) + 0.01; d2["Low"] = d2[["Open", "High", "Low", "Close"]].min(axis=1) - 0.01
        assert _k2k_yon1(d2, 0, 9) == ref
    import MUM_IZI_HAVUZ as HV
    e = _seri(300, tohum=64); A = HV.hv25_dizi(e, None); G1 = GT.gt_k2k_giris(A, np.array([150]))
    e2 = e.copy(); e2.iloc[166:, :4] = e2.iloc[166:, :4].to_numpy() * 3.0; G2 = GT.gt_k2k_giris(HV.hv25_dizi(e2, None), np.array([150]))
    assert all(np.array_equal(G1[k], G2[k], equal_nan=True) for k in ("E0", "R15", "s5", "s10")) and not G1["kesik"][0]
    O, H, L, C, s, t_ = _k2_seri("poz"); y0 = GT.gt_k2_yer_vek(H, L, np.array([s]), np.array([t_]))[0]
    Hb = np.r_[H[:t_ + 1], np.full(30, 999.0)]; Lb = np.r_[L[:t_ + 1], np.full(30, 0.1)]
    assert GT.gt_k2_yer_vek(Hb, Lb, np.array([s]), np.array([t_]))[0] == y0     # kontrol penceresi YER'i t sonrasını okumaz


@t
def test_k2k_karar_elle():
    a = {"n": 50, "fark": {"alt": 0.001}}; assert GT.gt_k2k_karar_yon(a) == "TUTAR"
    assert GT.gt_k2k_karar_yon({**a, "n": 49}) == "ÖLÇÜLEMEDİ" and GT.gt_k2k_karar_yon({**a, "fark": {"alt": 0.0}}) == "TUTMAZ"
    b = {"n": 30, "TFk15": {"alt": 0.001}, "medyan_fark": 0.01, "s5": {"fark": {"alt": 0.001}}, "besli_buyuk": 4, "besli_arti": 3}
    assert GT.gt_k2k_karar_kir(b) == "TUTAR"
    for k, v in (("n", 29), ("medyan_fark", 0.0), ("TFk15", {"alt": -0.001}), ("s5", {"fark": {"alt": -0.001}}), ("besli_arti", 2)):
        assert GT.gt_k2k_karar_kir({**b, k: v}) == ("ÖLÇÜLEMEDİ" if k == "n" else "TUTMAZ"), k
    assert GT.gt_k2k_karar_kir({**b, "besli_buyuk": 1, "besli_arti": 0}) == "TUTAR"          # büyük beşlik < 2: şart aranmaz
    assert GT.gt_k2k_karar_kir({**b, "besli_buyuk": 2, "besli_arti": 1}) == "TUTMAZ"


@t
def test_k2k_uctan_uca_sentetik():
    V = {f"S{i}": _seri(1600, tohum=300 + i, son="2022-12-30") for i in range(8)}; P, AD = _k2k_panel(V, Ls=(20, 40), adim=5)
    import MUM_IZI_HAVUZ as HV
    rows = []
    for sem, d in V.items():
        for tt in range(300, 1560, 60):
            g = d.index[tt + 1]; rows.append({"pazar": "ABD", "sembol": sem, "L": 40, "s": tt - 39, "t": tt, "tarih": d.index[tt], "ATRP20": 0.01 * (1 + tt % 5),
                                             "kol": "K2", "hucre": HV.hv_hucre_ad(g, "ABD").replace("|dis", "|yok"), "giris_tarih": g})
    OL = pd.DataFrame(rows); OL = OL[OL.hucre.isin(["ABD|d1619", "ABD|d2022"])]
    GT._GT_K2K_DURUM["kapi"] = True; GT._GT_K2_DURUM["kapi"] = True
    try:
        R = GT.gt_k2k_pazar("ABD", OL, V, P, AD, olc=True)
        E = GT.gt_k2k_taban1(R["olay"], R["kontrol"]); T2 = GT.gt_k2k_taban2(R["kontrol_kir"])
        sin = {"ABD": {"d1619": [0.015, 0.025, 0.035, 0.045], "d2022": [0.015, 0.025, 0.035, 0.045]}}
        K = GT.gt_k2k_kir_olay(E, {"ABD": V}, T2, sin)
    finally:
        GT._GT_K2K_DURUM["kapi"] = False; GT._GT_K2_DURUM["kapi"] = False
    assert len(E) == len(OL) and set(E.yon) <= {1, -1, 0, -9} and (E.yon == 1).sum() > 10
    KR = R["kontrol_kir"]; assert (KR.groupby("sembol").b.apply(lambda v: (np.diff(np.sort(v)) >= 15).all())).all()
    x = E[(E.hucre == "ABD|d2022") & (E.yon != -9)]; x = x[np.isfinite(x.k1_yuk)]
    TB = GT.gt_k2k_tablo(E, K); oa = TB["A"]["K2"]["ABD|d2022"]
    assert oa["n"] == len(x) and abs(oa["fark"]["ort"] - ((x.yon == 1).astype(float) - x.k1_yuk).mean()) < 1e-12
    KP = R["kontrol"]; s0, d0 = x.sembol.iloc[0], x.donem.iloc[0]; L0 = int(x.L.iloc[0])
    kk = KP[(KP.sembol == s0) & (KP.donem == d0) & (KP.L == L0) & ~KP.kesik]; assert abs(x.k1_yuk.iloc[0] - (kk.yon == 1).mean()) < 1e-12
    assert abs(x.k1_kos.iloc[0] - (kk.yon == 1).sum() / (kk.yon != 0).sum()) < 1e-12 and oa["kosullu"]["n"] == int((x.yon != 0).sum())
    T = K[K.durum == "TAMAM"]; ob = TB["B"]["K2"]["ABD|d2022"]; Tm = T[T.hucre == "ABD|d2022"]
    assert ob["n"] == len(Tm) and abs(ob["TFk15"]["ort"] - (Tm.R15 - Tm.T1k).mean()) < 1e-12
    r0 = Tm.iloc[0]; kr = KR[(KR.sembol == r0.sembol) & (KR.donem == r0.donem) & ~KR.kesik]; assert abs(r0.T1k - kr.R15.mean()) < 1e-12
    dd = V[r0.sembol]; assert r0.E0 == dd.Open.iloc[int(r0.b) + 1] and dd.Close.iloc[int(r0.b)] > r0.TAVAN
    assert TB["A"]["K2"]["AVR|d1619"]["karar"] == "ÖLÇÜLEMEDİ" and TB["B"]["K2"]["AVR|d1619"]["karar"] == "ÖLÇÜLEMEDİ" and "EMARE" in TB["_karar_B"]["sonuc"]
    md = GT.gt_k2k_tablo_md(TB); assert GT.GT_K2_BASLIK in md and "K7 UYARISI" in md and "TABLO A" in md and "TABLO B" in md


@t
def test_k2k_esik_sabit():
    K = GT.GT_K2K
    assert K["izleme"] == 20 and K["ufuk"] == 15 and K["tekil"] == 15 and K["k2_en_az"] == 5 and K["boot"] == {"B": 2000, "tohum": 6}
    assert K["karar"] == {"yon_n": 50, "kir_n": 30} and K["besli_en_az"] == 20 and K["besli_pay"] == 0.75 and K["hedef"] == [0.05, 0.10]
    assert K["olay_sha"] == "e0ef464c8159b1f403ba03537352e939ea699b3a2a5c6148366485eae99cbf55" and K["ana"] == "K2"


# ---------------------------------------------------------------- ÇÖL-K2 x PİYASA REJİMİ (EK 7)
def _g40_seri(bas="2015-01-05", son="2022-12-26", tohum=3):
    pz = pd.date_range(bas, son, freq="W-MON"); r = np.random.default_rng(tohum)
    return pd.DataFrame({"hno": YO.yo2_hno(pz), "n_kesit": 500, "G40": r.uniform(0.1, 0.8, len(pz)), "pazartesi": pz})


@t
def test_k2r_rejim_yalniz_onceki_hafta():
    G = _g40_seri(); D = pd.DatetimeIndex(["2018-03-07", "2020-03-20", "2022-06-13"])     # çarşamba, cuma, pazartesi
    r0 = GT.gt_k2r_rejim(D, G); h = YO.yo2_hno(D)
    assert (r0["hno_kullanilan"] == h - 1).all() and r0["var"].all()
    for i, x in enumerate(D):                                       # kullanılan değer = D'nin haftasından önceki haftanın G40'ı
        assert r0["g40"][i] == float(G.G40[G.hno == h[i] - 1].iloc[0])
    for i in range(len(D)):                                         # geri bozma: D'nin haftası ve sonrası bozulunca aynı
        G2 = G.copy(); G2.loc[G2.hno >= h[i], "G40"] = 0.0 if r0["g40"][i] > GT.gt_k2r_kesim() else 0.99
        r1 = GT.gt_k2r_rejim(D[i:i + 1], G2); assert r1["g40"][0] == r0["g40"][i] and r1["dip"][0] == r0["dip"][i]
        G3 = G.copy(); G3.loc[G3.hno == h[i] - 1, "G40"] = 0.0 if r0["g40"][i] > GT.gt_k2r_kesim() else 0.99   # ileri: önceki hafta değişince değişir
        r2 = GT.gt_k2r_rejim(D[i:i + 1], G3); assert r2["dip"][0] != r0["dip"][i]
    Gs = G.copy(); Gs["hno"] = Gs.hno - 1                           # seriyi bir hafta ileri kaydır (değer bir hafta erken bilinsin) -> sonuç değişir
    assert not np.array_equal(GT.gt_k2r_rejim(D, Gs)["g40"], r0["g40"])
    Gb = G[G.hno != h[0] - 1]; rb = GT.gt_k2r_rejim(D[:1], Gb)       # önceki hafta yoksa daha eski son hafta (<= 3 hafta)
    assert rb["hno_kullanilan"][0] == h[0] - 2
    Gc = G[(G.hno < h[0] - 4) | (G.hno >= h[0])]; assert not GT.gt_k2r_rejim(D[:1], Gc)["var"][0]


@t
def test_k2r_g40_hesap_elle_ve_pazartesi():
    ix = pd.date_range("2019-01-04", periods=45, freq="W-FRI")
    C1 = np.r_[np.full(40, 10.0), np.full(5, 12.0)]; C2 = np.r_[np.full(40, 10.0), np.full(5, 8.0)]
    W = {}
    for s, C in (("A", C1), ("B", C2)):
        W[s] = pd.DataFrame({"Open": C, "High": C * 1.01, "Low": C * 0.99, "Close": C, "bas": ix - pd.Timedelta(days=4), "bosluk": False}, index=ix)
    ev = {"A": np.ones(45, bool), "B": np.ones(45, bool)}
    eski = YO.YO_ESIK["piyasa"]["kume_en_az"]; YO.YO_ESIK["piyasa"]["kume_en_az"] = 2
    try:
        G = GT.gt_k2r_g40_hesap(W, ev)
    finally:
        YO.YO_ESIK["piyasa"]["kume_en_az"] = eski
    assert len(G) == 6 and (G.n_kesit == 2).all()                 # SMA40 39. bardan itibaren tanımlı (6 hafta)
    assert G.G40.iloc[0] == 0.0 and (G.G40.iloc[1:] == 0.5).all()   # 39. bar: ikisi de 10 = SMA (C > SMA değil); sonra A üstte, B altta
    assert (YO.yo2_hno(G.pazartesi) == G.hno.to_numpy()).all() and (G.pazartesi.dt.dayofweek == 0).all()


@t
def test_k2r_kesim_sabit():
    k0 = GT.gt_k2r_kesim(); G = _g40_seri(); D = pd.bdate_range("2016-01-04", "2022-12-01")
    r0 = GT.gt_k2r_rejim(D, G)
    G2 = G.copy(); G2.loc[G2.pazartesi >= pd.Timestamp("2016-01-01"), "G40"] *= 0.3      # 2016-22 verisi değişir
    r1 = GT.gt_k2r_rejim(D, G2)
    assert GT.gt_k2r_kesim() == k0 == 0.276760218650567 and GT.GT_K2R["kesim"] == k0
    assert np.array_equal(r1["dip"], r1["g40"] <= k0) and r1["dip"].sum() > r0["dip"].sum()   # kesim aynı, yalnız DİP günleri değişir
    yol = GT.GT_K2R["yo2_sayim"]
    if os.path.exists(yol):
        assert GT.gt_k2r_kesim_kaynak_denetim(yol)["kesim"] == k0
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "s.json"); open(p, "w").write('{"kesim": {"ABD": {"G40": 0.3}}}')
        try:
            GT.gt_k2r_kesim_kaynak_denetim(p)
        except GT.GTHata:
            pass
        else:
            raise AssertionError("farklı kesim yakalanmalı")


@t
def test_k2r_obek_elle():
    dip = np.zeros(120, bool); dip[[3, 4, 10]] = True; dip[[31, 32]] = True; dip[[52]] = True; dip[[100]] = True
    # 10 -> 31: arada 20 gün (fark 21) -> yeni; 32 -> 52: arada 19 gün (fark 20) -> aynı öbek; 52 -> 100 yeni
    oid, ob = GT.gt_k2r_obek(dip)
    assert ob == [(3, 10), (31, 52), (100, 100)] and oid[3] == oid[10] == 0 and oid[31] == oid[52] == 1 and oid[100] == 2 and oid[5] == -1
    o0, b0 = GT.gt_k2r_obek(np.zeros(5, bool)); assert b0 == [] and (o0 == -1).all()
    takvim = pd.bdate_range("2018-01-01", periods=120); h0 = YO.yo2_hno(takvim[:1])[0]       # 24 tam hafta (pazartesi başlar)
    G = pd.DataFrame({"hno": np.arange(h0 - 2, h0 + 24)}); G["G40"] = 0.9; G["n_kesit"] = 500
    for w in (1, 2, 5, 12, 16, 23):                                 # bu haftaların günleri DİP (önceki haftanın G40'ı düşük)
        G.loc[G.hno == h0 + w - 1, "G40"] = 0.1
    r = GT.gt_k2r_rejim(takvim, G); assert np.array_equal(np.flatnonzero(r["dip"]), np.concatenate([np.arange(5 * w, 5 * w + 5) for w in (1, 2, 5, 12, 16, 23)]))
    _, ob = GT.gt_k2r_obek(r["dip"]); assert ob == [(5, 29), (60, 84), (115, 119)]       # 29 -> 60 fark 31 yeni; 64 -> 80 fark 16 aynı; 84 -> 115 yeni
    gun = [7, 20, 27, 62, 82, 117, 100]
    E = GT.gt_k2r_olay_rejim(pd.DataFrame({"tarih": takvim[gun], "kol": "K2"}), G, takvim, ob)
    assert list(E.rejim) == ["DİPTE", "DİP DIŞI", "DİPTE", "DİPTE", "DİPTE", "DİPTE", "DİP DIŞI"]
    assert list(E.dip_donem) == [0, -1, 0, 1, 1, 2, -1]               # gün 20 öbek 0'ın tarih aralığında ama DİP değil -> -1


def _k2r_U(rows):
    return pd.DataFrame(rows, columns=["tarih", "besli", "R15", "s5"])


@t
def test_k2r_secim_elle():
    d1, d2 = pd.Timestamp("2020-03-16"), pd.Timestamp("2020-03-17")
    U = _k2r_U([(d1, 5, 0.10, 1), (d1, 5, -0.02, -1), (d1, 5, 0.04, 2), (d1, 4, 0.00, 0), (d1, 4, 0.06, 1), (d1, 3, -0.10, -1),
                (d2, 5, 0.20, 1)])
    G1, G2 = GT.gt_k2r_gun_ozet(U)
    g = G1.set_index("tarih"); assert g.EV_N[d1] == 6 and abs(g.EV_ORT[d1] - 0.08 / 6) < 1e-15
    b = G2.set_index(["tarih", "besli"]); assert b.B_N[(d1, 5)] == 3 and abs(b.B_ORT[(d1, 5)] - 0.04) < 1e-15 and b.B_P5[(d1, 5)] == 0.5
    eski = dict(GT.GT_K2R["evren"]); GT.GT_K2R["evren"]["gun_en_az"] = 3; GT.GT_K2R["evren"]["besli_en_az"] = 2
    try:
        E = pd.DataFrame({"tarih": [d1, d1, d2], "besli": [5, 3, 5], "R15": [0.10, -0.10, 0.20], "durum": "TAMAM"})
        X = GT.gt_k2r_olay_secim(E, G1, G2)
    finally:
        GT.GT_K2R["evren"].clear(); GT.GT_K2R["evren"].update(eski)
    assert abs(X.SECIM[0] - (0.10 - 0.08 / 6)) < 1e-15 and abs(X.SECIM_O[0] - (0.10 - 0.04)) < 1e-15
    assert abs(X.SECIM[1] - (-0.10 - 0.08 / 6)) < 1e-15 and np.isnan(X.SECIM_O[1]) and X.durum[1] == "ES_AZ"     # beşlik 3'te tek hisse (< 2)
    assert np.isnan(X.SECIM[2]) and np.isnan(X.SECIM_O[2]) and X.durum[2] == "ES_AZ"                               # d2 evreni 1 hisse


@t
def test_k2r_boot_kume_az_olculemedi_ve_karar():
    x = np.r_[np.full(40, 0.02), np.full(40, 0.01)]
    b4 = GT.gt_k2r_boot(x, np.repeat(["a", "b", "c", "d"], 20)); assert b4["durum"] == "ÖLÇÜLEMEDİ" and b4["alt"] is None and b4["kume"] == 4
    b5 = GT.gt_k2r_boot(x, np.repeat(["a", "b", "c", "d", "e"], 16)); assert b5["durum"] == "TAMAM" and b5["alt"] is not None and b5["alt"] > 0
    b5b = GT.gt_k2r_boot(x, np.repeat(["a", "b", "c", "d", "e"], 16)); assert b5b["alt"] == b5["alt"]                 # tohum 7: tekrarlanabilir
    o = {"rejim": "DİPTE", "n": 80, "dip_donem": 4, "SECIM_O": b4, "SECIM_O_medyan": 0.015, "s5_fark": 0.1}
    assert GT.gt_k2r_karar(o) == "ÖLÇÜLEMEDİ"
    o.update(dip_donem=5, SECIM_O=b5); assert GT.gt_k2r_karar(o) == "TUTAR"
    o.update(s5_fark=-0.01); assert GT.gt_k2r_karar(o) == "TUTMAZ"
    o.update(s5_fark=0.1, n=29); assert GT.gt_k2r_karar(o) == "ÖLÇÜLEMEDİ"
    o.update(n=80, SECIM_O_medyan=-0.001); assert GT.gt_k2r_karar(o) == "TUTMAZ"
    assert GT.gt_k2r_karar({**o, "rejim": "DİP DIŞI"}) == "BİLGİ"


@t
def test_k2r_kapi_ve_evren_hisse():
    d = _seri(700, tohum=41); sin = {"d1619": [0.01, 0.015, 0.02, 0.03], "d2022": [0.01, 0.015, 0.02, 0.03]}
    try:
        GT.gt_k2r_evren_hisse(d, [], sin)
    except GT.GTHata:
        pass
    else:
        raise AssertionError("kapı kapalıyken getiri hesaplanmamalı")
    d2 = d.copy(); d2.iloc[540:560, d2.columns.get_loc("Open")] = d2.Close.iloc[540:560].to_numpy()   # 540..559 gövdesiz -> 559 gününün 20 barı %100 gövdesiz
    GT._GT_K2R_DURUM["kapi"] = True
    try:
        u = GT.gt_k2r_evren_hisse(d2, [], sin); uz = GT.gt_k2r_evren_hisse(d2, [], sin, zorla=(559,))
    finally:
        GT._GT_K2R_DURUM["kapi"] = False
    k = u["k"]; assert len(k) > 100 and k.min() >= 139 and 559 not in set(k.tolist()) and 559 in set(uz["k"].tolist())
    assert uz["zorla"][uz["k"] == 559].all() and not uz["zorla"][uz["k"] != 559].any()
    i = int(np.flatnonzero(uz["k"] == 559)[0]); O, C = d2.Open.to_numpy(), d2.Close.to_numpy()
    assert abs(uz["R15"][i] - (C[559 + 15] / O[560] - 1)) < 1e-12
    D = pd.DatetimeIndex(u["tarih"]); assert (D >= pd.Timestamp("2016-01-01")).all() and (pd.DatetimeIndex(d2.index[k + 15]) <= GT.GT_KESIK).all()
    a = GT.gt_k2r_atrp20(d2.High.to_numpy(), d2.Low.to_numpy(), C)
    assert np.allclose(a, YO.yo_hisse_ozellik(O, d2.High.to_numpy(), d2.Low.to_numpy(), C, np.ones(len(C)))["ATRP20"], equal_nan=True)
    j = 300; s5 = GT.gt_k2k_simetrik(d2.High.to_numpy(), d2.Low.to_numpy(), np.array([j + 1]), np.array([j + 15]), np.array([O[j + 1]]), 0.05)[0]
    if j in set(k.tolist()):
        assert u["s5"][int(np.flatnonzero(k == j)[0])] == s5


@t
def test_k2r_uctan_uca_olay_hissesi_evrende():
    import MUM_IZI_HAVUZ as HV
    V = {f"S{i}": _seri(1300, tohum=500 + i, son="2022-12-30") for i in range(10)}
    d0 = V["S0"].copy(); tt0 = 900; d0.iloc[tt0 - 19:tt0 + 1, d0.columns.get_loc("Open")] = d0.Close.iloc[tt0 - 19:tt0 + 1].to_numpy()  # S0 t0: 20 bar gövdesiz
    lo = d0.Low.iloc[tt0 - 39:tt0 + 1].min(); d0.iloc[tt0 + 1, d0.columns.get_loc("Open")] = max(d0.Open.iloc[tt0 + 1], lo * 1.2)
    d0.iloc[tt0 + 1, d0.columns.get_loc("High")] = max(d0.High.iloc[tt0 + 1], d0.Open.iloc[tt0 + 1]); V["S0"] = d0
    rows = []
    for sem, d in V.items():
        for tt in ([tt0] if sem == "S0" else []) + list(range(400, 1250, 70)):
            g = d.index[tt + 1]; h = HV.hv_hucre_ad(g, "ABD")
            if h in ("ABD|d1619", "ABD|d2022"):
                at = float(GT.gt_k2r_atrp20(d.High.to_numpy(), d.Low.to_numpy(), d.Close.to_numpy())[tt])
                for kol in ("K2", "Y"):
                    rows.append({"pazar": "ABD", "sembol": sem, "L": 40, "s": tt - 39, "t": tt, "tarih": d.index[tt], "ATRP20": at, "kol": kol, "hucre": h,
                                 "giris_tarih": g, "son15_tarih": d.index[tt + 15]})
    OL = pd.DataFrame(rows)
    takvim = pd.bdate_range("2016-01-01", "2022-12-30"); takvim = takvim[takvim.isin(V["S0"].index)]
    G = _g40_seri(tohum=9); r = GT.gt_k2r_rejim(takvim, G); _, ob = GT.gt_k2r_obek(r["dip"])
    sin = {"d1619": [0.012, 0.016, 0.02, 0.026], "d2022": [0.012, 0.016, 0.02, 0.026]}
    eski = dict(GT.GT_K2R["evren"]); GT.GT_K2R["evren"]["gun_en_az"] = 3; GT.GT_K2R["evren"]["besli_en_az"] = 1
    GT._GT_K2R_DURUM["kapi"] = True; GT._GT_K2_DURUM["kapi"] = True
    try:
        X, U, G1, G2 = GT.gt_k2r_olc_hesap(OL, G, takvim, ob, sin, V, {})
        TB = GT.gt_k2r_tablo(X)
    finally:
        GT._GT_K2R_DURUM["kapi"] = False; GT._GT_K2_DURUM["kapi"] = False; GT.GT_K2R["evren"].clear(); GT.GT_K2R["evren"].update(eski)
    assert len(X) == len(OL) and set(X.rejim) <= {"DİPTE", "DİP DIŞI"} and (X.durum == "TAMAM").sum() > 50
    x0 = X[(X.sembol == "S0") & (X.t == tt0) & (X.kol == "K2")].iloc[0]; assert x0.durum == "TAMAM"
    j0 = U.attrs["sembol"].index("S0"); z = U[(U.j == j0) & (U.k == tt0)]; assert len(z) == 1 and bool(z.zorla.iloc[0])   # olay hissesi zorla evrende
    gun = U[U.tarih == x0.tarih]; assert x0.EV_N == len(gun) and abs(x0.SECIM - (x0.R15 - gun.R15.mean())) < 1e-12
    gb = gun[gun.besli == x0.besli]; assert abs(x0.SECIM_O - (x0.R15 - gb.R15.mean())) < 1e-12 and x0.B_N == len(gb)
    assert abs(x0.R15 - z.R15.iloc[0]) < 1e-12
    T = X[(X.durum == "TAMAM") & (X.kol == "K2") & (X.hucre == "ABD|d2022") & (X.rejim == "DİP DIŞI")]
    o = TB["K2"]["ABD|d2022"]["DİP DIŞI"]; assert o["n"] == len(T) and abs(o["SECIM_O"]["ort"] - T.SECIM_O.mean()) < 1e-12 and o["karar"] == "BİLGİ"
    assert TB["K2"]["ABD|d1619"]["DİPTE"]["karar"] in ("ÖLÇÜLEMEDİ", "TUTAR", "TUTMAZ") and "_karar" in TB
    md = GT.gt_k2r_tablo_md(TB); assert GT.GT_K2_BASLIK in md and "K7 UYARISI" in md and "SEÇİM_O" in md


@t
def test_k2r_esik_sabit():
    K = GT.GT_K2R
    assert K["kesim"] == 0.276760218650567 and K["obek_ara"] == 20 and K["gecikme_en_cok"] == 3 and K["boot"] == {"B": 2000, "tohum": 7, "kume_en_az": 5}
    assert K["karar"] == {"n": 30, "donem": 5} and K["simetrik"] == 0.05 and K["ana"] == "K2" and K["kollar"] == ["K2", "YMSB", "Y"]
    assert K["olay_sha"] == GT.GT_K2K["olay_sha"] and K["evren"]["k_min"] == 139 and K["evren"]["m"] == 20 and K["hucre"] == ["ABD|d1619", "ABD|d2022"]


# ---------------------------------------------------------------- KURAL-3 (EK 8)
@t
def test_k3_dipten_bar_elle():
    L = np.array([5.0, 6, 7, 8, 9, 6, 5, 7, 8, 9])                         # pencere 0..9, n = 10
    assert GT.gt_k3_dipten_bar(L, [0], [9])[0] == 9 / 10                   # dip ilk barda (eşit dipte ilk görülen: 0, 6 değil)
    L2 = np.array([9.0, 8, 7, 6, 2, 6, 7, 8, 9, 9]); assert GT.gt_k3_dipten_bar(L2, [0], [9])[0] == 5 / 10   # dip ortada (4. bar)
    L3 = np.array([9.0, 8, 7, 6, 5, 4, 3, 3.5, 3, 1]); assert GT.gt_k3_dipten_bar(L3, [0], [9])[0] == 0.0    # dip son barda
    L4 = np.array([9.0, 3, 7, 3, 8, 3, 9, 9, 9, 9]); assert GT.gt_k3_dipten_bar(L4, [0], [9])[0] == 8 / 10   # eşit dipler: ilk görülen (1. bar)
    v = GT.gt_k3_dipten_bar(np.r_[L2, L3], [0, 10, 5], [9, 19, 14])
    assert list(v) == [0.5, 0.0, (10 - 1 - int(np.argmin(np.r_[L2, L3][5:15]))) / 10]
    assert list(GT.gt_k3_zaman([0.5, 0.499, np.nan, 1.0])) == [True, False, False, True]
    r = np.random.default_rng(4); Lr = r.normal(10, 1, 300); s = r.integers(0, 200, 40); Lw = r.choice([20, 40, 80], 40); tt = np.minimum(s + Lw - 1, 299)
    ref = [(tt[i] - s[i] - int(np.argmin(Lr[s[i]:tt[i] + 1]))) / (tt[i] - s[i] + 1) for i in range(40)]    # uc_set.py olc tanımı
    assert np.allclose(GT.gt_k3_dipten_bar(Lr, s, tt), ref, rtol=0, atol=0)


@t
def test_k3_kollar_ayrik_ve_ad():
    r = np.random.default_rng(5); d1, y, z = (r.random(500) < 0.5 for _ in range(3)); K = GT.gt_k3_kol(d1, y, z)
    M = np.stack([K[k] for k in GT.GT_K3["kollar"]], 1); assert (M.sum(1) <= 1).all()                       # ayrık
    assert (K["ANA"] == (d1 & y & z)).all() and (K["ZAMANSIZ"] == (d1 & y & ~z)).all() and (K["PUANSIZ"] == (~d1 & y & z)).all()
    assert (M.any(1) == (y & (d1 | z))).all() and not (M.any(1) & ~y).any()                                  # üç kol da YER ister
    assert GT.gt_k3_kol_ad(True, True, True) == "D1+YER+ZAMAN" and GT.gt_k3_kol_ad(True, True, False) == "D1+YER_ZAMANSIZ"
    assert GT.gt_k3_kol_ad(True, False, True) == "D1+ZAMAN_YERSIZ" and GT.gt_k3_kol_ad(False, True, True) == "YER+ZAMAN_PUANSIZ"
    assert GT.gt_k3_kol_ad(False, False, True) == "KURAL_DISI" and GT.gt_k3_kol_ad(True, False, False) == "KURAL_DISI"


def _k3_panel(n=600, tohum=6):
    r = np.random.default_rng(tohum); tar = pd.to_datetime(r.choice(pd.date_range("2014-01-01", "2024-06-30").values, n))
    return pd.DataFrame({"sembol": [f"S{i % 9}" for i in range(n)], "L": r.choice([20, 40, 80], n), "s": r.integers(10, 400, n), "t": r.integers(400, 900, n),
                         "tarih": tar, "KIL": r.choice([0.0, 0.1, 0.3], n), "PUAN_ESIT": np.where(r.random(n) < 0.05, np.nan, r.normal(50, 10, n)).astype(np.float32),
                         "pazar": "ABD"})


@t
def test_k3_d1_sira_evren_ici_ve_2016_22():
    X = _k3_panel(); r = GT.gt_k3_d1_sira(X)
    dag = GT.gt_dagilim(X.assign(**{a: np.nan for a in GT.GT_OLCU_AD}))
    ref = GT.gt_sira_ekle(X.copy(), dag, ["PUAN_ESIT"]).PUAN_ESIT_r.to_numpy(np.float32)
    assert np.array_equal(r, ref, equal_nan=True) and r.dtype == np.float32                           # gt_dagilim + gt_sira_ekle ile AYNEN
    m = GT.gt_evren_maske(X)
    for L in GT.GT_L:                                                                                 # elle: evren içi aynı L dağılımı
        ii = np.flatnonzero(X.L.to_numpy() == L)[:5]; v = X.PUAN_ESIT.to_numpy(float); dg = v[m & (X.L.to_numpy() == L)]
        for i in ii:
            e = ((dg < v[i]).sum() + 0.5 * (dg == v[i]).sum()) / len(dg) if np.isfinite(v[i]) else np.nan
            assert (np.isnan(e) and np.isnan(r[i])) or abs(float(r[i]) - np.float32(e)) == 0
    dis = ~((X.tarih >= "2016-01-01") & (X.tarih <= "2022-12-31")).to_numpy(); assert dis.any() and (m & dis).sum() == 0
    X2 = X.copy(); X2.loc[dis, "PUAN_ESIT"] = np.float32(1e6); X2.loc[X2.KIL.to_numpy() > 0.2, "PUAN_ESIT"] = np.float32(-1e6)
    r2 = GT.gt_k3_d1_sira(X2); assert np.array_equal(r[m], r2[m], equal_nan=True)                     # 2016-22 dışı / evren dışı veri sırayı değiştirmez
    assert not GT.gt_k3_d1([np.nan, 0.8999, np.float32(0.9) - 1e-7])[[0, 1]].any() and GT.gt_k3_d1([0.9, 1.0]).all()
    try:
        GT.gt_k3_d1_sira(pd.concat([X, X.assign(pazar="BIST")]))
    except GT.GTHata:
        pass
    else:
        raise AssertionError("sıra iki pazar karışık hesaplanmamalı")


@t
def test_k3_sartlar_bolge_sonrasi_okunmaz():
    O, H, L, C, s, t_ = _k2_seri("poz"); db = GT.gt_k3_dipten_bar(L, [s], [t_])[0]; y = GT.gt_k2_yer_vek(H, L, np.array([s]), np.array([t_]))[0]
    for ek_h, ek_l in ((999.0, 0.001), (0.5, 0.4)):
        Hb = np.r_[H[:t_ + 1], np.full(40, ek_h)]; Lb = np.r_[L[:t_ + 1], np.full(40, ek_l)]
        assert GT.gt_k3_dipten_bar(Lb, [s], [t_])[0] == db and GT.gt_k2_yer_vek(Hb, Lb, np.array([s]), np.array([t_]))[0] == y
    d = _seri(700, tohum=71); s1 = np.arange(130, 600, 5); t1 = s1 + 39
    a = GT.gt_k3_dipten_bar(d.Low.to_numpy(float), s1, t1); b = GT.gt_k2_yer_vek(d.High.to_numpy(float), d.Low.to_numpy(float), s1, t1)
    for k in (0, 20, len(s1) - 1):                                                                    # her pencere kendi t'sinde kesilmiş seriyle aynı
        dd = d.iloc[:t1[k] + 1]
        assert GT.gt_k3_dipten_bar(dd.Low.to_numpy(float), [s1[k]], [t1[k]])[0] == a[k]
        assert GT.gt_k2_yer_vek(dd.High.to_numpy(float), dd.Low.to_numpy(float), s1[k:k + 1], t1[k:k + 1])[0] == b[k]


@t
def test_k3_tekil_40():
    df = pd.DataFrame({"sembol": ["A"] * 7 + ["B", "B"], "t": [100, 100, 120, 140, 179, 180, 300, 100, 139], "L": [40, 20, 80, 40, 20, 20, 80, 40, 20]})
    T = GT.gt_k2_tekil(df, bar=int(GT.GT_K3["olay"]["tekil"]))
    assert list(zip(T.sembol, T.t, T.L)) == [("A", 100, 20), ("A", 140, 40), ("A", 180, 20), ("A", 300, 80), ("B", 100, 40)]   # 139 - 100 = 39 < 40


@t
def test_k3_karar_elle_ve_kapi():
    b = {"n": 30, "TF15": {"alt": 0.001}, "medyan_fark": 0.01, "s5": {"fark": {"alt": 0.001}}, "besli_buyuk": 4, "besli_arti": 3}
    assert GT.gt_k3_karar(b, "TF15") == "TUTAR"
    for k, v in (("n", 29), ("medyan_fark", 0.0), ("TF15", {"alt": -0.001}), ("s5", {"fark": {"alt": 0.0}}), ("besli_arti", 2)):
        assert GT.gt_k3_karar({**b, k: v}, "TF15") == ("ÖLÇÜLEMEDİ" if k == "n" else "TUTMAZ"), k
    assert GT.gt_k3_karar({**b, "besli_buyuk": 1, "besli_arti": 0}, "TF15") == "TUTAR" and GT.gt_k3_karar({**b, "besli_buyuk": 2, "besli_arti": 1}, "TF15") == "TUTMAZ"
    bb = {**b, "TFk15": b["TF15"]}; bb.pop("TF15"); assert GT.gt_k3_karar(bb, "TFk15") == "TUTAR" and GT.gt_k3_karar(bb, "TF15") == "TUTMAZ"
    import MUM_IZI_HAVUZ as HV
    A = HV.hv25_dizi(_seri(400, tohum=72), None)
    for f in (lambda: GT.gt_k3_taban(A, "d2022"), lambda: GT.gt_k3_olay_A(A, np.array([300]), np.array([40]), ["d2022"]),
              lambda: GT.gt_k3_olc_hesap(pd.DataFrame(), {}, pd.DataFrame())):
        try:
            f()
        except GT.GTHata:
            pass
        else:
            raise AssertionError("kapı kapalıyken getiri hesaplanmamalı")


def _k3_seri(m, tohum=1, son="2022-12-30"):
    """Döngülü seri: 100 bar tepede (~30), 10 barda çöküş, 190 bar dipte (~10, küçük oynaklık); YER şartını sağlayan pencereler üretir."""
    r = np.random.default_rng(tohum); seviye = np.array([30.0 if (i % 300) < 100 else 30 - 2 * ((i % 300) - 99) if (i % 300) < 110 else 10.0 for i in range(m)])
    C = seviye * np.exp(np.cumsum(r.normal(0, 0.01, m)) * 0.3) * (1 + r.normal(0, 0.01, m)); O = C * (1 + r.normal(0, 0.006, m))
    H = np.maximum(O, C) * (1 + np.abs(r.normal(0, 0.008, m))) + 1e-6; L = np.minimum(O, C) * (1 - np.abs(r.normal(0, 0.008, m))) - 1e-6
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1e5 * np.exp(r.normal(0, 0.5, m))}, index=pd.bdate_range(end=son, periods=m))


@t
def test_k3_uctan_uca_sentetik():
    import MUM_IZI_HAVUZ as HV
    V = {f"S{i}": _k3_seri(1600, tohum=400 + i) for i in range(8)}; P, AD = _k2k_panel(V, Ls=(20, 40), adim=5)
    P = P[P.s >= 120].reset_index(drop=True); AD = AD[AD.s >= 120]; assert len(AD) > 50                 # olay evreni s >= 120
    r = np.random.default_rng(8); P = P.assign(KIL=0.0, govdesiz_pay=0.0, PUAN_ESIT=r.normal(50, 10, len(P)).astype(np.float32), pazar="ABD")
    P["D1_sira"] = GT.gt_k3_d1_sira(P); P.loc[r.random(len(P)) < 0.5, "D1_sira"] = np.float32(0.95)       # yapay: D1 payı yüksek
    A, say = GT.gt_k3_aday_pazar("ABD", P, V, AD)
    assert say["yer"] == len(AD) == len(A) and say["ANA_ham"] == int(A.ANA.sum()) and (A[["ANA", "ZAMANSIZ", "PUANSIZ"]].sum(axis=1) <= 1).all()
    try:
        GT.gt_k3_aday_pazar("ABD", P, V, AD.iloc[1:])
    except GT.GTHata:
        pass
    else:
        raise AssertionError("YER kümesi k2_aday ile aynı değilse durmalı")
    a0 = A.iloc[0]; assert a0.DIPTEN_BAR == GT.gt_k3_dipten_bar(V[a0.sembol].Low.to_numpy(float), [a0.s], [a0.t])[0]
    A["giris_tarih"] = [V[s].index[t + 1] for s, t in zip(A.sembol, A.t)]; A["hucre"] = [HV.hv_hucre_ad(g, "ABD") for g in A.giris_tarih]
    OL = pd.concat([GT.gt_k2_tekil(A[A[k] == 1], bar=40).assign(kol=k) for k in GT.GT_K3["kollar"]], ignore_index=True)
    OL = OL[OL.hucre.isin(["ABD|d1619", "ABD|d2022"])]; assert len(OL) > 20
    eski_v, eski_y = GT.MI.mi_veri, GT.gt_yukle; GT.MI.mi_veri = lambda p, a: {"V": V}; GT.gt_yukle = lambda p, ham=None: P
    sin = {p: {"d1619": [0.015, 0.025, 0.035, 0.045], "d2022": [0.015, 0.025, 0.035, 0.045]} for p in ("ABD", "AVR", "BIST")}
    GT._GT_K2K_DURUM["kapi"] = True; GT._GT_K2_DURUM["kapi"] = True; GT._GT_K3_DURUM["kapi"] = True
    try:
        KR = GT.gt_k2k_pazar("ABD", OL.iloc[:0], V, GT.gt_k2_evren(P), AD, olc=True)["kontrol_kir"]
        GA, E, K, kr = GT.gt_k3_olc_hesap(OL, sin, KR)
        KRb = KR.copy(); KRb.loc[KRb.index[0], "R15"] = 9.0
        try:
            GT.gt_k3_kr_denetim(KRb[KRb.sembol == KRb.sembol.iloc[0]], {"ABD": V}, {"ABD": P, "AVR": P.iloc[:0], "BIST": P.iloc[:0]})
        except GT.GTHata:
            pass
        else:
            raise AssertionError("bozuk Kontrol 2 dosyası denetimden geçmemeli")
    finally:
        GT.MI.mi_veri, GT.gt_yukle = eski_v, eski_y; GT._GT_K2K_DURUM["kapi"] = False; GT._GT_K2_DURUM["kapi"] = False; GT._GT_K3_DURUM["kapi"] = False
    assert kr["hisse"] > 0 and len(GA) == len(OL) == len(E) and (GA.durum == "TAMAM").sum() > 10
    x = GA[GA.durum == "TAMAM"].iloc[0]; d = V[x.sembol]; E0 = d.Open.iloc[int(x.t) + 1]
    assert abs(x.R15 - (d.Close.iloc[int(x.t) + 15] / E0 - 1)) < 1e-12
    Z = 10 ** 9; hi = next((i for i in range(int(x.t) + 1, int(x.t) + 16) if d.High.iloc[i] >= E0 * 1.05), Z)
    lo = next((i for i in range(int(x.t) + 1, int(x.t) + 16) if d.Low.iloc[i] <= E0 * 0.95), Z)
    assert x.s5 == (0 if hi == lo == Z else 2 if hi == lo else 1 if hi < lo else -1)
    Ah = HV.hv25_dizi(d, None); dn = x.hucre.split("|")[1]; a_, b_ = HV.HV_ESIK["hucre"]["donem"][dn]; tu = HV.hv25_uygun(Ah, 20, [], a_, b_, GT.GT_KESIK)
    o = HV.hv25_olc_dizi(Ah, tu, 20); v = GT.gt_k2k_simetrik(Ah["DH"], Ah["DL"], o["g0"], o["e15"], o["E0"], 0.05)
    assert abs(x.T1 - o["R15"].mean()) < 1e-12 and abs(x.ts5 - (v[v != 2] == 1).mean()) < 1e-12
    TB = GT.gt_k3_tablo(GA, E, K); oa = TB["A"]["ANA"]["ABD|d2022"]; T = GA[(GA.durum == "TAMAM") & (GA.kol == "ANA") & (GA.hucre == "ABD|d2022")]
    assert oa["n"] == len(T) and (not len(T) or abs(oa["TF15"]["ort"] - (T.R15 - T.T1).mean()) < 1e-12)
    assert TB["A"]["ANA"]["AVR|d1619"]["karar"] == "ÖLÇÜLEMEDİ" and TB["_karar_A"]["sonuc"] in ("EMARE (yaşayan evren)", "ÖLÇÜLEMEDİ", "EMARE DEĞİL")
    eb = E[E.yon == 1]; assert ((eb.b > eb.t) & (eb.b <= eb.t + 30)).all()
    md = GT.gt_k3_tablo_md(TB); assert GT.GT_K3_BASLIK in md and "K7 UYARISI" in md and "TABLO A" in md and "TABLO B" in md


@t
def test_k3_esles_gt5_gercek_veri():
    """GT5'in 21 sayfası (17 kural sayfası kolu aynen; 4 rastgele KURAL-3 kolunda değil) + uc_set_tablo açık sayfalarında Y / DIPTEN_BAR birebir.
    Getirisiz; gerçek veri (açık kopya + pencere paneli) yoksa ATLANIR (yazılır)."""
    if not (os.path.exists(GT._gt_ham("pencere_ABD.pkl")) and os.path.isdir(GT.GT_YOL["acik"])):
        print("ATLANDI test_k3_esles_gt5_gercek_veri: gerçek veri yok"); return
    import logging
    logging.disable(logging.INFO)
    try:
        R = GT.gt_k3_esles()
    finally:
        logging.disable(logging.NOTSET)
    assert R["gt5_kural_sayfa"] == 17 and R["gt5_kural_ayni"] == 17 and R["gt5_rastgele"] == 4 and R["gt5_rastgele_k3_kolda"] == 0
    assert R["uc_set"]["ayni"] == R["uc_set"]["acik"] and not R["uc_set"]["fark"] and R["gecti"]


@t
def test_k3_esik_sabit():
    K = GT.GT_K3
    assert K["D1"]["ust"] == 0.90 == GT.GT_ESIK["D1"]["ust"] and K["Y"] == GT.GT_K2["Y"] and K["ZAMAN"]["dipten_bar"] == 0.5
    assert K["kollar"] == ["ANA", "ZAMANSIZ", "PUANSIZ"] and K["ana"] == "ANA" and K["olay"]["tekil"] == 40 and K["olay"]["s_min"] == 120
    assert {k: K["olay"][k] for k in ("bas", "son", "s_min", "kilitli", "govdesiz", "tekil", "pazar")} == \
        {k: GT.GT_K2_OLAY[k] for k in ("bas", "son", "s_min", "kilitli", "govdesiz", "tekil", "pazar")}                   # olay evreni ÇÖL-K2 ile aynı
    O = K["olc"]; assert O["boot"] == {"B": 2000, "tohum": 8} and O["ufuk"] == 15 and O["taban_m"] == 20 and O["hedef"] == [0.05, 0.10] and O["uc"] == 0.20
    assert (O["besli_en_az"], O["besli_pay"], O["besli_sart_en_az"], O["izleme"], O["kir_tekil"], O["k2_en_az"]) == \
        (GT.GT_K2K["besli_en_az"], GT.GT_K2K["besli_pay"], GT.GT_K2K["besli_sart_en_az"], GT.GT_K2K["izleme"], GT.GT_K2K["tekil"], GT.GT_K2K["k2_en_az"])
    assert K["karar"] == {"n": 30} and K["emare_hucre"] == ["ABD|d1619", "ABD|d2022"] and K["hucre_karar"] == GT.GT_K2K["hucre_karar"]
    assert "%64" in GT.GT_K3_BASLIK and GT.GT_K3_BASLIK.startswith("DEDEKTÖRÜN BULDUĞU BÖLGELER")


if __name__ == "__main__":
    hata = 0
    for f in ISIM:
        try:
            f(); print("GEÇTİ", f.__name__)
        except Exception as ex:  # noqa: BLE001
            hata += 1; print("KALDI", f.__name__, type(ex).__name__, ex)
            import traceback; traceback.print_exc()
    if K2_YAPAY_PAY:
        print("ÇÖL-K2 dip parabolü yapay tip geçme payları:", {k: round(v, 4) for k, v in K2_YAPAY_PAY.items()})
    print(f"{len(ISIM) - hata}/{len(ISIM)} geçti")
    sys.exit(1 if hata else 0)
