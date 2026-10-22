# Isaretleme PDF'i: sayfa basina 2 grafik, saginda EVET / HAYIR kutulari. Yerlesim sabit (JSON), okuyucu bu yerlesimi kullanir.
import pandas as pd, numpy as np, pickle, json, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages
V=pickle.load(open('bist_2022.pkl','rb'))
s=pd.read_csv('goz_karar_2024_26.csv', index_col=0)
grup=sys.argv[1] if len(sys.argv)>1 else 'COL,SINIR'
cikti=sys.argv[2] if len(sys.argv)>2 else 'COL_ISARET.pdf'
sec=pd.concat([s[s.karar==k] for k in grup.split(',')])
W,H=8.5,11
SLOT=[dict(ax=[0.06,0.60,0.70,0.32], evet=[0.80,0.77,0.16,0.13], hayir=[0.80,0.61,0.16,0.13], notk=[0.06,0.515,0.90,0.065]),
      dict(ax=[0.06,0.12,0.70,0.32], evet=[0.80,0.29,0.16,0.13], hayir=[0.80,0.13,0.16,0.13], notk=[0.06,0.035,0.90,0.065])]
def mum(ax, df, a, b, d, e, dip, tav):
    x=np.arange(a,b); o=df.Open.values[a:b]; h=df.High.values[a:b]; l=df.Low.values[a:b]; c=df.Close.values[a:b]
    up=c>=o
    ax.vlines(x,l,h,color='k',lw=0.7)
    ax.bar(x[up],(c-o)[up],bottom=o[up],width=0.7,color='w',edgecolor='k',lw=0.7)
    ax.bar(x[~up],(o-c)[~up],bottom=c[~up],width=0.7,color='k')
    ax.add_patch(Rectangle((d-0.5,dip),e-d+1,tav-dip,fill=False,ec='tab:red',lw=1.6))
    ax.axvline(e,color='tab:blue',lw=0.9,ls='--'); ax.set_xlim(a-1,b); ax.set_xticks([])
yer=[]
with PdfPages(cikti) as pdf:
    fig=plt.figure(figsize=(W,H))
    fig.text(0.07,0.93,'ÇÖL İŞARETLEME',fontsize=20,weight='bold')
    fig.text(0.07,0.88,"Her grafiğin sağında iki kutu var. Gerçek çölse EVET kutusunun içine, değilse HAYIR kutusunun içine\n"
             "herhangi bir işaret koy (tik, çarpı, karalama, renk fark etmez). Kararsızsan ikisini de boş bırak.\n"
             "Altındaki NOT kutusuna istersen bir iki kelime yaz (ör. \"tepede sıkışma\", \"dip kırıldı\"); notları ben okurum.\n"
             "Grafiğin üstüne de çizebilirsin (ör. gerçek çöl bölgesini), ama makine yalnız EVET/HAYIR kutularını okur.\n"
             "Kırmızı kutu = kodun bulduğu kutu, mavi kesik çizgi = sinyal günü, sağındaki 40 bar sonrası.\n"
             f"Bu dosyada {len(sec)} grafik var (benim ÇÖL dediğim {int((sec.karar=='COL').sum())} + SINIR dediğim {int((sec.karar=='SINIR').sum())}).\n"
             "Bitince dosyayı kaydedip sohbete gönder.",fontsize=10,va='top')
    pdf.savefig(fig); plt.close(fig)
    sayfa=1
    for g in range(0,len(sec),2):
        fig=plt.figure(figsize=(W,H)); sayfa+=1
        for j,r in enumerate(sec.iloc[g:g+2].itertuples()):
            sl=SLOT[j]; ax=fig.add_axes(sl['ax']); df=V[r.sembol]; a=max(0,r.d-130); b=min(len(df),r.e+41)
            mum(ax,df,a,b,r.d,r.e,r.dip,r.tavan)
            ax.set_title(f"#{r.Index}  {r.sembol}  {r.sinyal}   kutu {r.bar} bar, yük %{r.yuk*100:.0f}",fontsize=12,loc='left')
            for ad,k in (('EVET','evet'),('HAYIR','hayir')):
                x0,y0,w,h=sl[k]
                fig.patches.append(Rectangle((x0,y0),w,h,transform=fig.transFigure,fill=False,ec='k',lw=1.5))
                fig.text(x0+w/2,y0+h+0.01,ad,ha='center',va='bottom',fontsize=12,weight='bold')
            x0,y0,w,h=sl['notk']
            fig.patches.append(Rectangle((x0,y0),w,h,transform=fig.transFigure,fill=False,ec='0.5',lw=1.0))
            fig.text(x0+0.005,y0+h-0.004,'NOT (istersen: neden değil / neden evet)',ha='left',va='top',fontsize=8,color='0.4')
            yer.append(dict(kid=int(r.Index),sembol=r.sembol,sinyal=str(r.sinyal),karar=r.karar,sayfa=sayfa,evet=sl['evet'],hayir=sl['hayir'],ax=sl['ax'],notk=sl['notk']))
        fig.text(0.5,0.012,f"sayfa {sayfa}",ha='center',fontsize=7)
        pdf.savefig(fig,dpi=72); plt.close(fig)
json.dump(yer,open(cikti.replace('.pdf','_yerlesim.json'),'w'))
print(cikti, len(sec),'grafik', sayfa,'sayfa')
