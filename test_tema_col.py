# test_tema_col.py — sahte col_tarayici klasörü: COL_v1 / OLCUM / DESEN_TAM'ın ilgili kısımları (Drive'daki kaynaktan
# birebir yeniden kurulmuş) + sentetik önbellek + sentetik fon fiyatları. Sınananlar:
# (1) yükleyici DESEN_TAM'dan YALNIZ islemler_olc + 5 yardımcıyı alıyor, ilk tanımı seçiyor, oturumu ezmiyor
# (2) ADIM 0 kapısı: doğru sayıda geçer, yanlış sayıda DURUR ve Adım 1–2 çalışmaz
# (3) ilk dalga tanımı elle kurulmuş seride tam doğru gün · geleceğe bakmıyor · "sonrası" 120 gün / SMA200 kuralı
# (4) eşleme: endüstri → tema fonu, sektör yedeği, eşlenemeyen dışarıda
# (5) KARAR: ekilmiş etki (iki sette) GEÇTİ · plasebo GEÇMEDİ · tek sette etki GEÇMEDİ · ters etki GEÇMEDİ · küçük dilim GEÇMEDİ
# (6) uçtan uca: dosyalar, grafik, damga · (7) çakışma kapısı
import os, io, sys, types, pickle, tempfile, textwrap, json
from contextlib import redirect_stdout, redirect_stderr
import numpy as np, pandas as pd
D0 = os.path.dirname(os.path.abspath(__file__))
HATA = []
def chk(ad, k, ek=""):
    print(f"  [{'OK' if k else 'HATA'}] {ad} {ek}"); (not k) and HATA.append(ad)

def modul_yukle(yol, ad):
    m = types.ModuleType(ad); m.__file__ = yol; sys.modules[ad] = m
    with redirect_stdout(io.StringIO()):
        exec(compile(open(yol).read(), yol, "exec"), m.__dict__)
    return m

