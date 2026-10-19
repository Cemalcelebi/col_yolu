# -*- coding: utf-8 -*-
"""test_yeniden_tara — python -I test_yeniden_tara.py [--mutasyon]"""
import os
import sys
import tempfile
import traceback
import types

import numpy as np
import pandas as pd

KLASOR = os.path.dirname(os.path.abspath(__file__))
KAYNAK = open(os.path.join(KLASOR, "yeniden_tara.py"), encoding="utf-8").read()


def yukle(kod=KAYNAK):
    m = types.ModuleType("yt_test"); m.__file__ = "yeniden_tara.py"; sys.modules["yt_test"] = m
    exec(compile(kod, "yeniden_tara.py", "exec"), m.__dict__)
    return m.__dict__


def seri(n=400, bas=10.0, seed=1, start="2023-01-02"):
    rng = np.random.default_rng(seed)
    c = bas * np.cumprod(1 + rng.normal(0.0003, 0.012, n)); ix = pd.bdate_range(start, periods=n)
    o = c * (1 + rng.normal(0, 0.003, n))
    return pd.DataFrame({"Open": o, "High": np.maximum(o, c) * 1.01, "Low": np.minimum(o, c) * 0.99, "Close": c, "Volume": 1e6}, index=ix)


def evren(n=6, uzunluk=400):
    V = {f"S{i}": seri(uzunluk, seed=10 + i) for i in range(n)}
    V["KISA"] = seri(200, seed=50, start="2023-06-01")                                         # tarama gününde <250 bar → tara atlar
    V["BITEN"] = seri(len(pd.bdate_range("2023-01-02", "2024-03-11")), seed=51)                # son tarihten sonra 15 bar → tara atlar
    return V


def olc_oyuncak(df, tarih=None):
    """col_olc taklidi: son 20 kapanışın bandı; her 3. hisse-günde None (tara 'if not o' dalı)."""
    x = df[df.index <= pd.Timestamp(tarih)] if tarih is not None else df
    c = x["Close"]
    if len(x) < 60 or int(c.iloc[-1] * 1000) % 3 == 0:
        return None
    return {"clv": round(float(c.iloc[-5:].mean() / c.iloc[-1] - 1), 3), "bant_son": float(c.iloc[-1] / c.iloc[-20:].max()), "ortaust": 0.5,
            "uzunluk": 20, "doji": 0.2, "alt_fitil": 0.1, "dar": np.nan, "gecerli_oran": 1.0, "onceki_250": np.nan,
            "GECER": bool(c.iloc[-1] > c.iloc[-20:].mean()), "taban": float(c.iloc[-20:].min()), "tavan": float(c.iloc[-20:].max())}


def tara_kopya(tarihler, ileri, veri, col_olc, AL_PAY):
    """COL_v1.tara() birebir (print'siz) — referans."""
    R = []
    for T in tarihler:
        Ts = pd.Timestamp(T)
        for s, df in veri.items():
            x = df[df.index <= Ts]
            if len(x) < 250: continue
            try: o = col_olc(df, T)
            except Exception: o = None
            if not o: continue
            il = df[df.index > Ts].head(ileri)
            if len(il) < 20: continue
            p0 = float(x.Close.iloc[-1]); yon = 'YOK'
            for c in il.Close.to_numpy(float):
                if c > o['tavan'] * AL_PAY: yon = 'YUKARI'; break
                if c < o['taban']: yon = 'ASAGI'; break
            if yon == 'YOK': continue
            R.append({'sembol': s, 'tarih': T, 'yon': yon, 'clv': o['clv'], 'bant_son': o['bant_son'], 'ortaust': o['ortaust'],
                      'uzunluk': o['uzunluk'], 'doji': o['doji'], 'alt_fitil': o['alt_fitil'], 'dar': o['dar'], 'gecerli_oran': o['gecerli_oran'],
                      'onceki_250': o.get('onceki_250'), 'GECER': o['GECER'], 'getiri': (float(il.Close.iloc[-1]) / p0 - 1) * 100})
    return pd.DataFrame(R)


TARIHLER = [pd.Timestamp("2024-01-08"), pd.Timestamp("2024-01-22"), pd.Timestamp("2024-02-05"), pd.Timestamp("2024-02-19")]


def T1_tara_ile_birebir(ns):
    V = evren(); al = 1.05
    ref = tara_kopya(TARIHLER, 60, V, olc_oyuncak, al)
    with tempfile.TemporaryDirectory() as K:
        S = ns["yt_calistir"](K, V, TARIHLER, "t", olc_oyuncak, al, ileri=60)
    y = S[S["yon"] != "YOK"].reset_index(drop=True)
    assert len(ref) > 5 and len(y) == len(ref), (len(ref), len(y))
    a = ref.sort_values(["tarih", "sembol"]).reset_index(drop=True); b = y.sort_values(["tarih", "sembol"]).reset_index(drop=True)
    for k in ("sembol", "yon", "GECER", "uzunluk"):
        assert list(a[k]) == list(b[k]), k
    for k in ("clv", "bant_son", "getiri"):
        assert np.allclose(a[k].astype(float), b[k].astype(float)), k
    assert list(pd.to_datetime(a["tarih"])) == list(b["tarih"])
    assert {"taban", "tavan"} <= set(S.columns)
    def olc_genis(df, tarih=None):                      # bant çok geniş → hiç kırılmaz → tara boş, biz YOK satırlarını saklarız
        o = olc_oyuncak(df, tarih)
        if o: o = {**o, "taban": o["taban"] * 0.3, "tavan": o["tavan"] * 3}
        return o
    assert len(tara_kopya(TARIHLER, 60, V, olc_genis, al)) == 0
    with tempfile.TemporaryDirectory() as K:
        S2 = ns["yt_calistir"](K, V, TARIHLER, "g", olc_genis, al, ileri=60)
    assert len(S2) > 5 and (S2["yon"] == "YOK").all()


