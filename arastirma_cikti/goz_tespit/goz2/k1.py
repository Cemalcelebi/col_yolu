# ÇÖL-K1: Cemal'in ilk set işaretlerinden öğrenilen üç özellik (27 Kas 2026; sabit): ince şerit + grafiğin altında + önce en az 2 kat tepe. Denetim aracı.
import sys, os, json, pickle, time, numpy as np, pandas as pd
sys.path.insert(0, '/home/user/col_yolu'); import logging; logging.disable(logging.INFO)
import MUM_IZI as MI, GOZ_TESPIT as GT
D = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(D); sys.path.insert(0, D)
from cetvel import goz_olcu
from levha import levha
K1 = dict(KUTU_ORAN=0.22, KUTU_YER=0.35, TEPE_KAT=2.0)
def k1(o): return bool(o and o['KUTU_ORAN'] <= K1['KUTU_ORAN'] and o['KUTU_YER'] <= K1['KUTU_YER'] and o['TEPE_KAT'] >= K1['TEPE_KAT'])
def olc(d, s, t): return goz_olcu(*(d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close')), int(s), int(t))
# 1) GT3 sayfalarında K1 x ana modelin mühürlü ön etiketi x kol
J = json.load(open(os.path.join(D, 'gt3_secim.json'), encoding='utf-8')); Y = json.load(open(os.path.join(D, 'gt3_goz_yargi.json'), encoding='utf-8'))['etiket']
et = {n: k for k, v in Y.items() for n in v}; VV = {}
def veri(p, kaynak):
    if (p, kaynak) not in VV: VV[(p, kaynak)] = MI.mi_veri(p, GT.GT_YOL['tam_bist'] if kaynak == 'tam' else GT.GT_YOL['acik'])['V']
    return VV[(p, kaynak)]
R = []
for r in J['sayfalar']:
    d = veri(r['pazar'], r['kaynak'])[r['sembol']]
    if r['kaynak'] == 'tam': d = d[d.index <= pd.Timestamp(J['kit_bit'][str(r['kitaplik_no'])])]
    R.append(dict(sayfa=r['sayfa'], kol=r['kol'], goz=et[r['sayfa']], K1=int(k1(olc(d, r['s'], r['t'])))))
T = pd.DataFrame(R); T.to_json(os.path.join(D, 'gt3_k1.json'), orient='records')
print('GT3: kol x ana modelin ön etiketi'); print(pd.crosstab(T.kol, T.goz)); print('\nGT3 D1 sayfaları: K1 x ön etiket'); print(pd.crosstab(T[T.kol == 'D1'].K1, T[T.kol == 'D1'].goz))
# 2) K1 havuzda: geçenler, 24 yeni + 8 rastgele, kör levha
kul = set()
for f in ('GT_onay_anahtar.json', 'GT2_onay_anahtar.json', 'GT3_onay_anahtar.json'):
    kul |= {(r['pazar'], r['sembol']) for r in json.load(open(os.path.join(C, f), encoding='utf-8'))['sayfalar']}
rng = np.random.default_rng(2719); H = []
for p in ('BIST', 'ABD'):
    t0 = time.time(); V = veri(p, 'acik'); P = pickle.load(open(f'/root/.kasa/ham/goz_tespit/pencere_{p}.pkl', 'rb')); P['tarih'] = pd.to_datetime(P['tarih'])
    Hv = P[(P.tarih >= '2016-01-01') & (P.tarih <= '2022-12-31') & (P.s >= 120) & (P.KIL <= 0.20) & (P.govdesiz_pay <= 0.30)][['sembol', 'L', 's', 't', 'ZIRVE_DUSUS', 'PUAN_ESIT']]
    F = Hv[Hv.ZIRVE_DUSUS <= -0.5]; G = []
    for sem, g in F.groupby('sembol'):
        d = V[sem]; O, Hh, L, Cc = (d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close'))
        for s, t, Lw in zip(g.s.values, g.t.values, g.L.values):
            if k1(goz_olcu(O, Hh, L, Cc, int(s), int(t))): G.append((sem, int(s), int(t), int(Lw)))
    G = pd.DataFrame(G, columns=['sembol', 's', 't', 'L'])
    print(f"{p}: havuz {len(Hv)}, ön süzgeç {len(F)}, K1 geçen {len(G)} (%{100 * len(G) / len(Hv):.2f}), hisse {G.sembol.nunique()} / {Hv.sembol.nunique()}, {time.time() - t0:.0f} sn")
    yeni = G[~G.sembol.map(lambda x: (p, x) in kul)]; sec = []
    for j in rng.permutation(len(yeni)):
        r = yeni.iloc[int(j)]
        if r.sembol in {x['sembol'] for x in sec}: continue
        sec.append(dict(kol='K1', pazar=p, sembol=r.sembol, s=int(r.s), t=int(r.t), L=int(r.L)))
        if len(sec) == 12: break
    n = 0
    for j in rng.permutation(len(Hv)):
        r = Hv.iloc[int(j)]
        if (p, r.sembol) in kul or r.sembol in {x['sembol'] for x in sec}: continue
        sec.append(dict(kol='RASTGELE', pazar=p, sembol=r.sembol, s=int(r.s), t=int(r.t), L=int(r.L))); n += 1
        if n == 4: break
    H += sec
for i, j in enumerate(rng.permutation(len(H))): H[j]['no'] = i + 1
H.sort(key=lambda r: r['no']); json.dump(H, open(os.path.join(D, 'k1_anahtar.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for b in range(0, len(H), 16):
    levha([(f"#{r['no']}", veri(r['pazar'], 'acik')[r['sembol']].iloc[:r['t'] + 1], r['s'], r['t']) for r in H[b:b + 16]], os.path.join(D, f'K1_LEVHA_{b // 16 + 1}.png'))
print('hücre', len(H))