# --------------------------------------------------------------- sahte col_tarayici (Drive kaynağından yeniden kuruldu)
COL_V1 = textwrap.dedent('''
    import numpy as np, pandas as pd
    AL_PAY = 1.002
    DOJI_ESIK = 0.15
    def gecerli_bar_maskesi(O, H, L, C, V):
        O,H,L,C,V = (np.asarray(a,float) for a in (O,H,L,C,V))
        m = np.isfinite(O)&np.isfinite(H)&np.isfinite(L)&np.isfinite(C)&(H>L)
        m &= np.where(np.isfinite(V), V>0, True)
        return m
    def carpanlar_hesapla(olcu, cds_pct=np.nan, borc_oz=np.nan, oz_negatif=0, kural=1):
        return 6.0, {}
    def bek(v):
        v=pd.Series(v,dtype=float).dropna()
        if not len(v): return np.nan
        kz=v[v>0].mean() if (v>0).any() else 0.0; ky=v[v<=0].mean() if (v<=0).any() else 0.0
        return float((v>0).mean()*kz+(v<=0).mean()*ky)
    def cds_yukle(dosya=None): return None
    def _bant(*a, **k): return None
''')
OLCUM = textwrap.dedent('''
    from dataclasses import dataclass
    import numpy as np, pandas as pd
    @dataclass
    class OlcumCfg:
        boot_tekrar: int = 1000
        guven_alt: float = 5.0
        guven_ust: float = 95.0
        min_islem: int = 30
        tohum: int = 20260923
    ocfg = OlcumCfg()
    def _olc_g(ad, vars_=None): return globals().get(ad, vars_)
    def _rng(ek=0): return np.random.default_rng(ocfg.tohum + int(ek))
    def _olc_bek(v):
        f = _olc_g('bek')
        if f is not None:
            try:
                r = float(f(v))
                if np.isfinite(r): return r
            except Exception: pass
        v = pd.Series(v).dropna().astype(float)
        if not len(v): return np.nan
        k = v[v > 0]; z = v[v <= 0]; p = len(k) / len(v)
        return p * (k.mean() if len(k) else 0.0) + (1 - p) * (z.mean() if len(z) else 0.0)
    def _olc_bant(V, anahtarlar=None):
        if not V: return {}
        df = pd.DataFrame(V); anahtarlar = anahtarlar or list(df.columns); out = {}
        for k in anahtarlar:
            if k not in df: continue
            s = pd.to_numeric(df[k], errors='coerce')
            if s.notna().sum() == 0: continue
            out[k] = (float(np.nanmedian(s)), float(np.nanpercentile(s, ocfg.guven_alt)), float(np.nanpercentile(s, ocfg.guven_ust)))
        return out
    def _gercek(b3):
        if not b3: return False
        _, lo, hi = b3
        return bool(np.isfinite(lo) and np.isfinite(hi) and (lo > 0 or hi < 0))
    def olculer(t):
        if t is None or not len(t): return {'n': 0}
        v = pd.to_numeric(t['getiri'], errors='coerce')
        e = pd.to_numeric(t['endeks'], errors='coerce') if 'endeks' in t else pd.Series(np.nan, index=t.index)
        f = (v - e).dropna()
        return {'n': int(len(v)), 'bek': _olc_bek(v), 'kazanan%': float(100 * (v > 0).mean()),
                'ort': float(v.mean()), 'medyan': float(v.median()), 'agir%': float(100 * (v < -20).mean()),
                'endeks_ustu': float(f.mean()) if len(f) else np.nan,
                'bar': float(pd.to_numeric(t['bar'], errors='coerce').median()) if 'bar' in t else np.nan}
    OLCU_ANAHTAR = ('bek', 'kazanan%', 'ort', 'agir%', 'endeks_ustu')
    def _gun_gruplari(t):
        g = pd.to_datetime(t['giris_t']).dt.normalize().values; gruplar = {}
        for pos, k in enumerate(g): gruplar.setdefault(k, []).append(pos)
        return np.array(list(gruplar.keys())), {k: np.asarray(v) for k, v in gruplar.items()}
    def bootstrap(t, maske=None, n=None, tohum_ek=0):
        n = ocfg.boot_tekrar if n is None else n
        if t is None or len(t) < 5: return {}
        anahtar, gruplar = _gun_gruplari(t); rng = _rng(tohum_ek)
        m = None if maske is None else np.asarray(pd.Series(maske).values, dtype=bool)
        A, B, D = [], [], []
        for _ in range(n):
            sec = rng.choice(len(anahtar), size=len(anahtar), replace=True)
            pos = np.concatenate([gruplar[anahtar[s]] for s in sec]); alt = t.iloc[pos]
            if m is None: A.append(olculer(alt)); continue
            mm = m[pos]; a, b = olculer(alt[~mm]), olculer(alt[mm])
            if a.get('n', 0) >= 5 and b.get('n', 0) >= 5:
                A.append(a); B.append(b); D.append({k: b.get(k, np.nan) - a.get(k, np.nan) for k in OLCU_ANAHTAR})
        r = {'a': _olc_bant(A, OLCU_ANAHTAR)}
        if m is not None: r['b'] = _olc_bant(B, OLCU_ANAHTAR); r['fark'] = _olc_bant(D, OLCU_ANAHTAR)
        return r
    def kiyas(t, maske, ad_a='A', ad_b='B', n=None, yaz=True):
        if t is None or t.empty: return {}
        m = pd.Series(np.asarray(maske, dtype=bool), index=t.index)
        oa, ob = olculer(t[~m]), olculer(t[m])
        if min(oa.get('n', 0), ob.get('n', 0)) < ocfg.min_islem:
            return {'olcu_a': oa, 'olcu_b': ob, 'yetersiz': True}
        r = bootstrap(t, maske=m.values, n=n); fb = r.get('fark', {})
        r.update({'olcu_a': oa, 'olcu_b': ob, 'bek_gercek': _gercek(fb.get('bek')), 'eu_gercek': _gercek(fb.get('endeks_ustu'))})
        return r
''')
DESEN = textwrap.dedent('''
    # sahte DESEN_TAM: gömülü çekirdek başta; sonra DESEN'in kendi (yüklenmemesi gereken) şeyleri
    from __future__ import annotations
    import logging, numpy as np, pandas as pd
    dlog = logging.getLogger('col.denetim_olc')
    _HATA_OLC = []
    def kirilim_bul_olc(o, en_gec=60, pay=None):
        pay=AL_PAY if pay is None else pay
        C=o['iC']; tv=float(o['seg']['tavan'])*pay
        for j in range(min(en_gec,len(C))):
            if C[j]>tv: return j
        return None
    def pnl_olc(o, kb, gp, ufuk=250, hedef=20, maliyet=0.4):
        C,H,s20=o['iC'],o['iH'],o['s20']; son_i=min(kb+ufuk,len(C)-1)
        m=H[kb+1:son_i+1]>=gp*(1+hedef/100)
        if m.any():
            jh=int(np.argmax(m))+kb+1; alt=np.where(C[jh+1:]<s20[jh+1:])[0]; jt=int(alt[0])+jh+1 if len(alt) else len(C)-1
            hv=True
        else: jt=son_i; hv=False
        return (C[jt]/gp-1)*100-maliyet, jt, hv
    def _olcu_olc(o):
        s=dict(o['seg']); s.setdefault('dar',np.nan); return s
    def _endeks_getiri_olc(xu, t1, t2):
        return np.nan
    def islemler_olc(OB, giris='kapanis', tekil=True, ufuk=120, hedef=20, maliyet=0.4, xu=None, cds=None, temel=True, en_gec=60):
        R=[]; _HATA_OLC.clear()
        for i,o in enumerate(OB):
            try:
                kb=kirilim_bul_olc(o,en_gec)
                if kb is None: continue
                iT=pd.to_datetime(o['iT']); C=o['iC']; O_=o['iO']
                if giris=='acilis':
                    if kb+1>=len(C): continue
                    gp=float(O_[kb+1]); kb_e=kb+1
                else: gp=float(C[kb]); kb_e=kb
                g,jt,hv=pnl_olc(o,kb_e,gp,ufuk=ufuk,hedef=hedef,maliyet=maliyet)
                if giris=='acilis':
                    if jt+1<len(C): cp=float(O_[jt+1]); jt_e=jt+1
                    else: cp=float(C[jt]); jt_e=jt
                    g=(cp/gp-1)*100-maliyet
                else: cp=float(C[jt]); jt_e=jt
                s=_olcu_olc(o); kt=iT[kb]; gt=iT[kb_e]; ct=iT[jt_e]
                poz,cc_=carpanlar_hesapla(s,np.nan,np.nan,0,1)
                R.append({'i':i,'sembol':o['sembol'],'sinyal':pd.Timestamp(o['tarih']),'kirilim':kt,'giris_t':gt,'giris':gp,'cikis_t':ct,'cikis':cp,
                          'getiri':g,'bar':jt_e-kb_e+1,'hedef':hv,'kb':kb_e,'jt':jt_e,'poz':poz,'endeks':np.nan})
            except Exception as e:
                _HATA_OLC.append(f'{i}: {e}')
        t=pd.DataFrame(R)
        if t.empty: return t
        t=t.sort_values(['sembol','kirilim','sinyal'],kind='stable')
        t['tekrar']=t.duplicated(['sembol','kirilim'],keep='first')
        if tekil: t=t[~t.tekrar]
        return t.sort_values('giris_t',kind='stable').reset_index(drop=True)
    DESEN_YUKLENDI = True          # bu satır yüklenmemeli
    def desen(o): return None      # yüklenmemeli
    def islemler_olc(*a, **k):     # İKİNCİ tanım — ilk seçilmeli
        raise RuntimeError("ikinci tanım yüklendi")
''')

