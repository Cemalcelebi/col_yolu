# =====================================================================
#  DENETIM — Col Yolu sisteminin gercekci olcumu   (2026-09-22)
#
#  Duzeltmeler:
#   1) TEKILLESTIRME : (sembol, kirilim gunu) bir kez sayilir (2 haftalik ornekleme tekrarlari atilir)
#   2) H=L / LIKIDITE: segmentte H==L veya hacim=0 bar orani >%20 ya da medyan TL hacim < esik -> dislanir
#                      doji/fitil sadece H>L & V>0 barlarla yeniden hesaplanir
#   3) GIRIS         : 'kapanis' (kirilim kapanisi) vs 'acilis' (ertesi gun acilisi — gercekci)
#   4) PORTFOY SIM   : tek model, gunluk ozsermaye egrisi, nakit siniri, pozisyon basi max %12
#                      boyut: 'esit' | 'carpan' (doji x fitil x kural) | 'atr' (oynakliga ters)
#                      istege bagli KUME SINIRI: acik pozisyonlarla 60g korelasyon>0.6 olan 3+ varsa girme
#   5) KIYAS         : ayni tarihlerde XU100 ve mevduat (%40/yil), max drawdown, CAGR
#   6) VERI KONTROL  : veri_yenile ek-yama bolunme/temettu kaymasi (son 15 gun yf vs VERI)
#   7) ESKI DONEM    : 2018-2022 (ayi + 2020 cokusu) icin onbellek kur ve ayni denetim
#
#  Kullanim (BASLAT sonrasi):
#    exec(open(f'{K}/DENETIM.py').read())
#    denetim(OB24,'BIST 24-26',VERI,xu)
#    denetim(OB23,'BIST 2023',VERI,xu)
#    veri_kontrol(VERI)                         # bolunme/duzeltme kaymasi
#    OBE=eski_donem_kur()                        # ~25-40 dk, bir kez; sonra:
#    denetim(OBE,'BIST 2018-22',VERI,xu)
#  SADECE OKUR. Yazdigi tek dosya: onbellek_ESKI.pkl ve denetim_*.csv
# =====================================================================
import numpy as np, pandas as pd, time, os, pickle

DN_COST=0.4          # gidis-donus %
DN_HEDEF=20; DN_UFUK=120; DN_MA=20
DN_LIK_TL=1_000_000  # segment medyan gunluk TL hacim alt siniri (BIST)
DN_HL_MAX=0.20       # segmentte H==L veya V==0 bar orani ust siniri
DN_MAX_POZ=12.0      # tek pozisyon max %
DN_MEVDUAT=0.40      # yillik

def _bek(v):
    v=pd.Series(v).dropna()
    if not len(v): return np.nan
    kz=v[v>0].mean() if (v>0).any() else 0; ky=v[v<=0].mean() if (v<=0).any() else 0
    return (v>0).mean()*kz+(v<=0).mean()*ky

def _kirilim(o, en_gec=60):
    tv=np.maximum(o['sO'],o['sC']).max()*1.002; C=o['iC']
    for j in range(min(en_gec,len(C))):
        if C[j]>tv: return j
    return None

def _cikis(o, e, gp):
    """e: giris bar indeksi (iC icinde). %20 -> SMA20 trail, hedefsiz DN_UFUK bar."""
    C,H,s20=o['iC'],o['iH'],o['s20']; son=min(e+DN_UFUK,len(C)-1)
    m=H[e+1:son+1]>=gp*(1+DN_HEDEF/100)
    if m.any():
        jh=int(np.argmax(m))+e+1; alt=np.where(C[jh+1:]<s20[jh+1:])[0]
        return (int(alt[0])+jh+1 if len(alt) else len(C)-1)
    return son

