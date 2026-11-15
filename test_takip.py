"""test_takip.py — takip.py T10 (stop maliyete) + T11 (seans acikken yarim bar) + T12 / COL_v1 D14 (uzun col etiketi kaldirildi, sektor ruzgari kaldi) mekanik sinama. Sentetik veri, gecici klasor; Drive'a dokunmaz.
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
# 6) T11: tarih verilmeden, seans ACIKKEN (TR 12:43, son bar = bugun) -> bugunun bari atilir, dunku bar ile karar (test 2 ile ayni: TUT, maliyette=1)
ns['TAKIP_SIMDI'] = df.index[-1] + pd.Timedelta(hours=12, minutes=43)
poz_yaz('t6', g)
with contextlib.redirect_stdout(io.StringIO()):
    A6, P6, K6 = ns['gun'](veri={'TEST': df}, oneki='t6', sessiz=True)
ok = len(K6) == 0 and len(P6) == 1 and int(P6.iloc[0].maliyette) == 1 and int(P6.iloc[0].bar) == len(yol) - 1
print('6 seans acik yarim bar:', 'OK' if ok else 'HATA', dict(poz=len(P6), kapanan=len(K6), bar=int(P6.iloc[0].bar) if len(P6) else None))
if not ok: hata.append(6)
# 7) T11: ayni veri, seans KAPALI (TR 19:30) -> bugunun bari kalir, test 1 ile ayni (maliyet cikisi)
ns['TAKIP_SIMDI'] = df.index[-1] + pd.Timedelta(hours=19, minutes=30)
poz_yaz('t7', g)
with contextlib.redirect_stdout(io.StringIO()):
    A7, P7, K7 = ns['gun'](veri={'TEST': df}, oneki='t7', sessiz=True)
ok = len(K7) == 1 and K7.iloc[0].neden == 'maliyet'
print('7 seans kapali tam bar:', 'OK' if ok else 'HATA', K7[['neden']].to_dict('records') if len(K7) else 'kapanan yok')
if not ok: hata.append(7)
ns['TAKIP_SIMDI'] = None
# ---- T12 / D14 (15 Kas 2026): uzun col etiketi ekrandan kalkti, sektor ruzgari kaldi ----
def seri_egim(son_artis):
    """300 bar: 0..239 duz 100, son 60 barda kapanis dogrusal olarak %son_artis artar."""
    ix = pd.bdate_range('2025-01-01', periods=300)
    C = np.r_[np.full(240, 100.0), 100.0 * (1 + son_artis * np.arange(1, 61) / 60)]
    return pd.DataFrame({'Open': C, 'High': C * 1.005, 'Low': C * 0.995, 'Close': C, 'Volume': 1e6}, index=ix)
V8 = {**{f'Y{i}': seri_egim(0.30) for i in range(5)}, **{f'D{i}': seri_egim(0.0) for i in range(8)}}
ns['_SEKTOR'] = {**{f'Y{i}': 'XYUKSELEN' for i in range(5)}, **{f'D{i}': 'XDUZ' for i in range(8)}}
_uz_cagri = []
_uz_asil = ns['uzun_col_olc']
ns['uzun_col_olc'] = lambda *a, **k: (_uz_cagri.append(1), _uz_asil(*a, **k))[1]   # cagri sayaci
c8 = float(V8['Y0'].Close.iloc[-1])
pd.DataFrame([{'sembol': 'Y0', 'eklendi': str(V8['Y0'].index[-10].date()), 'tavan': c8 * 1.03, 'taban': c8 * 0.5, 'bas': str(V8['Y0'].index[200].date()),
               'kural': 1, 'doji': 0.2, 'alt_fitil': 0.1, 'dar': 0.5, 'gecerli_oran': 1.0, 'atr_ref': 1.0}]).to_csv(f'{TMP}/takip_adaylar.csv', index=False)
for _f in ('takip_pozisyonlar.csv', 'takip_kapanan.csv'):
    if os.path.exists(f'{TMP}/{_f}'): os.remove(f'{TMP}/{_f}')
_b = io.StringIO()
with contextlib.redirect_stdout(_b):
    ns['gun'](veri=V8, oneki='takip', sessiz=False, tarih=V8['Y0'].index[-1])
cikti = _b.getvalue()
bas = [l for l in cikti.splitlines() if l.startswith('BEKLE')]
_sat = cikti.splitlines(); _i = next((i for i, l in enumerate(_sat) if l.startswith('BEKLE')), None)
satir = [l for l in (_sat[_i + 1:_i + 3] if _i is not None else []) if l.strip().startswith('Y0 ')]
# 8a) BEKLE basliginda 'uzun' yok, 'ruz%' var; Y0 satirinda ruz ve RUZGAR bayragi duruyor
ok = len(bas) == 1 and ' uzun ' not in bas[0] and 'ruz%' in bas[0] and len(satir) == 1 and 'RUZGAR' in satir[0]
print('8a BEKLE uzun yok/ruz :', 'OK' if ok else 'HATA', bas[0].strip() if bas else 'BEKLE yok', '|', satir[0].strip() if satir else 'Y0 satiri yok')
if not ok: hata.append('8a')
# 8b) gun() sonundaki ruzgar_listesi: 'SEKTOR RUZGARI' var, 'uzun colde' ve eski 'D9 RUZGAR LISTESI' yok, rüzgarli sektor basildi
ok = 'SEKTOR RUZGARI' in cikti and 'uzun colde' not in cikti and 'D9 RUZGAR LISTESI' not in cikti and 'XYUKSELEN' in cikti
print('8b ruzgar ozeti       :', 'OK' if ok else 'HATA', dict(sektor_ruzgari='SEKTOR RUZGARI' in cikti, uzun_colde='uzun colde' in cikti))
if not ok: hata.append('8b')
# 8c) ruzgar_listesi donusu = ruzgarli sektor tablosu; uzun_col_olc gun() / ruzgar_listesi / bugun_liste icinde cagrilmadi
with contextlib.redirect_stdout(io.StringIO()):
    t8 = ns['ruzgar_listesi'](V8)
    _co_asil = ns['col_olc']                     # bugun_liste sema sinamasi: her hisse aday olsun diye sabit col_olc
    ns['col_olc'] = lambda df, *a, **k: {'GECER': True, 'bas_tarih': df.index[200], 'uzunluk': 40, 'doji': 0.2, 'alt_fitil': 0.1, 'dar': 0.5,
                                         'gecerli_oran': 1.0, 'clv': 0.1, 'bant_son': 0.5, 'ortaust': 0.5, 'yukseklik_atr': 3.0,
                                         'taban': 95.0, 'tavan': 105.0}
    try: bl = ns['bugun_liste'](V8, hepsi=True)
    finally: ns['col_olc'] = _co_asil
ok = (list(t8.columns) == ['alt', 'sepet', 'ruz', 'uye'] and list(t8.alt) == ['XYUKSELEN'] and int(t8.uye.iloc[0]) == 5
      and abs(float(t8.sepet.iloc[0]) - 0.30) < 1e-6 and not _uz_cagri and len(bl) == 13 and 'uzun' not in bl.columns and {'ruz', 'ruzgar'} <= set(bl.columns)
      and set(bl[bl.ruzgar == 'RUZGAR'].sembol) == {f'Y{i}' for i in range(5)})
print('8c donus + cagri yok  :', 'OK' if ok else 'HATA', t8.to_dict('records'), dict(uzun_cagri=len(_uz_cagri), bugun_liste_sutun=list(getattr(bl, 'columns', []))[:5]))
if not ok: hata.append('8c')
# 8d) uzun_col_olc ve UZUN_* / RUZ_* sabitleri COL_v1'de duruyor (olcum referansi; birebir esitlik test_d9_yeniden'de)
ns['uzun_col_olc'] = _uz_asil
ok = callable(ns.get('uzun_col_olc')) and all(k in ns for k in ('UZUN_W', 'UZUN_BANT', 'UZUN_MUM', 'UZUN_KONUM', 'RUZ_GERI', 'RUZ_ESIK', 'RUZ_MIN_UYE', 'RUZ_MUTLAK', 'RUZ_BAYAT')) \
    and (ns['UZUN_W'], ns['UZUN_BANT'], ns['UZUN_MUM'], ns['UZUN_KONUM']) == (250, 1.5, 0.04, 0.5)
print('8d uzun_col_olc duruyor:', 'OK' if ok else 'HATA')
if not ok: hata.append('8d')
ns['_SEKTOR'] = None
import shutil; shutil.rmtree(TMP, ignore_errors=True)
print('SONUC:', 'HEPSI OK' if not hata else f'HATA {hata}')
sys.exit(1 if hata else 0)
