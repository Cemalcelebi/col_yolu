"""Veri sinamasi IS 2: bizim V_ABD (Yahoo kaynakli) vs Tiingo (bagimsiz). Anahtar yok: ag vekili kimlik dogrulamayi ekler.
Tiingo ham yanitlari repoya girmez (lisans): TIINGO_CACHE dizinine yazilir. Istek sayisi tavani 45, saatte 50 kota.
python veri_sinama_tiingo.py indir | karsilastir"""
import os, sys, json, time, numpy as np, pandas as pd, requests
from veri_sinama_sec import yukle, TOHUM
CACHE = os.environ.get("TIINGO_CACHE", "/tmp/claude-0/tiingo_cache"); os.makedirs(CACHE, exist_ok=True)
URL = "https://api.tiingo.com/tiingo/daily/{k}/prices"
def kodlar():
    V = yukle("ABD"); S = json.load(open("secim.json"))
    goz = [x["kod"] for x in S["ABD"]["secim"]]
    havuz = sorted(k for k in V if k not in goz)
    rng = np.random.RandomState(TOHUM)
    rast = [havuz[i] for i in rng.permutation(len(havuz))[:30]]
    return rast + goz + (["AAPL"] if os.environ.get("EK_AAPL") else [])
def indir():
    L = kodlar(); n_istek = 0
    for k in L:
        f = f"{CACHE}/{k}.json"
        if os.path.exists(f): continue
        while True:
            r = requests.get(URL.format(k=k.replace(".", "-").lower()), params=dict(startDate="2016-01-04", endDate="2023-12-29"),
                             headers={"Content-Type": "application/json"}, timeout=90); n_istek += 1
            print(k, r.status_code, n_istek, flush=True)
            if r.status_code == 429:
                print("429: 20 dk bekleniyor", flush=True); time.sleep(1200); continue
            break
        json.dump(dict(http=r.status_code, govde=r.json() if r.status_code == 200 else r.text[:300]), open(f, "w"))
        time.sleep(2)
        if n_istek >= 36 and not os.environ.get("EK_AAPL"): break
    print("istek", n_istek)
def hisse_say(k, V):
    j = json.load(open(f"{CACHE}/{k}.json"))
    if isinstance(j["govde"], dict) and "detail" in j["govde"]: return dict(kod=k, durum="KOTA", mesaj=j["govde"]["detail"][:80])
    if j["http"] != 200 or not j["govde"]: return dict(kod=k, durum="YOK", http=j["http"])
    T = pd.DataFrame(j["govde"]); T.index = pd.to_datetime(T.date).dt.tz_localize(None).dt.normalize()
    B = V[k].loc["2016-01-04":"2023-12-29"]; B = B[(B.High >= B.Low) & (B.Volume > 0) & (B.Close > 0)]
    ort = B.index.intersection(T.index); b = B.loc[ort]; t = T.loc[ort]
    rb = b.Close.pct_change(); rt = t.adjClose.pct_change(); m = rb.notna() & rt.notna()
    kor = float(np.corrcoef(rb[m], rt[m])[0, 1]); fark = (rb - rt).abs()[m]
    oran_a = b.Close / t.adjClose; oran_u = b.Close / t.close
    cv = lambda s: float(s.std() / s.mean())
    ob = b.Open / b.Close; ot = t.adjOpen / t.adjClose; fo = (ob / ot - 1).abs()
    hb = b.High / b.Close; ht = t.adjHigh / t.adjClose; fh = (hb / ht - 1).abs()
    lb = b.Low / b.Close; lt = t.adjLow / t.adjClose; fl = (lb / lt - 1).abs()
    hac = (b.Volume / t.adjVolume.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan)
    hacu = (b.Volume / t.volume.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan)
    gun = fark[fark > 0.01].sort_values(ascending=False)
    # tarih bazli: bizim gun, Tiingo'da yok / Tiingo gun, bizde yok
    fazla = B.index.difference(T.index); eksik = T.index.difference(B.index)
    # bolunme gunleri (Tiingo splitFactor != 1)
    bol = T.index[T.splitFactor != 1.0]
    s = dict(kod=k, durum="OK", ortak=len(ort), kor=kor, p_fark1=float((fark > .01).mean()), n_fark1=int((fark > .01).sum()),
             oran_adj_ort=float(oran_a.mean()), oran_adj_cv=cv(oran_a), oran_adj_ilk=float(oran_a.iloc[0]), oran_adj_son=float(oran_a.iloc[-1]),
             oran_ham_cv=cv(oran_u), oran_ham_ort=float(oran_u.mean()),
             p_acilis=float((fo > .005).mean()), p_yuksek=float((fh > .005).mean()), p_dusuk=float((fl > .005).mean()),
             hacim_med=float(hac.median()), hacim_ham_med=float(hacu.median()), bizde_fazla_gun=len(fazla), tiingo_fazla_gun=len(eksik),
             bolunme=[str(x.date()) for x in bol], temettu_gun=int((T.divCash > 0).sum()),
             ilk_gun_biz=str(B.index[0].date()), ilk_gun_t=str(T.index[0].date()))
    s["temiz"] = bool(kor >= 0.995 and s["p_fark1"] <= 0.005 and s["p_acilis"] <= 0.01)
    # en buyuk 5 fark gunu
    ayr = []
    for d, v in gun.head(5).items():
        ayr.append(dict(tarih=str(d.date()), biz_getiri=float(rb[d]), tiingo_getiri=float(rt[d]), biz_kap=float(b.Close[d]), tiingo_adj=float(t.adjClose[d]), tiingo_ham=float(t.close[d])))
    s["en_buyuk_farklar"] = ayr
    return s
def karsilastir():
    V = yukle("ABD"); L = kodlar(); out = []
    for k in L:
        if not os.path.exists(f"{CACHE}/{k}.json"): out.append(dict(kod=k, durum="ISTENMEDI")); continue
        out.append(hisse_say(k, V))
    ok = [o for o in out if o["durum"] == "OK"]; tm = sum(o["temiz"] for o in ok)
    ev = dict(istenen=len(L), olan=len(ok), yok=[o["kod"] for o in out if o["durum"] == "YOK"], kota_engeli=[o["kod"] for o in out if o["durum"] == "KOTA"], temiz=tm,
              hukum=("HÜKÜM VERİLEMEDİ: Tiingo aylık 500 sembol kotası doldu; yalnız %d hisse karşılaştırılabildi" % len(ok)) if len(ok) < 36 else ("VERİ TUTARLI" if tm >= 33 else "SORUNLU (temiz < 33)"), sorunlu=[o["kod"] for o in ok if not o["temiz"]])
    json.dump(dict(evren=ev, hisseler=out), open("veri_sinama_tiingo.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(ev, ensure_ascii=False))
if __name__ == "__main__":
    {"indir": indir, "karsilastir": karsilastir}[sys.argv[1]]()
