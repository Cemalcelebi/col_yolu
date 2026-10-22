# TCMB PPK karar gunleri: sektor ve borcluluk gruplarinin piyasaya gore tepkisi. BIST 2022-06 -> 2026-10-21.
import pickle, numpy as np, pandas as pd, sys
V=pickle.load(open('../goz/bist_2022.pkl','rb'))
sek=pd.read_csv('/home/user/col_yolu/sektor_BIST.csv').set_index('sembol')
tem=pd.read_csv('/home/user/col_yolu/temel_duz.csv', parse_dates=['aciklama'])
C=pd.DataFrame({s:d.Close for s,d in V.items()}).sort_index()
OLAY={
 'indirim_2022-23':['2022-08-18','2022-09-22','2022-10-20','2022-11-24','2023-02-23'],
 'indirim_2024-26':['2024-12-26','2025-01-23','2025-03-06','2025-07-24','2025-09-11','2025-10-23','2025-12-11','2026-01-22'],
 'sabit_2024-26':['2024-04-25','2024-06-27','2024-07-23','2024-08-20','2024-09-19','2024-10-17','2024-11-21','2025-06-19','2026-03-12','2026-04-22','2026-06-11','2026-07-23','2026-09-10'],
 'artirim_2023-25':['2023-06-22','2023-07-20','2023-08-24','2023-09-21','2023-10-26','2023-11-23','2023-12-21','2024-01-25','2024-03-21','2025-04-17'],
}
def borc_grup(s, D):
    t=tem[(tem.sembol==s)&(tem.aciklama<D)]
    if t.empty or pd.isna(t.iloc[-1].borc_oz): return 'veri yok'
    b=t.iloc[-1].borc_oz
    return 'net nakit' if b<0 else ('az borclu' if b<0.5 else 'borclu (>=0.5)')
rows=[]
for tur,tl in OLAY.items():
    for ds in tl:
        D=pd.Timestamp(ds); i=C.index.searchsorted(D)
        if i>=len(C) or C.index[i]!=D: print('tarih yok',ds,file=sys.stderr); continue
        for k,ad in ((0,'r0'),(5,'r5'),(20,'r20')):
            if i+k>=len(C): continue
            r=C.iloc[i+k]/C.iloc[i-1]-1; r=r.dropna(); r=r[(r>-0.6)&(r<1.5)]
            rel=(r-r.median())*100
            for s,v in rel.items():
                rows.append(dict(tur=tur,tarih=ds,ufuk=ad,sembol=s,rel=v,piy=r.median()*100,endeks=sek.endeks.get(s,'?')))
T=pd.DataFrame(rows)
T['borc']=[borc_grup(s,pd.Timestamp(d)) if u=='r0' else None for s,d,u in zip(T.sembol,T.tarih,T.ufuk)]
bmap=T[T.ufuk=='r0'].set_index(['tarih','sembol']).borc
T['borc']=[bmap.get((d,s)) for d,s in zip(T.tarih,T.sembol)]
T.to_csv('faiz_olay_satir.csv.gz',index=False)
print('piyasa medyani (gun, 5g, 20g):'); print(T.groupby(['tur','ufuk']).piy.first().unstack().round(2) if False else T.drop_duplicates(['tur','tarih','ufuk']).groupby(['tur','ufuk']).piy.mean().unstack().round(2))
def ozet(by):
    g=T.groupby(['tur','tarih','ufuk',by]).rel.median().reset_index()
    a=g.groupby([by,'tur','ufuk']).rel.agg(['mean',lambda x:(x>0).mean()*100,'size']).round(2)
    a.columns=['ort','arti%','n']; return a
S=ozet('endeks'); B=ozet('borc')
S.to_csv('faiz_sektor.csv'); B.to_csv('faiz_borc.csv')
p=S['ort'].unstack(['tur','ufuk'])
cols=[('indirim_2022-23','r0'),('indirim_2024-26','r0'),('indirim_2022-23','r5'),('indirim_2024-26','r5'),('indirim_2024-26','r20'),('sabit_2024-26','r0'),('artirim_2023-25','r0')]
p=p[[c for c in cols if c in p.columns]]
n=T.drop_duplicates('sembol').groupby('endeks').size()
p['hisse']=n
ar=S['arti%'].unstack(['tur','ufuk'])[('indirim_2024-26','r0')]
p['24-26 gun arti%']=ar
p=p[p.hisse>=4].sort_values(('indirim_2024-26','r0'),ascending=False)
pd.set_option('display.width',250); print(p.round(2).to_string())
print(); print(B['ort'].unstack(['tur','ufuk'])[[c for c in cols if c in B['ort'].unstack(['tur','ufuk']).columns]].round(2).to_string())
