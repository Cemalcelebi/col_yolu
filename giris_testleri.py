# =====================================================================
#  GIRIS STRATEJILERI — hepsi tek tabloda, endeksle kiyasli
#  A) kirilimda gir            B) 5 bar tutunma sonrasi gir
#  C) retest: tavana geri gel + tekrar kir    D) B ile C birlesimi
#  Her biri icin: %20 ve %30 hedef, endeks farki, sermaye devri
# =====================================================================
import numpy as np, pandas as pd

def giris_testleri(w, xu, veri=None, ufuk=250, k=5, maliyet=0.4,
                   retest_tol=0.02, retest_bekle=15):
    veri=veri if veri is not None else VERI
    R=[]
    for r in w.itertuples():
        df=veri.get(r.sembol)
        if df is None: continue
        T=pd.Timestamp(r.tarih); x=df[df.index<=T]; s=col_segment(x)
        if not s: continue
        il=df[df.index>T].head(ufuk)
        if len(il)<40: continue
        C=il.Close.to_numpy(float); H=il.High.to_numpy(float); L=il.Low.to_numpy(float)
        tav=s['tavan']
        kb=next((i for i,c in enumerate(C) if c>tav), None)
        if kb is None or kb+k>=len(C)-20: continue
        xo=xu[xu.index<=T]; xi=xu[xu.index>T].head(ufuk)
        if not len(xo) or len(xi)<40: continue
        XC=xi.Close.to_numpy(float)
        def cik(giris, bas_i, hedef):
            m=H[bas_i:]>=giris*(1+hedef/100)
            j=int(np.argmax(m))+bas_i if m.any() else len(C)-1
            return ((hedef if m.any() else (float(C[-1])/giris-1)*100)-maliyet,
                    j, (float(XC[min(j,len(XC)-1)])/float(XC[bas_i])-1)*100)
        d={'sembol':r.sembol}
        # A) kirilim
        gA=float(C[kb]); iA=kb+1
        # B) 5 bar tutunma
        teyit=bool((C[kb+1:kb+k+1]>tav).all() and C[kb+k]>gA)
        gB=float(C[kb+k]); iB=kb+k+1
        # C) retest: kirilimdan sonra 'retest_bekle' bar icinde tavana %tol yakin dip,
        #    sonra tekrar tavan ustu kapanis
        gC=iC=None
        for j in range(kb+1, min(kb+1+retest_bekle, len(C)-20)):
            if L[j]<=tav*(1+retest_tol):
                for q in range(j+1, min(j+8, len(C)-20)):
                    if C[q]>tav and C[q]>C[q-1]: gC=float(C[q]); iC=q+1; break
                break
        for hd in (20,30):
            a,ja,xa=cik(gA,iA,hd); d[f'A{hd}']=a; d[f'A{hd}_x']=xa; d[f'A{hd}_bar']=ja-kb
            if teyit:
                b,jb,xb=cik(gB,iB,hd); d[f'B{hd}']=b; d[f'B{hd}_x']=xb; d[f'B{hd}_bar']=jb-kb
            if gC is not None:
                c,jc,xc=cik(gC,iC,hd); d[f'C{hd}']=c; d[f'C{hd}_x']=xc; d[f'C{hd}_bar']=jc-kb
            if teyit and gC is not None:
                d[f'D{hd}']=b if iB<=iC else c
                d[f'D{hd}_x']=xb if iB<=iC else xc
                d[f'D{hd}_bar']=(jb if iB<=iC else jc)-kb
        R.append(d)
    p=pd.DataFrame(R)
    if p.empty: print("kayit yok"); return p
    print(f"\n  n={len(p)}  (A=kirilim  B=5bar tutunma  C=retest  D=B+C)\n")
    print(f"  {'strateji':>9s} {'n':>5s} {'medyan':>8s} {'kazanan':>8s} {'bekl':>7s} "
          f"{'endeks':>7s} {'FARK':>7s} {'yenen%':>7s} {'sure':>5s} {'devir':>6s} {'yillik':>8s}")
    for hd in (20,30):
        for st in 'ABCD':
            c=f'{st}{hd}'
            if c not in p: continue
            v=p[c].dropna()
            if len(v)<20: continue
            vx=p[f'{c}_x'].dropna(); fark=(v.values-vx.values)
            kz=v[v>0].mean() if (v>0).any() else 0; ky=v[v<=0].mean() if (v<=0).any() else 0
            bek=(v>0).mean()*kz+(v<=0).mean()*ky
            gun=float(p[f'{c}_bar'].dropna().median()); devir=252/max(gun,1)
            yil=((1+bek/100)**devir-1)*100
            print(f"  {st}/%{hd:<5d} {len(v):5d} {v.median():+7.1f}% {100*(v>0).mean():7.0f}% "
                  f"{bek:+6.1f}% {vx.median():+6.1f}% {np.median(fark):+6.1f}% "
                  f"{100*(fark>0).mean():6.0f}% {gun:5.0f} {devir:5.1f}x {yil:+7.0f}%")
        print()
    return p

print("[ok] giris_testleri yuklendi")
print("  p = giris_testleri(w, xu)")
