"""test_es_yeniden — ES_YENIDEN sentetik / getirisiz testleri (gerçek veride fark ya da taban hesaplanmaz; ağ yok).

Kapsam: TOPLAM = ZAMANLAMA + SEÇİM özdeşliği (elle örnek); T1 ve T2'nin olay günlerini de içeren BÜTÜN günlerden hesaplandığı (elle döngüyle);
R_H geçerli bar kuralı (High > Low, Volume > 0; giriş barı dahil H'inci geçerli bar); giriş kuralı ve ufkun kayıttan okunduğu (ES_KAYIT ile kaynak
modül sabitleri ve dosya sütunları); ay kümesi ve ayrı ay sayısı; bootstrap tohumu (aynı girdi aynı sonuç); karar kuralı; kapalı konu ve 26 Kasım
sonrası kayıtların seçilmediği; hücre ataması; çakışma kapısı.
Çalıştır: python test_es_yeniden.py"""
import os
import sys

import numpy as np
import pandas as pd

import ES_YENIDEN as ES

ISIM = []


def t(f):
    ISIM.append(f)
    return f


def _V(n_hisse=4, n=120, tohum=3, bas="2020-01-01"):
    r = np.random.default_rng(tohum); tarih = pd.bdate_range(bas, periods=n); V = {}
    for j in range(n_hisse):
        c = 20 * np.exp(np.cumsum(r.normal(0, 0.02, n))); o = c * np.exp(r.normal(0, 0.004, n))
        h = np.maximum(o, c) * 1.01; lo = np.minimum(o, c) * 0.99; v = np.full(n, 1000.0)
        V[f"S{j}"] = pd.DataFrame({"Open": o, "High": h, "Low": lo, "Close": c, "Volume": v}, index=tarih)
    return V


@t
def test_ozdeslik_elle():
    # elle örnek: R 0,10, T1 0,04, PİYASA 0,03, T2 0,01 -> TOPLAM 0,06, ZAMANLAMA 0,02, SEÇİM 0,04
    A = ES.es_ayristir([0.10], [0.04], [0.03], [0.01])
    assert abs(A["TOPLAM"][0] - 0.06) < 1e-12 and abs(A["ZAMANLAMA"][0] - 0.02) < 1e-12 and abs(A["SECIM"][0] - 0.04) < 1e-12
    r = np.random.default_rng(1); x = r.normal(size=(4, 50))
    A = ES.es_ayristir(*x)
    assert np.allclose(A["TOPLAM"], A["ZAMANLAMA"] + A["SECIM"])
    assert np.allclose(A["SECIM"], (x[0] - x[2]) - (x[1] - x[3]))


@t
def test_R_gecerli_kurali():
    V = _V(1, 30); d = V["S0"].copy()
    d.iloc[5, d.columns.get_loc("Volume")] = 0          # geçersiz bar (hacim 0)
    d.iloc[8, d.columns.get_loc("High")] = d.iloc[8].Low  # geçersiz bar (H = L)
    tt, R = ES.es_R_gecerli(d, 3)
    g = d[(d.High > d.Low) & (d.Volume > 0)]
    assert len(tt) == len(g) - 2
    for i in range(len(tt)):
        assert pd.Timestamp(tt[i]) == g.index[i] and abs(R[i] - (g.Close.iloc[i + 2] / g.Open.iloc[i] - 1)) < 1e-12
    assert pd.Timestamp("2020-01-08") not in set(pd.DatetimeIndex(tt))   # 5. bar (hacim 0) giriş değil


@t
def test_T1_T2_butun_gunler_olay_dahil():
    V = _V(4, 80); H = 5
    T = ES.es_taban_uzun(V, "gecerli", H, "2099-01-01"); P = ES.es_piyasa(T, en_az=1)
    bas, son = "2020-01-15", "2020-03-31"
    T1, T2, ng = ES.es_T1_T2(T, P, bas, son)
    # elle: her hisse, dönemdeki BÜTÜN giriş günleri (olay günü ayrımı yok)
    for j, s in enumerate(T["S"]):
        tt, R = ES.es_R_gecerli(V[s], H); m = (pd.DatetimeIndex(tt) >= bas) & (pd.DatetimeIndex(tt) <= son)
        assert abs(T1[j] - R[m].mean()) < 1e-12
    # T2 = günlük piyasa ortalamasının dönem ortalaması
    gun = {}
    for s in T["S"]:
        tt, R = ES.es_R_gecerli(V[s], H)
        for a, b in zip(pd.DatetimeIndex(tt), R):
            gun.setdefault(a, []).append(b)
    pg = [np.mean(v) for a, v in gun.items() if pd.Timestamp(bas) <= a <= pd.Timestamp(son)]
    assert abs(T2 - np.mean(pg)) < 1e-12 and ng == len(pg)
    # bir olay günü eklemek / çıkarmak T1'i değiştirmez (olay kümesi tabana girdi değil; bütün günler zaten içinde)
    olay_gun = pd.DatetimeIndex(ES.es_R_gecerli(V["S0"], H)[0])[20]
    rf = ES.es_olay_R_fiyat(T, np.array(["S0"]), np.array([olay_gun.to_datetime64()]))
    tt, R = ES.es_R_gecerli(V["S0"], H)
    assert abs(rf[0] - R[20]) < 1e-12


