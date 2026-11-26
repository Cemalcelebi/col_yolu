"""test_mum_izi13 — MUM_IZI_GOZ2 testleri: set 5 ve birleşik örneklem sayıları, işaret çevirme permütasyonu, yön karşılaştırması, ek tanım mührü, çakışma kapısı.
Çalıştır: python test_mum_izi13.py"""
import json
import os
import subprocess
import sys

import numpy as np

import MUM_IZI_GOZ2 as G2


def test_ornek():
    if not os.path.exists(G2.G2_YOL["set5"][0]):
        print("  (set 5 işaretleri yok: atlandı)"); return
    X = G2.g2_ornek(); s5 = X[X.set == "set5"]
    assert len(s5) == 24 and s5.sinif.value_counts().to_dict() == {"EVET": 11, "KISMEN": 8, "HAYIR": 5} and len(X) == 128
    assert not X.duplicated(["zaman", "sembol", "tarih"]).any()


def test_isaret_perm():
    assert G2.g2_isaret_perm(np.full(20, 0.05) + np.linspace(-0.001, 0.001, 20), 2000, 1) < 0.01
    rng = np.random.default_rng(3); assert G2.g2_isaret_perm(rng.normal(0, 1, 40), 2000, 1) > 0.05
    assert G2.g2_isaret_perm(np.array([0.1]), 100, 1) is None


def test_yon():
    def T(k):
        return {"karsilastirma": {f"EVET-HAYIR|{z}": {"esli_fark_fark": k[z]} for z in ("gunluk", "haftalik")}}
    J = {"ilk_bakis": {"tablo": T({"gunluk": 0.05, "haftalik": -0.15})}, "ikinci_bakis": {"tablo": T({"gunluk": -0.02, "haftalik": -0.03}),
         "evet_es": {"EVET-es|gunluk": {"esli_fark_ort": 0.01}, "EVET-es|haftalik": {"esli_fark_ort": 0.02}}},
         "ilk_bakis_evet_es": {"EVET-es|gunluk": {"esli_fark_ort": 0.03}, "EVET-es|haftalik": {"esli_fark_ort": -0.16}}}
    Y = G2.g2_yon(J)
    assert Y["gunluk"]["EVET-HAYIR_esli"]["ayni_yon"] is False and Y["haftalik"]["EVET-HAYIR_esli"]["ayni_yon"] is True
    assert Y["gunluk"]["EVET-es"]["ayni_yon"] is True and Y["haftalik"]["EVET-es"]["ayni_yon"] is False


def test_ek_sabit():
    assert G2.g2_ek_sha() == G2.g2_ek_sha() and G2.G2_EK["evet_es"]["perm"] == 10000 and "GZ_ESIK aynen" in G2.G2_EK["tanim"]


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_GOZ2 as M\nns = dict(vars(M))\nns['g2_yon'] = 1\nns['_CK_ONCE_G2'] = {'g2_yon': id(M.g2_yon)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_g2()')[0] + '_cakisma_kontrol_g2()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(G2.__file__)))
    assert "KAPALI" in r.stdout, (r.stdout, r.stderr[-500:])


