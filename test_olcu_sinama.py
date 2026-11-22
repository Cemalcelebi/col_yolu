"""test_olcu_sinama — OLCU_SINAMA.py mekanik denetimleri (sentetik veri; gerçek veri / sonuç görülmez).

Kapsam: çakışma kapısı; nedensel bölünme (ORTAK_CETVEL tam bilgi kuralının üst kümesi, veri kesilince önek aynı); evren 80. bardan sonra;
ölçüler (R / T5 / T10 / A / O5) = düz döngü; sürükleme delta 0 = taban, R sürüklemesi (1 + R)(1 + delta) - 1; os_es = kaba kuvvet (dışlama,
SIRA, eşsiz); hücre istatistiği (boot, L3O, TUTAR); kart sinyalleri (ondalık payı, MOM / STREV / HIGH52 düz hesap, giriş ertesi açılış);
EVREN PREFIX TESTİ sentetikte fark 0 ve bozulunca yakalıyor; plasebo ~0; yapay iz yakalanıyor; seçim kuralı; yeniden üretim uçtan uca;
e-posta taraması; kapı (ön kayıt yok -> durur).
Çalıştır:  python test_olcu_sinama.py   (ya da pytest -q test_olcu_sinama.py)
"""
from __future__ import annotations

import copy
import os
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import ORTAK_CETVEL as OC  # noqa: E402
import OLCU_SINAMA as OS  # noqa: E402


def _seri(n: int, tohum: int, bas: str = "2015-01-01", fiyat: float = 50.0, mu: float = 0.0003, sd: float = 0.02) -> pd.DataFrame:
    rng = np.random.default_rng(tohum)
    r = rng.normal(mu, sd, n)
    C = fiyat * np.exp(np.cumsum(r))
    O = np.r_[C[0], C[:-1]] * (1 + rng.normal(0, 0.005, n))
    H = np.maximum(O, C) * (1 + np.abs(rng.normal(0, 0.008, n))) + 1e-6
    L = np.minimum(O, C) * (1 - np.abs(rng.normal(0, 0.008, n)))
    V = rng.lognormal(np.log(2e5), 0.6, n)
    ix = pd.bdate_range(bas, periods=n)
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V, "Kur": 1.0}, index=ix)
    bos = rng.choice(np.arange(200, n), size=6, replace=False)
    d.iloc[bos, d.columns.get_loc("Volume")] = 0.0
    return d


def _ham(pazar: str, n_hisse: int, tohum: int, n: int = 2350) -> dict:
    rng = np.random.default_rng(tohum)
    H = {f"S{pazar[0]}{i:03d}": _seri(n, tohum * 1000 + i, fiyat=float(10 + i), sd=float(rng.uniform(0.01, 0.04))) for i in range(n_hisse)}
    # geç halka arz (2022-03; 2022-06-30'da < 80 bar) + seyrek hisse + 2:1 bölünme (kalıcı) + geri dönen sıçrama
    H[f"S{pazar[0]}IPO"] = _seri(450, tohum * 1000 + 901, bas="2022-03-01")
    sp = _seri(n, tohum * 1000 + 902)
    k = sp.index.get_loc(sp.index[1500])
    sp.iloc[k:, :4] = sp.iloc[k:, :4] / 2.0
    sp.iloc[k, :4] = sp.iloc[k - 1, :4].to_numpy() / 2.0 * np.array([1.0, 1.001, 0.999, 1.0])   # tam 2:1 oran
    H[f"S{pazar[0]}SPL"] = sp
    rv = _seri(n, tohum * 1000 + 903)
    a = 1800
    rv.iloc[a:a + 4, :4] = rv.iloc[a:a + 4, :4] * 1.5
    H[f"S{pazar[0]}REV"] = rv
    sy = _seri(n, tohum * 1000 + 904)
    H[f"S{pazar[0]}SEY"] = sy.iloc[::7]
    return H


