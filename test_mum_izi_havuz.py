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


if __name__ == "__main__":
    t = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in t:
        f(); print("GEÇTİ", f.__name__)
    print(f"{len(t)} test geçti")
    sys.exit(0)