@t
def test_piyasa_en_az_hisse():
    V = _V(3, 40); T = ES.es_taban_uzun(V, "gecerli", 5, "2099-01-01")
    assert np.isnan(ES.es_piyasa(T)).all()          # 3 hisse < 30
    assert np.isfinite(ES.es_piyasa(T, en_az=3)[:30]).all()


@t
def test_kesik():
    V = _V(2, 60)
    X = {s: d[d.index <= pd.Timestamp("2020-02-14")] for s, d in V.items()}
    T = ES.es_taban_uzun(X, "gecerli", 5, "2020-02-14")
    assert T["cal"].max() <= pd.Timestamp("2020-02-14")


@t
def test_giris_ufuk_kayittan():
    import CETVEL2 as C2
    import FON_IZI as F
    import KART_TUR1 as K1
    import KART_TUR2 as K2
    import OLCU_SINAMA as OS
    import UC_IZ2 as U2
    assert ES.ES_KAYIT["Ç209"]["hucre"]["acik_d1"] == K2.K2_ESIK["hucre"]["acik_d1"]
    assert ES.ES_KAYIT["Ç209"]["hucre"]["acik_d3"] == K2.K2_ESIK["hucre"]["acik_d3"]
    assert ES.ES_KAYIT["Ç205"]["hucre"]["acik"] == K1.KT_ESIK["hucre"]["acik"]
    assert ES.ES_KAYIT["Ç205"]["hucre"]["birikimli"][0] == K1.KT_ESIK["hucre"]["blok_bas"]
    assert ES.ES_KAYIT["Ç206"]["hucre"]["d1"] == OS.OS_ESIK["donem"]["d1"] and ES.ES_KAYIT["Ç206"]["hucre"]["d2"] == OS.OS_ESIK["donem"]["d2"]
    assert ES.ES_KAYIT["Ç226"]["hucre"] == U2.UC2_ESIK["donem"] and pd.Timestamp(ES.ES_KAYIT["Ç226"]["kesik"]) == U2.UC2_KESIK
    assert ES.ES_KAYIT["Ç204"]["hucre"]["egitim"] == C2.C2_ESIK["donem"]["egitim"]
    assert ES.ES_KAYIT["Ç204"]["hucre"]["sinama"] == C2.C2_ESIK["donem"]["sinama"]
    for k in ("Ç189", "Ç99"):
        assert ES.ES_KAYIT[k]["kural"] == "fi_olcut" and ES.ES_KAYIT[k]["H"] == F.FI_OLCUT["ufuk"] and ES.ES_KAYIT[k]["kesik"] == F.FI_OLCUT["kriz"]
    # dosyaların kendi ufuk sütunu (getirisiz, ilk satırlar)
    d = pd.read_csv(ES._es_tam(ES.ES_KAYIT["Ç209"]["dosya"][0]), nrows=5000, usecols=["ufuk"]); assert ES.ES_KAYIT["Ç209"]["H"] in set(d.ufuk)
    d = pd.read_csv(ES._es_tam(ES.ES_KAYIT["Ç205"]["dosya"][0]), nrows=5000, usecols=["ufuk"]); assert ES.ES_KAYIT["Ç205"]["H"] in set(d.ufuk)
    d = pd.read_csv(ES._es_tam(ES.ES_KAYIT["Ç206"]["dosya"][0]), nrows=50, usecols=["H"]); assert set(d.H) == {ES.ES_KAYIT["Ç206"]["H"]}
    for k in ES.ES_KAYIT:
        assert ES.ES_KAYIT[k]["kural"] in ("gecerli", "fi_olcut") and k in ES.ES_OKU


@t
def test_fi_olcut_kural_FON_IZI():
    import FON_IZI as F
    V = _V(35, 150)
    T = ES.es_taban_uzun(V, "fi_olcut", 60, "2099-01-01")
    P = F.fi_olcut_panel(V, dict(F.FI_OLCUT, kriz="2099-01-01"))
    j = P["kol"]["S1"]; d = 10
    r = [x for jj, dd, x in zip(T["J"], T["D"], T["R"]) if jj == j and dd == d]
    assert len(r) == 1 and abs(r[0] - P["R"][d, j]) < 1e-12
    assert abs(P["R"][d, j] - (V["S1"].Close.iloc[d + 59] / V["S1"].Open.iloc[d] - 1)) < 1e-12