def _vd(pazar: str, n_hisse: int, tohum: int, kesik=None) -> dict:
    V = _ham(pazar, n_hisse, tohum)
    if kesik is not None:
        V = {s: d[d.index <= pd.Timestamp(kesik)] for s, d in V.items()}
        V = {s: d for s, d in V.items() if len(d)}
    Vd = OC._oc_veri_sar(V, pazar); Vd["kesik"] = None if kesik is None else str(kesik)
    for s, d in Vd["V"].items():
        bad = ((d.Open > d.High) | (d.Open < d.Low)).to_numpy()
        if bad.any():
            d = d.copy(); d.loc[bad, "Open"] = np.clip(d.Open.to_numpy(float), d.Low.to_numpy(float), d.High.to_numpy(float))[bad]
            Vd["V"][s] = d
    return Vd


_PN: dict = {}


def _pn(pazar: str = "ABD", n_hisse: int = 70) -> dict:
    k = (pazar, n_hisse)
    if k not in _PN:
        _PN[k] = OS.os_panel(_vd(pazar, n_hisse, 7 if pazar == "ABD" else 11))
    return _PN[k]


# ------------------------------------------------------------------ çakışma kapısı
def test_cakisma_kapisi():
    kaynak = open(os.path.join(KOK, "OLCU_SINAMA.py"), encoding="utf-8").read()
    ns = {"__name__": "os_test"}
    exec(compile(kaynak, "OLCU_SINAMA.py", "exec"), ns)
    exec(compile(kaynak, "OLCU_SINAMA.py", "exec"), ns)          # aynı dosya yeniden: geçer
    ns2 = {"__name__": "os_test", "os_panel": "başka modülün adı", "_CK_KAYIT": {}}
    try:
        exec(compile(kaynak, "OLCU_SINAMA.py", "exec"), ns2)
    except RuntimeError as ex:
        assert "EZDİ" in str(ex)
    else:
        raise AssertionError("çakışma kapısı başka modülün adını ezmeye izin verdi")


# ------------------------------------------------------------------ nedensel bölünme
def test_bolunme_nedensel():
    for ad in ("SASPL", "SAREV"):
        Vd = _vd("ABD", 3, 7)
        s = ad.replace("SA", "SA")
        d = Vd["V"][s]; idx = d.index; n = len(idx); pos = np.arange(n); C = d.Close.to_numpy(float)
        yeni = OS.os_bolunme_disi(pos, C, n)
        sj = OC.oc_bolunme_supheli(C)                 # tam bilgi (C[i+10]) ORTAK_CETVEL kuralı
        cs = np.r_[0, np.cumsum(sj)]; dd = np.arange(n)
        eski = (cs[np.clip(dd, 0, n)] - cs[np.clip(dd - 61, 0, n)]) > 0   # [d-61, d-1]
        assert not (eski & ~yeni).any(), f"{s}: nedensel kural tam bilgi kuralının üst kümesi değil"
        a, k = OS.os_bolunme_aday(C)
        assert len(a) >= 1
        for i in a:   # sıçrama sonrası 10 bar bekleme: hep havuz dışı
            assert yeni[i + 1:i + 11].all()
        # veri sıçramadan 3 bar sonra kesilince önek aynı
        i0 = int(a[0]); m = i0 + 4
        kisa = OS.os_bolunme_disi(pos[:m], C[:m], m)
        assert np.array_equal(kisa, yeni[:m]), f"{s}: kesik önek farklı"
    a, k = OS.os_bolunme_aday(_vd("ABD", 3, 7)["V"]["SASPL"].Close.to_numpy(float))
    assert 1 in k                                       # 2:1 kalıcı
    a, k = OS.os_bolunme_aday(_vd("ABD", 3, 7)["V"]["SAREV"].Close.to_numpy(float))
    assert 0 in k                                       # geri dönen 1,5x: kalıcı değil


def test_evren_80_bar():
    Pn = _pn()
    j = Pn["kol"]["SAIPO"]; gec = Pn["gec"][:, j]
    k80 = np.flatnonzero(gec)[79]
    assert not Pn["evren"][:k80 + 1, j].any() and Pn["evren"][k80 + 1:, j].all()
    assert not Pn["ok"][:k80 + 1, j].any()


