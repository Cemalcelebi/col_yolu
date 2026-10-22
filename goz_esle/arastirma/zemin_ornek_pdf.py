# ZEMIN ornekleri (MUM_SUKUN v1.2 z_siki k=5): ABD, 3 mum govde, hissenin kendi gecmisinin en sakin %2'si (ANGX bugun %0,8). Rastgele, secim yok.
import pandas as pd, numpy as np, pickle
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
V=pickle.load(open(__import__('sys').argv[1] if len(__import__('sys').argv)>1 else '../goz/abd_2015.pkl','rb'))
O=pd.read_csv('/home/user/col_yolu/arastirma_cikti/mum_sukun/zemin_olaylar.csv.gz', parse_dates=['tarih'])
S=O[(O.pazar=='ABD')&(O.k==5)&(O.varyant=='z_siki')&O.once_yukari.notna()&O.r60.notna()]
T=O[(O.pazar=='ABD')&(O.k==5)&(O.varyant=='taban')&O.once_yukari.notna()]
N=24; n_up=int(round(N*S.once_yukari.mean()))
orn=pd.concat([S[S.once_yukari==1].sample(n_up,random_state=11), S[S.once_yukari==0].sample(N-n_up,random_state=11)]).sort_values('tarih').reset_index(drop=True)
YESIL,KIRMIZI='#1a9e5c','#d9412b'
def ciz(ax, d, i, baslik, sonra=60, once=50, k=5):
    a=max(0,i-once); b=min(len(d),i+sonra+1); x=np.arange(a,b)
    o,h,l,c=(d[x_].to_numpy()[a:b] for x_ in ('Open','High','Low','Close'))
    up=c>=o; col=np.where(up,YESIL,KIRMIZI)
    ax.vlines(x,l,h,color=col,lw=0.7)
    ax.bar(x,np.where(np.abs(c-o)<1e-9,(h-l)*0.01,c-o),bottom=o,width=0.7,color=col)
    ax.axvspan(i-k+0.5,i+0.5,color='#f2c94c',alpha=0.35,lw=0)
    ax.axvline(i,color='#3b6fb6',lw=0.9,ls='--')
    p=d.Close.iat[i]
    if sonra>0:
        ax.axhline(p*1.2,color=YESIL,lw=0.7,ls=':'); ax.axhline(p*0.9,color=KIRMIZI,lw=0.7,ls=':')
    ax.set_xlim(a-1,b+1); ax.set_xticks([]); ax.tick_params(labelsize=7)
    for sp in ('top','right'): ax.spines[sp].set_visible(False)
    ax.set_title(baslik,fontsize=9,loc='left')

with PdfPages('ZEMIN_ABD_ornek.pdf') as pdf:
    fig=plt.figure(figsize=(8.5,11))
    sk=orn.once_yukari.mean()*100; tum=S.once_yukari.mean()*100; tb=T.once_yukari.mean()*100
    txt=["ZEMİNE YAPIŞAN SIRA — AMERİKA ÖRNEKLERİ","",
         "Seçim: sert düşüş (10 günde en az %12, önceki 5 mum hissenin normalinden",
         "en az 1,3 kat büyük), ardından 60 günün dibinde 5 mumluk sıra:",
         " · 5 mumun toplam bandı en fazla 2 normal mum boyu",
         " · dipler hizalı (en yüksek dip − en düşük dip ≤ 0,5 normal mum)",
         " · mumlar arası açılış boşluğu ≤ 0,4 normal mum",
         " · sıra boyunca kayma ≤ 0,7 normal mum",
         "Normal mum = hissenin KENDİ önceki 250 gününün medyan H−L boyu.","",
         f"24 örnek rastgele; iyi/kötü oranı bütün sinyallerdeki orana eşitlendi.",
         "Hisse adları grafikte yok; sonda anahtar tablo var.",
         "Sarı bant = 5 mumluk sıra, mavi kesik = sinyal günü,",
         "yeşil noktalı = +%20, kırmızı noktalı = −%10. Sonrası 60 gün.","",
         f"Bütün ABD sinyallerinde (n {len(S)}) önce +%20 gelen: %{tum:.0f}",
         f"Aynı sert düşüşte sıra dağınıksa (taban, n {len(T)}): %{tb:.0f}"]
    fig.text(0.07,0.95,"\n".join(txt),fontsize=10.5,va='top')
    ax=fig.add_axes([0.07,0.07,0.86,0.36])
    a=V['ANGX']; ciz(ax,a,len(a)-1,"ANGX bugün: son 4 mum düz zemin şeklinde (dipler hizalı, boşluk yok). Ama düşüşteki mumlar\nnormalinin 1,1 katı; 'sert çarpma' eşiği 1,3 olduğu için sinyal sayılmadı.",sonra=0,k=4)
    pdf.savefig(fig); plt.close(fig)
    for g in range(0,len(orn),3):
        fig,axs=plt.subplots(3,1,figsize=(8.5,11))
        for j,r in enumerate(orn.iloc[g:g+3].itertuples()):
            d=V[r.sembol]; i=d.index.get_indexer([r.tarih])[0]
            snc='önce +%20' if r.once_yukari==1 else 'önce −%10'
            ciz(axs[j],d,i,f"Örnek {r.Index+1} · {r.tarih.date()} · {snc} · 60 gün sonra {r.r60:+.0f}%")
        plt.tight_layout(pad=1.5); pdf.savefig(fig,dpi=70); plt.close(fig)
    fig=plt.figure(figsize=(8.5,11)); fig.text(0.07,0.95,"ANAHTAR",fontsize=13,weight='bold',va='top')
    sat=[f"{r.Index+1:>2}  {r.sembol:<6} {r.tarih.date()}  {'+%20' if r.once_yukari==1 else '−%10'}  60g {r.r60:+6.1f}%" for r in orn.itertuples()]
    fig.text(0.07,0.91,"\n".join(sat),fontsize=10,va='top',family='monospace'); pdf.savefig(fig); plt.close(fig)
print('ornek', round(orn.once_yukari.mean()*100), 'tum', round(S.once_yukari.mean()*100), 'taban', round(T.once_yukari.mean()*100), len(S), len(T))
