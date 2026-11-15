# =====================================================================
#  TAKIP — her gun: gun()     (2026-09-18 denetim duzeltmeleri)
#  Kural: kapanis > tavan*AL_PAY -> AL | %20 vurunca trail (SMA20)
#         hedefsizde 120 bar -> SAT | trail'dekine ufuk uygulanmaz
#  POZISYON = carpanlar_hesapla() (COL_v1) — tek yer
#
#  DUZELTMELER:
#   T1) Aday eklenirken sinyal gunu segment olculeri (doji, alt_fitil, dar,
#       gecerli_oran, atr_ref) CSV'ye yazilir; boyut bunlardan hesaplanir.
#       Kirilim gunu segment YENIDEN hesaplanmaz (test ile ayni).
#   T2) Pozisyon CSV'ye kayit: poz%, cds_pct, borc_oz, oz_negatif, kural,
#       xu_giris (XU100 kapanisi), giris_acilis (ertesi gunun acilisi,
#       sonraki calistirmada dolar). Kapananda: cikis_acilis, getiri_acilis
#       (acilis->acilis), xu_getiri (ayni gunler endeks). 6 ay sonra agirlikli
#       ve gercekci kiyas icin gerekli.
#   T3) Kirilim esigi AL_PAY COL_v1'den (test = canli).
#   T4) Eski format CSV'ler otomatik tasinir (eksik sutun NaN -> notr carpan).
#   T5) takip_log.txt: her calistirma, hata ve olay satiri.
#   T6) 2026-10-17 COL BOZULDU cikisi (Cemal'in kurali: 'halka/taban kirilinca cik'):
#       pozisyon: kapanis < taban*(1-TABAN_TOL) -> SAT neden='taban' (stop degil, desen iptali).
#       aday   : kapanis < taban*(1-TABAN_TOL) -> listeden dus ('COL BOZULDU').
#       Eski pozisyon CSV'sinde taban yoksa giris gunu itibariyla col_segment ile yeniden hesaplanir,
#       o da yoksa giris*(1-TABAN_YEDEK) kullanilir ve log'a yazilir.
#   T7) 2026-10-17 FON SUZGECI: COL_v1 fon_etiket() varsa, tasfiye fonu payli hisse aday olmaz;
#       acik pozisyonda fon etiketi varsa TUT satirinda 'FON' uyarisi basilir (otomatik satmaz).
#   T8) 2026-10-18 D9 BAGLANTISI: COL_v1 D9 (uzun col + sektor ruzgari) gun() ekranina baglandi.
#       BEKLE satirlarina 'uzun' (6ay/12ay) ve 'ruz' (sektor sepeti 60g - piyasa, %) eklenir;
#       ekranin sonunda ruzgar_listesi() basilir (RUZGAR_LISTE=False ile kapanir). Alim/satim mantigi DEGISMEDI.
#   T9) 2026-10-20 BAYAT ADAY (COL_v1 D11 veri_bayat): verisi durmus hisse (yfinance 'no data' / islem durdurma;
#       BASLAT eski veriyi tutar) aday olabiliyordu ve 60 bar suresi hic dolmuyordu (df buyumuyor, aday listede kaliyordu).
#       Simdi: son bari ortak son tarihten VERI_BAYAT (5) is gunu eski hisse aday olmaz; listedeki aday 'VERI DURDU' ile duser.
#       Acik pozisyonda yalniz uyari basilir, otomatik satilmaz (islem durmus olabilir, satis mumkun olmayabilir).
#       Bayat orani VERI_BAYAT_UST'u (%10) asarsa toplu veri sorunu sayilir: temizlik yapilmaz, uyari basilir.
#   T10) 2026-10-21 STOP MALIYETE (Cemal'in yolu, COL_YOL olcumu: 50.006 obek islemi, 4 donem; "+%8'de stop maliyete +
#       %20 sonra SMA20 trail" 30 slot portfoyde 4 donem ort. +157 vs mevcut +144, agir kayip %10 -> %6; IZ_DEFTERI B15):
#       pozisyonda girisin uzerinde MALIYET_ESIK (%8) gorulduyse (onceki barlarin en yuksegi, ayni gun sayilmaz) stop = giris
#       fiyati; sonraki bir gunde Low <= giris ise SAT neden='maliyet', cikis = giris (stop emri maliyetten doldu), getiri 0.
#       Sira: taban (desen iptali) > maliyet > trail > ufuk. 'maliyette' sutunu CSV'de tutulur, TUT satirinda 'stop=maliyet' yazar.
#       AL kurali, carpanlar, trail ve ufuk DEGISMEDI. test_takip.py mekanik sinama.
#   T11) 2026-10-21 YARIM BAR (Cemal: 'gun() her saatte calissin, bugunun mumu bitmediyse dunku veriyle'): seans acikken
#       (TR is gunu 09:00-19:00, CANLI degilse) gun() bugune ait barlari veriden atar, son tam barla (dun) karar verir. tarih verilmisse
#       (replay) uygulanmaz. BASLAT B5 ayni isi VERI/XU100 yuklenirken yapar; bu kapi gun()'un kendi guvencesidir. TAKIP_SIMDI testi icin.
#   T12) 2026-11-15 UZUN COL ETIKETI KALDIRILDI (COL_v1 D14; Ç181a IZ DEGIL; Cemal 'uzun col etiketini kaldir'): BEKLE tablosundan
#       'uzun' sutunu kalkti, uzun_col_olc artik cagrilmaz (COL_v1'de olcum referansi olarak kalir). 'ruz%' ve 'RUZGAR' bayragi
#       (sektor ruzgari, Ç181c EMARE) aynen kalir; ekran sonundaki ruzgar_listesi() artik yalniz sektor ruzgari ozetini basar.
# =====================================================================
import os, logging, numpy as np, pandas as pd
_K='/content/drive/MyDrive/col_tarayici'
POZ_TABAN=6.0
TABAN_TOL=0.02      # T6: tabanin %2 altinda kapanis = col bozuldu
TABAN_YEDEK=0.15    # T6: taban hesaplanamazsa giris*(1-0.15)
MALIYET_ESIK=8.0    # T10: giris ustunde bu kadar % gorulunce stop maliyete (giris fiyati)
TAKIP_SIMDI=None    # T11: test icin sabit TR zamani (None = simdi)
A_KOL=['sembol','eklendi','tavan','taban','bas','kural','doji','alt_fitil','dar','gecerli_oran','atr_ref']
P_KOL=['sembol','giris_tarih','giris','tavan','taban','hedef_vurdu','bar','giris_acilis','poz','cds_pct','borc_oz','oz_negatif','kural',
       'doji','alt_fitil','dar','gecerli_oran','xu_giris','maliyette']