# ------------------------------------------------------------------ ölçüler = düz döngü
def _duz(Pn, d, j, H, delta=0.0):
    dep = Pn["dep"]; a, b = dep["off"][j], dep["off"][j + 1]
    O, Hh, L, C, pos = dep["O"][a:b], dep["H"][a:b], dep["L"][a:b], dep["C"][a:b], dep["POS"][a:b]
    e = int(np.flatnonzero(pos == d)[0])
    if e + H - 1 >= len(O) or pos[e + H - 1] - pos[e] > 2 * H - 1:
        return None
    tr = []
    for i in range(e - 14, e):
        pc = C[i - 1] if i >= 1 else np.nan
        tr.append(max(Hh[i], pc) - min(L[i], pc) if np.isfinite(pc) else Hh[i] - L[i])
    atr = np.mean(tr) / C[e - 1]; E0 = O[e]; mx, mn = -1e9, 1e9; up, dn = E0 * (1 + 1.5 * atr), E0 * (1 - 1.5 * atr); o5 = None
    for k in range(H):
        f = 1 + delta * (k + 1) / H
        hh, ll = Hh[e + k] * f, L[e + k] * f
        mx, mn = max(mx, hh), min(mn, ll)
        if o5 is None:
            if ll <= dn:
                o5 = 0.0
            elif hh >= up:
                o5 = 1.0
    return {"R": C[e + H - 1] * (1 + delta) / E0 - 1, "T5": float(mx >= 1.05 * E0), "T10": float(mx >= 1.10 * E0),
            "A": ((mx - E0) - (E0 - mn)) / (E0 * atr), "O5": 0.0 if o5 is None else o5}


def test_olcu_duz_dongu_ve_surukleme():
    Pn = _pn(); rng = np.random.default_rng(3)
    for H in (15, 60):
        Ms = OS.os_olcu_matris(Pn, H)
        dd, jj = np.nonzero(np.isfinite(Ms["A"]))
        for i in rng.choice(len(dd), 40, replace=False):
            el = _duz(Pn, dd[i], jj[i], H)
            for k in OS.OS_KAYNAK:
                assert abs(el[k] - Ms[k][dd[i], jj[i]]) < 1e-12, (H, k)
        sec = rng.choice(len(dd), 30, replace=False); d, j = dd[sec], jj[sec]; e = Pn["EIX"][d, j]
        x0 = OS.os_olcu_hesap(Pn["dep"], j, e, H, 0.0)
        for k in OS.OS_KAYNAK:
            assert np.allclose(x0[k], Ms[k][d, j], equal_nan=True)
        x2 = OS.os_olcu_hesap(Pn["dep"], j, e, H, 0.02)
        assert np.allclose(x2["R"], (1 + x0["R"]) * 1.02 - 1)
        assert (x2["T5"] >= x0["T5"]).all() and (x2["A"] > x0["A"]).all()
        for i in range(10):
            el = _duz(Pn, d[i], j[i], H, 0.02)
            for k in OS.OS_KAYNAK:
                assert abs(el[k] - x2[k][i]) < 1e-12, ("sürük", H, k)


# ------------------------------------------------------------------ eş = kaba kuvvet
def test_es_kaba_kuvvet():
    Pn = _pn(); Ms = OS.os_olcu_matris(Pn, 30); rng = np.random.default_rng(5)
    for kv in OS.OS_KOVA:
        KV = Pn[kv]; X = Ms["R"]; hv = OS.os_havuz(X, KV)
        dd, jj = np.nonzero((KV >= 0) & np.isfinite(X))
        sec = rng.choice(len(dd), 60, replace=False); d, j = dd[sec], jj[sec]
        exc = rng.choice(len(dd), 3000, replace=False); ed, ej = dd[exc], jj[exc]
        x = X[d, j] + rng.normal(0, 0.01, len(d))
        e = OS.os_es(hv, d, j, x, ed, ej)
        ex = set(zip(ed.tolist(), ej.tolist())) | set(zip(d.tolist(), j.tolist()))
        for i in range(len(d)):
            m = [jj2 for jj2 in range(KV.shape[1]) if KV[d[i], jj2] == KV[d[i], j[i]] and np.isfinite(X[d[i], jj2]) and (d[i], jj2) not in ex]
            r = X[d[i], m]
            if len(m) < 5:
                assert np.isnan(e["es"][i]); continue
            assert abs(e["es"][i] - r.mean()) < 1e-12 and e["n_es"][i] == len(m)
            assert abs(e["sira"][i] - ((r < x[i]).sum() + 0.5 * (r == x[i]).sum()) / len(m)) < 1e-12


