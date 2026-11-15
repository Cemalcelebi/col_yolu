"""Yeni token +%50 / +%100 gunluk hareket olcumu.
python3 -I olc.py temel      -> S1, S2, S3 tablolari (sonuc_temel.md) + panel_ozellik.pkl
python3 -I olc.py egit       -> S4 esikleri yalniz egitim yarisindan secer, esikler.json yazar (test yarisina bakmaz)
python3 -I olc.py test       -> esikler.json'u okur, test yarisinda olcer (sonuc_s4.md)
python3 -I olc.py ritual     -> S5 (sonuc_ritual.md)
"""
import json, os, sys, logging, datetime
import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
VERI = os.path.join(KOK, 'data')
logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('olc')
SON_GUN = pd.Timestamp('2026-11-07')
BOLME = pd.Timestamp('2025-07-01')
LIKIT_ESIK = 250_000.0   # gun 1-30 medyan USDT islem hacmi
OZ = ['d', 'vr1', 'vr3', 'dd', 'ddh', 'r_prev', 'comp', 'yakin50']
OZ_AD = {'d': 'listeden beri gun', 'vr1': 'hacim orani (t-1 / onceki 7g ort.)', 'vr3': 'hacim orani (son 3g / onceki 7g)',
         'dd': 'liste zirvesinden dusus (kapanis)', 'ddh': 'liste zirvesinden dusus (fitil)', 'r_prev': 'onceki gun getirisi',
         'comp': 'aralik sikismasi (son 3g / onceki 10g)', 'yakin50': 'son 10 gunde +%50 gun (0/1)'}


def evren():
    E = pd.read_csv(os.path.join(KOK, 'evren_ham.csv'), parse_dates=['liste', 'son'])
    p = os.path.join(KOK, 'rename_dislama.json')
    if os.path.exists(p):
        dis = json.load(open(p))
        E = E[~E.base.isin(dis)]
    return E


def panel():
    p = os.path.join(KOK, 'panel_ozellik.pkl')
    if os.path.exists(p):
        return pd.read_pickle(p)
    E = evren()
    S = pd.read_pickle(os.path.join(KOK, 'seriler.pkl'))
    par = []
    for e in E.itertuples():
        d = S[e.base]
        d = d[d.index >= e.liste]
        idx = pd.date_range(e.liste, d.index[-1], freq='D')
        d = d.reindex(idx)
        d['base'] = e.base
        d['d'] = np.arange(len(d))
        d['r'] = d.c / d.c.shift(1) - 1
        rng = (d.h - d.l) / d.c
        q = d.qv
        d['vr1'] = q.shift(1) / q.shift(2).rolling(7, min_periods=3).mean()
        d['vr3'] = q.shift(1).rolling(3, min_periods=2).mean() / q.shift(4).rolling(7, min_periods=3).mean()
        d['dd'] = d.c.shift(1) / d.c.cummax().shift(1) - 1
        d['ddh'] = d.c.shift(1) / d.h.cummax().shift(1) - 1
        d['r_prev'] = d.r.shift(1)
        d['comp'] = rng.shift(1).rolling(3, min_periods=2).mean() / rng.shift(4).rolling(10, min_periods=5).mean()
        d['yakin50'] = (d.r.shift(1).rolling(10, min_periods=1).max() >= 0.5).astype(float)
        d['liste'] = e.liste
        d['borsa'] = e.borsa
        d['binance'] = e.binance
        d['likit'] = q.iloc[1:31].median() >= LIKIT_ESIK
        par.append(d)
    P = pd.concat(par).rename_axis('t').reset_index()
    P.to_pickle(p)
    return P


def ozet(x, ad=''):
    x = pd.Series(x).dropna()
    if not len(x):
        return dict(grup=ad, n=0)
    w = x.clip(x.quantile(0.01), x.quantile(0.99))
    return dict(grup=ad, n=len(x), medyan=x.median(), ortalama=x.mean(), ort_w1_99=w.mean(), pozitif=(x > 0).mean(),
                alt_50=(x < -0.5).mean(), ust_100=(x > 1).mean(), p10=x.quantile(0.1), p90=x.quantile(0.9))


