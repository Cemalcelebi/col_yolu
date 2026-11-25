"""test_macd_uyum.py — MACD_UYUM sentetik testleri (veri gerekmez).

Kapsam: EMA bit eşitliği (pandas), mu_s10_vektor = yh_s10_bar (birebir), bilinen uyumsuzluk (U1), uyumsuzluk yok (U0), dipte değil (U1b var,
U1 yok), tazelik sınırı (t <= L2 + 20), tekilleştirme (her L2 bir olay, 15 bar aralık), olay taraması = kaba kuvvet referans (yh_s10_bar gün
gün), prefix (veri t'de kesilince aynı olay), hücre hükmü, karar kuralı, SIRA boot, çakışma kapısı.
Çalıştır: python test_macd_uyum.py   (ya da pytest -q test_macd_uyum.py)
"""
from __future__ import annotations

import copy
import os
import sys

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
if KOK not in sys.path:
    sys.path.insert(0, KOK)

import MACD_UYUM as MU  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402


# ---------------------------------------------------------------- yardımcılar
def _df(C: np.ndarray, L: np.ndarray = None, H: np.ndarray = None, bas: str = "2017-01-02") -> pd.DataFrame:
    C = np.asarray(C, float)
    L = C * 0.99 if L is None else np.asarray(L, float)
    H = C * 1.01 if H is None else np.asarray(H, float)
    O = np.r_[C[0], C[:-1]]
    O = np.clip(O, L, H)
    idx = pd.bdate_range(bas, periods=len(C))
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1000.0}, index=idx)


def _rw(n: int, tohum: int, vol: float = 0.025, drift: float = -0.0004) -> pd.DataFrame:
    rng = np.random.default_rng(tohum)
    r = rng.normal(drift, vol, n)
    C = 50 * np.exp(np.cumsum(r))
    sp = np.abs(rng.normal(0, vol / 2, n)) + 0.002
    return _df(C, C * (1 - sp), C * (1 + sp))


def _ref(d: pd.DataFrame, E=MU.MU_ESIK):
    """Kaba kuvvet referans: her gün yh_s10_dipler + yh_s10_bar; dip başına ilk gün; sonra 15 bar aralık."""
    L = d.Low.to_numpy(float); H = d.High.to_numpy(float); C = d.Close.to_numpy(float); n = len(L)
    rsi = MU._mu_rsi(C); Dp = E["dipte"]; taze = E["olay"]["taze_azami"]; ara = E["olay"]["ara"]

    def dipte(k):
        g = Dp["geri"]
        if k - g < 0:
            return False
        return bool(L[k] <= np.min(L[k - g:k]) * (1.0 + Dp["dip_tol"]) and C[k] <= Dp["tepe_pay"] * np.max(H[k - g:k + 1]))
    ham = {h: [] for h in ("U1", "U0", "U1b", "U2")}; gor = {h: set() for h in ham}
    for i in range(n):
        dip = YH.yh_s10_dipler(L, i)
        if not dip:
            continue
        L2 = dip[-1]
        if i - L2 > taze:
            continue
        b = YH.yh_s10_bar(L, C, i)
        onceki = [k for k in dip if k <= L2 - 8]
        L1 = onceki[-1] if onceki else -1
        dp = dipte(L2)
        kos = {"U1": b["S10"] == 1 and b["F68"] == 1 and dp,
               "U0": b["s65"] == 1 and b["s66"] == 0 and b["F68"] == 1 and dp,
               "U1b": b["S10"] == 1 and b["F68"] == 1,
               "U2": i == L2 + 6 and b["s65"] == 1 and L1 >= 0 and rsi[L1] < 30 and rsi[L2] > rsi[L1] and dp}
        for h, v in kos.items():
            if v and L2 not in gor[h]:
                ham[h].append((i, L2, L1)); gor[h].add(L2)
    out = {}
    for h, ev in ham.items():
        ev = sorted(ev); tut = []; son = -10 ** 9
        for e in ev:
            if e[0] - son >= ara:
                tut.append(e); son = e[0]
        out[h] = tut
    return out


def _mu_set(O: pd.DataFrame, h: str):
    g = O[O.hipotez == h]
    return sorted(zip(g.i.astype(int), g.L2.astype(int), g.L1.astype(int)))


