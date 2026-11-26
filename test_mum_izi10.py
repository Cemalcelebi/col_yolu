"""test_mum_izi10 — MUM_IZI_HAKEM testleri (gerçek fiyat ve hakem verisi yok): aday seçim kuralları (sayı, hisse başına bir, BIST tavanı, hariç listesi,
karışık sıra, tohumla aynı), hakem şeması (sıkı; çelişki DUR), onay seçimi (>= 24 -> 24, 12 / 12 ve eksik dilim tamamlama; < 24 -> hepsi; < 8 -> DUR),
eşik mührü, çakışma kapısı. EK 14: 1. / 2. parti anahtar sha'ları değişmez, parti 3 hariç tutma, KISMEN kabulü, iki aşamalı sıra,
kapak {N2}, öğrenme şeridi (sayım / sıra / metin), --hakem2 olmadan onay geriye uyumu (MUM_IZI12 onayı birebir).
EK 16 İŞ B (--olcek): mum boyu ölçüsü (tanım, geleceğe bakma yok), sağlam dikey sınır, yüzde ekseni adımı, sayfa çizimi geleceğe bakmaz, --olcek olmadan
MUM_IZI14 onayı birebir (pdf sha), ölçekli basım uçtan uca (bölge kimliği, kapılar, hisse adı yok, pdf sha = commit edilen), repodaki ölçekli dosyalar.
Çalıştır: python test_mum_izi10.py"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

import MUM_IZI_HAKEM as HK


def _olay(n_g=400, n_h=300, tohum=1):
    rng = np.random.default_rng(tohum); o = []
    for z, n in (("gunluk", n_g), ("haftalik", n_h)):
        for i in range(n):
            p = ["ABD", "AVR", "BIST"][int(rng.integers(3))]
            o.append({"zaman": z, "pazar": p, "sembol": f"{z[0]}{p}{int(rng.integers(0, 260))}", "tarih": f"2020-01-{1 + i % 28:02d}", "m": 20, "k": 8, "S": 0.5,
                      "evren": bool(rng.random() > 0.1)})
    return o


def test_aday_secim():
    o = _olay(); h = {o[0]["sembol"], o[5]["sembol"]}
    G = dict(HK.HK_ESIK["aday"], gunluk=60, haftalik=40, bist_tavan=10)
    S = HK.hk_aday_sec(o, h, G)
    assert len(S) == 100 and len({r["sembol"] for r in S}) == 100 and not ({r["sembol"] for r in S} & h)
    assert sum(r["zaman"] == "gunluk" for r in S) == 60 and all(r["evren"] for r in S)
    for z in ("gunluk", "haftalik"):
        assert sum(r["zaman"] == z and r["pazar"] == "BIST" for r in S) <= 10
    assert sorted(r["sayfa"] for r in S) == list(range(1, 101))
    zs = [r["zaman"] for r in sorted(S, key=lambda r: r["sayfa"])]; assert zs != sorted(zs)          # karışık sıra
    assert HK.hk_aday_sec(o, h, G) == S


def test_parti2_secim():
    o = _olay(400, 120, 3); h = {o[0]["sembol"]}
    G = dict(HK.HK_ESIK_P2, gunluk=100, haftalik=100)
    S = HK.hk_aday_sec(o, h, G); X = {z: [r for r in S if r["zaman"] == z] for z in ("gunluk", "haftalik")}
    assert len({r["sembol"] for r in S}) == len(S) and not ({r["sembol"] for r in S} & h)
    assert len(X["haftalik"]) < 100                                                    # haftalık yetmedi: olabildiği kadar (DUR yok)
    for z in X:
        nb = sum(r["pazar"] == "BIST" for r in X[z]); assert nb <= int(0.20 * len(X[z]) + 1e-9), (z, nb, len(X[z]))
    assert sorted(r["sayfa"] for r in S) == list(range(1, len(S) + 1)) and HK.hk_aday_sec(o, h, G) == S


def test_parti1_tekrar():
    y = os.path.join(HK.HK_PARTI[1]["klasor"], "mum_izi10_aday_anahtar.json")
    if not os.path.exists(y) or not os.path.exists(HK.HK_YOL["ham8"]):
        print("  (1. parti anahtarı / tarama ham dosyası yok: atlandı)"); return
    K = json.load(open(y, encoding="utf-8")); S = HK.hk_aday_sec(HK.hk_olaylar(), HK.hk_haric(1))
    assert [(r["sayfa"], r["sembol"]) for r in S] == [(r["sayfa"], r["sembol"]) for r in K["sayfalar"]] and HK._hk_sha() == K["esik_sha"]


def test_kapak_ve_anahtar_bul():
    assert HK.hk_kapak_metni("bak {M}, seç {N}, koy {K}", 600, 40, 24) == "bak 600, seç 40, koy 24"
    assert "300 adaya baktı, 20 tanesini seçti; bunlar onlar" in HK.hk_kapak_metni(None, 300, 20, 20)
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "x_anahtar.json"), "w").write("{}"); open(os.path.join(d, "a.pdf"), "w").write("")
        assert HK.hk_aday_anahtar_bul(d).endswith("x_anahtar.json")
        open(os.path.join(d, "y_anahtar.json"), "w").write("{}")
        try:
            HK.hk_aday_anahtar_bul(d); raise AssertionError("iki anahtar kabul edilmemeliydi")
        except HK.HKHata:
            pass


def test_hakem_sema():
    with tempfile.TemporaryDirectory() as d:
        y1 = os.path.join(d, "a.json"); y2 = os.path.join(d, "b.json")
        json.dump({"sayfalar": {"1": {"karar": "EVET", "puan": 8, "gerekce": "x"}, "2": {"karar": "hayır", "puan": 2, "gerekce": ""}}}, open(y1, "w", encoding="utf-8"),
                  ensure_ascii=False)
        json.dump({"sayfalar": {"3": {"karar": "EVET", "puan": 7.5, "gerekce": "y"}}}, open(y2, "w", encoding="utf-8"))
        H = HK.hk_hakem_oku([y1, y2]); assert H[1]["karar"] == "EVET" and H[2]["karar"] == "HAYIR" and H[3]["puan"] == 7.5
        for kotu in ({"sayfalar": {"1": {"karar": "BELKI", "puan": 5}}}, {"sayfalar": {"1": {"karar": "EVET", "puan": 11}}}, {"1": {"karar": "EVET", "puan": 1}}):
            json.dump(kotu, open(y2, "w", encoding="utf-8"))
            try:
                HK.hk_hakem_oku([y2]); raise AssertionError(f"kabul etmemeliydi: {kotu}")
            except HK.HKHata:
                pass
        json.dump({"sayfalar": {"1": {"karar": "HAYIR", "puan": 1, "gerekce": ""}}}, open(y2, "w", encoding="utf-8"))
        try:
            HK.hk_hakem_oku([y1, y2]); raise AssertionError("çelişki kabul edilmemeliydi")
        except HK.HKHata:
            pass


def test_onay_secim():
    ev = [{"sayfa": i, "zaman": "gunluk" if i % 3 else "haftalik"} for i in range(1, 41)]     # günlük 27, haftalık 13
    S = HK.hk_onay_sec(ev); assert len(S) == 24 and sum(r["zaman"] == "haftalik" for r in S) == 12
    assert sorted(r["yeni_sayfa"] for r in S) == list(range(2, 26)) and len({r["sayfa"] for r in S}) == 24
    ev2 = [r for r in ev if r["zaman"] == "gunluk"][:20] + [r for r in ev if r["zaman"] == "haftalik"][:6]      # haftalık 6: günlükten tamamlanır
    S2 = HK.hk_onay_sec(ev2); assert len(S2) == 24 and sum(r["zaman"] == "haftalik" for r in S2) == 6
    S3 = HK.hk_onay_sec(ev[:15]); assert len(S3) == 15
    try:
        HK.hk_onay_sec(ev[:7]); raise AssertionError("< 8 kabul edilmemeliydi")
    except HK.HKHata:
        pass
    assert HK.hk_onay_sec(ev) == S


def test_esik_ve_kapak():
    assert HK._hk_sha() == HK._hk_sha(json.loads(json.dumps(HK.HK_ESIK)))
    t = HK.HK_KAPAK.format(M=300, N=31, BUNLAR="x")
    assert "56 sayfanda" in t and "5 sayfanın 3'üne" in t and "300 adaya baktı, 31 tanesini seçti" in t
    G = HK.HK_ESIK["aday"]; assert (G["gunluk"], G["haftalik"], G["bist_tavan"], G["dosya_sayfa"]) == (150, 150, 30, 50)


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_HAKEM as M\nns = dict(vars(M))\nns['hk_onay_sec'] = 1\nns['_CK_ONCE_HK'] = {'hk_onay_sec': id(M.hk_onay_sec)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_hk()')[0] + '_cakisma_kontrol_hk()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(HK.__file__)))
    assert "KAPALI" in r.stdout, (r.stdout, r.stderr[-500:])


# ---------------------------------------------------------------- EK 14 (A1 parti 3, A2 ogren, A3 iki aşamalı onay)
P1_SHA = "adc567936c3e3c7a90487e3efd4739e545791a7174d57bf41b8eaa88b9476854"
P2_SHA = "2585baa68ebc718b86003c60a316fe0dc69bf9c8fbf023a102dc8042be40c429"


def test_parti1_2_anahtar_degismedi():
    import MUM_IZI as MI
    for pt, sha in ((1, P1_SHA), (2, P2_SHA)):
        y = os.path.join(HK.HK_PARTI[pt]["klasor"], f"{HK.HK_PARTI[pt]['onek']}_anahtar.json")
        if not os.path.exists(y):
            print(f"  ({pt}. parti anahtarı yok: atlandı)"); continue
        assert MI._mi_sha(y) == sha, (pt, MI._mi_sha(y))
    assert HK._hk_sha() == "e3e7af9dd5c99a5461b14149e47692176c4afbb55aec4091f141b0ca593c3997"
    assert HK._hk_sha(HK.HK_ESIK_P2) == "b0e7d3db1475639cb397690bdacaae10df70b54c66bc9db6877cbe3c90bfba35"


def test_parti2_tekrar():
    y = os.path.join(HK.HK_PARTI[2]["klasor"], "mum_izi12_aday_anahtar.json")
    if not os.path.exists(y) or not os.path.exists(HK.HK_YOL["ham8"]):
        print("  (2. parti anahtarı / tarama ham dosyası yok: atlandı)"); return
    K = json.load(open(y, encoding="utf-8")); S = HK.hk_aday_sec(HK.hk_olaylar(), HK.hk_haric(2), HK.HK_ESIK_P2)
    assert [(r["sayfa"], r["sembol"], r["tarih"]) for r in S] == [(r["sayfa"], r["sembol"], r["bolge_son"]) for r in K["sayfalar"]]


def test_parti3_esik_ve_haric():
    P2, P3 = HK.HK_ESIK_P2, HK.HK_ESIK_P3
    for k in ("gunluk", "haftalik", "bist_oran", "dosya_sayfa", "eksik_izin"):
        assert P2[k] == P3[k], k                                                        # kural / katman payları 2. partiyle aynı
    assert P3["tohum"] != P2["tohum"] and HK.HK_PARTI[3]["klasor"].endswith("hakem_aday3") and HK.HK_PARTI[3]["onek"] == "mum_izi14_aday"
    on = [os.path.basename(x) for x in HK.HK_PARTI[3]["onceki"]]
    for f in ("mum_izi10_aday_anahtar.json", "mum_izi12_aday_anahtar.json", "mum_izi10_onay_anahtar.json", "MUM_IZI12_onay_anahtar.json"):
        assert f in on, f
    # sentetik: hariç listesi önceki anahtarların hepsini kapsar, seçim onlarla kesişmez
    o = _olay(500, 400, 7); eski = HK.HK_PARTI[3]["onceki"]; eski_y = HK.HK_YOL["anahtarlar"]
    with tempfile.TemporaryDirectory() as d:
        try:
            yol = []
            for i, sem in enumerate(([o[1]["sembol"], o[2]["sembol"]], [o[450]["sembol"]], [o[600]["sembol"]])):
                y = os.path.join(d, f"k{i}.json"); json.dump({"sayfalar": [{"sembol": s} for s in sem]}, open(y, "w")); yol.append(y)
            HK.HK_YOL["anahtarlar"] = yol[:1]; HK.HK_PARTI[3]["onceki"] = yol[1:]
            h = HK.hk_haric(3); assert h == {o[1]["sembol"], o[2]["sembol"], o[450]["sembol"], o[600]["sembol"]}
            S = HK.hk_aday_sec(o, h, dict(P3, gunluk=80, haftalik=80)); assert not ({r["sembol"] for r in S} & h) and len({r["sembol"] for r in S}) == len(S)
            HK.HK_PARTI[3]["onceki"] = yol[1:] + [os.path.join(d, "yok.json")]
            try:
                HK.hk_haric(3); raise AssertionError("eksik anahtar kabul edilmemeliydi")
            except HK.HKHata:
                pass
        finally:
            HK.HK_PARTI[3]["onceki"] = eski; HK.HK_YOL["anahtarlar"] = eski_y


def test_parti3_gercek():
    y = os.path.join(HK.HK_PARTI[3]["klasor"], "mum_izi14_aday_anahtar.json")
    if not os.path.exists(y):
        print("  (3. parti anahtarı henüz yok: atlandı)"); return
    K = json.load(open(y, encoding="utf-8")); S = K["sayfalar"]; h = HK.hk_haric(3)
    assert K["parti"] == 3 and K["esik_sha"] == HK._hk_sha(HK.HK_ESIK_P3) and sorted(r["sayfa"] for r in S) == list(range(1, len(S) + 1))
    assert not ({r["sembol"] for r in S} & h) and len({r["sembol"] for r in S}) == len(S) and max(r["bolge_son"] for r in S) <= "2022-12-31"
    for z in ("gunluk", "haftalik"):
        X = [r for r in S if r["zaman"] == z]; assert len(X) <= 300 and sum(r["pazar"] == "BIST" for r in X) <= int(0.2 * len(X) + 1e-9)
    if os.path.exists(HK.HK_YOL["ham8"]):
        S2 = HK.hk_aday_sec(HK.hk_olaylar(), h, HK.HK_ESIK_P3); assert [(r["sayfa"], r["sembol"]) for r in S2] == [(r["sayfa"], r["sembol"]) for r in S]


def test_kismen_kabul():
    with tempfile.TemporaryDirectory() as d:
        y = os.path.join(d, "a.json")
        json.dump({"sayfalar": {"1": {"karar": "KISMEN", "puan": 6, "gerekce": ""}, "2": {"karar": "kısmen", "puan": 5}, "3": {"karar": "EVET", "puan": 9}}},
                  open(y, "w", encoding="utf-8"), ensure_ascii=False)
        H = HK.hk_hakem_oku([y]); assert H[1]["karar"] == "KISMEN" and H[2]["karar"] == "KISMEN" and H[3]["karar"] == "EVET"


def _aday2(n=40):
    return [{"sayfa": i, "zaman": "gunluk" if i % 2 else "haftalik", "hakem_puan": float(i % 7)} for i in range(1, n + 1)]


def test_iki_asamali_sira():
    ad = _aday2(40); H2 = {}
    for r in ad:
        i = r["sayfa"]; H2[i] = {"karar": ("EVET" if i % 3 == 0 else "KISMEN" if i % 3 == 1 else "HAYIR"), "puan": float(i % 5), "gerekce": ""}
    H2[100] = {"karar": "EVET", "puan": 10.0, "gerekce": "1. aşama EVET olmayan sayfa: girmez"}
    S = HK.hk_onay_sec2(ad, H2); assert len(S) == 24 and sorted(r["yeni_sayfa"] for r in S) == list(range(2, 26))
    a = sorted([r for r in ad if H2[r["sayfa"]]["karar"] == "EVET"], key=lambda r: (-(r["hakem_puan"] + H2[r["sayfa"]]["puan"]), r["sayfa"]))
    b = sorted([r for r in ad if H2[r["sayfa"]]["karar"] == "KISMEN"], key=lambda r: (-(r["hakem_puan"] + H2[r["sayfa"]]["puan"]), r["sayfa"]))
    bek = [r["sayfa"] for r in (a + b)[:24]]
    assert {r["sayfa"] for r in S} == set(bek) and all(H2[r["sayfa"]]["karar"] != "HAYIR" for r in S) and 100 not in {r["sayfa"] for r in S}
    assert sum(r["sinif"] == "a" for r in S) == len(a) and all(r["sinif"] == "a" for r in S if H2[r["sayfa"]]["karar"] == "EVET")
    assert [r["sayfa"] for r in sorted(S, key=lambda r: r["yeni_sayfa"])] != bek                 # PDF sırası tohumlu karışık
    assert HK.hk_onay_sec2(ad, H2) == S
    # eşitlik: küçük sayfa önce
    e = [{"sayfa": 5, "zaman": "gunluk", "hakem_puan": 8.0}, {"sayfa": 3, "zaman": "gunluk", "hakem_puan": 7.0}]
    E2 = {5: {"karar": "KISMEN", "puan": 7.0, "gerekce": ""}, 3: {"karar": "KISMEN", "puan": 8.0, "gerekce": ""}}
    G = dict(HK.HK_ESIK_ONAY2, hedef=1); assert HK.hk_onay_sec2(e, E2, G)[0]["sayfa"] == 3
    # a sınıfı, puanı düşük olsa da b'den önce
    E3 = {5: {"karar": "KISMEN", "puan": 10.0, "gerekce": ""}, 3: {"karar": "EVET", "puan": 0.0, "gerekce": ""}}
    assert HK.hk_onay_sec2(e, E3, G)[0]["sayfa"] == 3
    # az aday: hepsi (HAYIR hariç); 2. aşamada eksik sayfa -> DUR; hepsi HAYIR -> DUR
    S4 = HK.hk_onay_sec2(ad[:10], H2); assert len(S4) == sum(H2[i]["karar"] != "HAYIR" for i in range(1, 11))
    try:
        HK.hk_onay_sec2(ad, {k: v for k, v in H2.items() if k != 7}); raise AssertionError("eksik 2. aşama sayfası kabul edilmemeliydi")
    except HK.HKHata:
        pass
    try:
        HK.hk_onay_sec2(e, {5: {"karar": "HAYIR", "puan": 1.0, "gerekce": ""}, 3: {"karar": "HAYIR", "puan": 1.0, "gerekce": ""}}); raise AssertionError("boş set")
    except HK.HKHata:
        pass


def test_kapak_n2():
    assert HK.hk_kapak_metni("{M} / {N} / {N2} / {K}", 600, 40, 20, 15) == "600 / 40 / 15 / 20"
    assert HK.hk_kapak_metni("{M} / {N} / {K}", 600, 40, 20) == "600 / 40 / 20"
    t = HK.hk_kapak_metni(None, 600, 40, 20, 15); assert "600 adaya" in t and "40 tanesine" in t and "15 tanesine" in t and "20 tanesi" in t
    assert HK.hk_kapak_metni(None, 300, 20, 20) == HK.HK_KAPAK.format(M=300, N=20, BUNLAR="bunlar onlar")          # eski kapak aynen


def _sentetik_pdf(y, n=25):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    with PdfPages(y) as pdf:
        for i in range(1, n + 1):
            fig = plt.figure(figsize=(8.3, 11.7)); fig.text(0.1, 0.9, f"KAYNAKSAYFA{i}"); pdf.savefig(fig); plt.close(fig)


def test_ogren_serit():
    import pypdf
    rng = np.random.default_rng(14); sec = ["EVET", "KISMEN", "HAYIR"]
    with tempfile.TemporaryDirectory() as d:
        kay = []; bek = {s: 0 for s in sec}
        for k in range(2):
            p = os.path.join(d, f"s{k}.pdf"); _sentetik_pdf(p); e = os.path.join(d, f"e{k}.json"); sf = {}
            for i in range(2, 26):
                s = sec[int(rng.integers(3))]; bek[s] += 1; sf[str(i)] = {"isaret": s}
            json.dump({"sayfalar": sf}, open(e, "w")); kay.append({"pdf": p, "etiket": e, "anahtar": None})
        J = HK.hk_ogren(cikti=d, kaynak=kay, ad="OG.pdf"); assert J["n"] == 48 and J["sinif"] == bek
        R = pypdf.PdfReader(os.path.join(d, "OG.pdf")); assert len(R.pages) == 48
        L = HK.hk_ogren_liste(kay); gor = {s: 0 for s in sec}; son = -1
        for i, (pg, r) in enumerate(zip(R.pages, L)):
            t = pg.extract_text(); yz = HK.HK_OGREN["yazi"][r["sinif"]]
            assert yz in t and f"Örnek {i + 1} / 48" in t and f"KAYNAKSAYFA{r['sayfa']}" in t, (i, t[:200])
            assert sum(v in t for v in HK.HK_OGREN["yazi"].values() if v != yz) == 0
            assert float(pg.mediabox.height) == 842.4 + HK.HK_OGREN["serit_pt"]                       # sayfa üstten genişledi, grafik örtülmez
            gor[r["sinif"]] += 1; o = sec.index(r["sinif"]); assert o >= son; son = o                      # sıra: EVET -> KISMEN -> HAYIR
        assert gor == bek
        try:
            HK.hk_ogren(cikti=d, kaynak=kay, ad="OG.pdf"); raise AssertionError("üzerine yazmamalıydı")
        except HK.HKHata:
            pass
        json.dump({"sayfalar": {str(i): {"isaret": "EVET"} for i in range(2, 25)}}, open(kay[0]["etiket"], "w"))
        try:
            HK.hk_ogren_liste(kay); raise AssertionError("eksik etiket sayfası kabul edilmemeliydi")
        except HK.HKHata:
            pass


def test_ogren_gercek_kaynak():
    """Gerçek kaynaklar: sha kapısı, 48 örnek, sınıf sayıları json ile aynı."""
    if not all(os.path.exists(k["pdf"]) and os.path.exists(k["etiket"]) for k in HK.HK_OGREN["kaynak"]):
        print("  (öğrenme kaynakları yok: atlandı)"); return
    L = HK.hk_ogren_liste(); assert len(L) == 48
    bek = {s: 0 for s in HK.HK_OGREN["sira"]}
    for k in HK.HK_OGREN["kaynak"]:
        for v in json.load(open(k["etiket"], encoding="utf-8"))["sayfalar"].values():
            bek[v["isaret"]] += 1
    assert {s: sum(r["sinif"] == s for r in L) for s in bek} == bek


def test_onay_geriye_uyum():
    """--hakem2 yok: MUM_IZI12 onayı aynı girdilerle yeniden kurulur; anahtar sayfaları, kapak ve PDF sha'sı eskisiyle birebir."""
    import MUM_IZI as MI
    c = HK.HK_YOL["cikti"]; ea = os.path.join(c, "MUM_IZI12_onay_anahtar.json"); hk = os.path.join(c, "hakem_aday2", "mum_izi12_hakem_birlesik.json")
    if not (os.path.exists(ea) and os.path.exists(hk) and os.path.exists(os.path.join(c, "hakem_aday2", "mum_izi12_aday_anahtar.json"))):
        print("  (MUM_IZI12 onay girdileri yok: atlandı)"); return
    E = json.load(open(ea, encoding="utf-8"))
    with tempfile.TemporaryDirectory() as d:
        try:
            K = HK.hk_onay([hk], d, os.path.join(c, "hakem_aday2"), E["kapak"], "MUM_IZI12")
        except Exception as ex:                       # fiyat verisi yoksa atla (yalnız veri yokluğu)
            if "veri" in str(ex).lower() or isinstance(ex, (FileNotFoundError, KeyError)):
                print(f"  (fiyat verisi yok: atlandı: {ex})"); return
            raise
        for k in ("aday_bakilan", "hakem_evet", "secilen", "secilen_zaman", "tohum", "kapak", "sayfalar", "aday_anahtar_sha"):
            assert K[k] == E[k], k
        assert K["pdf_sha"] == E["pdf_sha"] and "hakem2_dosyasi" not in K


