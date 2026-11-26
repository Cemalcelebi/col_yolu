"""test_mum_izi10 — MUM_IZI_HAKEM testleri (gerçek fiyat ve hakem verisi yok): aday seçim kuralları (sayı, hisse başına bir, BIST tavanı, hariç listesi,
karışık sıra, tohumla aynı), hakem şeması (sıkı; çelişki DUR), onay seçimi (>= 24 -> 24, 12 / 12 ve eksik dilim tamamlama; < 24 -> hepsi; < 8 -> DUR),
eşik mührü, çakışma kapısı. EK 14: 1. / 2. parti anahtar sha'ları değişmez, parti 3 hariç tutma, KISMEN kabulü, iki aşamalı sıra,
kapak {N2}, öğrenme şeridi (sayım / sıra / metin), --hakem2 olmadan onay geriye uyumu (MUM_IZI12 onayı birebir).
EK 16 İŞ B (--olcek): mum boyu ölçüsü (tanım, geleceğe bakma yok), sağlam dikey sınır, yüzde ekseni adımı, sayfa çizimi geleceğe bakmaz, --olcek olmadan
MUM_IZI14 onayı birebir (pdf sha), ölçekli basım uçtan uca (bölge kimliği, kapılar, hisse adı yok, pdf sha = commit edilen), repodaki ölçekli dosyalar.
EK 18 İŞ A: eski mühürler (parti 3 anahtarı, eşikler, MUM_IZI14_OGREN birebir), kapı sınırı (0,70 dahil / 0,7001 hariç), 40 bar kuralı, geleceğe
bakma, KESİK, parti 4 seçimi ve hariç tutma, havuz sayımı, HK-O4 (12'ye tamamlama), parti 4 gerçek anahtar (ORAN bağımsız yeniden hesap, seçim yeniden
üretimi), yeni ölçekli onay uçtan uca, ölçekli öğrenme dosyası (65 örnek, şerit = json).
EK 20: katman sınırı (0,65 / 0,70), katmanlı seçim (6 / 6 / 6 / 6, hariç, tohum tekrarı, kapılar), gerçek getirisiz sayım, uçtan uca (iki koşu aynı pdf sha,
PDF'te katman / hakem / hisse / tarih yok, repodaki set birebir), MUM_IZI18 onay seti birebir yeniden üretim.
EK 22 (--gecmis): eşik / kapak, iki hariç anahtar birleşimi ve kapıları, gerçek getirisiz sayım (75; 10 / 17 / 28 / 20), sayfa geleceğe bakmaz (PNG bayt),
uzak görünüm 120 / az / < 40 DUR, kutu iki grafikte aynı barlar, uçtan uca (iki koşu aynı sha, PDF'te katman / hisse / tarih yok), eski komut birebir.
Çalıştır: python test_mum_izi10.py [süzgeç ...]   (ör. python test_mum_izi10.py ek20)"""
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


# ---------------------------------------------------------------- EK 18 İŞ A: mum boyu kapısı, parti 4, yeni ölçekli onay, ölçekli öğrenme
P3_SHA = "30bcf8948a3b4cde1f5b12cbf4abedbff5de2b336443fccfb85d3b752ce0e479"
OGREN14_SHA = "0ce66761b4149175fc9139097e8ba83df0bfd4ddd5f76691f345b96876bbfe66"


def test_ek18_eski_muhurler():
    """Eski partilerin anahtar / eşik sha'ları ve eski öğrenme dosyası değişmez (yeniden üretilir)."""
    import MUM_IZI as MI
    y = os.path.join(HK.HK_PARTI[3]["klasor"], "mum_izi14_aday_anahtar.json")
    if os.path.exists(y):
        assert MI._mi_sha(y) == P3_SHA
    assert HK._hk_sha(HK.HK_ESIK_P3) == "ddac418b37d0f5071822e4811709bd0084b277b953418a34dcab357815670246"
    assert HK._hk_sha(HK.HK_ESIK_OLCEK) == "31420ca2c67457990378fabf093f40a2ad32723f46c88f3cc3c46460d9f6814a"
    assert HK._hk_sha(HK.HK_ESIK_ONAY2) == "c4b077a3f0e5453405cc479751dd3d293518cb17f57f061a1367b3311f5619f3"
    assert [k for k in HK.HK_PARTI if not HK.HK_PARTI[k].get("olcek")] == [1, 2, 3] and HK.HK_PARTI[4]["olcek"]
    og = os.path.join(HK.HK_YOL["cikti"], "MUM_IZI14_OGREN.pdf")
    if os.path.exists(og) and all(os.path.exists(k["pdf"]) for k in HK.HK_OGREN["kaynak"]):
        assert MI._mi_sha(og) == OGREN14_SHA
        with tempfile.TemporaryDirectory() as d:
            J = HK.hk_ogren(cikti=d); assert J["sha"] == OGREN14_SHA, "eski ogren çıktısı değişti"
    for k in (1, 2, 3):                                          # eski partiler ölçekli onay yoluna sapmaz
        if os.path.exists(HK.HK_PARTI[k]["klasor"]):
            assert not HK._hk_olcek_parti_mi(HK.HK_PARTI[k]["klasor"])


def test_ek18_kapi_siniri():
    G = HK.HK_ESIK_P4; assert G["kapi"]["oran_en_cok"] == 0.70 and G["kapi"]["cok_kucuk"] == 0.50
    assert HK.hk_kapi(0.70) and HK.hk_kapi(0.6999) and not HK.hk_kapi(0.7001) and not HK.hk_kapi(float("nan")) and not HK.hk_kapi(None)
    assert HK.hk_katman(0.50) == "ÇOK KÜÇÜK" and HK.hk_katman(0.5001) == "KÜÇÜK" and HK.hk_katman(0.70) == "KÜÇÜK" and HK.hk_katman(0.7001) is None


def _ek18_veri(n=260, tohum=18):
    import pandas as pd
    O, H, L, C = _seri(n, tohum); ix = pd.bdate_range("2015-01-01", periods=n)
    H = H.copy(); L = L.copy(); H[150:170] = np.maximum(O, C)[150:170] * 1.001; L[150:170] = np.minimum(O, C)[150:170] * 0.999      # küçük mumlu bölge
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C}, index=ix)