def _uyumsuz(dipte_bozuk: bool = False) -> pd.DataFrame:
    """Bilinen pozitif uyumsuzluk: uzun düşüş, sert dip L1, tepki, yavaş ikinci dip L2 (daha aşağı), sonra yükseliş."""
    c = list(np.linspace(100, 62, 150))                      # 0-149 düşüş
    c += list(np.linspace(62, 50, 20)[1:])                   # 150-168 sert dip -> L1 ~ 168
    c += list(np.linspace(50, 58, 15)[1:])                   # tepki
    c += list(np.linspace(58, 49.8, 25)[1:])                 # yavaş ikinci dip (L2 daha aşağı)
    c += list(np.linspace(49.8, 60, 40)[1:])                 # yükseliş
    C = np.array(c, float)
    L = C * 0.99; H = C * 1.01
    if dipte_bozuk:
        k = int(np.argmin(C[180:])) + 180
        L = L.copy(); L[k - 100] = L[k] * 0.5                 # 120 bar içinde çok daha derin tek iğne (yalnız Low; dip penceresi dışında)
    return _df(C, L, H)


def _uyumsuzluk_yok() -> pd.DataFrame:
    """Dipte çift dip ama MACD ikinci dipte daha aşağı: yatay bölge (sığ L1), sonra sert çöküşle biraz daha aşağı L2, sonra yükseliş."""
    c = list(np.linspace(100, 60, 150))
    c += list(60 + 1.0 * np.sin(np.linspace(0, 3 * np.pi, 30)))
    c += list(np.linspace(c[-1], 62, 8)[1:])
    c += list(np.linspace(62, 58.5, 6)[1:])
    c += list(np.linspace(58.5, 66, 40)[1:])
    C = np.array(c, float)
    return _df(C)


# ---------------------------------------------------------------- testler
def test_ema_bit_esit():
    rng = np.random.default_rng(3)
    for _ in range(100):
        n = int(rng.integers(2, 260)); c = np.cumprod(1 + rng.normal(0, 0.03, n)) * 10
        for sp in (12, 26, 9):
            p = pd.Series(c).ewm(span=sp, adjust=False).mean().to_numpy()
            assert np.array_equal(p, MU.mu_ema(c[None, :], sp)[0])


def test_s10_vektor_yh_esit():
    bad = 0; tot = 0; s10 = 0
    for t in range(12):
        d = _rw(700, 100 + t); L = d.Low.to_numpy(float); C = d.Close.to_numpy(float)
        I = np.r_[np.arange(0, 80), np.random.default_rng(t).integers(0, len(d), 120)]
        v = MU.mu_s10_vektor(L, C, I)
        for q, i in enumerate(I):
            a = YH.yh_s10_bar(L, C, int(i))
            av = np.array([a[k] for k in YH._YH_S10_OZ]); vv = np.array([v[k][q] for k in YH._YH_S10_OZ])
            tot += 1; s10 += a["S10"] == 1
            bad += not np.array_equal(av, vv, equal_nan=True)
    assert bad == 0 and tot > 2000 and s10 > 10, (bad, tot, s10)


def test_tarama_referansla_ayni():
    top = {h: 0 for h in ("U1", "U0", "U1b", "U2")}
    for t in range(10):
        d = YH._yh_hazir(_rw(900, 200 + t, vol=0.03, drift=-0.0008))
        O, _ = MU.mu_hisse(d)
        R = _ref(d)
        for h in R:
            assert _mu_set(O, h) == sorted(R[h]), (t, h, _mu_set(O, h)[:5], sorted(R[h])[:5])
            top[h] += len(R[h])
    assert top["U1b"] > 5 and top["U0"] > 5, top


def test_bilinen_uyumsuzluk_U1():
    d = YH._yh_hazir(_uyumsuz())
    O, _ = MU.mu_hisse(d); R = _ref(d)
    assert len(R["U1"]) >= 1, R
    assert _mu_set(O, "U1") == sorted(R["U1"])
    e = O[O.hipotez == "U1"].iloc[0]
    assert e.S10 == 1 and e.F68 == 1 and e.dipte and e.F66 > 0 and e.F66m < 0 and e.F65 <= 0.01
    assert 6 <= e.tL2 <= 20
    assert abs(e.stop0 - e.low_L2 * 0.98) < 1e-12
    assert len(O[O.hipotez == "U0"]) == 0 or set(O[O.hipotez == "U0"].L2) != set(O[O.hipotez == "U1"].L2)