def test_onay_iki_asamali_uctan_uca():
    """--hakem2 ile hk_onay (gerçek 2. parti adayları, sentetik 2. aşama): anahtarda iki hakemin kararı + puanı + sınıf; PDF = kapak + seçilen; HAYIR yok."""
    import pypdf
    c = HK.HK_YOL["cikti"]; hk = os.path.join(c, "hakem_aday2", "mum_izi12_hakem_birlesik.json")
    if not (os.path.exists(hk) and os.path.exists(os.path.join(c, "hakem_aday2", "mum_izi12_aday_anahtar.json"))):
        print("  (2. parti hakem girdileri yok: atlandı)"); return
    H1 = HK.hk_hakem_oku([hk]); ev = sorted(n for n, v in H1.items() if v["karar"] == "EVET")
    with tempfile.TemporaryDirectory() as d:
        y2 = os.path.join(d, "h2.json")
        json.dump({"sayfalar": {str(n): {"karar": ["EVET", "KISMEN", "HAYIR"][i % 3], "puan": float(i % 10), "gerekce": ""} for i, n in enumerate(ev)}},
                  open(y2, "w", encoding="utf-8"))
        try:
            K = HK.hk_onay([hk], d, os.path.join(c, "hakem_aday2"), "{M} {N} {N2} {K}", "DENEME", y2)
        except Exception as ex:
            if "veri" in str(ex).lower() or isinstance(ex, (FileNotFoundError, KeyError)):
                print(f"  (fiyat verisi yok: atlandı: {ex})"); return
            raise
        na = sum(i % 3 == 0 for i in range(len(ev))); nb = sum(i % 3 == 1 for i in range(len(ev)))
        assert K["iki_hakem_evet"] == na and K["secilen"] == min(24, na + nb) and K["secilen_sinif"]["a"] == min(24, na)
        assert K["kapak"] == f"{len(H1)} {len(ev)} {na} {K['secilen']}" and K["tohum"] == HK.HK_ESIK_ONAY2["tohum"]
        assert all(x["hakem2_karar"] in ("EVET", "KISMEN") and x["hakem_karar"] == "EVET" and "hakem2_puan" in x and x["sinif"] in ("a", "b") for x in K["sayfalar"])
        assert len(pypdf.PdfReader(os.path.join(d, "DENEME_ONAY.pdf")).pages) == K["secilen"] + 1


