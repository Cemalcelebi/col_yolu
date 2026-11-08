"""Yeni token paneli: ham borsa mumlarindan token-gun paneli kurar.
python3 -I panel.py capraz   -> capraz_hedef.json (eski listelemelerin fiyat kontrolu icin indirilecek ciftler)
python3 -I panel.py kur      -> panel.pkl + evren.csv + dislanan.csv + rename_aday.csv
"""
import json, os, sys, re, glob, logging
import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
VERI = os.path.join(KOK, 'data')
logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('panel')
BASLA = pd.Timestamp('2023-06-01')
PENCERE = (pd.Timestamp('2024-01-01'), pd.Timestamp('2026-09-30'))
SON_GUN = pd.Timestamp('2026-11-07')
ONCELIK = {'binance': 0, 'okx': 1, 'gate': 2}

STABIL = set('''USDC FDUSD TUSD USDP DAI USDE USDS PYUSD USD1 RLUSD EURI EUR AEUR BFUSD XUSD USDD FRAX GHO USDG USDX USD0
LUSD CRVUSD SUSD USDY USDT0 EURC EURT XAUT PAXG BUSD USTC UST USDQ USDB USDJ SUSDE SUSDS FDUSD USDF USDA USDTB
DUSD AUSD EUSD ZUSD USDN USDK HUSD GUSD TRYB BIDR IDRT BRZ CNHT XSGD EURS USDR USR DEUSD SRUSD FXUSD CUSD MUSD
USDO USDH FRXUSD LISUSD BNSOL WBETH WBTC WETH STETH WSTETH CBBTC CBETH BETH RETH METH CMETH EZETH WEETH RSETH
JITOSOL JUPSOL MSOL BBSOL STSOL BTCB SOLVBTC LBTC FBTC TBTC UNIBTC PUMPBTC ENZOBTC XSOLVBTC SOLVBTCBBN BFBTC
STBTC WBNB WSOL WTRX WAVAX WMATIC WPOL WFTM WHYPE KHYPE STHYPE WSTUSR BNBXBT'''.split())
GATE_ADI = re.compile(r'xLong|xShort|xStock|Tokenized|\bStock\b|Wrapped|Bridged|Staked|Liquid Staking|'
                      r'\bGold\b|Dollar|\bEuro\b|\bETF\b|Treasury|Yield', re.I)
KALDIRAC = re.compile(r'(\d+[LS]|UP|DOWN|BULL|BEAR)$')


def gun(ms):
    return pd.to_datetime(np.asarray(ms, dtype='int64'), unit='ms').normalize()


def oku(borsa, cift):
    p = os.path.join(VERI, borsa, cift + '.json')
    if not os.path.exists(p):
        return None
    r = json.load(open(p))
    if not r:
        return pd.DataFrame(columns=['o', 'h', 'l', 'c', 'qv'])
    if borsa == 'binance':
        d = pd.DataFrame({'t': gun([x[0] for x in r]), 'o': [float(x[1]) for x in r], 'h': [float(x[2]) for x in r],
                          'l': [float(x[3]) for x in r], 'c': [float(x[4]) for x in r], 'qv': [float(x[7]) for x in r]})
    elif borsa == 'okx':
        d = pd.DataFrame({'t': gun([int(x[0]) for x in r]), 'o': [float(x[1]) for x in r], 'h': [float(x[2]) for x in r],
                          'l': [float(x[3]) for x in r], 'c': [float(x[4]) for x in r], 'qv': [float(x[7]) for x in r],
                          'ok': [x[8] for x in r]})
        d = d[d.ok == '1'].drop(columns='ok')
    else:  # gate: [t, quoteVol, c, h, l, o, baseVol, closed]
        d = pd.DataFrame({'t': gun([int(x[0]) * 1000 for x in r]), 'o': [float(x[5]) for x in r], 'h': [float(x[3]) for x in r],
                          'l': [float(x[4]) for x in r], 'c': [float(x[2]) for x in r], 'qv': [float(x[1]) for x in r],
                          'ok': [x[7] if len(x) > 7 else 'true' for x in r]})
        d = d[d.ok == 'true'].drop(columns='ok')
    d = d[(d.c > 0) & (d.t <= SON_GUN)].drop_duplicates('t').sort_values('t').set_index('t')
    return d