def test_ek18_oran_40bar_gelecek():
    """ORAN = hk_boy_olcu (tek tanım); önceki 40 bar aday, 39 bar değil; bölge sonrası barlar bozulunca ORAN aynı; KESİK aşımı DUR."""
    d = _ek18_veri(); ix = d.index
    olay = [{"zaman": "gunluk", "pazar": "ABD", "sembol": "X", "tarih": str(ix[169].date()), "m": 20, "evren": True},
            {"zaman": "gunluk", "pazar": "ABD", "sembol": "X", "tarih": str(ix[59].date()), "m": 20, "evren": True},      # önceki 40 bar
            {"zaman": "gunluk", "pazar": "ABD", "sembol": "X", "tarih": str(ix[58].date()), "m": 20, "evren": True}]      # önceki 39 bar
    R, sak = HK.hk_olay_oran(olay, veri=lambda z, p: {"X": d}, sakla=True)
    B = HK.hk_boy_olcu(d.High.to_numpy(float), d.Low.to_numpy(float), d.Close.to_numpy(float), 169, 20)
    assert R[0]["oran"] == B["oran"] and R[0]["oran"] < 0.5 and R[0]["katman"] == "ÇOK KÜÇÜK" and ("gunluk", "ABD", "X") in sak
    assert R[1]["onceki_n"] == 40 and np.isfinite(R[1]["oran"]) and R[2]["onceki_n"] == 39 and not np.isfinite(R[2]["oran"]) and R[2]["katman"] is None
    assert not HK.hk_kapi(R[2]["oran"])
    d2 = d.copy(); d2.iloc[170:] = d2.iloc[170:] * 9.0; d2.iloc[170:, 2] = d2.iloc[170:, 1] * 0.1
    R2, _ = HK.hk_olay_oran(olay[:1], veri=lambda z, p: {"X": d2}); assert R2[0]["oran"] == R[0]["oran"]
    import pandas as pd
    dk = d.copy(); dk.index = pd.bdate_range("2022-06-01", periods=len(d))
    try:
        HK.hk_olay_oran([dict(olay[0], tarih=str(dk.index[-1].date()))], veri=lambda z, p: {"X": dk}); raise AssertionError("KESİK aşımı kabul edildi")
    except HK.HKHata:
        pass


def _ek18_olay(tohum=4):
    rng = np.random.default_rng(tohum); o = []
    for z, n in (("gunluk", 500), ("haftalik", 60)):
        for i in range(n):
            p = ["ABD", "AVR", "BIST"][int(rng.integers(3))]; orn = float(rng.uniform(0.3, 1.6)) if rng.random() > 0.05 else float("nan")
            o.append({"zaman": z, "pazar": p, "sembol": f"{z[0]}{p}{int(rng.integers(0, 300))}", "tarih": f"2020-02-{1 + i % 28:02d}", "m": 20, "k": 8, "S": 0.5,
                      "evren": bool(rng.random() > 0.1), "oran": orn, "katman": HK.hk_katman(orn)})
    return o


def test_ek18_secim_ve_haric():
    o = _ek18_olay(); h = {o[0]["sembol"], o[3]["sembol"], o[510]["sembol"]}
    G = dict(HK.HK_ESIK_P4, gunluk=40, haftalik=300); S = HK.hk_aday_sec4(o, h, G)
    X = {z: [r for r in S if r["zaman"] == z] for z in ("gunluk", "haftalik")}
    uygun_h = {r["sembol"] for r in o if r["zaman"] == "haftalik" and r["evren"] and HK.hk_kapi(r["oran"]) and r["sembol"] not in h}
    assert len(X["gunluk"]) == 40 and len(X["haftalik"]) == len(uygun_h) < 300                    # haftalık yetmedi: hepsi, günlükle doldurulmadı
    assert all(HK.hk_kapi(r["oran"]) and r["evren"] and r["oran"] <= 0.70 for r in S) and not ({r["sembol"] for r in S} & h)
    assert len({r["sembol"] for r in S}) == len(S) and sorted(r["sayfa"] for r in S) == list(range(1, len(S) + 1)) and HK.hk_aday_sec4(o, h, G) == S
    G2 = dict(HK.HK_ESIK_P4); S2 = HK.hk_aday_sec4(o, h, G2)                                    # hepsi < hedef: kapıdan geçen her yeni hisse alınır
    uygun_g = {r["sembol"] for r in o if r["zaman"] == "gunluk" and r["evren"] and HK.hk_kapi(r["oran"]) and r["sembol"] not in h} - uygun_h
    assert len(S2) == len(uygun_h) + len(uygun_g) and sum(r["pazar"] == "BIST" for r in S2) > 0.2 * len(S2) - 10   # BIST tavanı yok
    # hariç listesi parti 4: önceki bütün anahtarlar (eksik anahtar DUR)
    on = [os.path.basename(x) for x in HK.HK_PARTI[4]["onceki"]]
    for f in ("mum_izi10_aday_anahtar.json", "mum_izi12_aday_anahtar.json", "mum_izi14_aday_anahtar.json", "mum_izi10_onay_anahtar.json",
              "MUM_IZI12_onay_anahtar.json", "MUM_IZI14_onay_anahtar.json"):
        assert f in on, f
    eski = HK.HK_PARTI[4]["onceki"]
    try:
        HK.HK_PARTI[4]["onceki"] = eski + ["/yok/yok.json"]
        try:
            HK.hk_haric(4); raise AssertionError("eksik anahtar kabul edildi")
        except HK.HKHata:
            pass
    finally:
        HK.HK_PARTI[4]["onceki"] = eski


def test_ek18_havuz_say():
    o = _ek18_olay(); h = {o[1]["sembol"]}; pb = {(o[2]["zaman"], o[2]["sembol"], o[2]["tarih"])}
    V = HK.hk_havuz_say(o, h, pb); g = V["grup"]["tum"]["gunluk"]
    X = [r for r in o if r["zaman"] == "gunluk" and r["evren"]]; ok = np.array([r["oran"] for r in X]); ok = ok[np.isfinite(ok)]
    assert g["n"] == len(X) and g["n_oran"] == len(ok) and abs(g["pay_le_0.70"] - np.mean(ok <= 0.70)) < 1e-12 and g["n_le_0.50"] == int((ok <= 0.5).sum())
    assert g["kapi_gecen_olay"] == int((ok <= 0.70).sum()) and sum(g["katman_olay"].values()) == g["kapi_gecen_olay"]
    assert V["grup"]["parti_1_3"]["gunluk"]["n"] == int(o[2]["evren"] and o[2]["zaman"] == "gunluk")
    assert V["grup"]["hic_gosterilmemis"]["gunluk"]["n"] == sum(1 for r in X if r["sembol"] not in h)


def test_ek18_onay_sec4():
    ad = _aday2(40); H2 = {}
    for r in ad:
        i = r["sayfa"]; H2[i] = {"karar": ("EVET" if i % 3 == 0 else "KISMEN" if i % 3 == 1 else "HAYIR"), "puan": float(i % 5), "gerekce": ""}
    kis = [{"sayfa": 100 + i, "zaman": "gunluk", "hakem_puan": 6.0 + 0.4 * i} for i in range(10)] + [{"sayfa": 99, "zaman": "gunluk", "hakem_puan": 5.9}]
    assert HK.hk_onay_sec4(ad, kis, H2) == HK.hk_onay_sec2(ad, H2)                          # doldurma yok: EK 14 kuralıyla birebir
    az = ad[:6]; S = HK.hk_onay_sec4(az, kis, H2); nab = sum(H2[r["sayfa"]]["karar"] != "HAYIR" for r in az)
    c = [r for r in S if r["sinif"] == "c"]
    assert len(S) == 12 and len(c) == 12 - nab and sorted(r["yeni_sayfa"] for r in S) == list(range(2, 14))
    assert [r["sayfa"] for r in sorted(c, key=lambda r: (-r["hakem_puan"], r["sayfa"]))] == [109, 108, 107, 106, 105, 104, 103, 102][:len(c)]
    assert all(r["hakem_puan"] >= 6 for r in c)
    assert 99 not in {r["sayfa"] for r in S}
    S2 = HK.hk_onay_sec4(az, [r for r in kis if r["hakem_puan"] < 6], H2); assert len(S2) == nab        # puan < 6 doldurmaz
    try:
        HK.hk_onay_sec4([], [], {}); raise AssertionError("boş set kabul edildi")
    except HK.HKHata:
        pass


