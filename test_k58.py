"""K58 testleri (ağ gerekmez; yalnız sentetik veri, gerçek getiri ölçmez). Çalıştırma: python test_k58.py

1) çakışma kapısı  2) ön kayıt mührü (zaman, üzerine yazmama, bozuk mühür reddi; gerçek K58_ON_KAYIT.md bugünkü eşiklerle aynı,
koşu meta'sı varsa ön kayıt koşudan önce)  3) mühürsüz koşu durur  4) FI_OLCUT kararı FON_IZI ile aynı (k58_tutar)
5) A: δ enjeksiyonu eşlere dokunmaz, plasebo hücreleri FI eş şartıyla uyumlu, tekrar aynı tohumla birebir, büyük δ tutar
6) C: aylık sinyalde geleceğe bakma yok (ay sonu k'dan sonraki fiyat bozulunca k ve öncesi sinyal / evren aynı); SMA sinyalleri de
7) C: portföy muhasebesi (devir, maliyet, kıyas) ve cetvel (kâhin sinyal TUTAR, NW t lag 0 = sıradan t), plasebo tohumla aynı
8) C4a: trend filtresi geleceğe bakmaz, sıfır atma düzeltmesi, karar kuralı  9) French ayrıştırıcı (sentetik zip; `python -I` alt
süreci dahil)  10) e-posta / anahtar yok  11) rapor yolu sentetik çıktılarla (gerçek veri yok).
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import K58 as K  # noqa: E402

FI = K.FI


def sentetik_V(n: int = 70, bas: str = "2015-06-01", bit: str = "2019-12-31", tohum: int = 1) -> dict:
    """Sentetik OHLCV paneli: hisse başına sabit sürüklenme (momentum kalıcılığı) + gürültü; birkaç hisse geç başlar."""
    rng = np.random.default_rng(tohum); idx = pd.bdate_range(bas, bit); V = {}
    for i in range(n):
        mu = rng.normal(0.0003, 0.0008); r = rng.normal(mu, 0.02, len(idx))
        c = 50 * np.exp(np.cumsum(r)); o = c * np.exp(rng.normal(0, 0.005, len(idx)))
        d = pd.DataFrame({"Open": o, "High": np.maximum(o, c) * 1.01, "Low": np.minimum(o, c) * 0.99, "Close": c,
                          "Volume": rng.integers(1e4, 1e6, len(idx)).astype(float)}, index=idx)
        V[f"S{i:03d}"] = d.iloc[int(rng.integers(0, 200)) if i % 7 == 0 else 0:]
    return V


def testler() -> list:
    hata = []
    # 1) çakışma kapısı
    src = open(os.path.join(KOK, "K58.py"), encoding="utf-8").read().replace("from __future__ import annotations\n", "")
    g = {"__name__": "kapi_test", "k58_kos": object(), "_CK_KAYIT": {"k58_kos": "BASKA.py"}}
    try:
        exec(compile(src, "K58.py", "exec"), g)
        hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) beklenmeyen hata: {ex}")
    g2 = {"__name__": "kapi_test2"}
    try:
        exec(compile(src, "K58.py", "exec"), g2); exec(compile(src, "K58.py", "exec"), g2)
    except Exception as ex:
        hata.append(f"1) temiz yükleme / yeniden yükleme durdu: {type(ex).__name__} {ex}")
    # 2) ön kayıt
    with tempfile.TemporaryDirectory() as td:
        y = K.k58_onkayit(td); ilk = open(y, encoding="utf-8").read()
        if K.k58_esik_sha() not in ilk or not re.search(r"^Yazım zamanı: \d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC", ilk, re.M):
            hata.append("2) ön kayıtta mühür / UTC zaman yok")
        for parca in ("## A.", "## B.", "## C.", "## C4.", "## D.", "C1 POZİTİF", "C2 PLASEBO", "C3:", "RİSK FİLTRESİ OLARAK TUTAR", "HAYATTA KALMA"):
            if parca not in ilk:
                hata.append(f"2) ön kayıtta '{parca}' yok")
        K.k58_onkayit(td)
        if open(y, encoding="utf-8").read() != ilk:
            hata.append("2) ön kayıt üzerine yazıldı")
        if K.k58_onkayit_dogrula(td)["sha"] != K.k58_esik_sha():
            hata.append("2) doğrulama mührü yanlış")
        open(y, "w", encoding="utf-8").write(ilk.replace(K.k58_esik_sha(), "0" * 64))
        try:
            K.k58_onkayit_dogrula(td); hata.append("2) bozuk mühür kabul edildi")
        except K.K58Hata:
            pass
        try:
            K.k58_onkayit(td); hata.append("2) mührü farklı ön kayıt sessizce kabul edildi")
        except K.K58Hata:
            pass
    gercek = K._k58_yol("onkayit")
    if not os.path.exists(gercek):
        hata.append("2) arastirma_cikti/k58_cetvel_sagla/K58_ON_KAYIT.md yok")
    else:
        oc = K.k58_onkayit_dogrula()
        my = K._k58_yol("meta")
        if os.path.exists(my):
            meta = json.load(open(my, encoding="utf-8"))
            if pd.Timestamp(oc["zaman_utc"]) > pd.Timestamp(meta["kos_baslangic"].replace(" UTC", "")):
                hata.append("2) ön kayıt koşudan sonra yazılmış")
    # 3) mühürsüz koşu durur
    with tempfile.TemporaryDirectory() as td:
        try:
            K.k58_kos(td, "B"); hata.append("3) ön kayıtsız koşu durmadı")
        except K.K58Hata:
            pass
    # 4) k58_tutar = FON_IZI kararı
    O = K._k58_olcut()
    taban = {"n": 50, "alt95": 0.01, "sira": 0.55, "portfoy": 0.3, "portfoy_esli_p90": 0.2}
    for degis, bek in (({}, True), ({"n": 29}, False), ({"alt95": -0.001}, False), ({"sira": 0.5}, False),
                       ({"portfoy": 0.2}, False), ({"n": 0}, False)):
        if K.k58_tutar({**taban, **degis}, O) != bek:
            hata.append(f"4) k58_tutar {degis} -> {not bek} (beklenen {bek})")
    # 5) A sentetik panelde
    V = sentetik_V()
    P = FI.fi_olcut_panel(V, O)
    A = {**K.K58_ESIK["A"], "n": [30], "delta": [0.0, 0.02, 0.5], "tekrar": 2, "bas": "2016-01-01", "bit": "2019-09-30"}
    hc = K.k58_gecerli_hucreler(P, A["bas"], A["bit"], A["min_es"])
    if not len(hc[0]):
        hata.append("5) geçerli plasebo hücresi yok")
    else:
        d, j = hc
        if not P["ok"][d, j].all() or (P["tarih"][d] < pd.Timestamp(A["bas"])).any() or (P["tarih"][d] > pd.Timestamp(A["bit"])).any():
            hata.append("5) plasebo hücresi FI 'ok' / tarih aralığı dışında")
        r1 = K.k58_guc_tekrar(P, hc, 30, 0, A, O); r2 = K.k58_guc_tekrar(P, hc, 30, 0, A, O); r3 = K.k58_guc_tekrar(P, hc, 30, 1, A, O)
        if pd.DataFrame(r1).to_json() != pd.DataFrame(r2).to_json():
            hata.append("5) aynı tohumla tekrar farklı sonuç verdi")
        if pd.DataFrame(r1).ort_fark.tolist() == pd.DataFrame(r3).ort_fark.tolist():
            hata.append("5) farklı tekrar aynı olay kümesini çekti")
        if not r1[-1]["tutar"] or not r1[-1]["s_aralik"]:
            hata.append("5) δ +%50 tutmadı (güç hesabı bozuk)")
        if abs((r1[1]["ort_fark"] - r1[0]["ort_fark"]) - 0.02) > 1e-9:
            hata.append("5) δ ortalama farka tam eklenmedi")
        rng = np.random.default_rng(3); s = rng.choice(len(hc[0]), 30, replace=False)
        X = FI.fi_olcut_olay(P, pd.DataFrame({"sembol": [P["sembol"][x] for x in hc[1][s]], "giris": P["tarih"][hc[0][s]]}))
        if X.fark.isna().any():
            hata.append("5) geçerli hücrede FI eşli fark NaN (eş şartı uyumsuz)")
        Y = K.k58_delta_ekle(X, 0.05)
        if not np.allclose(Y.esli_r60, X.esli_r60) or not np.allclose(Y.fark - X.fark, 0.05) or (Y.sira < X.sira - 1e-12).any():
            hata.append("5) δ enjeksiyonu eşlere dokundu / fark ya da sıra yanlış")
        with tempfile.TemporaryDirectory() as td:
            hy = os.path.join(td, "ham.csv"); A2 = {**A, "tekrar": 2}
            E = K.k58_guc(P, hy, A2, islem=1); E2 = K.k58_guc(P, hy, A2, islem=1)
            if len(E) != 2 * 3 or len(E2) != len(E):
                hata.append("5) k58_guc satır sayısı / kaldığı yerden sürme yanlış")
            Eg = K.k58_guc(P, os.path.join(td, "ham2.csv"), A2, islem=2)
            if not np.allclose(Eg.sort_values(["tekrar", "delta"]).ort_fark.to_numpy(), E.sort_values(["tekrar", "delta"]).ort_fark.to_numpy()):
                hata.append("5) paralel koşu seri koşudan farklı")
            Z = K.k58_guc_ozet(E)
            if set(Z.columns) < {"n", "delta", "guc", "guc4", "yari"} or len(Z) != 3:
                hata.append("5) güç özeti eksik")
    # 6) geleceğe bakma yok (aylık sinyal)
    Kc = {**K.K58_ESIK["C"], "bas": "2016-07-01", "kriz": "2019-12-31", "min_evren": 30}
    M = K.k58_aylik(V, Kc); Sm = K.k58_sinyal_momentum(M, Kc); Ss = K.k58_sinyal_sma(M)
    k0 = int(np.flatnonzero(M["olusum"])[10]); t0 = M["ay_sonu"][k0]
    rng = np.random.default_rng(9)
    Vb = {s: d.assign(Close=np.where(d.index > t0, d.Close * rng.uniform(0.3, 3.0, len(d)), d.Close)) for s, d in V.items()}
    Mb = K.k58_aylik(Vb, Kc); Smb = K.k58_sinyal_momentum(Mb, Kc); Ssb = K.k58_sinyal_sma(Mb)
    if not np.array_equal(M["U"][:k0 + 1], Mb["U"][:k0 + 1]) or not np.allclose(Sm[:k0 + 1], Smb[:k0 + 1], equal_nan=True):
        hata.append("6) momentum sinyali / evren ay sonu k'dan sonraki fiyatı görüyor")
    for ad in Ss:
        if not np.array_equal(Ss[ad][:k0 + 1], Ssb[ad][:k0 + 1]):
            hata.append(f"6) {ad} ay sonu k'dan sonraki fiyatı görüyor")
    if np.allclose(Sm[k0 + 13:], Smb[k0 + 13:], equal_nan=True):
        hata.append("6) bozma testi etkisiz (sonraki sinyaller de değişmedi)")
    if not np.allclose(M["R"][:k0], Mb["R"][:k0], equal_nan=True):
        hata.append("6) k'dan önceki ay getirileri değişti")
    if (M["ay_sonu"][M["olusum"]] < pd.Timestamp(Kc["bas"])).any() or M["olusum"][-1]:
        hata.append("6) oluşum ayı aralık dışında / son ay oluşumda")
    # 7) portföy muhasebesi ve cetvel
    R = np.array([[0.10, 0.0, -0.05], [0.0, 0.2, 0.1]]); U = np.ones_like(R, bool); ol = np.array([True, True])
    sec = np.array([[True, True, False], [True, True, False]])
    Pf = K.k58_portfoy(R, sec, U, ol, 0.001)
    w_k = np.array([0.5 * 1.1, 0.5, 0]) / 1.05; dv2 = np.abs(np.array([0.5, 0.5, 0]) - w_k).sum()
    if not (np.isclose(Pf["brut"][0], 0.05) and np.isclose(Pf["devir"][0], 1.0) and np.isclose(Pf["net"][0], (1 - 0.001) * 1.05 - 1)
            and np.isclose(Pf["devir"][1], dv2) and np.isclose(Pf["kiyas"][0], 0.05 / 3)):
        hata.append(f"7) portföy muhasebesi yanlış: {Pf}")
    x = np.random.default_rng(1).normal(0.001, 0.02, 120)
    t0_ = x.mean() / (x.std(ddof=0) / np.sqrt(len(x)))
    if not np.isclose(K.k58_nw_t(x, 0), t0_):
        hata.append("7) NW t (gecikme 0) sıradan t ile aynı değil")
    kah = M["R"].copy(); kah[~M["U"]] = np.nan
    o = K.k58_portfoy_olc(K.k58_portfoy(M["R"], K.k58_ust_dilim(kah, M["U"], 0.1), M["U"], M["olusum"], 0.001), Kc)
    if not o["tutar"]:
        hata.append("7) kâhin sinyal (gelecek ay getirisi) cetvelden geçmedi")
    e = np.r_[np.full(30, 0.01), np.full(30, -0.01), np.full(40, 0.002)]
    c = K.k58_cetvel(e, Kc)
    if c["s_alt"] is not True or not np.isclose(c["son30"], 0.002) or c["ay"] != 100:
        hata.append(f"7) cetvel alt dönem / son %30 yanlış: {c}")
    Kp = {**Kc, "plasebo_n": 3}
    p1 = K.k58_plasebo(M, 0.001, Kp); p2 = K.k58_plasebo(M, 0.001, Kp)
    if p1.to_json() != p2.to_json() or p1.nw_t.nunique() < 2:
        hata.append("7) plasebo tohumla birebir tekrar etmiyor / plasebolar aynı")
    if not (p1.brut_yillik_fazla >= p1.yillik_fazla - 1e-12).all():
        hata.append("7) maliyet net getiriyi düşürmüyor")
    sec_s = Ss["C4b1_sma200_ustu"]
    ep = K.k58_esli_plasebo(M, sec_s, 0.001, {**K.K58_ESIK["C4"], "esli_plasebo_n": 2}, Kc)
    if len(ep) != 2:
        hata.append("7) eşli plasebo satırı eksik")
    # 8) C4a trend filtresi
    idx = pd.bdate_range("2010-01-01", periods=900)
    c_ = np.r_[np.linspace(100, 200, 500), np.linspace(200, 80, 200), np.linspace(80, 150, 200)]
    d = pd.DataFrame({"Open": c_ * 0.999, "Close": c_}, index=idx)
    G = K.k58_trend_getiri(d, 0.001)
    t0 = 600; d2 = d.copy(); d2.iloc[t0:, :] = d2.iloc[t0:, :].to_numpy() * 1.7
    G2 = K.k58_trend_getiri(d2, 0.001)
    if not np.allclose(G.poz.to_numpy()[:t0 + 1], G2.poz.to_numpy()[:t0 + 1], equal_nan=True):
        hata.append("8) trend pozisyonu gün t'de t ve sonrası kapanışı görüyor")
    oc_ = K.k58_trend_olc(G, "2010-01-01", "2014-01-01")
    if not (abs(oc_["filtre_mdd"]) < abs(oc_["al_tut_mdd"])) or oc_["elde_pay"] >= 1:
        hata.append(f"8) filtre düşüşte nakde geçmedi: {oc_}")
    C4 = K.K58_ESIK["C4"]
    for o_, bek in (({"filtre_yillik": 0.0905, "al_tut_yillik": 0.10, "filtre_mdd": -0.30, "al_tut_mdd": -0.50}, "RİSK FİLTRESİ OLARAK TUTAR"),
                    ({"filtre_yillik": 0.08, "al_tut_yillik": 0.10, "filtre_mdd": -0.30, "al_tut_mdd": -0.50}, "TUTMAZ"),
                    ({"filtre_yillik": 0.10, "al_tut_yillik": 0.10, "filtre_mdd": -0.40, "al_tut_mdd": -0.50}, "TUTMAZ"),
                    ({"filtre_yillik": -0.01, "al_tut_yillik": -0.02, "filtre_mdd": -0.20, "al_tut_mdd": -0.60}, "RİSK FİLTRESİ OLARAK TUTAR")):
        if K.k58_trend_karar(o_, C4) != bek:
            hata.append(f"8) C4a karar kuralı yanlış: {o_}")
    with tempfile.TemporaryDirectory() as td:
        gun = pd.bdate_range("2019-01-01", periods=400).tz_localize("Europe/Istanbul")
        ts = [int(x) for x in (gun - pd.Timestamp("1970-01-01", tz="UTC")) // pd.Timedelta("1s")]
        cl = np.r_[np.full(300, 100000.0), np.full(100, 1000.0)] * np.linspace(1, 1.2, 400)
        J = {"chart": {"result": [{"meta": {"exchangeTimezoneName": "Europe/Istanbul"}, "timestamp": ts,
                                   "indicators": {"quote": [{"open": cl.tolist(), "close": cl.tolist()}]}}]}}
        yy = os.path.join(td, "x.json"); json.dump(J, open(yy, "w"))
        dd, notlar = K.k58_yahoo_oku(yy, {**C4, "kes": "2030-01-01"})
        if not notlar or (dd.Close.pct_change().abs() > 0.5).any():
            hata.append("8) sıfır atma düzeltilmedi")
        if K.k58_endeks_bas(K.k58_trend_getiri(dd, 0.003), "BIST") != "2020-01-01":
            hata.append("8) BIST başlangıç yılı kuralı yanlış")
    # 9) French ayrıştırıcı
    with tempfile.TemporaryDirectory() as td:
        ff = ("This file was created by test.\nThe 1-month TBill return is from test.\n\n,Mkt-RF,SMB,HML,RMW,CMA,RF\n"
              "196307,  -0.39,  -0.41,  -0.97,   0.68,  -1.18,   0.27\n196308,   5.07,  -0.80,   1.80,   0.36,  -0.35,   0.25\n"
              "196309,  -99.99,  -0.52,   0.13,  -0.71,   0.29,   0.27\n\n Annual Factors: January-December \n,Mkt-RF,SMB,HML,RMW,CMA,RF\n"
              "  1964,  12.0, 1.0, 2.0, 3.0, 4.0, 3.5\n")
        mo = "Momentum test\n\n          ,Mom   \n196307,   0.90\n196308,   1.00\n\n Annual Factors: \n,Mom\n  1964, 10.0\n"
        z1, z2 = os.path.join(td, "ff.zip"), os.path.join(td, "mo.zip")
        with zipfile.ZipFile(z1, "w") as z:
            z.writestr("F-F_Research_Data_5_Factors_2x3.csv", ff)
        with zipfile.ZipFile(z2, "w") as z:
            z.writestr("F-F_Momentum_Factor.csv", mo)
        D1 = K.k58_french_oku(z1); D2 = K.k58_french_isolated(z2); D1i = K.k58_french_isolated(z1)
        if list(D1.columns) != ["MKT_RF", "SMB", "HML", "RMW", "CMA", "RF"] or len(D1) != 3 or not np.isnan(D1.MKT_RF.iloc[2]) \
                or D1.index[0] != pd.Period("1963-07", "M") or not np.isclose(D1.SMB.iloc[1], -0.80):
            hata.append(f"9) French ayrıştırma yanlış: {D1}")
        if list(D2.columns) != ["UMD"] or len(D2) != 2 or not D1i.equals(D1):
            hata.append("9) French '-I' alt süreci farklı / momentum yanlış")
        Dj = D1.join(D2, how="left")
        try:
            Bk = {**K.K58_ESIK["B"], "donem": [["1963-2026", "1963-07", "2026-12"], ["2000-2026", "2000-01", "2026-12"]], "alt_donem": []}
            Zf, Tf = K.k58_french_olc(Dj, Bk)
            if len(Zf) != 12 or Tf.cetvel_tutar.any():
                hata.append("9) French ölçümü küçük veride satır / karar yanlış")
        except Exception as ex:
            hata.append(f"9) French ölçümü küçük veride beklenmeyen hata: {type(ex).__name__} {ex}")
        # uzun sentetik faktör serisi: bilinen ortalama ve t
        ay = pd.period_range("1963-07", "2026-08", freq="M"); rs = np.random.default_rng(5)
        Dl = pd.DataFrame({f: rs.normal(0.5, 4.0, len(ay)) for f in K.K58_ESIK["B"]["faktor"]}, index=ay)
        Zl, Tl = K.k58_french_olc(Dl)
        x = Dl.MKT_RF.to_numpy() / 100; r0 = Zl[(Zl.faktor == "MKT_RF") & (Zl.donem == "1963-2026")].iloc[0]
        if not (np.isclose(r0.ort_aylik, x.mean()) and np.isclose(r0.t, x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) and r0.ay == len(x)):
            hata.append("9) French istatistikleri yanlış")
        if len(Tl) != 6 or not {"cetvel_tutar", "alt_arti"} <= set(Tl.columns):
            hata.append("9) French cetvel tablosu eksik")
        with zipfile.ZipFile(os.path.join(td, "kotu.zip"), "w") as z:
            z.writestr("a.csv", "x"); z.writestr("b.csv", "y")
        try:
            K.k58_french_oku(os.path.join(td, "kotu.zip")); hata.append("9) çok dosyalı zip kabul edildi")
        except K.K58Hata:
            pass
    # 11) rapor yolu: sentetik çıktılarla bütün tablolar ve D kararları yazılır (gerçek veri yok)
    with tempfile.TemporaryDirectory() as td:
        K.k58_onkayit(td)
        Ea = K.k58_guc(P, K._k58_yol("a_ham", td), {**A, "n": [30], "delta": list(K.K58_ESIK["A"]["delta"]), "tekrar": 2}, islem=1)
        K.k58_guc_ozet(Ea).to_csv(K._k58_yol("a", td), index=False)
        Zl.to_csv(K._k58_yol("b", td), index=False); Tl.to_csv(K._k58_yol("b_cetvel", td), index=False)
        sat = [{"pazar": pz, "sinyal": "C1_momentum_12_1", **K.k58_portfoy_olc(K.k58_portfoy(M["R"], K.k58_ust_dilim(Sm, M["U"], 0.1), M["U"], M["olusum"], 0.001), Kc)}
               for pz in ("ABD", "BIST")]
        for ad, s_ in Ss.items():
            o_ = K.k58_portfoy_olc(K.k58_portfoy(M["R"], s_, M["U"], M["olusum"], 0.001), Kc); o_.update({"esli_plasebo_yuzdelik": 0.5, "ort_hisse": 10.0})
            sat.append({"pazar": "ABD", "sinyal": ad, **o_})
        pd.DataFrame(sat).to_csv(K._k58_yol("c", td), index=False)
        pd.concat([p1.assign(pazar="ABD"), p1.assign(pazar="BIST")]).to_csv(K._k58_yol("c_plasebo", td), index=False)
        oa = K.k58_trend_olc(G, "2010-01-01", "2014-01-01")
        pd.DataFrame([{"pazar": "ABD", "endeks": "SPY", "donem": "tam", "bas": "2010-01-01", **oa, "karar": K.k58_trend_karar(oa), "not": ""}]).to_csv(K._k58_yol("c4a", td), index=False)
        try:
            ry = K.k58_rapor(td); rt = open(ry, encoding="utf-8").read(); kr = K.k58_karar(td)
            for parca in ("## A.", "## B.", "## C.", "## C4a.", "D1:", "D2 (karar pazarı ABD)", "## Özet"):
                if parca not in rt:
                    hata.append(f"11) raporda '{parca}' yok")
            if not {"D1", "D2", "D2_ABD", "C4a", "C4b"} <= set(kr):
                hata.append(f"11) karar sözlüğü eksik: {set(kr)}")
        except Exception as ex:
            hata.append(f"11) rapor sentetik çıktılarla çöktü: {type(ex).__name__} {ex}")
    # 10) e-posta / anahtar yok
    dosyalar = [os.path.join(KOK, "K58.py"), os.path.join(KOK, "test_k58.py")] + ([gercek] if os.path.exists(gercek) else [])
    for y in dosyalar:
        t = open(y, encoding="utf-8").read()
        if re.search(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b", t):
            hata.append(f"10) e-posta var: {os.path.basename(y)}")
        if re.search(r"(api[_-]?key|token|secret|password)\s*[=:]\s*['\"][A-Za-z0-9_\-]{12,}", t, re.I):
            hata.append(f"10) anahtar benzeri dize var: {os.path.basename(y)}")
    return hata


if __name__ == "__main__":
    H = testler()
    if H:
        print("K58 TEST: HATA", len(H)); print("\n".join(H)); sys.exit(1)
    print("K58 TEST: 11/11 bölüm GEÇTİ")
