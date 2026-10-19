# =====================================================================
#  TEMEL VERI — Is Yatirim finansallari (bist_finansal_veriler_2022_2026.xlsx)
#  Uzun format (kalem x donem x sembol) -> hisse x ceyrek duz tablo
#  Gelir tablosu KUMULATIF -> ceyrege ayrilir. Bilanco anlik.
#  Aciklama gecikmesi: Q1/Q2/Q3 +50 gun, Q4 +70 gun (sizinti korumasi)
#  Olculer: net_kar_ttm_buyume, satis_ttm_buyume, roe, net_borc/ozkaynak
#
#  2026-09-18 DUZELTME (denetim D-borc):
#    ozkaynak <= 0 iken borc_oz = net_borc/ozkaynak NEGATIF cikiyordu ve
#    "net nakit" sayilip 1.5x aliyordu (en kotu bilanco en iyi sinifa).
#    Simdi: ozkaynak<=0 -> borc_oz = NaN, oz_negatif = 1 -> carpan 0.7.
#    temel_duz.csv'de 'oz_negatif' sutunu yoksa BASLAT yeniden hesaplar.
# =====================================================================
import numpy as np, pandas as pd, os, logging
_K='/content/drive/MyDrive/col_tarayici'
log=logging.getLogger('col.temel')
TEMEL_SUTUNLAR=['sembol','donem','yil','q','aciklama','net_kar_q','satis_q','ozkaynak','fin_borc','nakit',
                'nk_ttm','st_ttm','nk_buyume','st_buyume','roe','net_borc','borc_oz','oz_negatif','nk_pozitif']

def temel_yukle(dosya='bist_finansal_veriler_2022_2026.xlsx', zorla=False):
    y=f'{_K}/temel_duz.csv'
    if os.path.exists(y) and not zorla:
        try:
            t=pd.read_csv(y,parse_dates=['aciklama'])
            if 'oz_negatif' in t.columns:
                print(f"  temel: {len(t)} satir, {t.sembol.nunique()} hisse (onbellek)"); return t
            print("  temel: eski format (oz_negatif yok) -> yeniden hesaplaniyor")
        except Exception as e:
            log.warning(f'temel_duz.csv okunamadi ({e}), yeniden hesaplaniyor')
    xl=f'{_K}/{dosya}'
    if not os.path.exists(xl): raise FileNotFoundError(f'temel: {xl} yok')
    F=pd.read_excel(xl)
    ad='FINANCIAL_ITEM_NAME_TR'; donemler=[c for c in F.columns if '/' in str(c)]
    def kalem(g, isimler, topla=False):
        for isim in isimler:
            m=g[g[ad].astype(str).str.strip().str.upper()==isim.upper()]
            if len(m): return m[donemler].apply(pd.to_numeric,errors='coerce').sum() if topla else m[donemler].iloc[0].apply(pd.to_numeric,errors='coerce')
        for isim in isimler:
            m=g[g[ad].astype(str).str.contains(isim,case=False,na=False,regex=False)]
            if len(m): return m[donemler].iloc[0].apply(pd.to_numeric,errors='coerce')
        return pd.Series(np.nan,index=donemler)
    R=[]
    for s,g in F.groupby('SYMBOL'):
        nk=kalem(g,['DÖNEM KARI (ZARARI)','NET DÖNEM KARI/ZARARI','Dönem Karı (Zararı)'])
        st=kalem(g,['Satış Gelirleri','Hasılat'])
        oz=kalem(g,['Özkaynaklar'])
        fb=kalem(g,['Finansal Borçlar'],topla=True)
        nk_=kalem(g,['Nakit ve Nakit Benzerleri'])
        for dn in donemler:
            try:
                yil,ay=dn.split('/'); yil=int(yil); q=int(ay)//3
            except Exception: continue
            onc=f"{yil}/{int(ay)-3}" if q>1 else None
            nkq=nk[dn]-(nk[onc] if (onc and onc in nk.index) else 0) if q>1 else nk[dn]
            stq=st[dn]-(st[onc] if (onc and onc in st.index) else 0) if q>1 else st[dn]
            gec=50 if q<4 else 70
            if q<4: acik=pd.Timestamp(year=yil,month=3*q+1,day=1)+pd.Timedelta(days=gec)
            else:   acik=pd.Timestamp(year=yil+1,month=1,day=1)+pd.Timedelta(days=gec)
            R.append({'sembol':s,'donem':dn,'yil':yil,'q':q,'aciklama':acik,'net_kar_q':nkq,'satis_q':stq,
                      'ozkaynak':oz[dn],'fin_borc':fb[dn],'nakit':nk_[dn]})
    t=pd.DataFrame(R).sort_values(['sembol','yil','q']).reset_index(drop=True)
    t['nk_ttm']=t.groupby('sembol').net_kar_q.transform(lambda v: v.rolling(4).sum())
    t['st_ttm']=t.groupby('sembol').satis_q.transform(lambda v: v.rolling(4).sum())
    t['nk_buyume']=t.groupby('sembol').nk_ttm.transform(lambda v: (v/v.shift(4).abs()-1)*100)
    t['st_buyume']=t.groupby('sembol').st_ttm.transform(lambda v: (v/v.shift(4).abs()-1)*100)
    t['roe']=t.nk_ttm/t.ozkaynak.where(t.ozkaynak>0)*100          # ozkaynak<=0 -> NaN
    t['net_borc']=t.fin_borc-t.nakit
    t['oz_negatif']=(t.ozkaynak<=0).astype(int)                       # D-borc
    t['borc_oz']=t.net_borc/t.ozkaynak.where(t.ozkaynak>0)            # ozkaynak<=0 -> NaN
    t['nk_pozitif']=(t.nk_ttm>0).astype(int)
    t.to_csv(y,index=False)
    print(f"  temel: {len(t)} satir, {t.sembol.nunique()} hisse (hesaplandi+kaydedildi) | oz_negatif {int(t.oz_negatif.sum())} satir")
    return t

