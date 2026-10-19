# =====================================================================
#  SELALE DESENI — genisleyen tepe + cuce tepe + cokus   (2026-09-18)
#
#  Desen (Cemal):
#    Tepe1 -> Cukur1 -> Tepe2 (> Tepe1 x(1+LEG)) -> Cukur2 (< Cukur1 x(1-LEG))
#          -> Cuce Tepe (< Tepe2 x(1-DWARF), > Cukur2) -> SELALE (>=%15 dusus, 30 bar)
#
#  Iki mod:
#    KUTUPHANE : selale GERCEKLESMIS ornekleri bul (goz icin). Gelecek bilgisi kullanir.
#    TEST      : cuce tepe TEYIT ANINDA sinyal (gelecek bilgisi yok), ileride selale
#                geldi mi olc; ayni hisselerde rastgele gunlerin taban oraniyla kiyasla.
#
#  Tepe/cukur: bar, +-DISTANCE penceresinin en yuksegi/dusugu. Bir tepe ancak
#  DISTANCE bar sonra bilinir -> TEST modunda sinyal = cuce_tepe + DISTANCE.
#
#  Kullanim (BASLAT sonrasi):
#    exec(open(f'{K}/selale.py').read())
#    kut = selale_kutuphane(VERI, 'BIST')            # goz icin liste + csv
#    tst = selale_test(VERI, 'BIST')                 # ongoru testi
#    tst = selale_test(VERI_ABD, 'ABD')              # ABD (once VERI_ABD yukle)
# =====================================================================
import numpy as np, pandas as pd, time, os
from dataclasses import dataclass

@dataclass
class SelaleAyar:
    DISTANCE: int = 15          # pivot penceresi (bar). Tepe = +-DISTANCE icinde en yuksek High
    MIN_LEG_PCT: float = 0.05   # Tepe2 > Tepe1 x(1+..), Cukur2 < Cukur1 x(1-..)
    MIN_DWARF_PCT: float = 0.03 # Cuce < Tepe2 x(1-..)
    MIN_TOTAL_BARS: int = 40    # Tepe1 -> Cuce arasi
    MAX_TOTAL_BARS: int = 400
    WATERFALL_PCT: float = 0.15 # selale: cuce sonrasi min Low, cuceden bu kadar asagi
    WATERFALL_BARS: int = 30
    MIN_BAR: int = 250
AYAR=SelaleAyar()

def _pivotlar(H, L, d):
    """Sol-sag simetrik pivot: i, [i-d, i+d] araliginin max/min'i. Son d bar pivot olamaz (teyitsiz)."""
    n=len(H); P=[]; T=[]
    for i in range(d, n-d):
        if H[i]>=H[i-d:i+d+1].max(): P.append(i)
        if L[i]<=L[i-d:i+d+1].min(): T.append(i)
    return P, T

def _desen_ara(H, L, a: SelaleAyar):
    """(p1,t1,p2,t2,p3) indeks demetleri. Her p1 icin sirayla 'sonraki ilk uygun' pivot."""
    P,T=_pivotlar(H,L,a.DISTANCE)
    if len(P)<3 or len(T)<2: return []
    out=[]; Tarr=np.array(T); Parr=np.array(P)
    for p1 in P:
        t1c=Tarr[Tarr>p1]
        if not len(t1c): continue
        t1=int(t1c[0])
        p2c=Parr[Parr>t1]
        if not len(p2c): continue
        p2=int(p2c[0])
        if H[p2]<H[p1]*(1+a.MIN_LEG_PCT): continue
        t2c=Tarr[Tarr>p2]
        if not len(t2c): continue
        t2=int(t2c[0])
        if L[t2]>L[t1]*(1-a.MIN_LEG_PCT): continue
        p3c=Parr[Parr>t2]
        if not len(p3c): continue
        p3=int(p3c[0])
        if H[p3]>H[p2]*(1-a.MIN_DWARF_PCT): continue
        if H[p3]<=L[t2]: continue
        tb=p3-p1
        if tb<a.MIN_TOTAL_BARS or tb>a.MAX_TOTAL_BARS: continue
        out.append((p1,t1,p2,t2,p3))
    # ayni cuce tepe icin en eski p1'i tut (tekrarlari at)
    g={}
    for d_ in out: g.setdefault(d_[4], d_)
    return list(g.values())

def _selale_mi(L, p3, a: SelaleAyar):
    fut=L[p3+1:p3+1+a.WATERFALL_BARS]
    if len(fut)<5: return None, None
    dusus=(1-fut.min()/max(1e-9,L[p3]))  # cuce LOW'una gore degil, cuce HIGH'ina gore olculur (asagida)
    return fut, None

