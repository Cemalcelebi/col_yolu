# PARABOL şartı: (1) yapay sağlama, (2) GT3 sayfalarında ön kayıt bayrağı, (3) havuzda K1 + PARABOL: 16 yeni bölge + 4 rastgele, kör levha. Denetim aracı.
import sys, os, json, pickle, time, numpy as np, pandas as pd
sys.path.insert(0, '/home/user/col_yolu'); import logging; logging.disable(logging.INFO)
import MUM_IZI as MI, GOZ_TESPIT as GT
D = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(D); sys.path.insert(0, D)
from cetvel import goz_olcu
from levha import levha
from parabol import parabol, parabol_var, PARABOL_KURAL
K = dict(PARABOL_KURAL, bolum='ucte')
def pv(H, L, Cc, s, t): return parabol_var(parabol(H, L, Cc, s, t, 'ucte'), K)
# (1) yapay: 60 barlık bölge; son üçte bir = 20 bar
rng = np.random.default_rng(27); say = {}
def uret(tip, g):
    x = np.arange(60); son = np.linspace(-1, 1, 20)
    if tip == 'U dönüş': y = np.r_[100 - 0.10 * x[:40], 96 + 2.0 * (son + 0.3) ** 2 - 2.0 * 0.49]
    elif tip == 'düz': y = np.full(60, 100.0)
    elif tip == 'düzenli aşağı kayma': y = 100 - 0.12 * x
    elif tip == 'yavaşlayan düşüş (dibi sonda)': y = 100 - 8 * (1 - np.exp(-x / 25.0))
    elif tip == 'kubbe (ters)': y = np.r_[np.full(40, 100.0), 100 - 2.0 * (son + 0.3) ** 2 + 2.0 * 0.49]
    elif tip == 'rastgele yürüyüş': y = 100 + np.cumsum(rng.normal(0, 0.25, 60))
    c = y + rng.normal(0, g, 60); h = c + np.abs(rng.normal(0, g, 60)) + 0.05; l = c - np.abs(rng.normal(0, g, 60)) - 0.05
    return h, l, c
for tip in ('U dönüş', 'düz', 'düzenli aşağı kayma', 'yavaşlayan düşüş (dibi sonda)', 'kubbe (ters)', 'rastgele yürüyüş'):
    for g in (0.10, 0.30):
        say[(tip, g)] = int(sum(pv(*uret(tip, g), 0, 59) for _ in range(400)))
print('YAPAY (400 deneme; PARABOL geçen):'); [print(f'  {t:<32} gürültü {g:.2f}: {v:>3} / 400 (%{v / 4:.0f})') for (t, g), v in say.items()]
# (2) GT3 ön kayıt bayrağı
J = json.load(open(os.path.join(D, 'gt3_secim.json'), encoding='utf-8')); Y = json.load(open(os.path.join(D, 'gt3_goz_yargi.json'), encoding='utf-8'))['etiket']; et = {n: k for k, v in Y.items() for n in v}; VV = {}
def veri(p, kaynak):
    if (p, kaynak) not in VV: VV[(p, kaynak)] = MI.mi_veri(p, GT.GT_YOL['tam_bist'] if kaynak == 'tam' else GT.GT_YOL['acik'])['V']
    return VV[(p, kaynak)]
R = []
for r in J['sayfalar']:
    d = veri(r['pazar'], r['kaynak'])[r['sembol']]
    if r['kaynak'] == 'tam': d = d[d.index <= pd.Timestamp(J['kit_bit'][str(r['kitaplik_no'])])]
    H, L, Cc = (d[c].to_numpy(float) for c in ('High', 'Low', 'Close')); R.append(dict(sayfa=r['sayfa'], kol=r['kol'], goz=et[r['sayfa']], PARABOL=int(pv(H, L, Cc, int(r['s']), int(r['t'])))))