def listelemeler():
    """Her borsa ciftinin (base, ilk_gun, son_gun, seri_var) kaydi."""
    kay = []
    bi = json.load(open(os.path.join(VERI, 'binance_ilk_son.json')))
    for s, v in bi.items():
        if not (isinstance(v['ilk'], list) and v['ilk']):
            continue
        kay.append(dict(borsa='binance', cift=s, base=v['base'].upper(), ilk=gun([v['ilk'][0][0]])[0],
                        son=gun([v['son'][0][0]])[0] if v['son'] else pd.NaT, durum=v['status'], ad=''))
    for x in json.load(open(os.path.join(VERI, 'okx_instruments.json')))['data']:
        if x['quoteCcy'] != 'USDT':
            continue
        kay.append(dict(borsa='okx', cift=x['instId'], base=x['baseCcy'].upper(), ilk=gun([int(x['listTime'] or 0)])[0],
                        son=pd.NaT, durum=x['state'], ad=''))
    for x in json.load(open(os.path.join(VERI, 'gate_pairs.json'))):
        if x['quote'] != 'USDT':
            continue
        kay.append(dict(borsa='gate', cift=x['id'], base=x['base'].upper(), ilk=gun([int(x['buy_start'] or 0) * 1000])[0],
                        son=pd.NaT, durum=x['trade_status'], ad=x.get('base_name') or ''))
    return pd.DataFrame(kay)


def capraz():
    L = listelemeler()
    # okx/gate icin listTime/buy_start yaklasik; aday: herhangi bir borsada ilk >= 2023-12-01
    aday_base = set(L[L.ilk >= pd.Timestamp('2023-12-01')].base)
    hedef = []
    for _, r in L[L.base.isin(aday_base)].iterrows():
        if not os.path.exists(os.path.join(VERI, r.borsa, r.cift + '.json')):
            hedef.append([r.borsa, r.cift])
    json.dump(hedef, open(os.path.join(KOK, 'capraz_hedef.json'), 'w'))
    log.info('aday base %d, capraz indirilecek %d', len(aday_base), len(hedef))


def tutarli(a, b):
    """Iki serinin ortak gunlerde kapanis orani medyani ~1 mi."""
    o = a.c.reindex(b.index).dropna()
    if len(o) < 3:
        return None
    oran = (o / b.c.reindex(o.index)).median()
    return 0.67 <= oran <= 1.5


HISSE_ADI = re.compile(r'\bInc\b|Inc\.|Corporation|Incorporated|Holdings|\bplc\b|Technologies|Shares|Electronics|Markets|\bGlobal\b|'
                       r'NVIDIA|Tesla|^Meta$|^Intel$|Broadcom|^Circle$|Qualcomm|SpaceX|OpenAI|Anthropic|Palantir|Samsung|Coinbase|'
                       r'Micron|Marvell|Xiaomi|Zhipu|Unitree|Advanced Micro|Apple|Microsoft|Alphabet|Netflix|Robinhood|Quantinuum|ProShares')
ELLE_RENAME = {'AWE': 'STPT -> AWE Network ticker degisimi (2025)', 'SKY': 'MKR -> SKY goc (Sky Protocol)',
               'D': 'DAR -> D (DAR Open Network) ticker degisimi (Binance DARUSDT 2025-01-06 kapandi, D 2025-01-09 acildi)',
               'PDA': 'PLA -> PDA (PlayDapp) goc', 'TON': 'Toncoin 2021den beri islem goruyor; OKX/Gate listesinde TON adiyla yok, Binance cifti 2024'}


