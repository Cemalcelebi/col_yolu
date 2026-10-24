# -*- coding: utf-8 -*-
"""test_zincir_denetimi — python -I test_zincir_denetimi.py [--mutasyon]"""
import os
import sys
import tempfile
import traceback
import types

import numpy as np
import pandas as pd

KLASOR = os.path.dirname(os.path.abspath(__file__))
KAYNAK = open(os.path.join(KLASOR, "zincir_denetimi.py"), encoding="utf-8").read()


def yukle(kod=KAYNAK, on=None):
    m = types.ModuleType("zd_test"); m.__file__ = "zincir_denetimi.py"; sys.modules["zd_test"] = m
    if on:
        m.__dict__.update(on)
    exec(compile(kod, "zincir_denetimi.py", "exec"), m.__dict__)
    return m.__dict__


def seri(n=300, bas=10.0, seed=1, start="2024-01-01"):
    rng = np.random.default_rng(seed)
    c = bas * np.cumprod(1 + rng.normal(0.0005, 0.01, n))
    ix = pd.bdate_range(start, periods=n)
    o = c * (1 + rng.normal(0, 0.003, n))
    return pd.DataFrame({"Open": o, "High": np.maximum(o, c) * 1.01, "Low": np.minimum(o, c) * 0.99, "Close": c, "Volume": 1e6}, index=ix)


def evren(n=4):
    return {f"S{i}": seri(seed=10 + i) for i in range(n)}


def sinyaller(E, gun=100):
    return pd.DataFrame({"sembol": list(E), "tarih": [E[s].index[gun] for s in E]})


def T1_butunluk(ns):
    E = ns["_zd_evren"](evren())
    R = ns["zd_butunluk"](E); assert R["acilis_disi"] == 0 and "TEMİZ" in R["hukum"], R
    V = evren(); V["S0"].iloc[50, V["S0"].columns.get_loc("Open")] = V["S0"]["High"].iloc[50] * 1.5     # açılış aralık dışı
    V["S1"].iloc[60, V["S1"].columns.get_loc("High")] = V["S1"]["Low"].iloc[60] * 0.5                  # H<L
    R2 = ns["zd_butunluk"](ns["_zd_evren"](V))
    assert R2["acilis_disi"] >= 1 and R2["h_kucuk_l"] == 1 and R2["en_cok"][0][0] == "S1", R2


def T2_takvim(ns):
    V = evren(6); V["S0"] = V["S0"].drop(V["S0"].index[100:105])     # 5 gün eksik (6 hisseden 5'inde bar var → piyasa açık)
    ek = V["S1"].iloc[[50]].copy(); ek.index = [pd.Timestamp("2024-03-16")]   # cumartesi: tek hissede bar → piyasa açık sayılmamalı
    V["S1"] = pd.concat([V["S1"], ek]).sort_index()
    R = ns["zd_takvim"](ns["_zd_evren"](V))
    assert R["eksik_bar"] == 5 and R["en_cok"][0] == ("S0", 5), R


def T3_dolum(ns):
    V = evren(); S = sinyaller(V)
    V["S0"].iloc[101, V["S0"].columns.get_loc("Open")] = V["S0"]["Close"].iloc[100] * 1.10     # tavan açılış
    V["S2"].iloc[101, V["S2"].columns.get_loc("Open")] = V["S2"]["Close"].iloc[100] * 1.10     # tavan açılış
    V["S1"].iloc[101, V["S1"].columns.get_loc("Open")] = V["S1"]["Close"].iloc[100] * 0.90     # taban açılış
    R = ns["zd_dolum"](ns["_zd_evren"](V), ns["_zd_sinyaller"](S))
    assert R["n"] == 4 and abs(R["tavan_pay"] - 0.5) < 1e-9 and abs(R["taban_pay"] - 0.25) < 1e-9, R


def T4_temettu(ns):
    V = evren(); S = sinyaller(V); E = ns["_zd_evren"](V)
    T = {"S0": pd.Series([0.5], index=[E["S0"].index[110]]), "S1": pd.Series([0.3], index=[E["S1"].index[250]]), "S2": pd.Series(dtype=float)}
    R = ns["zd_temettu"](E, ns["_zd_sinyaller"](S), T, ufuk=120)
    assert R["n"] == 4 and R["etkilenen"] == 1, R                     # S1'inki pencere dışında (250 > 100+120)
    assert abs(R["verim_ort"] - 0.5 / float(E["S0"]["C"].iloc[109])) < 1e-9
    with tempfile.TemporaryDirectory() as K:
        sayac = {"n": 0}
        def indir(s):
            sayac["n"] += 1; return pd.Series([1.0], index=[pd.Timestamp("2024-05-01")])
        D = ns["zd_temettu_oku"](K, ["A", "B"], indir=indir); assert sayac["n"] == 2 and os.path.exists(os.path.join(K, "temettu.pkl"))
        D2 = ns["zd_temettu_oku"](K, ["A", "B", "C"], indir=indir); assert sayac["n"] == 3 and len(D2) == 3


