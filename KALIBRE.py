# =====================================================================
#  KALIBRE — segment v3 (goz kalibrasyonu) ve eski/yeni P&L kiyasi   (2026-09-18)
#
#  Cemal'in 29 gozle isaretli colu + 8 olumsuz ornek uzerinde bulunan:
#   - yerel=5 dip kontrolu colun icindeki kucuk sarkmada segmenti sifirliyor (11/26)
#   - cekirdek 5/7 sarti kirilim oncesi buyuyen mumlarda colu siliyor (4/26)
#   - cokusten sonra ATR sisiyor, cokus mumlari segmentte kaliyor, tavan yukari kayiyor
#  v3 = yerel 8 + min_cekirdek 3 + SOL KESME (colun son 20 barinin sakin ATR'siyle bant;
#       bant disinda kapanan son bardan sonrasi col).  Goz sonucu: aday 13/26 -> 23/26,
#       yanlis tavan 4 -> 2. Olumsuzlarda da daha cok segment bulur (3/8 -> 6/8): sekil
#       olculeri olumsuzu ayirmiyor; ayrim kirilim + trail. Net etki = P&L testi (asagida).
#
#  Kullanim (BASLAT sonrasi, Colab):
#     exec(open('/content/drive/MyDrive/col_tarayici/KALIBRE.py').read())
#     K1 = kalibre()                 <- 2024-26 ve 2023: eski vs v3, ~30-40 dk, sonuc ekranda + kalibre_sonuc.csv
#     v3_uygula()                    <- begenirsen: bu oturumda gun()/tara v3 ile calisir (kagit)
#     v3_kalici()                    <- kalici yapmak icin BASLAT'a satir ekler (geri almak: v3_geri())
# =====================================================================
import os, time, pickle, logging, numpy as np, pandas as pd
klog=logging.getLogger('col.kalibre')
V3=dict(yerel=8, min_cekirdek=3, tolerans=2)
V3_SOL_KES=dict(cek_bar=20, tol=1.0)
_col_segment_v2=col_segment          # orijinal (COL_v1)

def sol_kes(x, s, cek_bar=20, tol=1.0):
    """Segmentin son cek_bar bari = cekirdek. Sakin ATR = cekirdek TR medyani.
    Bant = [cekirdek min Low, cekirdek max govde ustu] +- tol*sakinATR.
    Kapanisi bant disinda olan SON bardan sonrasi segment; olculer yeniden hesaplanir."""
    try:
        seg=x[x.index>=pd.Timestamp(s['bas_tarih'])]
        if len(seg)<=cek_bar: return s
        ck=seg.tail(cek_bar)
        tr=np.maximum(ck.High-ck.Low, np.maximum((ck.High-ck.Close.shift()).abs(),(ck.Low-ck.Close.shift()).abs())).dropna()
        q=float(tr.median())
        if not np.isfinite(q) or q<=0: return s
        alt=float(ck.Low.min())-tol*q; ust=float(np.maximum(ck.Open,ck.Close).max())+tol*q
        disi=np.where((seg.Close.values<alt)|(seg.Close.values>ust))[0]
        if not len(disi): return s
        yb=int(disi.max())+1
        if len(seg)-yb<8: return s
        sg=seg.iloc[yb:]; atr=float(s['atr_ref'])
        O,H,L,C,Vv=(sg[c].to_numpy(float) for c in ('Open','High','Low','Close','Volume'))
        g=gecerli_bar_maskesi(O,H,L,C,Vv); ng=int(g.sum())
        s2=dict(s)
        s2.update({'bas_tarih':str(sg.index[0].date()),'uzunluk':len(sg),'hafta_bar':round(len(sg)/5.0,1),
                   'taban':round(float(L.min()),2),'tavan':round(float(np.maximum(O,C).max()),2),
                   'yukseklik_atr':round((H.max()-L.min())/atr,2),'gecerli_oran':round(ng/len(sg),3),
                   'govde_ort':round(float(np.abs(C-O).mean())/atr,2),'egim':round(_egim(C,atr),4),
                   'doji':round(float((np.abs(C[g]-O[g])/(H[g]-L[g])<DOJI_ESIK).mean()),3) if ng>=5 else np.nan,
                   'alt_fitil':round(float(((np.minimum(O[g],C[g])-L[g])/atr).mean()),3) if ng>=5 else np.nan,
                   'dar':dar_hafta_olc(x, len(x)-len(sg)),'sol_kesilen':yb,'sakin_atr':round(q,4)})
        return s2
    except Exception as e:
        klog.debug(f'sol_kes: {e}'); return s

