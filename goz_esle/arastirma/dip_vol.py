# Piyasa derin dipteyken (esit agirlik medyan endeks 60g <= -%20) oynak hisseler toparlanmada once mi gider? BIST 2016-26, iki donem.
import pickle, numpy as np, pandas as pd
V=pickle.load(open('bist_2015.pkl','rb'))
C=pd.DataFrame({s:d.Close for s,d in V.items()}).sort_index()
C=C[C.index>='2015-06-01']
R=C.pct_change(fill_method=None)
R=R.where((R>-0.25)&(R<0.25))                       # veri sicramasi kirp (BIST gunluk sinir %10)
piy=R.median(axis=1).fillna(0); E=(1+piy).cumprod()
e60=E/E.shift(60)-1
vol=R.rolling(60,min_periods=40).std()*np.sqrt(250)*100
olay=[]; son=None
for t,v in e60.items():
    if v<=-0.20 and (son is None or (C.index.get_loc(t)-C.index.get_loc(son))>120):
        olay.append(t); son=t
print('derin dip gunleri (60g <= -%20):', [str(t.date()) for t in olay]); print('bugun 60g', round(e60.iloc[-1]*100,1))
rows=[]
for t in olay:
    i=C.index.get_loc(t); v=vol.iloc[i].dropna(); c0=C.iloc[i]
    q=pd.qcut(v.rank(method='first'),3,labels=['dusuk','orta','yuksek'])
    for k in (20,60,120):
        if i+k>=len(C): continue
        f=(C.iloc[i+k]/c0-1)*100; f=f[(f>-95)&(f<1000)]
        piyk=(E.iloc[i+k]/E.iloc[i]-1)*100
        for g in ['dusuk','orta','yuksek']:
            s=f.reindex(q[q==g].index).dropna()
            rows.append(dict(tarih=t.date(),donem='2016-21' if t.year<2022 else '2022-26',ufuk=k,grup=g,med=s.median(),ort=s.clip(upper=300).mean(),arti=(s>0).mean()*100,b30=(s>=30).mean()*100,n=len(s),piy=piyk))
T=pd.DataFrame(rows); T.to_csv('../faiz/dip_vol.csv',index=False)
pd.set_option('display.width',200)
print(T.pivot_table(index=['tarih','ufuk'],columns='grup',values='med').round(1).join(T.drop_duplicates(['tarih','ufuk']).set_index(['tarih','ufuk']).piy.round(1)).to_string())
print(); print(T.groupby(['donem','ufuk','grup'])[['med','ort','arti','b30']].mean().round(1).unstack('grup').to_string())
# yuksek - dusuk farki kac olayda arti
P=T.pivot_table(index=['donem','tarih','ufuk'],columns='grup',values='med'); P['fark']=P['yuksek']-P['dusuk']
print(); print(P.groupby(['donem','ufuk']).fark.agg(['mean',lambda x:(x>0).sum(),'size']).round(1).to_string())
