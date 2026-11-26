"""test_mum_izi17 — MUM_IZI_GOZ2 EK 17 (set 6 = MUM_IZI14 ölçekli onay seti; birleşik 145) testleri: örneklem ve şema denetimi, getirisiz geçit (gz_olc_bir
kapılarıyla aynı), dokunma kuralı, hücre ölçüleri, set 1-5 fark sayımı, yön, ek tanım mührü, çalışan fonksiyonların değişmediği, çakışma kapısı.
Çalıştır: python test_mum_izi17.py"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

import MUM_IZI_GOZ as GZ
import MUM_IZI_GOZ2 as G2


def test_set6_ornek():
    if not os.path.exists(G2.K17_YOL["isaret6"]):
        print("  (set 6 işaretleri yok: atlandı)"); return
    X = G2.k17_ornek(); s6 = X[X.set == "set6"]
    assert len(s6) == 17 and len(X) == 145
    assert s6.sinif.value_counts().to_dict() == {"KISMEN": 7, "HAYIR": 6, "EVET": 4}
    assert s6.groupby(["sinif", "zaman"]).size().to_dict() == {("EVET", "gunluk"): 1, ("EVET", "haftalik"): 3, ("HAYIR", "gunluk"): 3, ("HAYIR", "haftalik"): 3,
                                                                ("KISMEN", "gunluk"): 4, ("KISMEN", "haftalik"): 3}
    assert not X.duplicated(["zaman", "sembol", "tarih"]).any()
    assert s6.loc[s6.sayfa == 4, "sembol"].item() == "AMD" and abs(s6.loc[s6.sayfa == 4, "boy_oran"].item() - 1.83) < 0.01
    assert np.isnan(s6.loc[s6.sayfa == 3, "boy_oran"].item())                      # TCAP.L: önceki mum yetersiz


def test_set6_sema_uyusmazlik_durur():
    if not os.path.exists(G2.K17_YOL["isaret6"]):
        print("  (set 6 işaretleri yok: atlandı)"); return
    eski = dict(G2.K17_YOL)
    with tempfile.TemporaryDirectory() as d:
        J = json.load(open(eski["isaret6"], encoding="utf-8")); J["sayfalar"].pop("18")
        y = os.path.join(d, "i.json"); json.dump(J, open(y, "w", encoding="utf-8"), ensure_ascii=False)
        J2 = json.load(open(eski["isaret6"], encoding="utf-8")); J2["sayfalar"]["5"]["zaman"] = "haftalik"
        y2 = os.path.join(d, "i2.json"); json.dump(J2, open(y2, "w", encoding="utf-8"), ensure_ascii=False)
        for yy in (y, y2):
            G2.K17_YOL["isaret6"] = yy
            try:
                G2.k17_set6(); raise AssertionError("durmadı")
            except G2.G2Hata:
                pass
            finally:
                G2.K17_YOL.update(eski)


def _seri(n=60, kapanis=None):
    idx = pd.bdate_range("2021-01-04", periods=n)
    C = np.full(n, 100.0) if kapanis is None else np.asarray(kapanis, float)
    return pd.DataFrame({"Open": C, "High": C * 1.01, "Low": C * 0.99, "Close": C, "Volume": 1.0}, index=idx)


def test_gecit_gz_ile_ayni():
    D = _seri(60); kesik = pd.Timestamp("2022-12-31")
    for tarih, m, bek in ((D.index[20], 5, ""), (D.index[59], 5, "giris_yok"), (D.index[50], 5, "ufuk_kesik")):
        r = {"zaman": "gunluk", "tarih": str(tarih.date()), "m": m}
        a = G2.k17_gecit_bir(D, None, r, kesik); b = GZ.gz_olc_bir(D, None, r, kesik)
        assert a["neden"] == bek == b["neden"] and a["olculebilir"] == b["olculdu"] and "R15" not in a
    C = np.full(60, 100.0); C[21] = 50.0; D2 = _seri(60, C); D2.loc[D2.index[21], "Open"] = 50.0   # giriş açılışı stop'un altında
    r = {"zaman": "gunluk", "tarih": str(D2.index[20].date()), "m": 5}
    assert G2.k17_gecit_bir(D2, None, r, pd.Timestamp("2022-12-31"))["neden"] == "giris_stop_altinda" == GZ.gz_olc_bir(D2, None, r, pd.Timestamp("2022-12-31"))["neden"]
    r = {"zaman": "gunluk", "tarih": str(D.index[30].date()), "m": 5}
    assert G2.k17_gecit_bir(D, None, r, D.index[40])["neden"] == "ufuk_kesik"       # 15. mum kesikten sonra


def test_dokunma_kurali():
    H = np.array([101, 104, 106, 112]); L = np.array([99, 97, 95, 90])
    assert G2.k17_dokunma(H, L, 100, 94, 0.05) == 1.0 and G2.k17_dokunma(H, L, 100, 94, 0.10) == 0.0      # +%10 günü stop'tan sonra
    assert G2.k17_dokunma(np.array([106]), np.array([93]), 100, 94, 0.05) == 0.0                          # aynı gün = stop önce
    assert G2.k17_dokunma(np.array([101, 102]), np.array([99, 99]), 100, 94, 0.05) == 0.0


def test_hucre_ve_tablolar():
    Y = pd.DataFrame({"set": ["set6"] * 5 + ["set5"] * 2, "sinif": ["EVET", "EVET", "HAYIR", "HAYIR", "KISMEN", "EVET", "HAYIR"],
                      "sinif_son": ["EVET", "EVET", "HAYIR", "HAYIR", "KISMEN", "EVET", "HAYIR"], "zaman": ["haftalik"] * 4 + ["gunluk"] * 3, "pazar": "ABD",
                      "olculdu": True, "R15": [0.1, -0.2, 0.05, 0.0, 0.03, 0.02, -0.01], "es_R15": [0.0, 0.1, 0.0, np.nan, 0.01, 0.0, 0.0],
                      "fark": [0.1, -0.3, 0.05, np.nan, 0.02, 0.02, -0.01], "d5_tum": [1, 0, 1, 0, 0, 1, 0], "d5": [1, 0, 1, 0, 0, 1, 0], "d10": [1, 0, 0, 0, 0, 0, 0],
                      "d20": 0.0, "stop15": [0, 1, 0, 0, 0, 0, 0], "max15": 0.1, "min15": -0.1, "R30": np.nan, "sira": 0.5, "es_d5": 0.3, "es_d10": 0.1, "es_d20": 0.0,
                      "es_stop15": 0.1, "neden": "", "hakem_sinif": ["a", "b", "a", "b", "a", np.nan, np.nan]})
    h = G2.k17_hucre(Y[(Y.set == "set6") & (Y.sinif == "EVET")])
    assert h["n"] == 2 and h["n_es"] == 2 and abs(h["R15_ort"] + 0.05) < 1e-12 and h["esinden_iyi_pay"] == 0.5 and h["d5_pay"] == 0.5 and h["stop_pay"] == 0.5
    h = G2.k17_hucre(Y[(Y.set == "set6") & (Y.sinif == "HAYIR")]); assert h["n"] == 2 and h["n_es"] == 1 and h["esinden_iyi_pay"] == 1.0
    T = G2.k17_tablolar(Y)
    assert T["hakem"]["set6|birlikte"]["n"] == 5 and T["hakem"]["set5|gunluk"]["n"] == 2 and T["hakem"]["set6_hakem_a|birlikte"]["n"] == 3
    assert T["birlesik"]["k17_hucre"]["EVET|haftalik"]["n"] == 2 and T["birlesik"]["k17_hucre"]["EVET|gunluk"]["n"] == 1
    assert T["ucuncu_bakis"]["gz"]["karsilastirma"]["EVET-HAYIR|haftalik"]["esli_p"] is None        # HAYIR eşli n 1 -> p yok


def test_yon():
    def K(v):
        return {"karsilastirma": {f"EVET-HAYIR|{z}": {"esli_fark_fark": v[z]} for z in ("gunluk", "haftalik")}}
    J13 = {"ilk_bakis": {"tablo": K({"gunluk": 0.05, "haftalik": -0.15})}, "ikinci_bakis": {"tablo": K({"gunluk": -0.02, "haftalik": 0.01}),
           "evet_es": {"EVET-es|gunluk": {"esli_fark_ort": -0.03}, "EVET-es|haftalik": {"esli_fark_ort": -0.15}}},
           "ilk_bakis_evet_es": {"EVET-es|gunluk": {"esli_fark_ort": 0.03}, "EVET-es|haftalik": {"esli_fark_ort": -0.16}}}
    T = {"ucuncu_bakis": {"gz": K({"gunluk": None, "haftalik": -0.1}), "evet_es": {"EVET-es|gunluk": {"esli_fark_ort": 0.2, "n_es": 1},
                                                                                  "EVET-es|haftalik": {"esli_fark_ort": -0.05, "n_es": 3}}}}
    Y = G2.k17_yon(T, J13)
    assert Y["haftalik"]["EVET-HAYIR_esli"]["ilkle_ayni_yon"] is True and Y["haftalik"]["EVET-HAYIR_esli"]["ikinciyle_ayni_yon"] is False
    assert Y["gunluk"]["EVET-HAYIR_esli"]["durum"] == "karşılaştırma yapılamaz" and Y["gunluk"]["EVET-es"]["durum"] == "karşılaştırma yapılamaz"
    assert Y["haftalik"]["EVET-es"]["ilkle_ayni_yon"] is True


def test_set15_farki():
    a = pd.DataFrame({"set": ["set1", "set1", "set5"], "sayfa": [3, 4, 2], "sembol": ["A", "B", "C"], "R15": [0.1, 0.2, 0.3], "es_R15": [0.0, 0.1, np.nan],
                      "fark": [0.1, 0.1, np.nan], "n_es": [10, 12, np.nan], "es_neden": [np.nan, np.nan, "es_az"]})
    b = a.copy(); b.loc[1, "es_R15"] = 0.12; b.loc[1, "fark"] = 0.08; b.loc[1, "n_es"] = 11
    b = pd.concat([b, pd.DataFrame({"set": ["set6"], "sayfa": [2], "sembol": ["D"], "R15": [0.0]})], ignore_index=True)
    F = G2.k17_set15_farki(a, b)
    assert F["satir"] == 3 and F["farkli"] == {"R15": 0, "es_R15": 1, "fark": 1, "n_es": 1} and abs(F["en_buyuk_mutlak_fark"]["fark"] - 0.02) < 1e-12
    assert len(F["degisen_satirlar"]) == 1


def test_ek_sabit():
    assert G2.k17_ek_sha() == G2.k17_ek_sha() and "GZ_ESIK aynen" in G2.K17_EK["tanim"] and G2.K17_EK["etiket"].startswith("BİLGİ")
    assert set(G2.K17_KONTROL) == {f"K{i}" for i in range(1, 15)}


def test_calisan_fonksiyonlar_degismedi():
    import ast
    eski = subprocess.run(["git", "show", "471ac28:MUM_IZI_GOZ2.py"], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(G2.__file__))).stdout
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
    assert G2.g2_ek_sha() == "f87dc6955ebad9306d117a5815bc59f129b9332dcc1dd559c886cad247f93447"
    for k in ("ornek", "onkayit", "kos", "pdf", "kopma_sayim", "kopma_onkayit", "kopma", "olcek_olcu", "olcek_onkayit", "olcek", "set6_sayim", "set6_onkayit", "set6_kos",
              "set6_pdf"):
        assert f'a.komut == "{k}"' in yeni


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_GOZ2 as M\nns = dict(vars(M))\nns['k17_yon'] = 1\nns['_CK_ONCE_G2'] = {'k17_yon': id(M.k17_yon)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_g2()')[0] + '_cakisma_kontrol_g2()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(G2.__file__)))
    assert "KAPALI" in r.stdout, (r.stdout, r.stderr[-500:])


def test_sonuc_olay_uyumu():
    """Sonuç varsa: olay csv 145 satır, sha uyumu ve iki hücre csv'den bağımsız yeniden üretim."""
    ys = os.path.join(G2.G2_YOL["cikti"], G2.K17_DOSYA["sonuc"])
    if not os.path.exists(ys):
        print("  (sonuç 17 yok: atlandı)"); return
    import MUM_IZI as MI
    J = json.load(open(ys, encoding="utf-8")); yo = os.path.join(G2.G2_YOL["cikti"], G2.K17_DOSYA["olay"])
    assert MI._mi_sha(yo) == J["olay_sha"]
    O = pd.read_csv(yo); assert len(O) == 145 and (O.set == "set6").sum() == 17
    for s, z in (("EVET", "haftalik"), ("HAYIR", "gunluk")):
        g = O[(O.set == "set6") & (O.sinif == s) & (O.zaman == z) & O.olculdu]; c = J["ucuncu_bakis"]["hucre"][f"{s}|{z}"]
        assert c["n"] == len(g) and abs(c["R15_ort"] - g.R15.mean()) < 1e-5
        f = g.fark.dropna(); assert abs(c["fark_ort"] - f.mean()) < 1e-5 and abs(c["esinden_iyi_pay"] - (f > 0).mean()) < 1e-12
    g = O[(O.sinif == "EVET") & (O.zaman == "haftalik")]; c = J["birlesik"]["tablo"]["hucre"]["EVET|haftalik"]
    assert c["n"] == len(g) and abs(c["fark_ort"] - g.fark.dropna().mean()) < 1e-5


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