# ------------------------------------------------------------------ hücre
def test_hucre():
    rng = np.random.default_rng(1); ay = np.repeat(np.arange(48), 50)
    c = OS.os_hucre(rng.normal(0.02, 0.05, len(ay)), ay, "+", perm=True)
    assert c["tutar_p"] and not c["tutar_n"] and c["p"] < 0.01 and c["boot_alt"] > 0 and c["l3o_p"] > 0
    c = OS.os_hucre(rng.normal(-0.02, 0.05, len(ay)), ay, "-", perm=True)
    assert c["tutar_n"] and not c["tutar_p"] and c["p"] < 0.01
    c = OS.os_hucre(rng.normal(0, 0.05, 20), ay[:20], "+")
    assert not c["tutar_p"] and c["n"] == 20                   # n < 30


# ------------------------------------------------------------------ kartlar
def test_kart_sinyal():
    Pn = _pn(); X = OS.os_kart_sinyal(Pn)
    g = X[X.havuz & np.isfinite(X.MOM)].groupby("tarih")
    pay = (g.MOM_ust.sum() / g.size()); pay = pay[g.size() >= 30]
    assert len(pay) > 20 and abs(pay.mean() - 0.10) < 0.03
    assert not (X.MOM_ust & X.MOM_alt).any() and not X.MOM_ust[~X.havuz].any()
    dep = Pn["dep"]; r = X[np.isfinite(X.MOM) & np.isfinite(X.HIGH52)].iloc[5]; j = int(r.j); a = dep["off"][j]
    C = dep["C"][a:dep["off"][j + 1]]; Hh = dep["H"][a:dep["off"][j + 1]]; k = int(r.k)
    assert abs(r.MOM - (C[k - 21] / C[k - 252] - 1)) < 1e-12 and abs(r.STREV - (C[k] / C[k - 21] - 1)) < 1e-12
    assert abs(r.HIGH52 - C[k] / Hh[k - 251:k + 1].max()) < 1e-12
    assert Pn["tarih"][int(r.d)] > r.tarih and int(r.d) == dep["POS"][a + k + 1]          # giriş = t'den sonraki ilk geçerli bar
    U, T = OS.os_bacak_olay(X, "MOM+", 60)
    for s, gg in T.groupby("sembol"):
        assert (np.diff(np.sort(gg.d.to_numpy())) >= 60).all()


# ------------------------------------------------------------------ prefix
def test_prefix_sentetik():
    Vu = _vd("ABD", 70, 7); Pu = OS.os_panel(Vu)
    Vk = _vd("ABD", 70, 7, kesik="2022-06-30"); Pk = OS.os_panel(Vk, Pu["sinir"])
    r = OS.os_prefix(Pk, Pu)
    assert r["tutar"] and r["toplam_fark"] == 0, r
    assert sum(v["n_kisa"] for v in r["olay"].values()) > 100
    # ORTAK_CETVEL min_bar kuralıyla (veri sonuna kadar bar sayısı) IPO hissesi kısa veride düşer; bizde evren önekte aynı
    assert "SAIPO" in Pk["kol"]
    # bozulunca yakalar
    Pk2 = dict(Pk); Pk2["ok"] = Pk["ok"].copy(); dd, jj = np.nonzero(Pk2["ok"][:100]); Pk2["ok"][dd[0], jj[0]] = False
    assert not OS.os_prefix(Pk2, Pu)["tutar"]