def col_segment_v3(df, tarih=None, yazdir=False, **kw):
    x=df[df.index<=pd.Timestamp(tarih)] if tarih is not None else df
    p={**V3, **kw}
    s=_col_segment_v2(x, yazdir=yazdir, **p)
    return sol_kes(x, s, **V3_SOL_KES) if s else None

def col_olc_v3(df, tarih=None):
    x=df[df.index<=pd.Timestamp(tarih)] if tarih is not None else df
    r=col_segment_v3(x)
    if not r or r['uzunluk']<MIN_UZ or r['yukseklik_atr']>MAX_YUK: return None
    if not r.get('atr_ref') or r['atr_ref']<=0: return None
    b=_bant(df, tarih if tarih is not None else df.index[-1])
    if not b: return None
    clv=_clv(x,r); C=x.Close.to_numpy(float)
    onc=(C[-1]/C[-250]-1)*100 if len(C)>=250 else np.nan
    gecer=bool(clv>=E_CLV and b['bant_son']>=E_BS and b['ortaust']>=E_OU)
    return {**r, **b, 'clv':round(clv,3),'onceki_250':round(onc,1) if np.isfinite(onc) else np.nan,'GECER':gecer}

def tara_v3(tarihler, ileri=60, veri=None):
    veri=veri if veri is not None else VERI; R=[]
    for i,T in enumerate(tarihler,1):
        Ts=pd.Timestamp(T); say=0
        for s,df in veri.items():
            x=df[df.index<=Ts]
            if len(x)<250: continue
            try: o=col_olc_v3(df,T)
            except Exception as e: klog.debug(f'{s}@{T}: {e}'); o=None
            if not o: continue
            il=df[df.index>Ts].head(ileri)
            if len(il)<20: continue
            p0=float(x.Close.iloc[-1]); yon='YOK'
            for c in il.Close.to_numpy(float):
                if c>o['tavan']*AL_PAY: yon='YUKARI'; break
                if c<o['taban']: yon='ASAGI'; break
            if yon=='YOK': continue
            R.append({'sembol':s,'tarih':T,'yon':yon,'clv':o['clv'],'bant_son':o['bant_son'],'ortaust':o['ortaust'],'uzunluk':o['uzunluk'],
                      'doji':o['doji'],'alt_fitil':o['alt_fitil'],'dar':o['dar'],'gecerli_oran':o['gecerli_oran'],'GECER':o['GECER'],
                      'getiri':(float(il.Close.iloc[-1])/p0-1)*100}); say+=1
        if i%5==0 or i==len(tarihler): print(f"  {i}/{len(tarihler)} {T} -> {say} (toplam {len(R)})")
    return pd.DataFrame(R)

def onbellek_kur_v3(dd, veri, ad, ileri=300):
    t0=time.time(); R=[]
    for i,r in enumerate(dd.itertuples()):
        if i%500==0: print(f"  {i}/{len(dd)} {time.time()-t0:.0f}s")
        df=veri.get(r.sembol)
        if df is None: continue
        T=pd.Timestamp(r.tarih); x=df[df.index<=T]
        try: s=col_segment_v3(x)
        except Exception: s=None
        if not s or s['uzunluk']<MIN_UZ or s['yukseklik_atr']>MAX_YUK: continue
        il=df[df.index>T].head(ileri)
        if len(il)<40: continue
        R.append(_kayit(r.sembol,T,getattr(r,'GECER',True),s,x,il))
    tmp=f'{K}/onbellek_{ad}.pkl.tmp'; pickle.dump(R,open(tmp,'wb')); os.replace(tmp,f'{K}/onbellek_{ad}.pkl')
    print(f"  {ad}: {len(R)} kayit, {time.time()-t0:.0f}s -> onbellek_{ad}.pkl"); return R