def _temiz_olcu(o):
    O,H,L,C,V=o['sO'],o['sH'],o['sL'],o['sC'],o['sV']
    ok=(H>L)&(V>0); hl_oran=1-ok.mean()
    lik=float(np.median(C*V))
    if ok.sum()<5: return hl_oran,lik,np.nan,np.nan
    a=o['seg']['atr_ref'] or np.nan
    rng=(H-L)[ok]; doji=float((np.abs(C-O)[ok]/rng<0.15).mean())
    fitil=float(((np.minimum(O,C)-L)[ok]/a).mean()) if a and a>0 else np.nan
    return hl_oran,lik,doji,fitil

def islemler(OB, giris='acilis', bist=True):
    """Tekillestirilmis, temizlenmis islem listesi."""
    R=[]; gor=set(); ham=0; dis_hl=0; dis_lik=0; dis_tekrar=0
    for o in OB:
        kb=_kirilim(o)
        if kb is None or kb+2>len(o['iC'])-25: continue
        ham+=1
        kt=pd.Timestamp(o['iT'][kb]).normalize(); key=(o['sembol'],kt)
        if key in gor: dis_tekrar+=1; continue
        gor.add(key)
        hl,lik,doji,fitil=_temiz_olcu(o)
        if hl>DN_HL_MAX: dis_hl+=1; continue
        if bist and lik<DN_LIK_TL: dis_lik+=1; continue
        if giris=='acilis': e=kb+1; gp=float(o['iO'][e])
        else: e=kb; gp=float(o['iC'][kb])
        if not np.isfinite(gp) or gp<=0: continue
        jt=_cikis(o,e,gp); cp=float(o['iC'][jt])
        a=o['seg'].get('atr_ref') or np.nan
        R.append({'sembol':o['sembol'],'giris_t':pd.Timestamp(o['iT'][e]).normalize(),'cikis_t':pd.Timestamp(o['iT'][jt]).normalize(),
                  'gp':gp,'cp':cp,'g':(cp/gp-1)*100-DN_COST,'e':e,'jt':jt,'o':o,
                  'doji':doji,'fitil':fitil,'kural':bool(o.get('GECER',True)),'atr_pct':a/gp*100 if np.isfinite(a) else np.nan})
    q=pd.DataFrame(R)
    bilgi={'ham':ham,'tekrar':dis_tekrar,'hl':dis_hl,'lik':dis_lik,'kalan':len(q)}
    return q,bilgi

def _agirlik(r, mod, med_atr):
    if mod=='esit': return 100/30
    if mod=='carpan':
        dc=1.5 if (np.isfinite(r.doji) and r.doji>=0.23) else (0.7 if (np.isfinite(r.doji) and r.doji<0.13) else 1.0)
        fc=2.5 if (np.isfinite(r.fitil) and r.fitil<0.12) else 1.0
        kc=1.0 if r.kural else 0.7
        return min(4.0*dc*fc*kc, DN_MAX_POZ)
    if mod=='atr':
        if not np.isfinite(r.atr_pct) or r.atr_pct<=0: return 100/30
        return float(np.clip(100/30*med_atr/r.atr_pct, 100/60, DN_MAX_POZ))
    raise ValueError(mod)

