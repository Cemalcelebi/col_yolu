"""test_tezgah2_dogrulama — TEZGAH2_DOGRULAMA.py mekanik denetimleri (sentetik veri; gerçek veri / sonuç görülmez, ağ isteği yok).

Kapsam: çakışma kapısı; sıçra-geri dön (P3) nedensel dışlama aralığı; P1 / P2 / P3 iç içe ve eşikler; evren prefix testi P1-P3 dahil
(tutar, bozulunca yakalar); seriler = TD serileri (havuz = P1); dönem pencereli karşılaştırma; havuz seçim kuralı (tam / yedek / eşitlik);
FRED ayrıştırma; eş-farkı SD kaba kuvvetle; yeniden üretim düz pandas tutar; e-posta taraması; kapı (ön kayıt yok -> durur); sha.
Çalıştır:  python test_tezgah2_dogrulama.py
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
import TEZGAH2_DOGRULAMA as T2  # noqa: E402
import TEZGAH_DOGRULAMA as TD  # noqa: E402
import OLCU_SINAMA as OS  # noqa: E402
import test_olcu_sinama as TOS  # noqa: E402  (yalnız sentetik veri üreticisi)

_C: dict = {}


def _panel():
    if "Pn" not in _C:
        Vd = TOS._vd("ABD", 70, 7); Pn = OS.os_panel(Vd); Pn["pazar"] = "ABD"
        _C.update({"Vd": Vd, "Pn": Pn, "M": T2.t2_havuz(Pn, Vd)})
    return _C["Vd"], _C["Pn"], _C["M"]


# ------------------------------------------------------------------ çakışma kapısı
def test_cakisma_kapisi():
    kaynak = open(os.path.join(KOK, "TEZGAH2_DOGRULAMA.py"), encoding="utf-8").read()
    ns = {"__name__": "t2_test"}
    exec(compile(kaynak, "TEZGAH2_DOGRULAMA.py", "exec"), ns)
    exec(compile(kaynak, "TEZGAH2_DOGRULAMA.py", "exec"), ns)          # aynı dosya yeniden: geçer
    ns2 = {"__name__": "t2_test", "t2_secim": "başka modülün adı", "_CK_KAYIT": {}}
    try:
        exec(compile(kaynak, "TEZGAH2_DOGRULAMA.py", "exec"), ns2)
    except RuntimeError as ex:
        assert "EZDİ" in str(ex)
    else:
        raise AssertionError("çakışma kapısı başka modülün adını ezmeye izin verdi")


# ------------------------------------------------------------------ P3 sıçra-geri dön
def test_sicra_geri_nedensel():
    m = 700; CK = np.full(m, 10.0); CK[300] = 16.0; CK[301] = 12.0           # +%60, ertesi bar 4 / 6 geri
    pos = np.arange(m) * 2; n = 2 * m + 3                                     # birleşik takvimde bar arası bir boş satır
    out = T2.t2_sg_disi(pos, CK, n)
    assert not out[:pos[301] + 1].any()                                       # onay barı (301) ve öncesi dışlanmaz
    assert out[pos[301] + 1:pos[550] + 1].all() and not out[pos[550] + 1:].any()   # nb(d) in [302, 550]
    # geri dönüş 3 bar içinde değil -> olay yok
    C2 = np.full(m, 10.0); C2[300:304] = 16.0; C2[304] = 10.0
    assert not T2.t2_sg_disi(pos, C2, n).any()
    # yarıdan az geri -> olay yok; aşağı sıçrama + yukarı dönüş -> olay
    C3 = np.full(m, 10.0); C3[300:] = 16.0; C3[301:] = 14.0
    assert not T2.t2_sg_disi(pos, C3, n).any()
    C4 = np.full(m, 10.0); C4[300:302] = 4.0; C4[302:] = 9.0
    o4 = T2.t2_sg_disi(pos, C4, n); assert o4[pos[302] + 1] and not o4[pos[302]]
    # nedensel: veri onay barından önce kesilirse olay yok; pencere veri sonunu aşarsa sona kadar
    assert not T2.t2_sg_disi(pos[:301], CK[:301], n).any()
    o5 = T2.t2_sg_disi(pos[:400], CK[:400], n); assert o5[pos[301] + 1:].all()


# ------------------------------------------------------------------ havuzlar
def test_havuz_ic_ice_ve_esik():
    Vd, Pn, M = _panel()
    assert (M["P1"] == (Pn["ok"] & (Pn["H"] >= 0))).all()
    assert not (M["P2"] & ~M["P1"]).any() and not (M["P3"] & ~M["P2"]).any() and M["P2"].sum() > 1000
    # tek hücre elle: d günü P2 <=> P1 ve d'den önceki son kapanış >= 2 ve Lq >= 1e6
    dd, jj = np.nonzero(M["P1"]); i = len(dd) // 2; d, j = dd[i], jj[i]
    s = Pn["sembol"][j]; x = Vd["V"][s]; once = x[x.index < Pn["tarih"][d]]
    beklenen = bool(once.Close.iloc[-1] * once.Kur.iloc[-1] >= 2.0 and Pn["Lq"][d, j] >= 1e6)
    assert bool(M["P2"][d, j]) == beklenen
    E = copy.deepcopy(T2.T2_ESIK); E["havuz"]["fiyat_min"]["ABD"] = 1e9
    assert T2.t2_havuz(Pn, Vd, E)["P2"].sum() == 0
    # sayım
    S = T2.t2_sayim(Pn, M)
    assert S["havuz"]["P1"]["hisse_gun_toplam"] == int(M["P1"].sum())
    y = S["havuz"]["P2"]["yil"]["2020"]; assert 0 <= y["lik_ust_pay"] <= 1 and y["hisse"] <= len(Pn["sembol"])


def test_prefix_havuz():
    Vu, Pu, Mu = _panel()
    Vk = TOS._vd("ABD", 70, 7, kesik="2022-06-30"); Pk = OS.os_panel(Vk, Pu["sinir"]); Pk["pazar"] = "ABD"; Mk = T2.t2_havuz(Pk, Vk)
    r = T2.t2_prefix(Pk, Pu, Mk, Mu, son="2022-05-31")
    assert r["tutar"] and r["toplam_fark"] == 0, r
    assert r["havuz_kisa"]["P3"] > 1000
    Mk2 = dict(Mk); Mk2["P3"] = Mk["P3"].copy(); dd, jj = np.nonzero(Mk2["P3"][:100]); Mk2["P3"][dd[0], jj[0]] = False
    r2 = T2.t2_prefix(Pk, Pu, Mk2, Mu, son="2022-05-31")
    assert not r2["tutar"] and r2["havuz_fark"]["P3"] == 1


# ------------------------------------------------------------------ seriler, karşılaştırma, seçim
def _z():
    if "Z" not in _C:
        Vd, Pn, M = _panel()
        Z = TD.td_kesit(Pn, Vd, None)
        for hv in T2.T2_HAVUZ:
            Z[hv] = M[hv][Z.d.to_numpy(np.int64), Z.j.to_numpy(np.int64)]
        _C["Z"] = Z
    return _C["Z"]


def test_seriler_td_ile_ayni():
    Z = _z()
    assert (Z.havuz == Z.P1).all()
    S = T2.t2_seriler(Z, "ABD"); St = TD.td_bizim_seriler(Z, "ABD")
    for k in ("PIYASA|-|EW", "PIYASA|-|LQ", "MOM|2X3|LQ", "MOM|D10-D1|EW", "STREV|2X3|LQ", "STREV|D1-D10|LQ"):
        a, b = S[f"ABD|P1|r|{k}"], St[f"ABD|havuz|r|{k}"]
        assert np.allclose(a.to_numpy(), b.to_numpy(), equal_nan=True) and a.index.equals(b.index), k
        a2, b2 = S[f"ABD|tum|r|{k}"], St[f"ABD|tum|r|{k}"]
        assert np.allclose(a2.to_numpy(), b2.to_numpy(), equal_nan=True), k
    assert "ABD|P3|r|MOM|2X3|LQ" in S


def test_karsilastir_donem():
    ix = pd.period_range("2000-01", "2023-12", freq="M"); rng = np.random.default_rng(4)
    R = {r: pd.Series(rng.normal(0.005, 0.04, len(ix)), index=ix) for r in {c[2] for c in TD.TD_CIFT}}
    S = {}
    for hv in T2.T2_HAVUZ:
        for k, b, r, p, a in TD.TD_CIFT:
            S[b.replace("|havuz|", f"|{hv}|")] = R[r] * 1.1 + (0 if hv != "P3" else rng.normal(0, 0.2, len(ix)))
    K = T2.t2_karsilastir(S, R)
    c = [x for x in K if x["havuz"] == "P1" and x["kod"] == "A5"][0]
    assert c["donem"]["d1"]["n"] == 84 and c["donem"]["d2"]["n"] == 96 and c["donem"]["d3"]["n"] == 96 and c["donem"]["tum"]["n"] == 282
    assert c["donem"]["d1"]["ilk"] == "2001-01" and c["donem"]["d3"]["son"] == "2023-12" and c["donem"]["d2"]["hukum"] == "DOĞRU"
    SEC = T2.t2_secim(K)
    assert SEC["secilen"] == "P1" and SEC["tam_gecen"] == ["P1", "P2"] and SEC["tablo"]["P3"]["dogru"] < 21
    assert "geniş tezgâh (P1)" in T2.t2_sonuc(K, "P1")


def _k(dogru: dict) -> list:
    """dogru: havuz -> DOĞRU olmayan (kod, dönem) kümesi."""
    K = []
    for hv in T2.T2_HAVUZ:
        for k, *_ in TD.TD_CIFT:
            K.append({"havuz": hv, "kod": k, "donem": {d: {"hukum": "KISMEN" if (k, d) in dogru[hv] else "DOĞRU", "pearson": 0.5, "isaret": 0.6}
                                                       for d in ("tum", "d1", "d2", "d3")}})
    return K


def test_secim_kurali():
    assert T2.t2_secim(_k({"P1": set(), "P2": set(), "P3": set()}))["secilen"] == "P1"
    s = T2.t2_secim(_k({"P1": {("A5", "d1")}, "P2": set(), "P3": set()}))
    assert s["secilen"] == "P2" and s["yol"].startswith("tam")
    # onluk farkı (A3) ve 'tum' dönemi seçime girmez
    assert T2.t2_secim(_k({"P1": {("A3", "d1"), ("A5", "tum")}, "P2": set(), "P3": set()}))["secilen"] == "P1"
    s = T2.t2_secim(_k({"P1": {("A5", "d1"), ("E3", "d2")}, "P2": {("A1", "d1")}, "P3": {("A8", "d3")}}))
    assert s["secilen"] == "P2" and s["yol"].startswith("yedek") and s["tablo"]["P2"]["dogru"] == 20
    s = T2.t2_secim(_k({"P1": {("A5", "d1")}, "P2": {("A1", "d1")}, "P3": {("A8", "d3"), ("A1", "d2")}}))
    assert s["secilen"] == "P1"                                              # eşitlikte geniş olan


# ------------------------------------------------------------------ FRED
def test_fred_ayristir():
    m = "observation_date,DEXUSEU\n2003-05-29,1.1700\n2003-05-30,.\n2003-06-02,1.1800\n"
    x = T2.t2_fred_ayristir(m)
    assert len(x) == 2 and x.index[-1] == pd.Timestamp("2003-06-02") and abs(x.iloc[0] - 1.17) < 1e-12
    for bozuk in ("DATE,XYZ\n2003-05-29,1.1\n", "observation_date,DEXUSEU\n29/05/2003,1.1\n"):
        try:
            T2.t2_fred_ayristir(bozuk)
        except T2.T2Hata:
            pass
        else:
            raise AssertionError("FRED bozuk girdi kabul edildi")


# ------------------------------------------------------------------ eş-farkı SD
def test_es_sd_kaba_kuvvet():
    Vd, Pn, M = _panel()
    E = copy.deepcopy(T2.T2_ESIK)
    R = T2.t2_es_sd(Pn, M["P2"], 15, E)
    d3 = [r for r in R if r["donem"] == "d3"][0]
    assert d3["n"] > 1000 and np.isfinite(d3["sd"]) and d3["sd"] > 0
    X = OS.os_olcu_matris(Pn, 15)["R"]; KV = np.where(M["P2"], Pn["KV1"], -1)
    f = []
    for d in range(len(Pn["tarih"])):
        if Pn["tarih"][d].year < 2016:
            continue
        for kv in np.unique(KV[d][KV[d] >= 0]):
            g = np.flatnonzero((KV[d] == kv) & np.isfinite(X[d]))
            if len(g) - 1 < 5:
                continue
            x = X[d, g]; f += list(x - (x.sum() - x) / (len(x) - 1))
    f = np.array(f)
    assert len(f) == d3["n"] and abs(f.std(ddof=1) - d3["sd"]) < 1e-12 and abs(f.mean() - d3["ort"]) < 1e-12


# ------------------------------------------------------------------ yeniden üretim (düz pandas)
def test_yeniden_duz():
    tmp = tempfile.mkdtemp(prefix="t2_test_")
    try:
        pd.to_pickle(TOS._ham("ABD", 40, 5), os.path.join(tmp, "V_ABD.pkl"))
        Vd = OS.os_veri("ABD", tmp); Pn = OS.os_panel(Vd); Pn["pazar"] = "ABD"; M = T2.t2_havuz(Pn, Vd)
        Z = TD.td_kesit(Pn, Vd, None)
        for hv in T2.T2_HAVUZ:
            Z[hv] = M[hv][Z.d.to_numpy(np.int64), Z.j.to_numpy(np.int64)]
        S = T2.t2_seriler(Z, "ABD", ["P1", "tum"])
        J = {"seriler": T2._t2_seri_json(S), "ref_seriler": {}}
        Y = T2.t2_yeniden(J, veri=tmp, aylar=["2017-03", "2020-04", "2023-06"])
        assert len(Y["satir"]) == 6 and all(x["tutar"] for x in Y["satir"]), Y["satir"]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ e-posta, kapı, sha
def test_eposta_kapi_sha():
    tmp = tempfile.mkdtemp(prefix="t2_test_")
    try:
        try:
            T2._t2_yaz(os.path.join(tmp, "x.md"), "iletişim: ornek@ornek.com")
        except T2.T2Hata as ex:
            assert "e-posta" in str(ex)
        else:
            raise AssertionError("e-posta taraması çalışmadı")
        try:
            T2.t2_kapi(onkayit=os.path.join(tmp, "yok.md"))
        except T2.T2Hata as ex:
            assert "ön kayıt yok" in str(ex)
        else:
            raise AssertionError("ön kayıtsız kapı açıldı")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    assert T2.t2_esik_sha() == T2.t2_esik_sha(copy.deepcopy(T2.T2_ESIK))
    assert set(T2.T2_KONTROL) == {f"K{i}" for i in range(1, 15)}
    assert "P1 = OLCU_SINAMA havuzu olduğu gibi" in T2.T2_ESIK["havuz"]["metin"] and "EN GENİŞ" in T2.T2_ESIK["secim"]["metin"]


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