def test_uyumsuzluk_yok_U0():
    d = YH._yh_hazir(_uyumsuzluk_yok())
    O, _ = MU.mu_hisse(d); R = _ref(d)
    assert len(R["U0"]) >= 1, R
    assert _mu_set(O, "U0") == sorted(R["U0"]) and _mu_set(O, "U1") == sorted(R["U1"])
    e = O[O.hipotez == "U0"].iloc[-1]
    assert e.s65 == 1 and e.s66 == 0 and e.F68 == 1 and e.dipte and e.F66 <= 0
    assert int(e.L2) not in set(O[O.hipotez == "U1"].L2.astype(int))          # aynı ikinci dipte MACD uyumsuzluğu yok -> U1 yok


def test_dipte_degil():
    d = YH._yh_hazir(_uyumsuz(dipte_bozuk=True))
    O, _ = MU.mu_hisse(d)
    assert len(O[O.hipotez == "U1b"]) >= 1
    assert len(O[O.hipotez == "U1"]) == 0 and len(O[O.hipotez == "U0"]) == 0
    assert not O[O.hipotez == "U1b"].dipte.any()


def test_tazelik_siniri():
    d = YH._yh_hazir(_uyumsuz())
    O, _ = MU.mu_hisse(d)
    e = O[O.hipotez == "U1"].iloc[0]; x = int(e.tL2)
    E = copy.deepcopy(MU.MU_ESIK); E["olay"]["taze_azami"] = x - 1
    O2, _ = MU.mu_hisse(d, E=E)
    assert int(e.L2) not in set(O2[(O2.hipotez == "U1")].L2.astype(int))
    assert _mu_set(O2, "U1") == sorted(_ref(d, E)["U1"])
    E["olay"]["taze_azami"] = 20
    assert (O[O.hipotez == "U1"].tL2 <= 20).all() and (O[O.hipotez == "U1"].tL2 >= 6).all()


def test_tekillestirme():
    E0 = copy.deepcopy(MU.MU_ESIK); E0["olay"]["ara"] = 0
    sinandi = 0
    for t in range(8):
        d = YH._yh_hazir(_rw(900, 300 + t, vol=0.03, drift=-0.0008))
        O, _ = MU.mu_hisse(d); O0, _ = MU.mu_hisse(d, E=E0)
        for h in ("U1", "U0", "U1b", "U2"):
            g = O[O.hipotez == h].sort_values("i"); g0 = O0[O0.hipotez == h].sort_values("i")
            assert not g.L2.duplicated().any() and not g0.L2.duplicated().any()      # her L2 en çok bir olay
            if len(g) > 1:
                assert (np.diff(g.i.to_numpy()) >= 15).all()
            tut, son = [], -10 ** 9
            for i in g0.i.to_numpy():
                if i - son >= 15:
                    tut.append(i); son = i
            assert list(g.i) == tut
            sinandi += int(len(g0) > len(g))
    assert sinandi >= 1


def test_prefix_kesik():
    d = YH._yh_hazir(_rw(900, 401, vol=0.03, drift=-0.0008))
    O, _ = MU.mu_hisse(d)
    assert len(O)
    for r in O.itertuples():
        kes = d[d.index <= r.tarih]
        Ok, _ = MU.mu_hisse(kes)
        e = Ok[(Ok.hipotez == r.hipotez) & (Ok.tarih == r.tarih)]
        assert len(e) == 1 and int(e.iloc[0].L2) == r.L2 and int(e.iloc[0].L1) == r.L1 and e.iloc[0].S10 == r.S10


def test_prefix_seri_basi():
    """Seri başına yakın olay (t = 60 .. 70): kesik seri kısa olsa da olay aynı çıkmalı (v1.0 hatası: n < 70 erken dönüş)."""
    bulundu = 0
    for t in range(40):
        d = YH._yh_hazir(_rw(300, 500 + t, vol=0.04, drift=-0.002))
        O, _ = MU.mu_hisse(d)
        for r in O[O.i <= 75].itertuples():
            Ok, _ = MU.mu_hisse(d.iloc[:r.i + 1])
            e = Ok[(Ok.hipotez == r.hipotez) & (Ok.tarih == r.tarih)]
            assert len(e) == 1 and int(e.iloc[0].L2) == r.L2, (t, r.hipotez, r.i)
            bulundu += 1
    assert bulundu >= 1


def test_hukum():
    c = {"n": 500, "guc": 0.9, "fark": 0.01, "boot_alt": 0.002, "sira": 0.55, "sira_alt": 0.52, "l3o": 0.004, "plasebo_gecti": True}
    assert MU.mu_hukum(c)[0] == "TUTAR"
    assert MU.mu_hukum({**c, "n": 20})[0] == "ÖLÇÜLEMEDİ"
    assert MU.mu_hukum({**c, "guc": 0.5})[0] == "ÖLÇÜLEMEDİ"
    assert MU.mu_hukum({**c, "sira_alt": 0.49})[0] == "TUTMADI"
    assert MU.mu_hukum({**c, "plasebo_gecti": False})[0] == "TUTMADI"
    assert MU.mu_hukum({**c, "boot_alt": -0.001})[0] == "TUTMADI"


