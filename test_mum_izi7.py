"""test_mum_izi7 — MUM_IZI_V4 testleri (gerçek fiyat verisi ve etiket yok): şablon dört parçadan geçer, sabit eşikler, vektörlü kural = düz döngü (K11),
dereceli puan eşikte 0,5, yapı yoksa VAR yok, karşı örneklerin düştüğü parça (görüntü bantlarıyla), geleceğe bakmama (K2), tekil küme, kappa,
etiket şeması, çakışma kapısı.
Çalıştır: python test_mum_izi7.py"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

import MUM_IZI as MI
import MUM_IZI_V4 as V4


def _seri(n=400, tohum=3):
    rng = np.random.default_rng(tohum)
    return tuple(map(np.exp, MI.mi_uret(rng, n, None, "ry")))


def test_sablon_gecer():
    S = V4.v4_sablon_denetim()
    assert S["VAR"] and S["k"] == 10 and all(S[e] for e in ("E1", "E2", "E3", "E4"))
    assert abs(S["deger"]["E4_pay"] - 0.5) < 1e-12 and abs(S["PUAN4"] - 0.5) < 1e-12      # şablon E4'te sınırda (önceden bilinen)


def test_sabit_esikler():
    E = V4.V4_ESIK
    assert (E["E1"]["bC_ort"], E["E2"]["ust_pay"], E["E3"]["icerden_pay"], E["E3"]["icerden_ust"], E["E3"]["govde_kat"], E["E3"]["spearman"],
            E["E3"]["son_bC"], E["E3"]["ortusme_kat"], E["E4"]["fitil_oran"], E["E4"]["pay"]) == (-0.3, 0.80, 0.80, 1.05, 1.5, 0.6, 0.6, 0.75, 0.30, 0.50)
    assert E["uzunluklar"] == list(range(16, 25)) and V4.v4_esik_sha() == V4.v4_esik_sha(json.loads(json.dumps(E)))


def test_vektor_duz_ayni():
    a = MI.mi_sablon_yukle(kalibre=False)["tam"]["ohlc"]; K = V4.v4_karsi(); fark = 0; n = 0
    for x in [a] + list(K.values()):
        W = {k: np.asarray(x[k] if k in x else a[k], float) for k in ("O", "H", "L", "C", "BU", "BO")}
        R = V4.v4_pencereler(*(W[k] for k in ("O", "H", "L", "C", "BU", "BO"))); d = V4.v4_duz(W)
        fark += int(bool(R["VAR"][0]) != bool(d["VAR"])); n += 1
    O, H, L, C = _seri(500, 5); BU, BO, _ = MI.mi_bant(C)
    for e in range(60, 500, 7):
        for m in (16, 19, 24):
            sl = slice(e - m + 1, e + 1); W = {"O": O[sl], "H": H[sl], "L": L[sl], "C": C[sl], "BU": BU[sl], "BO": BO[sl]}
            R = V4.v4_pencereler(*(W[k] for k in ("O", "H", "L", "C", "BU", "BO"))); d = V4.v4_duz(W); n += 1
            fark += int(bool(R["VAR"][0]) != bool(d["VAR"]))
            if d.get("yapi"):
                fark += sum(int(bool(R[x][0]) != bool(d[x])) for x in ("E1", "E2", "E3", "E4"))
    assert fark == 0 and n > 100, fark


def test_puan_esikte_yarim():
    assert abs(float(V4._g_ge(0.6, 0.6, 0.4)) - 0.5) < 1e-12 and abs(float(V4._g_le(-0.3, -0.3, 0.3)) - 0.5) < 1e-12
    assert abs(float(V4._g_ge(1.0, 0.6, 0.4)) - 1.0) < 1e-12 and float(V4._g_ge(0.1, 0.6, 0.4)) == 0.0 and float(V4._g_le(2.1, 1.5, 0.5)) == 0.0
    assert float(V4._g_ge(5.0, 0.6, 0.4)) == 1.0


def test_yapi_yoksa_yok():
    m = 20; C = np.linspace(100, 90, m); O = C + 0.1; H = O + 0.5; L = C - 0.2; BU = np.full(m, 105.0); BO = np.full(m, 100.0)
    R = V4.v4_pencereler(O, H, L, C, BU, BO)
    assert not R["yapi"][0] and not R["VAR"][0] and R["PUAN4"][0] == 0.0 and not R["E1"][0]


def test_karsi_ornek_dusen_parca():
    a = MI.mi_sablon_yukle(kalibre=False)["tam"]["ohlc"]; K = V4.v4_karsi()
    for n, x in K.items():
        R = V4.v4_pencereler(x["O"], x["H"], x["L"], x["C"], a["BU"], a["BO"])
        assert not R["VAR"][0], n
    R = V4.v4_pencereler(K["n8a"]["O"], K["n8a"]["H"], K["n8a"]["L"], K["n8a"]["C"], a["BU"], a["BO"]); assert not R["E2"][0]
    R = V4.v4_pencereler(K["n2"]["O"], K["n2"]["H"], K["n2"]["L"], K["n2"]["C"], a["BU"], a["BO"]); assert not R["E4"][0]


def test_gelecege_bakmama():
    O, H, L, C = _seri(500, 7); R = V4.v4_tara_seri(O, H, L, C)
    for t in (90, 233, 377, 499):
        Rk = V4.v4_tara_seri(O[:t + 1], H[:t + 1], L[:t + 1], C[:t + 1])
        assert bool(R["VAR"][t]) == bool(Rk["VAR"][t])
        a, b = R["PUAN4"][t], Rk["PUAN4"][t]; assert (np.isnan(a) and np.isnan(b)) or abs(a - b) < 1e-12
    Rs = V4.v4_tara_seri(O, H, L, C, sonlar=np.array([200, 201, 202]))
    assert np.allclose(Rs["PUAN4"][200:203], R["PUAN4"][200:203], equal_nan=True) and np.isnan(Rs["PUAN4"][199])


def test_tekil():
    e = np.array([10, 12, 20, 40, 41, 80]); p = np.zeros(100); p[[10, 12, 20, 40, 41, 80]] = [0.6, 0.7, 0.5, 0.9, 0.8, 0.55]
    assert V4.v4_tekil(e, p, 15).tolist() == [12, 40, 80]


def test_kappa():
    a = np.array([1, 1, 0, 0, 1, 0]); assert abs(V4.v4_kappa(a, a) - 1.0) < 1e-12
    b = np.array([1, 0, 1, 0]); c = np.array([1, 1, 0, 0]); assert abs(V4.v4_kappa(b, c)) < 1e-12
    assert np.isnan(V4.v4_kappa(np.ones(5, int), np.ones(5, int)))
    x = np.array([1, 1, 1, 0, 0, 0, 0, 0, 1, 0]); y = np.array([1, 1, 0, 0, 0, 0, 0, 1, 1, 0])     # po 0,8; pe 0,52 -> 0,5833
    assert abs(V4.v4_kappa(x, y) - (0.8 - 0.52) / 0.48) < 1e-12


def test_etiket_semasi():
    with tempfile.TemporaryDirectory() as d:
        y = os.path.join(d, "e.json")
        json.dump({"sayfalar": {"2": {"isaret": "EVET"}, "3": {"isaret": "hayır"}, "4": {"isaret": "IKISI"}}}, open(y, "w", encoding="utf-8"), ensure_ascii=False)
        E = V4.v4_etiket_oku(y); assert E[2] == (1, "EVET") and E[3] == (0, "HAYIR") and E[4] == (None, "IKISI")
        json.dump({"sayfalar": {"2": {"isaret": "benziyor"}}}, open(y, "w", encoding="utf-8"))
        try:
            V4.v4_etiket_oku(y); raise AssertionError("kabul etmemeliydi")
        except V4.V4Hata:
            pass


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_V4 as M\nns = dict(vars(M))\nns['v4_kappa'] = 1\nns['_CK_ONCE_V4'] = {'v4_kappa': id(M.v4_kappa)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_v4()')[0] + '_cakisma_kontrol_v4()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(V4.__file__)))
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
