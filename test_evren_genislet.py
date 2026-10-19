# -*- coding: utf-8 -*-
"""test_evren_genislet — python -I test_evren_genislet.py [--mutasyon]"""
import json
import os
import pickle
import sys
import tempfile
import traceback
import types

import numpy as np
import pandas as pd

KLASOR = os.path.dirname(os.path.abspath(__file__))
KAYNAK = open(os.path.join(KLASOR, "evren_genislet.py"), encoding="utf-8").read()


def yukle(kod=KAYNAK, on=None):
    m = types.ModuleType("evren_test"); m.__file__ = "evren_genislet.py"; sys.modules["evren_test"] = m
    if on:
        m.__dict__.update(on)
    exec(compile(kod, "evren_genislet.py", "exec"), m.__dict__)
    m.__dict__["_TEST_KOD"] = kod
    return m.__dict__


def ohlcv(n=120, bas="2024-01-01", fiyat=10.0):
    ix = pd.bdate_range(bas, periods=n)
    c = fiyat * (1 + 0.001 * np.arange(n))
    return pd.DataFrame({"Open": c, "High": c * 1.01, "Low": c * 0.99, "Close": c, "Volume": 1e6}, index=ix)


def kur(K, sarmal=True):
    V = {"AAA": ohlcv(), "BBB": ohlcv()}
    P = {"kayit": {"x": 1}, "veri": V} if sarmal else V
    pickle.dump(P, open(os.path.join(K, "veri_1d_turkey.pkl"), "wb"))
    pd.DataFrame({"sembol": ["AAA", "bbb.is", "CCC", "DDD", "EEE", "FFF"], "ozkaynak": [1] * 6}).to_csv(os.path.join(K, "temel_duz.csv"), index=False)
    open(os.path.join(K, "evren_ek_liste.txt"), "w", encoding="utf-8").write("# yorum\nGGG\nAAA\n")


def sahte_indir(s):
    if s == "CCC":
        return ohlcv(380, "2023-01-01")                         # eklenir, güncel (AAA ile aynı güne kadar)
    if s == "DDD":
        return ohlcv(200, "2022-01-01")                         # eklenir, son barı eski → çıkmış görünen
    if s == "EEE":
        return ohlcv(20)                                        # kısa
    if s == "FFF":
        return None                                             # veri yok
    if s == "GGG":
        raise RuntimeError("ağ")                                # hata
    raise AssertionError(f"beklenmeyen sembol {s}")


def T1_aday(ns):
    with tempfile.TemporaryDirectory() as K:
        kur(K)
        assert ns["eg_aday"](K, ["AAA", "BBB"]) == ["CCC", "DDD", "EEE", "FFF", "GGG"]


def T2_genislet_sarmal(ns):
    with tempfile.TemporaryDirectory() as K:
        kur(K)
        oz = ns["evren_genislet"](K, indir=sahte_indir)
        assert oz["eklendi"] == ["CCC", "DDD"] and oz["cikmis_gorunen"] == ["DDD"] and oz["kisa"] == ["EEE"] and oz["veri_yok"] == ["FFF"] and oz["hata"] == ["GGG"], oz
        P = pickle.load(open(os.path.join(K, "veri_1d_turkey.pkl"), "rb"))
        assert set(P["veri"]) == {"AAA", "BBB", "CCC", "DDD"} and P["kayit"]["x"] == 1 and P["kayit"]["evren_genislet"]["eklenen"] == ["CCC", "DDD"]
        assert list(P["veri"]["CCC"].columns) == ["Open", "High", "Low", "Close", "Volume"] and P["veri"]["CCC"].index.tz is None
        assert any(f.startswith("veri_1d_turkey.pkl.yedek_evren_") for f in os.listdir(K)), "yedek alınmadı"
        durum = json.load(open(os.path.join(K, "evren_ek_durum.json"), encoding="utf-8"))
        assert durum["CCC"] == "eklendi" and durum["FFF"] == "yok" and durum["EEE"] == "kisa" and durum["GGG"].startswith("hata")