# ---------------------------------------------------------------- EK 16 İŞ B: --olcek
def _seri(n=200, tohum=16):
    rng = np.random.default_rng(tohum); C = 50 * np.exp(np.cumsum(rng.normal(0, 0.02, n))); O = C * (1 + rng.normal(0, 0.005, n))
    H = np.maximum(O, C) * (1 + rng.uniform(0, 0.02, n)); L = np.minimum(O, C) * (1 - rng.uniform(0, 0.02, n))
    return O, H, L, C


def test_olcek_boy_olcu():
    O, H, L, C = _seri(); t, m = 150, 20; B = HK.hk_boy_olcu(H, L, C, t, m)
    b = (H - L) / C; s = t - m + 1
    assert abs(B["boy_mutlak"] - np.median(b[s:t + 1]) * 100) < 1e-9 and abs(B["onceki"] - np.median(b[s - 120:s]) * 100) < 1e-9
    assert abs(B["oran"] - B["boy_mutlak"] / B["onceki"]) < 1e-12 and B["onceki_n"] == 120 and B["bolge_n"] == 20 and B["son_bar"] == t
    H2, L2, C2 = H.copy(), L.copy(), C.copy(); H2[t + 1:] *= 5; L2[t + 1:] = np.nan; C2[t + 1:] = -1     # gelecek bozulsa da sonuç aynı
    assert HK.hk_boy_olcu(H2, L2, C2, t, m) == B
    B2 = HK.hk_boy_olcu(H, L, C, 60, 20)                                                                  # önceki 41 bar (>= 40): oran var
    assert B2["onceki_n"] == 41 and np.isfinite(B2["oran"])
    B3 = HK.hk_boy_olcu(H, L, C, 55, 20); assert B3["onceki_n"] == 36 and not np.isfinite(B3["oran"])   # < 40: boş
    assert "yetersiz" in HK.hk_boy_satiri(B3)[1] and "önceki 120 mumunda" in HK.hk_boy_satiri(B)[0] and "önceki 41 mumunda" in HK.hk_boy_satiri(B2)[0]
    for t_, m_ in ((200, 20), (10, 20), (-1, 5)):
        try:
            HK.hk_boy_olcu(H, L, C, t_, m_); raise AssertionError("geçersiz t kabul edildi")
        except HK.HKHata:
            pass


