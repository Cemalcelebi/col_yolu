# SEC başvuru geçmişi indirme (K54). E-posta User-Agent için SEC_EPOSTA ortam değişkeninden okunur; koda yazılmaz.
import os, sys, json, time, urllib.request, pandas as pd
S='/tmp/claude-0/-home-user-col-yolu/82c570e4-187d-577a-9149-eeb29748a7da/scratchpad'
UA = f"col_yolu arastirma {os.environ['SEC_EPOSTA']}"
E = pd.read_csv('/home/user/col_yolu/arastirma_cikti/col_yolu_abd/K51_EVREN_PIT.csv')
ct = json.load(open(f'{S}/k54/company_tickers.json')); tmap = {v['ticker'].upper(): int(v['cik_str']) for v in ct.values()}
cik = {}
for r in E.itertuples():
    c = str(r.cik).split(";")[0] if pd.notna(r.cik) else tmap.get(str(r.sembol).upper())
    if c is not None and str(c) not in ("nan", "None", ""): cik[r.sembol] = int(float(c))
json.dump(cik, open(f'{S}/k54/sembol_cik.json','w'))
ciks = sorted(set(cik.values())); print('sembol', len(E), 'cik bulunan', len(cik), 'tekil cik', len(ciks), flush=True)
out = {}; yol = f'{S}/k54/sec_ozet.json'
if os.path.exists(yol): out = json.load(open(yol))
t0 = time.time(); hata = 0
for n, c in enumerate(ciks, 1):
    k = str(c)
    if k in out: continue
    url = f"https://data.sec.gov/submissions/CIK{c:010d}.json"
    for dene in range(3):
        try:
            rq = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})
            with urllib.request.urlopen(rq, timeout=30) as r:
                raw = r.read()
                if r.headers.get('Content-Encoding') == 'gzip':
                    import gzip; raw = gzip.decompress(raw)
                d = json.loads(raw)
            f = d['filings']['recent']
            # eski dosyalardaki başvurular (çok başvurulu şirketler)
            ek = []
            for fx in d['filings'].get('files', []):
                try:
                    rq2 = urllib.request.Request("https://data.sec.gov/submissions/" + fx['name'], headers={"User-Agent": UA})
                    with urllib.request.urlopen(rq2, timeout=30) as r2:
                        raw2 = r2.read()
                        if r2.headers.get('Content-Encoding') == 'gzip':
                            import gzip; raw2 = gzip.decompress(raw2)
                        f2 = json.loads(raw2); ek.append(f2)
                    time.sleep(0.12)
                except Exception: pass
            forms = list(f['form']); dates = list(f['filingDate']); items = list(f.get('items', [''] * len(forms)))
            for f2 in ek:
                forms += list(f2['form']); dates += list(f2['filingDate']); items += list(f2.get('items', [''] * len(f2['form'])))
            out[k] = {"name": d.get('name'), "tickers": d.get('tickers'), "exchanges": d.get('exchanges'), "sic": d.get('sic'), "formerNames": d.get('formerNames'),
                      "form": forms, "date": dates, "items": items}
            break
        except Exception as ex:
            if '404' in str(ex): out[k] = None; hata += 1; break
            if dene == 2: out[k] = None; hata += 1
            time.sleep(3 * (dene + 1))
    time.sleep(0.12)
    if n % 200 == 0:
        json.dump(out, open(yol, 'w')); print(n, len(ciks), 'hata', hata, round(time.time() - t0), flush=True)
json.dump(out, open(yol, 'w')); print('SEC_BITTI', len(out), 'hata', hata, round(time.time() - t0), flush=True)
