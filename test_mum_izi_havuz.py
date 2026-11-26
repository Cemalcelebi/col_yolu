"""test_mum_izi_havuz — MUM_IZI_HAVUZ (EK 24, kodun seçtiği bütün bölgeler) sentetik testleri: kapı sınırı (0,70 dahil / 0,7001 hariç), hariç tutma (tam ve
yakın), 15 bar tekilleştirme, kesik assert, pencere kesiğini aşan olayın ölçülmemesi, eşten olaylı hisselerin dışlanması (ve hv_es_uye = gz_es_grup),
hücre ataması giriş tarihine göre, ay kümeli bootstrap ve permütasyon tohumu sabit, slot portföyü, hüküm / genel hüküm kuralı, çakışma kapısı.
Çalıştır: python test_mum_izi_havuz.py"""
import os
import sys

import numpy as np
import pandas as pd

import MUM_IZI_HAVUZ as HV
import MUM_IZI_GOZ as GZ
import MUM_IZI_GOZ2 as G2


def test_kapi_siniri():
    assert HV.hv_grup(0.70) == "KAPILI" and HV.hv_grup(0.6999) == "KAPILI"
    assert HV.hv_grup(0.7001) == "KAPISIZ" and HV.hv_grup(2.5) == "KAPISIZ"
    assert HV.hv_grup(float("nan")) == "ORAN_YOK" and HV.hv_grup(None) == "ORAN_YOK" and HV.hv_grup("x") == "ORAN_YOK"
    assert HV.HV_ESIK["kapi"]["oran_en_cok"] == 0.70 == HV.HK.HK_ESIK_P4["kapi"]["oran_en_cok"]


def test_tekil_15_bar():
    X = pd.DataFrame({"zaman": ["gunluk"] * 5 + ["haftalik"], "sembol": ["A", "A", "A", "A", "B", "A"], "t": [100, 114, 115, 129, 100, 105]})
    Y, at = HV.hv_tekil(X)
    a = Y[(Y.zaman == "gunluk") & (Y.sembol == "A")].t.tolist()
    assert a == [100, 115] and at == 2        # 114 (< 15 bar) atılır; 115 kalır; 129 (115'ten 14 bar) atılır
    assert len(Y[Y.zaman == "haftalik"]) == 1 and len(Y[Y.sembol == "B"]) == 1


def test_haric_tam_ve_yakin():
    ix = pd.bdate_range("2019-01-01", periods=300)
    X = pd.DataFrame({"zaman": ["gunluk"] * 4, "sembol": ["A", "A", "A", "C"], "tarih": [str(ix[100].date()), str(ix[130].date()), str(ix[200].date()),
                                                                                      str(ix[100].date())], "t": [100, 130, 200, 100]})
    H = [{"zaman": "gunluk", "sembol": "A", "bolge_son": str(ix[100].date())}, {"zaman": "gunluk", "sembol": "A", "bolge_son": str(ix[215].date())},
         {"zaman": "haftalik", "sembol": "C", "bolge_son": str(ix[100].date())}]
    Y = HV.hv_haric_isaretle(X, H, {("gunluk", "A"): ix})
    assert Y.haric.tolist() == ["tam", "", "yakin", ""]         # 200 ile 215: 15 bar (dahil) yakın; C haftalık hariç günlüğe değmez


def test_kesik_assert():
    ok = {"A": pd.DataFrame({"Close": [1.0, 2.0]}, index=pd.to_datetime(["2022-12-29", "2022-12-30"]))}
    assert HV.hv_kesik_kapi(ok) == pd.Timestamp("2022-12-30")
    bozuk = {"A": pd.DataFrame({"Close": [1.0, 2.0]}, index=pd.to_datetime(["2022-12-30", "2023-01-02"]))}
    try:
        HV.hv_kesik_kapi(bozuk)
    except HV.HVHata as ex:
        assert "KESİK" in str(ex)
    else:
        raise AssertionError("kesik aşımı durmadı")