def test_olcek_y_sinir_ve_adim():
    O, H, L, C = (x[:40].copy() for x in _seri()); H[3] = C[3] * 3; L[5] = C[5] * 0.2             # bölge dışında iki dev fitil
    kutu = (20, 39); y0, y1 = HK.hk_y_sinir(O, H, L, C, kutu)
    assert y1 < H[3] and y0 > L[5], "dev fitil ölçeği ezdi"
    assert y0 <= np.min(L[20:40]) and y1 >= np.max(H[20:40]), "bölge barı çerçeve dışında"
    H[30] = C[30] * 2.5; y0b, y1b = HK.hk_y_sinir(O, H, L, C, kutu); assert y1b >= H[30]                 # bölge içindeki dev fitil kesilmez
    BU = np.full(40, np.max(H) * 10); BA = np.full(40, 1e-6); y0c, y1c = HK.hk_y_sinir(O, H, L, C, kutu, BU=BU, BA=BA)
    lo, hi = HK.hk_y_sinir(O, H, L, C, kutu); sp = (hi - lo) / (1 + 2 * HK.HK_ESIK_OLCEK["pay"])
    assert (y1c - y0c) <= sp * (1 + 2 * HK.HK_ESIK_OLCEK["bant_pay"]) * (1 + 2 * HK.HK_ESIK_OLCEK["pay"]) + 1e-6   # bant genişlemesi sınırlı
    for lo_ in np.linspace(-90, -0.3, 40):
        for hi_ in np.linspace(0.2, 300, 40):
            s_, k = HK.hk_yuzde_adim(100 * (1 + lo_ / 100), 100 * (1 + hi_ / 100), 100.0)
            assert 4 <= len(k) <= 8 and s_ in HK.HK_ESIK_OLCEK["adim"] and 0.0 in k, (lo_, hi_, s_, k)
    assert HK._hk_yuzde_yazi(0.0) == "0" and HK._hk_yuzde_yazi(5) == "+%5" and HK._hk_yuzde_yazi(-2.5) == "−%2,5"


