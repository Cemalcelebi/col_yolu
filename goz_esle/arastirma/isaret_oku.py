# Isaretli PDF'i oku: temiz PDF ile piksel farki, kutu icindeki murekkep -> EVET / HAYIR / BOS. Kullanim: python3 isaret_oku.py temiz.pdf isaretli.pdf yerlesim.json cikti.csv
import sys, json, subprocess, numpy as np, pandas as pd, tempfile, os
from PIL import Image
temiz,isaretli,yer_p,cikti=sys.argv[1:5]
yer=json.load(open(yer_p)); DPI=100
def sayfalar(pdf, d):
    subprocess.run(['pdftoppm','-r',str(DPI),'-png',pdf,os.path.join(d,'p')],check=True)
    f=sorted(os.listdir(d)); return {i+1:np.asarray(Image.open(os.path.join(d,x)).convert('L'),dtype=np.int16) for i,x in enumerate(f)}
with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
    T=sayfalar(temiz,d1); M=sayfalar(isaretli,d2)
def murekkep(t,m,kutu):
    h,w=t.shape; x0,y0,bw,bh=kutu
    # figur koordinati (sol-alt) -> piksel (sol-ust); kenarliklari atlamak icin %8 icerden
    X0=int((x0+0.08*bw)*w); X1=int((x0+0.92*bw)*w); Y0=int((1-(y0+0.92*bh))*h); Y1=int((1-(y0+0.08*bh))*h)
    a=t[Y0:Y1,X0:X1]; b=m[Y0:Y1,X0:X1]
    if a.shape!=b.shape: return np.nan
    return float(np.mean(np.abs(a-b)>40))
rows=[]
for y in yer:
    t=T.get(y['sayfa']); m=M.get(y['sayfa'])
    if t is None or m is None or t.shape!=m.shape: rows.append(dict(kid=y['kid'],sembol=y['sembol'],sinyal=y['sinyal'],benim=y['karar'],evet=np.nan,hayir=np.nan,cizim=np.nan,cemal='OKUNAMADI')); continue
    e=murekkep(t,m,y['evet']); hh=murekkep(t,m,y['hayir']); c=murekkep(t,m,y['ax']); n=murekkep(t,m,y['notk'])
    if n>0.002:
        h,w=m.shape; x0,y0,bw,bh=y['notk']; os.makedirs('notlar',exist_ok=True)
        Image.fromarray(m[int((1-(y0+bh))*h):int((1-y0)*h), int(x0*w):int((x0+bw)*w)].astype(np.uint8)).save(f"notlar/not_{y['kid']}_{y['sembol']}.png")
    ESIK=0.004
    karar='EVET' if (e>ESIK and e>hh*1.5) else ('HAYIR' if (hh>ESIK and hh>e*1.5) else ('IKISI' if (e>ESIK and hh>ESIK) else 'BOS'))
    rows.append(dict(kid=y['kid'],sembol=y['sembol'],sinyal=y['sinyal'],benim=y['karar'],evet=round(e,4),hayir=round(hh,4),cizim=round(c,4),notk=round(n,4),cemal=karar))
R=pd.DataFrame(rows); R.to_csv(cikti,index=False)
print(R.cemal.value_counts().to_string()); print(pd.crosstab(R.benim,R.cemal))
