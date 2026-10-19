"""Cemal 19 Eki 23:28 ince ayar:
 (1) fiyat bolgeden AZ ayrilip donerse kabul; COK ayrilip donerse o bolge col degil
 (2) bolgenin solundaki inis (dev) mumlari cole dahil edilmemeli
 (3) en kritik: DOJI. Bolgede cok doji + dipte -> col. Agirlik burada.
Hisseye ozel olcu: ref = son 250 bar medyan gun araligi (%)."""
import sys, itertools, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/col_yolu')
import GOZ_ESLE as G
from scipy.stats import rankdata

ay = G.GozAyar(kok='etiket')
veri, e = G.k1_veri(ay)


def hazirla(df):
    O, H, L, C, V = (df[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close', 'Volume'))
    pc = np.r_[O[0], C[:-1]]
    ar = 100 * (H - L) / pc
    dg = 100 * (C / pc - 1)
    ref = pd.Series(ar).rolling(250, min_periods=120).median().to_numpy()
    rng = H - L
    govde_oran = np.where(rng > 0, np.abs(C - O) / np.where(rng > 0, rng, 1), 1.0)
    return dict(O=O, H=H, L=L, C=C, V=V, ar=ar, dg=dg, ref=ref, go=govde_oran)


def bolge2(D, e, bant_kat=5.0, uzak_kat=2.0, buyuk_kat=2.0, ardisik=3, min_bar=15, en_cok=250, sol_kat=1.5):
    """Geriye dogru buyuyen bolge.
    cekirdek = kapanislarin %10-%90 araligi (bolge buyudukce guncellenir).
    (a) cekirdek bandi > bant_kat x ref -> dur (bolge genisledi)
    (b) bir kapanis cekirdegin uzak_kat x ref otesinde -> dur (COK ayrilma; az ayrilma kabul)
    (c) ardisik ayni yonlu buyuk mum -> dur
    Sonra (2) SOL KIRPMA: bolgenin basindaki, gun araligi > sol_kat x ref olan ya da kapanisi cekirdek
    disinda kalan barlar atilir (bolgeye inis mumlari)."""
    C, ar, dg, ref = D['C'], D['ar'], D['dg'], D['ref']
    r = ref[e]
    if not np.isfinite(r) or r <= 0:
        return None
    P = C[e]
    s = e; seri = 0; yon = 0
    for j in range(e - 1, max(-1, e - en_cok), -1):
        if ar[j] >= buyuk_kat * r or abs(dg[j]) >= 0.9 * buyuk_kat * r:
            y = 1 if dg[j] > 0 else -1
            seri = seri + 1 if (seri and y == yon) else 1; yon = y
            if seri >= ardisik:
                s = max(s, j + ardisik); break
        else:
            seri = 0
        z = C[j:e + 1]
        lo, hi = np.percentile(z, 10), np.percentile(z, 90)
        med = np.median(z)
        if (hi - lo) / med * 100 > bant_kat * r:
            break
        tol = uzak_kat * r / 100 * med
        if C[j] > hi + tol or C[j] < lo - tol:
            break
        s = j
    # SOL KIRPMA
    z = C[s:e + 1]
    lo, hi = np.percentile(z, 10), np.percentile(z, 90)
    while s < e and (ar[s] > sol_kat * r or C[s] > hi or C[s] < lo):
        s += 1
    return (s, e) if e - s + 1 >= min_bar else None


def doji_olc(D, s, e, esik=0.15):
    go = D['go']; ar = D['ar']; ref = D['ref']
    r = ref[e]
    z = slice(s, e + 1)
    once = slice(max(0, s - 250), s)
    d = go[z] < esik
    d0 = go[once] < esik
    kucuk = ar[z] <= r
    return {
        'doji': float(d.mean()),
        'doji_goreli': float(d.mean() / d0.mean()) if d0.mean() > 0 else np.nan,     # hissenin kendi doji oranina gore
        'doji_kucuk': float((d & kucuk).mean()),                                      # kucuk doji (fitil dahil kucuk)
        'doji_yogun_max': float(pd.Series(d.astype(float)).rolling(10, min_periods=5).mean().max()),  # en yogun 10 bar
        'govde_med': float(np.median(go[z])),
    }


def dip_olc(D, s, e):
    H, L, C = D['H'], D['L'], D['C']
    o = slice(max(0, s - 250), s)
    if s < 60:
        return {'dip_konum': np.nan}
    tl, th = L[o].min(), H[o].max()
    return {'dip_konum': float((np.median(C[s:e + 1]) - tl) / (th - tl)) if th > tl else np.nan}


DZ = {s: hazirla(df) for s, df in veri.items()}


def esles(**kw):
    rows = []
    for r in e.itertuples():
        w = bolge2(DZ[r.sembol], int(r.si0), **kw)
        rows.append((r.sinif, G.iou(w[0], w[1], int(r.bi0), int(r.si0)) if w else 0.0, w))
    return rows


if __name__ == '__main__':
    R = []
    for bk, uk, sk in itertools.product((4, 5, 6, 8), (1.0, 1.5, 2.0, 3.0), (1.2, 1.5, 2.0)):
        rr = esles(bant_kat=bk, uzak_kat=uk, sol_kat=sk)
        c = [x for x in rr if x[0] == 'COL']
        R.append(dict(bant=bk, uzak=uk, sol=sk, col_iou50=sum(x[1] >= .5 for x in c), ort=round(np.mean([x[1] for x in c]), 3)))
    t = pd.DataFrame(R).sort_values(['col_iou50', 'ort'], ascending=False)
    print(t.head(10).to_string(index=False))
    t.to_csv('bolge2_izgara.csv', index=False)