K_KOL=P_KOL+['cikis_tarih','cikis','cikis_acilis','getiri','getiri_acilis','xu_cikis','xu_getiri','neden']

tlog=logging.getLogger('col.takip'); tlog.propagate=False   # ekrana degil, sadece dosyaya
def _log_kur():
    if any(isinstance(h,logging.FileHandler) for h in tlog.handlers): return
    try:
        fh=logging.FileHandler(f'{_K}/takip_log.txt',encoding='utf-8')
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s','%Y-%m-%d %H:%M'))
        tlog.addHandler(fh); tlog.setLevel(logging.INFO)
    except Exception as e: print('  [log] dosya acilamadi:',e)
_log_kur()

def _yol(oneki): return (f'{_K}/{oneki}_adaylar.csv', f'{_K}/{oneki}_pozisyonlar.csv', f'{_K}/{oneki}_kapanan.csv')
def _oku(y, kol):
    """T4: eski format dosyalari yeni sutunlara tasir."""
    if not os.path.exists(y): return pd.DataFrame(columns=kol)
    try: t=pd.read_csv(y)
    except Exception as e:
        tlog.error(f'{y} okunamadi: {e}'); return pd.DataFrame(columns=kol)
    for k in kol:
        if k not in t.columns: t[k]=np.nan
    if 'kural' in t.columns: t['kural']=t.kural.fillna(1).astype(int)
    return t[kol+[c for c in t.columns if c not in kol]]

