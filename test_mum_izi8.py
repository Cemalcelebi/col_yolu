"""test_mum_izi8 — MUM_IZI_V5 testleri: şablon bütün parçalardan geçer, sabit eşikler ve aday kuralların bileşimi, vektörlü parçalar = düz döngü (K11),
Y sınırı (0,6 x m), seçim kuralı (VAR en az, 0,03 farkta az parçalı, kappa <= 0,20 DUR), negatifin kendi ölçüsü, geleceğe bakmama (K2), tekil (en yüksek S),
etiket eşlemesi sayısı (61 / 16), çakışma kapısı.
Çalıştır: python test_mum_izi8.py"""
import json
import os
import subprocess
import sys

import numpy as np

import MUM_IZI as MI
import MUM_IZI_V5 as V5


def _seri(n=400, tohum=3):
    rng = np.random.default_rng(tohum)
    return tuple(map(np.exp, MI.mi_uret(rng, n, None, "ry")))


def test_sablon_hepsi():
    a = MI.mi_sablon_yukle()["tam"]["ohlc"]
    P = V5.v5_parcalar(*(a[x] for x in ("O", "H", "L", "C", "BU", "BO", "BA")), S=True)
    assert int(P["k"][0]) == 10 and all(bool(P[p][0]) for p in V5.PARCA), {p: bool(P[p][0]) for p in V5.PARCA}
    assert all(bool(V5.v5_kural(P, r)[0]) for r in V5.KURAL) and abs(float(P["d_S"][0]) - 1.0) < 1e-9
    assert abs(float(P["d_m1"][0]) - 0.3785) < 1e-3 and abs(float(P["d_m2"][0]) - 0.2029) < 1e-3 and abs(float(P["d_m3"][0]) - 0.4186) < 1e-3
    assert abs(float(P["d_m4"][0]) - 3.593) < 1e-2 and bool(V5.v5_kural(P, "R4+M")[0])
    print("   şablon M:", {x: round(float(P["d_" + x][0]), 3) for x in ("m1", "m2", "m3", "m4")})


def test_sabit_esik_ve_kurallar():
    E = V5.V5_ESIK["esik"]
    assert (E["k_ust"], E["en_az_sonra"], E["G1_ort"], E["G1_degisim"], E["G2_ust"], E["T_spearman"], E["T_son"], E["I_pay"], E["I_ust"], E["B_max"], E["B_med"],
            E["F_pay"], E["S"]) == (0.6, 5, -0.3, 2, 0.80, 0.5, 0.6, 0.60, 1.05, 0.9, 0.30, 0.50, 0.59)
    assert (E["m1"], E["m2"], E["m3"], E["m4"]) == (0.45, 0.25, 0.33, 1.5) and V5.v5_liste("R4+M") == V5.KURAL["R4"] + ["M"]
    K = V5.KURAL
    assert K["R2"] == K["R1"] + ["S"] and K["R3"] == K["R1"] + ["T"] and set(K["R6"]) == set(K["R3"]) | {"I", "B"} and set(K["R7"]) == set(K["R6"]) | {"F"}
    assert set(K["R8"]) == set(K["R6"]) | {"S"} and len(K) == 8 and V5.v5_esik_sha() == V5.v5_esik_sha(json.loads(json.dumps(V5.V5_ESIK)))


def test_vektor_duz_ayni():
    O, H, L, C = _seri(600, 5); BU, BO, _ = MI.mi_bant(C); fark = 0; n = 0; y = 0
    for e in range(60, 600, 3):
        for m in (16, 19, 22, 24):
            sl = slice(e - m + 1, e + 1); W = {"O": O[sl], "H": H[sl], "L": L[sl], "C": C[sl], "BU": BU[sl], "BO": BO[sl]}
            P = V5.v5_parcalar(*(W[k] for k in ("O", "H", "L", "C", "BU", "BO"))); d = V5.v5_duz(W); n += 1; y += int(d["Y"])
            fark += sum(int(bool(P[p][0]) != bool(d[p])) for p in V5.DUZ_PARCA)
    assert fark == 0 and y > 20, (fark, y)


