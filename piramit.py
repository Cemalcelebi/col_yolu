# =====================================================================
#  PIRAMIT — kirilimda YARIM gir, 5. barda teyit varsa TAMAMLA
#  Teyit: 5 bar tavan ustunde kaldi VE ilerleme > 0
#  Karsilastirma: (a) hepsine tam gir  (b) piramit  (c) sadece teyitlilere gir
#  Cikis hepsinde ayni: %HEDEF kar hedefi, stop yok
# =====================================================================
import numpy as np, pandas as pd

def piramit(w, veri=None, hedef=None, ufuk=250, k=5, maliyet=0.4):
    veri=veri if veri is not None else VERI
    hedef=HEDEF if hedef is None else hedef
    R=[]
    for r in w.itertuples():
        df=veri.get(r.sembol)
        if df is None: continue
        T=pd.Timestamp(r.tarih); x=df[df.index<=T]; s=col_segment(x)
        if not s: continue
        il=df[df.index>T].head(ufuk)
        if len(il)<40: continue
        C=il.Close.to_numpy(float); H=il.High.to_numpy(float)
        tav=s['tavan']
        kb=next((i for i,c in enumerate(C) if c>tav), None)
        if kb is None or kb+k>=len(C)-20: continue
        g1=float(C[kb])                         # 1. giris: kirilim kapanisi
        teyit=bool((C[kb+1:kb+k+1]>tav).all() and C[kb+k]>g1)
        g2=float(C[kb+k])                       # 2. giris: k. bar kapanisi
        # cikis: hedefe vuran ilk bar, yoksa ufuk sonu
        def sonuc(giris, bas_i):
            Hs=H[bas_i:]; Cs=C[bas_i:]
            m=Hs>=giris*(1+hedef/100)
            return (hedef if m.any() else (float(Cs[-1])/giris-1)*100) - maliyet
        r1=sonuc(g1,kb+1)
        r2=sonuc(g2,kb+k+1) if teyit else np.nan
        R.append({'sembol':r.sembol,'teyit':teyit,
                  'tam':r1,                                   # (a) tam pozisyon kirilimda
                  'piramit': 0.5*r1+0.5*(r2 if teyit else 0), # (b) yarim + teyitte yarim (yoksa yarim nakit)
                  'sadece_teyit': r1 if teyit else np.nan})   # (c) sadece teyitli isleme gir
    p=pd.DataFrame(R)
    if p.empty: print("kayit yok"); return p
    print(f"\n  n={len(p)} | teyit oranı %{100*p.teyit.mean():.0f} | hedef %{hedef}\n")
    print(f"  {'strateji':14s} {'n':>5s} {'medyan':>8s} {'ort':>7s} {'kazanan':>8s} {'beklenti':>9s}")
    for ad in ['tam','piramit','sadece_teyit']:
        v=p[ad].dropna()
        if len(v)<10: continue
        kz=v[v>0].mean() if (v>0).any() else 0; ky=v[v<=0].mean() if (v<=0).any() else 0
        print(f"  {ad:14s} {len(v):5d} {v.median():+7.1f}% {v.mean():+6.1f}% "
              f"{100*(v>0).mean():7.0f}% {(v>0).mean()*kz+(v<=0).mean()*ky:+8.1f}%")
    print("\n  'piramit' > 'tam' ise: teyit bekleyip eklemek deger katiyor")
    print("  'sadece_teyit' > 'tam' ise: teyitsiz islemlere hic girmemek daha iyi")
    return p

print("[ok] piramit yuklendi")
print("  p = piramit(w)          # w = kirilim_sonrasi ciktisi")
print("  p = piramit(w, hedef=30)")
