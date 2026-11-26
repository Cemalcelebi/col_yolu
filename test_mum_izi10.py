"""test_mum_izi10 — MUM_IZI_HAKEM testleri (gerçek fiyat ve hakem verisi yok): aday seçim kuralları (sayı, hisse başına bir, BIST tavanı, hariç listesi,
karışık sıra, tohumla aynı), hakem şeması (sıkı; çelişki DUR), onay seçimi (>= 24 -> 24, 12 / 12 ve eksik dilim tamamlama; < 24 -> hepsi; < 8 -> DUR),
eşik mührü, çakışma kapısı.
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
