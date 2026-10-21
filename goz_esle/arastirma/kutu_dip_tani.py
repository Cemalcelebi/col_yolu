"""Olcum (21 Eki, Cemal'in notu): OYLUM/EUYO'da kod, dusus ONCESI kucuk mumlu bolgeyi + dususu + yeni dibi tek kutu saydi.
Cemal: 'onceki bolge dibi kirilinca biter; col yeni dipten sonra sayilir.'
Burada uretim kutusuna (COL_v1._bolge_kutu) iki aday duzeltme uygulanip 37 etikette olculuyor:
  A) RAF KESME: kutudaki en dusuk dibin gunu d; d'den onceki kapanislarin medyani, d'den sonraki kapanislarin %90'inin
     ustundeyse (onceki bolge daha yuksek bir raf) kutu d'den baslar. Dip ayni seviyedeki bir fitilse kutu degismez.
  B) BANT 4x (BOLGE_BANT_KAT 6 -> 4) + A.
Her etiket icin: uretim sonucu, A ve B sonucu (kutu, bar, konum, imza, red). Yalniz kalibre_veri.csv (yerel), ileriye bakis yok.
Calistirma: python3 kutu_dip_tani.py <repo_kok> <cikti_csv>"""
import sys, io, contextlib, numpy as np, pandas as pd

K = sys.argv[1]
ns = {'__name__': 'COL_v1_ns'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(f'{K}/COL_v1.py', encoding='utf-8').read(), f'{K}/COL_v1.py', 'exec'), ns)
MIN_UZ, DIP_KONUM, DIP_SON_PAY, IMZA_MIN = ns['MIN_UZ'], ns['DIP_KONUM'], ns['DIP_SON_PAY'], ns['IMZA_MIN']
IMZA_KUCUK, IMZA_BB, IMZA_DOJI, IMZA_HACIM = ns['IMZA_KUCUK'], ns['IMZA_BB'], ns['IMZA_DOJI'], ns['IMZA_HACIM']


def kapilar(x, D, bbw, s, e):
    """_col_dip_e'nin (2) dipte (3) yeni dip yok (4) imza hesaplari, verilen (s, e) kutusu icin — uretimle ayni formuller."""
    C, H, L, ar, ref, go = D['C'], D['H'], D['L'], D['ar'], D['ref'], D['go']
    uz = e - s + 1
    r0 = ref[s] if (np.isfinite(ref[s]) and ref[s] > 0) else ref[e]
    o0 = max(0, s - 250)
    if s - o0 < 60: return dict(red='gecmis kisa', uz=uz)
    lo, hi = float(np.nanmin(L[o0:e + 1])), float(np.nanmax(H[o0:e + 1]))
    konum = float((np.median(C[s:e + 1]) - lo) / (hi - lo)) if hi > lo else np.nan
    k = s + max(1, int(round((1 - DIP_SON_PAY) * uz)))
    d1, d2 = float(np.nanmin(L[s:k])), float(np.nanmin(L[k:e + 1]))
    yeni_dip_yok = bool(d2 >= d1 * (1 - 0.5 * r0 / 100))
    kucuk = float(np.mean(ar[s:e + 1] <= r0))
    pen = bbw[max(0, e - 249):e + 1]; pen = pen[np.isfinite(pen)]
    kb = bbw[s:e + 1]; kb = kb[np.isfinite(kb)]
    bb = float((pen <= kb.min()).mean()) if (len(pen) >= 60 and len(kb)) else np.nan
    dj, dj0 = float((go[s:e + 1] < 0.10).mean()), float((go[o0:s] < 0.10).mean())
    doji_kat = (dj / dj0 if dj0 > 0 else (np.inf if dj > 0 else np.nan))
    V = x['Volume'].to_numpy(float)
    v1, v0 = np.nanmedian(V[s:e + 1]), np.nanmedian(V[max(0, s - 60):s])
    hacim_kat = float(v1 / v0) if (np.isfinite(v0) and v0 > 0 and np.isfinite(v1)) else np.nan
    imza = {'kucuk': kucuk >= IMZA_KUCUK, 'bollinger': bool(np.isfinite(bb) and bb <= IMZA_BB),
            'doji': bool(np.isfinite(doji_kat) and doji_kat >= IMZA_DOJI), 'hacim': bool(np.isfinite(hacim_kat) and hacim_kat <= IMZA_HACIM)}
    t = dict(uz=uz, konum=round(konum, 3), yeni_dip_yok=yeni_dip_yok, imza=int(sum(imza.values())), imza_ok=','.join(a for a, v in imza.items() if v))
    if uz < MIN_UZ: t['red'] = 'kisa'
    elif not (np.isfinite(konum) and konum <= DIP_KONUM): t['red'] = 'dipte degil'
    elif not yeni_dip_yok: t['red'] = 'yeni dip'
    elif t['imza'] < IMZA_MIN: t['red'] = 'imza az'
    else: t['red'] = 'COL'
    return t