_TEMEL=None
def _temel():
    global _TEMEL
    if _TEMEL is None:
        y=f'{_K}/temel_duz.csv'
        try: _TEMEL=pd.read_csv(y,parse_dates=['aciklama']) if os.path.exists(y) else pd.DataFrame()
        except Exception as e: tlog.error(f'temel_duz.csv: {e}'); _TEMEL=pd.DataFrame()
        if len(_TEMEL) and 'oz_negatif' not in _TEMEL.columns:
            _TEMEL['oz_negatif']=(_TEMEL.ozkaynak<=0).astype(int) if 'ozkaynak' in _TEMEL.columns else 0
            _TEMEL.loc[_TEMEL.oz_negatif==1,'borc_oz']=np.nan
            tlog.warning('temel_duz.csv eski format — oz_negatif bellekte turetildi; BASLAT yeniden hesaplar')
    return _TEMEL

def borc_bilgi(sembol, tarih):
    """-> (borc_oz, oz_negatif). Veri yoksa (nan, 0) -> notr carpan."""
    t=_temel()
    if t.empty: return np.nan, 0
    g=t[(t.sembol==sembol)&(t.aciklama<=pd.Timestamp(tarih))]
    if not len(g): return np.nan, 0
    r=g.iloc[-1]; ozn=int(r.get('oz_negatif',0) or 0)
    b=float(r.borc_oz) if np.isfinite(float(r.borc_oz)) else np.nan
    return b, ozn

def _xu_kapanis(tarih, acilis=False):
    """XU100 kapanisi (global xu varsa). acilis=True -> tarih SONRASI ilk barin acilisi."""
    x=globals().get('xu')
    if x is None or not len(x): return np.nan
    try:
        T=pd.Timestamp(tarih)
        if acilis:
            s=x[x.index>T]; return float(s.Open.iloc[0]) if len(s) else np.nan
        s=x[x.index<=T]; return float(s.Close.iloc[-1]) if len(s) else np.nan
    except Exception as e: tlog.debug(f'xu: {e}'); return np.nan

def _cds_pct(bugun):
    if 'cds_rejim' not in globals(): return np.nan
    try:
        r=cds_rejim(tarih=bugun); return float(r['pct250']) if r else np.nan
    except Exception as e: tlog.debug(f'cds: {e}'); return np.nan

def _taban_bul(sembol, giris_tarih, giris, veri):
    """T6: eski kayitlarda taban yoksa giris gununden bir onceki gun itibariyla col_segment ile hesapla."""
    try:
        df=veri.get(sembol)
        if df is not None and 'col_segment' in globals():
            x=df[df.index<pd.Timestamp(giris_tarih)]
            if len(x)>=60:
                r=col_segment(x)
                if r and r.get('taban'): return float(r['taban']), 'segment'
    except Exception as e: tlog.debug(f'{sembol} taban_bul: {e}')
    return float(giris)*(1-TABAN_YEDEK), 'yedek'

def _fon_uyari(sembol):
    try: return fon_etiket(sembol) if 'fon_etiket' in globals() else None
    except Exception: return None

def _acilis_doldur(T, veri):
    """T2: giris_acilis / cikis_acilis bos olanlari, tarih sonrasi ilk barin acilisiyla doldur."""
    for kol_t,kol_a in (('giris_tarih','giris_acilis'),('cikis_tarih','cikis_acilis')):
        if kol_t not in T.columns: continue
        for i,r in T.iterrows():
            if pd.notna(r.get(kol_a)) or pd.isna(r.get(kol_t)): continue
            df=veri.get(r.sembol)
            if df is None: continue
            s=df[df.index>pd.Timestamp(r[kol_t])]
            if len(s): T.loc[i,kol_a]=float(s.Open.iloc[0])
    if 'cikis_acilis' in T.columns:
        m=T.giris_acilis.notna()&T.cikis_acilis.notna()&(T.giris_acilis>0)
        T.loc[m,'getiri_acilis']=((T.loc[m,'cikis_acilis']/T.loc[m,'giris_acilis']-1)*100).round(1)
    return T

def _tr_zaman():
    z=globals().get('TAKIP_SIMDI')
    return pd.Timestamp(z) if z is not None else pd.Timestamp.utcnow().tz_localize(None)+pd.Timedelta(hours=3)
