import sys, json, pickle, numpy as np, pandas as pd, time
sys.path.insert(0, '/home/user/col_yolu')
import logging; logging.disable(logging.INFO)
import MUM_IZI as MI, GOZ_TESPIT as GT
from cetvel import goz_olcu
from levha import levha
GOZ1 = dict(KUTU_YER=0.20, KUTU_ORAN=0.33, TEPE_KAT=(1.4, 10.0), BOY_ORAN=0.45, GOV_ORAN=0.45, EGIM=(-0.25, 0.70), ONCE_DIP=-0.08)
def gecer(o):
    return (o['KUTU_YER'] <= GOZ1['KUTU_YER'] and o['KUTU_ORAN'] <= GOZ1['KUTU_ORAN'] and GOZ1['TEPE_KAT'][0] <= o['TEPE_KAT'] <= GOZ1['TEPE_KAT'][1]
            and o['BOY_ORAN'] <= GOZ1['BOY_ORAN'] and o['GOV_ORAN'] <= GOZ1['GOV_ORAN'] and GOZ1['EGIM'][0] <= o['EGIM'] <= GOZ1['EGIM'][1] and o['ONCE_DIP'] >= GOZ1['ONCE_DIP'])
A = pickle.load(open('/root/.kasa/ham/goz_tespit/dedektor_aday.pkl', 'rb'))
print({p: {k: (len(v) if hasattr(v, '__len__') else v) for k, v in A[p].items()} for p in A})
SON = {}; VV = {}
for p in ('BIST', 'ABD'):
    t0 = time.time(); V = MI.mi_veri(p, GT.GT_YOL['acik'])['V']; VV[p] = V
    P = pickle.load(open(f'/root/.kasa/ham/goz_tespit/pencere_{p}.pkl', 'rb')); P['tarih'] = pd.to_datetime(P['tarih'])
    H = P[(P.tarih >= '2016-01-01') & (P.tarih <= '2022-12-31') & (P.s >= 120) & (P.KIL <= 0.20) & (P.govdesiz_pay <= 0.30)][['sembol', 'L', 's', 't', 'tarih', 'bas_tarih', 'BOY_GRAFIK_ORAN']]
    n_h = len(H); F = H[H.BOY_GRAFIK_ORAN <= 0.55]; R = []
    for sem, g in F.groupby('sembol'):
        d = V[sem]; O, Hh, L, C = (d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close'))
        for s, t, Lw in zip(g.s.values, g.t.values, g.L.values):
            o = goz_olcu(O, Hh, L, C, int(s), int(t))
            if o and gecer(o): R.append(dict(pazar=p, sembol=sem, s=int(s), t=int(t), L=int(Lw), son=str(d.index[int(t)].date()), **o))
    R = pd.DataFrame(R)
    # tekilleştirme: aynı hissede pencere sonları arasında < 60 bar ise tek pencere (rastgele değil: en erken)
    R = R.sort_values(['sembol', 't', 'L']); tut = []; son = {}
    for i, r in R.iterrows():
        if r.sembol in son and r.t - son[r.sembol] < 60: continue
        son[r.sembol] = r.t; tut.append(i)
    T = R.loc[tut]
    print(p, 'havuz', n_h, 'ön süzgeç', len(F), 'GÖZ-1 geçen', len(R), 'tekil', len(T), 'hisse', T.sembol.nunique(), f'{time.time() - t0:.0f} sn', dict(T.L.value_counts()))
    SON[p] = dict(gecen=T, havuz=H)
pickle.dump(SON, open('goz1.pkl', 'wb'))
# levha: 64 geçen (32 + 32) + 16 rastgele havuz, karışık; anahtar dosyada
rng = np.random.default_rng(2716); hucre = []
for p in ('BIST', 'ABD'):
    T = SON[p]['gecen']; ii = rng.choice(len(T), min(32, len(T)), replace=False)
    hucre += [dict(kol='GOZ1', **T.iloc[i][['pazar', 'sembol', 's', 't', 'L', 'son']].to_dict()) for i in ii]
    Hh = SON[p]['havuz']; jj = rng.choice(len(Hh), 8, replace=False)
    hucre += [dict(kol='RASTGELE', pazar=p, sembol=Hh.iloc[j].sembol, s=int(Hh.iloc[j].s), t=int(Hh.iloc[j].t), L=int(Hh.iloc[j].L), son=str(Hh.iloc[j].tarih.date())) for j in jj]
sira = rng.permutation(len(hucre)); hucre = [dict(hucre[i], no=k + 1) for k, i in enumerate(sira)]
json.dump(hucre, open('levha_anahtar.json', 'w'), ensure_ascii=False, default=int)
for b in range(0, len(hucre), 16):
    Hc = []
    for h in hucre[b:b + 16]:
        d = VV[h['pazar']][h['sembol']].iloc[:int(h['t']) + 1]; Hc.append((f"#{h['no']}", d, int(h['s']), int(h['t'])))
    levha(Hc, f'aday_{b // 16 + 1}.png')
print('hücre', len(hucre))
