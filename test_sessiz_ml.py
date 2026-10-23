# test_sessiz_ml.py — SESSIZ_ML mekanik sinama (2026-10-23)
# Calistir: python3 test_sessiz_ml.py   (repo kokunde; veri indirilmez, sentetik seri)
# 1) Ileriye bakis yok: serinin gelecegi degistirilince gecmis gunlerin ozellikleri degismez.
# 2) Etiket: once +%20 / once -%10 / ayni gun ikisi = 0 / ufuk dolmamissa NaN.
# 3) Ileri yuruyen egitim: test yili Y icin egitim kumesinde etiket ufku Y'ye tasan olay yok (embargo).
# 4) Cikis: ilk stop, +%8 sonrasi maliyete stop, +%20 sonrasi SMA20 trail, 120 bar ufuk ve model cikisi dogru calisir.
# 5) Portfoy: 30 slot dolunca yeni sinyal atlanir; ozkaynak cikista guncellenir.
# 7) Vektorel etiket (sm_once_vek) dongulu sm_once ile birebir ayni; maliyet = komisyon + 2 x kayma = %0,8.
# 8) Egitim kaniti: logloss egrisi yazilir (egitim kaybi duser) ve model dosyasi diske kaydedilir.
# 6) Cakisma kapisi: modul bellekteki baska bir adi ezerse durur.
# 9) v1.2 pazar bazinda esik: iki pazarin puan duzeyi farkliysa her pazar kendi egitim esigini alir (havuz esigi degil).
import sys, numpy as np, pandas as pd

import FON_IZI as F
import SESSIZ_ML as S


def seri(n=600, tohum=4):
    rng = np.random.default_rng(tohum); idx = pd.bdate_range("2019-01-01", periods=n)
    c = 100 * np.cumprod(1 + rng.normal(0.0005, 0.02, n)); o = np.r_[c[0], c[:-1]]
    return pd.DataFrame({"Open": o, "High": np.maximum(o, c) * 1.01, "Low": np.minimum(o, c) * 0.99, "Close": c,
                         "Volume": rng.integers(1000, 5000, n).astype(float)}, index=idx)


