"""test_mum_izi9 — MUM_IZI_V6 testleri: 12 ölçü vektörlü = düz döngü (K11), şablon ölçüleri (K3 / BB3 muaf), eşik ve kapı mantığı, geleceğe bakmama (K2),
etiket kümesi sayıları, karşı örneklerin kuruluşu, çakışma kapısı.
Çalıştır: python test_mum_izi9.py"""
import json
import os
import subprocess
import sys

import numpy as np

import MUM_IZI as MI
import MUM_IZI_V6 as V6


def _seri(n=500, tohum=3):
    rng = np.random.default_rng(tohum)
    return tuple(map(np.exp, MI.mi_uret(rng, n, None, "ry")))


def test_olcu_duz_ayni():
    O, H, L, C = _seri(); BU, BO, BA = MI.mi_bant(C); fark = 0; n = 0
    for e in range(100, 500, 13):
        for m, k in ((16, 5), (20, 8), (24, 12)):
            s = e - m + 1; o = V6.v6_olcu(O, H, L, C, BU, BO, BA, s, e, k)
            od = V6.v6_olcu_duz(list(O), list(H), list(L), list(C), list(BU), list(BO), list(BA), s, e, k); n += 1
            for a in V6.ADAY:
                if not ((np.isnan(o[a]) and np.isnan(od[a])) or abs(o[a] - od[a]) < 1e-9):
                    fark += 1
    assert fark == 0 and n > 50, fark


def test_sablon_olculeri():
    a = MI.mi_sablon_yukle(kalibre=False)["tam"]["ohlc"]
    o = V6.v6_olcu(a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], 0, 19, 10, sablon=True)
    assert np.isnan(o["K3"]) and np.isnan(o["BB3"]) and all(np.isfinite(o[x]) for x in ("K1", "K2", "K4", "D1", "D2", "D3", "D4", "BB1", "BB2", "BB4"))
    print("   şablon:", {k: round(v, 3) for k, v in o.items() if np.isfinite(v)})


def test_kapi_mantik():
    kapi = {"K": {"aday": "K1", "esik": 0.5, "yon": "kucuk"}, "D": {"aday": "D2", "esik": 0.6, "yon": "buyuk"}, "BB": {"aday": "BB4", "esik": 0.5, "yon": "ikili"}}
    assert V6.v6_gec({"K1": 0.4, "D2": 0.7, "BB4": 1.0}, kapi) == {"K": True, "D": True, "BB": True}
    assert V6.v6_gec({"K1": 0.6, "D2": 0.5, "BB4": 0.0}, kapi) == {"K": False, "D": False, "BB": False}
    assert V6.v6_gec({"K1": float("nan"), "D2": 0.7, "BB4": 1.0}, kapi)["K"] is False


def test_gelecege_bakmama():
    O, H, L, C = _seri(600, 9); kapi = {"K": {"aday": "K3", "esik": 9.0, "yon": "kucuk"}, "BB": {"aday": "BB3", "esik": 1.0, "yon": "kucuk"}}
    R = V6.v6_tara_seri(O, H, L, C, kapi)
    for t in (150, 333, 599):
        Rk = V6.v6_tara_seri(O[:t + 1], H[:t + 1], L[:t + 1], C[:t + 1], kapi)
        assert bool(R["VAR"][t]) == bool(Rk["VAR"][t]) and bool(R["v5M"][t]) == bool(Rk["v5M"][t])
        if R["VAR"][t]:
            assert all(abs(R["olcu"][t][a] - Rk["olcu"][t][a]) < 1e-12 or (np.isnan(R["olcu"][t][a]) and np.isnan(Rk["olcu"][t][a])) for a in V6.ADAY)


def test_karsi_ornekler():
    rng = np.random.default_rng(1); K = V6.v6_karsi(rng); a = MI.mi_sablon_yukle()["tam"]["ohlc"]
    assert set(K) == {"n1", "n2", "n5", "n8", "n10"} and np.allclose(K["n10"]["C"], a["C"])
    assert K["n8"]["C"][10] - K["n8"]["O"][10] > 5 * np.max(np.abs(np.asarray(a["C"]) - np.asarray(a["O"])))
    with np.errstate(all="ignore"):
        f = (K["n10"]["H"] - K["n10"]["L"]) / (np.asarray(a["H"]) - np.asarray(a["L"]))
    assert (f >= 0.5 - 1e-9).all() and (f <= 3 + 1e-9).all()


def test_etiket_kumesi():
    if not os.path.exists(V6.V6_YOL["isaret8"]):
        print("  (işaret dosyası yok: atlandı)"); return
    X = V6.v6_etiketler(); K = X[X.kume == "karar"]
    assert int((K.cemal == 1).sum()) == 6 and int((K.cemal == 0).sum()) == 18, (int((K.cemal == 1).sum()), int((K.cemal == 0).sum()))
    assert int((X.set == "set3").sum()) == 24


def test_esik_sabit():
    assert V6.V6_ESIK["pay"] == 0.05 and V6.V6_ESIK["puan_en_az"] == 0.15 and V6.V6_ESIK["dur_pay"] == 0.5 and len(V6.ADAY) == 12
    assert V6.v6_esik_sha() == V6.v6_esik_sha(json.loads(json.dumps(V6.V6_ESIK)))


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_V6 as M\nns = dict(vars(M))\nns['v6_gec'] = 1\nns['_CK_ONCE_V6'] = {'v6_gec': id(M.v6_gec)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_v6()')[0] + '_cakisma_kontrol_v6()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(V6.__file__)))
    assert "KAPALI" in r.stdout, (r.stdout, r.stderr[-500:])


if __name__ == "__main__":
    adlar = [k for k in list(globals()) if k.startswith("test_")]
    hata = 0
    for k in adlar:
        try:
            globals()[k](); print("GEÇTİ", k)
        except Exception as ex:   # her test ayrı raporlanır
            hata += 1; print("KALDI", k, type(ex).__name__, ex)
    print(f"{len(adlar) - hata} / {len(adlar)} geçti")
    sys.exit(1 if hata else 0)
