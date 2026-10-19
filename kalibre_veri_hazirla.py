# ===== KALIBRE VERI — Colab'da tek hucre. 24 hissenin OHLCV'sini kucuk CSV'ye yazar (2026-09-18)
import os, pickle, pandas as pd
if not os.path.exists('/content/drive/MyDrive'):
    from google.colab import drive; drive.mount('/content/drive')
K='/content/drive/MyDrive/col_tarayici'
V=pickle.load(open(f'{K}/veri_1d_turkey.pkl','rb'))
V=V['veri'] if isinstance(V,dict) and 'veri' in V else V
S=['TEHOL','INVES','BURVA','EYGYO','BASCM','SEYKM','GEDZA','SUNTK','HDFGS','INFO','KATMR','OTTO',
   'TUKAS','ORCAY','TATGD','EUREN','VRGYO','VESTL','ARZUM','EMNIS','SKTAS','SMRTG','ODAS']
R=[]; yok=[]
for s in S:
    k=s if s in V else next((x for x in V if x.split('.')[0]==s),None)
    if k is None: yok.append(s); continue
    d=V[k][V[k].index>=pd.Timestamp('2024-01-01')][['Open','High','Low','Close','Volume']].copy()
    d.insert(0,'sembol',s); d.index.name='tarih'; R.append(d.reset_index())
t=pd.concat(R,ignore_index=True); t.to_csv(f'{K}/kalibre_veri.csv',index=False)
print(f"{t.sembol.nunique()} hisse, {len(t)} satir -> kalibre_veri.csv | yok: {yok}")
