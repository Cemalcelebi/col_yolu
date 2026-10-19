# =====================================================================
#  MFE / MAE ANALIZI — "kar nerede sonuyor?"
#
#  Kaynak: "Fixed Holding Period -> Maximum Favorable Excursion (MFE)
#  to find the profit decay cliff" + "Trailing Stop -> MAE to ensure
#  it isn't too tight"
#
#  MFE = pozisyon suresince gorulen EN YUKSEK kar
#  MAE = pozisyon suresince gorulen EN DERIN zarar
#
#  OLCTUKLERIMIZ:
#   1) MFE hangi barda zirve yapiyor (kar sonme noktasi)
#   2) MFE'nin ne kadarini kapanista koruyabiliyoruz (verimlilik)
#   3) Sabit tutma sureleri: 5..250 bar beklenti egrisi
#   4) Kar hedefi: %10/20/30/50 hedefe vurma orani ve beklenti
#   5) MAE dagilimi: stop nereye konursa kac islem kesilir
#
#  PARAMETRE EKLEMEZ — mevcut girisi degistirmeden cikisi optimize eder.
# =====================================================================
import numpy as np
import pandas as pd


def mfe_analiz(sec, veri=None, ufuk=250, hedefler=(10,20,30,50,75),
               stoplar=(5,10,15,20,25,30)):
    """sec: sembol+tarih iceren tablo (kurali gecen sinyaller)."""
    veri = veri if veri is not None else VERI
    R=[]
    for r in sec.itertuples():
        df = veri.get(r.sembol)
        if df is None: continue
        T = pd.Timestamp(r.tarih)
        il = df[df.index > T].head(ufuk)
        if len(il) < 30: continue
        p0 = float(df[df.index <= T].Close.iloc[-1])
        if p0 <= 0: continue
        H = il.High.to_numpy(float); L = il.Low.to_numpy(float); C = il.Close.to_numpy(float)
        mfe = (np.maximum.accumulate(H)/p0 - 1)*100      # o ana kadarki en yuksek kar
        mae = (np.minimum.accumulate(L)/p0 - 1)*100      # o ana kadarki en derin zarar
        d = {'sembol': r.sembol, 'tarih': r.tarih, 'n_bar': len(il),
             'MFE': float(mfe[-1]), 'MAE': float(mae[-1]),
             'zirve_bar': int(np.argmax(H)) + 1,
             'son': (float(C[-1])/p0 - 1)*100}
        # verimlilik: kapanis / zirve
        d['verim'] = d['son']/d['MFE'] if d['MFE'] > 0 else np.nan
        for h in (5,10,15,20,30,40,60,90,120,180,250):
            if len(C) >= h: d[f'g{h}'] = (float(C[h-1])/p0 - 1)*100
        # kar hedefleri
        for hd in hedefler:
            i = np.argmax(mfe >= hd) if (mfe >= hd).any() else -1
            d[f'hedef{hd}'] = int(i)+1 if i >= 0 else 0
        # stop senaryolari (stop yerse cikilir, yoksa sona kadar)
        for st in stoplar:
            i = np.argmax(mae <= -st) if (mae <= -st).any() else -1
            d[f'stop{st}'] = -st if i >= 0 else (float(C[-1])/p0 - 1)*100
        R.append(d)
    w = pd.DataFrame(R)
    if w.empty:
        print("[mfe] kayit yok"); return w

    def bek(v):
        v = pd.to_numeric(v, errors='coerce').dropna()
        v = v[abs(v) < 500]
        if len(v) < 10: return np.nan, np.nan, np.nan
        kz = v[v>0].median() if (v>0).any() else 0
        ky = v[v<=0].median() if (v<=0).any() else 0
        return float(v.median()), float(100*(v>0).mean()), float((v>0).mean()*kz+(v<=0).mean()*ky)

    print(f"\n{'='*70}\n  MFE / MAE  ({len(w)} sinyal)\n{'='*70}")
    print(f"  MFE medyan (en yuksek kar) : %{w.MFE.median():+.1f}")
    print(f"  MAE medyan (en derin zarar): %{w.MAE.median():+.1f}")
    print(f"  zirve kacinci bar          : medyan {w.zirve_bar.median():.0f}")
    print(f"  verimlilik (kapanis/zirve) : {w.verim.median():.2f}   "
          f"(1.0 = zirvede cikmis, 0 = hepsi geri verilmis)")

    print(f"\n  --- SABIT TUTMA SURESI ---")
    print(f"  {'sure':>6s} {'n':>5s} {'medyan':>8s} {'kazanan':>8s} {'beklenti':>9s}")
    en_iyi=(None,-1e9)
    for h in (5,10,15,20,30,40,60,90,120,180,250):
        k=f'g{h}'
        if k not in w: continue
        m,kz,b = bek(w[k])
        if np.isnan(m): continue
        print(f"  {h:6d} {int(w[k].notna().sum()):5d} {m:+7.1f}% {kz:7.0f}% {b:+8.1f}%")
        if b > en_iyi[1]: en_iyi=(h,b)
    print(f"  -> en yuksek beklenti: {en_iyi[0]} bar  (%{en_iyi[1]:+.1f})")

    print(f"\n  --- KAR HEDEFI ---")
    print(f"  {'hedef':>6s} {'vurma%':>8s} {'medyan bar':>11s}")
    for hd in hedefler:
        k=f'hedef{hd}'
        if k not in w: continue
        vur=w[k]>0
        mb=w.loc[vur,k].median() if vur.any() else np.nan
        print(f"  {hd:5d}% {100*vur.mean():7.0f}% {mb:11.0f}")

    print(f"\n  --- STOP SENARYOLARI ---")
    print(f"  {'stop':>6s} {'vurma%':>8s} {'medyan':>8s} {'beklenti':>9s}")
    for st in stoplar:
        k=f'stop{st}'
        if k not in w: continue
        vur=(w[k]<=-st+0.001)
        m,_,b = bek(w[k])
        print(f"  {st:5d}% {100*vur.mean():7.0f}% {m:+7.1f}% {b:+8.1f}%")
    m,kz,b = bek(w['g250'] if 'g250' in w else w['son'])
    print(f"  {'stopsuz':>6s} {'':>8s} {m:+7.1f}% {b:+8.1f}%")
    return w


print("[ok] MFE analizi yuklendi.")
print("  w = mfe_analiz(sec)   # sec: kurali gecen sinyaller (sembol,tarih)")