def _tarihler_2023():
    try:
        d=pd.read_csv(f'{K}/yeni_BIST_2023.csv'); return sorted(pd.to_datetime(d.tarih).dt.strftime('%Y-%m-%d').unique())
    except Exception:
        return list(pd.bdate_range('2023-01-02','2023-12-29',freq='2W-MON').strftime('%Y-%m-%d'))

def kalibre(donemler=('2024_26','2023'), xu_=None, mevduat_yillik=45.0):
    """Eski (OB24/OB23) vs v3: ayni tarih izgarasi, tekil, ertesi acilis, portfoy. Sonuc: kalibre_sonuc.csv"""
    xu_=xu_ if xu_ is not None else globals().get('xu')
    SON=[]
    for ad in donemler:
        if ad=='2024_26': tarihler=list(pd.bdate_range('2024-06-01','2026-04-01',freq='2W-MON').strftime('%Y-%m-%d')); OBe=globals().get('OB24')
        else: tarihler=_tarihler_2023(); OBe=globals().get('OB23')
        print(f"\n===== {ad}: v3 tarama ({len(tarihler)} tarih) =====")
        dd=tara_v3(tarihler); dd.to_csv(f'{K}/yeni_BIST_{ad}_v3.csv',index=False)
        OBv=onbellek_kur_v3(dd, VERI, f'{ad}_v3')
        for etiket,OB in (('ESKI',OBe),('V3',OBv)):
            if not OB: print(f'  {etiket}: onbellek yok'); continue
            t=islemler(OB,'acilis',tekil=True,xu=xu_)
            r=ozet(t,f'{ad} {etiket}') or {}
            p=portfoy(t,OB,xu=xu_,agirlikli=True,mevduat_yillik=mevduat_yillik,ad=f'{ad} {etiket}') or {}
            SON.append({'donem':ad,'kural':etiket,'sinyal':len(OB),'islem':r.get('n'),'kazanan%':r.get('kazanan'),'bek':r.get('bek'),'agir%':r.get('agir'),
                        'endeks_ustu':r.get('endeks_ustu'),'portfoy_toplam':p.get('toplam'),'yillik':p.get('yillik'),'max_dd':p.get('max_dd'),'atlanan':p.get('atlanan')})
        globals()[f'OB{ad[:2]}_v3' if ad=='2023' else 'OB24_v3']=OBv
    s=pd.DataFrame(SON); pd.set_option('display.width',220)
    print("\n===== KALIBRE SONUC (tekil, ertesi acilis, ufuk 120, agirlikli portfoy) ====="); print(s.round(1).to_string(index=False))
    s.to_csv(f'{K}/kalibre_sonuc.csv',index=False)
    print("\nKarar kurali: V3 iki donemde de bek ve portfoy_toplam'da ESKI'yi geciyorsa ve max_dd kotulesmiyorsa -> v3_kalici()")
    return s

def v3_uygula():
    """Bu oturumda gun()/tara/bugun_liste v3 segmentle calissin."""
    g=globals(); g['col_segment']=col_segment_v3; g['col_olc']=col_olc_v3
    print("[v3] col_segment/col_olc = v3 (yerel 8, cekirdek 3, sol kesme). Kagit takip artik v3.")

def v3_geri():
    g=globals(); g['col_segment']=_col_segment_v2
    exec(open(f'{K}/COL_v1.py').read(), g); print("[v3] geri alindi (COL_v1 yeniden yuklendi)")

def v3_kalici():
    """BASLAT.py sonuna KALIBRE yukle + v3_uygula() satiri ekler (yerinde yazar, kopya degil)."""
    y=f'{K}/BASLAT.py'; src=open(y).read()
    if 'KALIBRE.py' in src: print('[v3] BASLAT zaten v3 yukluyor'); return
    src+="\nexec(open(f'{K}/KALIBRE.py').read()); v3_uygula()   # 2026-09-18 goz kalibrasyonu\n"
    open(y,'w').write(src); print('[v3] BASLAT.py guncellendi: her baslatmada v3 aktif. Geri almak: BASLAT sonundaki satiri sil.')

print("[ok] KALIBRE: kalibre() | v3_uygula() | v3_kalici() | v3_geri()   (col_segment_v3 hazir)")