def _seri(n: int, son: str, tohum: int = 1) -> pd.DataFrame:
    ix = pd.bdate_range(end=son, periods=n); r = np.random.default_rng(tohum)
    C = 10 * np.exp(np.cumsum(r.normal(0, 0.01, n))); O = C * (1 + r.normal(0, 0.002, n))
    H = np.maximum(O, C) * 1.01; L = np.minimum(O, C) * 0.99
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1000.0}, index=ix)


def test_pencere_kesigi_olculmez():
    D = _seri(300, "2022-12-30")
    r1 = {"zaman": "gunluk", "tarih": str(D.index[-10].date()), "m": 16}      # 15. mum veri sonunu aşar
    g = G2.k17_gecit_bir(D, None, r1, HV.MI.MI_KESIK); assert not g["olculebilir"] and g["neden"] in ("ufuk_kesik",)
    r2 = {"zaman": "gunluk", "tarih": str(D.index[-40].date()), "m": 16}
    g2 = G2.k17_gecit_bir(D, None, r2, HV.MI.MI_KESIK)
    rec = GZ.gz_olc_bir(D, None, r2, HV.MI.MI_KESIK)
    assert g2["olculebilir"] == rec["olculdu"]
    T = HV.hv_tarihler(D, None, r2)
    if rec["olculdu"]:
        assert pd.Timestamp(T["giris"]) == pd.Timestamp(rec["giris"]) and pd.Timestamp(T["son15"]) == pd.Timestamp(rec["son15"])
    assert pd.Timestamp(T["bolge_bas"]) == pd.Timestamp(rec["bolge_bas"]) and pd.Timestamp(T["bolge_son"]) == pd.Timestamp(rec["bolge_son"])
    # kısa kesik: 15. mum kesiği aşarsa ölçülmez
    rec3 = GZ.gz_olc_bir(D, None, r2, pd.Timestamp(D.index[-30]))
    assert not rec3["olculdu"] and rec3["neden"] == "ufuk_kesik"


def _panel(n_gun: int = 60, n_his: int = 12, tohum: int = 3):
    r = np.random.default_rng(tohum); idx = pd.bdate_range("2019-01-01", periods=n_gun)
    Cl = 10 * np.exp(np.cumsum(r.normal(0, 0.01, (n_gun, n_his)), axis=0)); Op = Cl * (1 + r.normal(0, 0.002, (n_gun, n_his)))
    Hi = np.maximum(Op, Cl) * 1.01; Lo = np.minimum(Op, Cl) * 0.99
    KV = np.zeros((n_gun, n_his), int); KV[:, 10:] = 1                    # iki kova: 0..9 ve 10..11
    kol = {f"S{j}": j for j in range(n_his)}
    return {"P": {"tarih": idx, "kol": kol, "Op": Op, "Hi": Hi, "Lo": Lo}, "KV": KV, "Cl": Cl}, idx


def test_es_dislama_ve_gz_esitligi():
    Pn, idx = _panel()
    X = pd.DataFrame({"sembol": ["S0", "S1"], "giris": [idx[20], idx[20]], "son15": [idx[34], idx[34]], "bolge_bas": [idx[3], idx[3]],
                      "bolge_son": [idx[19], idx[19]], "R15": [0.01, 0.02], "zaman": ["gunluk", "gunluk"]})
    gun = {20: {0, 1, 2}}                                                    # S0, S1, S2 aynı gün olaylı
    E = GZ.gz_es_grup(Pn, X, gun); U = HV.hv_es_uye(Pn, X, gun)
    for i, u in enumerate(U):
        assert u["es_neden_u"] == "" and int(E.n_es.iloc[i]) == len(u["uye_R"]) == 7          # 10 - olaylı 3 = 7 (kova 0)
        assert abs(float(E.es_R15.iloc[i]) - float(np.mean(u["uye_R"]))) < 1e-12
    gun2 = {20: {0, 1, 2, 3, 4, 5}}                                          # 4 üye kalır -> es_az
    E2 = GZ.gz_es_grup(Pn, X, gun2); U2 = HV.hv_es_uye(Pn, X, gun2)
    assert all(u["es_neden_u"] == "es_az" for u in U2) and (E2.es_neden == "es_az").all()
    Pg = HV.hv_gun_olay(Pn, pd.DataFrame({"pazar": ["ABD", "ABD", "AVR"], "sembol": ["S0", "S5", "S6"], "giris": [idx[20], idx[21], idx[20]]}), "ABD")
    assert Pg == {20: {0}, 21: {5}}


