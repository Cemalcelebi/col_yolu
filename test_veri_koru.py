# -*- coding: utf-8 -*-
"""test_veri_koru — python -I test_veri_koru.py [--mutasyon]   (bolunme_onar.py aynı klasörde olmalı)"""
import datetime as _dt
import logging
import os
import pickle
import shutil
import sys
import tempfile
import time
import traceback
import types

import numpy as np
import pandas as pd

KLASOR = os.path.dirname(os.path.abspath(__file__))
KAYNAK = open(os.path.join(KLASOR, "veri_koru.py"), encoding="utf-8").read()
BO_YOL = os.path.join(KLASOR, "bolunme_onar.py")
# BASLAT.py (2026-09-18) içinden _tr_simdi … veri_yenile() + COL_v1 exec satırına kadar olan bölüm, birebir
BASLAT_PARCA = (
    'def _tr_simdi(): return _dt.datetime.now(_dt.timezone.utc)+_dt.timedelta(hours=3)\n'
    'def _beklenen_son_bar():\n'
    '    t=_tr_simdi(); g=t.date()\n'
    '    if t.weekday()<5 and t.hour>=19: return g\n'
    '    g=g-_dt.timedelta(days=1)\n'
    '    while g.weekday()>=5: g=g-_dt.timedelta(days=1)\n'
    '    return g\n'
    'def _temizle(y):\n'
    '    if y is None or not len(y): return None\n'
    "    y=y.dropna(how='all')\n"
    '    if not len(y): return None\n'
    '    if isinstance(y.columns,pd.MultiIndex): y.columns=y.columns.get_level_values(0)\n'
    '    y=y.rename(columns=str.title)\n'
    '    if y.index.tz is not None: y.index=y.index.tz_localize(None)\n'
    '    y.index=y.index.normalize()\n'
    "    y=y[['Open','High','Low','Close','Volume']].dropna(subset=['Close'])\n"
    "    return y[~y.index.duplicated(keep='last')]\n"
    'def sembol_bastan_indir(k, period=None):\n'
    '    """B2: tek hisseyi tum gecmisiyle yeniden indir (auto_adjust=False, ana veriyle ayni)."""\n'
    '    try:\n'
    "        y=_temizle(yf.download(k+'.IS',period=period or GUNLUK_PERIOD,interval='1d',progress=False,auto_adjust=False))\n"
    '        if y is not None and len(y)>=60: VERI[k]=y; return True\n'
    "    except Exception as e: blog.warning(f'{k} bastan indirme: {e}')\n"
    '    return False\n'
    'def veri_yenile(gun=15, zorla=False, sapma=0.005):\n'
    "    for _k in VERI: VERI[_k]=VERI[_k].dropna(subset=['Close'])\n"
    '    son=max(df.index[-1] for df in VERI.values()).date(); hedef=_beklenen_son_bar()\n'
    "    if son>=hedef and not zorla and not globals().get('CANLI',False):\n"
    '        print(f"  [yenile] veri guncel ({son}), indirme atlandi"); return son\n'
    "    semboller=[s+'.IS' for s in VERI]; guncel=0; hata=0; bastan=[]; t0=time.time()\n"
    '    for i in range(0,len(semboller),50):\n'
    '        grup=semboller[i:i+50]\n'
    "        try: y=yf.download(grup,period=f'{gun}d',interval='1d',group_by='ticker',progress=False,auto_adjust=False,threads=True)\n"
    '        except Exception as e: print("  [yenile] indirme hatasi:",e); hata+=len(grup); continue\n'
    '        for s in grup:\n'
    '            try:\n'
    '                yeni=_temizle(y[s] if len(grup)>1 else y)\n'
    '                if yeni is None: continue\n'
    "                k=s.replace('.IS',''); eski=VERI[k]\n"
    '                # ---- B2: ortusme kontrolu ----\n'
    '                ort=eski.index.intersection(yeni.index)\n'
    '                if len(ort)>=2:\n'
    "                    e_c=eski.loc[ort,'Close'].to_numpy(float); y_c=yeni.loc[ort,'Close'].to_numpy(float)\n"
    '                    m=np.isfinite(e_c)&np.isfinite(y_c)&(e_c>0)\n'
    '                    if m.any() and np.nanmax(np.abs(y_c[m]/e_c[m]-1))>sapma:\n'
    '                        bastan.append(k); continue\n'
    '                b=pd.concat([eski[eski.index<yeni.index[0]],yeni])\n'
    "                b=b[~b.index.duplicated(keep='last')]\n"
    '                if b.index[-1]>eski.index[-1]: guncel+=1\n'
    '                VERI[k]=b\n'
    "            except Exception as e: hata+=1; blog.debug(f'{s}: {e}')\n"
    '    for k in bastan:\n'
    '        if sembol_bastan_indir(k): guncel+=1\n'
    '        else: hata+=1\n'
    '    if bastan: print(f"  [yenile] seri uyusmadi (bolunme/temettu), bastan indirildi: {\', \'.join(bastan[:15])}{\' ...\' if len(bastan)>15 else \'\'} ({len(bastan)})")\n'
    '    _tr=_tr_simdi()\n'
    "    if _tr.weekday()<5 and 9<=_tr.hour<19 and not globals().get('CANLI',False):\n"
    '        _bugun=pd.Timestamp(_tr.date()); _at=0\n'
    '        for _k in VERI:\n'
    '            if len(VERI[_k]) and VERI[_k].index[-1].normalize()>=_bugun: VERI[_k]=VERI[_k][VERI[_k].index.normalize()<_bugun]; _at+=1\n'
    '        if _at: print(f"  [yenile] seans acik: {_at} hissede bugunun yarim bari atildi")\n'
    "    for _k in VERI: VERI[_k]=VERI[_k].dropna(subset=['Close'])\n"
    '    son=max(df.index[-1] for df in VERI.values()).date()\n'
    '    print(f"  [yenile] {guncel} hisse guncellendi | hata {hata} | son bar {son} | {time.time()-t0:.0f}s")\n'
    '    if guncel:\n'
    "        tmp=f'{K}/veri_1d_turkey.pkl.tmp'\n"
    "        pickle.dump(VERI,open(tmp,'wb')); os.replace(tmp,f'{K}/veri_1d_turkey.pkl')\n"
    '    return son\n'
    'veri_yenile()\n'
    "exec(open(f'{K}/COL_v1.py').read())\n"
)


