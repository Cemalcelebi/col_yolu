"""Kripto yeni token olcumu - veri indirme (Binance data-api, OKX, Gate).
Kullanim: python3 -I indir.py <asama> ; asama: binance_ilk | binance_tam | okx | gate | capraz
Ham yanitlar data/<borsa>/<cift>.json olarak saklanir (onbellek: varsa yeniden indirilmez).
"""
import json, os, sys, time, logging
import requests

KOK = os.path.dirname(os.path.abspath(__file__))
VERI = os.path.join(KOK, 'data')
CA = '/root/.ccr/ca-bundle.crt'
BASLA_MS = 1685577600000          # 2023-06-01 UTC
SIMDI_MS = int(time.time() * 1000)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler(os.path.join(KOK, 'indir.log')), logging.StreamHandler()])
log = logging.getLogger('indir')
S = requests.Session()


def al(url, params, bekle=0.12, deneme=5):
    for d in range(deneme):
        try:
            r = S.get(url, params=params, timeout=30, verify=CA)
            if r.status_code == 429:
                log.warning('429 %s', url); time.sleep(5 * (d + 1)); continue
            if r.status_code >= 500:
                time.sleep(2 * (d + 1)); continue
            time.sleep(bekle)
            return r.status_code, r.json()
        except Exception as e:  # ag hatasi
            log.warning('hata %s %s %s', url, params, e); time.sleep(3 * (d + 1))
    return None, None


def yaz(borsa, ad, veri):
    d = os.path.join(VERI, borsa); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, ad + '.json'), 'w') as f:
        json.dump(veri, f)


def var(borsa, ad):
    return os.path.exists(os.path.join(VERI, borsa, ad + '.json'))


def binance_semboller():
    b = json.load(open(os.path.join(VERI, 'binance_exchangeInfo.json')))['symbols']
    return [x for x in b if x['quoteAsset'] == 'USDT']


def binance_ilk():
    """Her USDT cifti icin ilk ve son mum (liste tarihi / delist tarihi)."""
    out = {}
    p = os.path.join(VERI, 'binance_ilk_son.json')
    if os.path.exists(p):
        out = json.load(open(p))
    for x in binance_semboller():
        s = x['symbol']
        if s in out:
            continue
        u = 'https://data-api.binance.vision/api/v3/klines'
        k1, ilk = al(u, {'symbol': s, 'interval': '1d', 'startTime': 0, 'limit': 1})
        k2, son = al(u, {'symbol': s, 'interval': '1d', 'limit': 1})
        out[s] = {'status': x['status'], 'base': x['baseAsset'], 'ilk': ilk, 'son': son, 'kod': [k1, k2]}
        if len(out) % 50 == 0:
            log.info('binance ilk %d', len(out)); json.dump(out, open(p, 'w'))
    json.dump(out, open(p, 'w'))
    log.info('binance ilk bitti %d', len(out))


def binance_tam(sembol):
    if var('binance', sembol):
        return
    u = 'https://data-api.binance.vision/api/v3/klines'
    t, tum = BASLA_MS, []
    while True:
        k, r = al(u, {'symbol': sembol, 'interval': '1d', 'startTime': t, 'limit': 1000})
        if not isinstance(r, list) or not r:
            break
        tum += r
        if len(r) < 1000:
            break
        t = r[-1][0] + 86400000
    yaz('binance', sembol, tum)


def okx_tam(inst):
    if var('okx', inst):
        return
    u = 'https://www.okx.com/api/v5/market/history-candles'
    after, tum = None, []
    for _ in range(40):
        p = {'instId': inst, 'bar': '1Dutc', 'limit': 100}
        if after:
            p['after'] = after
        k, r = al(u, p, bekle=0.15)
        if not r or r.get('code') != '0' or not r.get('data'):
            break
        tum += r['data']
        after = r['data'][-1][0]
        if int(after) < BASLA_MS or len(r['data']) < 100:
            break
    yaz('okx', inst, tum)


def gate_tam(cift):
    if var('gate', cift):
        return
    u = 'https://api.gateio.ws/api/v4/spot/candlesticks'
    tum, bas = [], BASLA_MS // 1000
    son = SIMDI_MS // 1000
    while bas < son:
        bit = min(bas + 900 * 86400, son)
        k, r = al(u, {'currency_pair': cift, 'interval': '1d', 'from': bas, 'to': bit}, bekle=0.08)
        if isinstance(r, list):
            tum += r
        else:
            log.warning('gate %s %s', cift, r)
        bas = bit + 1
    yaz('gate', cift, tum)


def main():
    asama = sys.argv[1]
    if asama == 'binance_ilk':
        binance_ilk()
    elif asama == 'binance_tam':
        ilk = json.load(open(os.path.join(VERI, 'binance_ilk_son.json')))
        hedef = [s for s, v in ilk.items() if v['ilk'] and isinstance(v['ilk'], list) and v['ilk']
                 and (v['ilk'][0][0] >= BASLA_MS or (v['son'] and v['son'][0][0] >= BASLA_MS + 180 * 86400000 and v['status'] != 'TRADING'))]
        log.info('binance tam hedef %d', len(hedef))
        for i, s in enumerate(hedef):
            binance_tam(s)
            if i % 50 == 0:
                log.info('binance tam %d/%d', i, len(hedef))
    elif asama == 'okx':
        o = json.load(open(os.path.join(VERI, 'okx_instruments.json')))['data']
        hedef = [x['instId'] for x in o if x['quoteCcy'] == 'USDT' and int(x['listTime'] or 0) >= BASLA_MS]
        log.info('okx hedef %d', len(hedef))
        for i, s in enumerate(hedef):
            okx_tam(s)
            if i % 50 == 0:
                log.info('okx %d/%d', i, len(hedef))
    elif asama == 'gate':
        g = json.load(open(os.path.join(VERI, 'gate_pairs.json')))
        hedef = [x['id'] for x in g if x['quote'] == 'USDT' and (x['buy_start'] or 0) * 1000 >= BASLA_MS - 0]
        hedef += [x['id'] for x in g if x['quote'] == 'USDT' and (x['buy_start'] or 0) < 86400 * 365]
        log.info('gate hedef %d', len(hedef))
        for i, s in enumerate(hedef):
            gate_tam(s)
            if i % 100 == 0:
                log.info('gate %d/%d', i, len(hedef))
    elif asama == 'capraz':
        # aday bazlarinin eski listelemelerini de indir (fiyat tutarlilik + erken liste kontrolu)
        liste = json.load(open(os.path.join(KOK, 'capraz_hedef.json')))
        log.info('capraz hedef %d', len(liste))
        for borsa, cift in liste:
            {'binance': binance_tam, 'okx': okx_tam, 'gate': gate_tam}[borsa](cift)
    log.info('asama bitti %s', asama)


if __name__ == '__main__':
    main()