def tablo(rows, yuzde=('medyan', 'ortalama', 'ort_w1_99', 'pozitif', 'alt_50', 'ust_100', 'p10', 'p90')):
    T = pd.DataFrame(rows)
    for c in T.columns:
        if c in yuzde:
            T[c] = T[c].map(lambda v: '' if pd.isna(v) else '%+.1f%%' % (100 * v) if c not in ('pozitif', 'alt_50', 'ust_100') else '%.1f%%' % (100 * v))
    return T.to_markdown(index=False)


def temel():
    P = panel()
    E = evren()
    out = []
    out.append('# Temel sonuclar (uretim %s)\n' % datetime.datetime.utcnow().isoformat())
    out.append('Evren: %d token; borsa dagilimi (ana seri): %s; Binance listeli: %d; likit (gun1-30 medyan hacim >= %.0f USDT): %d\n'
               % (len(E), E.borsa.value_counts().to_dict(), E.binance.sum(), LIKIT_ESIK, P.groupby('base').likit.first().sum()))
    out.append('Liste yili: %s\n' % E.liste.dt.year.value_counts().sort_index().to_dict())
    # ---- S1
    c0 = P[P.d == 0].set_index('base').c
    son = P.groupby('base').t.max()
    gruplar = {'hepsi': P.base.unique(), 'binance_listeli': P[P.binance].base.unique(), 'yalniz_okx_gate': P[~P.binance].base.unique(),
               'likit': P[P.likit].base.unique(), 'liste<2025-07': P[P.liste < BOLME].base.unique(), 'liste>=2025-07': P[P.liste >= BOLME].base.unique()}
    rows, rows_delist = [], []
    W = P.set_index(['base', 'd']).c
    for h in (7, 30, 90, 180):
        for gad, bs in gruplar.items():
            vals, delist, kisa = [], 0, 0
            for b in bs:
                lst = P.loc[P.base == b, 'liste'].iloc[0] if False else None
                ch = None
                for k in range(0, 4):
                    v = W.get((b, h - k))
                    if v is not None and not np.isnan(v):
                        ch = v; break
                if ch is not None:
                    vals.append(ch / c0[b] - 1)
            r = ozet(vals, gad); r['ufuk'] = h
            rows.append(r)
    out.append('\n## S1 Liste gunu kapanisindan gun h kapanisina getiri\n')
    T = pd.DataFrame(rows)
    out.append(tablo([{k: v for k, v in r.items()} for r in rows]))
    # delist/veri bitis sayimi
    Ed = E.set_index('base')
    erken_bitis = Ed[Ed.son < SON_GUN - pd.Timedelta(days=3)]
    out.append('\n\nSeri 7 Kasim 2026dan once biten (delist/veri yok) token: %d. Bunlarin ufuk eksikleri: %s\n' % (
        len(erken_bitis), {h: int(((erken_bitis.son - erken_bitis.liste).dt.days < h).sum()) for h in (7, 30, 90, 180)}))
    # delist edilenleri son fiyatla dahil eden varyant
    rows2 = []
    for h in (30, 90, 180):
        vals = []
        for b in gruplar['hepsi']:
            s = P[(P.base == b) & (P.d <= h)].c.dropna()
            if (Ed.loc[b, 'liste'] + pd.Timedelta(days=h)) > SON_GUN:
                continue
            vals.append(s.iloc[-1] / c0[b] - 1)
        r = ozet(vals, 'hepsi+delist son fiyat'); r['ufuk'] = h; rows2.append(r)
    out.append('\nVaryant (ufku 7 Kasim 2026 icinde kalan tum tokenlar; delist olanlar son kapanisla):\n\n' + tablo(rows2))
    # ---- S2
    out.append('\n\n## S2 +%50 / +%100 kapanis-kapanis gunleri\n')
    G = P[P.d >= 1]
    rows = []
    for gad, bs in gruplar.items():
        g = G[G.base.isin(bs)]
        n = len(bs)
        r = dict(grup=gad, token=n)
        for e, ad in ((0.5, '50'), (1.0, '100')):
            ilk90 = g[(g.d <= 90) & (g.r >= e)].base.nunique()
            tum = g[g.r >= e].base.nunique()
            r['ilk90_%s' % ad] = '%d (%.1f%%)' % (ilk90, 100 * ilk90 / n)
            r['tum_%s' % ad] = '%d (%.1f%%)' % (tum, 100 * tum / n)
            r['olay_%s' % ad] = int((g.r >= e).sum())
        r['token_gun'] = int(g.r.notna().sum())
        rows.append(r)
    out.append(pd.DataFrame(rows).to_markdown(index=False))
    # gun dagilimi
    for e, ad in ((0.5, '+%50'), (1.0, '+%100')):
        ev = G[G.r >= e]
        ilk = ev.groupby('base').d.min()
        out.append('\n\n%s: tum olaylarin listeden gun sayisi medyani %d (ceyrekler %d-%d), ilk olayin medyani %d (ceyrekler %d-%d); olay n=%d, token n=%d\n'
                   % (ad, ev.d.median(), ev.d.quantile(.25), ev.d.quantile(.75), ilk.median(), ilk.quantile(.25), ilk.quantile(.75), len(ev), len(ilk)))
    kova = [0, 1, 3, 7, 14, 30, 90, 180, 365, 2000]
    G2 = G[G.r.notna()].copy()
    G2['kova'] = pd.cut(G2.d, kova, labels=['1', '2-3', '4-7', '8-14', '15-30', '31-90', '91-180', '181-365', '366+'])
    H = G2.groupby('kova', observed=True).agg(token_gun=('r', 'size'), olay50=('r', lambda x: (x >= .5).sum()), olay100=('r', lambda x: (x >= 1).sum()))
    H['olay50_1000gun'] = (1000 * H.olay50 / H.token_gun).round(2)
    H['olay100_1000gun'] = (1000 * H.olay100 / H.token_gun).round(2)
    H['olay50_payi'] = (100 * H.olay50 / H.olay50.sum()).round(1)
    H['olay100_payi'] = (100 * H.olay100 / H.olay100.sum()).round(1)
    out.append('\nListeden gun kovasina gore olay sikligi (1000 token-gunde olay) ve olaylarin payi (%):\n\n' + H.reset_index().to_markdown(index=False))
    # likit alt grup ayni tablo
    H2 = G2[G2.likit].groupby('kova', observed=True).agg(token_gun=('r', 'size'), olay50=('r', lambda x: (x >= .5).sum()), olay100=('r', lambda x: (x >= 1).sum()))
    H2['olay50_1000gun'] = (1000 * H2.olay50 / H2.token_gun).round(2)
    H2['olay100_1000gun'] = (1000 * H2.olay100 / H2.token_gun).round(2)
    out.append('\n\nAyni tablo, yalniz likit tokenlar:\n\n' + H2.reset_index().to_markdown(index=False))
    # ---- S3
    out.append('\n\n## S3 Olay calismasi\n')
    idx = P.set_index(['base', 'd'])
    O, C = idx.o, idx.c
    for e, ad in ((1.0, '+%100'), (0.5, '+%50')):
        ev = G[G.r >= e][['base', 'd', 'likit', 'binance']]
        if e == 0.5:
            ev = ev[G.loc[ev.index, 'r'] < 1.0]   # +%50 ile +%100 arasi (ayri kume)
        for giris in ('ertesi_acilis', 'olay_kapanis'):
            rows = []
            for alt, evs in (('tum olaylar', ev), ('tokenin ilk olayi', ev.sort_values('d').drop_duplicates('base')), ('likit tokenlar', ev[ev.likit])):
                for k in (1, 3, 7, 30):
                    vals = []
                    for b, dd in zip(evs.base, evs.d):
                        g0 = O.get((b, dd + 1)) if giris == 'ertesi_acilis' else C.get((b, dd))
                        g1 = C.get((b, dd + k))
                        if g0 is not None and g1 is not None and not np.isnan(g0) and not np.isnan(g1) and g0 > 0:
                            vals.append(g1 / g0 - 1)
                    r = ozet(vals, alt); r['k'] = k
                    rows.append(r)
            out.append('\n### %s gunleri%s, giris=%s, cikis=gun t+k kapanisi\n\n' % (ad, ' (+%50 <= r < +%100)' if e == .5 else '', giris) + tablo(rows))
    open(os.path.join(KOK, 'sonuc_temel.md'), 'w').write('\n'.join(out))
    log.info('\n'.join(out))


