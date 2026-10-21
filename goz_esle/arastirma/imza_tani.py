"""Tani: Cemal'in 29 colunden D12'nin kacirdiklari hangi kapiya takiliyor? (yerel, kalibre_veri.csv)
Her COL etiketi icin: etiket bitis gunu ve cevresinde (±5 bar) uretim col_dip(tani=True) -> en iyi (imza en cok) sonuc.
Ek olcu: kucuk mum oranini 60 barlik onceki normale gore (ref60) ve kutu sonu Bollinger sirasi."""
import sys, io, contextlib, numpy as np, pandas as pd
K = sys.argv[1]
ns = {'__name__': 'COL_v1_ns'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(f'{K}/COL_v1.py', encoding='utf-8').read(), f'{K}/COL_v1.py', 'exec'), ns)
col_dip, _bolge_dizi, _bb_genislik, _bolge_kutu = ns['col_dip'], ns['_bolge_dizi'], ns['_bb_genislik'], ns['_bolge_kutu']
v = pd.read_csv(f'{K}/kalibre_veri.csv', parse_dates=['tarih'])
et = pd.read_csv(f'{K}/kalibre_etiketler.csv', parse_dates=['bas', 'son'])
rows = []
for _, r in et.iterrows():
    df = v[v.sembol == r.sembol].set_index('tarih').sort_index()[['Open', 'High', 'Low', 'Close', 'Volume']]
    if df.empty: rows.append(dict(sembol=r.sembol, sinif=r.sinif, not_='veri yok')); continue
    idx = df.index.searchsorted(r.son)
    best = None
    for e in range(max(0, idx - 5), min(len(df) - 1, idx + 5) + 1):
        out, t = col_dip(df.iloc[:e + 1], tani=True)
        sk = (out is not None, t.get('imza', -1), -abs(e - idx))
        if best is None or sk > best[0]: best = (sk, out, t, e)
    sk, out, t, e = best
    x = df.iloc[:e + 1]; D = _bolge_dizi(x); w = _bolge_kutu(D, e)
    ek = {}
    if w:
        s, e2 = w
        ar = D['ar']; ref60 = np.nanmedian(ar[max(0, s - 60):s]); ref250 = D['ref'][s]
        ek['mum/ref250'] = round(float(np.nanmedian(ar[s:e2 + 1]) / ref250), 2)
        ek['mum/ref60'] = round(float(np.nanmedian(ar[s:e2 + 1]) / ref60), 2)
        ek['kucuk60'] = round(float(np.mean(ar[s:e2 + 1] <= ref60)), 2)
        bbw = _bb_genislik(x); pen = bbw[max(0, e2 - 249):e2 + 1]; pen = pen[np.isfinite(pen)]
        ek['bb_son'] = round(float((pen <= bbw[e2]).mean()), 2) if np.isfinite(bbw[e2]) else np.nan
        C = D['C']; z = C[s:e2 + 1]; n3 = max(1, len(z) // 3)
        ek['egim3'] = round(float(np.median(z[-n3:]) / np.median(z[:n3]) - 1) * 100, 1)   # ilk ucte bir -> son ucte bir %
        lo, hi = np.percentile(z, 10), np.percentile(z, 90); ek['bant/ref'] = round(float((hi - lo) / np.median(z) * 100 / ref250), 1)
    rows.append(dict(sembol=r.sembol, sinif=r.sinif, cemal=f"{r.bas.date()}→{r.son.date()}", kutu=f"{t.get('bas_tarih','-')}→{t.get('son_tarih','-')}",
                     uz=t.get('uz'), sonuc='COL' if out else t.get('red'), konum=t.get('konum'), yeni_dip=t.get('yeni_dip_yok'),
                     kucuk=t.get('kucuk_oran'), bb=t.get('bb_min'), doji=t.get('doji_kat'), hacim=t.get('hacim_kat'), imza=t.get('imza_ok'), **ek))
T = pd.DataFrame(rows)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
print(T.to_string(index=False))
T.to_csv(sys.argv[2], index=False)
