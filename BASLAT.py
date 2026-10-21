# ===== BASLAT (2026-09-18 — denetim duzeltmeleri)
#  B1) veri_yenile: auto_adjust=FALSE (ana veri col_atilim_TEK ile boyle indi;
#      onceden True ile ekleniyordu -> temettu gununde iki farkli seri karisiyordu).
#  B2) Ortusen barlarda eski/yeni kapanis %0.5'ten fazla farkliysa (bolunme, bedelsiz,
#      temettu duzeltmesi) o hisse BASTAN indirilir. Sahte sicrama / sahte kirilim biter.
#  B3) onbellek.py, DENETIM.py yuklenir; OBUS de yuklenir; XU100 10 yil (2017-22 testi).
#  B4) temel_duz.csv eski formatsa (oz_negatif yok) yeniden hesaplanir.
#  B5) 2026-10-21 YARIM BAR (Cemal): gun() her saatte calisabilsin. Seans acikken (TR is gunu 09:00-19:00) bugunun
#      yarim bari VERI'den ve XU100'den HER ZAMAN atilir (indirme atlanmis olsa da; pkl'de kaldiysa pkl temizlenir),
#      karar dunku kapanisla verilir. 19:00 sonrasi bugunun bari kalir. CANLI=True ile kapanir.
import os, io, time, pickle, logging
if not os.path.exists('/content/drive/MyDrive'):
    from google.colab import drive; drive.mount('/content/drive')
K='/content/drive/MyDrive/col_tarayici'
blog=logging.getLogger('col.baslat')
def drive_indir(fid, ad):
    from google.colab import auth; auth.authenticate_user()
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    svc=build('drive','v3'); req=svc.files().get_media(fileId=fid); buf=io.BytesIO()
    dl=MediaIoBaseDownload(buf,req); done=False
    while not done: _,done=dl.next_chunk()
    open(f'{K}/{ad}','wb').write(buf.getvalue()); print(f"  {ad}: {len(buf.getvalue())} byte")
exec(open(f'{K}/col_atilim_TEK.py').read().replace('OTO_CALISTIR = True','OTO_CALISTIR = False'))
MARKETS=["turkey"]; TIMEFRAME="1d"; GUNLUK_PERIOD="10y"; hizli_baslat(tarama=False)
import yfinance as yf, pandas as pd, numpy as np, datetime as _dt
def _tr_simdi(): return _dt.datetime.now(_dt.timezone.utc)+_dt.timedelta(hours=3)
def _beklenen_son_bar():
    t=_tr_simdi(); g=t.date()
    if t.weekday()<5 and t.hour>=19: return g
    g=g-_dt.timedelta(days=1)
    while g.weekday()>=5: g=g-_dt.timedelta(days=1)
    return g
def _temizle(y):
    if y is None or not len(y): return None
    y=y.dropna(how='all')
    if not len(y): return None
    if isinstance(y.columns,pd.MultiIndex): y.columns=y.columns.get_level_values(0)
    y=y.rename(columns=str.title)
    if y.index.tz is not None: y.index=y.index.tz_localize(None)
    y.index=y.index.normalize()
    y=y[['Open','High','Low','Close','Volume']].dropna(subset=['Close'])
    return y[~y.index.duplicated(keep='last')]
def sembol_bastan_indir(k, period=None):
    """B2: tek hisseyi tum gecmisiyle yeniden indir (auto_adjust=False, ana veriyle ayni)."""
    try:
        y=_temizle(yf.download(k+'.IS',period=period or GUNLUK_PERIOD,interval='1d',progress=False,auto_adjust=False))
        if y is not None and len(y)>=60: VERI[k]=y; return True
    except Exception as e: blog.warning(f'{k} bastan indirme: {e}')
    return False
B2_NEDEN = {}   # VK_YAMA v1.0 (veri_koru: yenileme sonrası bölünme onarımı + B2 nedeni)
def _seans_acik():
    """B5: TR is gunu 09:00-19:00 arasi True (gunun bari henuz kapanmadi). CANLI=True ile kapali."""
    t=_tr_simdi(); return bool(t.weekday()<5 and 9<=t.hour<19 and not globals().get('CANLI',False))
