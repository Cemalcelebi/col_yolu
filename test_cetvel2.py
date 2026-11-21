"""test_cetvel2 — CETVEL2.py mekanik denetimleri (sentetik veri; gerçek veri / sonuç görülmez).

Kapsam: çakışma kapısı; R15 matrisi = düz döngü = POZITIF_KONTROL.pk_r15; kova (sınırlar yalnız eğitimden); c2_es = kaba kuvvet eş kurulumu
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
        assert os.path.exists(os.path.join(cikti, "cetvel2_guc.json")) and os.path.exists(os.path.join(cikti, "cetvel2_esik.json"))
        C2.c2_kapi(cikti, veri, git=False, kontrol=True)
        C2._C2_PN.clear(); C2._C2_A.clear()
        J = C2.c2_kos(cikti, veri, islem=1, git=False, kontrol=True)
        assert J["yeniden"]["tuttu"], J["yeniden"]
        assert J["sonuc"]["karar"] in ("EVET", "KISMEN", "HAYIR (KUSUR)")
        assert os.path.exists(os.path.join(cikti, "CETVEL2_POZITIF_KONTROL.md"))
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
