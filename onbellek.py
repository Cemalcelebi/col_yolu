# ===== ONBELLEK — sinyal + ileri veri, testler icin (2026-09-18)
#  Kayit: seg (col_segment sozlugu: doji/alt_fitil/dar/gecerli_oran dahil),
#         sT/sO/sH/sL/sC/sV (segment barlari, tarihli), iT/iO/iH/iL/iC/iV (ileri), s20.
#  onbellek_guncelle(OB, veri): eski pkl'lerde eksik alanlari (dar, gecerli_oran,
#  gecerli-bar doji/fitil, sT) sinyal gunu segmentini yeniden olcerek tamamlar.
import pickle, time, logging, numpy as np, pandas as pd
olog=logging.getLogger('col.onbellek')

def _kayit(sembol, T, gecer, s, x, il):
    seg=x[x.index>=pd.Timestamp(s['bas_tarih'])]
    s20=pd.concat([x.Close,il.Close]).rolling(20).mean().to_numpy(float)[-len(il):]
    return {'sembol':sembol,'tarih':T,'GECER':bool(gecer),'seg':s,'sT':seg.index.to_numpy(),
            'sO':seg.Open.to_numpy(float),'sH':seg.High.to_numpy(float),'sL':seg.Low.to_numpy(float),'sC':seg.Close.to_numpy(float),'sV':seg.Volume.to_numpy(float),
            'iO':il.Open.to_numpy(float),'iH':il.High.to_numpy(float),'iL':il.Low.to_numpy(float),'iC':il.Close.to_numpy(float),'iV':il.Volume.to_numpy(float),
            'iT':il.index.to_numpy(),'s20':s20}

def onbellek_kur(dd, veri, ad, ileri=300):
    t0=time.time(); R=[]; hata=0
    for i,r in enumerate(dd.itertuples()):
        if i%500==0: print(f"  {i}/{len(dd)} {time.time()-t0:.0f}s")
        df=veri.get(r.sembol)
        if df is None: continue
        T=pd.Timestamp(r.tarih); x=df[df.index<=T]
        try: s=col_segment(x)
        except Exception as e: olog.debug(f'{r.sembol}@{T}: {e}'); hata+=1; s=None
        if not s or s['uzunluk']<MIN_UZ or s['yukseklik_atr']>MAX_YUK: continue
        il=df[df.index>T].head(ileri)
        if len(il)<40: continue
        R.append(_kayit(r.sembol,T,getattr(r,'GECER',True),s,x,il))
    tmp=f'{K}/onbellek_{ad}.pkl.tmp'
    pickle.dump(R,open(tmp,'wb')); import os; os.replace(tmp,f'{K}/onbellek_{ad}.pkl')
    print(f"  {ad}: {len(R)} kayit, hata {hata}, {time.time()-t0:.0f}s -> onbellek_{ad}.pkl"); return R

def onbellek_guncelle(OB, veri, ad=None):
    """Eski kayitlara dar/gecerli_oran/sT ekler (segment sinyal gununde yeniden olculur).
    ad verilirse pkl ustune yazar."""
    t0=time.time(); n=0; hata=0
    for i,o in enumerate(OB):
        if 'sT' in o and 'dar' in o['seg'] and 'gecerli_oran' in o['seg']: continue
        df=veri.get(o['sembol'])
        if df is None: hata+=1; continue
        T=pd.Timestamp(o['tarih']); x=df[df.index<=T]
        try: s=col_segment(x)
        except Exception as e: olog.debug(f'{o["sembol"]}@{T}: {e}'); s=None
        if not s: hata+=1; continue
        seg=x[x.index>=pd.Timestamp(s['bas_tarih'])]
        o['seg']=s; o['sT']=seg.index.to_numpy()
        for k,c in (('sO','Open'),('sH','High'),('sL','Low'),('sC','Close'),('sV','Volume')): o[k]=seg[c].to_numpy(float)
        n+=1
        if i%500==0: print(f"  {i}/{len(OB)} {time.time()-t0:.0f}s")
    print(f"  guncellendi {n} | hata {hata} | {time.time()-t0:.0f}s")
    if ad:
        import os; tmp=f'{K}/onbellek_{ad}.pkl.tmp'; pickle.dump(OB,open(tmp,'wb')); os.replace(tmp,f'{K}/onbellek_{ad}.pkl')
        print(f"  -> onbellek_{ad}.pkl yazildi")
    return OB
print("[ok] onbellek.py: onbellek_kur(dd, veri, ad) | onbellek_guncelle(OB, veri, ad)")