# ---------------------------------------------------------------- EK 15: kopma
def _k15_sentetik():
    import pandas as pd
    rows = []
    # EVET haftalık: KOPMUS 3 (fark +0.1, +0.2, +0.3), BASKI 2 (-0.1, -0.3), KARISIK 1; günlük: KOPMUS 2, BASKI 1 (n < 2)
    spec = [("EVET", "haftalik", "KOPMUS", "KOPMUS", 8, 8, 0.1), ("EVET", "haftalik", "KOPMUS", "KOPMUS", 9, 7, 0.2), ("EVET", "haftalik", "KOPMUS", "KOPMUS", 7, 7, 0.3),
            ("EVET", "haftalik", "BASKI", "BASKI", 2, 3, -0.1), ("EVET", "haftalik", "BASKI", "BASKI", 4, 4, -0.3), ("EVET", "haftalik", "KOPMUS", "BELIRSIZ", 6, 5, 0.0),
            ("EVET", "gunluk", "KOPMUS", "KOPMUS", 8, 6, 0.05), ("EVET", "gunluk", "KOPMUS", "KOPMUS", 6, 6, np.nan), ("EVET", "gunluk", "BASKI", "BASKI", 3, 3, -0.2),
            ("HAYIR", "gunluk", "BASKI", "BASKI", 2, 2, -0.05), ("HAYIR", "gunluk", "BASKI", "KOPMUS", 4, 7, 0.01)]
    for i, (s, z, k1, k2, p1, p2, f) in enumerate(spec):
        rows.append({"set": "set1", "sayfa": i + 1, "sinif": s, "zaman": z, "olculdu": True, "R15": (0.0 if np.isnan(f) else f) + 0.01, "es_R15": 0.01, "fark": f,
                     "es_neden": "es_az" if np.isnan(f) else None})
    O = pd.DataFrame(rows)
    H1 = {("set1", i + 1): {"k": r[2], "puan": float(r[4]), "gerekce": ""} for i, r in enumerate(spec)}
    H2 = {("set1", i + 1): {"k": r[3], "puan": float(r[5]), "gerekce": ""} for i, r in enumerate(spec)}
    return O, H1, H2


def test_k15_uzlasi_duyarlilik():
    assert G2.k15_uzlasi("KOPMUS", "KOPMUS") == "KOPMUS" and G2.k15_uzlasi("BASKI", "BASKI") == "BASKI"
    assert G2.k15_uzlasi("KOPMUS", "BASKI") == "KARISIK" and G2.k15_uzlasi("BELIRSIZ", "BELIRSIZ") == "KARISIK" and G2.k15_uzlasi("KOPMUS", "BELIRSIZ") == "KARISIK"
    assert G2.k15_duyar(6.0) == "KOPMUS*" and G2.k15_duyar(5.5) == "ARA*" and G2.k15_duyar(4.5) == "ARA*" and G2.k15_duyar(4.0) == "BASKI*" and G2.k15_duyar(10) == "KOPMUS*"
    O, H1, H2 = _k15_sentetik(); D = G2.k15_birlestir(O, H1, H2)
    assert D.uzlasi.tolist()[:6] == ["KOPMUS", "KOPMUS", "KOPMUS", "BASKI", "BASKI", "KARISIK"] and D.duyarlilik.iloc[5] == "ARA*" and D.puan_ort.iloc[0] == 8.0


def test_k15_tablo_okuma_perm():
    O, H1, H2 = _k15_sentetik(); D = G2.k15_birlestir(O, H1, H2); T = G2.k15_tablolar(D)
    c = T["ANA|uzlasi|haftalik"]; assert c["hucre"]["KOPMUS"]["n"] == 3 and abs(c["hucre"]["KOPMUS"]["fark_ort"] - 0.2) < 1e-12 and c["hucre"]["KOPMUS"]["esinden_iyi_pay"] == 1.0
    assert abs(c["fark"]["esli_fark_fark"] - 0.4) < 1e-12 and c["fark"]["durum"] == "hesaplandı"
    import MUM_IZI_GOZ as GZ
    assert c["fark"]["esli_p"] == GZ.gz_perm(np.array([0.1, 0.2, 0.3]), np.array([-0.1, -0.3]), 10000, 15)   # tohum 15, 10.000
    assert G2.K15_EK["karsilastirma"]["tohum"] == 15 and G2.K15_EK["karsilastirma"]["perm"] == 10000
    g = T["ANA|uzlasi|gunluk"]; assert g["fark"]["durum"] == "karşılaştırma yapılamaz" and g["fark"]["esli_p"] is None and g["hucre"]["KOPMUS"]["n_es"] == 1
    R = G2.k15_okuma(T); assert R["uzlasi"]["haftalik"]["saglandi"] is True and R["uzlasi"]["karar"].startswith("OKUNAMADI")
    # günlüğü hesaplanabilir yap: okuma kuralı iki yönde de
    D2 = D.copy(); D2.loc[7, "fark"] = 0.15; D2.loc[7, "es_neden"] = None; D2.loc[9, "sinif"] = "EVET"; T2 = G2.k15_tablolar(D2)
    assert G2.k15_okuma(T2)["uzlasi"]["karar"] == "AYRIM YÖNÜ CEMAL'İN DEDİĞİ GİBİ"
    D3 = D2.copy(); D3.loc[[0, 1, 2], "fark"] = -0.5; assert G2.k15_okuma(G2.k15_tablolar(D3))["uzlasi"]["karar"] == "AYRIM YÖNÜ CEMAL'İN DEDİĞİ GİBİ DEĞİL"
    S = G2.k15_sayim(D); assert "ANA|uzlasi|gunluk" in S["karsilastirma_yapilamaz"] and "ANA|uzlasi|haftalik" not in S["karsilastirma_yapilamaz"]
    assert S["grup_n"]["ANA|uzlasi|gunluk|KOPMUS"] == {"n": 2, "n_es": 1, "n_lt2": True}