def test_karar():
    T = {"hukum": "TUTAR", "n": 400, "guc": 0.9, "fark": 0.02, "boot_alt": 0.005, "boot_ust": 0.03}
    Y = {"hukum": "TUTMADI", "n": 400, "guc": 0.9, "fark": 0.0, "boot_alt": -0.01, "boot_ust": 0.01}
    O_ = {"hukum": "ÖLÇÜLEMEDİ", "n": 40, "guc": 0.3, "fark": 0.01, "boot_alt": -0.02, "boot_ust": 0.04}
    hk = [f"{p}|{h}" for p in MU.MU_KARAR_PAZAR for h in MU.MU_DONEM]
    u0 = {k: {"n": 300, "fark": 0.0} for k in hk}
    assert MU.mu_karar({k: T for k in hk}, u0)["karar"] == "AÇIK VERİDE TUTTU"
    assert MU.mu_karar({k: T for k in hk}, {k: {"n": 300, "fark": 0.05} for k in hk})["karar"] == "TUTMADI"
    assert MU.mu_karar({**{k: T for k in hk}, hk[0]: Y}, u0)["karar"] == "TUTMADI"
    assert MU.mu_karar({**{k: O_ for k in hk}}, u0)["karar"] == "ÖLÇÜLEMEDİ"
    assert MU.mu_karar({**{k: T for k in hk}, hk[1]: O_}, u0)["karar"] == "ÖLÇÜLEMEDİ"
    N = {"hukum": "TUTMADI", "n": 400, "guc": 0.9, "fark": -0.02, "boot_alt": -0.03, "boot_ust": -0.005}
    assert MU.mu_karar({**{k: T for k in hk}, hk[2]: N}, u0)["karar"] == "ÇELİŞKİLİ"


def test_sira_boot():
    rng = np.random.default_rng(1)
    s = rng.uniform(0.4, 0.9, 300); ay = np.repeat([f"2018-{m:02d}" for m in range(1, 13)], 25)
    a, b = MU.mu_sira_boot(s, ay, 0)
    assert a < s.mean() < b and np.isfinite(a)
    assert MU.mu_sira_boot(s, ay, 0) == (a, b)


def test_dip_tanimi():
    L = np.array([5, 4, 3, 2, 1.5, 1, 1, 2, 3, 4, 5, 6, 7], float)    # eşit dizide ilk bar dip (sol katı, sağ eşit izinli)
    isd = MU.mu_dip(L)
    assert isd[5] and not isd[6]


def test_esik_sha_sabit():
    assert MU.mu_esik_sha() == MU.mu_esik_sha(copy.deepcopy(MU.MU_ESIK))
    E = copy.deepcopy(MU.MU_ESIK); E["dipte"]["tepe_pay"] = 0.79
    assert MU.mu_esik_sha(E) != MU.mu_esik_sha()


def _sentetik_pazar(n_hisse: int, tohum: int, ucuz: bool = False):
    """2015-06-01 .. 2022-12-30 iş günleri; rastgele yürüyüş + ara sıra derin düşüşler (dip olayları); hacim kademeli."""
    rng = np.random.default_rng(tohum)
    idx = pd.bdate_range("2015-06-01", "2022-12-30"); n = len(idx); V = {}
    for k in range(n_hisse):
        r = rng.normal(0.0002, 0.022 + 0.01 * (k % 4), n)
        for _ in range(6):
            a = int(rng.integers(150, n - 80)); r[a:a + 40] -= 0.012
        p0 = (2.0 + 2.5 * (k % 3)) if (ucuz and k % 2 == 0) else (20 + 5 * (k % 7))
        C = p0 * np.exp(np.cumsum(r)); sp = np.abs(rng.normal(0, 0.01, n)) + 0.004
        H = C * (1 + sp); L = C * (1 - sp); O = np.clip(np.r_[C[0], C[:-1]] * (1 + rng.normal(0, 0.003, n)), L, H)
        V[f"S{k:03d}"] = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1e5 * (1 + k % 9) * rng.uniform(0.5, 1.5, n)},
                                      index=idx)
    return V