def test_hucre_atama_giris_tarihine_gore():
    assert HV.hv_hucre_ad("2015-12-31", "ABD") == "ABD|o16" and HV.hv_hucre_ad("2016-01-04", "ABD") == "ABD|d1619"
    assert HV.hv_hucre_ad("2019-12-31", "AVR") == "AVR|d1619" and HV.hv_hucre_ad("2020-01-02", "AVR") == "AVR|d2022"
    assert HV.hv_hucre_ad("2022-12-30", "BIST") == "BIST|d2022" and HV.hv_hucre_ad("2023-01-02", "ABD") == "ABD|dis"


def test_boot_perm_tohum_sabit():
    r = np.random.default_rng(5); a = r.normal(0.01, 0.05, 80); b = r.normal(0, 0.05, 120)
    aa = np.array([f"2019-{1 + i % 12:02d}" for i in range(80)]); ab = np.array([f"2019-{1 + i % 12:02d}" for i in range(120)])
    p1 = HV.hv_tabaka_perm(a, b, aa, ab, 500, 7); p2 = HV.hv_tabaka_perm(a, b, aa, ab, 500, 7)
    b1 = HV.hv_ay_boot_fark(a, b, aa, ab, 500, 9); b2 = HV.hv_ay_boot_fark(a, b, aa, ab, 500, 9)
    assert p1 == p2 and b1 == b2 and 0 < p1 <= 1 and b1[0] < b1[1]
    # aynı dağılımlı iki grup: p büyük; kayık grup: p küçük
    assert HV.hv_tabaka_perm(a + 0.2, b, aa, ab, 500, 7) < 0.01
    import CETVEL2 as C2
    g = pd.to_datetime([f"2019-{1 + i % 12:02d}-15" for i in range(80)])
    c1 = C2.c2_hucre(a, np.zeros(80), np.full(80, 0.6), g, "+", tohum_ek=3, perm=True)
    c2 = C2.c2_hucre(a, np.zeros(80), np.full(80, 0.6), g, "+", tohum_ek=3, perm=True)
    assert c1["boot_alt"] == c2["boot_alt"] and c1["p"] == c2["p"]


def test_slot_ve_hukum():
    n = 40; g = pd.DataFrame({"giris": pd.bdate_range("2019-01-01", periods=n, freq="5B"), "sembol": [f"S{i}" for i in range(n)], "esli": True,
                              "R15": 0.05, "olculdu": True})
    g["son15"] = g.giris + pd.Timedelta(days=21); g["_uye"] = [np.array([-0.02, 0.0, 0.01, -0.01, 0.0])] * n
    s = HV.hv_slot(g, 11)
    assert s["slot_gecti"] and s["slot_yuzdelik"] == 1.0 and s == HV.hv_slot(g, 11)
    c = {"n": 40, "fark": 0.01, "boot_alt": 0.002, "boot_ust": 0.02, "sira": 0.55, "slot_gecti": True, "guc": 0.5}
    assert HV.hv_hukum(c)["hukum"] == "TUTAR"
    assert HV.hv_hukum(dict(c, slot_gecti=False))["hukum"] == "ÖLÇÜLEMEDİ"
    assert HV.hv_hukum(dict(c, slot_gecti=False, guc=0.9))["hukum"] == "TUTMADI"
    assert HV.hv_hukum(dict(c, n=29, guc=0.99))["hukum"] == "ÖLÇÜLEMEDİ"
    neg = HV.hv_hukum(dict(c, fark=-0.01, boot_alt=-0.02, boot_ust=-0.001, guc=0.9)); assert neg["neg_anlamli"] and neg["hukum"] == "TUTMADI"
    T = {"hukum": "TUTAR", "poz_anlamli": True, "neg_anlamli": False}; M = {"hukum": "TUTMADI", "poz_anlamli": False, "neg_anlamli": False}
    O = {"hukum": "ÖLÇÜLEMEDİ", "poz_anlamli": False, "neg_anlamli": False}; N = {"hukum": "TUTMADI", "poz_anlamli": False, "neg_anlamli": True}
    k = HV.HV_ESIK["hucre"]["karar"]
    assert HV.hv_genel(dict(zip(k, [T] * 4)))["genel"].startswith("AÇIK VERİDE TUTUYOR")
    assert HV.hv_genel(dict(zip(k, [M, O, O, O])))["genel"] == "TUTMADI"
    assert HV.hv_genel(dict(zip(k, [T, M, O, O])))["genel"] == "ÖLÇÜLEMEDİ"
    assert HV.hv_genel(dict(zip(k, [T, N, O, O])))["genel"] == "ÇELİŞKİLİ"
    assert HV.hv_genel(dict(zip(k, [O] * 4)))["olculemedi_hucre"] == k