def _p4_anahtar():
    return os.path.join(HK.HK_PARTI[4]["klasor"], "mum_izi18_aday_anahtar.json")


def test_ek18_parti4_gercek():
    import pypdf
    import pandas as pd
    import MUM_IZI as MI
    import MUM_IZI_V2 as MV
    y = _p4_anahtar()
    if not os.path.exists(y):
        print("  (4. parti anahtarı henüz yok: atlandı)"); return
    K = json.load(open(y, encoding="utf-8")); S = K["sayfalar"]; h = HK.hk_haric(4)
    assert K["parti"] == 4 and K["esik_sha"] == HK._hk_sha(HK.HK_ESIK_P4) and K["olcek_sha"] == HK._hk_sha(HK.HK_ESIK_OLCEK)
    assert sorted(r["sayfa"] for r in S) == list(range(1, len(S) + 1)) and len({r["sembol"] for r in S}) == len(S) and not ({r["sembol"] for r in S} & h)
    assert max(r["bolge_son"] for r in S) <= "2022-12-31" and all(HK.hk_kapi(r["oran"]) and r["katman"] == HK.hk_katman(r["oran"]) for r in S)
    for z in ("gunluk", "haftalik"):
        n = sum(r["zaman"] == z for r in S); assert n == K["n_zaman"][z] <= 300 and K["eksik"][z] == 300 - n
    for f, sha in K["dosya_sha"].items():
        yp = os.path.join(HK.HK_PARTI[4]["klasor"], f); assert MI._mi_sha(yp) == sha
        a, b = K["dosya_sayfa"][f]; R = pypdf.PdfReader(yp); assert len(R.pages) == b - a + 1 <= 50
        t = R.pages[0].extract_text() or ""; assert f"Sayfa {a}" in t and "mum boyu" in t and "benziyor" not in t          # ölçekli, kutusuz
    rng = np.random.default_rng(1); Vc = {}
    for i in rng.choice(len(S), size=min(6, len(S)), replace=False):           # ORAN veriden bağımsız yeniden hesap
        r = S[int(i)]; k = (r["zaman"], r["pazar"])
        if k not in Vc:
            Vc[k] = MV.mv_veri(*k)
        d = Vc[k][r["sembol"]]; t = d.index.get_loc(pd.Timestamp(r["bolge_son"])); s = t - r["pencere"] + 1
        b = ((d.High - d.Low) / d.Close).to_numpy(float)[:t + 1]; on = b[max(0, s - 120):s]; on = on[np.isfinite(on)]
        assert abs(np.nanmedian(b[s:t + 1]) / np.median(on) - r["oran"]) < 1e-9 and len(on) >= 40 and str(d.index[s].date()) == r["bolge_bas"]
    if os.path.exists(HK.HK_YOL["ham8"]):                                       # seçim yeniden üretimi
        olo, _ = HK.hk_olay_oran([o for o in HK.hk_olaylar() if o["evren"]]); S2 = HK.hk_aday_sec4(olo, h)
        assert [(r["sayfa"], r["sembol"], r["tarih"]) for r in S2] == [(r["sayfa"], r["sembol"], r["bolge_son"]) for r in S]
        HV = json.load(open(os.path.join(HK.HK_PARTI[4]["klasor"], "mum_izi18_havuz_sayim.json"), encoding="utf-8"))["havuz"]
        assert json.loads(json.dumps(HK.hk_havuz_say(olo, h, HK.hk_parti_bolgeleri()))) == HV
    jt = open(os.path.join(HK.HK_PARTI[4]["klasor"], "mum_izi18_havuz_sayim.json"), encoding="utf-8").read()
    assert not any(f'"{r["sembol"]}"' in jt for r in S)


def test_ek18_onay_yeni_uctan_uca():
    """Parti 4 adaylarıyla sentetik iki hakem: yeni ölçekli set (anahtar + json + PDF); json'da hisse / tarih yok; kapılar DUR."""
    import pypdf
    y = _p4_anahtar()
    if not os.path.exists(y):
        print("  (4. parti anahtarı henüz yok: atlandı)"); return
    kl = HK.HK_PARTI[4]["klasor"]; assert HK._hk_olcek_parti_mi(kl)
    S = json.load(open(y, encoding="utf-8"))["sayfalar"]; n = [r["sayfa"] for r in S]
    with tempfile.TemporaryDirectory() as d:
        h1 = os.path.join(d, "h1.json"); h2 = os.path.join(d, "h2.json")
        k1 = {str(i): {"karar": ["EVET", "KISMEN", "HAYIR", "HAYIR"][j % 4], "puan": float(j % 10), "gerekce": ""} for j, i in enumerate(n)}
        json.dump({"sayfalar": k1}, open(h1, "w", encoding="utf-8"))
        ev = [i for i in n if k1[str(i)]["karar"] == "EVET"]
        json.dump({"sayfalar": {str(i): {"karar": ["EVET", "HAYIR", "KISMEN"][j % 3], "puan": 7.0, "gerekce": ""} for j, i in enumerate(ev)}},
                  open(h2, "w", encoding="utf-8"))
        J = HK.hk_onay([h1], d, kl, None, "DENEME18", h2, olcek=True)
        K = json.load(open(os.path.join(d, "DENEME18_onay_anahtar.json"), encoding="utf-8"))
        na = sum(j % 3 == 0 for j in range(len(ev))); nb = sum(j % 3 == 2 for j in range(len(ev)))
        assert K["secilen_sinif"]["a"] == min(24, na) and K["secilen"] == len(K["sayfalar"]) == J["sayfa_sayisi"] - 1
        if na + nb >= 12:
            assert K["doldurulan"] == 0 and K["secilen"] == min(24, na + nb)
        else:
            assert K["secilen"] == min(12, na + nb + sum(1 for i in n if k1[str(i)]["karar"] == "KISMEN" and k1[str(i)]["puan"] >= 6)) and "tamamlandı" in K["kapak"]
        R = pypdf.PdfReader(os.path.join(d, "DENEME18_ONAY_OLCEKLI.pdf")); assert len(R.pages) == K["secilen"] + 1
        t = " ".join(p.extract_text() or "" for p in R.pages); assert "kısmen" in t and "mum boyu" in t and "%30" in t
        jt = open(os.path.join(d, "DENEME18_onay_olcekli.json"), encoding="utf-8").read()
        assert not any(f'"{x["sembol"]}"' in jt or x["bolge_son"] in jt for x in K["sayfalar"]) and all("oran" in x for x in K["sayfalar"])
        assert all(x["oran"] <= 0.70 for x in K["sayfalar"]) and J["pdf_sha"] == K["pdf_sha"]
        for kapi in ("var", "eksik_hakem", "hakem2_yok"):
            with tempfile.TemporaryDirectory() as d2:
                hh, hh2 = [h1], h2
                if kapi == "var":
                    open(os.path.join(d2, "DENEME18_onay_anahtar.json"), "w").write("{}")
                elif kapi == "eksik_hakem":
                    k2 = dict(k1); k2.pop(str(n[0])); y1 = os.path.join(d2, "e.json"); json.dump({"sayfalar": k2}, open(y1, "w")); hh = [y1]
                else:
                    hh2 = None
                try:
                    HK.hk_onay(hh, d2, kl, None, "DENEME18", hh2, olcek=True); raise AssertionError(f"kapı açık: {kapi}")
                except HK.HKHata:
                    pass
                assert not os.path.exists(os.path.join(d2, "DENEME18_ONAY_OLCEKLI.pdf"))