def T5_kesik(ns):
    V = evren(); E = ns["_zd_evren"](V)
    S = pd.DataFrame({"sembol": ["S0", "S1", "S2"], "tarih": [E["S0"].index[100], E["S1"].index[220], E["S2"].index[280]]})
    R = ns["zd_kesik"](E, ns["_zd_sinyaller"](S), ufuk=120, en_az=40)
    assert (R["tam"], R["kesik"], R["atilan"]) == (1, 1, 1), R


def T6_nedensellik(ns):
    V = evren(); E = ns["_zd_evren"](V); S = ns["_zd_sinyaller"](sinyaller(V))
    def seg_nedensel(x): return {"tavan": float(x["Close"].iloc[-20:].max())}
    def seg_sizintili(x): return {"tavan": float(x["Close"].iloc[-1]) * 1.3}      # d'deki değerle uyuşmaz
    S["tavan"] = [seg_nedensel(E[s].iloc[: E[s].index.get_loc(t) + 1].rename(columns={"C": "Close"}))["tavan"] for s, t in zip(S.sembol, S.tarih)]
    R = ns["zd_nedensellik"](E, S, seg_nedensel, ornek=4)
    assert R["uyum"] == 4 and R["uyumsuz"] == 0 and "nedensel" in R["hukum"], R
    R2 = ns["zd_nedensellik"](E, S, seg_sizintili, ornek=4)
    assert R2["uyumsuz"] == 4 and "uyuşmuyor" in R2["hukum"], R2


def T6b_nedensellik_col_olc(ns):
    """col_olc ile: (a) tam seri+tarih vs kesik seri (kod sızıntısı), (b) d'deki çok sütun uyumu, (c) E_eski ile karşılaştırma."""
    V = evren(); E = ns["_zd_evren"](V); S = ns["_zd_sinyaller"](sinyaller(V))
    def olc(df, tarih=None):
        x = df[df.index <= pd.Timestamp(tarih)] if tarih is not None else df
        c = x["Close"]
        return {"clv": round(float(c.iloc[-5:].mean() / c.iloc[-1] - 1), 3), "bant_son": float(c.iloc[-1] / c.iloc[-20:].max()), "uzunluk": 20 + int(c.iloc[-1] > c.iloc[-2]),
                "doji": np.nan, "GECER": bool(c.iloc[-1] > c.iloc[-20:].mean()), "tavan": float(c.iloc[-20:].max())}
    def olc_sizintili(df, tarih=None):                       # tarih verilince kesmiyor: geleceği görüyor
        return olc(df, None)
    for s, t in zip(S.sembol, S.tarih):
        o = olc(E[s].rename(columns={"C": "Close"}), t)
        for k, v in o.items():
            S.loc[(S.sembol == s) & (S.tarih == t), k] = v
    S["GECER"] = S["GECER"].astype(bool); S["uzunluk"] = S["uzunluk"].astype(int)
    R = ns["zd_nedensellik"](E, S, None, ornek=4, col_olc=olc)
    assert R["sizinti"] == 0 and R["uyum"] == 4 and R["uyumsuz"] == 0 and "NEDENSEL" in R["hukum"] and "doji" in R["kolonlar"], R
    R2 = ns["zd_nedensellik"](E, S, None, ornek=4, col_olc=olc_sizintili)
    assert R2["sizinti"] == 4 and "GELECEĞE" in R2["hukum"] and R2["sizinti_ornek"], R2
    # (c) ham veri farklı (bedelsiz onarımı gibi ×0.5): E_eski ile uyum, E ile uyumsuz
    V2 = {s: df * (0.5 if s == "S0" else 1.0) for s, df in V.items()}; V2 = {s: df.assign(Volume=1e6) for s, df in V2.items()}
    E2 = ns["_zd_evren"](V2)
    R3 = ns["zd_nedensellik"](E2, S, None, ornek=4, col_olc=olc)                   # S0 tavan yarıya iner → uyumsuz 1
    assert R3["uyumsuz"] == 1 and R3["kol_uyumsuz"]["tavan"] == 1 and R3["kol_uyumsuz"]["clv"] == 0, R3
    R4 = ns["zd_nedensellik"](E2, S, None, ornek=4, col_olc=olc, E_eski=E)        # d ham veriyle karşılaştırılır → uyum 4
    assert R4["uyum"] == 4 and R4["uyumsuz"] == 0 and "ham" in R4["hukum"], R4
    # sayısal eşitlik: yuvarlama payı içinde aynı, dışında farklı; NaN==NaN
    assert ns["_zd_esit"](0.123, 0.1234, "clv") and not ns["_zd_esit"](0.123, 0.130, "clv") and ns["_zd_esit"](np.nan, np.nan, "doji") and not ns["_zd_esit"](np.nan, 0.1, "doji")
    assert ns["_zd_esit"](20, 20.0, "uzunluk") and not ns["_zd_esit"](20, 21, "uzunluk") and ns["_zd_esit"](True, 1, "GECER") and not ns["_zd_esit"](True, False, "GECER")


