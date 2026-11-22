"""test_tezgah_dogrulama — TEZGAH_DOGRULAMA.py mekanik denetimleri (sentetik veri; gerçek veri / sonuç görülmez, ağ isteği yok).

Kapsam: çakışma kapısı; French CSV ayrıştırma (bölüm, eksik kod, yıllık satır atlama, sütun sayısı kapısı); French zip -> seriler
(piyasa = Mkt-RF + RF, onluk farkı, Prior_1_0 alt - üst, EW piyasa firma ağırlıklı); 2023-12 kesiği; hüküm eşikleri; karşılaştırma
(özdeş -> DOĞRU, gürültü -> UYUŞMUYOR, pencere, n < 36); portföy = düz hesap (onluk EW / LQ, 2x3, U30A30, sıralama getiriden bağımsız);
uçtan uca sentetik panel -> kesit -> seriler -> td_yeniden (düz pandas) tutar; e-posta taraması; kapı (ön kayıt yok -> durur).
Çalıştır:  python test_tezgah_dogrulama.py
"""
from __future__ import annotations

import io
import os
import shutil
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import TEZGAH_DOGRULAMA as TD  # noqa: E402
import OLCU_SINAMA as OS  # noqa: E402
import test_olcu_sinama as TOS  # noqa: E402  (yalnız sentetik veri üreticisi)


# ------------------------------------------------------------------ çakışma kapısı
def test_cakisma_kapisi():
    kaynak = open(os.path.join(KOK, "TEZGAH_DOGRULAMA.py"), encoding="utf-8").read()
    ns = {"__name__": "td_test"}
    exec(compile(kaynak, "TEZGAH_DOGRULAMA.py", "exec"), ns)
    exec(compile(kaynak, "TEZGAH_DOGRULAMA.py", "exec"), ns)          # aynı dosya yeniden: geçer
    ns2 = {"__name__": "td_test", "td_hukum": "başka modülün adı", "_CK_KAYIT": {}}
    try:
        exec(compile(kaynak, "TEZGAH_DOGRULAMA.py", "exec"), ns2)
    except RuntimeError as ex:
        assert "EZDİ" in str(ex)
    else:
        raise AssertionError("çakışma kapısı başka modülün adını ezmeye izin verdi")


# ------------------------------------------------------------------ French ayrıştırma
_PORT = """This file was created using the 202609 CRSP database.
It contains value- and equal-weighted returns for  10 prior-return portfolios.

Missing data are indicated by -99.99 or -999.

  Value Weight Returns -- Monthly
,Lo PRIOR,PRIOR 2,PRIOR 3,PRIOR 4,PRIOR 5,PRIOR 6,PRIOR 7,PRIOR 8,PRIOR 9,Hi PRIOR
202311,   1.00,   2.00,   3.00,   4.00,   5.00,   6.00,   7.00,   8.00,   9.00,  10.00
202312,  -1.00,   0.50,   0.50,   0.50,   0.50,   0.50,   0.50,   0.50,   0.50,   3.00
202401,   9.00,   9.00,   9.00,   9.00,   9.00,   9.00,   9.00,   9.00,   9.00,   9.00

  Average Equal Weighted Returns -- Monthly
,Lo PRIOR,PRIOR 2,PRIOR 3,PRIOR 4,PRIOR 5,PRIOR 6,PRIOR 7,PRIOR 8,PRIOR 9,Hi PRIOR
202311,   2.00,   2.00,   2.00,   2.00,   2.00,   2.00,   2.00,   2.00,   2.00,   4.00
202312, -99.99,   1.00,   1.00,   1.00,   1.00,   1.00,   1.00,   1.00,   1.00,   1.00

  Average Value Weighted Returns -- Annual
,Lo PRIOR,PRIOR 2,PRIOR 3,PRIOR 4,PRIOR 5,PRIOR 6,PRIOR 7,PRIOR 8,PRIOR 9,Hi PRIOR
2023,   5.00,   5.00,   5.00,   5.00,   5.00,   5.00,   5.00,   5.00,   5.00,   5.00

  Number of Firms in Portfolios
,Lo PRIOR,PRIOR 2,PRIOR 3,PRIOR 4,PRIOR 5,PRIOR 6,PRIOR 7,PRIOR 8,PRIOR 9,Hi PRIOR
202311,   100,   100,   100,   100,   100,   100,   100,   100,   100,   100
202312,   300,   100,   100,   100,   100,   100,   100,   100,   100,   100

Copyright 2026 Eugene F. Fama and Kenneth R. French
"""


