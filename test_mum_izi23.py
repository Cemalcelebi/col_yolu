"""test_mum_izi23 — MUM_IZI_GOZ2 EK 23 (set 9 = MUM_IZI22 geçmişli onay seti; kapıdan geçenler set 7+8+9; kapı havuzunda Cemal'in işareti; set 6-9; birleşik 205)
testleri: örneklem ve şema denetimi (oran kapısı, iki kutu, işaret değeri, sayfa kümesi), tablolar (işaretsiz satır sınıf tablolarına girmez, kapıdan geçenlere girer;
sınıf eşli farkı; karşılaştırma n >= 2 koruması), ek tanım mührü (önceki ek sha'lar değişmedi), çalışan fonksiyonların değişmediği (7752bef'e göre; EK 21 çıktıları
fa7de71..HEAD arasında değişmedi), çakışma kapısı, sonuç-olay uyumu ve bağımsız yeniden üretim.
Çalıştır: python test_mum_izi23.py"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

import MUM_IZI_GOZ2 as G2

KOK = os.path.dirname(os.path.abspath(G2.__file__))


def test_set9_ornek():
    X = G2.k23_ornek(); s9 = X[X.set == "set9"]
    assert len(s9) == 24 and len(X) == 205 and (X.set == "set8").sum() == 24 and (X.set == "set7").sum() == 12 and (X.set == "set6").sum() == 17
    assert s9.isaret.value_counts().to_dict() == {"EVET": 10, "KISMEN": 8, "HAYIR": 6} and s9.sinif.notna().all() and X.sinif.isna().sum() == 1
    assert ((s9.sinif == "EVET") & (s9.zaman == "gunluk")).sum() == 8 and ((s9.sinif == "EVET") & (s9.zaman == "haftalik")).sum() == 2
    assert ((s9.sinif == "KISMEN") & (s9.zaman == "gunluk")).sum() == 6 and ((s9.sinif == "HAYIR") & (s9.zaman == "gunluk")).sum() == 6
    assert (s9.sinif_duy == s9.sinif).all() and (s9.boy_oran <= 0.70).all() and s9.zaman.value_counts().to_dict() == {"gunluk": 20, "haftalik": 4}
    d = X[X.sinif_duy.fillna("-") != X.sinif.fillna("-")]
    assert d[["set", "sayfa"]].values.tolist() == [["set8", 11]]
    assert not X.duplicated(["zaman", "sembol", "tarih"]).any()
    assert s9.loc[s9.sayfa == 2, "sembol"].item() == "ISKPL" and abs(s9.loc[s9.sayfa == 2, "boy_oran"].item() - 0.469830778) < 1e-6
    assert s9.katman.value_counts().to_dict() == {"KISMEN|oran<=0,65": 6, "KISMEN|0,65<oran<=0,70": 6, "HAYIR|oran<=0,65": 6, "HAYIR|0,65<oran<=0,70": 6}
    # set 1-8 satırları k21_ornek ile aynı
    X8 = G2.k21_ornek(); a = X[X.set != "set9"].reset_index(drop=True)
    assert len(a) == len(X8) and (a[["set", "sayfa", "sembol", "tarih", "zaman"]].values == X8[["set", "sayfa", "sembol", "tarih", "zaman"]].values).all()


def test_set9_sema_durur():
    eski = dict(G2.K23_YOL)
    with tempfile.TemporaryDirectory() as d:
        J = json.load(open(eski["isaret9"], encoding="utf-8")); A = json.load(open(eski["anahtar9"], encoding="utf-8"))
        bozuk = []
        for i, f in enumerate((lambda j: j["sayfalar"].pop("13"), lambda j: j["sayfalar"]["5"].__setitem__("zaman", "haftalik"),
                               lambda j: j["sayfalar"]["4"].__setitem__("isaret", "BELIRSIZ"), lambda j: j["sayfalar"]["3"].__setitem__("yildiz", "evet"),
                               lambda j: j["sayfalar"]["9"].__setitem__("kutu_disi", "iki kutu işaretli"))):
            Jc = json.loads(json.dumps(J)); f(Jc); y = os.path.join(d, f"i{i}.json"); json.dump(Jc, open(y, "w", encoding="utf-8"), ensure_ascii=False)
            bozuk.append(("isaret9", y))
        for i, f in enumerate((lambda a: a["sayfalar"][0].__setitem__("oran", 0.5), lambda a: a["sayfalar"].pop(3))):
            Ac = json.loads(json.dumps(A)); f(Ac); y = os.path.join(d, f"a{i}.json"); json.dump(Ac, open(y, "w", encoding="utf-8"), ensure_ascii=False)
            bozuk.append(("anahtar9", y))
        for k, y in bozuk:
            G2.K23_YOL[k] = y
            try:
                G2.k23_set9(); raise AssertionError(f"durmadı: {k} {y}")
            except G2.G2Hata:
                pass
            finally:
                G2.K23_YOL.update(eski)


def _Y():
    n = 14
    Y = pd.DataFrame({"set": ["set9"] * 4 + ["set8"] * 3 + ["set7"] * 3 + ["set6"] * 2 + ["set1"] * 2,
                      "sinif": ["EVET", "KISMEN", "HAYIR", "EVET", None, "HAYIR", "EVET", "HAYIR", "KISMEN", "EVET", "EVET", "HAYIR", "EVET", "HAYIR"],
                      "zaman": ["gunluk", "gunluk", "gunluk", "haftalik", "gunluk", "haftalik", "gunluk", "gunluk", "haftalik", "gunluk", "haftalik", "haftalik", "gunluk",
                                "gunluk"],
                      "pazar": "ABD", "olculdu": True,
                      "R15": [0.1, -0.2, 0.05, 0.2, 0.3, 0.03, 0.02, -0.01, 0.04, 0.06, 0.1, 0.0, 0.05, -0.05],
                      "es_R15": [0.0, 0.1, 0.0, 0.1, 0.1, 0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.05, 0.0, 0.0]})
    Y["fark"] = Y.R15 - Y.es_R15
    for c, v in (("d5_tum", 0.0), ("d5", 0.0), ("d10", 0.0), ("d20", 0.0), ("stop15", 0.0), ("max15", 0.1), ("min15", -0.1), ("R30", np.nan), ("sira", 0.5),
                 ("es_d5", 0.3), ("es_d10", 0.1), ("es_d20", 0.0), ("es_stop15", 0.1), ("neden", ""), ("yildiz", False)):
        Y[c] = [v] * n
    Y["sinif_son"] = Y.sinif; Y["sinif_duy"] = Y.sinif; Y.loc[8, "sinif_duy"] = "EVET"
    return Y


def test_tablolar():
    Y = _Y(); T = G2.k23_tablolar(Y)
    B = T["altinci_bakis"]["hucre"]
    assert B["EVET|birlikte"]["n"] == 2 and B["EVET|gunluk"]["n"] == 1 and B["HAYIR|birlikte"]["n"] == 1 and B["isaretsiz|birlikte"]["n"] == 0
    K = T["kapidan_gecenler"]; Yk = Y.iloc[:10]
    assert K["set7+set8+set9|birlikte"]["n"] == 10 and K["set9|birlikte"]["n"] == 4 and K["set8|birlikte"]["n"] == 3 and K["set7|birlikte"]["n"] == 3
    assert abs(K["set7+set8+set9|birlikte"]["fark_ort"] - Yk.fark.mean()) < 1e-12 and "BİLGİ" in K["set7+set8+set9|birlikte"]["okuma"]
    assert K["set7+set8+set9|gunluk"]["n"] == 7
    KI = T["kapi_isaret"]; Yki = Yk[Yk.sinif.notna()]
    assert KI["hucre"]["EVET|birlikte"]["n"] == 4 and KI["hucre"]["HAYIR|birlikte"]["n"] == 3 and KI["hucre"]["EVET+KISMEN|birlikte"]["n"] == 6
    a = Yki[Yki.sinif == "EVET"].fark; b = Yki[Yki.sinif == "HAYIR"].fark
    assert abs(KI["karsilastirma"]["EVET-HAYIR|birlikte"]["esli_fark_fark"] - (a.mean() - b.mean())) < 1e-12
    assert abs(KI["sinif_es"]["EVET-es|birlikte"]["esli_fark_ort"] - a.mean()) < 1e-12 and abs(KI["hayir_es"]["HAYIR-es|birlikte"]["esli_fark_ort"] - b.mean()) < 1e-12
    assert KI["karsilastirma"]["EVET-HAYIR|haftalik"]["durum"] == "karşılaştırma yapılamaz"   # haftalık EVET 1, HAYIR 1
    assert KI["duyarlilik"]["hucre"]["EVET|birlikte"]["n"] == 5 and KI["duyarlilik"]["hucre"]["KISMEN|birlikte"]["n"] == 1
    OL = T["olcekli"]
    assert OL["hucre"]["EVET|birlikte"]["n"] == 5 and OL["hucre"]["HAYIR|birlikte"]["n"] == 4 and "gz" in OL and "evet_es" in OL
    assert T["birlesik"]["k17_hucre"]["EVET|birlikte"]["n"] == 6


def test_karsilastir_es_farki():
    Y = _Y()
    a = Y[Y.sinif == "EVET"].iloc[:1]; b = Y[Y.sinif == "HAYIR"]
    assert G2.k23_karsilastir(a, b)["durum"] == "karşılaştırma yapılamaz"
    c = G2.k23_karsilastir(Y[Y.sinif == "EVET"], b); assert c["durum"] == "hesaplandı" and c["esli_p"] is not None
    e = G2.k23_es_farki(Y); f = Y.fark.to_numpy()
    assert e["n_es"] == 14 and abs(e["esli_fark_ort"] - f.mean()) < 1e-12 and abs(e["esli_fark_med"] - np.median(f)) < 1e-12
    assert e["boot95"][0] < f.mean() < e["boot95"][1] and 0 < e["p"] <= 1
    e21 = G2.k21_es_farki(Y); assert abs(e21["esli_fark_ort"] - e["esli_fark_ort"]) < 1e-15   # aynı tanım, yalnız tohum farklı


def test_ek_sabit():
    assert "K21_EK aynen" in G2.K23_EK["tanim"] and G2.K23_EK["etiket"].startswith("BİLGİ")
    assert set(G2.K23_KONTROL) == {f"K{i}" for i in range(1, 15)} and G2.K23_EK["karsilastirma"] == {"n_min": 2, "perm": 10000, "boot": 5000, "tohum": 23}
    assert G2.k21_ek_sha() == "f4ca0d0b367d05d01ac3c125d5ad7e2e87d752af78450f5d316dfae6ef3a5fc0"
    assert G2.k19_ek_sha() == "3cbf5ea6d8ce41058193db168469fe30532f34a630ba09b3ec29b5b11b13ff90"
    assert G2.k17_ek_sha() == "8759a8a5693cff75903d074e0d5367b3691cd05cc7bef9b93c8874ef1e2aa4dd"
    assert G2.g2_ek_sha() == "f87dc6955ebad9306d117a5815bc59f129b9332dcc1dd559c886cad247f93447"
    assert G2.K21_EK["karsilastirma"]["tohum"] == 21 and G2.K19_EK["karsilastirma"]["tohum"] == 19


def test_calisan_fonksiyonlar_degismedi():
    import ast
    eski = subprocess.run(["git", "show", "7752bef:MUM_IZI_GOZ2.py"], capture_output=True, text=True, cwd=KOK).stdout
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
              "set6_pdf", "set7_sayim", "set7_onkayit", "set7_kos", "set7_pdf", "set8_sayim", "set8_onkayit", "set8_kos", "set8_pdf", "set9_sayim", "set9_onkayit", "set9_kos",
              "set9_pdf"):
        assert f'a.komut == "{k}"' in yeni
    d = subprocess.run(["git", "diff", "--stat", "9ac1ebf", "--", "MUM_IZI_GOZ.py", "arastirma_cikti/mum_izi/mum_izi21_sonuc.json", "arastirma_cikti/mum_izi/mum_izi21_olay.csv",
                        "arastirma_cikti/mum_izi/MUM_IZI21_SONRASI.pdf", "arastirma_cikti/mum_izi/cemal_mum_izi22_onay.json",
                        "arastirma_cikti/mum_izi/MUM_IZI22_onay_anahtar.json", "arastirma_cikti/mum_izi/MUM_IZI22_onay_olcekli.json"],
                       capture_output=True, text=True, cwd=KOK).stdout
    assert d.strip() == "", d


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_GOZ2 as M\nns = dict(vars(M))\nns['k23_tablolar'] = 1\nns['_CK_ONCE_G2'] = {'k23_tablolar': id(M.k23_tablolar)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_g2()')[0] + '_cakisma_kontrol_g2()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=KOK)
    assert "KAPALI" in r.stdout, (r.stdout, r.stderr[-500:])


def test_sonuc_olay_uyumu():
    """Sonuç varsa: olay csv 205 satır, sha uyumu, anahtar çakışması yok; hücreler csv'den bağımsız yeniden üretim (olculdu süzgeci her hücrede açık)."""
    ys = os.path.join(G2.G2_YOL["cikti"], G2.K23_DOSYA["sonuc"])
    if not os.path.exists(ys):
        print("  (sonuç 23 yok: atlandı)"); return
    import MUM_IZI as MI
    J = json.load(open(ys, encoding="utf-8")); yo = os.path.join(G2.G2_YOL["cikti"], G2.K23_DOSYA["olay"])
    assert MI._mi_sha(yo) == J["olay_sha"] and J["onkayit_kapi"]["kontrol"]["gecti"] and "KOD23_SHA" in J["onkayit_kapi"] and "set7+set8+set9|birlikte" in J["kapidan_gecenler"]
    O = pd.read_csv(yo); assert len(O) == 205 and (O.set == "set9").sum() == 24 and O.sinif.isna().sum() == 1
    for s, z in (("EVET", "gunluk"), ("HAYIR", "gunluk")):
        g = O[(O.set == "set9") & (O.sinif == s) & (O.zaman == z) & O.olculdu]; c = J["altinci_bakis"]["hucre"][f"{s}|{z}"]
        assert c["n"] == len(g) and abs(c["R15_ort"] - g.R15.mean()) < 1e-5
        f = g.fark.dropna(); assert abs(c["fark_ort"] - f.mean()) < 1e-5 and abs(c["esinden_iyi_pay"] - (f > 0).mean()) < 1e-12
    K = O[O.set.isin(["set7", "set8", "set9"]) & O.olculdu]; c = J["kapidan_gecenler"]["set7+set8+set9|birlikte"]
    assert c["n"] == len(K) and c["n_bolge"] == 60 and abs(c["fark_ort"] - K.fark.dropna().mean()) < 1e-5 and abs(c["d5_pay"] - K.d5_tum.mean()) < 1e-9
    Kg = K[K.zaman == "gunluk"]; assert abs(J["kapidan_gecenler"]["set7+set8+set9|gunluk"]["fark_ort"] - Kg.fark.dropna().mean()) < 1e-5
    P = K[K.sinif.notna()]
    a = P[P.sinif == "EVET"].fark.dropna(); b = P[P.sinif == "HAYIR"].fark.dropna(); c = J["kapi_isaret"]["karsilastirma"]["EVET-HAYIR|birlikte"]
    assert abs(c["esli_fark_fark"] - (a.mean() - b.mean())) < 1e-5 and c["n_es_a"] == len(a) and c["n_es_b"] == len(b)
    ak = P[P.sinif.isin(["EVET", "KISMEN"])].fark.dropna()
    assert abs(J["kapi_isaret"]["karsilastirma"]["(EVET+KISMEN)-HAYIR|birlikte"]["esli_fark_fark"] - (ak.mean() - b.mean())) < 1e-5
    Q = O[O.set.isin(["set6", "set7", "set8", "set9"]) & O.sinif.notna() & O.olculdu]
    a = Q[Q.sinif == "EVET"].fark.dropna(); b = Q[Q.sinif == "HAYIR"].fark.dropna()
    assert abs(J["olcekli"]["karsilastirma"]["EVET-HAYIR|birlikte"]["esli_fark_fark"] - (a.mean() - b.mean())) < 1e-5
    g = O[(O.sinif == "EVET") & (O.zaman == "gunluk") & O.olculdu]; c = J["birlesik"]["tablo"]["hucre"]["EVET|gunluk"]
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
