"""test_takip.py — takip.py T10 (stop maliyete) mekanik sinama. Sentetik veri, gecici klasor; Drive'a dokunmaz.
Calistirma: python3 test_takip.py  (repo kokunde; COL_v1.py ve takip.py ayni klasorde)"""
import contextlib, io, os, sys, tempfile
import numpy as np, pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
ns = {'__name__': 'takip_test_ns'}
with contextlib.redirect_stdout(io.StringIO()):
    for f in ('COL_v1.py', 'takip.py'):
        exec(compile(open(os.path.join(KOK, f), encoding='utf-8').read(), f, 'exec'), ns)
TMP = tempfile.mkdtemp(prefix='takip_t10_')
ns['_K'] = TMP                                   # CSV ve log gecici klasore
ns['xu'] = None


def seri(yol):
    """300 bar: 0..279 duz 100; sonra verilen (O,H,L,C) listesi."""
    n0 = 280
    ix = pd.bdate_range('2025-01-01', periods=n0 + len(yol))
    O = [100.0] * n0 + [y[0] for y in yol]; H = [100.5] * n0 + [y[1] for y in yol]
    L = [99.5] * n0 + [y[2] for y in yol]; C = [100.0] * n0 + [y[3] for y in yol]
    return pd.DataFrame({'Open': O, 'High': H, 'Low': L, 'Close': C, 'Volume': 1e6}, index=ix)


def poz_yaz(oneki, giris_tarih):
    P = pd.DataFrame([{'sembol': 'TEST', 'giris_tarih': giris_tarih, 'giris': 100.0, 'tavan': 99.0, 'taban': 90.0, 'hedef_vurdu': 0, 'bar': 0,
                       'giris_acilis': 100.0, 'poz': 6.0, 'cds_pct': np.nan, 'borc_oz': np.nan, 'oz_negatif': 0, 'kural': 1,
                       'doji': np.nan, 'alt_fitil': np.nan, 'dar': np.nan, 'gecerli_oran': np.nan, 'xu_giris': np.nan}])
    P.to_csv(f'{TMP}/{oneki}_pozisyonlar.csv', index=False)


def calistir(oneki, df, tarih):
    with contextlib.redirect_stdout(io.StringIO()):
        A, P, Kp = ns['gun'](veri={'TEST': df}, oneki=oneki, sessiz=True, tarih=tarih)
    return P, Kp


hata = []
# 1) +9 goruldu (onceki barlar), sonra Low girise iniyor -> SAT neden maliyet, cikis 100, getiri 0
yol = [(100, 103, 99.8, 102), (102, 106, 101, 105), (105, 109.5, 104, 108), (108, 109, 103, 104), (104, 105, 99.5, 101)]
df = seri(yol); g = str(df.index[279].date())
poz_yaz('t1', g); P, Kp = calistir('t1', df, df.index[-1])
ok = len(Kp) == 1 and Kp.iloc[0].neden == 'maliyet' and abs(float(Kp.iloc[0].cikis) - 100.0) < 1e-6 and abs(float(Kp.iloc[0].getiri)) < 1e-6
print('1 maliyet cikisi      :', 'OK' if ok else 'HATA', Kp[['neden', 'cikis', 'getiri']].to_dict('records') if len(Kp) else 'kapanan yok')
if not ok: hata.append(1)
# 2) ayni veri, bir gun once (Low 103, girise inmedi) -> TUT, maliyette=1
poz_yaz('t2', g); P, Kp = calistir('t2', df, df.index[-2])
ok = len(Kp) == 0 and len(P) == 1 and int(P.iloc[0].maliyette) == 1
print('2 maliyette isareti   :', 'OK' if ok else 'HATA', dict(poz=len(P), kapanan=len(Kp), maliyette=int(P.iloc[0].maliyette) if len(P) else None))
if not ok: hata.append(2)
# 3) +8 hic gorulmedi (en yuksek 104), Low girisin altina indi -> maliyet cikisi YOK (TUT)
yol3 = [(100, 102, 99.8, 101), (101, 104, 100.5, 103), (103, 103.5, 99.0, 100.5)]
df3 = seri(yol3)
poz_yaz('t3', g); P, Kp = calistir('t3', df3, df3.index[-1])
ok = len(Kp) == 0 and len(P) == 1 and int(P.iloc[0].maliyette) == 0
print('3 +8 yoksa stop yok   :', 'OK' if ok else 'HATA', dict(poz=len(P), kapanan=len(Kp)))
if not ok: hata.append(3)
# 4) +8 AYNI gun goruldu ve ayni gun Low girise indi -> henuz maliyet cikisi yok (onceki barlar esas), ertesi gun isaret
yol4 = [(100, 109, 99.5, 105)]
df4 = seri(yol4)
poz_yaz('t4', g); P, Kp = calistir('t4', df4, df4.index[-1])
ok = len(Kp) == 0 and len(P) == 1
print('4 ayni gun sayilmaz   :', 'OK' if ok else 'HATA', dict(poz=len(P), kapanan=len(Kp)))
if not ok: hata.append(4)
# 5) taban kirilinca 'taban' oncelikli (maliyette olsa da)
yol5 = [(100, 109.5, 99.8, 108), (108, 108, 85, 86)]
df5 = seri(yol5)
poz_yaz('t5', g); P, Kp = calistir('t5', df5, df5.index[-1])
ok = len(Kp) == 1 and Kp.iloc[0].neden == 'taban'
print('5 taban oncelikli     :', 'OK' if ok else 'HATA', Kp[['neden']].to_dict('records') if len(Kp) else 'kapanan yok')
if not ok: hata.append(5)
import shutil; shutil.rmtree(TMP, ignore_errors=True)
print('SONUC:', 'HEPSI OK' if not hata else f'HATA {hata}')
sys.exit(1 if hata else 0)