@t
def test_ay_kumesi():
    g = pd.to_datetime(pd.Series(["2020-01-02", "2020-01-30", "2020-02-03", "2021-01-05"]))
    a = ES.es_ay(g); assert list(a) == ["2020-01", "2020-01", "2020-02", "2021-01"]
    assert ES.es_ay_sayisi(g) == 3
    x = np.array([1.0, 2.0, 3.0, 4.0]); b1 = ES.es_boot(x, a); b2 = ES.es_boot(x, a)
    assert b1 == b2 and abs(b1["ort"] - 2.5) < 1e-12 and b1["alt"] <= b1["ort"] <= b1["ust"]
    # aynı aydaki iki olay birlikte örneklenir: bütün değerleri aynı ayda olan küme -> tek küme, aralık sıfır genişlikte
    b = ES.es_boot(np.array([1.0, 3.0]), np.array(["2020-01", "2020-01"])); assert abs(b["alt"] - 2.0) < 1e-12 and abs(b["ust"] - 2.0) < 1e-12


@t
def test_hucre_ata():
    h = ES.es_hucre_ata(["2016-03-01", "2020-01-01", "2023-05-05", "2015-01-01"], ES.ES_KAYIT["Ç204"]["hucre"])
    assert list(h) == ["egitim", "egitim", "sinama", "dis"]


@t
def test_karar_kurali():
    def c(n, ay, alt, ust, p):
        b = {"ort": (alt + ust) / 2, "alt": alt, "ust": ust, "p": p}
        return {"n": n, "ay": ay, "ZAMANLAMA": b, "TOPLAM": b}
    H = {"A|1": c(500, 40, 0.001, 0.01, 0.01), "A|2": c(300, 30, 0.002, 0.02, 0.03), "A|3": c(50, 10, -0.05, -0.01, 0.9)}
    k = ES.es_kol_karar(H, "ZAMANLAMA"); assert k["durum"] == "ADAY_ONCESI" and k["p"] == 0.03 and k["hucre"] == ["A|1", "A|2"]
    H["A|2"] = c(300, 11, 0.002, 0.02, 0.03); assert ES.es_kol_karar(H, "ZAMANLAMA")["durum"] == "ÖLÇÜLEMEDİ"
    H["A|2"] = c(300, 30, -0.002, 0.02, 0.2); assert ES.es_kol_karar(H, "ZAMANLAMA")["durum"] == "YOK"
    H = {"A|1": c(500, 40, -0.02, -0.01, 0.99), "A|2": c(300, 30, -0.03, -0.001, 0.99)}; assert ES.es_kol_karar(H, "ZAMANLAMA")["durum"] == "EKSI"
    assert ES.es_kol_karar({"A|1": c(500, 40, 0.01, 0.02, 0.001)}, "ZAMANLAMA")["durum"] == "ÖLÇÜLEMEDİ"


@t
def test_secim_kapali_ve_26_kasim():
    S = ES.es_secim(); kap = ES.es_envanter_kapali(); tar = ES.es_kayit_tarih()
    assert S["secilen"] and len(S["secilen"]) <= 20
    for k in S["secilen"]:
        assert k not in kap, k
        assert tar[k] < "2026-11-26", k
    for k in ("Ç255", "Ç273", "Ç251", "Ç250"):
        assert k not in S["secilen"]
    for k in ("Ç47", "Ç49", "Ç91", "Ç85", "Ç227"):
        assert k not in S["secilen"]
    # sentetik: kapalı ya da geç tarihli bir kayıt okuyucusu olsa da seçilmez
    tar2 = dict(tar); tar2["Ç209"] = "2026-11-26"
    assert "Ç209" not in ES.es_secim(tarih=tar2)["secilen"]
    # sıra: envanter dosya satırı büyükten küçüğe
    L1 = {r["kod"]: r["sira"] for r in ES.es_envanter_liste1()}
    sira = [L1[k] for k in S["secilen"]]; assert sira == sorted(sira)


@t
def test_cakisma_kapisi():
    kod = open(ES.ES_YOL["kod"], encoding="utf-8").read()
    g = {"__name__": "es_test", "__file__": ES.ES_YOL["kod"]}
    exec(compile(kod, ES.ES_YOL["kod"], "exec"), g)   # temiz ad alanı: geçer
    g2 = {"__name__": "es_test", "__file__": ES.ES_YOL["kod"], "es_secim": "eski_ad"}
    try:
        exec(compile(kod, ES.ES_YOL["kod"], "exec"), g2)
    except RuntimeError as ex:
        assert "çakışma kapısı" in str(ex)
    else:
        raise AssertionError("çakışma kapısı çalışmadı")


if __name__ == "__main__":
    hata = 0
    for f in ISIM:
        try:
            f(); print("GEÇTİ", f.__name__)
        except Exception as ex:  # noqa: BLE001
            hata += 1; print("KALDI", f.__name__, type(ex).__name__, ex)
    print(f"{len(ISIM) - hata} / {len(ISIM)}")
    sys.exit(1 if hata else 0)
