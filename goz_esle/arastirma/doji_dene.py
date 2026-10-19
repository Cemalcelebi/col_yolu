import sys, numpy as np, pandas as pd
sys.path.insert(0, '.')
from bolge2 import *

PRM = dict(bant_kat=6, uzak_kat=1.5, sol_kat=1.5)


def auc(a, b):
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 3 or len(b) < 3: return np.nan
    rr = rankdata(np.r_[a, b]); return (rr[:len(a)].sum() - len(a) * (len(a) + 1) / 2) / (len(a) * len(b))


rows = []
for r in e.itertuples():
    D = DZ[r.sembol]; w = bolge2(D, int(r.si0), **PRM)
    if not w: continue
    k = {}
    for es in (0.1, 0.15, 0.25):
        k.update({f'{a}_{es}': v for a, v in doji_olc(D, *w, esik=es).items()})
    k.update(dip_olc(D, *w)); k.update(tur=r.sinif, sembol=r.sembol, s=w[0], e=w[1], uz=w[1] - w[0] + 1,
                                        iou=G.iou(w[0], w[1], int(r.bi0), int(r.si0)))
    rows.append(k)
for s_ad, D in DZ.items():
    et = e[e.sembol == s_ad]; kal = []
    for en in range(260, len(D['C']), 5):
        w = bolge2(D, en, **PRM)
        if not w: continue
        if any(w[0] <= b and w[1] >= a for a, b in zip(et.bi0, et.si0)): continue
        if any(G.iou(w[0], w[1], a, b) > 0.3 for a, b in kal): continue
        kal.append(w)
        k = {}
        for es in (0.1, 0.15, 0.25):
            k.update({f'{a}_{es}': v for a, v in doji_olc(D, *w, esik=es).items()})
        k.update(dip_olc(D, *w)); k.update(tur='DIGER', sembol=s_ad, s=w[0], e=w[1], uz=w[1] - w[0] + 1)
        rows.append(k)
t = pd.DataFrame(rows); t.to_csv('doji_tum.csv', index=False)
print(t.tur.value_counts().to_string())
c, o, d = (t[t.tur == x] for x in ('COL', 'OLUMSUZ', 'DIGER'))
OL = [x for x in t.columns if x.startswith(('doji', 'govde'))] + ['dip_konum', 'uz']
out = pd.DataFrame({m: {'col': c[m].median(), 'diger': d[m].median(), 'degil': o[m].median(),
                        'auc_diger': auc(c[m].to_numpy(float), d[m].to_numpy(float)),
                        'auc_degil': auc(c[m].to_numpy(float), o[m].to_numpy(float))} for m in OL}).T.round(3)
pd.set_option('display.width', 200)
print(out.sort_values('auc_diger', ascending=False).to_string())
