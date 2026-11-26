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


# ---------------------------------------------------------------- EK 16: ölçek
def _k16_seri(T=200, h_once=4.0, h_bolge=(2, 2, 2, 2, 6, 2)):
    i = np.arange(T); C = np.where(i % 2 == 0, 100.0, 102.0); h = np.full(T, h_once); h[T - len(h_bolge):] = h_bolge
    return C.copy(), C + h / 2, C - h / 2, C


def test_k16_olcu_elle():
    O, H, L, C = _k16_seri(); P = G2.k16_olcu_bir(O, H, L, C, 6, (0.0, 10.0))
    pay = (4 / 100 + 4 / 102) / 2                                    # önceki 120 bar: 60 x 4/100, 60 x 4/102
    assert abs(P["BOY_MUTLAK"] - 100 * (2 / 102 + 2 / 100) / 2) < 1e-12   # bölge r sıralı: 3 x 2/102, 2 x 2/100, 6/100
    assert abs(P["BOY_OZ"] - 0.5) < 1e-12 and P["n_once"] == 120 and P["n_son"] == 2
    assert abs(P["SON_BOY_OZ"] - ((6 / 100 + 2 / 102) / 2) / pay) < 1e-12
    assert abs(P["BOY_BANT"] - 0.5) < 1e-12                          # son 20 kapanış 100 / 102: sigma 1, bant 4; H - L 2 -> 0,5
    assert abs(P["BOY_SAYFA"] - 0.2) < 1e-12 and abs(P["SISME"] - 10 / 6) < 1e-12   # H - L medyanı 2; bölge 97 .. 103
    assert G2.K16_EK["A2"]["tohum"] == 16 and G2.K16_EK["A2"]["perm"] == 10000 and G2.K16_ANA == "BOY_OZ"


def test_k16_once_penceresi_ve_40_bar():
    m = 6
    O, H, L, C = _k16_seri(T=m + 39); assert not np.isfinite(G2.k16_olcu_bir(O, H, L, C, m, None)["BOY_OZ"])          # 39 öncesi bar: boş
    O, H, L, C = _k16_seri(T=m + 40); assert np.isfinite(G2.k16_olcu_bir(O, H, L, C, m, None)["BOY_OZ"])              # 40: dolu
    O, H, L, C = _k16_seri(); b = G2.k16_olcu_bir(O, H, L, C, m, None)
    s = len(C) - m
    H2 = H.copy(); H2[s - 121] += 50; assert G2.k16_olcu_bir(O, H2, L, C, m, None)["BOY_OZ"] == b["BOY_OZ"]       # 121. önceki bar pencere dışı
    H3 = H.copy(); H3[s - 120] = L[s - 120] + 0.01; assert G2.k16_olcu_bir(O, H3, L, C, m, None)["BOY_OZ"] != b["BOY_OZ"]   # 120. önceki bar içeride
    H4 = H.copy(); H4[s - 60:s] += 10; assert G2.k16_olcu_bir(O, H4, L, C, m, None)["BOY_OZ"] < b["BOY_OZ"]          # öncesi büyüyünce oran düşer
    H5 = H.copy(); H5[s] += 1; assert G2.k16_olcu_bir(O, H5, L, C, m, None)["n_once"] == 120          # bölge barı öncesine girmez


def _k16_df(T=200, haftalik=False):
    O, H, L, C = _k16_seri(T)
    import pandas as pd
    ix = pd.bdate_range("2018-01-01", periods=T)
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1.0}, index=ix)
    if haftalik:
        d["bas"] = ix - pd.Timedelta(days=4)
    return d