def test_ek18_ogren_olcek():
    import pypdf
    G = HK.HK_OGREN2
    if not all(os.path.exists(k["etiket"]) and os.path.exists(k["anahtar"]) for g in G["gruplar"] for k in g["kaynak"]):
        print("  (öğrenme kaynakları yok: atlandı)"); return
    L = HK.hk_ogren_liste2(); assert len(L) == 65 and [r["ornek"] for r in L] == list(range(1, 66))
    for g in G["gruplar"]:
        bek = {s: 0 for s in G["sira"]}
        for k in g["kaynak"]:
            for v in json.load(open(k["etiket"], encoding="utf-8"))["sayfalar"].values():
                bek[v["isaret"]] += 1
        assert {s: sum(1 for r in L if r["grup"] == g["ad"] and r["sinif"] == s) for s in G["sira"]} == bek, g["ad"]
    assert sum(r["grup"] == "olcekli" for r in L) == 17 and all(r["grup"] == "olcekli" for r in L[:17])
    son = (-1, -1)
    for r in L:
        o = (r["grup_i"], G["sira"].index(r["sinif"])); assert o >= son; son = o
    yp = os.path.join(HK.HK_YOL["cikti"], G["ad"])
    if os.path.exists(yp):
        R = pypdf.PdfReader(yp); assert len(R.pages) == 65
        for pg, r in zip(R.pages, L):
            t = pg.extract_text() or ""; yz = f"{r['yazi_on']}: {G['yazi'][r['sinif']]}"
            assert yz in t and f"Örnek {r['ornek']} / 65" in t and "mum boyu" in t, (r["ornek"], t[:120])
            assert sum(f"{r['yazi_on']}: {v}" in t for s, v in G["yazi"].items() if s != r["sinif"]) == 0
            assert float(pg.mediabox.height) == 842.4 + G["serit_pt"]
            for x in ("sembol", "bolge_son"):
                assert r[x] not in t
    with tempfile.TemporaryDirectory() as d:                                  # eksik etiket sayfası DUR
        G2 = json.loads(json.dumps(G)); k = G2["gruplar"][0]["kaynak"][0]; E = json.load(open(k["etiket"], encoding="utf-8")); E["sayfalar"].pop("2")
        k["etiket"] = os.path.join(d, "e.json"); json.dump(E, open(k["etiket"], "w", encoding="utf-8"))
        try:
            HK.hk_ogren_liste2(G2); raise AssertionError("eksik etiket kabul edildi")
        except HK.HKHata:
            pass


# ---------------------------------------------------------------- EK 20: katmanlı ölçekli onay seti (kapı mı hakem mi)
P4_SHA = "a859f79924ae145eeb32597ca6734c54ae844185b1fd8e75caec6747b0961744"
EK18_MUHUR = {"hakem_aday4/mum_izi18_hakem_A.json": "710fd0afb0f1b70ad7d4a6aed97bd86d78f7ca021efac3f30c18527b949c249b",
              "hakem_aday4/mum_izi18_hakem2.json": "ec71e3109ed731fb19dd46203fdadb8ec2f27359fcd69508e888e58bcf327597",
              "MUM_IZI18_ONAY_OLCEKLI.pdf": "75e563dd498a536cda6b436e27a65f1387d7d687e1285e319dcbc828d4123187"}
_VC20 = {}


def _veri20(z, p):
    import MUM_IZI_V2 as MV
    if (z, p) not in _VC20:
        _VC20[(z, p)] = MV.mv_veri(z, p)
    return _VC20[(z, p)]


def _ek20_girdi():
    c = HK.HK_YOL["cikti"]; kl = HK.HK_PARTI[4]["klasor"]
    h = os.path.join(kl, "mum_izi18_hakem_A.json"); e = os.path.join(c, "MUM_IZI18_onay_anahtar.json")
    return c, kl, h, e, all(os.path.exists(x) for x in (h, e, _p4_anahtar()))


def test_ek20_katman_siniri():
    G = HK.HK_ESIK_ONAY5; assert G["tohum"] == 20 and G["katman_basi"] == 6 and G["oran_esik"] == 0.65 and len(G["katmanlar"]) == 4
    k = HK.hk_katman5
    assert k("KISMEN", 0.65) == G["katmanlar"][0] and k("KISMEN", 0.6501) == G["katmanlar"][1] and k("KISMEN", 0.70) == G["katmanlar"][1]
    assert k("HAYIR", 0.30) == G["katmanlar"][2] and k("HAYIR", 0.69) == G["katmanlar"][3]
    for kr, o in (("EVET", 0.5), ("KISMEN", 0.7001), ("HAYIR", float("nan")), ("HAYIR", None), ("X", 0.5)):
        try:
            k(kr, o); raise AssertionError(f"kabul edildi: {kr} {o}")
        except HK.HKHata:
            pass