def raf_kes(D, s, e):
    """A: kutudaki en dusuk dibin gunu d. Onceki kapanis medyani > sonraki kapanislarin %90'i ise kutu d'den baslar."""
    L, C = D['L'], D['C']
    d = s + int(np.nanargmin(L[s:e + 1]))
    if d - s >= 5 and e - d >= 5 and np.median(C[s:d]) > np.percentile(C[d:e + 1], 90):
        return d, True
    return s, False


def dene(x, e, bant_kat):
    eski = ns['BOLGE_BANT_KAT']; ns['BOLGE_BANT_KAT'] = bant_kat
    try:
        D = ns['_bolge_dizi'](x); bbw = ns['_bb_genislik'](x)
        w = ns['_bolge_kutu'](D, e)
    finally:
        ns['BOLGE_BANT_KAT'] = eski
    if not w: return dict(red='bolge yok'), None
    s, e2 = w
    s2, kesildi = raf_kes(D, s, e2)
    t = kapilar(x, D, bbw, s2, e2); t['kutu'] = f"{x.index[s2].date()}→{x.index[e2].date()}"; t['raf_kesildi'] = kesildi
    return t, (s2, e2)


v = pd.read_csv(f'{K}/kalibre_veri.csv', parse_dates=['tarih'])
et = pd.read_csv(f'{K}/kalibre_etiketler.csv', parse_dates=['bas', 'son'])
rows = []
for _, r in et.iterrows():
    df = v[v.sembol == r.sembol].set_index('tarih').sort_index()[['Open', 'High', 'Low', 'Close', 'Volume']]
    if df.empty: rows.append(dict(sembol=r.sembol, sinif=r.sinif, not_='veri yok')); continue
    idx = df.index.searchsorted(r.son)
    best = {}
    for ad, kat in (('uretim', ns['BOLGE_BANT_KAT']), ('A_raf', ns['BOLGE_BANT_KAT']), ('B_raf_bant4', 4.0)):
        b = None
        for e in range(max(0, idx - 5), min(len(df) - 1, idx + 5) + 1):
            x = df.iloc[:e + 1]
            if ad == 'uretim':
                out, t = ns['col_dip'](x, tani=True); t = dict(t); t['red'] = 'COL' if out else t.get('red'); t['kutu'] = f"{t.get('bas_tarih','-')}→{t.get('son_tarih','-')}"
            else:
                t, _ = dene(x, e, kat)
            sk = (t.get('red') == 'COL', t.get('imza', -1), -abs(e - idx))
            if b is None or sk > b[0]: b = (sk, t)
        t = b[1]
        best[f'{ad}'] = t.get('red'); best[f'{ad}_kutu'] = t.get('kutu'); best[f'{ad}_bar'] = t.get('uz'); best[f'{ad}_konum'] = t.get('konum'); best[f'{ad}_imza'] = t.get('imza_ok', '')
        if ad != 'uretim': best[f'{ad}_kesildi'] = t.get('raf_kesildi')
    rows.append(dict(sembol=r.sembol, sinif=r.sinif, cemal=f"{r.bas.date()}→{r.son.date()}", **best))
T = pd.DataFrame(rows)
pd.set_option('display.width', 300); pd.set_option('display.max_columns', 40)
print(T[['sembol', 'sinif', 'cemal', 'uretim', 'uretim_kutu', 'A_raf', 'A_raf_kutu', 'A_raf_kesildi', 'B_raf_bant4', 'B_raf_bant4_kutu', 'B_raf_bant4_bar']].to_string(index=False))
print()
for ad in ('uretim', 'A_raf', 'B_raf_bant4'):
    c = T[T.sinif == 'COL']; o = T[T.sinif == 'OLUMSUZ']
    print(f"{ad:12s}: COL yakalanan {int((c[ad]=='COL').sum())}/{len(c)} | OLUMSUZ'da yanlis alarm {int((o[ad]=='COL').sum())}/{len(o)}"
          + (f" | raf kesilen {int(T[ad+'_kesildi'].fillna(False).astype(bool).sum())}" if ad != 'uretim' else ''))
T.to_csv(sys.argv[2], index=False)