def test_Y_siniri():
    m = 20; C = np.r_[np.full(12, 95.0), np.linspace(101, 110, 8)]; O = C - 0.1; H = C + 0.3; L = C - 0.4; BU = np.full(m, 105.0); BO = np.full(m, 100.0)
    P = V5.v5_parcalar(O, H, L, C, BU, BO); assert int(P["k"][0]) == 12 and bool(P["Y"][0])          # 12 <= floor(0,6 x 20) = 12, sonra 7
    C2 = np.r_[np.full(13, 95.0), np.linspace(101, 110, 7)]
    P = V5.v5_parcalar(C2 - 0.1, C2 + 0.3, C2 - 0.4, C2, BU, BO); assert int(P["k"][0]) == 13 and not bool(P["Y"][0])


def test_secim_kurali():
    def t(var, kappa, parca):
        return {"VAR": var, "kappa": kappa, "parca": parca}
    tab = {"R1": t(20, 0.30, 3), "R3": t(10, 0.32, 4), "R6": t(7, 0.60, 6), "R4": t(9, 0.25, 5)}
    s = V5.v5_sec(tab, 8); assert s["secilen"] == "R1" and s["durum"] == "SEÇİLDİ"                     # R3 0,02 önde ama daha çok parça
    tab["R3"]["kappa"] = 0.34; assert V5.v5_sec(tab, 8)["secilen"] == "R3"
    s = V5.v5_sec({"R1": t(20, 0.18, 3), "R3": t(9, 0.2, 4)}, 8); assert s["durum"] == "DUR"
    assert V5.v5_sec({"R1": t(5, 0.9, 3)}, 8)["durum"] == "DUR"


def test_M_kapisi():
    m = 18; C = np.linspace(100, 110, m); O = C - 0.2; H = C + 1.0; L = O - 0.1; BU = C + 5; BO = C - 1
    P = V5.v5_parcalar(O, H, L, C, BU, BO); assert bool(P["M"][0])                            # küçük gövde, az alt fitil, uzun üst fitil
    P = V5.v5_parcalar(O, O + 0.2 + 0.1, L - 1.0, C, BU, BO); assert not bool(P["M"][0])      # alt fitil uzun
    P = V5.v5_parcalar(C - 3.0, C + 0.1, C - 3.05, C, BU, BO); assert not bool(P["M"][0])      # büyük gövde


def test_kendi_olcu():
    P = {"ham_B": np.array([False]), "ham_G1": np.array([True]), "d_cikis_govde": np.array([1.2])}
    assert V5._v5_kendi("n3", P) and not V5._v5_kendi("n6", P) and V5._v5_kendi("n8b", P)
    P["d_cikis_govde"] = np.array([0.5]); assert not V5._v5_kendi("n8b", P)


def test_gelecege_bakmama_ve_tekil():
    O, H, L, C = _seri(500, 7)
    for kural in ("R1", "R2"):
        R = V5.v5_tara_seri(O, H, L, C, kural, S_hep=True)
        for t in (120, 260, 499):
            Rk = V5.v5_tara_seri(O[:t + 1], H[:t + 1], L[:t + 1], C[:t + 1], kural, S_hep=True)
            assert bool(R["VAR"][t]) == bool(Rk["VAR"][t])
            a, b = R["S"][t], Rk["S"][t]; assert (np.isnan(a) and np.isnan(b)) or abs(a - b) < 1e-12
    e = np.array([10, 12, 20, 40, 41, 80]); S = np.zeros(100); S[[10, 12, 20, 40, 41, 80]] = [0.6, 0.7, 0.5, 0.9, 0.8, 0.55]
    assert V5.v5_tekil(e, S, 15).tolist() == [12, 40, 80]


def test_etiket_eslemesi():
    if not os.path.exists(V5.V5_YOL["etiket"]):
        print("  (etiket csv yok: atlandı)"); return
    X = V5.v5_etiketler(); assert len(X) == 61 and int(X.cemal.sum()) == 16 and set(X.set) == {"set1", "set2"}
    assert (X.m >= 16).all() and (X.m <= 24).all()


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_V5 as M\nns = dict(vars(M))\nns['v5_sec'] = 1\nns['_CK_ONCE_V5'] = {'v5_sec': id(M.v5_sec)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_v5()')[0] + '_cakisma_kontrol_v5()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(V5.__file__)))
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
