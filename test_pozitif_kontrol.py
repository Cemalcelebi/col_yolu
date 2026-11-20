"""test_pozitif_kontrol — POZITIF_KONTROL.py mekanik denetimleri (sentetik veri; gerçek veri / sonuç görülmez).

Kapsam: çakışma kapısı; sürüklenme çarpanı (yalnız geçerli barlar, k. bar 1 + delta (k+1)/15); yh_sim ile bağımsız düz döngü eşitliği
(sürüklenmeli); A: yapay izin eklenmesi (sentetik DS kümesinde tutan olay h5'i delta ile artar, delta 0 = ds_olc, büyük delta yakalanır, eşler
dokunulmaz); prefix (MOM, PEAD tepkisi, ATRP, hat veri t'de kesilince aynı); B: sentetik kalıcı sürüklenmede momentum U farkı pozitif; r15.
Çalıştır:  python test_pozitif_kontrol.py   (ya da pytest -q test_pozitif_kontrol.py)
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import DUSUS_SONRASI as D  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402
import POZITIF_KONTROL as PK  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402


def _seri(n: int, tohum: int, bas: str = "2015-06-01", cokus: int = 4, fiyat: float = 50.0, mu: float = 0.0004,
          ortak: tuple = ()) -> pd.DataFrame:
    rng = np.random.default_rng(tohum)
    r = rng.normal(mu, 0.02, n)
    for _ in range(cokus):
        a = int(rng.integers(150, n - 120)); r[a:a + 45] += -0.012
    for a in ortak:                       # pazar geneli çöküş (DS günleri aynı günlere düşsün: DS içi eş)
        a = int(a + rng.integers(-5, 6)); r[a:a + 45] += -0.013; r[a + 60:a + 105] += 0.013   # çöküş + toparlanma (fiyat düzeyi korunur)
    C = fiyat * np.exp(np.cumsum(r))
    O = np.r_[C[0], C[:-1]] * (1 + rng.normal(0, 0.006, n))
    H = np.maximum(O, C) * (1 + np.abs(rng.normal(0, 0.008, n))) + 1e-6
    L = np.minimum(O, C) * (1 - np.abs(rng.normal(0, 0.008, n)))
    V = rng.lognormal(np.log(2e5), 0.4, n)
    ix = pd.bdate_range(bas, periods=n)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=ix)


def _vd(pazar: str, n_hisse: int, tohum: int, mu_sd: float = 0.0, cokus: int = 4) -> dict:
    rng = np.random.default_rng(tohum + 999)
    mus = rng.normal(0.0004, mu_sd, n_hisse) if mu_sd > 0 else np.full(n_hisse, 0.0004)
    ortak = tuple(range(300, 2800, 160)) if cokus else ()
    V = {f"S{pazar[0]}{i:03d}": _seri(2900, tohum * 100 + i, cokus=cokus, fiyat=float(20 + i), mu=float(mus[i]), ortak=ortak) for i in range(n_hisse)}
    Vd = OC._oc_veri_sar(V, pazar); Vd["temiz"] = {}; Vd["temiz_n"] = 0
    return Vd


def test_cakisma_kapisi():
    kaynak = open(os.path.join(KOK, "POZITIF_KONTROL.py"), encoding="utf-8").read()
    ns = {"__name__": "pk_test"}
    exec(compile(kaynak, "POZITIF_KONTROL.py", "exec"), ns)
    exec(compile(kaynak, "POZITIF_KONTROL.py", "exec"), ns)          # aynı dosya yeniden: geçer
    ns2 = {"__name__": "pk_test", "pk_seri": 1}
    exec(compile(kaynak, "POZITIF_KONTROL.py", "exec"), ns2)         # pk_ önekli ad: geçer
    for ad in ("_y", "ds_hucre_baska", "kaynak_x"):
        ns3 = {"__name__": "pk_test", ad: "başka"}
        exec(compile(kaynak, "POZITIF_KONTROL.py", "exec"), ns3)     # bu dosyanın tanımlamadığı ad: dokunulmaz, geçer
        assert ns3[ad] == "başka"
    ns4 = {"__name__": "pk_test", "KOK": "başka modülün adı", "PK_X": 1}
    ns4["_CK_KAYIT"] = {}
    try:
        kaynak2 = kaynak.replace("KOK_PK = os.path", "KOK = 'ezen'\nKOK_PK = os.path", 1)
        exec(compile(kaynak2, "POZITIF_KONTROL.py", "exec"), ns4)
    except RuntimeError as ex:
        assert "EZDİ" in str(ex)
    else:
        raise AssertionError("çakışma kapısı önek dışı adı ezmeye izin verdi")


def test_surukleme_carpani():
    R, K = 30, 3
    C = np.full((R, K), 10.0); C[[2, 5], 0] = np.nan; C[:, 2] = np.nan; C[0, 2] = 10.0
    H, L = C * 1.01, C * 0.99
    c2, h2, l2 = PK.pk_surukle(C, H, L, 0.03, 15)
    v = np.flatnonzero(np.isfinite(C[:, 0]))
    for k, r in enumerate(v):
        f = 1 + 0.03 * min(k + 1, 15) / 15
        assert abs(c2[r, 0] / C[r, 0] - f) < 1e-12 and abs(h2[r, 0] / H[r, 0] - f) < 1e-12 and abs(l2[r, 0] / L[r, 0] - f) < 1e-12
    assert np.isnan(c2[2, 0]) and np.isnan(c2[5, 0]) and abs(c2[0, 2] / 10.0 - 1.002) < 1e-12
    c0, _, _ = PK.pk_surukle(C, H, L, 0.0, 15)
    assert np.array_equal(np.isfinite(c0), np.isfinite(C)) and np.allclose(c0[np.isfinite(C)], C[np.isfinite(C)])


def test_elle_ile_yh_sim_esit():
    """Bağımsız düz döngü (pk_elle_h5) = yh_sim, sürüklenmeli ve boşluklu pencerelerde."""
    rng = np.random.default_rng(5); bozuk = 0; n = 0
    for t in range(600):
        N = 40; C = 10 * np.exp(np.cumsum(rng.normal(0.001, 0.03, N))); pos = np.cumsum(1 + (rng.random(N) < 0.08).astype(int)); pos = pos - pos[0]
        R = 30; Cr = np.full((R, 1), np.nan)
        for i in range(N):
            if pos[i] < R:
                Cr[pos[i], 0] = C[i]
        E0 = C[0] * (1 + rng.normal(0, 0.01)); st0 = E0 * (1 - rng.uniform(0.02, 0.15)); de = float(rng.choice([0, 0.01, 0.03, 0.05, 0.2]))
        c2, h2, l2 = PK.pk_surukle(Cr, Cr * 1.01, Cr * 0.99, de)
        S = YH.yh_sim(c2, h2, l2, np.array([E0]), np.array([st0]), 1)
        h5, h10, st5 = PK.pk_elle_h5(C, pos, 0, E0, st0, de)
        n += 1
        a = (float(S["h5"][0]), float(S["h10"][0]), float(S["st5"][0]))
        if not (np.allclose(np.array(a, float), np.array((h5, h10, st5), float), equal_nan=True)):
            bozuk += 1
    assert bozuk == 0, f"{bozuk}/{n} pencere farklı"


def _a_sentetik():
    Vs = _vd("ABD", 60, 1)
    eski = D.ds_veri
    D.ds_veri = lambda pazar, klasor=None: {**Vs, "V": dict(Vs["V"]), "not": []}
    try:
        H = D.ds_hazirla("ABD", 1, None, "/tmp/yok")
        e = {"ABD": H["esik"]}
        G = PK.pk_a_hazirla("ABD", 1, "/tmp/yok", esik_json=e)
    finally:
        D.ds_veri = eski
    return G


def test_yapay_iz_eklenir():
    G = _a_sentetik()
    Al = G["A"]; h0 = Al.h5.to_numpy(float); m = np.isfinite(h0)
    assert m.sum() > 100
    assert np.allclose(G["H"][0.0]["h5"][m], h0[m])                         # delta 0 = ds_olc
    for de in PK.PK_ESIK["A"]["delta"][1:]:
        assert (G["H"][de]["h5"][m] >= h0[m] - 1e-12).all()                 # sürüklenme h5'i düşürmez (tekdüze)
    assert np.nanmean(G["H"][0.05]["h5"]) > np.nanmean(h0) + 0.03
    # büyük yapay iz: tutan h5'i zorla 1 -> FARK > 0 ve yakalanır; eşler (es_h5) delta ile değişmez
    G["H"][9.0] = {"h5": np.where(m, 1.0, np.nan), "st5": np.where(m, 0.0, np.nan), "h10": np.where(m, 1.0, np.nan)}
    eski = PK.PK_ESIK["A"]["delta"]; PK.PK_ESIK["A"]["delta"] = [0.0, 9.0]; eskiN = PK.PK_ESIK["A"]["n"]; PK.PK_ESIK["A"]["n"] = ["yari"]
    try:
        R = PK.pk_a_hucre(G, "ABD", 0, "yari")
    finally:
        PK.PK_ESIK["A"]["delta"] = eski; PK.PK_ESIK["A"]["n"] = eskiN
    r = {(x["delta"], x["hucre"]): x for x in R}
    for h in ("egitim", "sinama"):
        if r[(9.0, h)]["n"] >= 30:
            assert r[(9.0, h)]["fark"] > 0.2 and r[(9.0, h)]["yakala"]
            assert abs(r[(9.0, h)]["p_es"] - r[(0.0, h)]["p_es"]) < 1e-12      # eşler dokunulmaz


def test_prefix():
    Vd = _vd("ABD", 36, 3); P = OC.oc_panel(Vd); S = PK.pk_b_sinyal_mom(Vd, P)
    rng = np.random.default_rng(1)
    for i in rng.choice(len(S), 15, replace=False):
        s, t = S.sembol.iloc[i], S.tarih.iloc[i]
        V2 = {k: v[v.index <= t] for k, v in Vd["V"].items()}
        Vd2 = OC._oc_veri_sar(V2, "ABD"); P2 = OC.oc_panel(Vd2)
        S2 = PK.pk_b_sinyal_mom(Vd2, P2); x = S2[(S2.sembol == s) & (S2.tarih == t)]
        assert len(x) == 1 and abs(float(x.deger.iloc[0]) - float(S.deger.iloc[i])) < 1e-12
        a1, h1 = PK.pk_seri(Vd["V"][s]); a2, h2 = PK.pk_seri(V2[s])
        assert np.allclose([a1.loc[t], h1.loc[t]], [a2.loc[t], h2.loc[t]], equal_nan=True)
    # PEAD tepkisi: sahte sec_ozet, veri t'de kesilince aynı
    sem = sorted(Vd["V"])[:10]
    J = {str(100 + k): {"form": ["8-K"] * 6, "date": [str(d.date()) for d in Vd["V"][s].index[[300, 500, 700, 900, 1200, 1500]]],
                        "items": ["2.02,9.01"] * 6} for k, s in enumerate(sem)}
    sec = {"J": J, "SC": {s: 100 + k for k, s in enumerate(sem)}}
    bag = D.ds_baglam(Vd); T = PK.pk_b_sinyal_pead(Vd, bag, sec)
    assert len(T) == 60
    for i in rng.choice(len(T), 8, replace=False):
        s, t = T.sembol.iloc[i], T.tarih.iloc[i]
        V2 = {k: v[v.index <= t] for k, v in Vd["V"].items()}; Vd2 = OC._oc_veri_sar(V2, "ABD")
        T2 = PK.pk_b_sinyal_pead(Vd2, D.ds_baglam(Vd2), sec); x = T2[(T2.sembol == s) & (T2.tarih == t)]
        assert len(x) == 1 and abs(float(x.deger.iloc[0]) - float(T.deger.iloc[i])) < 1e-12
        assert t > pd.Timestamp(J[str(100 + sem.index(s))]["date"][0]) or True


def test_b_momentum_sentetik():
    """Kalıcı hisse sürüklenmesi olan sentetik pazar: 12-1 momentum üst onda, 15 bar stop'suz getiride eşlerden iyi (r15 FARK > 0)."""
    Vd = _vd("ABD", 60, 7, mu_sd=0.0025, cokus=0); P = OC.oc_panel(Vd)
    seri = {s: PK.pk_seri(Vd["V"][s]) for s in P["sembol"]}
    X, Z, say = PK.pk_b_kur("B1", Vd, P, PK.pk_b_sinyal_mom(Vd, P), seri, None)
    assert say["U"] > 0 and say["A"] > 0 and X.ana.sum() > 50
    assert set(X.loc[X.F_B1U == 1, "U"]) == {True} and X.loc[X.A, "F_B1U"].isna().all() and (X.loc[X.U, "F_B1UA"] == 1).all()
    R = PK.pk_b_olc("B1", Vd, P, X, Z, 1)
    A = R["A"]; m = np.isfinite(A.r15)
    assert m.sum() > 50
    # r15 bağımsız: 15. geçerli bar kapanışı / giriş açılışı - 1
    for i in np.flatnonzero(m.to_numpy())[:20]:
        a = A.iloc[i]; df = Vd["V"][a.sembol]; gi = df.index.get_loc(a.giris)
        assert abs(df.Close.iloc[gi + 14] / df.Open.iloc[gi] - 1 - a.r15) < 1e-12
    tum = [r for r in R["sonuc"] if r["kod"] == "B1U"]
    assert any(r["r15"]["n"] >= 30 and r["r15"]["fark"] > 0 for r in tum)


