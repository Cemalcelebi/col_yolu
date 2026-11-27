"""SONUÇ SONRASI BİLGİ okuması (karara girmez): yön farkı bölge sonundaki konumdan (SON_YER = (C_t - DİP) / (TAVAN - DİP)) mı geliyor?"""
import sys, pickle
sys.path.insert(0, "/home/user/col_yolu")
import numpy as np, pandas as pd
import MUM_IZI as MI, GOZ_TESPIT as G
E = pickle.load(open("/root/.kasa/ham/goz_tespit/k2/k2k_yon.pkl", "rb")); KP = pickle.load(open("/root/.kasa/ham/goz_tespit/k2/k2k_kontrol.pkl", "rb"))
out = []
for p in ("ABD",):
    V = MI.mi_veri(p, G.GT_YOL["acik"])["V"]; K = KP[(KP.pazar == p) & ~KP.kesik & KP.donem.notna()].copy(); sy = np.full(len(K), np.nan)
    for sem, ix in K.groupby("sembol").indices.items():
        d = V[sem]; H, L, C = d.High.values, d.Low.values, d.Close.values; t = K.t.values[ix]; Lw = K.L.values[ix]
        TV, DP = G.gt_k2k_tavan_dip(H, L, t - Lw + 1, t); sy[ix] = (C[t] - DP) / (TV - DP)
    K["SY"] = sy
    Ep = E[(E.pazar == p) & (E.yon != -9) & np.isfinite(E.k1_yuk)].copy()
    Ep["SY"] = [(V[s].Close.values[t] - dp) / (tv - dp) for s, t, tv, dp in zip(Ep.sembol, Ep.t, Ep.TAVAN, Ep.DIP)]
    sin = np.quantile(K.SY, [0.2, 0.4, 0.6, 0.8]); K["q"] = np.searchsorted(sin, K.SY) + 1; Ep["q"] = np.searchsorted(sin, Ep.SY) + 1
    T = K.groupby(["donem", "L", "q"]).yon.apply(lambda v: (v == 1).mean()).rename("tb").reset_index()
    T2 = K.groupby(["sembol", "donem", "q"]).yon.agg(tbh=lambda v: (v == 1).mean(), nh="size").reset_index()
    Ep = Ep.merge(T, on=["donem", "L", "q"], how="left").merge(T2, on=["sembol", "donem", "q"], how="left"); Ep.loc[~(Ep.nh >= 5), "tbh"] = np.nan
    print("SON_YER beşlik sınırları (ABD kontrol):", np.round(sin, 3))
    for kol in ("K2", "YMSB", "Y"):
        for dn in ("d1619", "d2022"):
            g = Ep[(Ep.kol == kol) & (Ep.donem == dn)]
            print(kol, dn, "n", len(g), "SY medyan olay", round(g.SY.median(), 3), "kontrol", round(K[K.donem == dn].SY.median(), 3),
                  "| q dağılımı", np.bincount(g.q, minlength=6)[1:].tolist(),
                  "| yukarı", round((g.yon == 1).mean(), 3), "konum eşli taban", round(g.tb.mean(), 3), "fark", round(((g.yon == 1) - g.tb).mean(), 3),
                  "| eski taban (hisse-dönem-L)", round(g.k1_yuk.mean(), 3), "| aynı hisse + konum beşliği: n", int(g.tbh.notna().sum()), "yukarı", round((g[g.tbh.notna()].yon == 1).mean(), 3), "taban", round(g.tbh.mean(), 3), "fark", round(((g[g.tbh.notna()].yon == 1) - g.tbh.dropna()).mean(), 3))
            for q in []:
                h = g[g.q == q]
                if len(h) >= 30:
                    print("   q", q, "n", len(h), "yukarı", round((h.yon == 1).mean(), 3), "taban", round(h.tb.mean(), 3))