def T3_kaldigi_yerden(ns):
    with tempfile.TemporaryDirectory() as K:
        kur(K)
        ns["evren_genislet"](K, indir=sahte_indir)
        sayac = {"n": 0}

        def ikinci(s):
            sayac["n"] += 1
            return sahte_indir(s) if s != "GGG" else ohlcv(100)
        oz = ns["evren_genislet"](K, indir=ikinci)
        # yok/kısa olanlar yeniden denenmez; eklenenler artık veride (aday değil); hata olan yeniden denenir
        assert sayac["n"] == 1 and oz["eklendi"] == ["GGG"], (sayac, oz)


def T4_duz_sozluk(ns):
    with tempfile.TemporaryDirectory() as K:
        kur(K, sarmal=False)
        oz = ns["evren_genislet"](K, indir=sahte_indir)
        P = pickle.load(open(os.path.join(K, "veri_1d_turkey.pkl"), "rb"))
        assert isinstance(P, dict) and "veri" not in P and "CCC" in P and oz["evren"] == 4


def T5_temizle(ns):
    ix = pd.date_range("2024-01-01", periods=5, tz="Europe/Istanbul")
    y = pd.DataFrame({"open": 1.0, "high": 2.0, "low": 0.5, "close": [1, np.nan, 1, 1, 1], "volume": 1, "adj close": 1.0}, index=ix)
    t = ns["eg_temizle"](y)
    assert list(t.columns) == ["Open", "High", "Low", "Close", "Volume"] and len(t) == 4 and t.index.tz is None
    assert ns["eg_temizle"](None) is None and ns["eg_temizle"](pd.DataFrame({"close": [1]})) is None


def T6_cakisma(ns):
    try:
        yukle(on={"eg_aday": 1})
    except RuntimeError as e:
        assert "çakışma" in str(e)
    else:
        raise AssertionError("kapı çalışmadı")


TESTLER = [T1_aday, T2_genislet_sarmal, T3_kaldigi_yerden, T4_duz_sozluk, T5_temizle, T6_cakisma]
MUTASYONLAR = [
    ("mevcut semboller elenmez", "if a and a not in m and a.isalnum()", "if a and a.isalnum()"),
    ("kısa seri eklenir", "elif len(df) < min_bar:", "elif False:"),
    ("yedek alınmaz", 'shutil.copy(yol, yol + time.strftime(".yedek_evren_%Y%m%d_%H%M"))', "pass"),
    ("kaldığı yerden sürmez", 'if durum.get(a) not in ("yok", "kisa")', "if True"),
    ("durum yazılmaz", 'json.dump(durum, open(dyol, "w", encoding="utf-8"), ensure_ascii=False, indent=0)', "pass"),
    ("tz atılmaz", 'y.index = y.index.tz_localize(None)', "pass"),
]


def kos(ns, sessiz=False):
    hata = []
    for t in TESTLER:
        try:
            t(ns)
        except Exception as e:
            hata.append((t.__name__, e))
            if not sessiz:
                print(f"  ✗ {t.__name__}: {e}"); traceback.print_exc()
        else:
            if not sessiz:
                print(f"  ✓ {t.__name__}")
    return hata


if __name__ == "__main__":
    if "--mutasyon" in sys.argv:
        kacan = []
        for ad, eski, yeni in MUTASYONLAR:
            assert eski in KAYNAK, f"mutasyon hedefi yok: {ad}"
            try:
                ns = yukle(KAYNAK.replace(eski, yeni, 1))
            except Exception:
                print(f"  ✓ yakalandı (yükleme): {ad}"); continue
            h = kos(ns, sessiz=True)
            print(f"  {'✓ yakalandı' if h else '✗ KAÇTI'}: {ad}" + (f" ← {h[0][0]}" if h else ""))
            if not h:
                kacan.append(ad)
        print(f"\n{len(MUTASYONLAR) - len(kacan)}/{len(MUTASYONLAR)} mutasyon yakalandı"); sys.exit(1 if kacan else 0)
    ns = yukle()
    h = kos(ns)
    print(f"\n{len(TESTLER) - len(h)}/{len(TESTLER)} test geçti"); sys.exit(1 if h else 0)