def _yarim_bar_at(veri):
    """B5: seans acikken bugune (ve sonrasina) ait barlari atar; sozlugu yerinde degistirir, atilan hisse sayisini doner."""
    if not _seans_acik(): return 0
    _bugun=pd.Timestamp(_tr_simdi().date()); _at=0
    for _k in list(veri):
        _df=veri[_k]
        if _df is not None and len(_df) and _df.index[-1].normalize()>=_bugun: veri[_k]=_df[_df.index.normalize()<_bugun]; _at+=1
    return _at
def veri_yenile(gun=15, zorla=False, sapma=0.005):
    for _k in VERI: VERI[_k]=VERI[_k].dropna(subset=['Close'])
    _at0=_yarim_bar_at(VERI)                              # B5: pkl'de bugunun yarim bari kaldiysa once at
    if _at0:
        print(f"  [yenile] seans acik ({_tr_simdi():%H:%M} TR): {_at0} hissede bugunun yarim bari atildi, karar dunku kapanisla")
        try:
            tmp=f'{K}/veri_1d_turkey.pkl.tmp'; pickle.dump(VERI,open(tmp,'wb')); os.replace(tmp,f'{K}/veri_1d_turkey.pkl')
        except Exception as e: blog.warning(f'B5 pkl temizlenemedi: {e}')
    son=max(df.index[-1] for df in VERI.values()).date(); hedef=_beklenen_son_bar()
    if son>=hedef and not zorla and not globals().get('CANLI',False):
        print(f"  [yenile] veri guncel ({son}), indirme atlandi"); return son
    semboller=[s+'.IS' for s in VERI]; guncel=0; hata=0; bastan=[]; t0=time.time(); B2_NEDEN.clear()
    for i in range(0,len(semboller),50):
        grup=semboller[i:i+50]
        try: y=yf.download(grup,period=f'{gun}d',interval='1d',group_by='ticker',progress=False,auto_adjust=False,threads=True)
        except Exception as e: print("  [yenile] indirme hatasi:",e); hata+=len(grup); continue
        for s in grup:
            try:
                yeni=_temizle(y[s] if len(grup)>1 else y)
                if yeni is None: continue
                k=s.replace('.IS',''); eski=VERI[k]
                # ---- B2: ortusme kontrolu ----
                ort=eski.index.intersection(yeni.index)
                if len(ort)>=2:
                    e_c=eski.loc[ort,'Close'].to_numpy(float); y_c=yeni.loc[ort,'Close'].to_numpy(float)
                    m=np.isfinite(e_c)&np.isfinite(y_c)&(e_c>0)
                    if m.any() and np.nanmax(np.abs(y_c[m]/e_c[m]-1))>sapma:
                        _i=int(np.nanargmax(np.abs(y_c[m]/e_c[m]-1))); B2_NEDEN[k]=(str(ort[m][_i].date()), float(y_c[m][_i]/e_c[m][_i]), str(eski.index[-1].date()))
                        bastan.append(k); continue
                b=pd.concat([eski[eski.index<yeni.index[0]],yeni])
                b=b[~b.index.duplicated(keep='last')]
                if b.index[-1]>eski.index[-1]: guncel+=1
                VERI[k]=b
            except Exception as e: hata+=1; blog.debug(f'{s}: {e}')
    for k in bastan:
        if sembol_bastan_indir(k): guncel+=1
        else: hata+=1
    if bastan: print(f"  [yenile] seri uyusmadi (bolunme/temettu), bastan indirildi: {', '.join(bastan[:15])}{' ...' if len(bastan)>15 else ''} ({len(bastan)})")
    _at=_yarim_bar_at(VERI)                               # B5
    if _at: print(f"  [yenile] seans acik ({_tr_simdi():%H:%M} TR): {_at} hissede bugunun yarim bari atildi, karar dunku kapanisla")
    for _k in VERI: VERI[_k]=VERI[_k].dropna(subset=['Close'])
    son=max(df.index[-1] for df in VERI.values()).date()
    print(f"  [yenile] {guncel} hisse guncellendi | hata {hata} | son bar {son} | {time.time()-t0:.0f}s")
    if guncel:
        tmp=f'{K}/veri_1d_turkey.pkl.tmp'
        pickle.dump(VERI,open(tmp,'wb')); os.replace(tmp,f'{K}/veri_1d_turkey.pkl')
    return son
