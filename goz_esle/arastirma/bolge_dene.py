"""Cemal'in mantigi: col = fiyat bolgeden ayrilmiyor + zamanla pespese kucuk mumlar.
Pespese buyuk mumla fiyat bolgeden ayriliyorsa orasi col degil (col biter).
Tek buyuk mum fiyat bolgeye geri donuyorsa col bozulmaz.
Bu betik parametre izgarasini Cemal'in Eylul etiketlerinde (orijinal, kirpilmamis) olcer."""
import sys, itertools, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/col_yolu')
import GOZ_ESLE as G

ay = G.GozAyar(kok='etiket', buyuk_aralik=None, buyuk_degisim=None)   # kirpma yok: orijinal etiket
veri, e = G.k1_veri(ay)


def hazirla(df):
    O, H, L, C = (df[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close'))
    pc = np.r_[O[0], C[:-1]]
    ar = 100 * (H - L) / pc
    dg = 100 * (C / pc - 1)
    # hisseye ozel olcu (Cemal 19 Eki: agir hisse %5'i nadiren gecer): son 250 barin medyan gun araligi %
    ref = pd.Series(ar).rolling(250, min_periods=120).median().to_numpy()
    return O, H, L, C, ar, dg, ref


def bolge_col(D, e, bant, buyuk, ardisik=2, min_bar=15, en_cok=250, goreli=True):
    """e gununde biten col: geriye dogru, kapanislar bant icinde kaldikca ve
    pespese (ardisik) ayni yonlu buyuk mum yokken uzar. Donus (s,e) ya da None."""
    O, H, L, C, ar, dg, ref = D
    if goreli:                     # esikler hissenin kendi normal gun araliginin kati
        r = ref[e]
        if not np.isfinite(r) or r <= 0:
            return None
        buyuk = buyuk * r          # buyuk mum = normal gunun 'buyuk' kati
        bant = bant * r / 100      # bant = normal gunun 'bant' kati (kapanislar, %)
    hi = lo = C[e]
    s = e
    seri = 0; yon = 0
    for j in range(e, max(0, e - en_cok), -1):
        b = ar[j] >= buyuk or abs(dg[j]) >= buyuk * 0.9
        if b:
            y = 1 if dg[j] > 0 else -1
            seri = seri + 1 if (seri and y == yon) else 1
            yon = y
            if seri >= ardisik:
                break                      # pespese buyuk mum: bolgeden ayrilma -> col burada biter
        else:
            seri = 0
        h2, l2 = max(hi, C[j]), min(lo, C[j])
        if (h2 - l2) / np.median(C[j:e + 1]) > bant:
            break                          # fiyat bolgeden ayrildi
        hi, lo, s = h2, l2, j
    if seri >= ardisik:                    # serinin ilk mumu da colun disinda kalir
        s = max(s, j + ardisik)
    return (s, e) if e - s + 1 >= min_bar else None


def olc(bant, buyuk, ardisik, min_bar, goreli=True):
    rows = []
    for r in e.itertuples():
        D = DZ[r.sembol]
        w = bolge_col(D, int(r.si), bant, buyuk, ardisik, min_bar, goreli=goreli)
        io = G.iou(w[0], w[1], int(r.bi), int(r.si)) if w else 0.0
        rows.append((r.sinif, io, w is not None))
    t = pd.DataFrame(rows, columns=['sinif', 'iou', 'var'])
    c, o = t[t.sinif == 'COL'], t[t.sinif == 'OLUMSUZ']
    return dict(goreli=goreli, bant=bant, buyuk=buyuk, ardisik=ardisik, min_bar=min_bar,
                col_iou50=int((c.iou >= .5).sum()), col_iou_ort=round(c.iou.mean(), 2),
                col_var=int(c['var'].sum()), olm_var=int(o['var'].sum()), olm_iou50=int((o.iou >= .5).sum()))


DZ = {s: hazirla(df) for s, df in veri.items()}
if __name__ == '__main__':
    R = [olc(b, k, a, m, goreli=False) for b, k, a, m in itertools.product((0.12, 0.15, 0.20, 0.25, 0.30, 0.40), (6, 7, 8, 10), (2, 3), (15,))]
    R += [olc(b, k, a, m, goreli=True) for b, k, a, m in itertools.product((3, 4, 5, 6, 8, 10), (1.5, 2.0, 2.5, 3.0), (2, 3), (15,))]
    t = pd.DataFrame(R).sort_values(['col_iou50', 'col_iou_ort'], ascending=False)
    pd.set_option('display.width', 200)
    print(t.head(20).to_string(index=False))
    t.to_csv('bolge_izgara.csv', index=False)
