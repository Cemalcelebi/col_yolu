# =====================================================================
#  KIRILIM SONRASI TEYIT — dev kazananlar ilk 5-10 barda farkli mi?
#  Girişte ayirt edemedik (49 olcu). Simdi kirilimdan SONRAKI davranisa
#  bakiyoruz: geri cekilme, tutunma, hacim, ardisik yukselis.
#  Ise yararsa strateji: kucuk gir -> teyit gelirse EKLE.
# =====================================================================
import numpy as np, pandas as pd

def kirilim_sonrasi(sec, veri=None, ufuk=250, k_list=(3,5,10)):
    veri = veri if veri is not None else VERI
    R=[]
    for r in sec.itertuples():
        df=veri.get(r.sembol)
        if df is None: continue
        T=pd.Timestamp(r.tarih)
        x=df[df.index<=T]; s=col_segment(x)
        if not s: continue
        il=df[df.index>T].head(ufuk)
        if len(il)<40: continue
        C=il.Close.to_numpy(float); H=il.High.to_numpy(float)
        L=il.Low.to_numpy(float); V=il.Volume.to_numpy(float)
        tav=s['tavan']; p0=float(x.Close.iloc[-1])
        kb=next((i for i,c in enumerate(C) if c>tav), None)
        if kb is None or kb>len(C)-25: continue
        gp=float(C[kb]); v_on=float(x.Volume.tail(20).mean())
        d={'sembol':r.sembol,'tarih':r.tarih,
           'MFE':(float(H.max())/gp-1)*100,
           'son':(float(C[-1])/gp-1)*100,
           'kirilim_hac':float(V[kb])/max(v_on,1)}
        for k in k_list:
            if kb+k>=len(C): continue
            seg=slice(kb+1,kb+k+1)
            Cs,Ls,Vs=C[seg],L[seg],V[seg]
            d[f'tutundu{k}']=int((Cs>tav).all())
            d[f'geri{k}']=(float(Ls.min())/gp-1)*100
            d[f'hac{k}']=float(Vs.mean())/max(v_on,1)
            d[f'yuk_kap{k}']=int((np.diff(np.r_[gp,Cs])>0).sum())
            d[f'ilerleme{k}']=(float(Cs[-1])/gp-1)*100
        R.append(d)
    w=pd.DataFrame(R)
    if w.empty: print("kayit yok"); return w
    w['sinif']=pd.cut(w.MFE,[-1e9,20,50,100,1e9],labels=['<20','20-50','50-100','100+'])
    print(f"\n  n={len(w)} | sinif dagilimi: {w.sinif.value_counts().sort_index().to_dict()}\n")
    kol=[c for c in w.columns if any(c.startswith(p) for p in
         ('tutundu','geri','hac','yuk_kap','ilerleme','kirilim_hac'))]
    print("  MFE sinifina gore kirilim sonrasi ozellikler (medyan):")
    print(w.groupby('sinif',observed=True)[kol].median().round(2).T.to_string())
    # 100+ vs <20 fark
    dev=w[w.sinif=='100+']; kt=w[w.sinif=='<20']
    print(f"\n  DEV (100+, n={len(dev)}) vs KOTU (<20, n={len(kt)}):")
    for c in kol:
        a,b=dev[c].median(),kt[c].median()
        print(f"    {c:14s} dev {a:+7.2f} | kotu {b:+7.2f} | fark {a-b:+7.2f}")
    return w

def teyit_stratejisi(w, k=5, gerisinir=-3.0):
    """kirilimdan k bar sonra tutundu & geri<gerisinir ise EKLE senaryosu"""
    if f'tutundu{k}' not in w: print("k yok"); return
    ok=w[(w[f'tutundu{k}']==1)&(w[f'geri{k}']>gerisinir)]
    yok=w[~w.index.isin(ok.index)]
    for ad,g in [("TEYIT VAR",ok),("teyit yok",yok),("hepsi",w)]:
        if len(g)<10: continue
        print(f"  {ad:10s} n={len(g):4d} MFE med %{g.MFE.median():+.1f} "
              f"son med %{g.son.median():+.1f} 100+ orani %{100*(g.MFE>=100).mean():.1f} "
              f"kaybeden %{100*(g.son<0).mean():.1f}")

print("[ok] kirilim_sonrasi yuklendi")
print("  w = kirilim_sonrasi(d[d.GECER])")
print("  teyit_stratejisi(w, k=5)")