def T7_pnl_ve_maliyet(ns):
    # deterministik seri: giriş 10, 30. günde 12.5 (hedef aşıldı), sonra SMA20 altına düşüş → trail çıkış
    n = 200; ix = pd.bdate_range("2024-01-01", periods=n); c = np.full(n, 10.0)
    c[101:131] = np.linspace(10, 12.5, 30); c[131:] = 12.5
    c[103] = 9.9                                    # hedef öncesi küçük sarkma: trail aktif değilken çıkış OLMAMALI
    c[160:] = 9.0                                   # sert düşüş: SMA20 altına
    M = pd.DataFrame({"O": c, "H": c * 1.001, "L": c * 0.999, "C": c, "V": 1e6}, index=ix)
    p = ns["zd_pnl"](M, 100, np.nan, ufuk=120, maliyet=0.0)
    assert abs(p - (9.0 / 10.0 - 1) * 100) < 1e-6, p             # 160. gün kapanış 9.0'da çıkar
    p2 = ns["zd_pnl"](M, 100, np.nan, ufuk=120, maliyet=0.01); assert abs((p - p2) - 2.0) < 1e-9
    # hedefe ulaşmayan: ufuk sonu çıkış
    c2 = np.full(n, 10.0); c2[101:] = 10.5
    M2 = pd.DataFrame({"O": c2, "H": c2 * 1.001, "L": c2 * 0.999, "C": c2, "V": 1e6}, index=ix)
    assert abs(ns["zd_pnl"](M2, 50, np.nan, ufuk=120, maliyet=0.0) - 5.0) < 1e-6
    V = evren(); R = ns["zd_maliyet"](ns["_zd_evren"](V), ns["_zd_sinyaller"](sinyaller(V).assign(tavan=0.01)))   # denetim: giris kirilimdan; dusuk tavan = hemen kirilim
    b = [v[1] for v in R["ozet"].values()]; assert b[0] > b[1] > b[2] and abs((b[0] - b[2]) - 2.2) < 1e-6, R


def T8_hayatta(ns):
    with tempfile.TemporaryDirectory() as K:
        V = evren(); V["S3"] = V["S3"].iloc[:-60]
        pd.DataFrame({"sembol": ["S0", "ZZZ"]}).to_csv(os.path.join(K, "temel_duz.csv"), index=False)
        R = ns["zd_hayatta"](ns["_zd_evren"](V), K)
        assert R["son_bari_eski"] == ["S3"] and R["temelde_var_evrende_yok"] == ["ZZZ"], R


def T9_uctan_uca(ns):
    with tempfile.TemporaryDirectory() as K:
        V = evren(); S = sinyaller(V)
        def indir(s): return pd.Series(dtype=float)
        R = ns["zincir_denetimi"](K, {"kayit": {}, "veri": V}, S, col_segment=lambda x: {"tavan": float(x["Close"].iloc[-20:].max())}, indir=indir)
        assert os.path.exists(os.path.join(K, "zincir_denetimi_rapor.txt")) and all(k in R for k in ("butunluk", "takvim", "dolum", "temettu", "kesik", "nedensellik", "maliyet", "hayatta"))
        assert "1 BÜTÜNLÜK" in R["rapor"] and "8 HAYATTA" in R["rapor"]


TESTLER = [T1_butunluk, T2_takvim, T3_dolum, T4_temettu, T5_kesik, T6_nedensellik, T6b_nedensellik_col_olc, T7_pnl_ve_maliyet, T8_hayatta, T9_uctan_uca]
MUTASYONLAR = [
    ("açılış aralık kontrolü kalkar", '(M["O"] > M["H"] * 1.0001) | (M["O"] < M["L"] * 0.9999)', "(M[\"O\"] < 0)"),
    ("takvim eşiği açık gün tanımı bozulur", "sayac[sayac >= esik * len(E)].index", "tum"),
    ("tavan payı taban olarak sayılır", "tavan = float((a >= limit).mean())", "tavan = float((a <= -limit).mean())"),
    ("temettü penceresi sınırsız", "tt = t[(t.index > r.tarih) & (t.index <= son)]", "tt = t[(t.index > r.tarih)]"),
    ("kesik sınıflama bozuk", "elif ileri >= en_az:", "elif ileri >= 0:"),
    ("nedensellik uyum toleransı gevşer", "return abs(fa - fb) <= 0.0015 + 0.002 * abs(fb)", "return abs(fa - fb) <= 5"),
    ("kod sızıntısı sayılmaz", "sizinti += 1; sizinti_ornek.append", "sizinti_ornek.append"),
    ("E_eski yok sayılır", "EK = E_eski if E_eski is not None else E", "EK = E"),
    ("GECER karşılaştırması bozuk", 'if kol == "GECER":\n        return bool(a) == bool(b)', 'if kol == "GECER":\n        return True'),
    ("trail: hedef şartı kalkar", 'if not trail and float(M["H"].iloc[j]) >= g * (1 + hedef):', "if not trail:"),
    ("maliyet iki yön düşülmez", "- 1 - 2 * maliyet) * 100\n    return (float(M[\"C\"].iloc[son])", "- 1 - maliyet) * 100\n    return (float(M[\"C\"].iloc[son])"),
    ("hayatta: eski bar eşiği kalkar", "(son - M.index[-1]).days > bayat_gun", "False"),
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
