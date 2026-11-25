"""test_macd_uyum_es.py — MACD_UYUM_ES sentetik testleri (veri gerekmez).

Kapsam: K20 / K1 / KG bayrakları yalnız geçmiş barlardan; ham durumdan olay üretimi = MU.mu_hisse (U1); ham durum veri kesilince aynı (K2);
dışlamalı eş aritmetiği (c2_es + ek dışlama) = kaba kuvvet; kirli sayısı = kaba kuvvet; C (kirli - temiz) = kaba kuvvet; çakışma kapısı.
Çalıştır: python test_macd_uyum_es.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
if KOK not in sys.path:
    sys.path.insert(0, KOK)

import CETVEL2 as C2  # noqa: E402
import MACD_UYUM as MU  # noqa: E402
import MACD_UYUM_ES as ES  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402
from test_macd_uyum import _rw, _uyumsuz  # noqa: E402


def test_bayrak_yalniz_gecmis():
    t = pd.bdate_range("2020-01-01", periods=100).values
    u1 = np.zeros(100, bool); u1[50] = True; sb = np.zeros(100, bool); sb[30] = True
    B = ES.es_bayrak_seri(t, u1, sb, t, 20)
    assert not B["K1"][50] and not B["K20"][50], "olay günü kendi bayrağını görmemeli (yalnız b-1 ve öncesi)"
    assert B["K1"][51] and not B["K1"][52]
    assert B["K20"][51] and B["K20"][70] and not B["K20"][71] and not B["K20"][49]
    assert B["KG"][31] and B["KG"][50] and not B["KG"][51] and not B["KG"][30]
    # panel günü hissenin barı olmayan gün: b = tarih < gün sayısı
    g = np.array([t[50] + np.timedelta64(12, "h")])
    assert ES.es_bayrak_seri(t, u1, sb, g, 20)["K1"][0]


def test_bayrak_gelecek_degismez():
    t = pd.bdate_range("2020-01-01", periods=100).values
    rng = np.random.default_rng(3)
    u1 = rng.random(100) < 0.1; sb = u1 | (rng.random(100) < 0.1)
    B = ES.es_bayrak_seri(t, u1, sb, t, 20)
    for k in range(10, 100, 7):
        u2 = u1.copy(); u2[k:] = ~u2[k:]; s2 = sb.copy(); s2[k:] = ~s2[k:]
        B2 = ES.es_bayrak_seri(t, u2, s2, t, 20)
        for f in ES.ES_BAYRAK:
            assert np.array_equal(B[f][:k + 1], B2[f][:k + 1]), f"{f}: gün {k} gelecekteki bara bağlı"


def _seriler():
    out = [YH._yh_hazir(_uyumsuz())]
    for s in range(6):
        out.append(YH._yh_hazir(_rw(900, 40 + s, vol=0.03, drift=-0.0006)))
    return out


def test_ham_olay_mu_hisse_ile_ayni():
    top = 0
    for d in _seriler():
        H = ES.es_ham(d)
        O, _ = MU.mu_hisse(d)
        ref = sorted(O[O.hipotez == "U1"].i.astype(int).tolist())
        assert sorted(H["olay_u1"].tolist()) == ref, (H["olay_u1"][:5], ref[:5])
        assert H["u1"][ref].all() if ref else True
        assert not (H["u1"] & ~H["s10f68"]).any(), "ham U1 ⊂ ham S10F68 olmalı"
        refb = O[O.hipotez == "U1b"].i.astype(int).tolist()
        assert H["s10f68"][refb].all() if refb else True
        top += len(ref)
    assert top >= 1, "sentetikte en az bir U1 olayı beklenir"


def test_ham_durum_prefix():
    for d in _seriler()[:4]:
        H = ES.es_ham(d)
        for k in (120, 300, 501, len(d) - 3):
            if k >= len(d):
                continue
            Hk = ES.es_ham(d.iloc[:k])
            assert np.array_equal(H["u1"][:k], Hk["u1"]) and np.array_equal(H["s10f68"][:k], Hk["s10f68"]), f"prefix {k}"


def _sentetik_panel(tohum=5, nd=40, nu=60):
    rng = np.random.default_rng(tohum)
    KV = rng.integers(-1, 4, size=(nd, nu)); R15 = np.round(rng.normal(0, 0.05, (nd, nu)), 3)
    R15[rng.random((nd, nu)) < 0.05] = np.nan
    Pn = {"KV": KV, "R15": R15}
    C2._c2_havuz(Pn)
    return Pn, rng


def test_dislamali_es_kaba_kuvvet():
    Pn, rng = _sentetik_panel()
    nd, nu = Pn["KV"].shape
    F = rng.random((nd, nu)) < 0.25
    ok = np.flatnonzero((Pn["KV"].ravel() >= 0) & np.isfinite(Pn["R15"].ravel()))
    sec = rng.choice(ok, 50, replace=False); d = (sec // nu).astype(np.int64); j = (sec % nu).astype(np.int64)
    X = pd.DataFrame({"d": d, "j": j, "r15": Pn["R15"][d, j]})
    har0 = ES.es_dislanan(Pn, d, j)
    kd, kj = ES.es_kirli_cift(Pn, F, d)
    e0 = ES.es_es(Pn, X); e1 = ES.es_es(Pn, X, kd, kj)
    har1 = har0 | ES.es_dislanan(Pn, kd, kj)
    isr = F[Pn["h_d"], Pn["h_j"]]
    nk = ES.es_kume_say(Pn, d, j, isr, har0)
    for x in range(len(X)):
        for e, h in ((e0, har0), (e1, har1)):
            k = ES.es_kaba(Pn, int(d[x]), int(j[x]), float(X.r15[x]), h)
            assert k["n_es"] == e["n_es"][x]
            for c in ("es_r15", "sira"):
                assert (np.isnan(k[c]) and np.isnan(e[c][x])) or np.isclose(k[c], e[c][x], rtol=1e-12), (x, c, k[c], e[c][x])
        # kirli sayısı: aynı (d, kova) üyeleri, olay çiftleri hariç, F bayraklı — tamamen bağımsız döngü
        n = 0
        for jj in range(nu):
            if Pn["KV"][d[x], jj] == Pn["KV"][d[x], j[x]] and np.isfinite(Pn["R15"][d[x], jj]) and F[d[x], jj] and \
                    not any((d[y] == d[x]) and (j[y] == jj) for y in range(len(X))):
                n += 1
        assert nk[x] == n, (x, nk[x], n)
        assert e1["n_es"][x] == e0["n_es"][x] - nk[x]


def test_c_kirli_temiz_kaba():
    Pn, rng = _sentetik_panel(7, nd=30, nu=80)
    nd, nu = Pn["KV"].shape
    Pn["P"] = {"tarih": pd.DatetimeIndex(pd.bdate_range("2017-01-02", periods=nd))}
    F = rng.random((nd, nu)) < 0.3
    C = ES.es_c(Pn, F, None, 0)["d1619"]
    sw = ww = 0.0; nh = 0
    for dd in range(nd):
        for k in range(36):
            m = (Pn["KV"][dd] == k) & np.isfinite(Pn["R15"][dd])
            a = m & F[dd]; b = m & ~F[dd]
            if a.sum() >= 1 and b.sum() >= 5:
                sw += a.sum() * (Pn["R15"][dd][a].mean() - Pn["R15"][dd][b].mean()); ww += a.sum(); nh += 1
    assert C["n_hucre"] == nh and np.isclose(C["fark"], sw / ww, rtol=1e-12) and C["alt"] <= C["fark"] <= C["ust"]


def test_esik_sha_sabit():
    assert ES.es_esik_sha() == ES.es_esik_sha(dict(ES.ES_ESIK))


def test_cakisma_kapisi():
    kaynak = open(os.path.join(KOK, "MACD_UYUM_ES.py"), encoding="utf-8").read()
    ns = {"__name__": "es_test"}
    exec(compile(kaynak, "MACD_UYUM_ES.py", "exec"), ns)
    exec(compile(kaynak, "MACD_UYUM_ES.py", "exec"), ns)
    ns2 = {"__name__": "es_test", "es_ham": "başka modülün adı", "_CK_KAYIT": {"es_ham": "BASKA.py"}}
    try:
        exec(compile(kaynak, "MACD_UYUM_ES.py", "exec"), ns2)
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