def test_french_ayristir():
    B = TD.td_french_ayristir(_PORT)
    vw = TD._td_bolum(B, "Value Weight", "Monthly"); ew = TD._td_bolum(B, "Equal Weighted", "Monthly"); nf = TD._td_bolum(B, "Number of Firms")
    assert vw.shape == (3, 10) and ew.shape == (2, 10) and nf.shape == (2, 10)
    assert vw.loc[pd.Period("2023-11", "M"), "Hi PRIOR"] == 10.0 and np.isnan(ew.loc[pd.Period("2023-12", "M"), "Lo PRIOR"])
    assert not any("Annual" in k for k in B)                       # yıllık bölüm (4 haneli) alınmaz
    bozuk = _PORT.replace("202312,  -1.00,", "202312,")
    try:
        TD.td_french_ayristir(bozuk)
    except TD.TDHata as ex:
        assert "sütun sayısı" in str(ex)
    else:
        raise AssertionError("sütun sayısı kapısı çalışmadı")


def _zip(ad: str, metin: str) -> bytes:
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr(ad.replace("_CSV.zip", ".csv"), metin)
    return b.getvalue()


def _fac(kol: str, deger: str) -> str:
    return f"Header text\n\n,{kol}\n202311,{deger}\n202312,{deger}\n202401,{deger}\n\n Annual Factors:\n,{kol}\n2023,{deger}\n"


def test_french_seriler_ve_kesik():
    z = {"F-F_Research_Data_Factors_CSV.zip": _zip("F-F_Research_Data_Factors_CSV.zip",
                                                    "x\n\n,Mkt-RF,SMB,HML,RF\n202311,   2.00,  0.1,  0.2,   0.40\n202312,  -1.00, 0.1, 0.2, 0.50\n"),
         "F-F_Momentum_Factor_CSV.zip": _zip("F-F_Momentum_Factor_CSV.zip", _fac("Mom", "1.50")),
         "F-F_ST_Reversal_Factor_CSV.zip": _zip("F-F_ST_Reversal_Factor_CSV.zip", _fac("ST_Rev", "-0.70")),
         "10_Portfolios_Prior_12_2_CSV.zip": _zip("10_Portfolios_Prior_12_2_CSV.zip", _PORT),
         "10_Portfolios_Prior_1_0_CSV.zip": _zip("10_Portfolios_Prior_1_0_CSV.zip", _PORT),
         "Europe_3_Factors_CSV.zip": _zip("Europe_3_Factors_CSV.zip", "x\n\n,Mkt-RF,SMB,HML,RF\n202311,   3.00,  0.1,  0.2,   0.40\n"),
         "Europe_Mom_Factor_CSV.zip": _zip("Europe_Mom_Factor_CSV.zip", _fac("WML", "2.00"))}
    S, _ = TD.td_french_seriler(z)
    p11, p12 = pd.Period("2023-11", "M"), pd.Period("2023-12", "M")
    assert abs(S["US_MKT"][p11] - 0.024) < 1e-12 and abs(S["US_MKT"][p12] - (-0.005)) < 1e-12
    assert abs(S["US_MOM"][p11] - 0.015) < 1e-12 and abs(S["US_STREV"][p11] + 0.007) < 1e-12
    assert abs(S["US_P12_VW_FARK"][p11] - 0.09) < 1e-12 and abs(S["US_P1_VW_FARK"][p11] + 0.09) < 1e-12   # P1: alt - üst
    assert abs(S["US_P12_EW_FARK"][p11] - 0.02) < 1e-12
    assert abs(S["US_EWMKT"][p11] - (9 * 2 + 4) / 10 / 100) < 1e-12              # firma ağırlıklı (eşit sayı)
    assert np.isnan(S["US_EWMKT"][p12])                                            # eksik onluk -> NaN (min_count)
    assert abs(S["EU_MKT"][p11] - 0.034) < 1e-12 and abs(S["EU_WML"][p11] - 0.02) < 1e-12
    K = TD._td_kes(S)
    assert all(v.index.max() <= pd.Period("2023-12", "M") for v in K.values() if len(v))
    assert pd.Period("2024-01", "M") in S["US_MOM"].index and pd.Period("2024-01", "M") not in K["US_MOM"].index
    assert TD._ay_ts("2023-12") == pd.Timestamp("2023-12-31")                       # KASA kesiğini aşmaz (end_time değil)