def test_k16_gelecege_bakma_yok():
    d = _k16_df(260); t = 199; m = 6
    r = {"set": "set5", "sayfa": 1, "zaman": "gunluk", "bolge_son": str(d.index[t].date()), "bolge_bas": str(d.index[t - m + 1].date()), "m": m}
    x = G2.k16_bolge_dizi(d, r); assert len(x[3]) == t + 1
    P = G2.k16_olcu_bir(*x, m, G2.k16_sayfa_ylim("set5", *x, m))
    d2 = d.copy(); d2.iloc[t + 1:, :4] = d2.iloc[t + 1:, :4] * 3.7; d2.iloc[t + 1:, 1] += 40
    x2 = G2.k16_bolge_dizi(d2, r); P2 = G2.k16_olcu_bir(*x2, m, G2.k16_sayfa_ylim("set5", *x2, m))
    assert all((P[k] == P2[k]) or (np.isnan(P[k]) and np.isnan(P2[k])) for k in P), "sonraki barlar ölçüyü değiştirdi"
    try:
        G2.k16_bolge_dizi(d, dict(r, bolge_bas="2018-01-02")); assert False, "bölge başı denetimi çalışmadı"
    except G2.G2Hata:
        pass
    dw = _k16_df(260, haftalik=True); rw = dict(r, zaman="haftalik", bolge_bas=str(dw.bas.iloc[t - m + 1].date()))
    assert len(G2.k16_bolge_dizi(dw, rw)[0]) == t + 1


def test_k16_ylim_sayfa_ile_ayni():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import MUM_IZI_V2 as MV
    d = _k16_df(260); rng = np.random.default_rng(16); d["High"] += rng.uniform(0, 3, len(d)); d["Low"] -= rng.uniform(0, 3, len(d)); t = 199; m = 8
    r = {"set": "set5", "sayfa": 1, "zaman": "gunluk", "bolge_son": str(d.index[t].date()), "bolge_bas": str(d.index[t - m + 1].date()), "m": m}
    x = G2.k16_bolge_dizi(d, r); y = G2.k16_sayfa_ylim("set5", *x, m)
    try:
        import MUM_IZI_HAKEM as HK   # yalnız okunur: sayfayı çizen fonksiyon
        fig = plt.figure(figsize=(8.3, 11.7)); HK._hk_sayfa(fig, d, {"tarih": r["bolge_son"], "m": m, "zaman": "gunluk"}, MV.mv_sablon()["tam"]["ohlc"], 1, True)
        yh = fig.axes[1].get_ylim(); plt.close(fig); assert np.allclose(y, yh), (y, yh)
    except ImportError:
        print("  (MUM_IZI_HAKEM yok: sayfa karşılaştırması atlandı)")
    y3 = G2.k16_sayfa_ylim("set3", *x, m, 3); i0 = t - m + 1 - 15; lo = x[2][i0:].min(); hi = x[1][i0:].max()
    assert np.allclose(y3, (lo - 0.2 * (hi - lo), hi + 0.05 * (hi - lo)))


def _k16_sentetik_D():
    import pandas as pd
    rows = []
    for z, ozs, fs in (("gunluk", [0.5, 0.6, 0.7, 1.2, 1.4, 1.6], [0.10, 0.20, 0.30, -0.10, -0.20, 0.00]),
                       ("haftalik", [0.4, 0.8, 0.9, 1.1, 1.3, np.nan], [0.05, 0.15, -0.05, -0.30, 0.02, 0.5])):
        for i, (o, f) in enumerate(zip(ozs, fs)):
            rows.append({"set": "set1", "sayfa": len(rows) + 1, "sinif": "EVET", "zaman": z, "olculdu": True, "es_neden": None, "R15": f + 0.01, "fark": f,
                         **{k: o for k in G2.K16_AILE_OLCU}})
    rows.append({"set": "set1", "sayfa": 99, "sinif": "HAYIR", "zaman": "gunluk", "olculdu": True, "es_neden": "es_az", "R15": 0.0, "fark": np.nan,
                 **{k: 1.0 for k in G2.K16_AILE_OLCU}})
    return pd.DataFrame(rows)


