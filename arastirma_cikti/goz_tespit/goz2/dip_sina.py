# DİP PARABOLÜ: (1) yapay sağlama + eşik basamağı (yalnız yapay negatif sınırlarıyla), (2) Cemal'in ilk set işaretleri, (3) GT3 ön kayıt bayrağı, (4) havuz: K1 + DİP PARABOLÜ kör levha.
import sys, os, json, pickle, numpy as np, pandas as pd
sys.path.insert(0, '/home/user/col_yolu'); import logging; logging.disable(logging.INFO)
import MUM_IZI as MI, GOZ_TESPIT as GT
D = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(D); sys.path.insert(0, D)
from cetvel import goz_olcu
from levha import levha
from parabol import dip_parabol, dip_parabol_var, DIP_PARABOL_KURAL
rng = np.random.default_rng(28)
def uret(tip, g):
    x = np.arange(60); son = np.linspace(-1, 1, 20)
    if tip in ('U dönüş', 'U + sonda daha derin dip'): d = np.r_[100 - 0.10 * x[:40], 96 + 2.0 * (son + 0.3) ** 2 - 0.98]
    elif tip == 'düz': d = np.full(60, 100.0)
    elif tip == 'düzenli aşağı kayma': d = 100 - 0.12 * x
    elif tip == 'yavaşlayan düşüş (dibi sonda)': d = 100 - 8 * (1 - np.exp(-x / 25.0))
    elif tip == 'kubbe (ters)': d = np.r_[np.full(40, 100.0), 100 - 2.0 * (son + 0.3) ** 2 + 0.98]
    elif tip == 'rastgele yürüyüş': d = 100 + np.cumsum(rng.normal(0, 0.25, 60))
    l = d + rng.normal(0, g, 60)
    if tip == 'U + sonda daha derin dip': l[-2] = l.min() - 0.8
    h = l + 0.3 + np.abs(rng.normal(0, 1.2, 60))                      # üst taraf oynak (bir yukarı bir aşağı)
    return h, l
TIP = ['U dönüş', 'U + sonda daha derin dip', 'düz', 'düzenli aşağı kayma', 'yavaşlayan düşüş (dibi sonda)', 'kubbe (ters)', 'rastgele yürüyüş']
SINIR = {'U dönüş': ('>=', 0.90), 'U + sonda daha derin dip': ('<=', 0.02), 'düz': ('<=', 0.10), 'düzenli aşağı kayma': ('<=', 0.02), 'yavaşlayan düşüş (dibi sonda)': ('<=', 0.05), 'kubbe (ters)': ('<=', 0.01), 'rastgele yürüyüş': ('<=', 0.10)}
ORN = {(t, g): [uret(t, g) for _ in range(400)] for t in TIP for g in (0.10, 0.30)}; sec = None
for r2, yk in [(0.40, 0.15), (0.50, 0.20), (0.60, 0.25), (0.70, 0.30)]:
    K = dict(DIP_PARABOL_KURAL, r2=r2, yukselis=yk); pay = {k: float(np.mean([dip_parabol_var(dip_parabol(h, l, 0, 59, K), K) for h, l in v])) for k, v in ORN.items()}
    uy = all((pay[(t, g)] >= s) if y == '>=' else (pay[(t, g)] <= s) for t, (y, s) in SINIR.items() for g in (0.10, 0.30))
    print(f'basamak r2 >= {r2:.2f}, yükseliş >= {yk:.2f}: ' + '; '.join(f'{t[:14]} {100 * pay[(t, 0.10)]:.0f}/{100 * pay[(t, 0.30)]:.0f}' for t in TIP) + (' -> SINIRLAR TUTTU' if uy else ''))
    if uy and sec is None: sec = K
if sec is None: print('HİÇBİR BASAMAK sınırları tutmadı; en sıkı basamak kullanılıyor'); sec = K
K = sec; json.dump(K, open(os.path.join(D, 'dip_parabol_kural.json'), 'w'), indent=1)
def dv(H, L, s, t): return int(dip_parabol_var(dip_parabol(H, L, s, t, K), K))
VV = {}
def veri(p, kaynak):
    if (p, kaynak) not in VV: VV[(p, kaynak)] = MI.mi_veri(p, GT.GT_YOL['tam_bist'] if kaynak == 'tam' else GT.GT_YOL['acik'])['V']
    return VV[(p, kaynak)]
# (2) Cemal'in ilk seti
C1 = json.load(open(os.path.join(C, 'cemal_gt_onay.json'), encoding='utf-8')); A1 = json.load(open(os.path.join(C, 'GT_onay_anahtar.json'), encoding='utf-8'))['sayfalar']; KT = {r['no']: r for r in json.load(open('/root/.kasa/ham/goz_tespit/kitaplik_olcu.json', encoding='utf-8')) if r['durum'] == 'tamam'}; R = []
for r in A1:
    d = veri(r['pazar'], r['kaynak'])[r['sembol']]
    if r['kaynak'] == 'tam': d = d[d.index <= pd.Timestamp(KT[r['kitaplik_no']]['bit'])]
    R.append(dict(sayfa=r['sayfa'], kol=r['kol'], cemal=C1['sinif4'][str(r['sayfa'])], DIP=dv(d['High'].to_numpy(float), d['Low'].to_numpy(float), int(r['s']), int(r['t']))))