def T2_kaldigi_yerden(ns):
    V = evren(); al = 1.002
    class Kes(Exception): pass
    say = {"n": 0}; asil = ns["yt_bir_tarih"]
    def kesen(T, *a, **k):                       # 3. tarihte oturum kesilir (Colab kopması)
        say["n"] += 1
        if say["n"] == 3:
            raise Kes()
        return asil(T, *a, **k)
    with tempfile.TemporaryDirectory() as K:
        ns["yt_bir_tarih"] = kesen
        try:
            ns["yt_calistir"](K, V, TARIHLER, "t", olc_oyuncak, al, ileri=60); assert False, "kesilmedi"
        except Kes:
            pass
        finally:
            ns["yt_bir_tarih"] = asil
        D = ns["yt_durum_oku"](os.path.join(K, "yeniden_tara_t.pkl"))
        assert D["bitti"] == ["2024-01-08", "2024-01-22"], D["bitti"]
        n_once = len(D["satirlar"])
        S = ns["yt_calistir"](K, V, TARIHLER, "t", olc_oyuncak, al, ileri=60)          # kaldığı yerden
        D2 = ns["yt_durum_oku"](os.path.join(K, "yeniden_tara_t.pkl"))
        assert len(D2["bitti"]) == 4 and len(set(D2["bitti"])) == 4
        ref = ns["yt_calistir"](tempfile.mkdtemp(), V, TARIHLER, "t", olc_oyuncak, al, ileri=60)      # tek seferde
        assert len(S) == len(ref) and S["sembol"].tolist() == ref["sembol"].tolist() and np.allclose(S["clv"].astype(float), ref["clv"].astype(float))
        assert not S.duplicated(subset=["sembol", "tarih"]).any() and len(D2["satirlar"]) > n_once


def T3_parametre_degisirse_sifirdan(ns):
    V = evren(); al = 1.002
    with tempfile.TemporaryDirectory() as K:
        ns["yt_calistir"](K, V, TARIHLER[:2], "t", olc_oyuncak, al, ileri=60)
        S = ns["yt_calistir"](K, V, TARIHLER[:2], "t", olc_oyuncak, al, ileri=40)      # ileri değişti → sıfırdan
        D = ns["yt_durum_oku"](os.path.join(K, "yeniden_tara_t.pkl"))
        assert D["ileri"] == 40 and len(D["bitti"]) == 2
        ref = tara_kopya(TARIHLER[:2], 40, V, olc_oyuncak, al)
        assert len(S[S.yon != "YOK"]) == len(ref) and np.allclose(sorted(S[S.yon != "YOK"]["getiri"]), sorted(ref["getiri"]))


def T4_veri_degisirse_yeniden(ns):
    V = evren(); al = 1.002
    with tempfile.TemporaryDirectory() as K:
        ns["yt_calistir"](K, V, TARIHLER, "t", olc_oyuncak, al, ileri=60)
        V2 = dict(V); V2["S1"] = V["S1"] * 0.5; V2["S1"]["Volume"] = 1e6          # S1 onarılmış (bedelsiz gibi)
        V2["S2"] = pd.concat([V["S2"], V["S2"].iloc[-1:].set_index(pd.DatetimeIndex([V["S2"].index[-1] + pd.Timedelta(days=1)]))])   # S2'ye yeni bar: imza değişmez
        S = ns["yt_calistir"](K, V2, TARIHLER, "t", olc_oyuncak, al, ileri=60)
        ref = ns["yt_calistir"](tempfile.mkdtemp(), V2, TARIHLER, "t", olc_oyuncak, al, ileri=60)
        a = S.sort_values(["tarih", "sembol"]).reset_index(drop=True); b = ref.sort_values(["tarih", "sembol"]).reset_index(drop=True)
        assert len(a) == len(b) and np.allclose(a["tavan"].astype(float), b["tavan"].astype(float)) and np.allclose(a["getiri"].astype(float), b["getiri"].astype(float))
        im1 = ns["yt_imza"](V, TARIHLER[-1]); im2 = ns["yt_imza"](V2, TARIHLER[-1])
        assert im1["S1"] != im2["S1"] and im1["S2"] == im2["S2"] and im1["S0"] == im2["S0"]