def yukle(kod=KAYNAK):
    m = types.ModuleType("veri_koru_test"); m.__file__ = "veri_koru.py"; sys.modules["veri_koru_test"] = m
    exec(compile(kod, "veri_koru.py", "exec"), m.__dict__)
    m.__dict__["_KOD"] = kod
    return m.__dict__


def seri(n=200, bas=100.0, seed=1, start="2024-01-01"):
    rng = np.random.default_rng(seed)
    c = bas * np.cumprod(1 + rng.normal(0, 0.01, n))
    ix = pd.bdate_range(start, periods=n)
    return pd.DataFrame({"Open": c * (1 + rng.normal(0, 0.003, n)), "High": c * 1.012, "Low": c * 0.988, "Close": c,
                         "Volume": (1e6 + rng.integers(0, 1e5, n)).astype(float)}, index=ix)


def bedelsiz(df, k, oran):
    d = df.copy()
    for c in ("Open", "High", "Low", "Close"):
        d.iloc[k:, d.columns.get_loc(c)] = d[c].iloc[k:] * oran
    d.iloc[k:, d.columns.get_loc("Volume")] = d["Volume"].iloc[k:] / oran
    return d


def kapanis_sicrama(df):
    r = df["Close"].to_numpy(float); r = r[1:] / r[:-1]
    return int(((r <= 0.62) | (r >= 1.6)).sum())