def portfoy(q, mod='esit', veri=None, kume=False, kume_esik=0.6, kume_max=3):
    """Gunluk ozsermaye egrisi. Nakit siniri gercek. Donus: egri (Series), islem sayisi, atlanan."""
    if q.empty: return pd.Series(dtype=float),0,0
    med_atr=float(q.atr_pct.median())
    # fiyat yolu: her islem icin tarih->kapanis
    girisler=q.sort_values('giris_t')
    takvim=sorted(set(pd.to_datetime(np.concatenate([r.o['iT'][r.e:r.jt+1] for r in girisler.itertuples()])).normalize()))
    giris_gun={}; [giris_gun.setdefault(r.giris_t,[]).append(r) for r in girisler.itertuples()]
    nakit=100.0; acik=[]; egri={}; alinan=0; atlanan=0; ozs=100.0
    getiri_cache={}
    def _ret(sym, t):
        if veri is None or sym not in veri: return None
        k=(sym,t)
        if k not in getiri_cache:
            df=veri[sym]; x=df.Close[df.index<=t].tail(61)
            getiri_cache[k]=x.pct_change().dropna().to_numpy() if len(x)>=40 else None
        return getiri_cache[k]
    for t in takvim:
        # cikislar
        kal=[]
        for p in acik:
            if p['cikis_t']<=t: nakit+=p['adet']*p['cp']*(1-DN_COST/200)
            else: kal.append(p)
        acik=kal
        # girisler
        for r in giris_gun.get(t,[]):
            if any(p['sembol']==r.sembol for p in acik): continue
            if kume and veri is not None:
                rn=_ret(r.sembol,t)
                if rn is not None:
                    say=0
                    for p in acik:
                        rp=_ret(p['sembol'],t)
                        if rp is not None and len(rp)==len(rn) and np.corrcoef(rn,rp)[0,1]>kume_esik: say+=1
                    if say>=kume_max: atlanan+=1; continue
            w=_agirlik(r,mod,med_atr); tutar=min(ozs*w/100, nakit)
            if tutar<ozs*0.005: atlanan+=1; continue
            nakit-=tutar; alinan+=1
            yol=dict(zip(pd.to_datetime(r.o['iT'][r.e:r.jt+1]).normalize(), r.o['iC'][r.e:r.jt+1]))
            acik.append({'sembol':r.sembol,'adet':tutar*(1-DN_COST/200)/r.gp,'cp':r.cp,'cikis_t':r.cikis_t,'yol':yol,'son':r.gp})
        # degerleme
        deger=0.0
        for p in acik:
            if t in p['yol']: p['son']=p['yol'][t]
            deger+=p['adet']*p['son']
        ozs=nakit+deger; egri[t]=ozs
    return pd.Series(egri).sort_index(), alinan, atlanan

def _ozet_egri(e):
    if len(e)<2: return np.nan,np.nan,np.nan
    yil=max((e.index[-1]-e.index[0]).days/365.25,0.1)
    top=(e.iloc[-1]/e.iloc[0]-1)*100; cagr=((e.iloc[-1]/e.iloc[0])**(1/yil)-1)*100
    dd=((e/e.cummax())-1).min()*100
    return top,cagr,dd

def denetim(OB, ad, veri=None, xu=None, bist=True, kume_test=True):
    t0=time.time()
    print(f"\n{'='*70}\n  DENETIM: {ad}\n{'='*70}")
    # --- islem basi: kapanis vs acilis, tekillestirilmis ---
    for giris in ('kapanis','acilis'):
        q,b=islemler(OB,giris,bist)
        if giris=='kapanis':
            print(f"  ham kirilim {b['ham']} | tekrar atilan {b['tekrar']} | H=L atilan {b['hl']} | likidite atilan {b['lik']} | KALAN {b['kalan']}")
        print(f"  giris={giris:8s} n={len(q):4d} kazanan %{100*(q.g>0).mean():.0f} bekl %{_bek(q.g):+.1f} medyan %{q.g.median():+.1f} agir(<-20) %{100*(q.g<-20).mean():.1f}")
    q,_=islemler(OB,'acilis',bist)
    if q.empty: print("  islem yok"); return
    # fitil n kontrolu (tekillesmis)
    f=q[q.fitil<0.12]; print(f"  fitil<0.12 tekil n={len(f)} bekl %{_bek(f.g):+.1f} | digerleri %{_bek(q[q.fitil>=0.12].g):+.1f}")
    # --- portfoy ---
    bas,son=q.giris_t.min(),q.cikis_t.max()
    xu_top=np.nan
    if xu is not None and len(xu):
        x=xu.Close[(xu.index>=bas)&(xu.index<=son)]
        if len(x)>1: xu_top=(x.iloc[-1]/x.iloc[0]-1)*100
    yil=max((son-bas).days/365.25,0.1); mev_top=((1+DN_MEVDUAT)**yil-1)*100
    print(f"\n  PORTFOY (ertesi gun acilisi giris, nakit sinirli, maliyet %{DN_COST})   donem {bas.date()} -> {son.date()} ({yil:.1f} yil)")
    print(f"  {'boyut':16s} {'islem':>5s} {'atlanan':>7s} {'TOPLAM':>8s} {'YILLIK':>7s} {'MAX DD':>7s}")
    satir=[]
    modlar=[('esit',False),('carpan',False),('atr',False)]
    if kume_test and veri is not None: modlar+= [('esit',True),('atr',True)]
    for mod,km in modlar:
        e,al,at=portfoy(q,mod,veri,kume=km)
        top,cagr,dd=_ozet_egri(e); et=mod+(' +kume' if km else '')
        print(f"  {et:16s} {al:5d} {at:7d} {top:+7.0f}% {cagr:+6.0f}% {dd:+6.0f}%")
        satir.append({'set':ad,'boyut':et,'islem':al,'toplam':top,'yillik':cagr,'maxdd':dd})
    print(f"  {'XU100 ayni donem':16s} {'':5s} {'':7s} {xu_top:+7.0f}%")
    print(f"  {'MEVDUAT %40':16s} {'':5s} {'':7s} {mev_top:+7.0f}% {DN_MEVDUAT*100:+6.0f}%")
    pd.DataFrame(satir).to_csv(f"{K}/denetim_{ad.replace(' ','_')}.csv",index=False)
    print(f"  ({time.time()-t0:.0f}s)")
    return q

