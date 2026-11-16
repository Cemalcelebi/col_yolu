"""SIKISMA_S7 testleri (pytest; her sınama assert eder). Çalıştırma: python -m pytest test_sikisma_s7.py -q   ya da   python test_sikisma_s7.py

1) SIKISMA_OBEK.py HEAD ile aynı ve sha = S5 ön kaydındaki KOD sha  2) ad kesişimi + çakışma kapısı  3) skaler = vektör ön süzgeç  4) Z1-Z6 ve sınıf
elle  5) sentetik DİP / YOL / orta  6) kırılım + kilit  7) ÖNEK DEĞİŞMEZLİĞİ (V_BIST 3 hisse x 5 kesim; yoksa sentetik) + gelecek bozma  8) S5 kutu
makinesi = COL_S6_TASLAK.pine listesi, S6 varsayılanı  9) ön yazım mührü + tasarım seçimi yeniden  10) kontrol kapısı  11) Pine varsayılanları, beklenen
blok, getiri etiketi yok  12) e-posta / anahtar yok.
"""
from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
warnings.filterwarnings("ignore")
import SIKISMA_S7 as S7  # noqa: E402
import SIKISMA_OBEK as SO  # noqa: E402
import SIKISMA_YENIDEN as SY  # noqa: E402

E7 = S7.SO7_ESIK
VERI_VAR = os.path.exists(os.path.join(SO.SO_YOL["veri"], "V_BIST.pkl"))


def _seri(segler, tohum=1, bas="2016-01-04"):
    """segler: [(gün, günlük kayma, getiri oynaklığı, mum yarı genişliği)] (test_sikisma_obek._seri ile aynı kurgu)."""
    rng = np.random.default_rng(tohum)
    r, w, sik = [], [], []
    for g, k, s, m in segler:
        r += list(k + rng.normal(0, s, g)); w += list(np.abs(rng.normal(m, m * 0.2, g))); sik += [m < 0.005] * g
    r = np.array(r); w = np.array(w); sik = np.array(sik); n = len(r)
    idx = pd.bdate_range(bas, periods=n)
    C = 100 * np.exp(np.cumsum(r))
    O = np.r_[C[0], C[:-1]] * np.where(sik, 1.0, 1 + rng.normal(0, 0.003, n))
    H = np.fmax(C, O) * (1 + w); L = np.fmin(C, O) * (1 - w)
    return SY.sy_veri_hazirla(pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.integers(1e5, 2e5, n).astype(float) * 100 / C},
                                           index=idx), SY.SY_ESIK)


ARKA = (400, 0.0, 0.01, 0.012)


def _dip(tohum=7):
    return _seri([ARKA, (60, -0.008, 0.004, 0.012), (45, 0.0, 0.0008, 0.002), (60, 0.0, 0.01, 0.012)], tohum)


def _yol(tohum=9):
    return _seri([ARKA, (60, 0.006, 0.004, 0.012), (45, 0.0004, 0.0008, 0.002), (60, 0.0, 0.01, 0.012)], tohum)


def _orta(tohum=3):
    return _seri([ARKA, (40, 0.008, 0.003, 0.012), (20, -0.008, 0.003, 0.012), (45, 0.0, 0.0008, 0.002), (60, 0.0, 0.01, 0.012)], tohum)


def test_obek_dosyasi_head_ile_ayni_ve_s5_kod_sha_tutar():
    yol = os.path.join(KOK, "SIKISMA_OBEK.py")
    r = subprocess.run(["git", "-C", KOK, "diff", "--quiet", "HEAD", "--", "SIKISMA_OBEK.py"], capture_output=True)
    assert r.returncode == 0, "SIKISMA_OBEK.py HEAD'den farklı"
    ok = SO.so_onkayit_dogrula(git=False)            # mühür + KOD / SC_KOD / SY_KOD sha (SAPMA olursa SOHata)
    assert ok["kod"] == SY._sy_sha_dosya(yol)