veri_yenile()
exec(open(f'{K}/veri_koru.py', encoding='utf-8').read()); VK = veri_koru(K, VERI, B2_NEDEN)
exec(open(f'{K}/COL_v1.py').read())
for f in ['kalibrasyon.py','kirilim_sonrasi.py','piramit.py','giris_testleri.py','takip.py','temel.py','onbellek.py','DENETIM.py']:
    y=f'{K}/{f}'
    if os.path.exists(y):
        try: exec(open(y).read())
        except Exception as e: print(f"[hata] {f}: {e}")
    else: print("[eksik]", f)
def _yh(ad, hesapla):
    y=f'{K}/{ad}.csv'
    if os.path.exists(y): t=pd.read_csv(y); print(f"  {ad}: yuklendi ({len(t)})"); return t
    t=hesapla(); t.to_csv(y,index=False); print(f"  {ad}: hesaplandi+kaydedildi ({len(t)})"); return t
d = _yh('v1_final_BIST', lambda: tara(pd.bdate_range('2024-06-01','2026-04-01',freq='2W-MON').strftime('%Y-%m-%d')))
try: w = _yh('kirilim_sonrasi_w', lambda: kirilim_sonrasi(d[d.GECER]))
except Exception as e: w=None; print('[w yok]',e)
try:
    d23=pd.read_csv(f'{K}/yeni_BIST_2023.csv')
    d23=d23[d23.GECER] if 'GECER' in d23 else d23[(d23.clv>=-0.164)&(d23.bant_son>=0.509)&(d23.ortaust>=0.40)]
    print(f"  d23: {len(d23)}")
except Exception as e: d23=None; print('[d23 yok]',e)
try: t=temel_yukle()          # B4: eski format ise kendi yeniden hesaplar
except Exception as e: t=None; print('[temel yok]',e)
OB24=OB23=OBUS=None
for _ad,_f in (('OB24','onbellek_2024_26.pkl'),('OB23','onbellek_2023.pkl'),('OBUS','onbellek_ABD.pkl')):
    try: globals()[_ad]=pickle.load(open(f'{K}/{_f}','rb'))
    except Exception as e: print(f'[{_ad} yok] {e}')
def pnl_ob(o, kb, gp, ufuk=250, hedef=20, maliyet=0.4):
    """Eski imza korunur (getiri, jt); govde DENETIM.pnl ile ayni."""
    g,jt,_=pnl(o, kb, gp, ufuk=ufuk, hedef=hedef, maliyet=maliyet); return g,jt
print(f"  onbellek: OB24 {len(OB24) if OB24 else '-'} | OB23 {len(OB23) if OB23 else '-'} | OBUS {len(OBUS) if OBUS else '-'}")
try:
    xu = endeks_yukle(period='10y')
    _xd={'xu':xu}
    if _yarim_bar_at(_xd): xu=_xd['xu']; print(f"  [endeks] seans acik: XU100 bugunun yarim bari atildi, son bar {xu.index[-1].date()}")   # B5
except Exception as e: xu=None; print("[endeks yok]", e)
tr=_tr_simdi()
print(f"\nHAZIR | VERI {len(VERI)} | d {len(d)} | d23 {len(d23) if d23 is not None else '-'} | TR saat {tr:%H:%M}")
print('  A,P,Kp = gun()          <- gunluk')
print('  denetim(OB24, OB23, OBUS, xu)   <- tum duzeltilmis metrikler (30 sn)')