T = pd.DataFrame(R); Dd = T[T.kol != 'RASTGELE']; print('\nİLK SET (rastgele hariç 24): DİP PARABOLÜ x Cemal'); print(pd.crosstab(Dd.DIP, Dd.cemal).to_string()); print('geçen sayfalar:', {int(a): b for a, b in zip(Dd[Dd.DIP == 1].sayfa, Dd[Dd.DIP == 1].cemal)}, '| rastgele 6:', T[T.kol == 'RASTGELE'].DIP.tolist())
# (3) GT3 ön kayıt
J = json.load(open(os.path.join(D, 'gt3_secim.json'), encoding='utf-8')); Y = json.load(open(os.path.join(D, 'gt3_goz_yargi.json'), encoding='utf-8'))['etiket']; et = {n: k for k, v in Y.items() for n in v}; R = []
for r in J['sayfalar']:
    d = veri(r['pazar'], r['kaynak'])[r['sembol']]
    if r['kaynak'] == 'tam': d = d[d.index <= pd.Timestamp(J['kit_bit'][str(r['kitaplik_no'])])]
    R.append(dict(sayfa=r['sayfa'], kol=r['kol'], goz=et[r['sayfa']], DIP=dv(d['High'].to_numpy(float), d['Low'].to_numpy(float), int(r['s']), int(r['t']))))
T3 = pd.DataFrame(R); json.dump(dict(kural=K, not_="ÖN KAYIT (Cemal'in GT3 işaretlerinden önce): DİP PARABOLÜ = bölgenin son üçte birinde (en az 10 mum) mum dipleri yukarı açılan parabol çiziyor, sonda daha derin dip yok", sayfalar=R), open(os.path.join(D, 'gt3_dip_parabol_onkayit.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nGT3: DİP PARABOLÜ x kol'); print(pd.crosstab(T3.kol, T3.DIP).to_string()); print('GT3 D1: DİP PARABOLÜ x ana modelin ön etiketi'); print(pd.crosstab(T3[T3.kol == 'D1'].DIP, T3[T3.kol == 'D1'].goz).to_string())
# (4) havuz
K1 = dict(KUTU_ORAN=0.22, KUTU_YER=0.35, TEPE_KAT=2.0); kul = set()
for f in ('GT_onay_anahtar.json', 'GT2_onay_anahtar.json', 'GT3_onay_anahtar.json'): kul |= {(r['pazar'], r['sembol']) for r in json.load(open(os.path.join(C, f), encoding='utf-8'))['sayfalar']}
kul |= {(r['pazar'], r['sembol']) for r in json.load(open(os.path.join(D, 'k1_anahtar.json'), encoding='utf-8'))}
rs = np.random.default_rng(2721); Hc = []
for p in ('BIST', 'ABD'):
    V = veri(p, 'acik'); P = pickle.load(open(f'/root/.kasa/ham/goz_tespit/pencere_{p}.pkl', 'rb')); P['tarih'] = pd.to_datetime(P['tarih'])
    Hv = P[(P.tarih >= '2016-01-01') & (P.tarih <= '2022-12-31') & (P.s >= 120) & (P.KIL <= 0.20) & (P.govdesiz_pay <= 0.30)][['sembol', 'L', 's', 't', 'ZIRVE_DUSUS']]
    F = Hv[Hv.ZIRVE_DUSUS <= -0.5]; G = []; nk1 = 0; nh = 0; nhp = 0
    for sem, g in Hv.groupby('sembol'):                                   # havuzun tamamında taban oran (her 7. pencere)
        d = V[sem]; Hh, L = d['High'].to_numpy(float), d['Low'].to_numpy(float)
        for s, t in zip(g.s.values[::7], g.t.values[::7]): nh += 1; nhp += dv(Hh, L, int(s), int(t))
    for sem, g in F.groupby('sembol'):
        d = V[sem]; O, Hh, L, Cc = (d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close'))
        for s, t, Lw in zip(g.s.values, g.t.values, g.L.values):
            o = goz_olcu(O, Hh, L, Cc, int(s), int(t))
            if o and o['KUTU_ORAN'] <= K1['KUTU_ORAN'] and o['KUTU_YER'] <= K1['KUTU_YER'] and o['TEPE_KAT'] >= K1['TEPE_KAT']:
                nk1 += 1
                if dv(Hh, L, int(s), int(t)): G.append((sem, int(s), int(t), int(Lw)))
    G = pd.DataFrame(G, columns=['sembol', 's', 't', 'L']); print(f'{p}: havuzda DİP PARABOLÜ %{100 * nhp / nh:.1f} (örnek {nh}); K1 {nk1}; K1 + DİP PARABOLÜ {len(G)} (K1 içinde %{100 * len(G) / max(nk1, 1):.1f}; havuzun %{100 * len(G) / len(Hv):.2f}), hisse {G.sembol.nunique()}')
    yeni = G[~G.sembol.map(lambda x: (p, x) in kul)]; sec_ = []
    for j in rs.permutation(len(yeni)):
        r = yeni.iloc[int(j)]
        if r.sembol in {x['sembol'] for x in sec_}: continue
        sec_.append(dict(kol='K1+DIP', pazar=p, sembol=r.sembol, s=int(r.s), t=int(r.t), L=int(r.L)))
        if len(sec_) == 8: break
    n = 0
    for j in rs.permutation(len(Hv)):
        r = Hv.iloc[int(j)]
        if (p, r.sembol) in kul or r.sembol in {x['sembol'] for x in sec_}: continue
        sec_.append(dict(kol='RASTGELE', pazar=p, sembol=r.sembol, s=int(r.s), t=int(r.t), L=int(r.L))); n += 1
        if n == 2: break
    Hc += sec_
for i, j in enumerate(rs.permutation(len(Hc))): Hc[j]['no'] = i + 1
Hc.sort(key=lambda r: r['no']); json.dump(Hc, open(os.path.join(D, 'dip_anahtar.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
levha([(f"#{r['no']}", veri(r['pazar'], 'acik')[r['sembol']].iloc[:r['t'] + 1], r['s'], r['t']) for r in Hc], os.path.join(D, 'DIP_LEVHA.png'), sutun=5); print('hücre', len(Hc))
