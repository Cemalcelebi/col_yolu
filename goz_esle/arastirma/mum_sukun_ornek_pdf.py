# MUM_SUKUN ornekleri: ABD, 3 mum govde, hissenin kendi gecmisinin en sakin %2'si (ANGX bugun %0,8). Rastgele, secim yok.
import pandas as pd, numpy as np, pickle
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
V=pickle.load(open('../goz/abd_2015.pkl','rb'))
O=pd.read_csv('/home/user/col_yolu/arastirma_cikti/mum_sukun/mum_sukun_olaylar.csv.gz', parse_dates=['tarih'])
S=O[(O.pazar=='ABD')&(O.k==3)&(O.olcu=='govde')&(O.varyant=='p02')&O.once_yukari.notna()&O.r60.notna()]
T=O[(O.pazar=='ABD')&(O.k==3)&(O.olcu=='govde')&(O.varyant=='taban')&O.once_yukari.notna()]
n_up=int(round(30*S.once_yukari.mean()))
orn=pd.concat([S[S.once_yukari==1].sample(n_up,random_state=11), S[S.once_yukari==0].sample(30-n_up,random_state=11)]).sort_values('tarih').reset_index(drop=True)
YESIL,KIRMIZI='#1a9e5c','#d9412b'
def ciz(ax, d, i, baslik, sonra=60, once=120, k=3):
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
with PdfPages('MUM_SUKUN_ABD_ornek.pdf') as pdf:
    fig=plt.figure(figsize=(8.5,11))
    sk=orn.once_yukari.mean()*100; tum=S.once_yukari.mean()*100; tb=T.once_yukari.mean()*100
    txt=["MUM SÜKUNETİ — AMERİKA ÖRNEKLERİ","",
         "Seçim: ABD hissesi, 60 günlük tepesinden en az %20 aşağıda ve dibe yakın;",
         "son 3 mumun gövdesi, hissenin KENDİ önceki 250 gününün en sakin %2'sinde.",
         "ANGX bugün bu durumda (kendi geçmişinin %0,8'inde).","",
         f"Aşağıdaki 30 örnek rastgele seçildi; iyi/kötü sonuç oranı bütün sinyallerdeki orana eşitlendi.",
         "(İlk denemede saf rastgele 30 örnek %23 çıktı, bütünü temsil etmiyordu.)",
         "Hisse adları grafikte yok; sonda anahtar tablo var.","",
         "Grafikte: sarı bant = sakin 3 mum, mavi kesik çizgi = sinyal günü,",
         "yeşil noktalı = +%20, kırmızı noktalı = −%10. Sinyalden sonra 60 gün görünüyor.","",
         f"Bu 30 örnekte önce +%20 gelen: %{sk:.0f}",
         f"Bütün ABD sinyallerinde (n {len(S)}): %{tum:.0f}",
         f"Aynı durumda normal boy mumlu günlerde (taban, n {len(T)}): %{tb:.0f}"]
    fig.text(0.07,0.93,"\n".join(txt),fontsize=11,va='top')
    ax=fig.add_axes([0.07,0.08,0.86,0.38])
    a=V['ANGX']; ciz(ax,a,len(a)-1,"ANGX bugün (22 Eki 2026): sarı bant = son 3 mum, sonrası henüz yok",sonra=0)
    pdf.savefig(fig); plt.close(fig)
    for g in range(0,len(orn),2):
        fig,axs=plt.subplots(2,1,figsize=(8.5,11))
        for j,r in enumerate(orn.iloc[g:g+2].itertuples()):
            d=V[r.sembol]; i=d.index.get_indexer([r.tarih])[0]
            snc='önce +%20 geldi' if r.once_yukari==1 else 'önce −%10 geldi'
            ciz(axs[j],d,i,f"Örnek {r.Index+1} · {r.tarih.date()} · {snc} · 60 gün sonra {r.r60:+.0f}% · mumlar normalinin {r.oran:.2f} katı")
        plt.tight_layout(pad=2); pdf.savefig(fig,dpi=70); plt.close(fig)
    fig=plt.figure(figsize=(8.5,11)); fig.text(0.07,0.95,"ANAHTAR",fontsize=13,weight='bold',va='top')
    sat=[f"{r.Index+1:>2}  {r.sembol:<6} {r.tarih.date()}  {'+%20' if r.once_yukari==1 else '−%10'}  60g {r.r60:+6.1f}%" for r in orn.itertuples()]
    fig.text(0.07,0.91,"\n".join(sat),fontsize=10,va='top',family='monospace'); pdf.savefig(fig); plt.close(fig)
print('ornek once+20 %', round(orn.once_yukari.mean()*100), 'tum', round(S.once_yukari.mean()*100), 'taban', round(T.once_yukari.mean()*100), 'n', len(S), len(T))
print(orn[['sembol','tarih','once_yukari','r60','oran']].round(2).to_string())