def klasor():
    K = tempfile.mkdtemp(prefix="vk_")
    shutil.copy(BO_YOL, os.path.join(K, "bolunme_onar.py"))
    return K


# ---------------------------------------------------------------- testler
def test_ham_bolunme_onarilir(ns):
    K = klasor(); ham = bedelsiz(seri(), 120, 0.5)
    assert kapanis_sicrama(ham) == 1
    V = {"AAA": ham, "BBB": seri(seed=2)}
    R = ns["veri_koru"](K, V)
    assert R["degisen_hisse"] == 1 and len(R["onarilan"]) == 1, R["degisen_hisse"]
    assert kapanis_sicrama(V["AAA"]) == 0 and R["kalan"] == [], R["kalan"]
    assert abs(V["AAA"]["Close"].iloc[0] / seri()["Close"].iloc[0] - 0.5) < 0.01          # geçmiş yeni ölçeğe çekildi
    assert R["yazildi"] and os.path.exists(os.path.join(K, "veri_1d_turkey.pkl"))
    P = pickle.load(open(os.path.join(K, "veri_1d_turkey.pkl"), "rb"))
    pd.testing.assert_frame_equal(P["AAA"], V["AAA"])
    assert len(pd.read_csv(os.path.join(K, "veri_koru_gunluk.csv"))) == 1


def test_onarilmis_ve_temiz_dokunulmaz(ns):
    K = klasor(); ham = bedelsiz(seri(), 120, 0.5)
    V = {"AAA": ham}
    ns["veri_koru"](K, V, kaydet=False)
    onarilmis = V["AAA"].copy(); temiz = seri(seed=3)
    V2 = {"AAA": onarilmis.copy(), "CCC": temiz.copy()}
    R = ns["veri_koru"](K, V2)
    assert R["degisen_hisse"] == 0 and not R["yazildi"]
    assert not os.path.exists(os.path.join(K, "veri_1d_turkey.pkl"))
    pd.testing.assert_frame_equal(V2["AAA"], onarilmis); pd.testing.assert_frame_equal(V2["CCC"], temiz)


def test_acilis_hatasi_ve_kalan_sicrama(ns):
    K = klasor()
    a = seri(seed=4); a.iloc[100, a.columns.get_loc("Open")] = a["Close"].iloc[99] * 0.5        # bozuk açılış, kapanış normal
    b = seri(seed=5)
    for c in ("Close", "High", "Low"):                                                         # açılış normal, kapanış 2 kat (onarılamaz)
        b.iloc[150:, b.columns.get_loc(c)] = b[c].iloc[150:] * 2.0
    b.iloc[151:, b.columns.get_loc("Open")] = b["Open"].iloc[151:] * 2.0
    a0, b0 = a.copy(), b.copy()
    V = {"AAA": a, "BBB": b}
    R = ns["veri_koru"](K, V)
    assert R["degisen_hisse"] == 0 and not R["yazildi"] and R["dokunulmayan"] == 1, (R["degisen_hisse"], R["dokunulmayan"])
    pd.testing.assert_frame_equal(V["AAA"], a0); pd.testing.assert_frame_equal(V["BBB"], b0)
    assert [x[0] for x in R["kalan"]] == ["BBB"] and R["kalan"][0][2] > 1.9, R["kalan"]


def test_b2_ozet(ns):
    b2 = {"A": ("2026-10-08", 1.02, "2026-10-08"), "B": ("2026-10-08", 0.97, "2026-10-08"), "C": ("2026-10-01", 1.5, "2026-10-08")}
    o = ns["vk_b2_ozet"](b2)
    assert o["n"] == 3 and o["son_barda"] == 2, o
    assert o["tarihler"][0] == ("2026-10-08", 2)
    assert ns["vk_b2_ozet"](None)["n"] == 0