def test_ad_kesisimi_ve_cakisma_kapisi():
    ad7 = {n for n in dir(S7) if n.startswith(("so_s7", "_so7", "SO7", "_s7", "S7"))}
    diger = set()
    for f in os.listdir(KOK):
        if f.endswith(".py") and f != "SIKISMA_S7.py" and not f.startswith("test_"):
            try:
                tr = ast.parse(open(os.path.join(KOK, f), encoding="utf-8").read())
            except (SyntaxError, UnicodeDecodeError):
                continue
            for nd in tr.body:
                if isinstance(nd, (ast.FunctionDef, ast.ClassDef)):
                    diger.add(nd.name)
                elif isinstance(nd, ast.Assign):
                    diger |= {x.id for x in nd.targets if isinstance(x, ast.Name)}
    assert len(ad7) > 20 and not (ad7 & diger), sorted(ad7 & diger)
    g = {"so_s7_bolgeler": lambda: None, "__name__": "x"}
    try:
        exec(compile(open(os.path.join(KOK, "SIKISMA_S7.py"), encoding="utf-8").read(), "SIKISMA_S7.py", "exec"), g)
        assert False, "çakışma kapısı durmadı"
    except RuntimeError as ex:
        assert "EZDİ" in str(ex) and "so_s7_bolgeler" in str(ex)


def test_skaler_vektor_ve_elle_olculer():
    d = _dip(); A = S7._so7_diziler(d)
    V = S7._so7_olcu_vek(A, 8); fark = 0.0
    for e in range(300, A["n"], 11):
        m = S7._so7_olcu(A, e - 7, e)
        for k in V:
            if np.isfinite(V[k][e]) or np.isfinite(m[k]):
                fark = max(fark, abs(V[k][e] - m[k]) / max(1e-12, abs(m[k])))
    assert fark < 1e-9, fark
    s_, e_ = 470, 485
    m = S7._so7_olcu(A, s_, e_)
    H, L, C = d.High.to_numpy(), d.Low.to_numpy(), d.Close.to_numpy(); Cp = np.r_[np.nan, C[:-1]]
    assert abs(m["R"] - np.median(((H - L) / Cp)[s_ - 250:s_])) < 1e-15
    mm = np.sort(((H - L) / C)[s_:e_ + 1])
    assert abs(m["z1"] - np.median(mm[:-1])) < 1e-15 and m["z2_ikinci"] == mm[-2] and m["z2_max"] == mm[-1]
    w = np.sort(C[s_:e_ + 1])
    assert abs(m["band"] - (min(w[-2] / w[0], w[-1] / w[1]) - 1)) < 1e-15
    assert abs(m["egim"] - np.polyfit(np.arange(16), np.log(C[s_:e_ + 1]), 1)[0] * 16) < 1e-10
    assert m["z5_son"] == L[e_ - 5:e_ + 1].min() and m["z5_ilk"] == L[s_:e_ - 5].min()          # floor(2*16/5) = 6
    bb = np.full(len(C), np.nan)
    for j in range(19, len(C)):
        bb[j] = 4 * np.std(C[j - 19:j + 1]) / np.mean(C[j - 19:j + 1])
    assert abs(m["z6"] - np.min(bb[s_:e_ + 1])) < 1e-12 and abs(m["z6p"] - np.mean(bb[s_ - 250:s_] <= np.min(bb[s_:e_ + 1]))) < 1e-12
    c = C[s_ - 120:e_ + 1]; md = np.median(C[s_:e_ + 1])
    assert abs(m["konum"] - (md - c.min()) / (c.max() - c.min())) < 1e-12 and abs(m["tepe"] - (C[s_ - 120:s_].max() / md - 1)) < 1e-12
    assert abs(m["sma"] - C[e_ - 49:e_ + 1].mean()) < 1e-9


