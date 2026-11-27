# GT8 bağımsız sağlama (K11): iki hücre satır dosyasından değil, ham fiyat + olay listesinden düz döngülerle yeniden üretilir; GOZ_TESPIT / MUM_IZI_HAVUZ
# ölçüm fonksiyonları KULLANILMAZ (yalnız veri yükleme MUM_IZI.mi_veri). (A) ANA ABD 2016-19 bölge sonu girişi; (B) ANA ABD 2020-22 tavan kırılımı girişi.
# Çalıştır: python arastirma_cikti/goz_tespit/gt8_sagla.py
import sys, json, pickle, logging, numpy as np, pandas as pd
sys.path.insert(0, '/home/user/col_yolu'); logging.disable(logging.INFO)
import MUM_IZI as MI
KES = pd.Timestamp('2022-12-31'); DON = {'d1619': ('2016-01-01', '2019-12-31'), 'd2022': ('2020-01-01', '2022-12-31')}
V = MI.mi_veri('ABD', '/tmp/mum_izi/acik')['V']; assert max(d.index.max() for d in V.values()) <= KES
OL = pickle.load(open('/root/.kasa/ham/goz_tespit/k3/k3_olay.pkl', 'rb')); Z = json.load(open('/home/user/col_yolu/arastirma_cikti/goz_tespit/gt8_ozet.json'))


def ilk(H, L, E0, a, b, x):
    """a..b barlarında High >= E0(1+x) önce mi (1), Low <= E0(1-x) mi (-1); aynı bar 2; hiçbiri 0."""
    for i in range(a, b + 1):
        u, d = H[i] >= E0 * (1 + x), L[i] <= E0 * (1 - x)
        if u and d:
            return 2
        if u:
            return 1
        if d:
            return -1
    return 0


def taban(d, dn):
    O, H, L, C = (d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close')); ix = d.index; a, b = map(pd.Timestamp, DON[dn]); R, S = [], []
    for k in range(19, len(d) - 15):
        if ix[k + 15] > KES or not (a <= ix[k + 1] <= b):
            continue
        E0 = O[k + 1]
        if not (E0 > 0 and E0 > L[k - 19:k + 1].min() * 0.98):
            continue
        R.append(C[k + 15] / E0 - 1); S.append(ilk(H, L, E0, k + 1, k + 15, 0.05))
    if len(R) < 30:
        return None
    S = np.array(S); return float(np.mean(R)), float(((S[S != 2]) == 1).mean())


# ---------------- (A) ANA ABD 2016-19
g = OL[(OL.kol == 'ANA') & (OL.hucre == 'ABD|d1619')]; sat = []; TB = {}
for r in g.itertuples():
    d = V[r.sembol]; O, H, L, C = (d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close')); t = int(r.t)
    if t + 15 >= len(d) or d.index[t + 15] > KES:
        continue
    E0 = O[t + 1]
    if not (E0 > 0 and E0 > L[int(r.s):t + 1].min() * 0.98):
        continue
    if r.sembol not in TB:
        TB[r.sembol] = taban(d, 'd1619')
    if TB[r.sembol] is None:
        continue
    sat.append((C[t + 15] / E0 - 1, TB[r.sembol][0], ilk(H, L, E0, t + 1, t + 15, 0.05), TB[r.sembol][1]))
X = np.array(sat); R, T1, s5, tb = X.T; m = s5 != 2
A_b = {'n': len(X), 'TF15': float((R - T1).mean()), 'medyan_fark': float(np.median(R) - np.median(T1)), 's5_pay': float((s5[m] == 1).mean()),
       's5_taban': float(tb[m].mean()), 's5_fark': float(((s5[m] == 1) - tb[m]).mean())}
o = Z['tablo']['A']['ANA']['ABD|d1619']
A_r = {'n': o['n'], 'TF15': o['TF15']['ort'], 'medyan_fark': o['medyan_fark'], 's5_pay': o['s5']['pay'], 's5_taban': o['s5']['taban'], 's5_fark': o['s5']['fark']['ort']}

# ---------------- (B) ANA ABD 2020-22
KR = pickle.load(open('/root/.kasa/ham/goz_tespit/k2/k2k_kontrol_kir.pkl', 'rb')); KR = KR[(KR.pazar == 'ABD') & (KR.donem == 'd2022') & ~KR.kesik]
g = OL[(OL.kol == 'ANA') & (OL.hucre == 'ABD|d2022')]; sat = []; KT = {}
for sem, gg in g.groupby('sembol'):
    d = V[sem]; O, H, L, C = (d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close')); ix = d.index; gec = np.flatnonzero(H > L); bs = []
    for r in gg.itertuples():
        t, s = int(r.t), int(r.s); TV, DP = H[s:t + 1].max(), L[s:t + 1].min(); iz = gec[gec > t][:20]
        if len(iz) < 20 or ix[iz[-1]] > KES:
            continue
        for i in iz:
            if C[i] > TV:
                bs.append(int(i)); break
            if C[i] < DP:
                break
    tut = []
    for b in sorted(set(bs)):
        if not tut or b - tut[-1] >= 15:
            tut.append(b)
    for b in tut:
        if b + 15 >= len(d) or ix[b + 15] > KES or not O[b + 1] > 0:
            continue
        if sem not in KT:                                                   # kontrol kırılımları: dosyadaki b günleri, ölçü ham fiyattan yeniden
            k = KR[KR.sembol == sem]; RR, SS = [], []
            for bb in k.b.astype(int):
                e0 = O[bb + 1]; RR.append(C[bb + 15] / e0 - 1); SS.append(ilk(H, L, e0, bb + 1, bb + 15, 0.05))
            SS = np.array(SS); KT[sem] = (float(np.mean(RR)), float((SS[SS != 2] == 1).mean())) if len(RR) >= 5 else None
        if KT[sem] is None:
            continue
        E0 = O[b + 1]; sat.append((C[b + 15] / E0 - 1, KT[sem][0], ilk(H, L, E0, b + 1, b + 15, 0.05), KT[sem][1]))
X = np.array(sat); R, T1k, s5, tb = X.T; m = s5 != 2
B_b = {'n': len(X), 'TFk15': float((R - T1k).mean()), 'medyan_fark': float(np.median(R) - np.median(T1k)), 's5_pay': float((s5[m] == 1).mean()),
       's5_taban': float(tb[m].mean()), 's5_fark': float(((s5[m] == 1) - tb[m]).mean())}
o = Z['tablo']['B']['ANA']['ABD|d2022']
B_r = {'n': o['n'], 'TFk15': o['TFk15']['ort'], 'medyan_fark': o['medyan_fark'], 's5_pay': o['s5']['pay'], 's5_taban': o['s5']['taban'], 's5_fark': o['s5']['fark']['ort']}
out = {'A_ANA_ABD_d1619': {'rapor': A_r, 'bagimsiz': A_b}, 'B_ANA_ABD_d2022': {'rapor': B_r, 'bagimsiz': B_b}}
for k, v in out.items():
    v['en_buyuk_fark'] = max(abs(float(v['rapor'][a]) - float(v['bagimsiz'][a])) for a in v['rapor'])
print(json.dumps(out, indent=1))