def ek_dislama(E, D, L):
    """Tokenlasmis hisse / pre-IPO tokenlari, onekli (1000X, 1MX) kopyalar ve bilinen ticker degisimleri."""
    gate_ad = L[L.borsa == 'gate'].set_index('base').ad.to_dict()
    hisse = {b for b, a in gate_ad.items() if isinstance(a, str) and HISSE_ADI.search(a)}
    alt = set()
    for b in hisse:
        alt.add(b)
        if b[-1:] in ('G', 'X', 'B'):
            alt.add(b[:-1])
        if b.endswith('ON'):
            alt.add(b[:-2])
    for b, a in gate_ad.items():   # xStock / Ondo adlari zaten dislandi; alttakileri de ekle
        if isinstance(a, str) and re.search(r'xStock|Ondo Tokenized', a):
            alt.add(b[:-1] if b.endswith('X') else b[:-2] if b.endswith('ON') else b)
    ilk = L.groupby('base').ilk_gercek.min().to_dict()
    yeni_dis, tut = [], []
    for e in E.itertuples():
        b = e.base
        neden = None
        if b in hisse or (b[-1:] in ('B', 'G', 'X') and b[:-1] in alt) or (b[:1] == 'X' and b[1:] in alt):
            neden = 'tokenlasmis hisse/pre-IPO'
        # 2026 tokenlasmis hisse dalgasi: Binance '...B', OKX 'X...', Gate '...G' (elle gozden gecirildi: hepsi hisse/ETF)
        elif e.liste >= pd.Timestamp('2026-05-01') and ((e.borsa == 'binance' and b.endswith('B')) or
                                                       (e.borsa == 'okx' and b.startswith('X')) or (e.borsa == 'gate' and b.endswith('G'))):
            neden = 'tokenlasmis hisse (2026 sonek kurali)'
        elif isinstance(e.ad, str) and re.search(r'^\s*Ondo (?!Finance)', e.ad):
            neden = 'Ondo tokenlasmis sepet'
        m = re.match(r'^(1000000|10000|1000|100|1M)(.+)$', b)
        if neden is None and m and m.group(2) in ilk and ilk[m.group(2)] < e.liste:
            neden = 'onekli kopya (%s, ilk %s)' % (m.group(2), ilk[m.group(2)].date())
        mk = re.match(r'^(.+?)[35][LS]$', b)
        if neden is None and mk and mk.group(1) in ilk:
            neden = 'kaldiracli token (%s)' % mk.group(1)
        if neden is None and b in ELLE_RENAME:
            neden = 'ticker degisimi: ' + ELLE_RENAME[b]
        if neden:
            yeni_dis.append(dict(base=b, neden=neden))
        else:
            tut.append(e.Index)
    log.info('ek dislama %d: %s', len(yeni_dis), [x['base'] for x in yeni_dis])
    return E.loc[tut].reset_index(drop=True), pd.concat([D, pd.DataFrame(yeni_dis)], ignore_index=True)