def test_french_elle_bosluklu():
    tmp = tempfile.mkdtemp(prefix="td_test_")
    try:
        icerik = {"F-F_Momentum_Factor_CSV.zip": "x\n\n,Mom\n202003,   8.20\n",
                  "F-F_Research_Data_Factors_CSV.zip": "x\n\n,Mkt-RF,SMB,HML,RF\n201811,   1.71,  -0.72,   0.34,   0.18\n",
                  "10_Portfolios_Prior_12_2_CSV.zip": "x\n  Value Weight Returns -- Monthly\n,a,b,c,d,e,f,g,h,i,j\n202106,   2.55,0,0,0,0,0,0,0,0,   9.25\n",
                  "Europe_Mom_Factor_CSV.zip": "x\n\n,WML\n201912    ,2.45\n"}
        for ad, m in icerik.items():
            open(os.path.join(tmp, ad), "wb").write(_zip(ad, m))
        J = {"ref_seriler": {"US_MOM": {"2020-03": 0.082}, "US_MKT": {"2018-11": 0.0189}, "US_P12_VW_FARK": {"2021-06": 0.067},
                             "EU_WML": {"2019-12": 0.0245}}}
        R = TD.td_french_elle(J, kl=tmp)
        assert all(r["tutar"] for r in R), R                        # Avrupa '201912    ,' biçimi dahil (H-TD1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ hüküm ve karşılaştırma
def test_hukum():
    h = TD.td_hukum
    assert h(0.75, 0.72, 96, False) == "DOĞRU" and h(0.75, 0.65, 96, False) == "KISMEN" and h(0.55, 0.9, 96, False) == "KISMEN"
    assert h(0.39, 0.9, 96, False) == "UYUŞMUYOR" and h(0.85, 0.9, 96, True) == "KISMEN" and h(0.91, 0.8, 96, True) == "DOĞRU"
    assert h(0.95, 0.95, 20, True) == "ÖLÇÜLEMEDİ" and h(float("nan"), 0.9, 96, False) == "ÖLÇÜLEMEDİ"


def test_karsilastir():
    ix = pd.period_range("2014-01", "2024-06", freq="M"); rng = np.random.default_rng(1)
    ref = pd.Series(rng.normal(0, 0.03, len(ix)), index=ix)
    K = TD.td_karsilastir(ref * 2 + 0.001, ref, False)
    assert K["n"] == 96 and K["ilk"] == "2016-01" and K["son"] == "2023-12"
    assert abs(K["pearson"] - 1) < 1e-12 and abs(K["egim"] - 2) < 1e-9 and K["hukum"] == "DOĞRU" and len(K["ayrisan"]) == 10
    G = TD.td_karsilastir(pd.Series(rng.normal(0, 0.03, len(ix)), index=ix), ref, False)
    assert G["hukum"] == "UYUŞMUYOR" and 0.3 < G["isaret"] < 0.7
    k = TD.td_karsilastir(ref[ix >= pd.Period("2021-06", "M")], ref, True)
    assert k["hukum"] == "ÖLÇÜLEMEDİ"


# ------------------------------------------------------------------ portföy = düz hesap
def _z(n_ay: int = 4, n: int = 60, tohum: int = 3) -> pd.DataFrame:
    rng = np.random.default_rng(tohum); sat = []
    for a in range(n_ay):
        ay = pd.Period("2018-01", "M") + a
        for i in range(n):
            sat.append({"sembol": f"H{i:03d}", "ay": ay, "MOM": rng.normal(), "STREV": rng.normal(), "havuz": bool(rng.random() > 0.1),
                        "Lq": float(rng.lognormal(10, 1)), "r": float(rng.normal(0.01, 0.08)), "r_os": float(rng.normal(0.0, 0.05))})
    Z = pd.DataFrame(sat); Z["tut"] = Z.ay + 1
    return Z


