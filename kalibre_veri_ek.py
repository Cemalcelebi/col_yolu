# ===== KALIBRE VERI EK — istenen hisseleri kalibre_veri.csv'ye ekler (2026-09-18)
#  Kullanim: S=['BINBN','PAPIL','ESCAR','PEKER']; exec(open('/content/drive/MyDrive/col_tarayici/kalibre_veri_ek.py').read())
import os, pickle, pandas as pd
if not os.path.exists('/content/drive/MyDrive'):
    from google.colab import drive; drive.mount('/content/drive')
K='/content/drive/MyDrive/col_tarayici'
V=pickle.load(open(f'{K}/veri_1d_turkey.pkl','rb'))
V=V['veri'] if isinstance(V,dict) and 'veri' in V else V
S=globals().get('S',['BINBN','PAPIL','ESCAR','PEKER'])
y=f'{K}/kalibre_veri.csv'
eski=pd.read_csv(y,parse_dates=['tarih']) if os.path.exists(y) else pd.DataFrame(columns=['tarih','sembol','Open','High','Low','Close','Volume'])
R=[]; yok=[]
for s in S:
    k=s if s in V else next((x for x in V if x.split('.')[0]==s),None)
    if k is None: yok.append(s); continue
    d=V[k][V[k].index>=pd.Timestamp('2024-01-01')][['Open','High','Low','Close','Volume']].copy()
    d.insert(0,'sembol',s); d.index.name='tarih'; R.append(d.reset_index())
t=pd.concat([eski[~eski.sembol.isin(S)]]+R,ignore_index=True).sort_values(['sembol','tarih'])
t.to_csv(y,index=False)
print(f"{t.sembol.nunique()} hisse, {len(t)} satir -> kalibre_veri.csv | eklenen: {[s for s in S if s not in yok]} | yok: {yok}")