def test_olcek_sayfa_gelecege_bakmaz():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd
    import MUM_IZI_V2 as MV
    O, H, L, C = _seri(); ix = pd.bdate_range("2015-01-01", periods=len(C)); d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C}, index=ix)
    a = MV.mv_sablon()["tam"]["ohlc"]; r = {"tarih": str(ix[150].date()), "m": 20, "zaman": "gunluk"}
    fig = plt.figure(figsize=(8.3, 11.7)); o1 = HK._hk_sayfa_olcek(fig, d, r, a, 2); plt.close(fig)
    d2 = d.copy(); d2.iloc[151:] = d2.iloc[151:] * 7.0
    fig = plt.figure(figsize=(8.3, 11.7)); o2 = HK._hk_sayfa_olcek(fig, d2, r, a, 2); plt.close(fig)
    assert o1 == o2 and o1["seri_uzunluk_kullanilan"] == 151 and o1["son_bar_index"] == 150
    assert 4 <= o1["cizgi"] <= 8 and o1["y_sinir_yuzde"][0] < 0 < o1["y_sinir_yuzde"][1]


def _hk14_girdi():
    c = HK.HK_YOL["cikti"]; h = os.path.join(c, "hakem_aday3")
    hk = [os.path.join(h, f"mum_izi14_hakem_{x}.json") for x in "ABCD"]; h2 = os.path.join(h, "mum_izi14_hakem2.json"); ea = os.path.join(c, "MUM_IZI14_onay_anahtar.json")
    ok = all(os.path.exists(y) for y in hk + [h2, ea, os.path.join(h, "mum_izi14_aday_anahtar.json")])
    return c, h, hk, h2, ea, ok