def veri_kontrol(veri, gun=20, esik=1.0, ornek=None):
    """VERI'deki son barlar ile yf'in guncel (duzeltilmis) verisini karsilastirir. Fark>esik% olan hisse = eski kisim duzeltilmemis."""
    import yfinance as yf
    semb=list(veri)[:ornek] if ornek else list(veri); bozuk=[]; t0=time.time()
    for i in range(0,len(semb),50):
        g=[s+'.IS' for s in semb[i:i+50]]
        try: y=yf.download(g,period=f'{gun+40}d',group_by='ticker',progress=False,auto_adjust=True,threads=True)
        except Exception: continue
        for s in g:
            try:
                yy=y[s].dropna(how='all').Close; k=s.replace('.IS','')
                if yy.index.tz is not None: yy.index=yy.index.tz_localize(None)
                yy.index=yy.index.normalize(); v=veri[k].Close
                ort=yy.index.intersection(v.index)[:gun]      # ORTUSEN en eski barlar
                if len(ort)<5: continue
                fark=float((v.loc[ort]/yy.loc[ort]-1).abs().max()*100)
                if fark>esik: bozuk.append((k,round(fark,1)))
            except Exception: pass
    bozuk.sort(key=lambda z:-z[1])
    print(f"  veri_kontrol: {len(semb)} hisse, {len(bozuk)} hissede eski kisim yf'den %{esik}+ farkli ({time.time()-t0:.0f}s)")
    if bozuk: print("   ", ", ".join(f"{s}({f}%)" for s,f in bozuk[:30]))
    return bozuk

def eski_donem_kur(bas='2018-01-01', son='2022-12-31', freq='4W-MON', ad='ESKI'):
    """2018-2022 icin cekirdek sinyal taramasi + onbellek. Uzun (~25-40 dk). Bir kez."""
    y=f"{K}/onbellek_{ad}.pkl"
    if os.path.exists(y): OBx=pickle.load(open(y,'rb')); print(f"  onbellek_{ad}: {len(OBx)} (hazir)"); return OBx
    tarihler=pd.bdate_range(bas,son,freq=freq).strftime('%Y-%m-%d')
    print(f"  eski donem taramasi: {len(tarihler)} tarih ({bas}..{son})")
    dd=tara(tarihler, ileri=60)
    dd.to_csv(f"{K}/sinyal_{ad}.csv",index=False)
    return onbellek_kur(dd, VERI, ad)

print("[ok] DENETIM yuklendi")
print("  denetim(OB24,'BIST 24-26',VERI,xu) | denetim(OB23,'BIST 2023',VERI,xu)")
print("  veri_kontrol(VERI) | OBE=eski_donem_kur(); denetim(OBE,'BIST 2018-22',VERI,xu)")
