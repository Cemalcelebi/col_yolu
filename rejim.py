# =====================================================================
#  REJIM — CDS (carpan) + EEM (ikinci isik). 2026-09-07
#  Dis veri taramasi (10 seri, 2 donem): tutarli olanlar CDS ve EEM.
#  VIX, DXY, TRY oynakligi tersine dondu. Brent/altin zamanla karisik.
#  CDS tek carpan: +2.8/+3.7 | CDS+EEM skor carpan: +1.2/+3.9 -> CDS kalir,
#  EEM gosterge. Skor<0.8 hucresi: 2024-26 %32, 2023 %58 kazanan (FELAKET).
# =====================================================================
import numpy as np, pandas as pd

def eem_rejim(tarih=None):
    try:
        import yfinance as yf
        y=yf.download('EEM',period='2y',progress=False,auto_adjust=True)
        if isinstance(y.columns,pd.MultiIndex): y.columns=y.columns.get_level_values(0)
        e=y.Close.dropna(); e.index=pd.to_datetime(e.index).tz_localize(None)
        if tarih is not None: e=e[e.index<=pd.Timestamp(tarih)]
        if len(e)<120: return None
        pct=float((e.tail(250)<e.iloc[-1]).mean())
        return {'eem':round(float(e.iloc[-1]),2),'pct250':round(pct,2),'tarih':str(e.index[-1].date()),
                'etiket':'EM istahi ZAYIF' if pct<0.3 else ('EM istahi GUCLU' if pct>=0.6 else 'EM orta')}
    except Exception: return None

def rejim_ozet(tarih=None):
    c=cds_rejim(tarih=tarih) if 'cds_rejim' in globals() else None
    if not c: return "  [rejim] CDS verisi yok"
    poz=c.get('pozisyon_yuzde', round(6*c['carpan'],1))
    out=f"  CDS {c['cds']} bp ({c['tarih']}) | yuzdelik {c['pct250']} | {c['etiket']} -> POZISYON %{poz}"
    e=eem_rejim(tarih)
    if e:
        skor=c['pct250']+e['pct250']
        hucre=('!!! FELAKET HUCRESI (skor<0.8): gecmiste %32-58 kazanan, agir kayip %10+ — cok temkinli' if skor<0.8 else
               ('IYI HUCRE (skor>=1.2): gecmiste %78-93 kazanan' if skor>=1.2 else 'ORTA HUCRE (0.8-1.2): %55 kazanan (Aralik 2024 profili)'))
        out+=f"\n  EEM {e['eem']} ({e['tarih']}) | yuzdelik {e['pct250']} | {e['etiket']}\n  CDS+EEM skor {skor:.2f} -> {hucre}"
    if c.get('veri_yasi_gun',0)>30: out+="\n  [!] CDS verisi eski — investing.com'dan guncelle: cds_2022.csv"
    return out

print("[ok] rejim yuklendi")
print(rejim_ozet())