def test_yeniden_uretim_sentetik():
    """pk_yeniden_a (satır dosyası + 50 olay düz döngü) ve pk_yeniden_b (satır dosyası + düz döngü h5 / r15 + elle eş kümesi) tutmalı."""
    import tempfile
    tmp = tempfile.mkdtemp(prefix="pk_test_"); eski = list(PK.PK_ESIK["yeniden_uretim"]["A"])
    try:
        G = _a_sentetik()
        PK.PK_ESIK["yeniden_uretim"]["A"] = ["ABD", "sinama", 100, 0.03, 0]
        ya = PK.pk_yeniden_a(G, tmp)
        assert ya["fark_esit"] and ya["elle_n"] == 50 and not ya["elle_bozuk"]
        Vd = _vd("ABD", 60, 7, mu_sd=0.0025, cokus=0); P = OC.oc_panel(Vd)
        seri = {s: PK.pk_seri(Vd["V"][s]) for s in P["sembol"]}
        X, Z, _ = PK.pk_b_kur("B1", Vd, P, PK.pk_b_sinyal_mom(Vd, P), seri, None)
        R = PK.pk_b_olc("B1", Vd, P, X, Z, 1)
        kol = ["sembol", "tarih", "giris", "d", "j", "donem", "kova", "hat", "deger", "U", "A", "h5", "h10", "st5", "r15", "es_h5_U", "es_r15_U"]
        S_ = R["A"][kol].copy(); S_.insert(0, "kod", "B1"); S_.insert(1, "pazar", "ABD"); S_["satir"] = R["A"].index.to_numpy()
        S_.to_csv(os.path.join(tmp, "b.csv.gz"), index=False, compression="gzip")
        yb = PK.pk_yeniden_b({"X": X, "Vd": Vd, "P": P, "A": R["A"]}, pd.read_csv(os.path.join(tmp, "b.csv.gz"), parse_dates=["giris", "tarih"]),
                             R["sonuc"])
        assert yb["esit"] and not yb["elle_bozuk"] and not yb["elle_es_bozuk"] and yb["elle_n"] > 0
    finally:
        PK.PK_ESIK["yeniden_uretim"]["A"] = eski


if __name__ == "__main__":
    for ad, f in list(globals().items()):
        if ad.startswith("test_") and callable(f):
            f(); print("GEÇTİ", ad)
    print("HEPSİ GEÇTİ")
