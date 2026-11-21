"""test_cetvel2 — CETVEL2.py mekanik denetimleri (sentetik veri; gerçek veri / sonuç görülmez).

Kapsam (v2.2 eki: c2_rh / c2_panel_h düz döngü, H = 15 v2.1 ile aynı, iki yönlü plasebo, hücre adları, R45 / sonuç kuralı, ön kayıt -> kapı -> koşu
sentetik, KASA kesik aşımı, v2.1 regresyonu gerçek açık veride (veri yoksa atlanır)): çakışma kapısı; R15 matrisi = düz döngü = POZITIF_KONTROL.pk_r15; kova (sınırlar yalnız eğitimden); c2_es = kaba kuvvet eş kurulumu
(dışlama, SIRA, eşsiz); plasebo ~0 ve kapı; yapay iz yakalanıyor (+ ve -); prefix (veri t'de kesilince kova girdileri aynı); güç eğrisi;
etiket kuralları; c2_olc uçtan uca; ön kayıt -> kapı -> pozitif kontrol koşusu (A / B / C / yeniden üretim) sentetik klasörde.
Çalıştır:  python test_cetvel2.py   (ya da pytest -q test_cetvel2.py)
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import CETVEL2 as C2  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402
import POZITIF_KONTROL as PK  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402


def _seri(n: int, tohum: int, bas: str = "2015-06-01", fiyat: float = 50.0, mu: float = 0.0003, sd: float = 0.02) -> pd.DataFrame:
    rng = np.random.default_rng(tohum)
    r = rng.normal(mu, sd, n)
    C = fiyat * np.exp(np.cumsum(r))
    O = np.r_[C[0], C[:-1]] * (1 + rng.normal(0, 0.005, n))
    H = np.maximum(O, C) * (1 + np.abs(rng.normal(0, 0.008, n))) + 1e-6
    L = np.minimum(O, C) * (1 - np.abs(rng.normal(0, 0.008, n)))
    V = rng.lognormal(np.log(2e5), 0.6, n)
    ix = pd.bdate_range(bas, periods=n)
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=ix)
    bos = rng.choice(np.arange(200, n), size=8, replace=False)      # birkaç geçersiz bar (V = 0) -> geçerli bar kuralı
    d.iloc[bos, d.columns.get_loc("Volume")] = 0.0
    return d


def _ham(pazar: str, n_hisse: int, tohum: int, n: int = 2900) -> dict:
    rng = np.random.default_rng(tohum)
    return {f"S{pazar[0]}{i:03d}": _seri(n, tohum * 1000 + i, fiyat=float(10 + i), sd=float(rng.uniform(0.01, 0.04))) for i in range(n_hisse)}


def _vd(pazar: str, n_hisse: int, tohum: int) -> dict:
    Vd = OC._oc_veri_sar(_ham(pazar, n_hisse, tohum), pazar); Vd["temiz"] = {}; Vd["temiz_n"] = 0
    return Vd


_PN: dict = {}


def _pn(n_hisse: int = 120) -> dict:
    if n_hisse not in _PN:
        _PN[n_hisse] = C2.c2_panel(_vd("ABD", n_hisse, 7))
    return _PN[n_hisse]


# ------------------------------------------------------------------ çakışma kapısı
def test_cakisma_kapisi():
    kaynak = open(os.path.join(KOK, "CETVEL2.py"), encoding="utf-8").read()
    ns = {"__name__": "c2_test"}
    exec(compile(kaynak, "CETVEL2.py", "exec"), ns)
    exec(compile(kaynak, "CETVEL2.py", "exec"), ns)          # aynı dosya yeniden: geçer
    ns2 = {"__name__": "c2_test", "c2_es": 1}
    exec(compile(kaynak, "CETVEL2.py", "exec"), ns2)         # c2_ önekli ad: geçer
    ns3 = {"__name__": "c2_test", "kaynak_x": "başka"}
    exec(compile(kaynak, "CETVEL2.py", "exec"), ns3)
    assert ns3["kaynak_x"] == "başka"
    ns4 = {"__name__": "c2_test", "KOK": "başka modülün adı", "_CK_KAYIT": {}}
    try:
        kaynak2 = kaynak.replace("KOK_C2 = os.path", "KOK = 'ezen'\nKOK_C2 = os.path", 1)
        exec(compile(kaynak2, "CETVEL2.py", "exec"), ns4)
    except RuntimeError as ex:
        assert "EZDİ" in str(ex)
    else:
        raise AssertionError("çakışma kapısı önek dışı adı ezmeye izin verdi")


# ------------------------------------------------------------------ R15
def test_r15_duz_dongu_ve_pk_r15():
    Pn = _pn(); P = Pn["P"]; idx = P["tarih"]; V = Pn["Vd"]["V"]
    rng = np.random.default_rng(1)
    for _ in range(300):
        j = int(rng.integers(len(P["sembol"]))); s = P["sembol"][j]; df = V[s]
        k = int(rng.integers(len(df))); d = idx.get_loc(df.index[k])
        if k + 14 < len(df) and idx.get_loc(df.index[k + 14]) - d <= 29:
            v = df.Close.iloc[k + 14] / df.Open.iloc[k] - 1
        else:
            v = np.nan
        assert np.isclose(Pn["R15"][d, j], v, rtol=1e-12, equal_nan=True), (s, d)
    dd = rng.integers(0, len(idx), 2000); jj = rng.integers(0, len(P["sembol"]), 2000)
    pk = PK.pk_r15(P, Pn["Cl"], dd, jj)
    ok = np.isfinite(P["Op"][dd, jj])                        # pk_r15 giriş barı geçerli olmalı
    assert np.allclose(pk[ok], Pn["R15"][dd, jj][ok], equal_nan=True)
    # kriz kesiği: 31.08.2026 sonrası veri yok, son girişlerde 15 bar yoksa NaN
    son = np.flatnonzero(idx <= pd.Timestamp("2026-08-31"))[-1]
    assert np.isnan(Pn["R15"][son - 5:, :]).all()


# ------------------------------------------------------------------ kova
def test_kova_sinir_yalniz_egitimden():
    Vd = _vd("ABD", 60, 11); Pn = C2.c2_panel(Vd)
    Vd2 = _vd("ABD", 60, 11)
    for s, d in Vd2["V"].items():                            # sınama dönemini boz: sınırlar değişmemeli
        m = d.index >= "2023-01-01"
        d.loc[m, ["Open", "High", "Low", "Close"]] *= np.linspace(1, 5, m.sum())[:, None]
    Pn2 = C2.c2_panel(Vd2)
    assert Pn["sinir"]["ATRP"] == Pn2["sinir"]["ATRP"] and Pn["sinir"]["F15"] == Pn2["sinir"]["F15"]
    KV = Pn["KV"]; ok = KV >= 0
    assert ok.any() and KV[ok].max() < 36
    at = KV[ok] // 12; lq = (KV[ok] % 12) // 4; fq = KV[ok] % 4
    assert np.array_equal(lq, Pn["LQ"][ok]) and set(np.unique(at)) <= {0, 1, 2} and set(np.unique(fq)) <= {0, 1, 2, 3}
    a = Pn["ATRP"][ok]; t1, t2 = Pn["sinir"]["ATRP"]
    assert np.array_equal(at, np.where(a <= t1, 0, np.where(a <= t2, 1, 2)))


# ------------------------------------------------------------------ eş kurulumu (kaba kuvvet)
def _es_kaba(Pn, d, j, x, exc, me):
    P = Pn["P"]; k = Pn["KV"][d, j]
    if k < 0 or not np.isfinite(x):
        return np.nan, np.nan, 0
    m = (Pn["KV"][d] == k) & np.isfinite(Pn["R15"][d]) & P["ok"][d] & (P["H"][d] >= 0)
    for (dd, jj) in exc:
        if dd == d:
            m[jj] = False
    m[j] = False
    e = Pn["R15"][d, m]
    if len(e) < me:
        return np.nan, np.nan, len(e)
    return float(e.mean()), float(((e < x).sum() + 0.5 * (e == x).sum()) / len(e)), len(e)


def test_es_kaba_kuvvet():
    Pn = _pn(); KV = Pn["KV"]
    rng = np.random.default_rng(3)
    dd, jj = np.nonzero((KV >= 0) & np.isfinite(Pn["R15"]))
    sec = rng.choice(len(dd), 400, replace=False)
    d, j = dd[sec], jj[sec]
    x = Pn["R15"][d, j] * (1 + rng.choice([0.0, 0.03], size=len(d)))
    x[:5] = Pn["R15"][d[:5], j[:5]]                          # eşitlik (kendi değeri) durumu
    for me in (1, 2):
        e = C2.c2_es(Pn, d, j, x, d, j, es_min=me)
        exc = set(zip(d.tolist(), j.tolist()))
        for i in range(len(d)):
            es, sr, n = _es_kaba(Pn, d[i], j[i], x[i], exc, me)
            assert np.isclose(e["es_r15"][i], es, equal_nan=True, rtol=1e-12), i
            assert np.isclose(e["sira"][i], sr, equal_nan=True, rtol=1e-12), i
            assert e["n_es"][i] == n, (i, e["n_es"][i], n)
    # dışlama yok (yalnız kendisi)
    e = C2.c2_es(Pn, d[:50], j[:50], x[:50], es_min=1)
    for i in range(50):
        es, sr, n = _es_kaba(Pn, d[i], j[i], x[i], set(), 1)
        assert np.isclose(e["es_r15"][i], es, equal_nan=True) and e["n_es"][i] == n
    # varsayılan en az 5 eş: az eşli olay eşsiz
    e5 = C2.c2_es(Pn, d, j, x, d, j)
    assert np.all(np.isnan(e5["fark"][e5["n_es"] < 5]))


# ------------------------------------------------------------------ plasebo ve yapay iz
def _hucre_rast(Pn, n, delta, tohum, yon="+"):
    rng = np.random.default_rng(tohum); P = Pn["P"]
    dd, jj = np.nonzero((Pn["KV"] >= 0) & np.isfinite(Pn["R15"]))
    sec = rng.choice(len(dd), n, replace=False); d, j = dd[sec], jj[sec]
    x = (1 + Pn["R15"][d, j]) * (1 + delta) - 1
    e = C2.c2_es(Pn, d, j, x, d, j, es_min=1)
    return C2.c2_hucre(x, e["es_r15"], e["sira"], P["tarih"][d], yon, tohum_ek=tohum, egri=None)


def test_plasebo_sifir_ve_yapay_iz():
    Pn = _pn()
    F0 = [_hucre_rast(Pn, 600, 0.0, t)["fark"] for t in range(10)]
    assert abs(np.mean(F0)) < 0.004, np.mean(F0)
    c = _hucre_rast(Pn, 600, 0.05, 99)
    assert c["yakala_p"] and c["fark"] > 0.03 and c["sira"] > 0.5 and c["p"] < 0.01
    c = _hucre_rast(Pn, 600, -0.05, 98, yon="-")
    assert c["yakala_n"] and c["tutar"] and c["fark"] < -0.03 and c["sira"] < 0.5
    # plasebo kapısı fonksiyonu: aynı günlerle rastgele hisseler
    P = Pn["P"]; d = np.flatnonzero(P["tarih"] >= pd.Timestamp("2018-01-01"))[:400:2]
    old = C2.C2_ESIK["es_min"]; C2.C2_ESIK["es_min"] = 1
    try:
        pl = C2.c2_plasebo(Pn, np.repeat(d, 3), "+", None, tohum_sayi=10)
    finally:
        C2.C2_ESIK["es_min"] = old
    assert abs(pl["fark_ort"]) < 0.005 and pl["tutar_pay"] <= 0.2 and pl["n_ort"] > 300
    assert pl["tutar_pay"] == pl["tutar_pay_arti"] and 0 <= pl["tutar_pay_eksi"] <= 0.2
    rd, rj = C2.c2_rastgele(Pn, np.repeat(d[:5], 4), np.random.default_rng(0))
    assert len(set(zip(rd.tolist(), rj.tolist()))) == len(rd)          # gün içinde yerine koymadan


# ------------------------------------------------------------------ prefix
def test_prefix():
    Pn = _pn(); P = Pn["P"]; rng = np.random.default_rng(5); V = Pn["Vd"]["V"]
    sat = []
    for s in rng.choice(P["sembol"], 30, replace=False):
        t = V[s].index[int(rng.integers(200, len(V[s]) - 40))]
        sat.append({"sembol": s, "tarih": t})
    X, _ = C2.c2_olay(pd.DataFrame(sat), Pn, tekil_gun=1)
    pr = C2.c2_prefix(Pn, X, n=len(X))
    assert pr["n"] > 10 and pr["bozuk"] == 0, pr


# ------------------------------------------------------------------ güç
def test_guc_egrisi():
    rng = np.random.default_rng(2); f = rng.normal(0, 0.1, 5000)
    e = C2.c2_guc_egri(f)
    assert abs(e["b"] + 0.5) < 0.1
    g100, g1000 = C2.c2_guc(100, e), C2.c2_guc(1000, e)
    assert g1000 > g100
    s1000 = 0.1 / np.sqrt(1000) * np.sqrt(1 - 1000 / 5000)     # sonlu evren düzeltmesi yaklaşık
    assert 0.5 < g1000 < 1.0 and abs(np.exp(e["a"] + e["b"] * np.log(1000)) - s1000) / s1000 < 0.35
    assert np.isnan(C2.c2_guc(100, None))


# ------------------------------------------------------------------ etiket
def _h(fark, alt, ust, n=500, guc=0.9, kapi=True, tp=None, tn=None):
    tp = (fark > 0 and alt > 0) if tp is None else tp
    tn = (fark < 0 and ust < 0) if tn is None else tn
    return {"n": n, "fark": fark, "boot_alt": alt, "boot_ust": ust, "guc": guc, "plasebo_gecti": kapi, "tutar_p": tp, "tutar_n": tn,
            "tutar": tp}


def test_etiket():
    H = {p: {h: _h(0.01, 0.002, 0.02) for h in C2.C2_HUCRE} for p in C2.C2_KARAR}
    assert C2.c2_etiket(H, "+")["etiket"] == "KATKI+"
    H["AVR"]["sinama"] = _h(0.01, 0.002, 0.02, kapi=False)
    assert C2.c2_etiket(H, "+")["etiket"] == "SORGULA"
    H["AVR"]["sinama"] = _h(0.01, 0.002, 0.02, guc=0.5)
    assert C2.c2_etiket(H, "+")["etiket"] == "ÖLÇÜLEMEDİ"
    H["AVR"]["sinama"] = _h(-0.01, -0.02, -0.002)
    H["AVR"]["egitim"] = _h(0.01, 0.002, 0.02)
    assert C2.c2_etiket(H, "+")["etiket"] == "ÇELİŞKİLİ"
    Hn = {p: {h: _h(-0.01, -0.02, -0.002) for h in C2.C2_HUCRE} for p in C2.C2_KARAR}
    assert C2.c2_etiket(Hn, "-")["etiket"] == "KATKI−"
    assert C2.c2_etiket(Hn, "+")["etiket"] == "KATKI− (ters)"
    assert C2.c2_bh([0.001, 0.5, 0.04], 0.10) == [True, False, True]


# ------------------------------------------------------------------ sonuç kuralı (iii) birleşik
def test_sonuc_kurali_birlesik():
    def J(yakala_1000):
        A = [{"pazar": p, "hucre": h, "taban": "RAST", "n_hedef": nk, "delta": 0.0, "yakala": (yakala_1000 if nk == "1000" else 0.0), "tohum": 20}
             for p in C2.C2_KARAR for h in C2.C2_HUCRE for nk in ("100", "300", "1000", "yari")]
        A += [{"pazar": p, "hucre": h, "taban": "RAST", "n_hedef": "300", "delta": 0.02, "yakala": 0.9, "tohum": 20} for p in C2.C2_KARAR for h in C2.C2_HUCRE]
        B = [{"kod": k, "pazar": "ABD", "hucre": h, "fark": f, "boot_alt": a, "boot_ust": 0.02} for k, f, a in
             (("B1U", 0.01, 0.001), ("B1A", -0.01, -0.02), ("B2U", 0.0, -0.01), ("B2A", 0.0, -0.01)) for h in C2.C2_HUCRE]
        C = [{"pazar": p, "hucre": h, "n_hedef": "tam", "gecti": True} for p in C2.C2_KARAR for h in C2.C2_HUCRE]
        return {"A": {"ozet": {"tablo": A}}, "B": {"hucre": B}, "C": {"satir": C}}
    assert C2.c2_sonuc(J(0.15))["karar"] == "EVET"            # tek n hücresinde 3 / 20 artık KUSUR değil (birleşik %3,75)
    assert C2.c2_sonuc(J(0.45))["karar"] == "HAYIR (KUSUR)"   # birleşik %11,25 > %10


# ------------------------------------------------------------------ c2_olc uçtan uca
def test_c2_olc_uctan_uca():
    Pn = _pn(); P = Pn["P"]; V = Pn["Vd"]["V"]; rng = np.random.default_rng(8)
    sat = []
    for s in P["sembol"]:
        ix = V[s].index
        for k in range(300, len(ix) - 30, 70):
            sat.append({"pazar": "ABD", "sembol": s, "tarih": ix[k], "F_X": float(rng.random() < 0.5)})
    O = pd.DataFrame(sat)
    old = C2.C2_ESIK["es_min"]; C2.C2_ESIK["es_min"] = 1; C2._C2_PN["ABD"] = Pn
    try:
        R = C2.c2_olc(O, {"X": {"bayrak": "F_X", "yon": "+"}, "HEP": {"bayrak": None, "yon": "?"}}, guc={"egri": {}})
    finally:
        C2.C2_ESIK["es_min"] = old; C2._C2_PN.pop("ABD", None)
    S, Hc, Et = R["satir"], R["hucre"], R["etiket"]
    for c in ("r15", "h5", "st5", "h5_atr", "r60", "es_r15_X", "sira_X", "fark_X", "kova", "f15", "atrp"):
        assert c in S.columns, c
    assert set(Hc.kod) == {"X", "HEP"} and set(Hc.hucre) == {"egitim", "sinama"}
    x = Hc[(Hc.kod == "X") & (Hc.hucre == "sinama")].iloc[0]
    g = S[(S.F_X == 1) & (S.donem == "sinama")]
    assert x["n"] == int(np.isfinite(g.fark_X).sum()) and np.isclose(x["fark"], g.fark_X.mean())
    assert np.isnan(S.loc[S.F_X != 1, "fark_X"]).all()
    assert len(Et) == 2 and set(Et.columns) >= {"etiket", "etiket_ham", "bh_gecti", "p_bh"}
    # tekil 15: aynı hissede 15 günden yakın olay düşer
    jl = int(np.argmax((P["ok"] & (P["H"] >= 0)).sum(0)))            # havuzda en çok bulunan hisse (alt %20 likidite dışı)
    sl = P["sembol"][jl]; ixl = V[sl].index
    ks = [k for k in range(300, len(ixl) - 40) if all(P["ok"][P["tarih"].get_loc(ixl[k + q]), jl] for q in (1, 6, 31))][:1]
    O2 = pd.DataFrame([{"pazar": "ABD", "sembol": sl, "tarih": ixl[ks[0] + q]} for q in (0, 5, 30)])
    X2, sy = C2.c2_olay(O2.drop(columns="pazar"), Pn)
    assert len(X2) == 2 and sy["tekil"] == 1


# ------------------------------------------------------------------ ön kayıt -> kapı -> koşu (sentetik klasör)
def test_onkayit_kapi_kos_sentetik():
    tmp = tempfile.mkdtemp(prefix="c2_test_")
    eski_yol = dict(C2.C2_YOL); eski_es = C2.C2_ESIK["es_min"]; eski_A = json.loads(json.dumps(C2.C2_ESIK["A"]))
    eski_pl = dict(C2.C2_ESIK["plasebo"]); eski_yu = dict(C2.C2_ESIK["yeniden_uretim"])
    try:
        veri = os.path.join(tmp, "veri"); cikti = os.path.join(tmp, "cikti"); os.makedirs(veri); os.makedirs(cikti)
        H = {p: _ham(p, 70, 20 + i) for i, p in enumerate(C2.C2_PAZAR)}
        for p in C2.C2_PAZAR:
            pd.to_pickle(H[p], os.path.join(veri, f"V_{p}.pkl"))
        rng = np.random.default_rng(4); ds, pb = [], []
        for p in C2.C2_PAZAR:
            for s, d in H[p].items():
                ix = d.index[(d.index >= "2016-03-01") & (d.index <= "2026-07-01")]
                for k in range(0, len(ix), 45):
                    ds.append({"pazar": p, "sembol": s, "tarih": ix[k]})
                if p in ("ABD", "AVR"):
                    me = pd.Series(ix, index=ix).groupby(ix.to_period("M")).max()
                    for t in me.iloc[::2]:
                        u = rng.random()
                        if u < 0.2 or u > 0.8:
                            for kod in (["B1", "B2"] if p == "ABD" else ["B1"]):
                                pb.append({"kod": kod, "pazar": p, "sembol": s, "tarih": t, "giris": t + pd.offsets.BDay(1),
                                           "donem": "egitim" if t < pd.Timestamp("2023-01-01") else "sinama", "U": u > 0.8, "A": u < 0.2})
        dsy = os.path.join(tmp, "ds_olay.csv.gz"); pd.DataFrame(ds).to_csv(dsy, index=False, compression="gzip")
        pby = os.path.join(tmp, "pk_b.csv.gz"); pd.DataFrame(pb).to_csv(pby, index=False, compression="gzip")
        pjy = os.path.join(tmp, "pk.json")
        json.dump({"B": {"sonuc": [{"kod": k, "pazar": "ABD", "hucre": h, "h5": {"fark": 0.01, "boot_alt": -0.01, "boot_ust": 0.03, "p": 0.2, "n": 100},
                                    "r15": {"fark": 0.001, "boot_alt": -0.01, "boot_ust": 0.01}} for k in ("B1U", "B1A") for h in C2.C2_HUCRE]}},
                  open(pjy, "w"))
        C2.C2_YOL.update({"veri": veri, "cikti": cikti, "ds_olay": dsy, "pk_b": pby, "pk_json": pjy})
        C2.C2_ESIK["es_min"] = 1
        C2.C2_ESIK["A"]["tohum_sayi"] = 2; C2.C2_ESIK["A"]["n"] = [30, "yari"]
        C2.C2_ESIK["plasebo"]["tohum_sayi"] = 3; C2.C2_ESIK["yeniden_uretim"]["elle_r15"] = 10; C2.C2_ESIK["yeniden_uretim"]["elle_es"] = 2
        C2._C2_PN.clear(); C2._C2_A.clear()
        yol = C2.c2_onkayit_yaz(cikti, veri, ds_yol=dsy)
        metin = open(yol, encoding="utf-8").read()
        assert "KONTROL LİSTESİ" in metin and "C2_ESIK_SHA" in metin and "ATRP t1" in metin and "## 1. CETVEL2 TANIMI" in metin
        assert os.path.exists(C2._c2_yol("guc", cikti)) and os.path.exists(C2._c2_yol("esik", cikti))
        C2.c2_kapi(cikti, veri, git=False, kontrol=True)
        C2._C2_PN.clear(); C2._C2_A.clear()
        J = C2.c2_kos(cikti, veri, islem=1, git=False, kontrol=True)
        assert J["yeniden"]["tuttu"], J["yeniden"]
        assert J["sonuc"]["karar"] in ("EVET", "KISMEN", "HAYIR (KUSUR)")
        assert os.path.exists(C2._c2_yol("rapor", cikti))
        try:
            C2.c2_kos(cikti, veri, islem=1, git=False)
        except C2.C2Hata as ex:
            assert "ikinci koşu" in str(ex)
        else:
            raise AssertionError("ikinci koşu durmadı")
        # mühür: eşik sözlüğü değişince kapı durur
        C2.C2_ESIK["es_min"] = 2
        try:
            C2.c2_kapi(cikti, veri, git=False, kontrol=False)
        except C2.C2Hata as ex:
            assert "C2_ESIK_SHA" in str(ex)
        else:
            raise AssertionError("kapı değişen eşik sözlüğünü yakalamadı")
    finally:
        C2.C2_YOL.clear(); C2.C2_YOL.update(eski_yol); C2.C2_ESIK["es_min"] = eski_es; C2.C2_ESIK["A"] = eski_A
        C2.C2_ESIK["plasebo"] = eski_pl; C2.C2_ESIK["yeniden_uretim"] = eski_yu
        C2._C2_PN.clear(); C2._C2_A.clear()
        shutil.rmtree(tmp, ignore_errors=True)


# ================================================================== v2.2 (ufuk H = 15 / 30 / 45; KART_TUR1_IS_TANIMI.md ADIM K1)
def test_v22_rh_ve_havuz():
    Pb = _pn(); P = Pb["P"]; idx = P["tarih"]; V = Pb["Vd"]["V"]
    P15 = C2.c2_panel_h(Pb, 15)
    assert np.array_equal(np.isnan(P15["R15"]), np.isnan(Pb["R15"])) and np.array_equal(P15["h_r"], Pb["h_r"])
    assert P15["R15"] is not Pb["R15"] and Pb.get("ufuk") is None           # taban panel değişmedi
    for H in (30, 45):
        Pn = C2.c2_panel_h(Pb, H); Rz = 2 * H; rng = np.random.default_rng(H)
        for _ in range(300):
            j = int(rng.integers(len(P["sembol"]))); s = P["sembol"][j]; df = V[s]
            k = int(rng.integers(len(df))); d = idx.get_loc(df.index[k])
            if k + H - 1 < len(df) and idx.get_loc(df.index[k + H - 1]) - d <= Rz - 1:
                v = df.Close.iloc[k + H - 1] / df.Open.iloc[k] - 1
            else:
                v = np.nan
            assert np.isclose(Pn["R15"][d, j], v, rtol=1e-12, equal_nan=True), (H, s, d)
        assert len(Pn["h_r"]) == int(((Pn["KV"] >= 0) & np.isfinite(Pn["R15"])).sum()) and Pn["ufuk"] == H
        assert np.array_equal(Pn["KV"], Pb["KV"])                               # kova ufuktan bağımsız
        # eş kaba kuvvet (ufuk H havuzu)
        dd, jj = np.nonzero((Pn["KV"] >= 0) & np.isfinite(Pn["R15"]))
        sec = rng.choice(len(dd), 100, replace=False); d, j = dd[sec], jj[sec]; x = Pn["R15"][d, j]
        e = C2.c2_es(Pn, d, j, x, d, j, es_min=1); exc = set(zip(d.tolist(), j.tolist()))
        for i in range(len(d)):
            es, sr, n = _es_kaba(Pn, d[i], j[i], x[i], exc, 1)
            assert np.isclose(e["es_r15"][i], es, equal_nan=True, rtol=1e-12) and e["n_es"][i] == n


def test_v22_donem_ve_esik():
    g = pd.to_datetime(["2015-12-31", "2016-01-01", "2019-12-31", "2020-01-01", "2022-12-31", "2023-01-02"])
    assert list(C2._c2_donem22(g)) == ["dis", "d1619", "d1619", "d2022", "d2022", "dis"]
    assert C2.C2_ESIK22["kova_donem"] == C2.C2_ESIK["donem"]["egitim"]
    assert C2.C2_ESIK22["ufuklar"] == [15, 30, 45] and C2.C2_ESIK22["karar_ufuk"] == [15, 30]
    assert C2.c2_esik22_sha() != C2.c2_esik_sha()
    import IZ_KARNE as IK
    assert {k["kod"] for k in IK.IK_KONTROL} <= set(C2.C2_KONTROL22)


def test_v22_plasebo_iki_yon():
    Pn = _pn(); P = Pn["P"]; d = np.flatnonzero(P["tarih"] >= pd.Timestamp("2018-01-01"))[:300:2]
    old = C2.C2_ESIK["es_min"]; C2.C2_ESIK["es_min"] = 1
    try:
        a = C2.c2_plasebo(Pn, np.repeat(d, 3), "?", None, tohum_sayi=8)
        b = C2.c2_plasebo(Pn, np.repeat(d, 3), "?", None, tohum_sayi=8, iki_yon_ayri=True)
        c = C2.c2_plasebo(Pn, np.repeat(d, 3), "+", None, tohum_sayi=8, iki_yon_ayri=True)
        c0 = C2.c2_plasebo(Pn, np.repeat(d, 3), "+", None, tohum_sayi=8)
    finally:
        C2.C2_ESIK["es_min"] = old
    Pl = C2.C2_ESIK["plasebo"]
    assert a["fark_ort"] == b["fark_ort"] and a["tutar_pay"] == b["tutar_pay"]
    ok_v21 = abs(a["fark_ort"]) < Pl["fark_mutlak"] and a["tutar_pay"] <= Pl["tutar_pay"]
    ok_v22 = abs(b["fark_ort"]) < Pl["fark_mutlak"] and b["tutar_pay_arti"] <= Pl["tutar_pay"] and b["tutar_pay_eksi"] <= Pl["tutar_pay"]
    assert a["gecti"] == ok_v21 and b["gecti"] == ok_v22
    assert c["gecti"] == c0["gecti"]                                        # '+' hipotezde v2.1 ile aynı
    # birleşik payı %7'yi aşan ama yön başına %7 içinde kalan durum: v2.2 geçer, v2.1 düşer (sözde tohum tablosuyla)
    S = pd.DataFrame({"tutar_p": [True] + [False] * 19, "tutar_n": [False] + [True] + [False] * 18})
    assert (S.tutar_p | S.tutar_n).mean() == 0.10 and S.tutar_p.mean() <= 0.07 and S.tutar_n.mean() <= 0.07


def test_v22_etiket_hucreler():
    hl = C2.C2_HUCRE22
    H = {p: {h: _h(0.01, 0.002, 0.02) for h in hl} for p in C2.C2_KARAR}
    assert C2.c2_etiket(H, "+", hucreler=hl)["etiket"] == "KATKI+"
    H["ABD"]["d2022"] = _h(-0.01, -0.02, -0.002)
    e = C2.c2_etiket(H, "+", hucreler=hl)
    assert e["etiket"] == "ÇELİŞKİLİ" and "d1619 / d2022" in e["neden"]
    # tek hücre (K2 birikimli kasa hücresi)
    H1 = {p: {"kasa4": _h(0.01, 0.002, 0.02)} for p in C2.C2_KARAR}
    assert C2.c2_etiket(H1, "+", hucreler=["kasa4"])["etiket"] == "KATKI+"


def _olaylar_sentetik(Pn, tohum=8, adim=70):
    P = Pn["P"]; V = Pn["Vd"]["V"]; rng = np.random.default_rng(tohum); sat = []
    for s in P["sembol"]:
        ix = V[s].index
        for k in range(300, len(ix) - 30, adim):
            sat.append({"pazar": "ABD", "sembol": s, "tarih": ix[k], "F_X": float(rng.random() < 0.5)})
    return pd.DataFrame(sat)


def test_v22_olc_ufuk15_v21_ile_ayni_ve_ufuk30():
    Pb = _pn(); O = _olaylar_sentetik(Pb)
    old = C2.C2_ESIK["es_min"]; C2.C2_ESIK["es_min"] = 1
    C2._C2_PN["ABD"] = Pb; C2._C2_PN22[("baz", "ABD")] = Pb
    try:
        hip = {"X": {"bayrak": "F_X", "yon": "+"}, "HEP": {"bayrak": None, "yon": "?"}}
        R21 = C2.c2_olc(O, hip, guc={"egri": {}}, plasebo=False, bilgi=False)
        R15 = C2.c2_olc22(O, hip, 15, guc={"egri": {}}, plasebo=False, bilgi=False)
        R30 = C2.c2_olc22(O, hip, 30, guc={"egri": {}}, plasebo=True, bilgi=False)
        Rk = C2.c2_olc22(O, hip, 30, donem={"acik": ["2016-01-01", "2022-12-31"], "kasa": ["2023-01-01", "2023-12-31"]}, guc={"egri": {}},
                         plasebo=False, bilgi=False)
    finally:
        C2.C2_ESIK["es_min"] = old; C2._C2_PN.pop("ABD", None); C2._C2_PN22.clear()
    a, b = R21["satir"], R15["satir"]
    assert len(a) == len(b) and (a.sembol.to_numpy() == b.sembol.to_numpy()).all()
    for c in ("r15", "es_r15_X", "sira_X", "fark_X", "kova", "E0", "es_r15_HEP", "fark_HEP"):
        assert np.allclose(a[c].to_numpy(float), b[c].to_numpy(float), rtol=0, atol=0, equal_nan=True), c
    assert set(R15["hucre"].hucre) == {"d1619", "d2022"} and (R15["hucre"].ufuk == 15).all() and "ufuk" not in R21["hucre"].columns
    S, Hc = R30["satir"], R30["hucre"]
    assert (S.ufuk == 30).all() and set(Hc.hucre) == {"d1619", "d2022"}
    x = Hc[(Hc.kod == "X") & (Hc.hucre == "d2022")].iloc[0]; g = S[(S.F_X == 1) & (S.donem == "d2022")]
    assert x["n"] == int(np.isfinite(g.fark_X).sum()) and np.isclose(x["fark"], g.fark_X.mean())
    # tekil 30: aynı hissede ardışık olaylar >= 30 birleşik takvim günü arayla
    for s_, gg in S.groupby("sembol"):
        assert (np.diff(np.sort(gg.d.to_numpy())) >= 30).all()
    # R_H = c2_rh
    Pn30 = C2.c2_panel_h(Pb, 30)
    assert np.allclose(S.r15.to_numpy(float), Pn30["R15"][S.d.to_numpy(int), S.j.to_numpy(int)], equal_nan=True)
    assert set(Rk["hucre"].hucre) == {"acik", "kasa"} and "ufuk" in Rk["etiket"].columns
    try:
        C2.c2_olc22(O, hip, 20)
    except C2.C2Hata:
        pass
    else:
        raise AssertionError("tanımsız ufuk durmadı")


def test_v22_r45_ve_sonuc_kurali():
    def J(b45, b30, kapi45=True, b1a=-0.01):
        B = []
        for H, ba in ((15, -0.001), (30, b30), (45, b45)):
            for h in C2.C2_HUCRE22:
                B.append({"kod": "B1U", "pazar": "ABD", "hucre": h, "ufuk": H, "fark": 0.01, "boot_alt": ba[h] if isinstance(ba, dict) else ba,
                          "boot_ust": 0.03})
                B.append({"kod": "B1A", "pazar": "ABD", "hucre": h, "ufuk": H, "fark": b1a, "boot_alt": b1a - 0.01 if b1a < 0 else 0.001,
                          "boot_ust": 0.02})
        C = [{"pazar": p, "hucre": h, "ufuk": H, "n_hedef": "tam", "gecti": (kapi45 if H == 45 else True)} for p in ("ABD", "AVR", "BIST")
             for h in C2.C2_HUCRE22 for H in (15, 30, 45)]
        A = [{"ufuk": H, "pazar": p, "hucre": h, "taban": "RAST", "n_hedef": nk, "delta": de, "yakala": (0.9 if de == 0.02 and nk == "300" else
                                                                                                         0.02), "tohum": 20}
             for H in (15, 30, 45) for p in C2.C2_KARAR for h in C2.C2_HUCRE22 for nk in ("100", "300", "1000") for de in (0.0, 0.02)]
        return {"A": {"ozet": {"tablo": A}}, "B": {"hucre": B}, "C": {"satir": C}}
    r = C2.c2_r45(J(0.002, {"d1619": 0.001, "d2022": -0.001}))
    assert r["karar"] == "KARAR" and r["i"] and r["ii"]
    assert C2.c2_r45(J(0.002, 0.001))["karar"] == "BİLGİ"                 # R30 iki dönemde de görüyor
    assert C2.c2_r45(J({"d1619": 0.002, "d2022": -0.001}, -0.001))["karar"] == "BİLGİ"
    assert C2.c2_r45(J(0.002, -0.001, kapi45=False))["karar"] == "BİLGİ"
    s = C2.c2_sonuc22(J(0.002, 0.001))
    assert s["30"]["karar"] == "EVET" and s["15"]["karar"] == "KISMEN"       # R15'te B1U boot alt < 0
    s = C2.c2_sonuc22(J(0.002, 0.001, b1a=0.01))
    assert all(v["karar"] == "HAYIR (KUSUR)" for v in s.values())


def _ham22(pazar, n_hisse, tohum, n=1980):
    rng = np.random.default_rng(tohum)
    return {f"S{pazar[0]}{i:03d}": _seri(n, tohum * 1000 + i, fiyat=float(10 + i), sd=float(rng.uniform(0.01, 0.04))) for i in range(n_hisse)}


def test_v22_onkayit_kapi_kos_sentetik():
    tmp = tempfile.mkdtemp(prefix="c2_22_test_")
    eski_yol = dict(C2.C2_YOL); eski_es = C2.C2_ESIK["es_min"]; eski_pl = dict(C2.C2_ESIK["plasebo"])
    eski_A = json.loads(json.dumps(C2.C2_ESIK22["A"])); eski_Y = json.loads(json.dumps(C2.C2_ESIK22["yeniden_uretim"]))
    eski_C = json.loads(json.dumps(C2.C2_ESIK22["C"]))
    try:
        veri = os.path.join(tmp, "veri"); cikti = os.path.join(tmp, "cikti"); os.makedirs(veri); os.makedirs(cikti)
        H = {p: _ham22(p, 45, 30 + i) for i, p in enumerate(C2.C2_PAZAR)}
        assert max(d.index.max() for d in H["ABD"].values()) <= pd.Timestamp("2022-12-31")
        for p in C2.C2_PAZAR:
            pd.to_pickle(H[p], os.path.join(veri, f"V_{p}.pkl"))
        ds = []
        for p in C2.C2_PAZAR:
            for i, (s, d) in enumerate(H[p].items()):     # hisse başına kaydırılmış günler (aynı gün olaylar eş havuzunu boşaltmasın)
                ix = d.index[(d.index >= "2016-03-01")]
                ds += [{"pazar": p, "sembol": s, "tarih": ix[k]} for k in range(i % 37, len(ix), 37)]
        ds.append({"pazar": "ABD", "sembol": "SA000", "tarih": pd.Timestamp("2024-05-02")})     # kesik sonrası satır: kopyaya girmez
        dsy = os.path.join(tmp, "ds_olay.csv.gz"); pd.DataFrame(ds).to_csv(dsy, index=False, compression="gzip")
        C2.C2_YOL.update({"veri": veri, "cikti": cikti, "ds_olay": dsy})
        C2.C2_ESIK["es_min"] = 1; C2.C2_ESIK["plasebo"]["tohum_sayi"] = 3
        C2.C2_ESIK22["A"]["tohum_sayi"] = 2; C2.C2_ESIK22["A"]["n"] = [30]; C2.C2_ESIK22["C"]["n"] = ["tam"]
        C2.C2_ESIK22["yeniden_uretim"]["elle_rh"] = 4; C2.C2_ESIK22["yeniden_uretim"]["elle_es"] = 1
        C2._C2_PN22.clear(); C2._C2_A22.clear()
        yol = C2.c2_onkayit22_yaz(cikti, veri, kasa=False)
        metin = open(yol, encoding="utf-8").read()
        for k in ("KONTROL LİSTESİ", "C2_ESIK22_SHA", "R45 KURALI", "ATRP t1", "VERİ YOK", "KASA: açık kesik", "C2_DS_ACIK22_SHA"):
            assert k in metin, k
        ac = pd.read_csv(os.path.join(cikti, "c2_ds_olay_acik_v2.2.csv.gz"), parse_dates=["tarih"])
        assert ac.tarih.max() <= pd.Timestamp("2022-12-31") and len(ac) == len(ds) - 1
        g = json.load(open(C2._c2_yol("guc", cikti, "_v2.2"), encoding="utf-8"))
        assert set(g["egri"]["ABD"]) == {"d1619", "d2022", "acik"} and set(g["egri"]["ABD"]["acik"]) == {"15", "30", "45"}
        C2.c2_kapi22(cikti, veri, git=False, kontrol=True)
        C2._C2_PN22.clear(); C2._C2_A22.clear()
        J = C2.c2_kos22(cikti, veri, islem=1, git=False, kontrol=True, kasa=False, regresyon=False)
        assert J["yeniden"]["tuttu"], J["yeniden"]
        assert set(J["sonuc"]) == {"15", "30", "45"} and J["r45"]["karar"] in ("KARAR", "BİLGİ")
        assert os.path.exists(C2._c2_yol("rapor", cikti, "_v2.2"))
        Bs = pd.read_csv(C2._c2_yol("b_satir", cikti, "_v2.2"), parse_dates=["giris"])
        assert set(Bs.ufuk) == {15, 30, 45} and Bs.giris.max() <= pd.Timestamp("2022-12-31")
        assert pd.to_datetime(J["en_gec"]["c2_b_olay_v2.2.csv.gz"]) <= pd.Timestamp("2022-12-31")
        try:
            C2.c2_kos22(cikti, veri, islem=1, git=False, kasa=False, regresyon=False)
        except C2.C2Hata as ex:
            assert "ikinci koşu" in str(ex)
        else:
            raise AssertionError("ikinci koşu durmadı")
        C2.C2_ESIK22["r45_kurali"] += " "
        try:
            C2.c2_kapi22(cikti, veri, git=False, kontrol=False)
        except C2.C2Hata as ex:
            assert "C2_ESIK22_SHA" in str(ex)
        else:
            raise AssertionError("kapı değişen v2.2 eşik sözlüğünü yakalamadı")
    finally:
        C2.C2_YOL.clear(); C2.C2_YOL.update(eski_yol); C2.C2_ESIK["es_min"] = eski_es; C2.C2_ESIK["plasebo"] = eski_pl
        C2.C2_ESIK22["A"] = eski_A; C2.C2_ESIK22["yeniden_uretim"] = eski_Y; C2.C2_ESIK22["C"] = eski_C
        if C2.C2_ESIK22["r45_kurali"].endswith(" "):
            C2.C2_ESIK22["r45_kurali"] = C2.C2_ESIK22["r45_kurali"][:-1]
        C2._C2_PN22.clear(); C2._C2_A22.clear(); C2._C2_B22.clear()
        shutil.rmtree(tmp, ignore_errors=True)


def test_v22_kasa_kapisi_kesik_asimi():
    import KASA as KS
    tmp = tempfile.mkdtemp(prefix="c2_22_kasa_")
    try:
        y = os.path.join(tmp, "olay.csv"); pd.DataFrame({"tarih": ["2022-12-30", "2023-01-03"]}).to_csv(y, index=False)
        try:
            KS.kasa_kapisi([y], kesik="2022-12-31")
        except KS.KasaHata as ex:
            assert "KESİK AŞIMI" in str(ex)
        else:
            raise AssertionError("kasa kapısı kesik aşımını yakalamadı")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_v22_regresyon_v21_gercek():
    """v2.1 çağrısı açık veride c2_b_olay_v2.1 satırlarıyla birebir (gerçek veri yoksa atlanır)."""
    gerek = [os.path.join(C2.C2_YOL["veri"], "V_ABD.pkl"), os.path.join(C2.C2_YOL["veri"], "V_AVR.pkl"), C2.C2_YOL["pk_b"],
             C2._c2_yol("b_satir", None, "_v2.1"), C2._c2_yol("esik", None, "_v2.1")]
    if not all(os.path.exists(y) for y in gerek) or os.environ.get("C2_REGRESYON_ATLA"):
        print("  (atlandı: gerçek veri / v2.1 satır dosyası yok)"); return
    R = C2.c2_regresyon21()
    assert R["tuttu"], R
    assert len(R["hucre"]) == 3 and all(h["n_21"] >= 1000 for h in R["hucre"])


if __name__ == "__main__":
    import time as _t
    hata = 0
    for ad, f in list(globals().items()):
        if ad.startswith("test_") and callable(f):
            t0 = _t.time()
            try:
                f(); print(f"GEÇTİ  {ad} ({_t.time() - t0:.1f} sn)")
            except Exception as ex:  # noqa: BLE001
                hata += 1; print(f"KALDI  {ad}: {type(ex).__name__}: {ex}")
                import traceback; traceback.print_exc()
    print("SONUÇ:", "hepsi geçti" if not hata else f"{hata} test kaldı")
    sys.exit(1 if hata else 0)