def _veri_yok(ex):
    return "veri" in str(ex).lower() or isinstance(ex, (FileNotFoundError, KeyError))


def test_onay_geriye_uyum_14():
    """--olcek yok: MUM_IZI14 onayı aynı girdilerle yeniden kurulur; PDF sha ve anahtar sayfaları mühürlü eskisiyle birebir."""
    c, h, hk, h2, ea, ok = _hk14_girdi()
    if not ok:
        print("  (MUM_IZI14 onay girdileri yok: atlandı)"); return
    E = json.load(open(ea, encoding="utf-8"))
    with tempfile.TemporaryDirectory() as d:
        try:
            K = HK.hk_onay(hk, d, h, E["kapak"], "MUM_IZI14", h2)
        except Exception as ex:
            if _veri_yok(ex):
                print(f"  (fiyat verisi yok: atlandı: {ex})"); return
            raise
        assert K["pdf_sha"] == E["pdf_sha"] and K["sayfalar"] == E["sayfalar"] and K["kapak"] == E["kapak"]


def test_onay_olcek_uctan_uca():
    """--olcek: eski anahtar kopyasıyla geçici klasörde; bölge kimliği eşit, 18 sayfa, json'da hisse adı yok, pdf sha = repodaki ölçekli json; kapılar DUR."""
    import shutil
    import pypdf
    import MUM_IZI as MI
    c, h, hk, h2, ea, ok = _hk14_girdi()
    if not ok:
        print("  (MUM_IZI14 onay girdileri yok: atlandı)"); return
    E = json.load(open(ea, encoding="utf-8")); sha0 = MI._mi_sha(ea)
    with tempfile.TemporaryDirectory() as d:
        shutil.copy(ea, d)
        try:
            J = HK.hk_onay(hk, d, h, E["kapak"], "MUM_IZI14", h2, olcek=True)
        except Exception as ex:
            if _veri_yok(ex) and not isinstance(ex, HK.HKHata):
                print(f"  (fiyat verisi yok: atlandı: {ex})"); return
            raise
        yp = os.path.join(d, "MUM_IZI14_ONAY_OLCEKLI.pdf"); yj = os.path.join(d, "MUM_IZI14_onay_olcekli.json")
        R = pypdf.PdfReader(yp); assert len(R.pages) == 18 == J["sayfa_sayisi"]
        assert J["bolge_kimligi"]["esit"] and J["eski_anahtar_sha"] == sha0 and J["pdf_sha"] == MI._mi_sha(yp)
        assert J["kapak"] == E["kapak"] + " " + HK.HK_ESIK_OLCEK["kapak_ek"]
        assert [x["yeni_sayfa"] for x in J["sayfalar"]] == [x["yeni_sayfa"] for x in E["sayfalar"]] == list(range(2, 19))
        assert [x["zaman"] for x in J["sayfalar"]] == [x["zaman"] for x in E["sayfalar"]]
        jt = open(yj, encoding="utf-8").read(); pt = " ".join(p.extract_text() or "" for p in R.pages)
        for x in E["sayfalar"]:
            assert f'"{x["sembol"]}"' not in jt and x["bolge_son"] not in jt and x["bolge_bas"] not in jt, "json'da hisse / tarih"
        assert all("sembol" not in x and "bolge_son" not in x for x in J["sayfalar"]) and "kısmen" in pt and "Sayfa 18" in pt and "mum boyu" in pt
        rp = os.path.join(c, "MUM_IZI14_onay_olcekli.json")
        if os.path.exists(rp):                                      # yeniden üretim: repodaki ölçekli PDF ile birebir
            assert json.load(open(rp, encoding="utf-8"))["pdf_sha"] == J["pdf_sha"]
        for kapi in ("var", "kapak", "kimlik", "hakem"):            # kapılar
            with tempfile.TemporaryDirectory() as d2:
                E2 = json.loads(json.dumps(E)); kp = E["kapak"]; hh = list(hk)
                if kapi == "var":
                    shutil.copy(ea, d2); open(os.path.join(d2, "MUM_IZI14_onay_olcekli.json"), "w").write("{}")
                elif kapi == "kapak":
                    shutil.copy(ea, d2); kp = E["kapak"] + " x"
                elif kapi == "kimlik":
                    E2["sayfalar"][0]["bolge_son"] = "1999-01-01"; json.dump(E2, open(os.path.join(d2, "MUM_IZI14_onay_anahtar.json"), "w", encoding="utf-8"))
                else:
                    shutil.copy(ea, d2); hh = hk[:3]
                try:
                    HK.hk_onay(hh, d2, h, kp, "MUM_IZI14", h2, olcek=True); raise AssertionError(f"kapı açık kaldı: {kapi}")
                except HK.HKHata:
                    pass
                assert not os.path.exists(os.path.join(d2, "MUM_IZI14_ONAY_OLCEKLI.pdf")), kapi
    assert MI._mi_sha(ea) == sha0