def test_k16_bolme_perm_okuma():
    import pandas as pd
    import MUM_IZI_GOZ as GZ
    assert G2.k16_yari(pd.Series([1.0, 2, 3, 4, 5, np.nan])).tolist() == ["KUCUK", "KUCUK", "KUCUK", "BUYUK", "BUYUK", None]
    D = _k16_sentetik_D(); T = G2.k16_a2(D); c = T["EVET|BOY_OZ|gunluk"]
    assert c["KUCUK"]["n"] == 3 and abs(c["KUCUK"]["fark_ort"] - 0.2) < 1e-12 and abs(c["BUYUK"]["fark_ort"] + 0.1) < 1e-12
    assert abs(c["fark"]["esli_fark_fark"] - 0.3) < 1e-12 and c["fark"]["p"] == GZ.gz_perm(np.array([0.1, 0.2, 0.3]), np.array([-0.1, -0.2, 0.0]), 10000, 16)
    h = T["EVET|BOY_OZ|haftalik"]; assert h["KUCUK"]["n"] == 3 and h["BUYUK"]["n"] == 2       # medyan 0,9 (NaN yarıya girmez)
    assert c["spearman"]["n"] == 6 and c["spearman"]["rho"] < 0
    R = G2.k16_okuma(T); assert R["karar"] == "YÖN CEMAL'İN DEDİĞİ GİBİ" and R["etiket"] == "BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK"
    D2 = D.copy(); D2.loc[(D2.zaman == "haftalik") & (D2.BOY_OZ <= 0.9), "fark"] = -0.5; assert G2.k16_okuma(G2.k16_a2(D2))["karar"] == "YÖN CEMAL'İN DEDİĞİ GİBİ DEĞİL"
    D3 = D.copy(); D3.loc[(D3.zaman == "haftalik") & (D3.BOY_OZ > 0.9), "fark"] = np.nan; assert G2.k16_okuma(G2.k16_a2(D3))["karar"] == "OKUNAMADI"
    GN = G2.k16_grup_n(D); assert GN["EVET|BOY_OZ|gunluk"]["KUCUK"] == {"n": 3, "n_es": 3} and GN["HEPSI|BOY_OZ|gunluk"]["n_bolge"] == 7
    q = G2._k16_bh([0.01, None, 0.04, 0.03]); assert q[1] is None and abs(q[0] - 0.03) < 1e-12 and abs(q[2] - 0.04) < 1e-12


def test_k16_notlu_gercek():
    import pandas as pd
    if not os.path.exists(G2.K16_YOL["sonrasi13"]):
        print("  (MUM_IZI13_SONRASI yok: atlandı)"); return
    D = pd.read_csv(G2.K16_YOL["olay13"], usecols=G2.K16_GETIRISIZ); N = G2.k16_notlu(D)
    assert N.sembol.tolist() == ["TRMET", "SLDB", "TOON", "SIG", "SANM", "NCMI", "ALNY", "EBAY", "EFOR", "IESC"] and N.fiziksel_sayfa.tolist() == [4, 5, 7, 8, 9, 10, 11, 12, 13, 14]
    assert (N["set"] == "set5").all() and N.sinif.tolist() == ["EVET"] * 8 + ["KISMEN"] * 2


def test_k16_mevcut_degismedi():
    import ast
    eski = subprocess.run(["git", "show", "9f81e38:MUM_IZI_GOZ2.py"], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(G2.__file__))).stdout
    if not eski:
        print("  (eski sürüm git'te yok: atlandı)"); return
    yeni = open(G2.__file__, encoding="utf-8").read()

    def fonk(src):
        t = ast.parse(src); out = {}
        for n in t.body:
            if isinstance(n, ast.FunctionDef):
                out[n.name] = ast.get_source_segment(src, n)
            elif isinstance(n, (ast.Assign, ast.AnnAssign)):
                hed = n.targets[0] if isinstance(n, ast.Assign) else n.target
                if isinstance(hed, ast.Name):
                    out[hed.id] = ast.get_source_segment(src, n)
        return out
    fe, fy = fonk(eski), fonk(yeni)
    for ad, s in fe.items():
        if ad != "_g2_ana":
            assert fy.get(ad) == s, f"değişti: {ad}"
    assert G2.k15_ek_sha() == "cbbb6430e21474099f42930a139d5a96f69d418e698adf244c95b08cbe19f982"   # MUM_IZI15 ön kaydındaki EK15_SHA
    for k in ("ornek", "onkayit", "kos", "pdf", "kopma_sayim", "kopma_onkayit", "kopma"):
        assert f'a.komut == "{k}"' in yeni
    import MUM_IZI as MI
    assert MI._mi_sha(G2.K16_YOL["olay13"]) == "fc27c506ae981157f13b2aeb534e2c9c098a947ad0b158130f0c5845f73dcec8"   # mum_izi13_olay.csv değişmedi


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
