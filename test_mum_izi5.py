"""test_mum_izi5 — MUM_IZI_V3 testleri (gerçek fiyat verisi ve işaret dosyası yok): şablonun kendine uzaklığı 0, vektör / düz döngü eşitliği (K11),
yeniden örnekleme, bant koordinatı, geleceğe bakmama (seri t'de kesilince aynı sonuç; K2), tekil küme, AUC / tam permütasyon p, işaret
ayrıştırıcı, eksik haftalı pencere, telafi yasağı, çakışma kapısı.
Çalıştır: python test_mum_izi5.py"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

import MUM_IZI as MI
import MUM_IZI_V3 as V3


def _seri(n=400, tohum=3):
    rng = np.random.default_rng(tohum)
    lO, lH, lL, lC = MI.mi_uret(rng, n, None, "ry")
    return tuple(map(np.exp, (lO, lH, lL, lC)))


def _D():
    return {"tau": [0.3, 0.3, 0.3], "q20": [0.15, 0.2, 0.2]}


def test_sablon_kendine_sifir():
    S = V3.v3_sablon(); a = S["ohlc"]
    F = V3.v3_aileler(V3.v3_ozet(a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"]), S["Z"])
    assert all(abs(float(f[0])) < 1e-12 for f in F), F
    assert bool(V3.v3_aday(*F, _D())[0]) and abs(float(V3.v3_D3(*F, _D())[0])) < 1e-12


def test_vektor_duz_ayni():
    S = V3.v3_sablon(); O, H, L, C = _seri(); BU, BO, BA = MI.mi_bant(C)
    for e, m in ((60, 16), (120, 18), (200, 20), (250, 22), (330, 24), (399, 17)):
        sl = slice(e - m + 1, e + 1); W = {"O": O[sl], "H": H[sl], "L": L[sl], "C": C[sl], "BU": BU[sl], "BO": BO[sl]}
        Fv = [float(f[0]) for f in V3.v3_aileler(V3.v3_ozet(W["O"], W["H"], W["L"], W["C"], W["BU"], W["BO"]), S["Z"])]
        Fd = [float(x) for x in V3.v3_duz(W, S)]
        assert np.allclose(Fv, Fd, atol=1e-12), (e, m, Fv, Fd)


def test_yeniden_ornekleme():
    x = np.arange(20.0)[None, :]
    assert np.allclose(V3._lin(x, 20), x)
    y = np.linspace(0, 1, 16)[None, :]
    assert np.allclose(V3._lin(y, 20), np.linspace(0, 1, 20)[None, :])
    z = np.array([[0.0, 1.0, 0.0, 1.0]])
    assert set(np.unique(V3._yakin(z, 20))) <= {0.0, 1.0}


def test_bant_koordinati():
    C = np.full(5, 10.0); O = C.copy(); BU = np.full(5, 12.0); BO = np.full(5, 10.0)
    Z = V3.v3_ozet(O, C + 2, C - 2, C, BU, BO)
    assert np.allclose(Z["seq"][0, :, 0], 0) and np.allclose(Z["seq"][0, :, 2], 1) and np.allclose(Z["seq"][0, :, 3], -1)
    Z2 = V3.v3_ozet(O, C + 2, C - 2, C, BO, BO)                 # üst bant = SMA -> geçersiz
    assert not bool(Z2["gecerli"][0])


def test_gelecege_bakmama():
    S = V3.v3_sablon(); O, H, L, C = _seri(500, 7); D = _D()
    R = V3.v3_tara_seri(O, H, L, C, S, D)
    for t in (80, 211, 333, 499):
        Rk = V3.v3_tara_seri(O[:t + 1], H[:t + 1], L[:t + 1], C[:t + 1], S, D)
        a, b = R["D3"][t], Rk["D3"][t]
        assert (np.isnan(a) and np.isnan(b)) or abs(a - b) < 1e-12, (t, a, b)
        assert bool(R["aday"][t]) == bool(Rk["aday"][t])


def test_tekil_kume():
    e = np.array([10, 12, 20, 40, 41, 80]); d3 = np.zeros(100); d3[[10, 12, 20, 40, 41, 80]] = [3, 2, 5, 1, 4, 9]
    assert V3.v3_tekil(e, d3, 15).tolist() == [12, 40, 80]
    assert V3.v3_tekil(np.array([], np.int64), d3).tolist() == []


def test_auc_perm():
    x = np.array([0.1, 0.2, 0.3, 1.0, 1.1, 1.2, 1.3]); y = np.array([1, 1, 1, 0, 0, 0, 0])
    assert abs(V3.v3_auc(x[y == 1], x[y == 0]) - 1.0) < 1e-12
    assert abs(V3.v3_perm_p(x, y) - 1 / 35) < 1e-12                 # C(7, 3) = 35
    assert abs(V3.v3_auc(np.array([1.0]), np.array([1.0])) - 0.5) < 1e-12
    rng = np.random.default_rng(5); x = rng.normal(size=12); y = np.r_[np.ones(4, int), np.zeros(8, int)]
    p = V3.v3_perm_p(x, y); assert 0 < p <= 1


def test_isaret_ayristirici():
    ornekler = [({"sayfalar": [{"sayfa": 3, "isaret": "benziyor"}, {"sayfa": 4, "isaret": "benzemiyor"}, {"sayfa": 5, "isaret": None}]}, 0),
                ({"3": "✓", "4": "✗", "5": ""}, 0), ({"isaretler": {"1": "BENZİYOR", "2": "x"}}, 2), ({"benziyor": [3], "benzemiyor": [4, 6], "isaretsiz": [5]}, 0)]
    for J, kay in ornekler:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(J, f, ensure_ascii=False); yol = f.name
        E = V3.v3_etiket_oku(yol); os.unlink(yol)
        bas = 3 - kay
        assert E[bas] == 1 and E[bas + 1] == 0, E


def test_eksik_hafta_penceresi():
    S = V3.v3_sablon(); O, H, L, C = _seri(200, 11); bos = np.zeros(200, bool); bos[100] = True
    R = V3.v3_tara_seri(O, H, L, C, S, _D(), bos)
    # 100. barda boşluk: pencere 2..m. barında boşluk olan sonlar (100 <= e <= 100 + m - 2) bütün uzunluklarda geçersiz
    assert np.isnan(R["D3"][100:115]).all()
    assert np.isfinite(R["D3"][140:200]).all()


def test_telafi_yasagi():
    D = _D(); F1 = np.array([0.0, 0.0, 0.5]); F2 = np.array([0.0, 0.9, 0.0]); F3 = np.array([0.0, 0.0, 0.0])
    assert V3.v3_aday(F1, F2, F3, D).tolist() == [True, False, False]
    assert not bool(V3.v3_aday(np.array([np.nan]), np.array([0.0]), np.array([0.0]), D)[0])


def test_esik_sha_sabit():
    assert V3.v3_esik_sha() == V3.v3_esik_sha(json.loads(json.dumps(V3.MV3_ESIK)))
    assert V3.MV3_ESIK["D3"]["agirlik"] == [0.5, 0.25, 0.25] and V3.MV3_ESIK["sinama"]["hukum"] == {"UYUMLU": 0.80, "KISMEN": 0.65}


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_V3 as M\nns = dict(vars(M))\nns['v3_auc'] = 1\nns['_CK_ONCE_V3'] = {'v3_auc': id(M.v3_auc)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_v3()')[0] + '_cakisma_kontrol_v3()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(V3.__file__)))
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