def test_olcekli_repo_dosyalari():
    """Repodaki ölçekli set: json'daki pdf sha = dosya; eski anahtar / eski PDF sha'ları mühürlü dosyalarla aynı; 18 sayfa; hisse adı yok."""
    import pypdf
    import MUM_IZI as MI
    c = HK.HK_YOL["cikti"]; yj = os.path.join(c, "MUM_IZI14_onay_olcekli.json"); yp = os.path.join(c, "MUM_IZI14_ONAY_OLCEKLI.pdf")
    if not (os.path.exists(yj) and os.path.exists(yp)):
        print("  (ölçekli set henüz yok: atlandı)"); return
    J = json.load(open(yj, encoding="utf-8")); E = json.load(open(os.path.join(c, "MUM_IZI14_onay_anahtar.json"), encoding="utf-8"))
    assert J["pdf_sha"] == MI._mi_sha(yp) and len(pypdf.PdfReader(yp).pages) == 18
    assert J["eski_anahtar_sha"] == MI._mi_sha(os.path.join(c, "MUM_IZI14_onay_anahtar.json")) == "7f783321f23e8fdd9b5cfd87af92e5fa4332aea9e00cd139be520a4d1b766474"
    assert J["eski_pdf_sha"] == MI._mi_sha(os.path.join(c, "MUM_IZI14_ONAY.pdf")) == E["pdf_sha"] == "584b0db8bd0ff11897a95fdac07a973a5c7657c869774afa80d16dff98e29bf7"
    jt = open(yj, encoding="utf-8").read(); assert not any(f'"{x["sembol"]}"' in jt for x in E["sayfalar"]) and J["bolge_kimligi"]["esit"]


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