def _yarim_bar_at(veri):
    """T11: seans acikken (TR is gunu 09:00-19:00, CANLI degil) bugune ait barlari atar. -> (yeni sozluk, atilan hisse sayisi, bugun)"""
    t=_tr_zaman()
    if not (t.weekday()<5 and 9<=t.hour<19) or globals().get('CANLI',False): return veri, 0, None
    b=t.normalize(); at=0; y={}
    for s,df in veri.items():
        if df is not None and len(df) and df.index[-1].normalize()>=b: y[s]=df[df.index.normalize()<b]; at+=1
        else: y[s]=df
    return y, at, b
def gun(veri=None, hedef=20, ma=20, ufuk=120, oneki='takip', sessiz=False, tarih=None):
    veri=veri if veri is not None else VERI
    if tarih is not None:
        T=pd.Timestamp(tarih); veri={s:df[df.index<=T] for s,df in veri.items()}
    else:                                                # T11: seans acikken bugunun yarim bari atilir
        veri,_at,_b=_yarim_bar_at(veri)
        if _at:
            tlog.info(f'T11 seans acik: {_at} hissede {_b.date()} yarim bari atildi')
            if not sessiz: print(f"  [seans acik] {_at} hissede bugunun ({_b.date()}) yarim bari atildi; karar son tam barla")
    bugun=str(max(df.index[-1] for df in veri.values() if len(df)).date())
    yA,yP,yK=_yol(oneki)
    A=_oku(yA,A_KOL); P=_oku(yP,P_KOL); Kp=_oku(yK,K_KOL)
    cds_pct=_cds_pct(bugun) if oneki=='takip' else np.nan
    cds_c=CARPAN['cds'](cds_pct)
    try: bayat,b_sinir,b_toplu=veri_bayat(veri) if 'veri_bayat' in globals() else ({},None,False)   # T9
    except Exception as e: tlog.warning(f'T9 veri_bayat: {e}'); bayat,b_sinir,b_toplu={},None,False
    b_suz={} if b_toplu else bayat                      # T9: toplu veri sorununda suzgec uygulanmaz
    if b_toplu: tlog.warning(f'T9 toplu veri sorunu: {len(bayat)} hisse bayat (sinir {b_sinir.date()}), temizlik yapilmadi')
    # ---- yeni adaylar (T1: sinyal gunu olculeri kaydedilir) ----
    R=[]; mevcut=set(A.sembol)|set(P.sembol)
    for s,df in veri.items():
        if len(df)<250 or s in mevcut: continue
        if s in b_suz: continue                         # T9: verisi durmus hisse aday olmaz
        if _fon_uyari(s): continue                      # T7: tasfiye fonu payli hisse aday olmaz
        try: o=col_olc(df)
        except Exception as e: tlog.debug(f'{s} col_olc: {e}'); o=None
        if o: R.append([s,bugun,o['tavan'],o['taban'],o['bas_tarih'],int(o['GECER']),o['doji'],o['alt_fitil'],o['dar'],o['gecerli_oran'],o['atr_ref']])
    if R: A=pd.concat([A,pd.DataFrame(R,columns=A_KOL)],ignore_index=True)
    # ---- kirilim -> AL ----
    al=[]; dus=[]; bozuk=[]; durdu=[]
    for r in A.itertuples():
        if str(r.eklendi)==bugun: continue
        df=veri.get(r.sembol)
        if df is None or not len(df): continue
        if r.sembol in b_suz:                           # T9: veri durdu -> aday duser (60 bar suresi hic dolmazdi)
            durdu.append(r.sembol); tlog.info(f'VERI DURDU aday {r.sembol} son bar {b_suz[r.sembol].date()}'); continue
        c=float(df.Close.iloc[-1])
        if c>r.tavan*AL_PAY:
            bo,ozn=borc_bilgi(r.sembol,bugun)
            poz,cc=carpanlar_hesapla(r._asdict(), cds_pct, bo, ozn, int(r.kural))
            al.append([r.sembol,bugun,c,r.tavan,r.taban,0,0,np.nan,round(poz,2),cds_pct,bo,ozn,int(r.kural),
                       r.doji,r.alt_fitil,r.dar,r.gecerli_oran,_xu_kapanis(bugun),0])
            tlog.info(f'AL {r.sembol} @{c:.2f} poz%{poz:.1f} carpan={cc}')
        elif pd.notna(r.taban) and c<float(r.taban)*(1-TABAN_TOL):
            bozuk.append(r.sembol); tlog.info(f'COL BOZULDU aday {r.sembol} @{c:.2f} taban {r.taban}')
        elif len(df[df.index>pd.Timestamp(r.eklendi)])>=60: dus.append(r.sembol)
    if al: P=pd.concat([P,pd.DataFrame(al,columns=P_KOL)],ignore_index=True)
    A=A[~A.sembol.isin([a[0] for a in al]+dus+bozuk+durdu)].reset_index(drop=True)
    # ---- pozisyonlar: trail / ufuk ----
    kapat=[]; tut=[]; durdu_poz=[]
    for i,r in P.iterrows():
        df=veri.get(r.sembol)
        if df is None or not len(df): continue
        if r.sembol in b_suz:                           # T9: yalniz uyari, otomatik satilmaz (islem durmus olabilir)
            durdu_poz.append(r.sembol); tlog.warning(f'VERI DURDU pozisyon {r.sembol} son bar {b_suz[r.sembol].date()}')
        il=df[df.index>pd.Timestamp(r.giris_tarih)]
        c=float(df.Close.iloc[-1]); bar=len(il); g=(c/r.giris-1)*100
        hv=bool(r.hedef_vurdu) or (len(il)>0 and float(il.High.max())>=r.giris*(1+hedef/100))
        s20=float(df.Close.rolling(ma).mean().iloc[-1])
        if pd.isna(r.get('taban')):                      # T6: eski kayit -> taban yeniden hesapla
            tb,kay=_taban_bul(r.sembol,r.giris_tarih,r.giris,veri); P.loc[i,'taban']=tb; r=P.loc[i]
            tlog.warning(f'{r.sembol} taban yoktu -> {tb:.2f} ({kay})')
        taban_kirildi=pd.notna(r.taban) and c<float(r.taban)*(1-TABAN_TOL)
        # T10: onceki barlarda +MALIYET_ESIK gorulduyse stop = giris; bugun Low <= giris -> maliyetten cikis (ayni gun sayilmaz)
        il_once=il.iloc[:-1] if len(il) else il
        m8=bool(pd.notna(r.get('maliyette')) and int(r.get('maliyette') or 0)==1) or (len(il_once)>0 and float(il_once.High.max())>=float(r.giris)*(1+MALIYET_ESIK/100))
        lo=float(df.Low.iloc[-1]) if np.isfinite(df.Low.iloc[-1]) else c
        maliyet_stop=bool(m8 and lo<=float(r.giris))
        neden='taban' if taban_kirildi else ('maliyet' if maliyet_stop else ('trail' if (hv and c<s20) else ('ufuk' if (bar>=ufuk and not hv) else None)))
        P.loc[i,'hedef_vurdu']=int(hv); P.loc[i,'bar']=bar; P.loc[i,'maliyette']=int(m8)
        if neden:
            cf=float(r.giris) if neden=='maliyet' else c        # T10: stop emri maliyetten dolar
            gf=0.0 if neden=='maliyet' else g
            xk=_xu_kapanis(bugun); xg=(xk/r.xu_giris-1)*100 if (np.isfinite(xk) and pd.notna(r.xu_giris) and r.xu_giris>0) else np.nan
            kapat.append(list(P.loc[i,P_KOL].values)+[bugun,cf,np.nan,round(gf,1),np.nan,xk,round(xg,1) if np.isfinite(xg) else np.nan,neden])
            tlog.info(f'SAT {r.sembol} @{cf:.2f} {gf:+.1f}% {neden} bar={bar}')
        else: tut.append((r.sembol,c,g,bar,hv,s20,float(r.taban) if pd.notna(r.taban) else np.nan,_fon_uyari(r.sembol),m8))
    if kapat: Kp=pd.concat([Kp,pd.DataFrame(kapat,columns=K_KOL)],ignore_index=True)
    P=P[~P.sembol.isin([k[0] for k in kapat])].reset_index(drop=True)
    P=_acilis_doldur(P,veri); Kp=_acilis_doldur(Kp,veri)
    try:
        A.to_csv(yA,index=False); P.to_csv(yP,index=False); Kp.to_csv(yK,index=False)
    except Exception as e: tlog.error(f'CSV yazilamadi: {e}'); print('  [!] CSV yazilamadi:',e)
    if sessiz:
        olay=[f"AL {a[0]}@{a[2]:.2f}" for a in al]+[f"SAT {k[0]}@{k[len(P_KOL)+1]:.2f}({k[len(P_KOL)+3]:+.0f}%)" for k in kapat]
        if olay: print(f"  {bugun}  "+"  ".join(olay))
        return A,P,Kp
    tlog.info(f'gun {bugun} aday {len(A)} poz {len(P)} kapanan {len(Kp)} cds_pct {cds_pct}')
    print(f"\n== {bugun}  CDS {cds_pct if np.isfinite(cds_pct) else '?'} -> {cds_c}x")
    print(f"aday {len(A)} | poz {len(P)} | kapanan {len(Kp)}")
    if b_toplu: print(f"\n[!] VERI SORUNU: {len(bayat)} hissede {b_sinir.date()} sonrasi veri yok — toplu guncelleme sorunu, bayat aday temizligi yapilmadi (T9)")
    if al:
        print("\nAL  (hisse  pozisyon%  borc  doji  fitil  dar)")
        for a in al: print(f"  {a[0]:6s} %{a[7]:.1f}  {a[9] if np.isfinite(a[9]) else '?'}{' OZ-' if a[10] else ''}  {a[12]}  {a[13]}  {a[14]}  {'kural' if a[11] else 'serbest'}")
    if kapat:
        print("\nSAT  (hisse  kar%  endeks%)")
        for k in kapat: print(f"  {k[0]:6s} {k[len(P_KOL)+3]:+.0f}%  {k[len(P_KOL)+6] if np.isfinite(k[len(P_KOL)+6]) else '?'}  {k[-1]}")
    if tut:
        print("\nTUT  (hisse  kar%  durum  tabana%)")
        for s,c,g,b,hv,s20,tb,fe,m8 in sorted(tut,key=lambda z:-z[2]):
            tbs=f"taban {(tb/c-1)*100:+.0f}%" if np.isfinite(tb) else "taban ?"
            fon=f"  FON {fe[0].split()[0].title()} %{fe[1]:.0f}" if fe else ""
            ms="  stop=maliyet" if m8 else ""                   # T10
            print(f"  {s:6s} {g:+4.0f}%  {('TRAIL sat:'+f'{(s20/c-1)*100:+.0f}%') if hv else str(ufuk-b)+'g'}  {tbs}{ms}{fon}")
    if durdu_poz: print("\n[!] VERI DURDU — acik pozisyon, fiyat eski, elle kontrol et:", ", ".join(f"{s} (son bar {b_suz[s].date()})" for s in durdu_poz))
    RZ=pd.DataFrame()                                    # T8: D9 sektor ruzgari (COL_v1 yoksa bos)
    if 'sektor_ruzgar' in globals():
        try: RZ=sektor_ruzgar(veri)
        except Exception as e: tlog.warning(f'T8 ruzgar: {e}')
    def _rz(s):                                          # T8/T12: (ruz%, ruzgar var mi); uzun col kaldirildi
        rz=float(RZ.ruz.get(s,np.nan)) if (not RZ.empty and s in RZ.index) else np.nan
        sp=float(RZ.sepet.get(s,np.nan)) if (not RZ.empty and s in RZ.index) else np.nan
        var=bool(np.isfinite(rz) and np.isfinite(sp) and rz>=globals().get('RUZ_ESIK',0.10) and sp>globals().get('RUZ_MUTLAK',0.0))
        return rz, var
    if len(A):
        rows=[]
        for r in A.itertuples():
            df=veri.get(r.sembol)
            if df is None or not len(df): continue
            c=float(df.Close.iloc[-1]); uz=(c/r.tavan-1)*100
            if uz<-8: continue
            bo,ozn=borc_bilgi(r.sembol,bugun)
            poz,_=carpanlar_hesapla(r._asdict(), cds_pct, bo, ozn, int(r.kural))
            rz,var=_rz(r.sembol)
            rows.append((r.sembol,uz,poz,r.doji,r.alt_fitil,int(r.kural),rz,var))
        rows.sort(key=lambda z:-z[1])
        print(f"\nBEKLE  (hisse  tavana%  girilecek%  doji  fitil  ruz%)   [tavana -8% icindekiler, toplam aday {len(A)}]")
        for s,uz,poz,dv,fv,kr,rz,var in rows:
            rzs=f"{rz*100:+.0f}" if np.isfinite(rz) else "?"
            print(f"  {s:6s} {uz:+4.0f}%   %{poz:.1f}   {dv}  {fv}  {rzs:>4s}{'  RUZGAR' if var else ''}  {'' if kr else '(serbest)'}")
    if dus: print("\nSURESI DOLDU (60 bar):", ", ".join(dus))
    if bozuk: print("\nCOL BOZULDU (taban kirildi, aday dustu):", ", ".join(bozuk))
    if durdu: print(f"\nVERI DURDU ({globals().get('VERI_BAYAT',5)}+ is gunu veri yok, aday dustu):", ", ".join(f"{s} (son bar {b_suz[s].date()})" for s in durdu))
    if len(Kp):
        v=Kp.getiri.astype(float); va=Kp.getiri_acilis.astype(float).dropna(); vx=Kp.xu_getiri.astype(float).dropna()
        print(f"\nKAPANAN {len(Kp)}: kazanan %{100*(v>0).mean():.0f}  ort {v.mean():+.1f}%"
              +(f" | acilis->acilis ort {va.mean():+.1f}% (n={len(va)})" if len(va) else "")
              +(f" | endeks ort {vx.mean():+.1f}%" if len(vx) else ""))
    if oneki=='takip' and globals().get('RUZGAR_LISTE',False) and 'ruzgar_listesi' in globals():   # T8/T12: sektor ruzgari ozeti
        try: ruzgar_listesi(veri)
        except Exception as e: tlog.warning(f'T8 ruzgar_listesi: {e}'); print('  [!] ruzgar listesi:',e)
    return A,P,Kp