def selale_kutuphane(veri, ad, a: SelaleAyar=AYAR, kaydet=True):
    """Selale GERCEKLESMIS ornekler (goz icin)."""
    t0=time.time(); R=[]; hata=0
    for s,df in veri.items():
        try:
            if len(df)<a.MIN_BAR: continue
            H=df.High.to_numpy(float); L=df.Low.to_numpy(float); idx=df.index
            for p1,t1,p2,t2,p3 in _desen_ara(H,L,a):
                fut=L[p3+1:p3+1+a.WATERFALL_BARS]
                if len(fut)<5: continue
                dusus=(H[p3]-fut.min())/H[p3]
                if dusus<a.WATERFALL_PCT: continue
                R.append({'hisse':s,'tepe1':str(idx[p1].date()),'tepe1_f':round(H[p1],2),'cukur1':str(idx[t1].date()),'cukur1_f':round(L[t1],2),
                          'tepe2':str(idx[p2].date()),'tepe2_f':round(H[p2],2),'cukur2':str(idx[t2].date()),'cukur2_f':round(L[t2],2),
                          'cuce':str(idx[p3].date()),'cuce_f':round(H[p3],2),'selale_%':round(dusus*100,1),'toplam_bar':p3-p1})
        except Exception as e: hata+=1
    q=pd.DataFrame(R)
    print(f"  {ad}: {len(q)} selale ornegi, {q.hisse.nunique() if len(q) else 0} hisse, hata {hata}, {time.time()-t0:.0f}s")
    if kaydet and len(q):
        y=f"{K}/selale_kutuphane_{ad}.csv"; q.to_csv(y,index=False); print(f"  -> {y}")
    return q

def selale_test(veri, ad, a: SelaleAyar=AYAR, rastgele=3000, tohum=42):
    """Ongoru: cuce tepe TEYIT aninda (p3+DISTANCE) sinyal. Sonraki WATERFALL_BARS icinde selale (>=%15) geldi mi?
    Taban: ayni evrende rastgele gunlerde ayni olcum."""
    t0=time.time(); R=[]; rng=np.random.default_rng(tohum); taban=[]
    for s,df in veri.items():
        if len(df)<a.MIN_BAR: continue
        H=df.High.to_numpy(float); L=df.Low.to_numpy(float); C=df.Close.to_numpy(float); idx=df.index; n=len(C)
        try: desenler=_desen_ara(H,L,a)
        except Exception: continue
        for p1,t1,p2,t2,p3 in desenler:
            sig=p3+a.DISTANCE                       # teyit ani
            if sig+a.WATERFALL_BARS>=n: continue
            c0=C[sig]; fut=L[sig+1:sig+1+a.WATERFALL_BARS]; fc=C[sig+1:sig+1+a.WATERFALL_BARS]
            dusus=(c0-fut.min())/c0; son=(fc[-1]/c0-1)*100
            # sinyal aninda fiyat cuceye gore nerede (zaten dustu mu?)
            R.append({'hisse':s,'cuce':str(idx[p3].date()),'sinyal':str(idx[sig].date()),'sinyal_f':round(c0,2),
                      'cuce_altinda_%':round((c0/H[p3]-1)*100,1),'maxdusus_%':round(dusus*100,1),'son_%':round(son,1),'selale':int(dusus>=a.WATERFALL_PCT)})
        # taban: rastgele gunler
        if n-a.WATERFALL_BARS-1<=a.MIN_BAR: continue
        if n-a.WATERFALL_BARS-1<=a.MIN_BAR: continue
        for _ in range(max(1,rastgele//max(1,len(veri)))):
            i=int(rng.integers(a.MIN_BAR, n-a.WATERFALL_BARS-1))
            c0=C[i]; fut=L[i+1:i+1+a.WATERFALL_BARS]; fc=C[i+1:i+1+a.WATERFALL_BARS]
            taban.append({'maxdusus_%':(c0-fut.min())/c0*100,'son_%':(fc[-1]/c0-1)*100,'selale':int((c0-fut.min())/c0>=a.WATERFALL_PCT)})
    q=pd.DataFrame(R); tb=pd.DataFrame(taban)
    print(f"\n  {ad}  desen sinyali n={len(q)} ({q.hisse.nunique() if len(q) else 0} hisse) | taban n={len(tb)} | {time.time()-t0:.0f}s")
    if not len(q): return q
    print(f"  {'':28s} {'selale(>=%15/30b)':>18s} {'maxdusus medyan':>16s} {'son_% medyan':>13s} {'dusen(son<0)':>13s}")
    print(f"  {'DESEN (cuce teyit ani)':28s} {100*q.selale.mean():17.0f}% {q['maxdusus_%'].median():15.1f}% {q['son_%'].median():+12.1f}% {100*(q['son_%']<0).mean():12.0f}%")
    print(f"  {'TABAN (rastgele gun)':28s} {100*tb.selale.mean():17.0f}% {tb['maxdusus_%'].median():15.1f}% {tb['son_%'].median():+12.1f}% {100*(tb['son_%']<0).mean():12.0f}%")
    # sinyal aninda cuceden ne kadar asagida -> alt gruplar
    print(f"\n  sinyal aninda fiyat cuce tepeye gore:")
    for et,m in [('hala cuce yakininda (>-5%)',q['cuce_altinda_%']>-5),('-5..-15% asagida',(q['cuce_altinda_%']<=-5)&(q['cuce_altinda_%']>-15)),('<-15% (selale basladi)',q['cuce_altinda_%']<=-15)]:
        z=q[m]
        if len(z)>=10: print(f"    {et:28s} n={len(z):4d} selale %{100*z.selale.mean():.0f} son_% medyan {z['son_%'].median():+.1f}")
    y=f"{K}/selale_test_{ad}.csv"; q.to_csv(y,index=False); print(f"  -> {y}")
    return q

print("[ok] selale yuklendi")
print("  kut = selale_kutuphane(VERI,'BIST')   |   tst = selale_test(VERI,'BIST')")