def _ek20_sentetik(n=80, tohum=7):
    rng = np.random.default_rng(tohum); A = []; H = {}
    for i in range(1, n + 1):
        A.append({"sayfa": i, "zaman": "gunluk" if i % 5 else "haftalik", "oran": [0.45, 0.60, 0.66, 0.69][(i // 2) % 4] + float(rng.uniform(0, 0.009))})
        H[i] = {"karar": "KISMEN" if i % 2 else "HAYIR", "puan": float(i % 10), "gerekce": ""}
    return A, H


def test_ek20_secim_sentetik():
    """Katman başına 6, hariç tutma, tohum tekrarı, sayfa sırası karışık, kapılar (EVET / hakem eksik / sayım / katman < 6) DUR."""
    A, H = _ek20_sentetik(); G = dict(HK.HK_ESIK_ONAY5, beklenen=None); hs = {1, 2, 3}
    s, S = HK.hk_katman_sec(A, H, hs, G); s2, S2 = HK.hk_katman_sec(A, H, hs, G); assert S == S2 and s == s2
    assert s["kalan"] == len(A) - 3 and sum(v for k, v in s.items() if k != "kalan") == s["kalan"]
    assert sorted(r["yeni_sayfa"] for r in S) == list(range(2, 26)) and not ({r["sayfa"] for r in S} & hs)
    assert all(sum(r["katman"] == k for r in S) == 6 for k in G["katmanlar"]) and len({r["sayfa"] for r in S}) == 24
    assert [r["katman"] for r in sorted(S, key=lambda r: r["yeni_sayfa"])] != [k for k in G["katmanlar"] for _ in range(6)]   # karışık sıra
    assert all(r["katman"] == HK.hk_katman5(H[r["sayfa"]]["karar"], r["oran"]) and r["hakem_karar"] == H[r["sayfa"]]["karar"] for r in S)
    _, S3 = HK.hk_katman_sec(A, H, hs, dict(G, tohum=21)); assert S3 != S                                  # tohum seçimi belirler
    H2 = dict(H); H2[10] = {"karar": "EVET", "puan": 9.0, "gerekce": ""}
    H3 = dict(H); H3.pop(10)
    for ad_, aa, hh, hx, gg in (("evet", A, H2, hs, G), ("eksik", A, H3, hs, G), ("sayim", A, H, hs, dict(G, beklenen={"kalan": 1})),
                                ("az", A[:20], {i: H[i] for i in range(1, 21)}, set(), G), ("yabanci", A, H, {999}, G)):
        try:
            HK.hk_katman_sec(aa, hh, hx, gg); raise AssertionError(f"kapı açık: {ad_}")
        except HK.HKHata:
            pass
    s4, _ = HK.hk_katman_sec(A, H2, hs | {10}, G); assert s4["kalan"] == len(A) - 4                         # EVET hariçteyse sorun yok


def test_ek20_gercek_sayim():
    """Gerçek girdiler: getirisiz sayım iş tanımıyla aynı (99; 16 / 23 / 34 / 26), seçim 6 / 6 / 6 / 6, hariç 12 sayfa seçilmez, tekrar aynı."""
    c, kl, h, e, ok = _ek20_girdi()
    if not ok:
        print("  (EK 20 girdileri yok: atlandı)"); return
    import MUM_IZI as MI
    A = json.load(open(_p4_anahtar(), encoding="utf-8"))["sayfalar"]; H = HK.hk_hakem_oku([h]); E = json.load(open(e, encoding="utf-8"))
    hs = {int(x["aday_sayfa"]) for x in E["sayfalar"]}; assert len(hs) == 12 and E["aday_anahtar_sha"] == MI._mi_sha(_p4_anahtar()) == P4_SHA
    s, S = HK.hk_katman_sec(A, H, hs); assert s == HK.HK_ESIK_ONAY5["beklenen"] and HK.hk_katman_sec(A, H, hs) == (s, S)
    assert all(sum(r["katman"] == k for r in S) == 6 for k in HK.HK_ESIK_ONAY5["katmanlar"]) and not ({r["sayfa"] for r in S} & hs)
    bag = {}                                                                     # bağımsız sayım
    for r in A:
        if r["sayfa"] in hs:
            continue
        kk = (H[r["sayfa"]]["karar"], r["oran"] <= 0.65); bag[kk] = bag.get(kk, 0) + 1
    assert bag == {("KISMEN", True): 16, ("KISMEN", False): 23, ("HAYIR", True): 34, ("HAYIR", False): 26}


def test_ek20_onay_uctan_uca():
    """İki koşu aynı pdf sha; 25 sayfa; kapak metni iş tanımındaki metin; PDF metninde katman / hakem kararı / hisse / tarih yok; json'da hisse / tarih /
    katman yok; repodaki MUM_IZI20 çıktıları birebir; eski mühürlü dosyalar değişmez; kapılar (çıktı var, yanlış hariç, --ad yok) DUR."""
    import pypdf
    import MUM_IZI as MI
    c, kl, h, e, ok = _ek20_girdi()
    if not ok:
        print("  (EK 20 girdileri yok: atlandı)"); return
    m0 = {k: MI._mi_sha(os.path.join(c, k)) for k in EK18_MUHUR}; e0 = MI._mi_sha(e)
    assert m0 == EK18_MUHUR, "mühürlü EK 18 dosyası değişti"
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        try:
            J1 = HK.hk_onay_katman([h], e, d1, kl, "MUM_IZI20", veri=_veri20)
        except Exception as ex:
            if _veri_yok(ex) and not isinstance(ex, HK.HKHata):
                print(f"  (fiyat verisi yok: atlandı: {ex})"); return
            raise
        J2 = HK.hk_onay_katman([h], e, d2, kl, "MUM_IZI20", veri=_veri20)
        assert J1["pdf_sha"] == J2["pdf_sha"] and J1["anahtar_sha"] == J2["anahtar_sha"], "tohum tekrarı: aynı girdi farklı çıktı"
        K = json.load(open(os.path.join(d1, "MUM_IZI20_onay_anahtar.json"), encoding="utf-8")); yp = os.path.join(d1, "MUM_IZI20_ONAY_OLCEKLI.pdf")
        assert K["secilen"] == 24 and sorted(x["yeni_sayfa"] for x in K["sayfalar"]) == list(range(2, 26)) and K["pdf_sha"] == MI._mi_sha(yp)
        assert set(K["secilen_katman"].values()) == {6} and K["sayim"] == HK.HK_ESIK_ONAY5["beklenen"]
        assert K["kapak"] == HK.HK_KAPAK5.replace("{K}", "24") and K["kapak"].startswith("Bu sette 24 bölge var.")
        assert not ({x["aday_sayfa"] for x in K["sayfalar"]} & set(K["haric_aday_sayfa"])) and len(K["haric_aday_sayfa"]) == 12
        R = pypdf.PdfReader(yp); assert len(R.pages) == 25
        pt = " ".join(p.extract_text() or "" for p in R.pages); tek = " ".join(pt.split())
        assert "Bu sette 24 bölge var." in tek and "mum boyu" in pt and "kısmen" in pt and "Sayfa 25" in pt
        Hh = HK.hk_hakem_oku([h])
        for x in K["sayfalar"]:
            assert x["sembol"] not in pt and x["bolge_son"] not in pt and x["bolge_bas"] not in pt, "PDF'te hisse / tarih"
            g = Hh[x["aday_sayfa"]]["gerekce"].strip()
            assert not g or g[:40] not in pt, "PDF'te hakem gerekçesi"
        for yasak in HK.HK_ESIK_ONAY5["katmanlar"] + ["KISMEN", "HAYIR", "EVET", "katman", "Katman", "hakem kararı", "0,65 <", "<= 0,65"]:
            assert yasak not in pt, f"PDF metninde: {yasak}"
        jt = open(os.path.join(d1, "MUM_IZI20_onay_olcekli.json"), encoding="utf-8").read(); jo = json.loads(jt)
        assert not any(f'"{x["sembol"]}"' in jt or x["bolge_son"] in jt for x in K["sayfalar"]), "json'da hisse / tarih"
        assert all("katman" not in x and "hakem_karar" not in x for x in jo["sayfalar"]) and "KISMEN" not in jt and "HAYIR" not in jt
        assert [abs(x["oran"] - y["oran"]) < 1e-12 for x, y in zip(jo["sayfalar"], K["sayfalar"])] and all(x["oran"] <= 0.70 for x in jo["sayfalar"])
        rp = os.path.join(c, "MUM_IZI20_onay_anahtar.json")
        if os.path.exists(rp):                                                  # repodaki set yeniden üretilir
            RK = json.load(open(rp, encoding="utf-8")); assert RK["pdf_sha"] == J1["pdf_sha"] == MI._mi_sha(os.path.join(c, "MUM_IZI20_ONAY_OLCEKLI.pdf"))
            assert RK["sayfalar"] == K["sayfalar"] and MI._mi_sha(rp) == J1["anahtar_sha"]
        for kapi in ("var", "haric", "ad"):
            with tempfile.TemporaryDirectory() as d3:
                ee, aa = e, "MUM_IZI20"
                if kapi == "var":
                    open(os.path.join(d3, "MUM_IZI20_onay_olcekli.json"), "w").write("{}")
                elif kapi == "haric":
                    E2 = json.load(open(e, encoding="utf-8")); E2["sayfalar"][0]["sembol"] = "YOK"; ee = os.path.join(d3, "x.json")
                    json.dump(E2, open(ee, "w", encoding="utf-8"))
                else:
                    aa = None
                try:
                    HK.hk_onay_katman([h], ee, d3, kl, aa, veri=_veri20); raise AssertionError(f"kapı açık: {kapi}")
                except HK.HKHata:
                    pass
                assert not os.path.exists(os.path.join(d3, "MUM_IZI20_ONAY_OLCEKLI.pdf")), kapi
    assert {k: MI._mi_sha(os.path.join(c, k)) for k in EK18_MUHUR} == m0 and MI._mi_sha(e) == e0


def test_ek20_ek18_onay_birebir():
    """Eski komut çıktısı değişmedi: MUM_IZI18 ölçekli onay seti aynı girdilerle yeniden kurulur, pdf sha ve anahtar sayfaları mühürlü eskisiyle birebir."""
    import MUM_IZI as MI
    c, kl, h, e, ok = _ek20_girdi(); h2 = os.path.join(kl, "mum_izi18_hakem2.json")
    if not (ok and os.path.exists(h2)):
        print("  (EK 18 onay girdileri yok: atlandı)"); return
    E = json.load(open(e, encoding="utf-8")); ek = " " + HK.HK_KAPAK4_DOLDUR.format(C=E["doldurulan"])
    kp = E["kapak"][:-len(ek)] if E["doldurulan"] and E["kapak"].endswith(ek) else E["kapak"]
    with tempfile.TemporaryDirectory() as d:
        try:
            J = HK.hk_onay([h], d, kl, kp, "MUM_IZI18", h2, olcek=True)
        except Exception as ex:
            if _veri_yok(ex) and not isinstance(ex, HK.HKHata):
                print(f"  (fiyat verisi yok: atlandı: {ex})"); return
            raise
        K = json.load(open(os.path.join(d, "MUM_IZI18_onay_anahtar.json"), encoding="utf-8"))
        assert J["pdf_sha"] == E["pdf_sha"] == MI._mi_sha(os.path.join(c, "MUM_IZI18_ONAY_OLCEKLI.pdf")) and K["sayfalar"] == E["sayfalar"] and K["kapak"] == E["kapak"]
    assert HK._hk_sha(HK.HK_ESIK_ONAY4) == E["esik_onay4_sha"] and HK._hk_sha(HK.HK_ESIK_OLCEK) == E["esik_olcek_sha"]


# ---------------------------------------------------------------- EK 22: --gecmis (geçmişli sayfa)
EK22_KAPAK = ("Bu sette 24 bölge var. İstediğin gibi her sayfada artık iki grafik var: üstte bölgenin gerisi (önceki 120 mum) ve bölge, altta yakından bölge. "
              "Sonrası yok. Hepsi mum boyu şartını geçen adaylar (oran en çok 0,70); hakem seçmedi, karışık. Her sayfada bir kutuyu işaretle; en iyilere yıldız "
              "koyabilirsin. Önceki sette (gerisi görünmeden) 23 bölgenin 7'sine benziyor dedin.")
EK20_DOSYA = ("MUM_IZI20_ONAY_OLCEKLI.pdf", "MUM_IZI20_onay_anahtar.json", "MUM_IZI20_onay_olcekli.json")


def _ek22_girdi():
    c, kl, h, e, ok = _ek20_girdi(); e2 = os.path.join(c, "MUM_IZI20_onay_anahtar.json")
    return c, kl, h, [e, e2], ok and os.path.exists(e2)


def _ek22_muhur(c):
    import MUM_IZI as MI
    return {k: MI._mi_sha(os.path.join(c, k)) for k in list(EK18_MUHUR) + ["MUM_IZI18_onay_anahtar.json", "MUM_IZI18_onay_olcekli.json"] + list(EK20_DOSYA)
            if os.path.exists(os.path.join(c, k))}


def test_ek22_esik_ve_eski_muhur():
    """HK-O6 iş tanımıyla aynı (tohum 22, 6'şar, dört katman, beklenen sayım, 120 / 40); kapak metni iş tanımındaki metin; eski eşik sha'ları (HK-O5, HK-OL)
    MUM_IZI20 anahtarındakiyle aynı (eski çizim / seçim değişmedi)."""
    G = HK.HK_ESIK_ONAY6
    assert G["tohum"] == 22 and G["katman_basi"] == 6 and G["oran_esik"] == 0.65 and G["kapi_en_cok"] == 0.70
    assert G["katmanlar"] == HK.HK_ESIK_ONAY5["katmanlar"] and G["uzak_onceki"] == 120 and G["uzak_en_az"] == 40
    assert G["beklenen"] == {"kalan": 75, "KISMEN|oran<=0,65": 10, "KISMEN|0,65<oran<=0,70": 17, "HAYIR|oran<=0,65": 28, "HAYIR|0,65<oran<=0,70": 20}
    assert HK.HK_KAPAK6.replace("{K}", "24") == EK22_KAPAK
    assert HK.HK_ACIKLAMA6.startswith("Üst: bölgenin gerisi (önceki 120 mum) + bölge. Alt: yakından bölge.")
    y = os.path.join(HK.HK_YOL["cikti"], "MUM_IZI20_onay_anahtar.json")
    if os.path.exists(y):
        K = json.load(open(y, encoding="utf-8"))
        assert HK._hk_sha(HK.HK_ESIK_ONAY5) == K["esik_onay5_sha"] and HK._hk_sha(HK.HK_ESIK_OLCEK) == K["esik_olcek_sha"]


def test_ek22_haric_birlesik():
    """İki hariç anahtar birleşimi (12 + 24 = 36, çakışma yok); aynı anahtar iki kez, başka aday anahtarı, uyuşmayan sayfa, boş liste, olmayan dosya DUR."""
    c, kl, h, ee, ok = _ek22_girdi()
    if not ok:
        print("  (EK 22 girdileri yok: atlandı)"); return
    ay = _p4_anahtar(); Ad = {int(r["sayfa"]): r for r in json.load(open(ay, encoding="utf-8"))["sayfalar"]}
    hs, b = HK.hk_haric_birlesik(ee, Ad, ay)
    s1 = {int(x["aday_sayfa"]) for x in json.load(open(ee[0], encoding="utf-8"))["sayfalar"]}
    s2 = {int(x["aday_sayfa"]) for x in json.load(open(ee[1], encoding="utf-8"))["sayfalar"]}
    assert hs == s1 | s2 and len(s1) == 12 and len(s2) == 24 and not (s1 & s2) and [x["n"] for x in b] == [12, 24]
    with tempfile.TemporaryDirectory() as d:
        E = json.load(open(ee[1], encoding="utf-8")); E["sayfalar"][3]["sembol"] = "YOK"; yb = os.path.join(d, "b.json"); json.dump(E, open(yb, "w", encoding="utf-8"))
        E = json.load(open(ee[1], encoding="utf-8")); E["aday_anahtar_sha"] = "0" * 64; ys = os.path.join(d, "s.json"); json.dump(E, open(ys, "w", encoding="utf-8"))
        for ad_, L in (("iki kez", [ee[0], ee[0]]), ("bozuk", [ee[0], yb]), ("sha", [ys]), ("bos", []), ("yok", [os.path.join(d, "yok.json")])):
            try:
                HK.hk_haric_birlesik(L, Ad, ay); raise AssertionError(f"kapı açık: {ad_}")
            except HK.HKHata:
                pass


def test_ek22_gercek_sayim():
    """Gerçek girdiler: getirisiz sayım iş tanımıyla aynı (75; 10 / 17 / 28 / 20; bağımsız sayımla), seçim 6 / 6 / 6 / 6, gösterilmiş 36 sayfa seçilmez,
    tekrar aynı; yalnız MUM_IZI18 hariç tutulursa sayım kapısı DUR."""
    c, kl, h, ee, ok = _ek22_girdi()
    if not ok:
        print("  (EK 22 girdileri yok: atlandı)"); return
    ay = _p4_anahtar(); A = json.load(open(ay, encoding="utf-8"))["sayfalar"]; Ad = {int(r["sayfa"]): r for r in A}; H = HK.hk_hakem_oku([h])
    hs, _ = HK.hk_haric_birlesik(ee, Ad, ay); assert len(hs) == 36
    s, S = HK.hk_katman_sec(A, H, hs, HK.HK_ESIK_ONAY6); assert s == HK.HK_ESIK_ONAY6["beklenen"] and HK.hk_katman_sec(A, H, hs, HK.HK_ESIK_ONAY6) == (s, S)
    assert all(sum(r["katman"] == k for r in S) == 6 for k in HK.HK_ESIK_ONAY6["katmanlar"]) and not ({r["sayfa"] for r in S} & hs)
    assert sorted(r["yeni_sayfa"] for r in S) == list(range(2, 26)) and len({r["sayfa"] for r in S}) == 24
    bag = {}
    for r in A:
        if r["sayfa"] in hs:
            continue
        kk = (H[r["sayfa"]]["karar"], r["oran"] <= 0.65); bag[kk] = bag.get(kk, 0) + 1
    assert bag == {("KISMEN", True): 10, ("KISMEN", False): 17, ("HAYIR", True): 28, ("HAYIR", False): 20}
    _, S5 = HK.hk_katman_sec(A, H, hs, dict(HK.HK_ESIK_ONAY6, tohum=20)); assert S5 != S                  # tohum seçimi belirler
    hs1, _ = HK.hk_haric_birlesik(ee[:1], Ad, ay)
    try:
        HK.hk_katman_sec(A, H, hs1, HK.HK_ESIK_ONAY6); raise AssertionError("tek hariçle sayım kapısı açık")
    except HK.HKHata:
        pass


def _ek22_png(d, r, n=None):
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import MUM_IZI_V2 as MV
    a = MV.mv_sablon()["tam"]["ohlc"]; fig = plt.figure(figsize=tuple(HK.HK_ESIK_ONAY6["cizim"]["sayfa_boyu"]))
    try:
        o = HK._hk_sayfa_gecmis(fig, d, r, a, 2); b = io.BytesIO(); fig.savefig(b, format="png", dpi=40); return o, b.getvalue()
    finally:
        plt.close(fig)


def test_ek22_sayfa_gelecege_bakmaz():
    """Geçmişli sayfa: bölge sonrası barlar bozulunca / silinince ölçü ve görüntü (PNG bayt) aynı; uzak görünüm önceki 120 mum (az varsa olan kadar, < 40 DUR);
    bölge kutusu iki grafikte aynı barlar (m bar, pencerenin son m barı); ORAN EK 16 ölçüsüyle aynı."""
    import pandas as pd
    O, H, L, C = _seri(); ix = pd.bdate_range("2015-01-01", periods=len(C)); d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C}, index=ix)
    r = {"tarih": str(ix[150].date()), "m": 20, "zaman": "gunluk"}
    o1, p1 = _ek22_png(d, r)
    d2 = d.copy(); d2.iloc[151:] = d2.iloc[151:] * 7.0; d2.iloc[160, 1] = 1e6
    o2, p2 = _ek22_png(d2, r); o3, p3 = _ek22_png(d.iloc[:151], r)
    assert o1 == o2 == o3 and p1 == p2 == p3, "bölge sonrası sayfayı değiştirdi"
    assert o1["seri_uzunluk_kullanilan"] == 151 and o1["son_bar_index"] == 150 and o1["uzak_onceki_bar"] == 120 and o1["yakin_onceki_bar"] == 15
    assert o1["uzak"]["pencere_bar"] == 140 and o1["yakin"]["pencere_bar"] == 35
    for g in ("uzak", "yakin"):
        k0, k1 = o1[g]["kutu"]; assert k1 == o1[g]["pencere_bar"] - 1 and k1 - k0 + 1 == 20, g
        assert 4 <= o1[g]["cizgi"] <= 8 and o1[g]["y_sinir_yuzde"][0] < 0 < o1[g]["y_sinir_yuzde"][1]
    B = HK.hk_boy_olcu(H, L, C, 150, 20); assert o1["oran"] == B["oran"]
    o4, _ = _ek22_png(d, {"tarih": str(ix[80].date()), "m": 20, "zaman": "gunluk"}); assert o4["uzak_onceki_bar"] == 61 and o4["uzak"]["pencere_bar"] == 81
    try:
        _ek22_png(d, {"tarih": str(ix[55].date()), "m": 20, "zaman": "gunluk"}); raise AssertionError("< 40 önceki mum kabul edildi")
    except HK.HKHata:
        pass


def test_ek22_onay_uctan_uca():
    """İki koşu aynı pdf / anahtar sha; 25 sayfa; kapak metni aynen; PDF metninde katman / hakem kararı / hisse / tarih yok; json'da hisse / tarih / katman yok;
    anahtarda uzak_onceki_bar 40..120; repodaki MUM_IZI22 çıktıları birebir; mühürlü eski dosyalar değişmez; kapılar DUR, yarım PDF kalmaz."""
    import pypdf
    import MUM_IZI as MI
    c, kl, h, ee, ok = _ek22_girdi()
    if not ok:
        print("  (EK 22 girdileri yok: atlandı)"); return
    m0 = _ek22_muhur(c); assert {k: m0[k] for k in EK18_MUHUR} == EK18_MUHUR, "mühürlü EK 18 dosyası değişti"
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        try:
            J1 = HK.hk_onay_gecmis([h], ee, d1, kl, "MUM_IZI22", veri=_veri20)
        except Exception as ex:
            if _veri_yok(ex) and not isinstance(ex, HK.HKHata):
                print(f"  (fiyat verisi yok: atlandı: {ex})"); return
            raise
        J2 = HK.hk_onay_gecmis([h], ee, d2, kl, "MUM_IZI22", veri=_veri20)
        assert J1["pdf_sha"] == J2["pdf_sha"] and J1["anahtar_sha"] == J2["anahtar_sha"], "tohum tekrarı: aynı girdi farklı çıktı"
        K = json.load(open(os.path.join(d1, "MUM_IZI22_onay_anahtar.json"), encoding="utf-8")); yp = os.path.join(d1, "MUM_IZI22_ONAY_GECMISLI.pdf")
        assert K["secilen"] == 24 and sorted(x["yeni_sayfa"] for x in K["sayfalar"]) == list(range(2, 26)) and K["pdf_sha"] == MI._mi_sha(yp)
        assert set(K["secilen_katman"].values()) == {6} and K["sayim"] == HK.HK_ESIK_ONAY6["beklenen"] and K["kapak"] == EK22_KAPAK
        assert not ({x["aday_sayfa"] for x in K["sayfalar"]} & set(K["haric_aday_sayfa"])) and len(K["haric_aday_sayfa"]) == 36
        assert all(40 <= x["uzak_onceki_bar"] <= 120 for x in K["sayfalar"]) and all(x["oran"] <= 0.70 for x in K["sayfalar"])
        for k_ in ("yeni_sayfa", "aday_sayfa", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "pencere", "oran", "hakem_karar", "hakem_puan", "katman",
                   "uzak_onceki_bar"):
            assert all(k_ in x for x in K["sayfalar"]), k_
        R = pypdf.PdfReader(yp); assert len(R.pages) == 25
        pt = " ".join(p.extract_text() or "" for p in R.pages); tek = " ".join(pt.split())
        assert "Bu sette 24 bölge var." in tek and "Yakından" in pt and "gerisi" in pt and "kısmen" in pt and "Sayfa 25" in pt
        Hh = HK.hk_hakem_oku([h])
        for x in K["sayfalar"]:
            assert x["sembol"] not in pt and x["bolge_son"] not in pt and x["bolge_bas"] not in pt, "PDF'te hisse / tarih"
            g = Hh[x["aday_sayfa"]]["gerekce"].strip(); assert not g or g[:40] not in pt, "PDF'te hakem gerekçesi"
        for yasak in HK.HK_ESIK_ONAY6["katmanlar"] + ["KISMEN", "HAYIR", "EVET", "katman", "Katman", "hakem kararı", "0,65 <", "<= 0,65"]:
            assert yasak not in pt, f"PDF metninde: {yasak}"
        jt = open(os.path.join(d1, "MUM_IZI22_onay_olcekli.json"), encoding="utf-8").read(); jo = json.loads(jt)
        assert not any(f'"{x["sembol"]}"' in jt or x["bolge_son"] in jt or x["bolge_bas"] in jt for x in K["sayfalar"]), "json'da hisse / tarih"
        assert all("katman" not in x and "hakem_karar" not in x for x in jo["sayfalar"]) and "KISMEN" not in jt and "HAYIR" not in jt
        assert [x["uzak_onceki_bar"] for x in jo["sayfalar"]] == [x["uzak_onceki_bar"] for x in K["sayfalar"]]
        assert all(x["seri_uzunluk_kullanilan"] == x["son_bar_index"] + 1 for x in jo["sayfalar"]), "sonrası kullanıldı"
        rp = os.path.join(c, "MUM_IZI22_onay_anahtar.json")
        if os.path.exists(rp):                                                  # repodaki set yeniden üretilir
            RK = json.load(open(rp, encoding="utf-8")); assert RK["pdf_sha"] == J1["pdf_sha"] == MI._mi_sha(os.path.join(c, "MUM_IZI22_ONAY_GECMISLI.pdf"))
            assert RK["sayfalar"] == K["sayfalar"] and MI._mi_sha(rp) == J1["anahtar_sha"]
            assert MI._mi_sha(os.path.join(c, "MUM_IZI22_onay_olcekli.json")) == MI._mi_sha(os.path.join(d1, "MUM_IZI22_onay_olcekli.json"))
        for kapi in ("var", "tek_haric", "iki_kez", "ad"):
            with tempfile.TemporaryDirectory() as d3:
                hh, aa = ee, "MUM_IZI22"
                if kapi == "var":
                    open(os.path.join(d3, "MUM_IZI22_onay_olcekli.json"), "w").write("{}")
                elif kapi == "tek_haric":
                    hh = ee[:1]
                elif kapi == "iki_kez":
                    hh = [ee[0], ee[1], ee[1]]
                else:
                    aa = None
                try:
                    HK.hk_onay_gecmis([h], hh, d3, kl, aa, veri=_veri20); raise AssertionError(f"kapı açık: {kapi}")
                except HK.HKHata:
                    pass
                assert not os.path.exists(os.path.join(d3, "MUM_IZI22_ONAY_GECMISLI.pdf")), kapi
    assert _ek22_muhur(c) == m0, "mühürlü eski dosya değişti"


def test_ek22_eski_komut_birebir():
    """--gecmis verilmeyince eski komut (EK 20, tek --haric) aynı çıktıyı verir: komut satırından MUM_IZI20 seti yeniden kurulur, pdf / anahtar / json sha
    repodakiyle birebir. --haric iki anahtar --gecmis olmadan, --gecmis --katmanli olmadan DUR (dönüş 2)."""
    import MUM_IZI as MI
    c, kl, h, ee, ok = _ek22_girdi()
    if not (ok and all(os.path.exists(os.path.join(c, k)) for k in EK20_DOSYA)):
        print("  (EK 20 çıktıları yok: atlandı)"); return
    with tempfile.TemporaryDirectory() as d:
        try:
            rc = HK._hk_ana(["onay", "--olcek", "--katmanli", "--hakem", h, "--aday", kl, "--haric", ee[0], "--ad", "MUM_IZI20", "--cikti", d])
        except Exception as ex:
            if _veri_yok(ex) and not isinstance(ex, HK.HKHata):
                print(f"  (fiyat verisi yok: atlandı: {ex})"); return
            raise
        assert rc == 0
        for k in EK20_DOSYA:
            assert MI._mi_sha(os.path.join(d, k)) == MI._mi_sha(os.path.join(c, k)), f"eski çıktı değişti: {k}"
        assert HK._hk_ana(["onay", "--olcek", "--katmanli", "--hakem", h, "--aday", kl, "--haric", ee[0], ee[1], "--ad", "X", "--cikti", d]) == 2
        assert HK._hk_ana(["onay", "--olcek", "--gecmis", "--hakem", h, "--aday", kl, "--haric", ee[0], "--ad", "X", "--cikti", d]) == 2
        assert not any(f.startswith("X_") for f in os.listdir(d))


if __name__ == "__main__":
    adlar = [k for k in list(globals()) if k.startswith("test_") and (len(sys.argv) < 2 or any(a in k for a in sys.argv[1:]))]   # süzgeç: python test_mum_izi10.py ek20
    hata = 0
    for k in adlar:
        try:
            globals()[k](); print("GEÇTİ", k)
        except Exception as ex:   # her test ayrı raporlanır
            hata += 1; print("KALDI", k, type(ex).__name__, ex)
    print(f"{len(adlar) - hata} / {len(adlar)} geçti")
    sys.exit(1 if hata else 0)