# Colab taze oturum koşulu: COL_v1 ve OLCUM ikisi de özel '_h' (günlükçü) tanımlar; OLCUM'un KENDİ çakışma kapısı vardır.
COL_V1 += '_h = "COL günlükçüsü"\n'
OLCUM = "_CK_ONCE = {k: id(v) for k, v in globals().items()}\n" + OLCUM + textwrap.dedent('''
    _h = "OLCUM günlükçüsü"
    def _cakisma_kontrol(_once=_CK_ONCE, _dosya='OLCUM.py'):
        g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
        atla = ('_CK_ONCE', '_CK_KAYIT', '_cakisma_kontrol')
        degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla]
        ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya)
        for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
        if ezilen:
            raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}. Üretim modülü bozulmuş olabilir")
    _cakisma_kontrol()
''')

FONLAR = sorted({"SMH", "IGV", "XOP", "XLE", "ITA", "XBI", "IHI", "KRE", "XHB", "XME", "GDX", "TAN", "URA",
                 "XLK", "XLF", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC", "SPY"})
IX = pd.bdate_range("2019-01-01", "2026-09-25")

def fon_fiyat(dalgali=("SMH",), r=np.random.default_rng(1)):
    """Sakin fonlar (SPY ile aynı, küçük gürültü) + 'dalgali' fonlarda 2022-03 ve 2024-06'da +%25 dalga."""
    spy = 100 * np.exp(np.cumsum(r.normal(0.0003, 0.008, len(IX))))
    P = {"SPY": spy}
    for f in FONLAR:
        if f == "SPY": continue
        x = spy * np.exp(np.cumsum(r.normal(0, 0.002, len(IX))))
        if f in dalgali:
            for bas in ("2022-03-01", "2024-06-03"):
                i = IX.searchsorted(pd.Timestamp(bas)); x = x.copy()
                x[i:i + 40] *= np.linspace(1, 1.25, 40); x[i + 40:] *= 1.25
        P[f] = x
    return pd.DataFrame(P, index=IX)

def ob_kayit(sembol, sinyal, getiri_hedef, r):
    """Sinyal günü T; T+1'de kırılım (kapanış > tavan×1.002), ertesi açılış giriş; sonra yol: getiri_hedef'e ulaşan düz yol."""
    iT = pd.bdate_range(pd.Timestamp(sinyal) + pd.offsets.BDay(1), periods=160)
    tavan = 10.0; C = np.full(160, 9.9); C[0] = 10.1                       # kb = 0
    son = 10.1 * (1 + getiri_hedef / 100)
    C[1:] = np.linspace(10.1, son, 159) * (1 + r.normal(0, 0.0005, 159))
    O = np.r_[C[0], C[:-1]]; H = np.maximum(O, C) * 1.001
    s20 = C * 0.5                                                          # trail tetiklenmez: getiri yol sonuna kadar taşınır
    return {"sembol": sembol, "tarih": pd.Timestamp(sinyal), "GECER": True,
            "seg": {"tavan": tavan, "atr_ref": 0.2, "gecerli_oran": 1.0, "doji": 0.2, "alt_fitil": 0.1, "dar": 0.5},
            "iT": iT.to_numpy(), "iO": O, "iH": H, "iC": C, "s20": s20}

def klasor_kur(td, tema_etki, tohum, sadece_bir_set=False, ters=False, n=160):
    """İki set; semboller: T* (SMH'ye eşlenir = tema), N* (XLP'ye = sakin), U* (eşlenemez). Tema etkisi: getiri + etki."""
    r = np.random.default_rng(tohum)
    for ad in ("arsiv/desen",):
        os.makedirs(os.path.join(td, ad), exist_ok=True)
    open(os.path.join(td, "COL_v1.py"), "w").write(COL_V1)
    open(os.path.join(td, "OLCUM.py"), "w").write(OLCUM)
    open(os.path.join(td, "arsiv/desen/DESEN_TAM.py"), "w").write(DESEN)
    H = []
    setler = {}
    P = fon_fiyat()
    D, S, _ = TC["tc_dalga"](P)
    for k, (ad, bas, bit) in enumerate((("ABD 2024-26", "2024-01-02", "2026-03-01"), ("ABD 2022-23", "2022-01-03", "2023-10-01"))):
        OB = []
        gunler = pd.bdate_range(bas, bit)
        for j in range(n):
            tip = "T" if j % 2 == 0 else "N"
            if j % 17 == 0: tip = "U"
            s = f"{tip}{k}{j:03d}.AM"
            g0 = gunler[r.integers(0, len(gunler) - 1)]
            kir = g0 + pd.offsets.BDay(1)
            tema = bool(S["SMH"].asof(kir)) if tip == "T" else False
            etki = tema_etki if (tema and not (sadece_bir_set and k == 1)) else 0.0
            if ters: etki = -etki
            gt = float(r.normal(6, 12) + etki)
            OB.append(ob_kayit(s, g0, gt, r))
            H.append({"sembol": s, "sektor": "Technology" if tip == "T" else ("Consumer Defensive" if tip == "N" else "BILINMIYOR"),
                      "endustri": "Semiconductors" if tip == "T" else ("Grocery Stores" if tip == "N" else "BILINMIYOR")})
        setler[ad] = OB
        pickle.dump(OB, open(os.path.join(td, TC["TC_TABAN"][ad]["dosya"]), "wb"))
    pd.DataFrame(H).drop_duplicates("sembol").to_csv(os.path.join(td, "sektor_ABD.csv"), index=False)
    return setler, P

TCm = modul_yukle(os.path.join(D0, "tema_col.py"), "tema_col_test"); TC = TCm.__dict__

print("T1 yükleyici")
with tempfile.TemporaryDirectory() as td:
    klasor_kur(td, 0, 1)
    ns = TC["tc_yukle"](td)
    chk("islemler_olc + yardımcılar yüklendi", all(a in ns for a in TC["TC_OLC_ADLAR"]))
    chk("DESEN'in geri kalanı YÜKLENMEDİ", "DESEN_YUKLENDI" not in ns and "desen" not in ns)
    chk("İLK tanım seçildi (ikinci tanım hata fırlatırdı)", isinstance(TC["tc_islemler"](ns, []), pd.DataFrame))
    chk("OLCUM.kiyas ve COL.bek aynı ad alanında", "kiyas" in ns and "bek" in ns)
    chk("oturum ezilmedi (kiyas/islemler_olc test globallerinde yok)", "kiyas" not in TC and "islemler_olc" not in TC)
    chk("kaynak md5 damgası", len(ns["_tc_kaynak"]["olc_md5"]) == 32)
    g_ = {"__name__": "eski_yontem"}
    try:
        with redirect_stdout(io.StringIO()):
            exec(COL_V1, g_); exec(OLCUM, g_)
        chk("sahte dünya Colab hatasını birebir üretir (eski yöntem: aynı ad alanı -> '_h' EZDİ)", False)
    except RuntimeError as e:
        chk("sahte dünya Colab hatasını birebir üretir (eski yöntem: aynı ad alanı -> '_h' EZDİ)", "'_h'" in str(e), str(e)[:70])
    chk("yeni yükleyici: OLCUM kendi kapısıyla temiz yüklendi, COL'un _h'si korunur, kiyas COL.bek'i görür",
        ns["_h"] == "COL günlükçüsü" and ns["kiyas"].__globals__["_h"] == "OLCUM günlükçüsü" and ns["kiyas"].__globals__["bek"] is ns["bek"])

print("T2 ADIM 0 kapısı")
with tempfile.TemporaryDirectory() as td:
    setler, P = klasor_kur(td, 0, 2)
    ns = TC["tc_yukle"](td)
    gercek = {ad: {"kazanan": 100 * float((TC["tc_islemler"](ns, OB)["getiri"] > 0).mean()),
                   "bek": float(ns["bek"](TC["tc_islemler"](ns, OB)["getiri"]))} for ad, OB in setler.items()}
    A0 = TC["tc_adim0"](ns, setler, gercek)
    chk("doğru sayılar -> GEÇTİ", A0["gecti"], str({k: (round(v['kazanan'], 1), round(v['bek'], 2)) for k, v in A0['setler'].items()}))
    yanlis = {k: {"kazanan": v["kazanan"] + 3, "bek": v["bek"]} for k, v in gercek.items()}
    chk("kazanan 3 puan farklı -> GEÇMEDİ", not TC["tc_adim0"](ns, setler, yanlis)["gecti"])
    yanlis = {k: {"kazanan": v["kazanan"], "bek": v["bek"] + 0.3} for k, v in gercek.items()}
    chk("bek 0.3 farklı -> GEÇMEDİ", not TC["tc_adim0"](ns, setler, yanlis)["gecti"])
    with redirect_stdout(io.StringIO()) as b, redirect_stderr(io.StringIO()):
        R = TC["tema_col"](K=td, ns=ns, setler=setler, P=P, beklenen=yanlis, yfinance_ile=False, n_boot=200)
    chk("ADIM 0 geçmezse DURUR: Adım 1–2 yok, grafik/CSV yok", "DURULDU" in R["ozet"] and "ADIM 1" not in R["ozet"]
        and not os.path.exists(os.path.join(td, "tema_dalga.png")) and not os.path.exists(os.path.join(td, "tema_col_islemler.csv")))
    chk("damga yine yazıldı", os.path.exists(os.path.join(td, "tema_col.json")))

print("T3 ilk dalga tanımı")
ix = pd.bdate_range("2020-01-01", periods=500)
spy = pd.Series(100.0, index=ix)
f = pd.Series(100.0, index=ix); f.iloc[300:340] = np.linspace(100, 125, 40); f.iloc[340:] = 125
Pt = pd.DataFrame({"SPY": spy, "SMH": f})
Dt, St, Ut = TC["tc_dalga"](Pt)
ilk = Dt.index[Dt["SMH"]].min()
# 60 günlük getiri ≥ %15 ilk nerede? 100→ linspace: bağımsız hesap
beklenen_ilk = next(ix[i] for i in range(60, 500) if f.iloc[i] / f.iloc[i - 60] - 1 >= 0.15 and f.iloc[i] > f.iloc[i - 199:i + 1].mean())
chk("ilk dalga günü bağımsız hesapla aynı", ilk == beklenen_ilk, f"{ilk.date()} vs {beklenen_ilk.date()}")
Dk, Sk, _ = TC["tc_dalga"](Pt.iloc[:ix.get_loc(ilk) + 1])
chk("geleceğe bakmıyor: seri o günde kesilince de aynı gün dalga", bool(Dk["SMH"].iloc[-1]) and not Dk["SMH"].iloc[:-1].any())
son_dalga = Dt.index[Dt["SMH"]].max(); i_son = ix.get_loc(son_dalga)
chk("son dalga gününden 119 gün sonra 'sonrası' DOĞRU", bool(St["SMH"].iloc[i_son + 119]))
chk("120. gün 'sonrası' YANLIŞ", not bool(St["SMH"].iloc[i_son + 120]))
f2 = f.copy(); f2.iloc[i_son + 30:] = 90
St2 = TC["tc_dalga"](pd.DataFrame({"SPY": spy, "SMH": f2}))[1]
chk("SMA200 altına inince 'sonrası' YANLIŞ", not bool(St2["SMH"].iloc[i_son + 60]))
spy2 = spy.copy(); spy2.iloc[300:340] = np.linspace(100, 120, 40); spy2.iloc[340:] = 120
chk("SPY de aynı yükselince (fark < 10 puan) dalga YOK", not TC["tc_dalga"](pd.DataFrame({"SPY": spy2, "SMH": f}))[0]["SMH"].any())

print("T4 eşleme")
with tempfile.TemporaryDirectory() as td:
    pd.DataFrame([{"sembol": "AAA.AM", "sektor": "Technology", "endustri": "Semiconductors"},
                  {"sembol": "BBB.AM", "sektor": "Technology", "endustri": "Consumer Electronics"},
                  {"sembol": "CCC.AM", "sektor": "Energy", "endustri": "Oil & Gas E&P"},
                  {"sembol": "DDD.AM", "sektor": "BILINMIYOR", "endustri": "BILINMIYOR"}]).to_csv(os.path.join(td, "sektor_ABD.csv"), index=False)
    H = TC["tc_harita"](td, ["AAA.AM", "BBB", "CCC.AM", "DDD.AM", "EEE.AM"], yfinance_ile=False)
    chk("yarı iletken -> SMH (endüstri)", H.loc["AAA", "fon"] == "SMH" and H.loc["AAA", "kaynak"] == "endüstri")
    chk("tüketici elektroniği -> XLK (sektör yedeği)", H.loc["BBB", "fon"] == "XLK" and H.loc["BBB", "kaynak"] == "sektör")
    chk("petrol arama -> XOP", H.loc["CCC", "fon"] == "XOP")
    chk("bilinmeyen -> fon yok (None, NaN değil)", H.loc["DDD", "fon"] is None and H.loc["DDD", "kaynak"] == "yok")
    t = pd.DataFrame({"sembol": ["AAA.AM", "DDD.AM", "EEE.AM"], "kirilim": pd.to_datetime(["2022-05-02"] * 3), "getiri": [1.0, 2, 3]})
    S_ = pd.DataFrame({"SMH": [True]}, index=pd.to_datetime(["2022-04-29"]))
    te = TC["tc_etiketle"](t, H, S_)
    chk("eşlenemeyen (DDD, EEE) tema=boş (dışarıda); AAA asof doğru", te["tema"].tolist()[0] is True and te["tema"].iloc[1:].isna().all(), str(te["tema"].tolist()))

print("T5 KARAR mantığı (sentetik işlem tabloları, gerçek kiyas/bootstrap)")
with tempfile.TemporaryDirectory() as td:
    klasor_kur(td, 0, 3); ns = TC["tc_yukle"](td)
def tablo(etki_t, etki_b=0.0, n=600, tohum=0, pay=0.35, dar=False):
    r = np.random.default_rng(tohum); g = pd.bdate_range("2022-01-03", periods=400)
    tema = r.random(n) < pay; gir = g[r.integers(0, len(g), n)]
    get = r.normal(6, 14, n) + np.where(tema, etki_t, 0)
    if dar:                                   # tema ortalaması yüksek ama kuyruğu İNCE: ≥30 neredeyse yok
        get = np.where(tema, r.normal(6 + etki_t, 4, n), get)
    get = np.where(tema & (r.random(n) < etki_b), get + 35, get)
    t = pd.DataFrame({"giris_t": gir, "getiri": get, "tema": tema, "endeks": np.nan})
    t["buyuk"] = t["getiri"] >= 30; return t
KR = TC["tc_karar"](ns, {"A": tablo(8, 0.25, tohum=1), "B": tablo(8, 0.25, tohum=2)}, n_boot=300)
chk("ekilmiş etki iki sette -> GEÇTİ", KR["gecti"], str(KR["neden"]))
KR = TC["tc_karar"](ns, {"A": tablo(0, 0, tohum=3), "B": tablo(0, 0, tohum=4)}, n_boot=300)
chk("plasebo -> GEÇMEDİ", not KR["gecti"], str(KR["neden"][:2]))
KR = TC["tc_karar"](ns, {"A": tablo(8, 0.25, tohum=5), "B": tablo(0, 0, tohum=6)}, n_boot=300)
chk("yalnız bir sette etki -> GEÇMEDİ, neden B'yi söylüyor", not KR["gecti"] and any(n_.startswith("B:") for n_ in KR["neden"]), str(KR["neden"]))
KR = TC["tc_karar"](ns, {"A": tablo(-8, 0, tohum=7), "B": tablo(-8, 0, tohum=8)}, n_boot=300)
chk("ters etki -> GEÇMEDİ, 'TERS' yazıyor", not KR["gecti"] and any("TERS" in n_ for n_ in KR["neden"]), str(KR["neden"][:2]))
KR = TC["tc_karar"](ns, {"A": tablo(8, 0.25, tohum=9, n=60, pay=0.2), "B": tablo(8, 0.25, tohum=10)}, n_boot=300)
chk("küçük dilim -> GEÇMEDİ (karar verilemez)", not KR["gecti"] and any("karar verilemez" in n_ for n_ in KR["neden"]), str(KR["neden"][:2]))
KR = TC["tc_karar"](ns, {"A": tablo(1.0, 0.0, tohum=15), "B": tablo(8, 0.25, tohum=16)}, n_boot=300)
fA = KR["setler"]["A"]["bek_fark"]
chk("zayıf etki: orta > 0 ama alt bant ≤ 0 -> GEÇMEDİ (alt banda bakılıyor)", fA[0] > 0 >= fA[1] and not KR["setler"]["A"]["sart1"] and not KR["gecti"], f"A bant {fA}")
KR = TC["tc_karar"](ns, {"A": tablo(8, 0.0, tohum=11, dar=True), "B": tablo(8, 0.0, tohum=12, dar=True)}, n_boot=300)
chk("beklenti iyi ama büyük kazanan artmıyor -> GEÇMEDİ (şart 2)", not KR["gecti"] and any("büyük kazanan" in n_ for n_ in KR["neden"]),
    str([round(s["buyuk_oran"], 2) for s in KR["setler"].values()]))

def tablo_az(tohum):                            # gerisinde hiç büyük kazanan yok, temada yalnız 2 → oran ∞ ama n az
    t = tablo(8, 0, tohum=tohum); t["getiri"] = t["getiri"].clip(upper=29)
    i = t.index[t["tema"]][:2]; t.loc[i, "getiri"] = 60; t["buyuk"] = t["getiri"] >= 30; return t
KR = TC["tc_karar"](ns, {"A": tablo_az(13), "B": tablo_az(14)}, n_boot=300)
chk("oran ∞ ama temada 2 büyük kazanan -> şart 2 GEÇMEDİ", not KR["gecti"] and not KR["setler"]["A"]["sart2"] and any("tesadüf" in n_ for n_ in KR["neden"]))

print("T6 uçtan uca (sentetik önbellek + fon, ağsız)")
with tempfile.TemporaryDirectory() as td:
    setler, P = klasor_kur(td, 20, 13, n=400)
    ns = TC["tc_yukle"](td)
    gercek = {ad: {"kazanan": 100 * float((TC["tc_islemler"](ns, OB)["getiri"] > 0).mean()),
                   "bek": float(ns["bek"](TC["tc_islemler"](ns, OB)["getiri"]))} for ad, OB in setler.items()}
    with redirect_stdout(io.StringIO()) as b, redirect_stderr(io.StringIO()):
        R = TC["tema_col"](K=td, ns=ns, setler=setler, P=P, beklenen=gercek, yfinance_ile=False, n_boot=200)
    out = R["ozet"]
    chk("ADIM 0/1/2 raporda", all(x in out for x in ("ADIM 0 GEÇTİ", "ADIM 1", "ADIM 2", "KARAR:")))
    chk("dosyalar", all(os.path.exists(os.path.join(td, f)) for f in ("tema_col.txt", "tema_col.json", "tema_col_islemler.csv", "tema_dalga.csv", "tema_dalga.png")))
    T6 = pd.read_csv(os.path.join(td, "tema_col_islemler.csv"))
    chk("eşlenemeyen U* hisseleri dışarıda (tema boş)", T6[T6.sembol.str.startswith("U")]["tema"].isna().all() and len(T6[T6.sembol.str.startswith("U")]) > 0)
    chk("N* (sakin fon) hiç 'tema' değil", not T6[T6.sembol.str.startswith("N")]["tema"].fillna(False).astype(bool).any())
    chk("T* içinde tema=True olanlar var", T6[T6.sembol.str.startswith("T")]["tema"].fillna(False).astype(bool).sum() > 20)
    J = json.load(open(os.path.join(td, "tema_col.json")))
    chk("damga: tanım sürümü + kaynak md5 + karar", J["tanim"]["surum"] == "v1" and len(J["kaynak"]["olc_md5"]) == 32 and J["karar"] in ("GEÇTİ", "GEÇMEDİ"))
    chk("ekilmiş +20 tema etkisiyle KARAR GEÇTİ", J["karar"] == "GEÇTİ", str(J.get("neden")))

print("T6b uçtan uca plasebo (tema etkisi 0, 3 tohum)")
kararlar = []
for toh in (21, 22, 23):
    with tempfile.TemporaryDirectory() as td:
        setler, P = klasor_kur(td, 0, toh, n=400); ns = TC["tc_yukle"](td)
        gercek = {ad: {"kazanan": 100 * float((TC["tc_islemler"](ns, OB)["getiri"] > 0).mean()),
                       "bek": float(ns["bek"](TC["tc_islemler"](ns, OB)["getiri"]))} for ad, OB in setler.items()}
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            TC["tema_col"](K=td, ns=ns, setler=setler, P=P, beklenen=gercek, yfinance_ile=False, n_boot=200)
        kararlar.append(json.load(open(os.path.join(td, "tema_col.json")))["karar"])
chk("plasebo: 3 dünyada da GEÇMEDİ", all(k == "GEÇMEDİ" for k in kararlar), str(kararlar))

print("T7 çakışma kapısı")
try:
    with redirect_stdout(io.StringIO()):
        exec(open(os.path.join(D0, "tema_col.py")).read(), TCm.__dict__)
    chk("yeniden yükleme", True)
except RuntimeError as e:
    chk("yeniden yükleme", False, str(e))
print(f"\n{'=' * 60}\n  SONUÇ: {len(HATA)} hata" + (f" -> {HATA}" if HATA else "  — hepsi geçti"))