def test_k15_kappa_spearman():
    k = G2.k15_kappa(["KOPMUS", "BASKI", "BELIRSIZ", "KOPMUS"], ["KOPMUS", "BASKI", "BELIRSIZ", "KOPMUS"]); assert abs(k["kappa"] - 1.0) < 1e-12
    k = G2.k15_kappa(["KOPMUS", "BASKI"] * 10, ["BASKI", "KOPMUS"] * 10); assert k["kappa"] < 0
    O, H1, H2 = _k15_sentetik(); D = G2.k15_birlestir(O, H1, H2); S = G2.k15_spearman(D); assert S["haftalik"]["n"] == 6 and S["haftalik"]["rho"] > 0.5 and S["gunluk"]["rho"] is None


def test_k15_eksik_sayfa_ve_sema():
    O, H1, H2 = _k15_sentetik(); del H2[("set1", 3)]
    try:
        G2.k15_birlestir(O, H1, H2); assert False, "eksik sayfa durdurmadı"
    except G2.G2Hata as ex:
        assert "set1:3" in str(ex) and "K2" in str(ex)
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        y = os.path.join(d, "h.json"); json.dump({"sayfalar": {"set1": {"1": {"k": "KOPMUŞ", "puan": 5}}}}, open(y, "w"))
        try:
            G2.k15_hakem_oku(y); assert False
        except G2.G2Hata:
            pass
        json.dump({"sayfalar": {"set1": {"1": {"k": "BASKI", "puan": 11}}}}, open(y, "w"))
        try:
            G2.k15_hakem_oku(y); assert False
        except G2.G2Hata:
            pass


def test_k15_gercek_eslesme():
    if not os.path.exists(G2.K15_YOL["K1"]):
        print("  (hakem json yok: atlandı)"); return
    D, G, _ = G2.k15_veri(); assert len(D) == 128 and G["sayim"]["toplam"] == 128
    assert [c["set2"] for c in G["tekrar"]["ciftler"]] == [7, 8, 9, 20, 26, 28, 34, 46]


def test_mevcut_komutlar_degismedi():
    import ast
    eski = subprocess.run(["git", "show", "46f1be3:MUM_IZI_GOZ2.py"], capture_output=True, text=True,
                          cwd=os.path.dirname(os.path.abspath(G2.__file__))).stdout
    if not eski:
        print("  (eski sürüm git'te yok: atlandı)"); return
    yeni = open(G2.__file__, encoding="utf-8").read()

    def fonk(src):
        t = ast.parse(src); return {n.name: ast.get_source_segment(src, n) for n in t.body if isinstance(n, (ast.FunctionDef, ast.Assign)) and getattr(n, "name", None)}
    fe, fy = fonk(eski), fonk(yeni)
    for ad, s in fe.items():
        if ad != "_g2_ana":
            assert fy.get(ad) == s, f"değişti: {ad}"
    assert G2.g2_ek_sha() == "f87dc6955ebad9306d117a5815bc59f129b9332dcc1dd559c886cad247f93447"   # MUM_IZI13 ön kaydındaki EK13_SHA
    for k in ("ornek", "onkayit", "kos", "pdf"):
        assert f'a.komut == "{k}"' in yeni


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