def test_baslat_yama(ns):
    yeni, d = ns["baslat_yama"](BASLAT_PARCA)
    assert d and ns["VK_ISARET"] in yeni
    assert "B2_NEDEN.clear()" in yeni and "B2_NEDEN[k]=" in yeni and "VK = veri_koru(K, VERI, B2_NEDEN)" in yeni
    assert yeni.count("bastan.append(k); continue") == 1
    assert ns["baslat_yama"](yeni) == (yeni, False)                                        # ikinci kez: dokunmaz
    for bozuk in (BASLAT_PARCA.replace("bastan.append(k); continue", "bastan.append(k)\n                        continue"),
                  BASLAT_PARCA + "\nveri_yenile()\nexec(open(f'{K}/COL_v1.py').read())\n"):
        try:
            ns["baslat_yama"](bozuk)
        except ValueError:
            pass
        else:
            raise AssertionError("eksik/çift çapa sessiz geçti")
    eski_satir = [l for l in BASLAT_PARCA.splitlines() if l.strip()]
    yeni_satir = yeni.splitlines()
    degisen = [l for l in eski_satir if l not in yeni_satir]
    assert len(degisen) == 1 and "B2_NEDEN" not in degisen[0] and "t0=time.time()" in degisen[0], degisen


class SahteYF:
    """yfinance yerine: liste → son N gün (çoklu sütun), tek sembol → tüm geçmiş (ham)."""
    def __init__(self, tam):
        self.tam = tam; self.bastan = []

    def download(self, t, period=None, interval=None, group_by=None, progress=None, auto_adjust=None, threads=None):
        if isinstance(t, list):
            gun = int(str(period).rstrip("d"))
            parca = {s: self.tam[s.replace(".IS", "")].tail(gun) for s in t}
            return parca[t[0]] if len(t) == 1 else pd.concat(parca, axis=1)
        self.bastan.append(t)
        return self.tam[t.replace(".IS", "")].copy()


def test_uctan_uca_yenileme_onarimi_ezmez(ns):
    """Gerçek olay: onarılmış seri + son barı yarım kalmış → B2 baştan HAM indirir → veri_koru onarır, B2 nedeni son bar."""
    K = klasor(); open(os.path.join(K, "veri_koru.py"), "w", encoding="utf-8").write(ns["_KOD"])
    yeni, _ = ns["baslat_yama"](BASLAT_PARCA)
    yeni = yeni[:yeni.index("exec(open(f'{K}/COL_v1.py').read())")]
    temiz = seri(n=260, seed=7); ham_tam = bedelsiz(temiz, 120, 0.5)
    ns0 = {}; exec(compile(open(BO_YOL, encoding="utf-8").read(), "bolunme_onar.py", "exec"), ns0)
    onarilmis, _ = ns0["bo_onar"](ham_tam, ns0["bo_bul"](ham_tam))
    eski = onarilmis.iloc[:259].copy(); eski.iloc[-1, eski.columns.get_loc("Close")] *= 1.03         # dünkü yarım bar
    b_tam = seri(n=260, seed=8); b_eski = b_tam.iloc[:259].copy()
    yf = SahteYF({"AAA": ham_tam, "BBB": b_tam})
    g = {"VERI": {"AAA": eski, "BBB": b_eski}, "K": K, "yf": yf, "pd": pd, "np": np, "time": time, "pickle": pickle, "os": os,
         "blog": logging.getLogger("t"), "_dt": _dt, "GUNLUK_PERIOD": "10y"}
    exec(compile(yeni, "BASLAT.py", "exec"), g)
    V = g["VERI"]
    assert yf.bastan == ["AAA.IS"], yf.bastan
    assert kapanis_sicrama(V["AAA"]) == 0, "onarım ezildi"
    assert len(V["AAA"]) == 260 and len(V["BBB"]) == 260
    assert abs(V["AAA"]["Close"].iloc[0] / onarilmis["Close"].iloc[0] - 1) < 1e-9
    assert g["B2_NEDEN"]["AAA"][0] == g["B2_NEDEN"]["AAA"][2] == str(eski.index[-1].date()), g["B2_NEDEN"]
    assert g["VK"]["b2"]["son_barda"] == 1 and g["VK"]["degisen_hisse"] == 1
    P = pickle.load(open(os.path.join(K, "veri_1d_turkey.pkl"), "rb"))
    assert kapanis_sicrama(P["AAA"]) == 0 and len(P["AAA"]) == 260