def pop(P):
    Q = P[(P.d >= 2) & P.r.notna()].copy()
    Q['s100'] = Q.r >= 1.0
    Q['s50'] = Q.r >= 0.5
    return Q


def kural_maske(Q, kural):
    m = pd.Series(True, index=Q.index)
    for oz, yon, esik in kural:
        m &= (Q[oz] >= esik) if yon == '>=' else (Q[oz] <= esik)
    return m.fillna(False)


def degerle(Q, kural, hedef):
    m = kural_maske(Q, kural)
    taban = Q[hedef].mean()
    p = Q.loc[m, hedef].mean() if m.sum() else np.nan
    return dict(destek=m.mean(), gun=int(m.sum()), olay=int(Q.loc[m, hedef].sum()), taban=taban, p_sinyal=p,
                lift=p / taban if taban else np.nan, yakalama=Q.loc[m, hedef].sum() / max(Q[hedef].sum(), 1))


def egit():
    P = panel()
    Q = pop(P[P.liste < BOLME])
    log.info('egitim token %d token-gun %d s100 %d s50 %d', Q.base.nunique(), len(Q), Q.s100.sum(), Q.s50.sum())
    sonuc = {'yazildi_utc': datetime.datetime.utcnow().isoformat(), 'egitim': 'liste < 2025-07-01',
             'kural': 'her ozellik icin egitim yuzdelik (5..95) esikleri, iki yon; destek >= %5 ve sinyalde >= 20 olay; en yuksek lift. '
                      'Kombinasyon: secilen tekli kurallarin ikili VE birlesimi, destek >= %2, en yuksek lift. '
                      'Ikinci set: yalniz d >= 8 gunleri (listeden ilk haftayi disarida birakir).',
             'hedefler': {}}
    for hedef in ('s100', 's50'):
        for ad, QQ in (('tum', Q), ('d>=8', Q[Q.d >= 8])):
            tekli = []
            for oz in OZ:
                if ad == 'd>=8' and oz == 'd':
                    continue
                x = QQ[oz].dropna()
                adaylar = sorted(set(x.quantile(np.arange(0.05, 0.96, 0.05)).round(6))) if oz != 'yakin50' else [1.0]
                best = None
                for esik in adaylar:
                    for yon in (('>=',) if oz == 'yakin50' else ('>=', '<=')):
                        r = degerle(QQ, [(oz, yon, float(esik))], hedef)
                        if r['destek'] >= 0.05 and r['olay'] >= 20 and (best is None or r['lift'] > best[1]['lift']):
                            best = ([(oz, yon, float(esik))], r)
                if best:
                    tekli.append(best)
            tekli.sort(key=lambda b: -b[1]['lift'])
            kombi = None
            for i in range(len(tekli)):
                for j in range(i + 1, len(tekli)):
                    k = tekli[i][0] + tekli[j][0]
                    r = degerle(QQ, k, hedef)
                    if r['destek'] >= 0.02 and r['olay'] >= 20 and (kombi is None or r['lift'] > kombi[1]['lift']):
                        kombi = (k, r)
            sonuc['hedefler']['%s|%s' % (hedef, ad)] = {'tekli': [{'kural': b[0], 'egitim': b[1]} for b in tekli],
                                                        'kombi': {'kural': kombi[0], 'egitim': kombi[1]} if kombi else None}
    json.dump(sonuc, open(os.path.join(KOK, 'esikler.json'), 'w'), indent=1, default=float)
    log.info(json.dumps(sonuc, indent=1, default=float)[:6000])