T = pd.DataFrame(R); json.dump(dict(kural=K, not_="ÖN KAYIT (Cemal'in GT3 işaretlerinden önce): PARABOL = bölgenin son üçte birinde (en az 10 mum) yukarı açılan parabol", sayfalar=R), open(os.path.join(D, 'gt3_parabol_onkayit.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nGT3: PARABOL x kol'); print(pd.crosstab(T.kol, T.PARABOL).to_string()); print('GT3 D1: PARABOL x ana modelin ön etiketi'); print(pd.crosstab(T[T.kol == 'D1'].PARABOL, T[T.kol == 'D1'].goz).to_string())
# (3) havuz: K1 + PARABOL
K1 = dict(KUTU_ORAN=0.22, KUTU_YER=0.35, TEPE_KAT=2.0)
kul = set()
for f in ('GT_onay_anahtar.json', 'GT2_onay_anahtar.json', 'GT3_onay_anahtar.json'): kul |= {(r['pazar'], r['sembol']) for r in json.load(open(os.path.join(C, f), encoding='utf-8'))['sayfalar']}
kul |= {(r['pazar'], r['sembol']) for r in json.load(open(os.path.join(D, 'k1_anahtar.json'), encoding='utf-8'))}
rs = np.random.default_rng(2720); Hc = []
for p in ('BIST', 'ABD'):
    V = veri(p, 'acik'); P = pickle.load(open(f'/root/.kasa/ham/goz_tespit/pencere_{p}.pkl', 'rb')); P['tarih'] = pd.to_datetime(P['tarih'])
    Hv = P[(P.tarih >= '2016-01-01') & (P.tarih <= '2022-12-31') & (P.s >= 120) & (P.KIL <= 0.20) & (P.govdesiz_pay <= 0.30)][['sembol', 'L', 's', 't', 'ZIRVE_DUSUS']]
    F = Hv[Hv.ZIRVE_DUSUS <= -0.5]; G = []; nk1 = 0
    for sem, g in F.groupby('sembol'):
        d = V[sem]; O, Hh, L, Cc = (d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close'))
        for s, t, Lw in zip(g.s.values, g.t.values, g.L.values):
            o = goz_olcu(O, Hh, L, Cc, int(s), int(t))
            if o and o['KUTU_ORAN'] <= K1['KUTU_ORAN'] and o['KUTU_YER'] <= K1['KUTU_YER'] and o['TEPE_KAT'] >= K1['TEPE_KAT']:
                nk1 += 1
                if pv(Hh, L, Cc, int(s), int(t)): G.append((sem, int(s), int(t), int(Lw)))
    G = pd.DataFrame(G, columns=['sembol', 's', 't', 'L']); print(f'{p}: havuz {len(Hv)}, K1 {nk1}, K1 + PARABOL {len(G)} (K1 içinde %{100 * len(G) / max(nk1, 1):.0f}; havuzun %{100 * len(G) / len(Hv):.2f}), hisse {G.sembol.nunique()}')
    yeni = G[~G.sembol.map(lambda x: (p, x) in kul)]; sec = []
    for j in rs.permutation(len(yeni)):
        r = yeni.iloc[int(j)]
        if r.sembol in {x['sembol'] for x in sec}: continue
        sec.append(dict(kol='K1+PARABOL', pazar=p, sembol=r.sembol, s=int(r.s), t=int(r.t), L=int(r.L)))
        if len(sec) == 8: break
    n = 0
    for j in rs.permutation(len(Hv)):
        r = Hv.iloc[int(j)]
        if (p, r.sembol) in kul or r.sembol in {x['sembol'] for x in sec}: continue
        sec.append(dict(kol='RASTGELE', pazar=p, sembol=r.sembol, s=int(r.s), t=int(r.t), L=int(r.L))); n += 1
        if n == 2: break
    Hc += sec
for i, j in enumerate(rs.permutation(len(Hc))): Hc[j]['no'] = i + 1
Hc.sort(key=lambda r: r['no']); json.dump(Hc, open(os.path.join(D, 'parabol_anahtar.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
levha([(f"#{r['no']}", veri(r['pazar'], 'acik')[r['sembol']].iloc[:r['t'] + 1], r['s'], r['t']) for r in Hc], os.path.join(D, 'PARABOL_LEVHA.png'), sutun=5)
print('hücre', len(Hc))
