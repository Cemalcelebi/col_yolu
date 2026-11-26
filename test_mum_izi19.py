"""test_mum_izi19 — MUM_IZI_GOZ2 EK 19 (set 7 = MUM_IZI18 mum boyu kapılı onay seti; set 6+7; birleşik 157) testleri: örneklem ve şema denetimi (yıldız dahil),
karşılaştırma n >= 2 koruması, YÖN satırında n >= 2 koruması (EK 17 HATA düzeltmesi; k17_yon değişmez), tablolar, önceki koşu fark sayımı, ek tanım mührü,
çalışan fonksiyonların değişmediği (f218598'e göre), çakışma kapısı, sonuç-olay uyumu ve bağımsız yeniden üretim.
Çalıştır: python test_mum_izi19.py"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

import MUM_IZI_GOZ2 as G2

KOK = os.path.dirname(os.path.abspath(G2.__file__))


def test_set7_ornek():
    if not os.path.exists(G2.K19_YOL["isaret7"]):
        print("  (set 7 işaretleri yok: atlandı)"); return
    X = G2.k19_ornek(); s7 = X[X.set == "set7"]
    assert len(s7) == 12 and len(X) == 157 and (X.set == "set6").sum() == 17
    assert s7.sinif.value_counts().to_dict() == {"EVET": 6, "HAYIR": 4, "KISMEN": 2}
    assert s7.groupby(["sinif", "zaman"]).size().to_dict() == {("EVET", "gunluk"): 5, ("EVET", "haftalik"): 1, ("HAYIR", "gunluk"): 4, ("KISMEN", "gunluk"): 2}
    assert sorted(s7[s7.yildiz].sayfa) == [3, 12] and not X[X.set != "set7"].yildiz.any()
    assert not X.duplicated(["zaman", "sembol", "tarih"]).any()
    assert s7.loc[s7.sayfa == 9, "sembol"].item() == "KTB" and abs(s7.loc[s7.sayfa == 9, "boy_oran"].item() - 0.502) < 0.001
    assert (s7.katman == "KÜÇÜK").all()


def test_set7_sema_uyusmazlik_durur():
    if not os.path.exists(G2.K19_YOL["isaret7"]):
        print("  (set 7 işaretleri yok: atlandı)"); return
    eski = dict(G2.K19_YOL)
    with tempfile.TemporaryDirectory() as d:
        J = json.load(open(eski["isaret7"], encoding="utf-8")); yy = []
        for i, f in enumerate((lambda j: j["sayfalar"].pop("13"), lambda j: j["sayfalar"]["5"].__setitem__("zaman", "haftalik"),
                               lambda j: j["sayfalar"]["3"].__setitem__("yildiz", "evet"))):
            Jc = json.loads(json.dumps(J)); f(Jc); y = os.path.join(d, f"i{i}.json"); json.dump(Jc, open(y, "w", encoding="utf-8"), ensure_ascii=False); yy.append(y)
        for y in yy:
            G2.K19_YOL["isaret7"] = y
            try:
                G2.k19_set7(); raise AssertionError("durmadı")
            except G2.G2Hata:
                pass
            finally:
                G2.K19_YOL.update(eski)


def _Y():
    return pd.DataFrame({"set": ["set7"] * 5 + ["set6"] * 3 + ["set1"] * 2, "sinif": ["EVET", "EVET", "HAYIR", "KISMEN", "EVET", "HAYIR", "HAYIR", "EVET", "EVET", "HAYIR"],
                         "zaman": ["gunluk"] * 4 + ["haftalik"] + ["gunluk"] * 3 + ["haftalik"] * 2, "pazar": "ABD", "olculdu": True,
                         "R15": [0.1, -0.2, 0.05, 0.0, 0.03, 0.02, -0.01, 0.04, 0.1, 0.0], "es_R15": [0.0, 0.1, 0.0, np.nan, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0],
                         "fark": [0.1, -0.3, 0.05, np.nan, 0.02, 0.02, -0.01, 0.04, 0.1, 0.0], "d5_tum": 0.0, "d5": 0.0, "d10": 0.0, "d20": 0.0, "stop15": 0.0,
                         "max15": 0.1, "min15": -0.1, "R30": np.nan, "sira": 0.5, "es_d5": 0.3, "es_d10": 0.1, "es_d20": 0.0, "es_stop15": 0.1, "neden": "",
                         "yildiz": [True, False, False, False, True, False, False, False, False, False], "sinif_son": None})


def test_karsilastir_n_korumasi():
    Y = _Y(); Y["sinif_son"] = Y.sinif
    a = Y[(Y.set == "set7") & (Y.sinif == "EVET") & (Y.zaman == "gunluk")]; b = Y[(Y.set == "set7") & (Y.sinif == "HAYIR")]
    c = G2.k19_karsilastir(a, b); assert c["durum"] == "karşılaştırma yapılamaz" and c["esli_fark_fark"] is None and c["n_es_b"] == 1
    b2 = Y[Y.sinif == "HAYIR"]; c = G2.k19_karsilastir(a, b2)
    assert c["durum"] == "hesaplandı" and abs(c["esli_fark_fark"] - (-0.1 - (0.05 + 0.02 - 0.01 + 0.0) / 4)) < 1e-12 and c["esli_p"] is not None


def test_tablolar():
    Y = _Y(); Y["sinif_son"] = Y.sinif; T = G2.k19_tablolar(Y)
    assert T["dorduncu_bakis"]["hucre"]["EVET|gunluk"]["n"] == 2 and T["dorduncu_bakis"]["hucre"]["EVET|birlikte"]["n"] == 3
    assert T["kapi"]["set7|birlikte"]["n"] == 5 and T["kapi"]["set7_yildiz|birlikte"]["n"] == 2 and T["kapi"]["set6|birlikte"]["n"] == 3
    assert T["olcekli"]["hucre"]["HAYIR|gunluk"]["n"] == 3 and T["olcekli"]["hucre"]["EVET+KISMEN|birlikte"]["n"] == 5
    assert T["olcekli"]["karsilastirma"]["EVET-HAYIR|gunluk"]["durum"] == "hesaplandı"
    assert T["olcekli"]["karsilastirma"]["EVET-HAYIR|haftalik"]["durum"] == "karşılaştırma yapılamaz"     # haftalık HAYIR yok
    assert T["birlesik"]["k17_hucre"]["EVET|haftalik"]["n"] == 2


def test_yon_n_korumasi():
    """EK 17 HATA: EVET n 1 iken EVET - HAYIR yön satırı 'hesaplandı' çıkıyordu. k19_yon iki grupta n >= 2 ister; k17_yon değişmez."""
    def K(v, na, nb):
        return {"karsilastirma": {f"EVET-HAYIR|{z}": {"esli_fark_fark": v[z], "n_es_a": na[z], "n_es_b": nb[z]} for z in ("gunluk", "haftalik")}}

    def E(v, n):
        return {f"EVET-es|{z}": {"esli_fark_ort": v[z], "n_es": n[z]} for z in ("gunluk", "haftalik")}
    J13 = {"ilk_bakis": {"tablo": K({"gunluk": 0.05, "haftalik": -0.15}, {"gunluk": 10, "haftalik": 10}, {"gunluk": 10, "haftalik": 10})},
           "ikinci_bakis": {"tablo": K({"gunluk": -0.02, "haftalik": 0.01}, {"gunluk": 5, "haftalik": 5}, {"gunluk": 5, "haftalik": 1}),
                            "evet_es": E({"gunluk": -0.03, "haftalik": -0.15}, {"gunluk": 5, "haftalik": 5})},
           "ilk_bakis_evet_es": E({"gunluk": 0.03, "haftalik": -0.16}, {"gunluk": 10, "haftalik": 10})}
    J17 = {"ucuncu_bakis": {"gz": K({"gunluk": -0.007, "haftalik": 0.22}, {"gunluk": 1, "haftalik": 3}, {"gunluk": 3, "haftalik": 3}),
                            "evet_es": E({"gunluk": -0.13, "haftalik": 0.025}, {"gunluk": 1, "haftalik": 3})}}
    T = {"dorduncu_bakis": {"gz": K({"gunluk": 0.04, "haftalik": 0.3}, {"gunluk": 5, "haftalik": 1}, {"gunluk": 4, "haftalik": 0}),
                            "evet_es": E({"gunluk": 0.02, "haftalik": 0.1}, {"gunluk": 5, "haftalik": 1})}}
    Y = G2.k19_yon(T, J13, J17)
    assert Y["haftalik"]["EVET-HAYIR_esli"]["durum"] == "karşılaştırma yapılamaz" and Y["haftalik"]["EVET-es"]["durum"] == "karşılaştırma yapılamaz"
    g = Y["gunluk"]["EVET-HAYIR_esli"]
    assert g["durum"] == "hesaplandı" and g["ucuncu"] is None and g["ucuncule_ayni_yon"] is None and g["ilkle_ayni_yon"] is True and g["ikincile_ayni_yon"] is False
    assert Y["gunluk"]["EVET-es"]["ucuncu"] is None and Y["gunluk"]["EVET-es"]["ilkle_ayni_yon"] is True
    # ikinci bakış haftalık HAYIR n 1: değer kullanılmaz
    assert Y["haftalik"]["EVET-HAYIR_esli"]["ikinci"] is None
    # gerçek EK 17 çıktısı: düzeltilmiş okuma üçüncü bakış günlük EVET - HAYIR'ı kullanmaz; eski json değişmeden kalır
    ys = os.path.join(G2.G2_YOL["cikti"], G2.K17_DOSYA["sonuc"])
    if os.path.exists(ys):
        J = json.load(open(ys, encoding="utf-8"))
        assert J["yon"]["gunluk"]["EVET-HAYIR_esli"]["durum"] == "hesaplandı"                   # eski kusurlu etiket json'da duruyor (değişmez)
        assert G2._k19_kv(J["ucuncu_bakis"]["gz"]["karsilastirma"], "EVET-HAYIR|gunluk") is None   # düzeltilmiş okuma


def test_onceki_farki():
    a = pd.DataFrame({"set": ["set1", "set1", "set6"], "sayfa": [3, 4, 2], "sembol": ["A", "B", "C"], "R15": [0.1, 0.2, 0.3], "es_R15": [0.0, 0.1, np.nan],
                      "fark": [0.1, 0.1, np.nan], "n_es": [10, 12, np.nan], "es_neden": [np.nan, np.nan, "es_az"]})
    b = a.copy(); b.loc[1, "es_R15"] = 0.12; b.loc[1, "fark"] = 0.08; b.loc[1, "n_es"] = 11
    b = pd.concat([b, pd.DataFrame({"set": ["set7"], "sayfa": [2], "sembol": ["D"], "R15": [0.0]})], ignore_index=True)
    F = G2.k19_onceki_farki(a, b)
    assert F["satir"] == 3 and F["beklenen"] == 3 and F["farkli"] == {"R15": 0, "es_R15": 1, "fark": 1, "n_es": 1}
    assert abs(F["en_buyuk_mutlak_fark"]["fark"] - 0.02) < 1e-12 and len(F["degisen_satirlar"]) == 1 and F["es_neden_degisen"] == 0


def test_ek_sabit():
    assert G2.k19_ek_sha() == G2.k19_ek_sha() and "GZ_ESIK aynen" in G2.K19_EK["tanim"] and G2.K19_EK["etiket"].startswith("BİLGİ")
    assert set(G2.K19_KONTROL) == {f"K{i}" for i in range(1, 15)} and G2.K19_EK["karsilastirma"] == {"n_min": 2, "perm": 10000, "tohum": 19}
    assert G2.k17_ek_sha() == "8759a8a5693cff75903d074e0d5367b3691cd05cc7bef9b93c8874ef1e2aa4dd"
    assert G2.g2_ek_sha() == "f87dc6955ebad9306d117a5815bc59f129b9332dcc1dd559c886cad247f93447"


def test_calisan_fonksiyonlar_degismedi():
    import ast
    eski = subprocess.run(["git", "show", "f218598:MUM_IZI_GOZ2.py"], capture_output=True, text=True, cwd=KOK).stdout
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
    for k in ("ornek", "onkayit", "kos", "pdf", "kopma_sayim", "kopma_onkayit", "kopma", "olcek_olcu", "olcek_onkayit", "olcek", "set6_sayim", "set6_onkayit", "set6_kos",
              "set6_pdf", "set7_sayim", "set7_onkayit", "set7_kos", "set7_pdf"):
        assert f'a.komut == "{k}"' in yeni
    # MUM_IZI_GOZ.py ve EK 17 çıktıları değişmedi
    d = subprocess.run(["git", "diff", "--stat", "f218598", "--", "MUM_IZI_GOZ.py", "arastirma_cikti/mum_izi/mum_izi17_sonuc.json", "arastirma_cikti/mum_izi/mum_izi17_olay.csv",
                        "arastirma_cikti/mum_izi/MUM_IZI17_SONRASI.pdf"], capture_output=True, text=True, cwd=KOK).stdout
    assert d.strip() == "", d


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_GOZ2 as M\nns = dict(vars(M))\nns['k19_yon'] = 1\nns['_CK_ONCE_G2'] = {'k19_yon': id(M.k19_yon)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_g2()')[0] + '_cakisma_kontrol_g2()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=KOK)
    assert "KAPALI" in r.stdout, (r.stdout, r.stderr[-500:])


def test_sonuc_olay_uyumu():
    """Sonuç varsa: olay csv 157 satır, sha uyumu ve üç hücre csv'den bağımsız yeniden üretim (set 7, set 6+7, birleşik) + set 6+7 farkı."""
    ys = os.path.join(G2.G2_YOL["cikti"], G2.K19_DOSYA["sonuc"])
    if not os.path.exists(ys):
        print("  (sonuç 19 yok: atlandı)"); return
    import MUM_IZI as MI
    J = json.load(open(ys, encoding="utf-8")); yo = os.path.join(G2.G2_YOL["cikti"], G2.K19_DOSYA["olay"])
    assert MI._mi_sha(yo) == J["olay_sha"]
    O = pd.read_csv(yo); assert len(O) == 157 and (O.set == "set7").sum() == 12
    for s, z in (("EVET", "gunluk"), ("HAYIR", "gunluk")):
        g = O[(O.set == "set7") & (O.sinif == s) & (O.zaman == z) & O.olculdu]; c = J["dorduncu_bakis"]["hucre"][f"{s}|{z}"]
        assert c["n"] == len(g) and abs(c["R15_ort"] - g.R15.mean()) < 1e-5
        f = g.fark.dropna(); assert abs(c["fark_ort"] - f.mean()) < 1e-5 and abs(c["esinden_iyi_pay"] - (f > 0).mean()) < 1e-12
    P = O[O.set.isin(["set6", "set7"])]
    a = P[P.sinif == "EVET"].fark.dropna(); b = P[P.sinif == "HAYIR"].fark.dropna(); c = J["olcekli"]["karsilastirma"]["EVET-HAYIR|birlikte"]
    assert abs(c["esli_fark_fark"] - (a.mean() - b.mean())) < 1e-5
    g = O[(O.sinif == "EVET") & (O.zaman == "gunluk")]; c = J["birlesik"]["tablo"]["hucre"]["EVET|gunluk"]
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