def test():
    S = json.load(open(os.path.join(KOK, 'esikler.json')))
    P = panel()
    Qe = pop(P[P.liste < BOLME])
    Qt = pop(P[P.liste >= BOLME])
    out = ['# S4 sonuclari (esikler %s tarihinde egitimden yazildi; test %s)\n' % (S['yazildi_utc'], datetime.datetime.utcnow().isoformat()),
           'Egitim: %d token, %d token-gun, +%%100 gun %d, +%%50 gun %d. Test (liste >= 2025-07-01): %d token, %d token-gun, +%%100 gun %d, +%%50 gun %d.\n'
           % (Qe.base.nunique(), len(Qe), Qe.s100.sum(), Qe.s50.sum(), Qt.base.nunique(), len(Qt), Qt.s100.sum(), Qt.s50.sum()),
           'Secim kurali: ' + S['kural'] + '\n']
    for anah, v in S['hedefler'].items():
        hedef, ad = anah.split('|')
        QQt = Qt if ad == 'tum' else Qt[Qt.d >= 8]
        rows = []
        for t in v['tekli'] + ([v['kombi']] if v['kombi'] else []):
            rt = degerle(QQt, t['kural'], hedef)
            re_ = t['egitim']
            rows.append({'kural': ' VE '.join('%s %s %.4g' % (OZ_AD[o], y, e) for o, y, e in t['kural']),
                         'egit_destek': '%.1f%%' % (100 * re_['destek']), 'egit_P': '%.2f%%' % (100 * re_['p_sinyal']), 'egit_lift': '%.2f' % re_['lift'],
                         'test_destek': '%.1f%%' % (100 * rt['destek']), 'test_olay': rt['olay'], 'test_P': '%.2f%%' % (100 * rt['p_sinyal']) if rt['gun'] else '',
                         'test_taban': '%.2f%%' % (100 * rt['taban']), 'test_lift': '%.2f' % rt['lift'], 'test_yakalama': '%.0f%%' % (100 * rt['yakalama'])})
        out.append('\n### hedef %s, populasyon %s (test taban %.2f%%, egitim taban %.2f%%)\n\n' % (
            '+%100' if hedef == 's100' else '+%50', ad, 100 * QQt[hedef].mean(), 100 * (Qe if ad == 'tum' else Qe[Qe.d >= 8])[hedef].mean())
            + pd.DataFrame(rows).to_markdown(index=False))
    # tanimlayici: olay gunleri vs ayni tokenlarin rastgele olay-disi gunleri
    Q = pop(P)
    rng = np.random.default_rng(7)
    sp_tok = Q[Q.s50].base.unique()
    non = Q[Q.base.isin(sp_tok) & ~Q.s50]
    orn = non.iloc[rng.choice(len(non), size=min(len(non), 20 * int(Q.s100.sum())), replace=False)]
    rows = []
    for oz in OZ:
        rows.append({'ozellik': OZ_AD[oz], '+%100 gunu medyan': Q.loc[Q.s100, oz].median(), '+%50 gunu medyan': Q.loc[Q.s50, oz].median(),
                     'rastgele olay-disi gun medyan': orn[oz].median(), '+%100 p25-p75': '%.3g / %.3g' % tuple(Q.loc[Q.s100, oz].quantile([.25, .75])),
                     'olay-disi p25-p75': '%.3g / %.3g' % tuple(orn[oz].quantile([.25, .75]))})
    out.append('\n\n### Olay gunleri vs ayni tokenlarin rastgele olay-disi gunleri (tum ornek; olay-disi orneklem n=%d, olay tokeni n=%d, +%%100 n=%d, +%%50 n=%d)\n\n'
               % (len(orn), len(sp_tok), Q.s100.sum(), Q.s50.sum()) + pd.DataFrame(rows).to_markdown(index=False, floatfmt='.3g'))
    open(os.path.join(KOK, 'sonuc_s4.md'), 'w').write('\n'.join(out))
    log.info('\n'.join(out))