def test_sentetik_bolgeler_kirilim_kilit():
    d = _dip(); C = d.Close.to_numpy(); B = S7.so_s7_bolgeler(d, "ABD")
    bd = [r for r in B if 450 <= r["s_i"] <= 505]          # öbek 460'ta başlar; geriye uzatma düşüşün son birkaç barını alabilir
    assert bd and all(r["sinif"] == "DIP" and r["e_i"] - r["s_i"] + 1 >= 8 for r in bd), B
    assert all(465 <= r["e_i"] <= 512 for r in B), [(r["s_i"], r["e_i"]) for r in B]
    for r in B:
        k = r["kilit_i"]
        if r["tur"] == "YUKARI":
            assert C[k] > r["ust"] * 1.01
        elif r["tur"] == "AŞAĞI":
            assert C[k] < r["alt"] * 0.99
        assert r["son_i"] == k - 1 or r["tur"] == "AÇIK"
    for a_, b_ in zip(B, B[1:]):
        assert b_["s_i"] > a_["kilit_i"] and b_["e_i"] >= a_["kilit_i"] + 8
    assert any(r["sinif"] == "YOL" and 450 <= r["s_i"] <= 505 for r in S7.so_s7_bolgeler(_yol(), "ABD"))
    assert not [r for r in S7.so_s7_bolgeler(_orta(), "ABD") if 450 <= r["e_i"] <= 520]


def test_onek_degismezligi():
    """GELECEĞE BAKMA: seri kesilince kesimden önce onaylanmış bölgelerin s, e, sınıf, R aynı; biten bölge tamamen aynı; kesimden sonrası bozulunca aynı."""
    if VERI_VAR:
        D = S7._so7_bistveri(["FENER", "CCOLA", "ENJSA"]); pz = "BIST"
        kesim = ["2024-03-15", "2024-11-29", "2025-08-08", "2025-10-24", "2026-07-10"]
    else:
        d = _dip(); D = {"D1": d, "Y1": _yol(), "D2": _dip(11)}; pz = "ABD"
        kesim = [str(d.index[i].date()) for i in (470, 480, 490, 500, 520)]
    hata, n_k = [], 0
    for s, dd in D.items():
        Bt = S7.so_s7_bolgeler(dd, pz, sembol=s)
        for kt in kesim:
            dk = dd[dd.index <= pd.Timestamp(kt)]; nk = len(dk)
            Bk = S7.so_s7_bolgeler(dk, pz, sembol=s)
            once = [r for r in Bt if r["e_i"] < nk]
            if [(r["s_i"], r["e_i"], r["sinif"], r["R"]) for r in once] != [(r["s_i"], r["e_i"], r["sinif"], r["R"]) for r in Bk]:
                hata.append(f"{s} {kt}: önek farklı")
            for r1, r2 in zip(once, Bk):
                n_k += 1
                if r1["kilit_i"] < nk:
                    if (r1["son_i"], r1["tur"], r1["ust"], r1["alt"]) != (r2["son_i"], r2["tur"], r2["ust"], r2["alt"]):
                        hata.append(f"{s} {kt} {r1['onay']}: bitmiş bölge farklı")
                elif r2["tur"] != "AÇIK" or r2["son_i"] != nk - 1:
                    hata.append(f"{s} {kt} {r1['onay']}: kesimde açık olmalı")
            db = dd.copy(); db.iloc[nk:, :4] = db.iloc[nk:, :4] * 2.5
            Bb = [r for r in S7.so_s7_bolgeler(db, pz, sembol=s) if r["e_i"] < nk]
            if [(r["s_i"], r["e_i"], r["sinif"]) for r in Bb] != [(r["s_i"], r["e_i"], r["sinif"]) for r in once]:
                hata.append(f"{s} {kt}: gelecek bozulunca önek değişti")
    assert not hata and n_k > 0, (n_k, hata[:3])


def test_s5_s6_kutu_makinesi():
    if not VERI_VAR:
        return
    D = S7._so7_bistveri(["FENER", "CCOLA", "ENJSA"])
    B5 = S7.so_s7_kutu_s56(D["FENER"], "BIST", "S5")
    bek = [("2025-09-01", "2025-09-01", "AŞAĞI"), ("2025-10-31", "2025-10-31", "YUKARI"), ("2025-11-04", "2025-11-06", "AŞAĞI"), ("2025-11-10", "2025-11-10", "YUKARI")]
    assert [(r["bas"], r["bitis"], r["tur"]) for r in B5 if "2025-08-25" <= r["bas"] <= "2025-11-30"] == bek
    assert not any(r["bas"] >= "2025-07-01" for s in D for r in S7.so_s7_kutu_s56(D[s], "BIST", "S6"))


