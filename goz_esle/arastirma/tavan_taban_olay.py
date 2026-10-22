# Olay calismasi: >=4 tavan (10 gun icinde) ardindan >=3 taban (sonraki 6 gun icinde), BIST 2022-06 -> 2026-10.
import pickle, numpy as np, pandas as pd
V=pickle.load(open('bist_2022.pkl','rb'))
# piyasa: gunluk medyan getiri
R=pd.DataFrame({s:d.Close.pct_change() for s,d in V.items()})
piy=R.median(axis=1)
rows=[]
for s,d in V.items():
    c=d.Close.to_numpy(float); h=d.High.to_numpy(float); l=d.Low.to_numpy(float); n=len(c)
    if n<80: continue
    r=np.r_[np.nan, c[1:]/c[:-1]-1]
    tav=r>=0.095; tab=r<=-0.095
    son=-999
    for e in range(15,n):
        if e-son<40: continue
        if tab[e-5:e+1].sum()>=3 and tab[e]:            # e: 3. taban gunu (son 6 gunde)
            w0=e-15
            ilk_tab=e-5+int(np.argmax(tab[e-5:e+1]))
            if tav[w0:ilk_tab].sum()>=4:
                tepe=h[w0:e+1].max(); bas=c[w0]
                rows.append(dict(sembol=s, tarih=d.index[e].date(), giris=c[e], tepe=tepe, kos=(tepe/bas-1)*100, geri=(c[e]/tepe-1)*100,
                    **{f'r{k}':((c[e+k]/c[e]-1)*100 if e+k<n else np.nan) for k in (5,20,60,120)},
                    **{f'p{k}':((np.prod(1+piy.loc[d.index[e+1:e+k+1]].fillna(0))-1)*100 if e+k<n else np.nan) for k in (20,60)},
                    dip60=((l[e+1:e+61].min()/c[e]-1)*100 if e+60<n else np.nan),
                    ulas41=(bool((h[e+1:e+121]>=c[e]*1.41).any()) if e+120<n else np.nan),
                    ulas41_60=(bool((h[e+1:e+61]>=c[e]*1.41).any()) if e+60<n else np.nan)))
                son=e
O=pd.DataFrame(rows); O.to_csv('../begyo/olaylar.csv',index=False)
print('olay', len(O), 'hisse', O.sembol.nunique())
print(O[['kos','geri','r5','r20','r60','r120','dip60']].describe(percentiles=[.25,.5,.75]).round(1).to_string())
for k in (20,60):
    m=O[f'r{k}'].notna(); print(f'{k}g: pozitif %{(O.loc[m,f"r{k}"]>0).mean()*100:.0f}, piyasaya gore medyan {(O.loc[m,f"r{k}"]-O.loc[m,f"p{k}"]).median():+.1f}')
m=O.dip60.notna(); print('60g icinde -%20 daha dusen %', round((O.loc[m,'dip60']<=-20).mean()*100), ' -%30 %', round((O.loc[m,'dip60']<=-30).mean()*100))
for c_ in ('ulas41_60','ulas41'):
    m=O[c_].notna(); print(c_, '+%41 (maliyet 3.97) gorulme %', round(O.loc[m,c_].astype(float).mean()*100), 'n', m.sum())
print(O.sort_values('tarih').tail(12)[['sembol','tarih','kos','geri','r20','r60','dip60']].round(1).to_string())