def kur():
    L = listelemeler()
    seri = {}
    for _, r in L.iterrows():
        d = oku(r.borsa, r.cift)
        if d is not None:
            if (r.borsa == 'gate' and r.ilk > pd.Timestamp('2000-01-01') and len(d)
                    and (r.ilk - d.index[0]).days <= 120):
                # buy_start'tan en fazla 120 gun once baslayan mumlar Gate on-piyasa (pre-market): at.
                # Daha eski mumlar = buy_start sifirlanmis eski cift (yeniden listeleme); token eski sayilir.
                d = d[d.index >= r.ilk]
            elif r.borsa == 'gate' and r.ilk > pd.Timestamp('2000-01-01') and len(d) and r.ilk > d.index[0]:
                # uzun on-piyasa: buy_start +-3 gununde >=5x kirilma varsa onceki mumlar on-piyasa olcegi
                rr = np.log(d.c).diff()
                yak = rr[(rr.index >= r.ilk - pd.Timedelta(days=3)) & (rr.index <= r.ilk + pd.Timedelta(days=3))]
                if len(yak) and yak.abs().max() > np.log(5):
                    d = d[d.index >= r.ilk]
            seri[(r.borsa, r.cift)] = d
    # gercek ilk gun: binance icin ilk mum; okx/gate icin seri BASLA'dan sonra basliyorsa ilk mum, yoksa liste zamani
    def ilk_gun(r):
        d = seri.get((r.borsa, r.cift))
        if r.borsa == 'binance':
            return r.ilk
        if d is not None and len(d):
            return d.index[0] if d.index[0] > BASLA + pd.Timedelta(days=2) else min(r.ilk, d.index[0])
        return r.ilk
    L['ilk_gercek'] = L.apply(ilk_gun, axis=1)
    L['seri_n'] = [len(seri[(b, c)]) if (b, c) in seri else -1 for b, c in zip(L.borsa, L.cift)]
    L.to_csv(os.path.join(KOK, 'listelemeler.csv'), index=False)

    evren, dis = [], []
    for base, g in L.groupby('base'):
        g = g.sort_values(['ilk_gercek', 'borsa'], key=lambda s: s.map(ONCELIK) if s.name == 'borsa' else s)
        # pencere ici listelemesi olmayan base'ler atlanir
        if not ((g.ilk_gercek >= PENCERE[0]) & (g.ilk_gercek <= PENCERE[1])).any():
            continue
        # aday: pencere icindeki en erken, serisi olan listeleme
        icerde = g[(g.ilk_gercek >= PENCERE[0]) & (g.ilk_gercek <= PENCERE[1]) & (g.seri_n > 0)]
        if icerde.empty:
            dis.append(dict(base=base, neden='seri yok')); continue
        icerde = icerde.assign(pr=icerde.borsa.map(ONCELIK)).sort_values(['ilk_gercek', 'pr'])
        ana = icerde.iloc[0]
        da = seri[(ana.borsa, ana.cift)]
        # daha erken (pencere oncesi) listeleme ayni token mi?
        erken = g[g.ilk_gercek < ana.ilk_gercek - pd.Timedelta(days=1)]
        eski_ayni = False
        for _, e in erken.iterrows():
            de = seri.get((e.borsa, e.cift))
            t = tutarli(de, da) if de is not None and len(de) else None
            if t is None or t:   # kontrol edilemiyorsa ayni token varsay (muhafazakar)
                eski_ayni = True; break
        if eski_ayni:
            # erken listeleme pencere icindeyse onu ana yap (ilk dongude zaten en erken secildi); pencere disiysa dis
            dis.append(dict(base=base, neden='pencere oncesi listeleme (%s %s)' % (e.borsa, e.ilk_gercek.date()))); continue
        ad = ' '.join(g.ad.astype(str))
        if base in STABIL or base.startswith('USD') or (base.endswith('USD') and len(base) > 3):
            dis.append(dict(base=base, neden='stabil/sarili')); continue
        if GATE_ADI.search(ad):
            dis.append(dict(base=base, neden='ad: ' + ad[:60])); continue
        if KALDIRAC.search(base) and re.search(r'\d+x(Long|Short)', ad):
            dis.append(dict(base=base, neden='kaldiracli')); continue
        d = da[da.index >= ana.ilk_gercek].copy()
        if len(d) < 30:
            dis.append(dict(base=base, neden='<30 mum')); continue
        if (d.c / d.c.shift(1)).max() > 100:
            dis.append(dict(base=base, neden='fiyat olcegi hatasi (tek gunde >100x)')); continue
        lr = np.log(d.c).diff().dropna()
        if lr.std() < 0.02:
            dis.append(dict(base=base, neden='dusuk oynaklik/pegli (std %.4f)' % lr.std())); continue
        borsalar = ','.join(sorted(set(g.borsa)))
        evren.append(dict(base=base, borsa=ana.borsa, cift=ana.cift, liste=ana.ilk_gercek, n=len(d),
                          son=d.index[-1], borsalar=borsalar, binance=('binance' in borsalar),
                          binance_durum=','.join(g[g.borsa == 'binance'].durum), ad=ad[:40]))
    E = pd.DataFrame(evren)
    D = pd.DataFrame(dis)
    E, D = ek_dislama(E, D, L)
    # isim degisikligi adaylari: binance BREAK cifti delist +-10 gun icinde ve fiyat orani ~10^k
    br = L[(L.borsa == 'binance') & (L.durum == 'BREAK') & (L.seri_n > 0)]
    ren = []
    for _, e in E.iterrows():
        d0 = seri[(e.borsa, e.cift)]
        c0 = d0.c.iloc[0]
        for _, b in br.iterrows():
            db = seri[(b.borsa, b.cift)]
            if not len(db):
                continue
            if abs((db.index[-1] - e.liste).days) <= 10 and b.base != e.base:
                oran = c0 / db.c.iloc[-1]
                k = np.round(np.log10(oran))
                if abs(np.log10(oran) - k) < np.log10(1.25):
                    ren.append(dict(base=e.base, eski=b.cift, eski_son=db.index[-1].date(), yeni_liste=e.liste.date(),
                                    oran=round(oran, 4)))
    R = pd.DataFrame(ren)
    R.to_csv(os.path.join(KOK, 'rename_aday.csv'), index=False)
    E.to_csv(os.path.join(KOK, 'evren_ham.csv'), index=False)
    D.to_csv(os.path.join(KOK, 'dislanan.csv'), index=False)
    pd.to_pickle({k: seri[(r.borsa, r.cift)] for k, r in zip(E.base, E.itertuples())}, os.path.join(KOK, 'seriler.pkl'))
    log.info('evren %d, dislanan %d, rename aday %d', len(E), len(D), len(R))
    log.info(D.neden.str.split(' ').str[0].value_counts().to_string())
    log.info(E.borsa.value_counts().to_string())


if __name__ == '__main__':
    {'capraz': capraz, 'kur': kur}[sys.argv[1]]()