def temel_esle(dd, t):
    dd=dd.copy(); dd['t']=pd.to_datetime(dd.tarih); kol=['nk_buyume','st_buyume','roe','borc_oz','oz_negatif','nk_pozitif','donem']
    out=[]
    for r in dd.itertuples():
        g=t[(t.sembol==r.sembol)&(t.aciklama<=r.t)]
        out.append(g.iloc[-1][kol].to_dict() if len(g) else {k:np.nan for k in kol})
    for k in kol: dd[k]=[o[k] for o in out]
    return dd

def temel_test(setler, t=None, veri=None, ufuk=250, hedef=20, ma=20, maliyet=0.4):
    t=t if t is not None else temel_yukle(); veri=veri if veri is not None else VERI
    for ad,dd in setler:
        z=temel_esle(dd,t); R=[]
        for r in z.itertuples():
            df=veri.get(r.sembol)
            if df is None: continue
            T=r.t; x=df[df.index<=T]; s=col_segment(x)
            if not s: continue
            il=df[df.index>T].head(ufuk)
            if len(il)<30: continue
            C=il.Close.to_numpy(float); H=il.High.to_numpy(float)
            kb=next((j for j,c in enumerate(C) if c>s['tavan']*AL_PAY),None)
            if kb is None or kb>len(C)-25: continue
            gp=float(C[kb]); s20=pd.concat([x.Close,il.Close]).rolling(ma).mean().to_numpy(float)[-len(il):]
            m=H[kb+1:]>=gp*(1+hedef/100)
            if m.any():
                jh=int(np.argmax(m))+kb+1; alt=np.where(C[jh+1:]<s20[jh+1:])[0]; jt=int(alt[0])+jh+1 if len(alt) else len(C)-1
            else: jt=len(C)-1
            R.append({'g':(C[jt]/gp-1)*100-maliyet,'nk_buyume':r.nk_buyume,'st_buyume':r.st_buyume,'roe':r.roe,'borc_oz':r.borc_oz,'oz_negatif':r.oz_negatif,'nk_pozitif':r.nk_pozitif})
        q=pd.DataFrame(R)
        if q.empty: print(f"\n === {ad}: kayit yok ==="); continue
        print(f"\n === {ad} n={len(q)} (temel verisi olan {int(q.roe.notna().sum())}) | taban kazanan %{100*(q.g>0).mean():.0f} bekl %{bek(q.g):+.1f} ===")
        print(f"  {'olcu':12s} {'dilim':>10s} {'aralik':>18s} {'n':>5s} {'kazanan':>8s} {'bekl':>7s} {'agir%':>6s}")
        for k in ['nk_buyume','st_buyume','roe','borc_oz']:
            v=q[k].replace([np.inf,-np.inf],np.nan).dropna()
            if len(v)<60: continue
            qq=v.quantile([0.33,0.67]).values
            for et,m in [('dusuk 1/3',q[k]<qq[0]),('orta 1/3',(q[k]>=qq[0])&(q[k]<qq[1])),('yuksek 1/3',q[k]>=qq[1])]:
                s_=q[m]
                if len(s_)>=20: print(f"  {k:12s} {et:>10s} {s_[k].min():8.1f}..{s_[k].max():8.1f} {len(s_):5d} {100*(s_.g>0).mean():7.0f}% {bek(s_.g):+6.1f}% {100*(s_.g<-20).mean():5.1f}%")
            print()
        for et,m in [('nk_ttm ZARAR',q.nk_pozitif==0),('nk_ttm KAR',q.nk_pozitif==1),('OZ NEGATIF',q.oz_negatif==1)]:
            s_=q[m]
            if len(s_)>=10: print(f"  {'sinif':12s} {et:>12s} {'':>16s} {len(s_):5d} {100*(s_.g>0).mean():7.0f}% {bek(s_.g):+6.1f}% {100*(s_.g<-20).mean():5.1f}%")

print("[ok] temel yuklendi (2026-09-18: oz_negatif)")
print("   t = temel_yukle()   <- ilk sefer 1-2 dk, sonra onbellek")
print("   temel_test([('BIST 2024-26', d[d.GECER]), ('BIST 2023', d23)], t)")