def test_portfoy_duz():
    Z = _z(); m = Z.havuz.to_numpy(bool)
    P = TD.td_portfoy(Z, m, "MOM", "r")
    for ay, g in Z[m].groupby("ay"):
        g = g.sort_values("sembol").copy(); g["pct"] = g.MOM.rank(method="first", pct=True)
        g["o"] = np.clip(np.ceil(g.pct * 10), 1, 10)
        d10, d1 = g[g.o == 10], g[g.o == 1]
        assert abs(P["D10-D1|EW"][ay + 1] - (d10.r.mean() - d1.r.mean())) < 1e-12
        assert abs(P["D10|LQ"][ay + 1] - np.average(d10.r, weights=d10.Lq)) < 1e-12
        med = g.Lq.median(); u = g.pct > 0.7; a = g.pct <= 0.3; b = g.Lq > med
        w = lambda x: np.average(x.r, weights=x.Lq)  # noqa: E731
        f = 0.5 * (w(g[u & ~b]) + w(g[u & b])) - 0.5 * (w(g[a & ~b]) + w(g[a & b]))
        assert abs(P["2X3|LQ"][ay + 1] - f) < 1e-12
        assert abs(P["U30A30|EW"][ay + 1] - (g[u].r.mean() - g[a].r.mean())) < 1e-12
    # sıralama getiriden bağımsız: getiriler değişince onluk üyelikleri (N) değişmez
    Z2 = Z.copy(); Z2["r"] = np.random.default_rng(9).permutation(Z2.r.to_numpy())
    P2 = TD.td_portfoy(Z2, m, "MOM", "r")
    assert P2["N"].equals(P["N"])
    S = TD.td_bizim_seriler(Z.assign(j=0, d=0), "ABD")
    assert abs(S["ABD|havuz|r|STREV|D1-D10|EW"].iloc[0] + TD.td_portfoy(Z, m, "STREV", "r")["D10-D1|EW"].iloc[0]) < 1e-15
    assert "ABD|buyuk|r|MOM|2X3|LQ" in S and "ABD|havuz|r_os|PIYASA|-|EW" in S


# ------------------------------------------------------------------ uçtan uca sentetik + yeniden üretim
def test_uctan_uca_yeniden():
    tmp = tempfile.mkdtemp(prefix="td_test_")
    try:
        H = TOS._ham("ABD", 40, 5)
        pd.to_pickle(H, os.path.join(tmp, "V_ABD.pkl"))
        Vd = OS.os_veri("ABD", tmp)
        Pn = OS.os_panel(Vd)
        Z = TD.td_kesit(Pn, Vd, None)
        # r = tutma ayı son kapanışı / t kapanışı - 1 (bir satır elle)
        r0 = Z[np.isfinite(Z.r)].iloc[123]; d = Vd["V"][r0.sembol]
        son = d[d.index.to_period("M") == r0.tut].Close.iloc[-1]
        assert abs(r0.r - (son / d.loc[r0.tarih, "Close"] - 1)) < 1e-12
        assert (Z.tarih.dt.to_period("M") == Z.ay).all()
        S = TD.td_bizim_seriler(Z, "ABD")
        J = {"seriler": TD._td_seri_json(S), "ref_seriler": {}}
        Y = TD.td_yeniden(J, veri=tmp)
        assert all(x["tutar"] for x in Y["satir"]), Y["satir"]
        E1 = TD.td_e1(Pn)
        assert len(E1) >= 5 and all(np.isfinite(r["gece_ew_bp"]) for r in E1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ e-posta, kapı, sha
def test_eposta_ve_kapi():
    tmp = tempfile.mkdtemp(prefix="td_test_")
    try:
        try:
            TD._td_yaz(os.path.join(tmp, "x.md"), "iletişim: ornek@ornek.com")
        except TD.TDHata as ex:
            assert "e-posta" in str(ex)
        else:
            raise AssertionError("e-posta taraması çalışmadı")
        try:
            TD.td_kapi(onkayit=os.path.join(tmp, "yok.md"))
        except TD.TDHata as ex:
            assert "ön kayıt yok" in str(ex)
        else:
            raise AssertionError("ön kayıtsız kapı açıldı")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    import copy
    assert TD.td_esik_sha() == TD.td_esik_sha(copy.deepcopy(TD.TD_ESIK))
    assert set(TD.TD_KONTROL) == {f"K{i}" for i in range(1, 15)}


if __name__ == "__main__":
    import time as _t
    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    hata = 0
    for ad, f in list(globals().items()):
        if ad.startswith("test_") and callable(f) and getattr(f, "__module__", "") == __name__:
            t0 = _t.time()
            try:
                f(); print(f"GEÇTİ  {ad} ({_t.time() - t0:.1f} sn)")
            except Exception as ex:  # noqa: BLE001
                hata += 1; print(f"KALDI  {ad}: {type(ex).__name__}: {ex}")
                import traceback; traceback.print_exc()
    print("SONUÇ:", "hepsi geçti" if not hata else f"{hata} test kaldı")
    sys.exit(1 if hata else 0)