def sina():
    hata = []; A = S.SMAyar(); FA = F.FIAyar()
    d = seri(); z1 = S.sm_ozellik(d, FA)
    d2 = d.copy(); d2.iloc[450:, :4] *= 3.0; d2.iloc[450:, 4] *= 7
    z2 = S.sm_ozellik(d2, FA)
    a = z1.iloc[:450][S.OZ_KOL[:38]]; b = z2.iloc[:450][S.OZ_KOL[:38]]
    if not np.allclose(a.to_numpy(dtype=float), b.to_numpy(dtype=float), equal_nan=True):
        hata.append("1) gelecek degisince gecmis ozellik degisti (ileriye bakis)")
    h = np.array([100, 101, 125, 100, 100.]); l = np.array([100, 99, 99, 85, 100.])
    if S.sm_once(h, l, 100, 0, 3, 0.2, 0.1) != 1.0: hata.append("2) once +%20 isaretlenmedi")
    l2 = l.copy(); l2[1] = 85
    if S.sm_once(h, l2, 100, 0, 3, 0.2, 0.1) != 0.0: hata.append("2) once -%10 isaretlenmedi")
    h3 = h.copy(); h3[1] = 125; l3 = l.copy(); l3[1] = 85
    if S.sm_once(h3, l3, 100, 0, 3, 0.2, 0.1) != 0.0: hata.append("2) ayni gun ikisi olumsuz sayilmadi")
    if not np.isnan(S.sm_once(h, l, 100, 2, 3, 0.2, 0.1)): hata.append("2) ufuk dolmadan etiket verildi")
    rng = np.random.default_rng(0); n = 3000
    O = pd.DataFrame({"tarih": pd.to_datetime("2016-01-01") + pd.to_timedelta(rng.integers(0, 3800, n), "D"),
                      "y": rng.integers(0, 2, n).astype(float), "pazar": rng.choice(["BIST", "ABD"], n)})
    for k in S.OZ_KOL:
        O[k] = rng.normal(size=n)
    yakalanan = []
    import lightgbm as lgb
    orj = lgb.LGBMClassifier.fit
    def fit_izle(self, X, y, **kw):
        yakalanan.append(X.index); return orj(self, X, y, **kw)
    lgb.LGBMClassifier.fit = fit_izle
    try:
        A3 = S.SMAyar(test_yillari=(2021, 2023), gbm={**A.gbm, "n_estimators": 10})
        S.sm_ileri_egit(O, "y", 90, A3)
    finally:
        lgb.LGBMClassifier.fit = orj
    for Y, ix in zip((2021, 2023), yakalanan):
        if (O.loc[ix, "tarih"] + pd.Timedelta(days=90) >= pd.Timestamp(f"{Y}-01-01")).any():
            hata.append(f"3) {Y} egitiminde embargo ihlali")
    n = 200; o = np.full(n, 100.0); c = o.copy(); hh = o * 1.001; ll = o * 0.999; sma = np.full(n, 99.0)
    j, f, ned, _ = S.sm_cikis(o, hh, ll * np.r_[1, 1, 0.9, np.ones(n - 3)], c, sma, 0, 95.0, A)
    if not (j == 2 and ned == "stop" and abs(f - 95.0) < 1e-9): hata.append(f"4) ilk stop yanlis: {j} {f} {ned}")
    ust = np.full(n, 100.2)                     # dipler girisin ustunde: maliyete stop yalniz dip inince tetiklenmeli
    h4 = hh.copy(); h4[3] = 109; l4 = ust.copy(); l4[6] = 99.5
    j, f, ned, _ = S.sm_cikis(o, h4, l4, c, sma, 0, 95.0, A)
    if not (j == 6 and ned == "maliyet" and abs(f - 100) < 1e-9): hata.append(f"4) maliyete stop yanlis: {j} {f} {ned}")
    h5 = hh.copy(); h5[3] = 121; c5 = c.copy(); c5[10] = 98.0; s5 = np.full(n, 99.0)
    j, f, ned, _ = S.sm_cikis(o, h5, ust, c5, s5, 0, 95.0, A)
    if not (j == 10 and ned == "trail"): hata.append(f"4) trail yanlis: {j} {ned}")
    j, f, ned, _ = S.sm_cikis(o, hh, ll, c, sma, 0, 95.0, A)
    if not (j == 120 and ned == "ufuk"): hata.append(f"4) ufuk yanlis: {j} {ned}")
    ps = np.full(n, 0.1); ps[7] = 0.9
    j, f, ned, _ = S.sm_cikis(o, hh, ll, c, sma, 0, 95.0, A, ps, 0.5)
    if not (j == 7 and ned == "model"): hata.append(f"4) model cikisi yanlis: {j} {ned}")
    t0 = pd.Timestamp("2024-01-01")
    I = pd.DataFrame({"giris_t": [t0] * 31, "cikis_t": [t0 + pd.Timedelta(days=10)] * 31, "getiri": [0.3] * 30 + [5.0]})
    r = S.sm_portfoy(I, A)
    if not (r["islem"] == 30 and abs(r["portfoy"] - 30.0) < 1e-6): hata.append(f"5) portfoy slot/ozkaynak yanlis: {r}")
    dv = seri(800, 9); h7, l7, c7 = (dv[k].to_numpy() for k in ("High", "Low", "Close")); ix = np.arange(0, 800, 7)
    for uf, yu, asg in ((20, 0.1, 0.1), (60, 0.2, 0.1), (250, 1.0, 0.3)):
        v1 = S.sm_once_vek(h7, l7, c7, ix, uf, yu, asg); v2 = np.array([S.sm_once(h7, l7, c7[i], i, uf, yu, asg) for i in ix])
        if not np.array_equal(np.nan_to_num(v1, nan=-1), np.nan_to_num(v2, nan=-1)): hata.append(f"7) vektorel etiket farkli (ufuk {uf})")
    hh9 = np.array([100, 101, 102, 101, 100.]); ll9 = np.array([100, 99, 98, 99, 100.]); cc9 = np.full(5, 100.0)
    if S.sm_ilk_vek(hh9, ll9, cc9, np.array([0]), 3, 0.1, 0.1)[0] != 0.0: hata.append("7) hicbiri gelmeyince 0 verilmedi")
    ll9b = ll9.copy(); ll9b[2] = 89
    if S.sm_ilk_vek(hh9, ll9b, cc9, np.array([0]), 3, 0.1, 0.1)[0] != -1.0: hata.append("7) once asagi -1 verilmedi")
    if abs(A.maliyet - 0.008) > 1e-12: hata.append(f"7) maliyet yanlis: {A.maliyet}")
    import tempfile, os
    with tempfile.TemporaryDirectory() as td:
        O8 = O.copy(); O8["y"] = (O8[S.OZ_KOL[0]] + rng.normal(0, 1, len(O8)) > 0).astype(float)
        A8 = S.SMAyar(test_yillari=(2023,), gbm={**A.gbm, "n_estimators": 50}, cikti=td)
        _, _, _, kan = S.sm_ileri_egit(O8, "y", 90, A8, ad="deneme")
        if kan.empty or not (kan.egitim_kayip_son.iat[0] < kan.egitim_kayip_ilk.iat[0]) or not os.path.exists(kan.dosya.iat[0]):
            hata.append(f"8) egitim kaniti eksik: {kan.to_dict('records')}")
        O9 = O8.copy(); O9["pazar"] = np.where(np.arange(len(O9)) % 2 == 0, "ABD", "BIST")
        O9.loc[O9.pazar == "ABD", S.OZ_KOL[0]] += 3.0
        O9["y"] = (O9[S.OZ_KOL[0]] + rng.normal(0, 1, len(O9)) > 0).astype(float)
        P9, _, _, _ = S.sm_ileri_egit(O9, "y", 90, S.SMAyar(test_yillari=(2023,), gbm={**A.gbm, "n_estimators": 50}, cikti=td))
        t9 = P9[P9.p.notna()]
        if "esik_pz" not in t9 or t9.esik_pz.isna().any():
            hata.append("9) pazar esigi yazilmadi")
        else:
            e9 = t9.groupby("pazar").esik_pz.first()
            if not (e9.get("ABD", 0) > e9.get("BIST", 1)):
                hata.append(f"9) pazar esikleri ayrismadi: {e9.to_dict()}")
    g = {"SMAyar": object(), "__name__": "kapi_test"}
    try:
        src = open("SESSIZ_ML.py", encoding="utf-8").read()
        g["_CK_KAYIT"] = {"SMAyar": "BASKA.py"}
        exec(compile(src.replace("from __future__ import annotations\n", ""), "SESSIZ_ML.py", "exec"), g)
        hata.append("6) cakisma kapisi baska dosyanin adini ezince durmadi")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex): hata.append(f"6) beklenmeyen hata: {ex}")
    except Exception as ex:
        hata.append(f"6) kapi sinamasi calismadi: {type(ex).__name__} {ex}")
    return hata


if __name__ == "__main__":
    h = sina()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_sessiz_ml: 9/9 OK")
