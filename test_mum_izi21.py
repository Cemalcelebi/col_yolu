"""test_mum_izi21 — MUM_IZI_GOZ2 EK 21 (set 8 = MUM_IZI20 katmanlı onay seti; kapıdan geçenler set 7+8; set 6+7+8; birleşik 181) testleri: örneklem ve şema
denetimi (işaretsiz satır, iki kutu, oran kapısı), karşılaştırma n >= 2 koruması, kapıdan geçenler okuma kuralı, tablolar (işaretsiz satır sınıf tablolarına girmez,
kapıdan geçenlere girer), duyarlılık, ek tanım mührü (önceki ek sha'lar değişmedi), çalışan fonksiyonların değişmediği (e0d9e35'e göre; EK 19 / 17 çıktıları 4c947e1'e göre), çakışma kapısı, sonuç-olay
uyumu, sonuç json'unda anahtar çakışması olmadığı (EK 19 HATA) ve bağımsız yeniden üretim.
Çalıştır: python test_mum_izi21.py"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

import MUM_IZI_GOZ2 as G2

KOK = os.path.dirname(os.path.abspath(G2.__file__))


def test_set8_ornek():
    X = G2.k21_ornek(); s8 = X[X.set == "set8"]
    assert len(s8) == 24 and len(X) == 181 and (X.set == "set7").sum() == 12 and (X.set == "set6").sum() == 17
    assert s8.isaret.value_counts().to_dict() == {"HAYIR": 9, "EVET": 7, "KISMEN": 7, "YOK": 1}
    assert s8.sinif.isna().sum() == 1 and s8.loc[s8.sinif.isna(), "sayfa"].item() == 15 and X.sinif.isna().sum() == 1
    d = s8[s8.sinif_duy.fillna("-") != s8.sinif.fillna("-")]
    assert d.sayfa.tolist() == [11] and d.sinif.item() == "KISMEN" and d.sinif_duy.item() == "EVET"
    assert (X[X.set != "set8"].sinif_duy.fillna("-") == X[X.set != "set8"].sinif.fillna("-")).all()
    assert (s8.boy_oran <= 0.70).all() and s8.zaman.value_counts().to_dict() == {"gunluk": 18, "haftalik": 6}
    assert not X.duplicated(["zaman", "sembol", "tarih"]).any()
    assert s8.loc[s8.sayfa == 2, "sembol"].item() == "TEMN.SW" and abs(s8.loc[s8.sayfa == 2, "boy_oran"].item() - 0.66100) < 1e-4


def test_set8_sema_durur():
    eski = dict(G2.K21_YOL)
    with tempfile.TemporaryDirectory() as d:
        J = json.load(open(eski["isaret8"], encoding="utf-8")); A = json.load(open(eski["anahtar8"], encoding="utf-8"))
        bozuk = []
        for i, f in enumerate((lambda j: j["sayfalar"].pop("13"), lambda j: j["sayfalar"]["5"].__setitem__("zaman", "haftalik"),
                               lambda j: j["sayfalar"]["4"].__setitem__("isaret", "BELIRSIZ"), lambda j: j["sayfalar"]["3"].__setitem__("yildiz", "evet"),
                               lambda j: j["sayfalar"]["9"].__setitem__("kutu_disi", "iki kutu işaretli"))):
            Jc = json.loads(json.dumps(J)); f(Jc); y = os.path.join(d, f"i{i}.json"); json.dump(Jc, open(y, "w", encoding="utf-8"), ensure_ascii=False)
            bozuk.append(("isaret8", y))
        Ac = json.loads(json.dumps(A)); Ac["sayfalar"][0]["oran"] = 0.5; y = os.path.join(d, "a.json"); json.dump(Ac, open(y, "w", encoding="utf-8"), ensure_ascii=False)
        bozuk.append(("anahtar8", y))
        for k, y in bozuk:
            G2.K21_YOL[k] = y
            try:
                G2.k21_set8(); raise AssertionError(f"durmadı: {k} {y}")
            except G2.G2Hata:
                pass
            finally:
                G2.K21_YOL.update(eski)


def _Y():
    n = 12
    Y = pd.DataFrame({"set": ["set8"] * 5 + ["set7"] * 3 + ["set6"] * 2 + ["set1"] * 2,
                      "sinif": ["EVET", "KISMEN", "HAYIR", None, "HAYIR", "EVET", "HAYIR", "KISMEN", "EVET", "HAYIR", "EVET", "HAYIR"],
                      "zaman": ["gunluk", "gunluk", "gunluk", "gunluk", "haftalik", "gunluk", "gunluk", "haftalik", "haftalik", "haftalik", "gunluk", "gunluk"],
                      "pazar": "ABD", "olculdu": True,
                      "R15": [0.1, -0.2, 0.05, 0.3, 0.03, 0.02, -0.01, 0.04, 0.1, 0.0, 0.05, -0.05],
                      "es_R15": [0.0, 0.1, 0.0, 0.1, 0.01, 0.0, 0.0, 0.0, 0.0, 0.05, 0.0, 0.0]})
    Y["fark"] = Y.R15 - Y.es_R15
    for c, v in (("d5_tum", 0.0), ("d5", 0.0), ("d10", 0.0), ("d20", 0.0), ("stop15", 0.0), ("max15", 0.1), ("min15", -0.1), ("R30", np.nan), ("sira", 0.5),
                 ("es_d5", 0.3), ("es_d10", 0.1), ("es_d20", 0.0), ("es_stop15", 0.1), ("neden", ""), ("yildiz", False)):
        Y[c] = [v] * n
    Y["sinif_son"] = Y.sinif; Y["sinif_duy"] = Y.sinif; Y.loc[1, "sinif_duy"] = "EVET"
    return Y


def test_tablolar():
    Y = _Y(); T = G2.k21_tablolar(Y)
    B = T["besinci_bakis"]["hucre"]
    assert B["EVET|gunluk"]["n"] == 1 and B["HAYIR|birlikte"]["n"] == 2 and B["isaretsiz|birlikte"]["n"] == 1
    assert sum(B[f"{s}|birlikte"]["n"] for s in ("EVET", "KISMEN", "HAYIR")) == 4          # işaretsiz sınıf tablosunda yok
    K = T["kapidan_gecenler"]
    assert K["set7+set8|birlikte"]["n"] == 8 and K["set8|birlikte"]["n"] == 5 and K["set7|birlikte"]["n"] == 3   # işaretsiz kapıdan geçenlerde var
    assert abs(K["set7+set8|birlikte"]["fark_ort"] - Y.iloc[:8].fark.mean()) < 1e-12 and "BİLGİ" in K["set7+set8|birlikte"]["okuma"]
    O = T["olcekli"]
    assert O["hucre"]["EVET|birlikte"]["n"] == 3 and O["hucre"]["HAYIR|birlikte"]["n"] == 4 and O["hucre"]["EVET+KISMEN|birlikte"]["n"] == 5
    assert O["duyarlilik"]["hucre"]["EVET|birlikte"]["n"] == 4 and O["duyarlilik"]["hucre"]["KISMEN|birlikte"]["n"] == 1
    c = O["karsilastirma"]["EVET-HAYIR|birlikte"]; ha = Y.iloc[:10]; a = ha[ha.sinif == "EVET"].fark; b = ha[ha.sinif == "HAYIR"].fark
    assert c["durum"] == "hesaplandı" and abs(c["esli_fark_fark"] - (a.mean() - b.mean())) < 1e-12
    assert O["karsilastirma"]["EVET-HAYIR|gunluk"]["durum"] == "hesaplandı" and O["karsilastirma"]["EVET-HAYIR|haftalik"]["durum"] == "karşılaştırma yapılamaz"   # haftalık EVET 1
    assert abs(O["hayir_es"]["HAYIR-es|birlikte"]["esli_fark_ort"] - b.mean()) < 1e-12
    assert T["birlesik"]["k17_hucre"]["EVET|birlikte"]["n"] == 4


def test_karsilastir_ve_okuma():
    Y = _Y()
    a = Y[Y.sinif == "EVET"].iloc[:1]; b = Y[Y.sinif == "HAYIR"]
    assert G2.k21_karsilastir(a, b)["durum"] == "karşılaştırma yapılamaz"
    c = G2.k21_karsilastir(Y[Y.sinif == "EVET"], b); assert c["durum"] == "hesaplandı" and c["esli_p"] is not None
    assert G2.k21_okuma({"boot95": [0.01, 0.05], "n_es": 40}) == "eşlerinden iyi; BİLGİ"
    assert G2.k21_okuma({"boot95": [-0.05, -0.01], "n_es": 40}) == "eşlerinden kötü; BİLGİ"
    assert G2.k21_okuma({"boot95": [-0.05, 0.01], "n_es": 20}) == "ayrışmıyor; ÖRNEKLEM YETERSİZ; BİLGİ"
    e = G2.k21_es_farki(Y); f = Y.fark.to_numpy()
    assert e["n_es"] == 12 and abs(e["esli_fark_ort"] - f.mean()) < 1e-12 and e["boot95"][0] < f.mean() < e["boot95"][1] and 0 < e["p"] <= 1


def test_ek_sabit():
    assert G2.k21_ek_sha() == G2.k21_ek_sha() and "K19_EK aynen" in G2.K21_EK["tanim"] and G2.K21_EK["etiket"].startswith("BİLGİ")
    assert set(G2.K21_KONTROL) == {f"K{i}" for i in range(1, 15)} and G2.K21_EK["karsilastirma"] == {"n_min": 2, "perm": 10000, "boot": 5000, "tohum": 21}
    assert G2.k19_ek_sha() == "3cbf5ea6d8ce41058193db168469fe30532f34a630ba09b3ec29b5b11b13ff90"
    assert G2.k17_ek_sha() == "8759a8a5693cff75903d074e0d5367b3691cd05cc7bef9b93c8874ef1e2aa4dd"
    assert G2.g2_ek_sha() == "f87dc6955ebad9306d117a5815bc59f129b9332dcc1dd559c886cad247f93447"


def test_calisan_fonksiyonlar_degismedi():
    import ast
    eski = subprocess.run(["git", "show", "e0d9e35:MUM_IZI_GOZ2.py"], capture_output=True, text=True, cwd=KOK).stdout
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
              "set6_pdf", "set7_sayim", "set7_onkayit", "set7_kos", "set7_pdf", "set8_sayim", "set8_onkayit", "set8_kos", "set8_pdf"):
        assert f'a.komut == "{k}"' in yeni
    d = subprocess.run(["git", "diff", "--stat", "4c947e1", "--", "MUM_IZI_GOZ.py", "arastirma_cikti/mum_izi/mum_izi19_sonuc.json", "arastirma_cikti/mum_izi/mum_izi19_olay.csv",
                        "arastirma_cikti/mum_izi/MUM_IZI19_SONRASI.pdf", "arastirma_cikti/mum_izi/mum_izi17_sonuc.json", "arastirma_cikti/mum_izi/mum_izi17_olay.csv"],
                       capture_output=True, text=True, cwd=KOK).stdout
    assert d.strip() == "", d


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_GOZ2 as M\nns = dict(vars(M))\nns['k21_tablolar'] = 1\nns['_CK_ONCE_G2'] = {'k21_tablolar': id(M.k21_tablolar)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_g2()')[0] + '_cakisma_kontrol_g2()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=KOK)
    assert "KAPALI" in r.stdout, (r.stdout, r.stderr[-500:])


def test_sonuc_olay_uyumu():
    """Sonuç varsa: olay csv 181 satır, sha uyumu, anahtar çakışması yok (onkayit_kapi kaydı duruyor) ve hücreler csv'den bağımsız yeniden üretim."""
    ys = os.path.join(G2.G2_YOL["cikti"], G2.K21_DOSYA["sonuc"])
    if not os.path.exists(ys):
        print("  (sonuç 21 yok: atlandı)"); return
    import MUM_IZI as MI
    J = json.load(open(ys, encoding="utf-8")); yo = os.path.join(G2.G2_YOL["cikti"], G2.K21_DOSYA["olay"])
    assert MI._mi_sha(yo) == J["olay_sha"] and J["onkayit_kapi"]["kontrol"]["gecti"] and "KOD21_SHA" in J["onkayit_kapi"] and "set7+set8|birlikte" in J["kapidan_gecenler"]
    O = pd.read_csv(yo); assert len(O) == 181 and (O.set == "set8").sum() == 24 and O.sinif.isna().sum() == 1
    for s, z in (("EVET", "gunluk"), ("HAYIR", "gunluk")):
        g = O[(O.set == "set8") & (O.sinif == s) & (O.zaman == z) & O.olculdu]; c = J["besinci_bakis"]["hucre"][f"{s}|{z}"]
        assert c["n"] == len(g) and abs(c["R15_ort"] - g.R15.mean()) < 1e-5
        f = g.fark.dropna(); assert abs(c["fark_ort"] - f.mean()) < 1e-5 and abs(c["esinden_iyi_pay"] - (f > 0).mean()) < 1e-12
    K = O[O.set.isin(["set7", "set8"]) & O.olculdu]; c = J["kapidan_gecenler"]["set7+set8|birlikte"]
    assert c["n"] == len(K) == 36 and abs(c["fark_ort"] - K.fark.dropna().mean()) < 1e-5 and abs(c["d5_pay"] - K.d5_tum.mean()) < 1e-9
    P = O[O.set.isin(["set6", "set7", "set8"]) & O.sinif.notna()]
    a = P[P.sinif == "EVET"].fark.dropna(); b = P[P.sinif == "HAYIR"].fark.dropna(); c = J["olcekli"]["karsilastirma"]["EVET-HAYIR|birlikte"]
    assert abs(c["esli_fark_fark"] - (a.mean() - b.mean())) < 1e-5
    ad = P.sinif.where(P.sayfa.ne(11) | P.set.ne("set8"), "EVET"); a2 = P[ad == "EVET"].fark.dropna()
    assert abs(J["olcekli"]["duyarlilik"]["karsilastirma"]["EVET-HAYIR|birlikte"]["esli_fark_fark"] - (a2.mean() - b.mean())) < 1e-5
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