def test_bh():
    a = HV._hv_bh([0.01, 0.04, None, 0.03], 0.1)
    assert a[2] is None and abs(a[0] - 0.03) < 1e-12 and abs(a[1] - 0.04) < 1e-12 and abs(a[3] - 0.04) < 1e-12


def test_cakisma_kapisi():
    yol = os.path.join(os.path.dirname(os.path.abspath(HV.__file__)), "MUM_IZI_HAVUZ.py")
    g = {"__name__": "x", "__file__": yol, "hv_grup": object()}
    try:
        exec(compile(open(yol, encoding="utf-8").read(), yol, "exec"), g)
    except RuntimeError as ex:
        assert "çakışma kapısı" in str(ex)
    else:
        raise AssertionError("çakışma kapısı durmadı")


def test_sha():
    assert len(HV.hv_esik_sha()) == 64 and HV.hv_esik_sha() == HV.hv_esik_sha(dict(HV.HV_ESIK))
    E = dict(HV.HV_ESIK); E["surum"] = "x"; assert HV.hv_esik_sha(E) != HV.hv_esik_sha()


# ================================================================ EK 25 (rastgele gün tabanı, zamanlama / seçim, piyasa tahmini)
def _uzun(n: int = 1600, son: str = "2022-12-30", tohum: int = 7) -> pd.DataFrame:
    ix = pd.bdate_range(end=son, periods=n); r = np.random.default_rng(tohum)
    C = 10 * np.exp(np.cumsum(r.normal(0, 0.02, n))); O = C * (1 + r.normal(0, 0.01, n))
    H = np.maximum(O, C) * (1 + np.abs(r.normal(0, 0.015, n))); L = np.minimum(O, C) * (1 - np.abs(r.normal(0, 0.015, n)))
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1000.0}, index=ix)


