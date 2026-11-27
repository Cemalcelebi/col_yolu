"""Bağımsız yeniden üretim (gt_k2k_* / hv25 fonksiyonları kullanılmadan): K2 ABD 2016-19 YÖN payı + farkı, K2 ABD 2020-22 TFk15."""
import sys, pickle, json
sys.path.insert(0, "/home/user/col_yolu")
import numpy as np, pandas as pd
import MUM_IZI as MI, GOZ_TESPIT as G   # yalnız veri yükleyici ve yol
KES = pd.Timestamp("2022-12-31")
OL = pickle.load(open("/root/.kasa/ham/goz_tespit/k2/k2_olay.pkl", "rb")); AD = pickle.load(open("/root/.kasa/ham/goz_tespit/k2/k2_aday.pkl", "rb"))
V = MI.mi_veri("ABD", G.GT_YOL["acik"])["V"]
P = pickle.load(open("/root/.kasa/ham/goz_tespit/pencere_ABD.pkl", "rb"))
tr = pd.to_datetime(P.tarih); P = P[(tr >= "2016-01-01") & (tr <= "2022-12-31") & (P.s >= 120) & (P.KIL <= 0.2) & (P.govdesiz_pay <= 0.3)]
ADs = set(zip(AD[AD.pazar == "ABD"].sembol, AD[AD.pazar == "ABD"].L, AD[AD.pazar == "ABD"].t))

def donem(ts):
    if pd.Timestamp("2016-01-01") <= ts <= pd.Timestamp("2019-12-31"): return "d1619"
    if pd.Timestamp("2020-01-01") <= ts <= pd.Timestamp("2022-12-31"): return "d2022"
    return None

def yon(d, s, t):
    H = d.High.values; L = d.Low.values; C = d.Close.values; n = len(C)
    if t + 20 >= n or d.index[t + 20] > KES: return None, None
    tv = H[s:t + 1].max(); dp = L[s:t + 1].min()
    for j in range(t + 1, t + 21):
        if C[j] > tv: return 1, j
        if C[j] < dp: return -1, j
    return 0, None

# ---- 1) YÖN K2 ABD d1619
E = OL[(OL.kol == "K2") & (OL.hucre == "ABD|d1619")]
xs = []
for sem, g in E.groupby("sembol"):
    d = V[sem]; Pk = P[P.sembol == sem]
    for _, r in g.iterrows():
        y, _ = yon(d, int(r.s), int(r.t))
        if y is None: continue
        c = Pk[(Pk.L == r.L)]; vals = []
        for s_, t_ in zip(c.s.values, c.t.values):
            if (sem, int(r.L), int(t_)) in ADs or t_ + 1 >= len(d) or donem(d.index[t_ + 1]) != "d1619": continue
            yy, _ = yon(d, int(s_), int(t_))
            if yy is not None: vals.append(yy)
        if len(vals) < 5: continue
        xs.append((y, np.mean(np.array(vals) == 1)))
xs = np.array(xs)
print("YON K2 ABD d1619: n", len(xs), "yukari", (xs[:, 0] == 1).mean(), "asagi", (xs[:, 0] == -1).mean(), "taban", xs[:, 1].mean(), "fark", ((xs[:, 0] == 1) - xs[:, 1]).mean())

# ---- 2) TFk15 K2 ABD d2022
def r15(d, b):
    n = len(d)
    if b + 15 >= n or d.index[b + 15] > KES: return None
    return d.Close.values[b + 15] / d.Open.values[b + 1] - 1

E = OL[(OL.kol == "K2") & (OL.hucre == "ABD|d2022")]
tf = []
for sem, g in E.groupby("sembol"):
    d = V[sem]; Pk = P[P.sembol == sem]; bs = set()
    for L_, s_, t_ in zip(Pk.L.values, Pk.s.values, Pk.t.values):
        if (sem, int(L_), int(t_)) in ADs or t_ + 1 >= len(d) or donem(d.index[t_ + 1]) is None: continue
        yy, b = yon(d, int(s_), int(t_))
        if yy == 1: bs.add(b)
    kept = []
    for b in sorted(bs):
        if not kept or b - kept[-1] >= 15: kept.append(b)
    Rk = [r15(d, b) for b in kept if b + 1 < len(d) and donem(d.index[b + 1]) == "d2022"]
    Rk = [x for x in Rk if x is not None]
    eb = []
    for _, r in g.iterrows():
        y, b = yon(d, int(r.s), int(r.t))
        if y == 1: eb.append(b)
    ek = []
    for b in sorted(eb):
        if not ek or b - ek[-1] >= 15: ek.append(b)
    for b in ek:
        R = r15(d, b)
        if R is None or len(Rk) < 5: continue
        tf.append((R, np.mean(Rk)))
tf = np.array(tf)
print("TFk15 K2 ABD d2022: n", len(tf), "TFk15", (tf[:, 0] - tf[:, 1]).mean(), "medyan fark", np.median(tf[:, 0]) - np.median(tf[:, 1]))