def test_on_yazim_muhur_ve_tasarim_secimi():
    S7._so7_on_yazim_oku()                               # mühür tutmazsa S7Hata
    if not VERI_VAR:
        return
    J = S7.so_s7_tasarim(yaz=False)
    assert J["secilen"] == E7["secilen"] and J["en_cok_tutan"] == 7 and J["secilen_kacan"] == ["CCOLA-E"] and J["tam_tutan_nokta"] == 0
    assert S7.so_s7_pine_blok(yaz=False) in open(S7._so7_yol("pine"), encoding="utf-8").read()


def test_kontrol_kapisi():
    import IZ_KARNE as IK
    assert IK.ik_kontrol_kapisi(S7._so7_yol("tasarim"))["gecti"]


def test_pine_varsayilanlar_ve_getiri_yok():
    pt = open(S7._so7_yol("pine"), encoding="utf-8").read()

    def inp(ad):
        mt = re.search(rf"^{ad}\s*=\s*input\.\w+\(([-0-9.]+)", pt, re.M)
        return float(mt.group(1)) if mt else None
    sc = E7["secilen"]
    assert (inp("kM"), inp("bbEsik"), inp("Lmin"), inp("bantBIST"), inp("bantDiger"), inp("egimAlt"), inp("egimUst")) == \
        (sc["k_m"], sc["bb"], sc["Lmin"], sc["bant"]["BIST"], sc["bant"]["ABD"], sc["egim"][0], sc["egim"][1])
    assert (inp("Lmax"), inp("z2Zipla"), inp("z2Hepsi"), inp("z5R"), inp("rGun"), inp("dipKonum"), inp("dipTepe"), inp("yolKonum"), inp("kirPay"),
            inp("gecmisMin"), inp("sinifGun"), inp("bbDagilim"), inp("bbGun"), inp("smaGun"), inp("smaEgimGun")) == \
        (E7["Lmax"], E7["z2_zipla_haric"], E7["z2_hepsi"], E7["z5_R"], E7["R_gun"], E7["dip_konum"], E7["dip_tepe"], E7["yol_konum"], E7["kirilim"],
         E7["gecmis_min"], E7["sinif_gun"], E7["bb_dagilim"], E7["bb_gun"], E7["sma_gun"], E7["sma_egim_gun"])
    kod = pt.split("// ==== BEKLENEN KUTULAR")[0]
    assert "//@version=5" in kod and "max_boxes_count=500" in kod and "max_labels_count=500" in kod
    satir = "\n".join(x for x in kod.splitlines() if not x.strip().startswith("//") and "kör yargı" not in x)
    assert not re.search(r"(20g|getiri|kazanç|kazanc)", satir, re.I)
    assert "SIKISMA_S7.py" in pt and "SIKISMA_OBEK.py so_s7" not in pt


def test_eposta_anahtar_yok():
    desen = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    kl = SO.SO_YOL["cikti"]
    dosyalar = [os.path.join(KOK, "SIKISMA_S7.py"), os.path.join(KOK, "test_sikisma_s7.py")] + \
        [os.path.join(kl, f) for f in os.listdir(kl) if f.startswith(("S7_", "s7_", "COL_S7", "PINE_S7"))]
    for f in dosyalar:
        t = open(f, encoding="utf-8").read()
        assert not desen.search(t), f
        assert not re.search(r"(api[_-]?key|token|secret)\s*[:=]\s*['\"][A-Za-z0-9]{12,}", t, re.I), f


if __name__ == "__main__":
    n_h = 0
    for ad, f in [(k, v) for k, v in globals().items() if k.startswith("test_") and callable(v)]:
        try:
            f(); print("TAMAM", ad)
        except Exception as ex:   # noqa: BLE001
            n_h += 1; print("HATA ", ad, repr(ex)[:300])
    sys.exit(1 if n_h else 0)