def gun_abd():
    global VERI, MARKETS, GUNLUK_PERIOD
    bist_veri=VERI
    try:
        MARKETS=["america"]; GUNLUK_PERIOD="5y"; hizli_baslat(tarama=False)
        A,P,Kp=gun(oneki='abd')
    finally:
        VERI=bist_veri; MARKETS=["turkey"]; GUNLUK_PERIOD="10y"; print("\n[BIST'e donuldu]")
    return A,P,Kp

def replay(bas, son=None, veri=None, oneki='replay', sifirla=True):
    """Gunluk yeniden oynatma: canli mantigin birebir aynisi -> en temiz dogrulama."""
    veri=veri if veri is not None else VERI
    if sifirla:
        for y in _yol(oneki):
            if os.path.exists(y): os.remove(y)
    ornek=max(veri.values(), key=len)
    tarihler=ornek.index[(ornek.index>=pd.Timestamp(bas))&(ornek.index<=pd.Timestamp(son or ornek.index[-1]))]
    print(f"REPLAY {tarihler[0].date()} -> {tarihler[-1].date()}  ({len(tarihler)} gun)\n")
    for T in tarihler: A,P,Kp=gun(veri, oneki=oneki, sessiz=True, tarih=T)
    if len(Kp):
        v=Kp.getiri.astype(float); print(f"\n{len(Kp)} islem | kazanan %{100*(v>0).mean():.0f} | ort %{v.mean():+.1f} | bek %{bek(v):+.1f}")
    return A,P,Kp

print(f"[ok] takip (2026-11-15 T12: uzun col etiketi kaldirildi | 2026-10-21 T11: seans acikken bugunun yarim bari atilir | T10: +%{MALIYET_ESIK:.0f} gorulunce stop maliyete | 2026-10-20 T9: verisi durmus aday duser | 2026-10-18 T8: D9 uzun col + ruzgar ekranda | 2026-10-17 T6: taban kirilinca cik, tol %{TABAN_TOL*100:.0f} | T7: fon suzgeci; 2026-09-18: sinyal gunu olculeri, acilis/endeks kaydi, log)")