def ritual():
    g = json.load(open(os.path.join(VERI, 'ritual', 'gate_1d.json')))
    d = pd.DataFrame({'t': pd.to_datetime([int(x[0]) for x in g], unit='s'), 'o': [float(x[5]) for x in g], 'h': [float(x[3]) for x in g],
                      'l': [float(x[4]) for x in g], 'c': [float(x[2]) for x in g], 'qv': [float(x[1]) for x in g], 'kapali': [x[7] for x in g]}).set_index('t')
    m = json.load(open(os.path.join(VERI, 'ritual', 'mexc_1d.json')))
    dm = pd.DataFrame({'t': pd.to_datetime([x[0] for x in m], unit='ms'), 'o': [float(x[1]) for x in m], 'h': [float(x[2]) for x in m],
                       'l': [float(x[3]) for x in m], 'c': [float(x[4]) for x in m], 'qv': [float(x[7]) for x in m]}).set_index('t')
    h1 = json.load(open(os.path.join(VERI, 'ritual', 'gate_1h.json')))
    dh = pd.DataFrame({'t': pd.to_datetime([int(x[0]) for x in h1], unit='s'), 'c': [float(x[2]) for x in h1], 'h': [float(x[3]) for x in h1],
                       'qv': [float(x[1]) for x in h1]}).set_index('t').sort_index()
    out = ['# RITUAL/USDT (S5)\n', 'Gate gunluk:\n\n' + d.to_markdown(floatfmt='.6g'), '\nMEXC gunluk:\n\n' + dm.to_markdown(floatfmt='.6g')]
    dh['r24'] = dh.c / dh.c.shift(24) - 1
    out.append('\nGate saatlik, son 30 saat (r24 = 24 saatlik kapanis degisimi):\n\n' + dh.tail(30).to_markdown(floatfmt='.5g'))
    # ozellikler: spike gunu t = son (Gate 8 Kasim, kismi) ; bilgiler t-1'e kadar
    rng = (d.h - d.l) / d.c
    t = d.index[-1]
    i = len(d) - 1
    q = d.qv
    f = {'d (Gate ilk mumundan)': i, 'd (MEXC ilk mumundan)': (t - dm.index[0]).days,
         'vr1': q.iloc[i - 1] / q.iloc[max(0, i - 8):i - 1].mean(),
         'vr3': q.iloc[i - 3:i].mean() / q.iloc[max(0, i - 10):i - 3].mean(),
         'dd (kapanis)': d.c.iloc[i - 1] / d.c.iloc[:i].max() - 1, 'ddh (Gate fitil)': d.c.iloc[i - 1] / d.h.iloc[:i].max() - 1,
         'ddh (MEXC fitil, 0.25 acilis igne dahil)': dm.c.iloc[-2] / dm.h.iloc[:-1].max() - 1,
         'r_prev': d.c.iloc[i - 1] / d.c.iloc[i - 2] - 1,
         'comp': rng.iloc[i - 3:i].mean() / rng.iloc[max(0, i - 13):i - 3].mean(),
         'yakin50': float((d.c / d.c.shift(1) - 1).iloc[max(0, i - 10):i].max() >= 0.5),
         'olay gunu r (Gate 8 Kasim kismi)': d.c.iloc[i] / d.c.iloc[i - 1] - 1,
         'olay gunu r (Gate 7 Kasim tam gun)': d.c.iloc[i - 1] / d.c.iloc[i - 2] - 1,
         'max 24s r (Gate saatlik)': dh.r24.max()}
    P = panel()
    Q = pop(P)
    rows = []
    kars = {'vr1': 'vr1', 'vr3': 'vr3', 'dd (kapanis)': 'dd', 'ddh (Gate fitil)': 'ddh', 'r_prev': 'r_prev', 'comp': 'comp', 'd (Gate ilk mumundan)': 'd'}
    for k, v in f.items():
        r = {'olcu': k, 'RITUAL': round(v, 4)}
        if k in kars:
            oz = kars[k]
            r['+%100 gunlerinde yuzdelik'] = '%.0f' % (100 * (Q.loc[Q.s100, oz].dropna() <= v).mean())
            r['tum token-gunlerde yuzdelik'] = '%.0f' % (100 * (Q[oz].dropna() <= v).mean())
        rows.append(r)
    out.append('\n\nOzellikler (t = 8 Kasim 2026 UTC, kismi gun; bilgiler 7 Kasim kapanisina kadar):\n\n' + pd.DataFrame(rows).to_markdown(index=False))
    # getiri buyuklugu: d<=30 gunluk getiriler icinde
    G = P[(P.d >= 1) & (P.d <= 30) & P.r.notna()]
    for v in (0.9988, f['olay gunu r (Gate 8 Kasim kismi)']):
        out.append('\nGunluk getiri %+.1f%%: ilk 30 gundeki tum token-gunlerin %%%.2f\'si bundan buyuk (n=%d); +%%50 olaylari icinde yuzdelik %.0f'
                   % (100 * v, 100 * (G.r > v).mean(), len(G), 100 * (G.loc[G.r >= .5, 'r'] <= v).mean()))
    open(os.path.join(KOK, 'sonuc_ritual.md'), 'w').write('\n'.join(out))
    log.info('\n'.join(out))