def test_25_yakin_dislama_donem_kesik():
    D = _uzun(); A = HV.hv25_dizi(D, None)
    el0 = HV.hv25_uygun(A, 10, set(), "2016-01-01", "2022-12-31")
    k = int(el0[len(el0) // 2]) + 1                                         # bilinen bölgenin giriş barı
    el = HV.hv25_uygun(A, 10, {k}, "2016-01-01", "2022-12-31")
    assert len(el) and (np.abs(el + 1 - k) >= 15).all()
    assert (k - 1 - 14) not in set(el) and (k - 1 - 15) in set(el) and (k - 1 + 15) in set(el) and (k - 1 + 14) not in set(el)   # |fark| 14 dışlanır, 15 kalır
    el2 = HV.hv25_uygun(A, 10, set(), "2019-01-01", "2019-12-31")          # dönem sınırı (giriş tarihine göre)
    g = A["giris_tarih"][el2 + 1]; assert len(el2) and (g >= pd.Timestamp("2019-01-01")).all() and (g <= pd.Timestamp("2019-12-31")).all()
    assert (A["tarih"][el2 + 15] > pd.Timestamp("2019-12-31")).any()       # 15. mum dönem dışına taşabilir
    ks = D.index[-100]; el3 = HV.hv25_uygun(A, 10, set(), "2016-01-01", "2022-12-31", ks)   # pencere kesiği
    assert (A["tarih"][el3 + 15] <= ks).all() and int(el3.max()) + 15 == int(A["tarih"].get_loc(ks))
    E0 = A["DO"][el0 + 1]; st = np.array([D.Low.to_numpy()[t - 9:t + 1].min() * 0.98 for t in el0]); assert (E0 > st).all()   # stop = önceki m barın dibi x 0,98


def test_25_olc_dizi_gz_esitligi():
    D = _uzun(); A = HV.hv25_dizi(D, None); r = np.random.default_rng(3)
    el = HV.hv25_uygun(A, 12, set(), "2016-01-01", "2022-12-31"); ts = r.choice(el, 60, replace=False); q = HV.hv25_olc_dizi(A, ts, 12)
    for i, t in enumerate(ts):
        g = GZ.gz_olc_bir(D, None, {"zaman": "gunluk", "tarih": str(D.index[t].date()), "m": 12}, HV.MI.MI_KESIK)
        assert g["olculdu"] and abs(g["R15"] - q["R15"][i]) < 1e-12 and abs(g["stop"] - q["stop"][i]) < 1e-12 and g["E0"] == q["E0"][i]
        assert g["d5"] == q["d5"][i] and g["d10"] == q["d10"][i] and g["stop15"] == q["stop15"][i]
        assert abs(q["stop"][i] - D.Low.to_numpy()[t - 11:t + 1].min() * 0.98) < 1e-12
    # uygun olmayanlar gz'de de ölçülmez (giriş <= stop ya da kesik)
    tum = np.arange(11, len(D) - 15); dis = sorted(set(tum) - set(el))[:40]
    for t in dis:
        g = GZ.gz_olc_bir(D, None, {"zaman": "gunluk", "tarih": str(D.index[t].date()), "m": 12}, HV.MI.MI_KESIK)
        assert (not g["olculdu"]) or D.index[t + 1] < pd.Timestamp("2016-01-01")
    # haftalık
    D2 = _uzun(2600, tohum=11); W = HV.MV.mv_haftalik_panel({"S": D2})["S"]; A2 = HV.hv25_dizi(D2, W)
    el = HV.hv25_uygun(A2, 8, set(), "2010-01-01", "2022-12-31"); ts = r.choice(el, 40, replace=False); q = HV.hv25_olc_dizi(A2, ts, 8)
    for i, t in enumerate(ts):
        g = GZ.gz_olc_bir(D2, W, {"zaman": "haftalik", "tarih": str(W.index[t].date()), "m": 8}, HV.MI.MI_KESIK)
        assert g["olculdu"] and abs(g["R15"] - q["R15"][i]) < 1e-12 and abs(g["stop"] - q["stop"][i]) < 1e-12 and g["d10"] == q["d10"][i]
        gi = D2.index.get_loc(pd.Timestamp(g["giris"])); ei = D2.index.get_loc(pd.Timestamp(g["son15"]))
        assert G2.k17_dokunma(D2.High.to_numpy()[gi:ei + 1], D2.Low.to_numpy()[gi:ei + 1], g["E0"], g["stop"], 0.05) == q["d5"][i]
        assert pd.Timestamp(g["giris"]) == A2["giris_tarih"][t + 1]


def test_25_tohum_tekrar():
    a = HV._hv25_rng(1, "gunluk|ABD|X|2019-01-02|EK24").choice(1000, 200, replace=False)
    b = HV._hv25_rng(1, "gunluk|ABD|X|2019-01-02|EK24").choice(1000, 200, replace=False)
    c = HV._hv25_rng(1, "gunluk|ABD|Y|2019-01-02|EK24").choice(1000, 200, replace=False)
    assert (a == b).all() and not (a == c).all() and len(set(a)) == 200 and HV.HV25_ESIK["tohum"] == 2511


def test_25_piyasa_olayli_dislama():
    V = {f"S{j}": _uzun(300, tohum=20 + j) for j in range(8)}
    V["S0"] = V["S0"].copy(); V["S0"].iloc[110:, :4] = V["S0"].iloc[110:, :4] * 3     # S0: giriş sonrası x3
    M = HV.hv25_piyasa_matris(V); d, e = 105, 119
    v_hep, n_hep = HV.hv25_piyasa_R(M, d, e, []); v_dis, n_dis = HV.hv25_piyasa_R(M, d, e, [M["kol"]["S0"]])
    assert n_hep == 8 and n_dis == 7 and v_hep > v_dis + 0.2
    R = [V[s].Close.iloc[e] / V[s].Open.iloc[d] - 1 for s in sorted(V) if s != "S0"]; assert abs(v_dis - np.mean(R)) < 1e-12
    X = pd.DataFrame({"pazar": ["ABD", "ABD", "AVR"], "sembol": ["S0", "S3", "S1"], "giris": [str(M["cal"][d].date()), np.nan, str(M["cal"][d].date())],
                      "tarih": [str(M["cal"][d - 1].date()), str(M["cal"][d - 1].date()), str(M["cal"][d - 1].date())]})
    gh = HV.hv25_gun_haric(X, "ABD", M); assert gh == {d: {M["kol"]["S0"], M["kol"]["S3"]}}   # girişsiz olay: bölge sonundan sonraki gün


def test_25_takvim_sayi_gelecege_bakmaz():
    cal = pd.bdate_range("2019-01-01", periods=40)
    bs = [cal[10], cal[10], cal[12], cal[20]]
    S = HV.hv25_sayi(cal, [str(x.date()) for x in bs])
    assert S[9] == 0 and S[10] == 2 and S[12] == 3 and S[14] == 3 and S[15] == 1 and S[16] == 1 and S[17] == 0 and S[19] == 0 and S[20] == 1 and S[24] == 1 and S[25] == 0
    assert list(HV.hv25_durum(np.array([0, 1, 2, 3, 7]))) == ["SAYI = 0", "SAYI = 1-2", "SAYI = 1-2", "SAYI >= 3", "SAYI >= 3"]
    try:
        HV.hv25_sayi(cal, ["2019-01-05"])                                       # cumartesi: takvimde yok -> DUR
    except HV.HVHata:
        pass
    else:
        raise AssertionError("takvim dışı bölge sonu durmadı")
    cal2 = pd.bdate_range("2015-11-01", "2022-12-30"); g = HV.hv25_takvim_gunler(cal2)
    assert (cal2[g + 1] >= pd.Timestamp("2016-01-01")).all() and (cal2[g + 15] <= pd.Timestamp("2022-12-31")).all() and int(g.max()) + 15 == len(cal2) - 1


def test_25_dus20():
    ix = pd.bdate_range("2019-01-01", periods=60); C = np.ones((60, 3)); C[30:, :] = 0.9
    D = HV.hv25_dus20({"Cl": C, "Op": C, "cal": ix}); assert np.isnan(D[:20]).all() and abs(D[49] + 0.1) < 1e-12 and abs(D[50]) < 1e-12


def test_25_boot():
    r = np.random.default_rng(1); x = r.normal(0.01, 0.05, 300); ay = np.array([f"2019-{1 + i % 12:02d}" for i in range(300)])
    a = HV.hv25_boot(x, ay, "t"); b = HV.hv25_boot(x, ay, "t")
    assert a == b and a["alt"] < a["ort"] < a["ust"] and abs(a["ort"] - x.mean()) < 1e-12
    t2 = {"c": {"ort": 0.004, "rep": np.full(10000, 0.004)}}
    c = HV.hv25_boot(x, ay, "t", np.array(["c"] * 300), t2)
    assert abs(c["ort"] - (x.mean() - 0.004)) < 1e-12 and abs(c["alt"] - (a["alt"] - 0.004)) < 1e-12
    t2b = {"c": {"ort": 0.004, "rep": np.random.default_rng(2).normal(0.004, 0.01, 10000)}}
    d = HV.hv25_boot(x, ay, "t", np.array(["c"] * 300), t2b); assert d["ust"] - d["alt"] > c["ust"] - c["alt"]   # T2 belirsizliği aralığı genişletir
    f = HV.hv25_boot_fark(x + 0.05, ay, x, ay, "f"); assert f["alt"] > 0 and f == HV.hv25_boot_fark(x + 0.05, ay, x, ay, "f")
    rep = HV.hv25_t2_rep(x, ay, "k"); assert len(rep) == 10000 and abs(rep.mean() - x.mean()) < 0.002


def test_25_okuma():
    assert HV.hv25_okuma(30, 12, 0.01, 0.001, 0.02) == "MUTLAK KÂRLI" and HV.hv25_okuma(29, 12, 0.01, 0.001, 0.02) == "ÖLÇÜLEMEDİ"
    assert HV.hv25_okuma(30, 11, 0.01, 0.001, 0.02) == "ÖLÇÜLEMEDİ" and HV.hv25_okuma(40, 20, 0.01, -0.001, 0.02) == "AYRIŞMIYOR"
    assert HV.hv25_okuma(40, 20, -0.01, -0.02, -0.001) == "RASTGELE GÜNDEN KÖTÜ" and HV.hv25_okuma(5, 3, 0.01, 0.001, 0.02, sart=False) == "MUTLAK KÂRLI"
    assert HV.hv25_okuma(40, 20, 0.01, 0.001, 0.02, "ZAMANLAMA") == "ZAMANLAMA VAR"
    P = {"fark": 0.01, "alt": 0.001, "ust": 0.02}; N = {"fark": 0.01, "alt": -0.001, "ust": 0.02}; T = {"fark": -0.01, "alt": -0.02, "ust": -0.001}
    assert HV.hv25_takvim_okuma({"d1619": P, "d2022": P}) == "PİYASA YÜKSELİŞİNİ ÖNCELİYOR"
    assert HV.hv25_takvim_okuma({"d1619": P, "d2022": N}) == "TEK DÖNEM" and HV.hv25_takvim_okuma({"d1619": N, "d2022": N}) == "GÖSTERİLEMEDİ"
    assert HV.hv25_takvim_okuma({"d1619": T, "d2022": T}) == "GÖSTERİLEMEDİ (ters yönde)" and HV.hv25_takvim_okuma({"d1619": {"fark": None}, "d2022": P}) == "TEK DÖNEM"


def test_25_ek24_degismedi():
    import ast
    import json as _j
    import subprocess
    kok = os.path.dirname(os.path.abspath(HV.__file__)); C = HV.HV_YOL["cikti"]
    J = _j.load(open(os.path.join(C, "mum_izi24_sonuc.json"), encoding="utf-8"))
    assert HV.MI._mi_sha(os.path.join(C, "mum_izi24_olay.csv.gz")) == J["olay_sha"]                 # EK 24 olay satırları değişmedi
    assert f"ESIK24_SHA: {HV.hv_esik_sha()}" in open(os.path.join(C, "MUM_IZI24_ON_KAYIT.md"), encoding="utf-8").read()   # EK 24 eşikleri
    eski = subprocess.run(["git", "show", "ae2a235:MUM_IZI_HAVUZ.py"], cwd=kok, capture_output=True, text=True).stdout
    if not eski:
        return                                                                 # git geçmişi yoksa (Colab) atlanır
    yeni = open(os.path.join(kok, "MUM_IZI_HAVUZ.py"), encoding="utf-8").read()
    def kaynak(src):
        return {n.name: ast.get_source_segment(src, n) for n in ast.parse(src).body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name != "_hv_ana"}
    ke, ky = kaynak(eski), kaynak(yeni)
    farkli = [k for k in ke if ke[k] != ky.get(k)]
    assert not farkli, f"EK 24 fonksiyonları değişti: {farkli}"
    assert HV.HV_ESIK is not None and HV.HV25_ESIK["T1"]["cekim"] == 200 and HV.HV25_ESIK["T2"]["m"] == 20


def _sentetik_girdi():
    V = {f"S{j}": _uzun(1900, tohum=40 + j) for j in range(12)}; W = HV.MV.mv_haftalik_panel(V); r = np.random.default_rng(9); sat = []
    for zi, z in enumerate(("gunluk", "haftalik")):
        for j, s in enumerate(sorted(V)):
            B = W[s] if z == "haftalik" else V[s]
            for k, t in enumerate(sorted(r.choice(np.arange(150, len(B) - 20), 3, replace=False))):
                m = int(r.integers(8, 20)); tr = str(B.index[t].date())
                g = GZ.gz_olc_bir(V[s], W[s] if z == "haftalik" else None, {"zaman": z, "tarih": tr, "m": m}, HV.MI.MI_KESIK)
                d5 = g.get("d5", np.nan)
                if z == "haftalik" and g["olculdu"]:
                    gi = V[s].index.get_loc(g["giris"]); ei = V[s].index.get_loc(g["son15"])
                    d5 = G2.k17_dokunma(V[s].High.to_numpy()[gi:ei + 1], V[s].Low.to_numpy()[gi:ei + 1], g["E0"], g["stop"], 0.05)
                gir = str(pd.Timestamp(g["giris"]).date()) if g.get("giris") is not None else np.nan
                rec = {"zaman": z, "pazar": "ABD", "sembol": s, "m": m, "t": t, "tarih": tr, "bolge_bas": str(g["bolge_bas"].date()), "bolge_son": str(g["bolge_son"].date()),
                       "hucre": HV.hv_hucre_ad(gir, "ABD") if isinstance(gir, str) else "ABD|yok", "olculdu": bool(g["olculdu"]), "giris": gir,
                       "E0": g.get("E0", np.nan), "stop": g["stop"], "son15": str(pd.Timestamp(g["son15"]).date()) if g.get("son15") is not None else np.nan,
                       "R15": g.get("R15", np.nan), "d5": d5, "d10": g.get("d10", np.nan), "fark": float(r.normal(0, 0.03)), "esli": True}
                if k < 2:
                    sat.append(dict(rec, kaynak="EK24", grup=("KAPILI" if (j + k) % 2 else "KAPISIZ"), ana=True, haric="", set="", sinif=""))
                else:
                    sat.append(dict(rec, kaynak="GOZ23", grup="GOZ", ana=False, haric="", set="set7", sinif=["BENZİYOR", "KISMEN", "BENZEMİYOR"][j % 3], t=-1))
    return V, W, pd.DataFrame(sat)


def test_25_uctan_uca_sentetik():
    V, W, X = _sentetik_girdi(); eski = (HV.hv_blok, HV.hv25_girdi)
    try:
        HV.hv_blok = lambda z, p: (V, (W if z == "haftalik" else None), None)
        HV.hv25_girdi = lambda: X.copy()
        X1, EK, S0 = HV.hv25_isle(True); S = HV.hv25_sayim(X1, S0); X2, S2 = HV.hv25_sayim_kos()
        assert HV.hv_json_sha(S) == HV.hv_json_sha(S2)                       # getirisiz sayım hesapla aynı
        m = X1.olculdu
        assert np.allclose(X1.R15[m].astype(float), X1.R15_y[m].astype(float), atol=1e-12) and (X1.d5[m].astype(float) == X1.d5_y[m]).all()
        assert (X1.d10[m].astype(float) == X1.d10_y[m]).all() and np.isfinite(X1.T1_R15[m]).all() and np.isfinite(X1.PIY_R15[m]).all()
        assert set(EK["T2"]) >= {"gunluk|ABD|d1619", "gunluk|ABD|d2022"}
        T = HV.hv25_tablolar(X1, EK); md = HV.hv25_rapor_tablo({"tablo": T})
        assert "KAPILI" in T["ornek"] and "GOZ_7_9" in T["goz"] and "ABD" in T["takvim"] and "PİYASA TAHMİNİ ABD" in md
        X3, EK3, _ = HV.hv25_isle(True)
        assert np.allclose(X3.T1_R15.fillna(9).to_numpy(float), X1.T1_R15.fillna(9).to_numpy(float), atol=0, rtol=0)   # tohum 2511: tekrarlanabilir
    finally:
        HV.hv_blok, HV.hv25_girdi = eski


if __name__ == "__main__":
    t = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in t:
        f(); print("GEÇTİ", f.__name__)
    print(f"{len(t)} test geçti")
    sys.exit(0)
