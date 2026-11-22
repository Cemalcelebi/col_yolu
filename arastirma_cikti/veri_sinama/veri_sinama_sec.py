"""Veri sinamasi: hisse ve pencere secimi (tohum 20261122). Yalniz /tmp/kasa/acik okunur."""
import pickle, json, numpy as np, pandas as pd
K = "/tmp/kasa/acik/"
TOHUM = 20261122
W = 120
def yukle(p):
    with open(K + f"V_{p}.pkl", "rb") as f: return pickle.load(f)
def tdeg(d):
    t = d.Close * d.Volume * (d["Kur"] if "Kur" in d.columns else 1.0)
    return float(t.iloc[-20:].median())
def sec(p, n_atlama, n_diger, rng, atlama_esik=0.15):
    V = yukle(p)
    # likidite: son 20 gun medyan islem degeri, evrenin ust yarisi (yalniz 2023-12-29'da islem gorenler)
    td = {s: tdeg(d) for s, d in V.items() if d.index[-1] >= pd.Timestamp("2023-12-20") and len(d) >= 400}
    med = np.median(list(td.values()))
    ust = sorted(s for s, v in td.items() if v >= med)
    ad, di = [], []
    for s in ust:
        d = V[s]; d = d[(d.High >= d.Low) & (d.Volume > 0) & (d.Close > 0)]
        d = d.loc["2018-01-01":"2023-12-29"]
        if len(d) < W + 60: continue
        r = d.Close.pct_change()
        idx = np.where(r.abs().values > atlama_esik)[0]
        idx = [i for i in idx if W // 2 <= i < len(d) - W // 2]
        (ad if idx else di).append((s, idx))
    ad.sort(); di.sort()
    out = []
    for s, idx in [ad[i] for i in rng.permutation(len(ad))[:n_atlama]]:
        i = int(rng.choice(idx)); out.append((s, "atlama", i))
    for s, idx in [di[i] for i in rng.permutation(len(di))[:n_diger]]:
        out.append((s, "rastgele", None))
    return V, out, dict(evren=len(td), ust_yari=len(ust), atlamali_aday=len(ad), digeri=len(di), medyan_tl=med)
if __name__ == "__main__":
    rng = np.random.RandomState(TOHUM)
    sonuc = {}
    for p, na, nd in [("ABD", 3, 3), ("AVR", 0, 3), ("BIST", 3, 2)]:
        V, o, bilgi = sec(p, na, nd, rng)
        L = []
        for s, tip, i in o:
            d = V[s]; d = d[(d.High >= d.Low) & (d.Volume > 0) & (d.Close > 0)].loc["2018-01-01":"2023-12-29"]
            if tip == "atlama": b = i - W // 2
            else: b = int(rng.randint(0, len(d) - W + 1))
            pen = d.iloc[b:b + W]
            L.append(dict(kod=s, tip=tip, bas=str(pen.index[0].date()), son=str(pen.index[-1].date())))
        sonuc[p] = dict(bilgi=bilgi, secim=L)
        print(p, bilgi); [print("  ", x) for x in L]
    json.dump(sonuc, open("secim.json", "w"), ensure_ascii=False, indent=1)