# ------------------------------------------------------------------ uçtan uca (görev, seçim, yeniden üretim)
def test_uctan_uca_sentetik():
    Y0 = copy.deepcopy(OS.OS_ESIK["yapay"])
    tmp = tempfile.mkdtemp(prefix="os_test_")
    try:
        OS.OS_ESIK["yapay"]["tohum_sayi"] = 3
        OS._OS_IS["P"], OS._OS_IS["X"] = {}, {}; OS._OS_IS["plasebo_T"] = 4
        for p, t in (("ABD", 7), ("AVR", 11)):
            V = _ham(p, 300, t)
            pd.to_pickle(V, os.path.join(tmp, f"V_{p}.pkl"))
            P = OS.os_panel(_vd(p, 300, t)); P["pazar"] = p
            OS._OS_IS["P"][p] = P; OS._OS_IS["X"][p] = OS.os_kart_sinyal(P)
        S = [OS._os_gorev((p, H)) for H in OS.OS_ESIK["ufuk"] for p in ("ABD", "AVR")]
        hucre = pd.DataFrame([h for s in S for h in s["hucre"]]); pl = pd.DataFrame([h for s in S for h in s["plasebo"]])
        sd = pd.DataFrame([h for s in S for h in s["plasebo_sd"]]); ya = pd.DataFrame([h for s in S for h in s["yapay"]])
        assert set(hucre.bacak) == set(OS.OS_BACAK) and set(hucre.olcu) == set(OS.OS_OLCU) and len(hucre) == 5 * 6 * 2 * 2 * 2 * 3
        # plasebo ortalama fark ~0 (O1)
        m = pl[pl.olcu == "O1"].fark.mean()
        assert abs(m) < 0.01, m
        # yapay iz: +%5 n 1000 (ölçülebilirse) R farkı yakalanır
        yy = ya[(~ya.olculmedi.astype(bool)) & (ya.olcu == "O1") & (ya.delta == 0.05)]
        assert len(yy) and yy.groupby("n_hedef").yakala.mean().max() >= 0.6
        g = pl.groupby(["pazar", "H", "kova", "olcu", "donem"])
        plo = g.agg(fark_ort=("fark", "mean"), pay_p=("tutar_p", "mean"), pay_n=("tutar_n", "mean")).reset_index().merge(sd)
        plo["gecti"] = (plo.fark_ort.abs() < 0.03 * plo.sd) & (plo.pay_p <= 0.07) & (plo.pay_n <= 0.07)
        yo = ya[~ya.olculmedi.astype(bool)].groupby(["pazar", "H", "donem", "n_hedef", "delta", "kova", "olcu"]).agg(
            yakala_pay=("yakala", "mean")).reset_index()
        sec = OS.os_secim(hucre, plo, yo)
        assert len(sec["tablo"]) == 36
        for s in S:
            s["satir"].to_csv(OS._os_yol("kart", tmp, p=s["pazar"], h=s["H"]), index=False, compression={"method": "gzip", "mtime": 0})
        Yr = OS.os_yeniden({"kart_hucre": hucre.to_dict("records")}, veri=tmp, cikti=tmp)
        assert Yr["tutar"] and Yr["olay_n"] == 30, Yr
    finally:
        OS.OS_ESIK["yapay"] = Y0
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ süreç
def test_eposta_ve_kapi():
    tmp = tempfile.mkdtemp(prefix="os_test_")
    try:
        try:
            OS._os_yaz(os.path.join(tmp, "x.md"), "iletisim: birisi" + "@" + "ornek.com", "deneme")
        except OS.OSHata:
            pass
        else:
            raise AssertionError("e-posta deseni yazıldı")
        try:
            OS.os_kapi(onkayit=os.path.join(tmp, "yok.md"))
        except OS.OSHata as ex:
            assert "ön kayıt yok" in str(ex)
        else:
            raise AssertionError("ön kayıtsız kapı açıldı")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    assert OS.os_esik_sha() == OS.os_esik_sha(copy.deepcopy(OS.OS_ESIK))


if __name__ == "__main__":
    import time as _t
    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)
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