TESTLER = [test_ham_bolunme_onarilir, test_onarilmis_ve_temiz_dokunulmaz, test_acilis_hatasi_ve_kalan_sicrama, test_b2_ozet,
           test_baslat_yama, test_uctan_uca_yenileme_onarimi_ezmez]

MUTASYONLAR = [
    ("onarılan VERI'ye yazılmıyor", "VERI[s] = yeni; degisen += 1", "degisen += 1"),
    ("pkl kaydedilmiyor", "if degisen and kaydet:", "if False and degisen and kaydet:"),
    ("onarılmayan da onarılmış sayılıyor", 'on = [r for r in kayit if r["onarildi"]]', "on = list(kayit)"),
    ("dokunulmayan sayılmıyor", "dokunulmayan += len(kayit) - len(on)", "dokunulmayan += 0"),
    ("yamalı metin tekrar yamalanıyor", "if VK_ISARET in metin:", "if False:"),
    ("çift çapa geçiyor", "if n != 1:", "if n < 1:"),
    ("son bar sayımı ters", "if v[0] == v[2])", "if v[0] != v[2])"),
    ("yukarı sıçrama görülmüyor", "((r <= VK_SICRAMA_ALT) | (r >= VK_SICRAMA_UST))", "(r <= VK_SICRAMA_ALT)"),
    ("B2 eski son bar yerine ilk bar", "str(eski.index[-1].date()))\\n", "str(eski.index[0].date()))\\n"),
    ("veri_koru çağrılmıyor", "; VK = veri_koru(K, VERI, B2_NEDEN)\\n", "; VK = {}\\n"),
    ("B2 farkı yanlış barda", "_i=int(np.nanargmax(", "_i=int(np.nanargmin("),
    ("açılış oranı yerine her şey onarılıyor", "            if not ol:\n                continue\n", "            if not ol:\n                ol = [(1, 0.5)]\n"),
]


def kos(ns, sessiz=False):
    hata = []
    for t in TESTLER:
        try:
            t(ns)
        except Exception as e:
            hata.append((t.__name__, e))
            if not sessiz:
                print(f"  ✗ {t.__name__}: {e}"); traceback.print_exc()
        else:
            if not sessiz:
                print(f"  ✓ {t.__name__}")
    return hata


if __name__ == "__main__":
    logging.disable(logging.WARNING)
    if "--mutasyon" in sys.argv:
        kacan = []
        for ad, eski, yeni in MUTASYONLAR:
            assert eski in KAYNAK, f"mutasyon hedefi yok: {ad}"
            try:
                ns = yukle(KAYNAK.replace(eski, yeni, 1))
            except Exception:
                print(f"  ✓ yakalandı (yükleme): {ad}"); continue
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                h = kos(ns, sessiz=True)
            print(f"  {'✓ yakalandı' if h else '✗ KAÇTI'}: {ad}" + (f" ← {h[0][0]}" if h else ""))
            if not h:
                kacan.append(ad)
        print(f"\n{len(MUTASYONLAR) - len(kacan)}/{len(MUTASYONLAR)} mutasyon yakalandı"); sys.exit(1 if kacan else 0)
    ns = yukle()
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        h = kos(ns, sessiz=True)
    for t in TESTLER:
        print(f"  {'✗' if any(x[0] == t.__name__ for x in h) else '✓'} {t.__name__}" + "".join(f": {e}" for n, e in h if n == t.__name__))
    print(f"\n{len(TESTLER) - len(h)}/{len(TESTLER)} test geçti"); sys.exit(1 if h else 0)
