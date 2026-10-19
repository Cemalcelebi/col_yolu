"""Cemal 19 Eki 23:07: bolge + dip + bollinger sikismasi + kucuk mum + akumulasyon izi + hacim kurumasi
BIRLIKTE olculsun; olculer hisseye ozel (hissenin kendi gecmisine gore).
Bu betik: (1) her Cemal etiketi icin bolge kurali penceresi, (2) veri boyunca bolge kurali pencereleri (diger),
(3) her pencereye 'col karnesi' (5 grup), (4) Cemal COL vs OLUMSUZ vs diger kiyasi."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/col_yolu')
import GOZ_ESLE as G

ay = G.GozAyar(kok='etiket')
veri, e = G.k1_veri(ay)


def karne(df, s, e_):
    """Hisseye ozel (kendi gecmisine gore) col ozellikleri. Ileriye bakis yok."""
    O, H, L, C, V = (df[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close', 'Volume'))
    pc = np.r_[O[0], C[:-1]]
    ar = (H - L) / pc
    r = {}
    gec0 = max(0, s - 250)
    once = slice(gec0, s)
    z = slice(s, e_ + 1)
    if s - gec0 < 60:
        return r
    # 1) DIP: bolge medyani, bolge oncesi 250 barin araliginda nerede (0 dip, 1 tepe) + onceki tepeden dusus
    tl, th = L[once].min(), H[once].max()
    Pm = np.median(C[z])
    r['dip_konum'] = (Pm - tl) / (th - tl) if th > tl else np.nan
    r['onceki_dusus'] = Pm / th - 1
    # 2) BOLLINGER SIKISMASI: bolge sonundaki BB genisligi, hissenin kendi son 250 barindaki yeri (0 = en dar)
    cs = pd.Series(C[:e_ + 1])
    m = cs.rolling(20).mean(); sd = cs.rolling(20).std(ddof=0)
    bbw = (4 * sd / m).to_numpy()
    ref = bbw[max(0, e_ - 250):e_ + 1]; ref = ref[np.isfinite(ref)]
    r['bb_sira'] = float((ref <= bbw[e_]).mean()) if len(ref) > 50 else np.nan
    zz = bbw[s:e_ + 1]; zz = zz[np.isfinite(zz)]
    r['bb_min_sira'] = float((ref <= zz.min()).mean()) if len(ref) > 50 and len(zz) else np.nan
    # 3) KUCUK MUM: hissenin kendi normal gununden (bolge oncesi 250 bar medyan araligi) kucuk bar orani
    norm = np.median(ar[once])
    r['kucuk_mum'] = float((ar[z] <= norm).mean())
    r['mum_oran'] = float(np.median(ar[z]) / norm) if norm > 0 else np.nan
    # 4) AKUMULASYON IZI: yukselen gun hacmi / dusen gun hacmi, OBV egimi (bolge hacmine gore), CLV
    up = C[z] > pc[z]; dn = C[z] < pc[z]
    vu, vd = V[z][up].sum(), V[z][dn].sum()
    r['hacim_yon'] = float(vu / vd) if vd > 0 else np.nan
    obv = np.cumsum(np.sign(C[z] - pc[z]) * V[z])
    vm = V[z].mean()
    r['obv_egim'] = float(np.polyfit(np.arange(len(obv)), obv, 1)[0] / vm) if vm > 0 and len(obv) > 3 else np.nan
    rng = H[z] - L[z]
    r['clv'] = float(np.mean(np.where(rng > 0, ((C[z] - L[z]) - (H[z] - C[z])) / np.where(rng > 0, rng, 1), 0)))
    # 5) HACIM KURUMASI: bolge medyan hacmi / bolge oncesi 120 bar medyan hacmi
    v0 = np.median(V[max(0, s - 120):s])
    r['hacim_kuruma'] = float(np.median(V[z]) / v0) if v0 > 0 else np.nan
    r['uz'] = e_ - s + 1
    return r


rows = []
etk_bolge = {}
for r in e.itertuples():
    D = G.bolge_hazirla(veri[r.sembol])
    w = G.bolge_col(D, int(r.si0), ay)
    if not w:
        continue
    k = karne(veri[r.sembol], *w)
    k.update(tur=r.sinif, sembol=r.sembol, etiket=r.etiket_id, s=w[0], e=w[1])
    rows.append(k)
# diger bolgeler: etiketlere degmeyen gunlerde, 5 gunde bir
for s_ad, df in veri.items():
    D = G.bolge_hazirla(df)
    et = e[e.sembol == s_ad]
    son_e = -999
    for en in range(260, len(df), 5):
        w = G.bolge_col(D, en, ay)
        if not w:
            continue
        if any(G.iou(w[0], w[1], int(a), int(b)) > 0.1 or (w[0] <= b and w[1] >= a) for a, b in zip(et.bi0, et.si0)):
            continue
        if en - son_e < 20:          # ayni bolgeyi tekrar sayma
            continue
        son_e = en
        k = karne(df, *w)
        k.update(tur='DIGER', sembol=s_ad, etiket='', s=w[0], e=w[1])
        rows.append(k)
t = pd.DataFrame(rows)
t.to_csv('karne_tum.csv', index=False)
OL = ['dip_konum', 'onceki_dusus', 'bb_sira', 'bb_min_sira', 'kucuk_mum', 'mum_oran', 'hacim_yon', 'obv_egim', 'clv', 'hacim_kuruma', 'uz']
pd.set_option('display.width', 220)
print(t.tur.value_counts().to_string())
print(t.groupby('tur')[OL].median().round(2).T.to_string())
from scipy.stats import rankdata
def auc(a, b):
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 3 or len(b) < 3: return np.nan
    rr = rankdata(np.r_[a, b]); return (rr[:len(a)].sum() - len(a) * (len(a) + 1) / 2) / (len(a) * len(b))
c, o, d = (t[t.tur == x] for x in ('COL', 'OLUMSUZ', 'DIGER'))
print(pd.DataFrame({m: {'auc_vs_diger': auc(c[m].to_numpy(float), d[m].to_numpy(float)),
                        'auc_vs_olumsuz': auc(c[m].to_numpy(float), o[m].to_numpy(float))} for m in OL}).T.round(2).to_string())