def T5_ileri_bul_ve_tarihler(ns):
    V = evren(); al = 1.002
    ref = tara_kopya(TARIHLER, 40, V, olc_oyuncak, al)
    u, oran = ns["yt_ileri_bul"](ref, V)
    assert u == 40 and oran[40] > 0.9 and oran[60] < 0.3, (u, oran)
    assert ns["yt_tarihler"](ref) == TARIHLER
    bos = ref.copy(); bos["getiri"] = 123.0
    assert ns["yt_ileri_bul"](bos, V)[0] is None


def T6_karsilastir(ns):
    V = evren(); al = 1.002
    ref = tara_kopya(TARIHLER, 60, V, olc_oyuncak, al)
    with tempfile.TemporaryDirectory() as K:
        S = ns["yt_calistir"](K, V, TARIHLER, "t", olc_oyuncak, al, ileri=60)
    R = ns["yt_karsilastir"](ref, S)
    assert R["ortak"] == len(ref) and R["yalniz_eski"] == 0 and R["yalniz_yeni"] == 0 and R["gecer_ayni"] == R["ortak"] and R["uzunluk_ayni"] == R["ortak"]
    e2 = ref.copy(); e2.loc[e2.index[0], "GECER"] = not bool(e2.iloc[0]["GECER"]); e2 = e2.iloc[:-2]
    R2 = ns["yt_karsilastir"](e2, S)
    assert R2["gecer_ayni"] == R2["ortak"] - 1 and R2["yalniz_yeni"] == 2 and "yalnız yenide 2" in R2["rapor"]
    g = ref[ref.GECER.astype(bool)]                                   # d23 gibi yalnız GECER liste
    R3 = ns["yt_karsilastir"](g, S)
    assert R3["sadece_gecer"] and R3["yeni"] == int(S[(S.yon != "YOK")]["GECER"].astype(bool).sum()) and R3["yalniz_yeni"] == 0 and R3["ortak"] == len(g)


def T7_uctan_uca(ns):
    V = evren(); al = 1.002
    ref = tara_kopya(TARIHLER, 60, V, olc_oyuncak, al)
    with tempfile.TemporaryDirectory() as K:
        d2 = ns["yeniden_tara"](K, {"kayit": {}, "veri": V}, ref, "t", olc_oyuncak, al)
        assert os.path.exists(os.path.join(K, "v2_t.csv")) and os.path.exists(os.path.join(K, "v2_t_tum.csv")) and os.path.exists(os.path.join(K, "v2_t_rapor.txt"))
        assert len(d2) == len(ref) and (d2["yon"] != "YOK").all()
        r = open(os.path.join(K, "v2_t_rapor.txt"), encoding="utf-8").read(); assert "ileri=60" in r and f"ortak {len(ref)}" in r
        kotu = ref.copy(); kotu["getiri"] = 0.0
        try:
            ns["yeniden_tara"](K, V, kotu, "t2", olc_oyuncak, al); assert False, "ufuk bulunamayınca durmadı"
        except ValueError:
            pass


TESTLER = [T1_tara_ile_birebir, T2_kaldigi_yerden, T3_parametre_degisirse_sifirdan, T4_veri_degisirse_yeniden, T5_ileri_bul_ve_tarihler, T6_karsilastir, T7_uctan_uca]
MUTASYONLAR = [
    ("250 bar şartı kalkar", "if len(x) < 250:\n            continue", "if len(x) < 10:\n            continue"),
    ("ileri penceresi 20 bar şartı kalkar", "if len(il) < 20:\n            continue", "if len(il) < 0:\n            continue"),
    ("AL_PAY uygulanmaz", 'if c > o["tavan"] * al_pay:', 'if c > o["tavan"]:'),
    ("taban kırılması yön vermez", 'if c < o["taban"]:\n                yon = "ASAGI"; break', 'if c < 0:\n                yon = "ASAGI"; break'),
    ("getiri son bar yerine ilk bar", '"getiri": (float(il["Close"].iloc[-1]) / p0 - 1) * 100', '"getiri": (float(il["Close"].iloc[0]) / p0 - 1) * 100'),
    ("bitmiş tarih yeniden taranır (ilerleme kaybı)", 'kalan = [t for t in tarihler if str(t.date()) not in D["bitti"]]', "kalan = list(tarihler)"),
    ("parametre değişimi fark edilmez", 'if D["bitti"] and any(D.get(k) != v for k, v in anahtar.items()):', "if False:"),
    ("değişen hisse fark edilmez", "degisen = sorted(s for s in imza if D[\"imza\"] is not None and D[\"imza\"].get(s) != imza[s])", "degisen = []"),
    ("imza yeni barları da sayar", "x = df[df.index <= son_tarih]", "x = df"),
    ("ufuk eşiği gevşer", "return (en if oran[en] >= 0.6 else None), oran", "return en, oran"),
    ("yalnız-GECER eski liste tanınmaz", 'sadece_gecer = bool(e["GECER"].astype(bool).all()) if len(e) else False', "sadece_gecer = False"),
    ("karşılaştırma GECER sayımı bozuk", 'R["gecer_ayni"] = int((ge == gy).sum())', 'R["gecer_ayni"] = len(ortak)'),
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
    import logging; logging.disable(logging.WARNING)
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