def test_uctan_uca_sentetik(tmp_dir: str = None):
    """Sentetik üç pazar: tarama -> huni -> güç -> ölçüm (R15 + plasebo + R30 + ikincil) -> satır dosyası -> yeniden üretim -> rapor."""
    import json
    import shutil
    import tempfile
    import CETVEL2 as C2
    kok = tmp_dir or tempfile.mkdtemp(prefix="mu_test_")
    veri = os.path.join(kok, "veri"); kasa = os.path.join(kok, "kasa"); cikti = os.path.join(kok, "cikti")
    os.makedirs(veri); os.makedirs(os.path.join(kasa, "acik")); os.makedirs(cikti)
    for i, p in enumerate(MU.MU_PAZAR):
        pd.to_pickle(_sentetik_pazar(70, 900 + i, ucuz=(p == "ABD")), os.path.join(veri, f"V_{p}.pkl"))
    json.dump({"acik_kesik": "2022-12-31", "acilan": [], "muhur_id": "sentetik"}, open(os.path.join(kasa, "acik", "KASA_DURUM.json"), "w"))
    eski = dict(MU.MU_YOL); C2._C2_PN22.clear()
    try:
        MU.MU_YOL["kasa"] = kasa
        K = MU.mu_kasa(veri)
        assert K["kesik"] == "2022-12-31"
        Os, H = [], {}
        for pi, p in enumerate(MU.MU_PAZAR):
            Pb = C2.c2_panel22_al(p, veri, None)
            O, h = MU.mu_pazar(p, veri, Pb["Vd"])
            e = MU.mu_esitlik(Pb["Vd"], O, p, pi)
            assert e["esit"] == e["n"] >= 150
            H[p] = {**h, "c2": MU.mu_c2_huni(O, p, veri)}
            Os.append(O)
        O = pd.concat(Os, ignore_index=True)
        assert (O.hipotez == "U1").sum() > 20 and (O.hipotez == "U0").sum() > 20, O.hipotez.value_counts()
        T = MU.mu_huni_tablo(O, H); G = MU.mu_guc_beklenti(T)
        assert len(T) and len(G) == len(MU.MU_HIP) * 3 * 2
        J = MU.mu_olc_hepsi(O, veri, cikti, {"onkayit": "sentetik", "kasa": K}, MU._mu_simdi())
        assert os.path.exists(os.path.join(cikti, "sonuc.json")) and os.path.exists(os.path.join(cikti, "UYUM_RAPOR.md"))
        assert all(v["tuttu"] for v in J["yeniden"].values())
        assert all(v["tuttu"] == v["n"] for v in J["prefix"].values())
        assert J["karar"]["karar"] in ("AÇIK VERİDE TUTTU", "TUTMADI", "ÖLÇÜLEMEDİ", "ÇELİŞKİLİ")
        X = pd.read_csv(os.path.join(cikti, "uyum_satir.csv.gz"))
        for k in ("pazar", "sembol", "tarih", "giris", "stop0", "h5", "h10", "stop_oldu", "r15", "es_r15"):
            assert k in X.columns, k
        assert pd.to_datetime(X.tarih).max() <= pd.Timestamp("2022-12-31")
        assert (X.stop0 > 0).all()
    finally:
        MU.MU_YOL.clear(); MU.MU_YOL.update(eski); C2._C2_PN22.clear()
        if tmp_dir is None:
            shutil.rmtree(kok, ignore_errors=True)


def test_cakisma_kapisi():
    kaynak = open(os.path.join(KOK, "MACD_UYUM.py"), encoding="utf-8").read()
    ns = {"__name__": "mu_test"}
    exec(compile(kaynak, "MACD_UYUM.py", "exec"), ns)
    exec(compile(kaynak, "MACD_UYUM.py", "exec"), ns)          # aynı dosya yeniden: geçer
    ns2 = {"__name__": "mu_test", "mu_dip": "başka modülün adı", "_CK_KAYIT": {"mu_dip": "BASKA.py"}}
    try:
        exec(compile(kaynak, "MACD_UYUM.py", "exec"), ns2)
    except RuntimeError as ex:
        assert "EZDİ" in str(ex)
    else:
        raise AssertionError("çakışma kapısı durmadı")


if __name__ == "__main__":
    testler = [(k, v) for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    ok = 0
    for ad, f in testler:
        try:
            f(); ok += 1; print(f"GEÇTİ  {ad}")
        except Exception as ex:   # rapor için yakala, sonda çıkış kodu
            print(f"KALDI  {ad}: {type(ex).__name__}: {ex}")
    print(f"{ok} / {len(testler)} test geçti")
    sys.exit(0 if ok == len(testler) else 1)