def ek():
    """Ek tablolar: taban ileri getiri, olay gunu hacim filtresi, erken/gec olaylar, sinyal gunu alim getirisi (test yarisi)."""
    P = panel()
    P = P.sort_values(['base', 't'])
    g = P.groupby('base')
    for k in (1, 3, 7, 30):
        P['f%d' % k] = g.c.shift(-k) / P.c - 1          # olay/gun kapanisindan t+k kapanisina
        P['a%d' % k] = g.c.shift(-(k - 1)) / P.o - 1     # gun t acilisindan t+k-1 kapanisina (sinyal t-1 kapanisinda bilinir)
    out = ['# Ek tablolar\n']
    rows = []
    for ad, m in (('tum token-gunleri (d>=1)', P.d >= 1), ('d 1-90', (P.d >= 1) & (P.d <= 90)), ('+%100 gunleri', P.r >= 1),
                  ('+%100, olay gunu hacmi >= 1M USDT', (P.r >= 1) & (P.qv >= 1e6)), ('+%100, olay gunu hacmi < 1M USDT', (P.r >= 1) & (P.qv < 1e6)),
                  ('+%100, d <= 30', (P.r >= 1) & (P.d <= 30)), ('+%100, d > 30', (P.r >= 1) & (P.d > 30)),
                  ('+%100, Binance listeli token', (P.r >= 1) & P.binance), ('+%50-100, olay gunu hacmi >= 1M', (P.r >= .5) & (P.r < 1) & (P.qv >= 1e6))):
        for k in (1, 7, 30):
            r = ozet(P.loc[m, 'f%d' % k], ad); r['k'] = k; rows.append(r)
    out.append('## Kapanistan t+k kapanisina getiri: taban vs olay alt gruplari\n\n' + tablo(rows))
    # round-trip
    ev = P[P.r >= 1]
    out.append('\n\n+%%100 gunlerinin ertesi gun kapanis-kapanis getirisi <= -%%33 olanlar: %.1f%%, <= -%%50: %.1f%% (n=%d). '
               'Olay gunu kapanisinin gun ici zirveye orani medyani %.2f (1 = zirvede kapanis).' % (
                   100 * (ev.f1 <= -1 / 3).mean(), 100 * (ev.f1 <= -.5).mean(), len(ev), (ev.c / ev.h).median()))
    out.append('\nOlay gunu USDT islem hacmi ceyrekleri (+%%100): %s' % ev.qv.quantile([.1, .25, .5, .75, .9]).round(-3).to_dict())
    # sinyal gunu alim (test yarisi, on kayitli esikler)
    S = json.load(open(os.path.join(KOK, 'esikler.json')))
    T = P[(P.liste >= BOLME) & (P.d >= 2) & P.r.notna()]
    rows = []
    v = S['hedefler']['s100|tum']
    for t in v['tekli'][:4] + [v['kombi']]:
        m = kural_maske(T, t['kural'])
        for k in (1, 7):
            r = ozet(T.loc[m, 'a%d' % k], ' VE '.join('%s %s %.3g' % (o, y, e) for o, y, e in t['kural'])); r['k'] = k; rows.append(r)
    for k in (1, 7):
        r = ozet(T['a%d' % k], 'TUM test token-gunleri (taban)'); r['k'] = k; rows.append(r)
    out.append('\n\n## Test yarisi: sinyal gunu acilisinda al, gun t+k-1 kapanisinda sat (k=1 ayni gun)\n\n' + tablo(rows))
    open(os.path.join(KOK, 'sonuc_ek.md'), 'w').write('\n'.join(out))
    log.info('\n'.join(out))


if __name__ == '__main__':
    {'temel': temel, 'egit': egit, 'test': test, 'ritual': ritual, 'ek': ek}[sys.argv[1]]()
